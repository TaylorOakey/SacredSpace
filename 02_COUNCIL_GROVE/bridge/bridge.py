#!/usr/bin/env python3
"""bridge.py — SacredSpace git bridge between agents (cloud Claude <-> local OpenCode).

Pillar 02 · COUNCIL_GROVE. Stdlib only, no build tools, no secrets.

Design: git is the transport, so every artifact is append-only and one-file-per-
event. Messages are immutable files in msgs/; an ack is a new file in acks/.
Two agents writing at once therefore never produce a merge conflict.

  bridge.py send  --to opencode --title "..." [--body "..."|-] [--re ID] [--push]
  bridge.py inbox [--as NAME] [--all]
  bridge.py read  ID
  bridge.py ack   ID [--note "..."] [--push]
  bridge.py lease acquire|release|check|list [PATH|GLOB ...] [--ttl MIN] [--note ..] [--push]
  bridge.py sync                      # fetch, rebase, push (retries on network error)
  bridge.py status
  bridge.py handoff [--task ..] [--done ..] [--next ..] [--to AGENT]

Identity: --as NAME, else $BRIDGE_AGENT, else "claude".
Branch:   --branch NAME, else $BRIDGE_BRANCH, else the current branch.
"""
import argparse, fnmatch, hashlib, os, re, subprocess, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
MSGS, ACKS, LEASES = HERE / "msgs", HERE / "acks", HERE / "leases"
HANDOFF = HERE.parent / "LATEST_HANDOFF.md"


def git(*args, check=True, cwd=None):
    r = subprocess.run(["git", *args], cwd=cwd or HERE, capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr.strip()}")
    return r.stdout.strip()


def root():
    return Path(git("rev-parse", "--show-toplevel"))


def branch(args):
    return args.branch or os.environ.get("BRIDGE_BRANCH") or git("branch", "--show-current")


def me(args):
    return (args.who or os.environ.get("BRIDGE_AGENT") or "claude").lower()


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40] or "msg"


def parse(path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---\n"):
        head, _, body = text[4:].partition("\n---\n")
        for line in head.splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
    meta["id"] = path.stem
    return meta, body.strip()


def messages():
    return [parse(p) for p in sorted(MSGS.glob("*.md"))]


def acked(mid):
    return {p.name.split(".")[-2] for p in ACKS.glob(f"{mid}.*.ack")}


def commit(paths, msg):
    r = root()
    git("add", "--", *[str(p) for p in paths], cwd=r)
    git("commit", "-m", msg, "--only", "--", *[str(p) for p in paths], cwd=r)


def sync(args, quiet=False):
    b = branch(args)
    for i, wait in enumerate((0, 2, 4, 8, 16)):
        time.sleep(wait)
        f = subprocess.run(["git", "fetch", "origin", b], cwd=HERE, capture_output=True, text=True)
        if f.returncode == 0 or "couldn't find remote ref" in f.stderr:
            break
    else:
        sys.exit("fetch failed after retries:\n" + f.stderr)
    remote_exists = subprocess.run(["git", "rev-parse", "--verify", f"origin/{b}"], cwd=HERE,
                                   capture_output=True).returncode == 0
    if remote_exists:
        git("pull", "--rebase", "--autostash", "origin", b)
    for wait in (0, 2, 4, 8, 16):
        time.sleep(wait)
        p = subprocess.run(["git", "push", "-u", "origin", b], cwd=HERE, capture_output=True, text=True)
        if p.returncode == 0:
            if not quiet:
                print(f"synced {b}", file=sys.stderr)
            return
        if "rejected" in p.stderr:  # raced with the other agent: re-rebase, retry
            git("pull", "--rebase", "--autostash", "origin", b)
    sys.exit("push failed after retries:\n" + p.stderr)


def cmd_send(a):
    body = sys.stdin.read() if a.body == "-" else (a.body or "")
    now = datetime.now(timezone.utc)
    mid = f"{now:%Y%m%dT%H%M%SZ}-{me(a)}-{slug(a.title)}"
    head = [f"from: {me(a)}", f"to: {a.to.lower()}", f"title: {a.title}",
            f"created: {now:%Y-%m-%dT%H:%M:%SZ}", f"branch: {branch(a)}"]
    if a.re:
        head.append(f"re: {a.re}")
    path = MSGS / f"{mid}.md"
    path.write_text("---\n" + "\n".join(head) + "\n---\n" + body.strip() + "\n", encoding="utf-8")
    paths = [path]
    if a.re:  # replying closes the loop on the original
        paths.append(write_ack(a.re, me(a), f"replied in {mid}"))
    commit(paths, f"bridge: {me(a)} -> {a.to.lower()}: {a.title}")
    print(mid)
    if a.push:
        sync(a)


def write_ack(mid, who, note=""):
    if not (MSGS / f"{mid}.md").exists():
        sys.exit(f"no such message: {mid}")
    p = ACKS / f"{mid}.{who}.ack"
    p.write_text(f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ} {note}\n", encoding="utf-8")
    return p


def cmd_ack(a):
    p = write_ack(a.id, me(a), a.note)
    commit([p], f"bridge: {me(a)} ack {a.id}")
    if a.push:
        sync(a)


def cmd_inbox(a):
    who, shown = me(a), 0
    for m, _ in messages():
        if not a.all and (m["to"] not in (who, "all") or who in acked(m["id"])):
            continue
        shown += 1
        print(f"{m['id']}\n   {m['from']} -> {m['to']}  {m['title']}")
    if not shown:
        print(f"inbox empty for {who}")


def cmd_read(a):
    m, body = parse(MSGS / f"{a.id}.md")
    print("\n".join(f"{k}: {v}" for k, v in m.items()), "\n\n" + body)
    print("\nacked by:", ", ".join(sorted(acked(a.id))) or "nobody")


def cmd_status(a):
    b = branch(a)
    git("fetch", "origin", b, check=False)
    ab = git("rev-list", "--left-right", "--count", f"HEAD...origin/{b}", check=False) or "? ?"
    ahead, behind = ab.split()[:2]
    print(f"branch {b}: {ahead} ahead, {behind} behind origin")
    for who in sorted({m["to"] for m, _ in messages()}):
        n = sum(1 for m, _ in messages() if m["to"] in (who, "all") and who not in acked(m["id"]))
        print(f"  {who}: {n} unacked")


def cmd_handoff(a):
    r = root()
    open_msgs = [m for m, _ in messages() if m["to"] in (a.to or "all", "all") and (a.to or "all") not in acked(m["id"])]
    log = git("log", "--oneline", "-8", cwd=r)
    dirty = git("status", "--short", cwd=r) or "(clean)"
    out = [f"# HANDOFF — {me(a)} -> {a.to or 'any'}",
           f"_{datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC} · branch `{branch(a)}` · `{git('rev-parse', '--short', 'HEAD')}`_", "",
           f"**TASK:** {a.task or '—'}", f"**DONE:** {a.done or '—'}", f"**NEXT:** {a.next or '—'}", "",
           "## Open bridge messages", *(f"- `{m['id']}` {m['title']}" for m in open_msgs), "" if open_msgs else "- none", "",
           "## Recent commits", "```", log, "```", "## Working tree", "```", dirty, "```", "",
           "## Resume", "```bash", f"git fetch origin {branch(a)} && git checkout {branch(a)} && git pull --rebase",
           f"python3 02_COUNCIL_GROVE/bridge/bridge.py inbox --as {a.to or 'opencode'}", "```"]
    HANDOFF.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {HANDOFF}")


# ── advisory file leases (so two agents don't edit the same paths at once) ─────
# One immutable file per acquire; a release is a sibling .released file. Advisory
# only: it tells the other agent "I'm working here", it does not block git.

def norm(p):
    return os.path.normpath(p).lstrip("./")


def overlaps(a, b):
    a, b = norm(a), norm(b)
    return (fnmatch.fnmatch(a, b) or fnmatch.fnmatch(b, a)
            or a.startswith(b.rstrip("*/") + "/") or b.startswith(a.rstrip("*/") + "/") or a == b)


def active_leases():
    now, out = datetime.now(timezone.utc), []
    for p in sorted(LEASES.glob("*.lease")):
        if p.with_suffix(".released").exists():
            continue
        m, _ = parse(p)
        if datetime.strptime(m["expires"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) > now:
            out.append(m)
    return out


def cmd_lease(a):
    LEASES.mkdir(exist_ok=True)
    who = me(a)
    if a.action == "list":
        rows = active_leases()
        for m in rows:
            print(f"{m['id']}\n   {m['agent']} holds {m['path']} until {m['expires']}  {m.get('note', '')}")
        return print("no active leases") if not rows else None
    if not a.paths:
        sys.exit("give at least one path or glob")
    if a.action == "check":
        hits = [(m, p) for p in a.paths for m in active_leases() if m["agent"] != who and overlaps(p, m["path"])]
        for m, p in hits:
            print(f"CONFLICT {p} <- {m['agent']} ({m['path']}, until {m['expires']})")
        sys.exit(1 if hits else 0)
    if a.action == "acquire":
        clash = [(m, p) for p in a.paths for m in active_leases() if m["agent"] != who and overlaps(p, m["path"])]
        if clash:
            for m, p in clash:
                print(f"held by {m['agent']}: {m['path']} until {m['expires']}", file=sys.stderr)
            sys.exit("lease refused (run `sync` first if this looks stale)")
        now = datetime.now(timezone.utc)
        made = []
        for p in a.paths:
            lid = f"{now:%Y%m%dT%H%M%SZ}-{who}-{hashlib.sha1(norm(p).encode()).hexdigest()[:8]}"
            exp = now + timedelta(minutes=a.ttl)
            f = LEASES / f"{lid}.lease"
            f.write_text(f"---\nagent: {who}\npath: {norm(p)}\nexpires: {exp:%Y-%m-%dT%H:%M:%SZ}\nnote: {a.note}\n---\n", encoding="utf-8")
            made.append(f); print(lid)
        commit(made, f"bridge: {who} lease {', '.join(norm(p) for p in a.paths)}")
    else:  # release
        done = []
        for m in active_leases():
            if m["agent"] == who and any(overlaps(p, m["path"]) for p in a.paths):
                f = LEASES / f"{m['id']}.released"
                f.write_text(f"{datetime.now(timezone.utc):%Y-%m-%dT%H:%M:%SZ}\n", encoding="utf-8")
                done.append(f); print("released", m["id"])
        if not done:
            return print("nothing to release")
        commit(done, f"bridge: {who} release leases")
    if a.push:
        sync(a)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--as", dest="who")
    ap.add_argument("--branch")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send"); s.add_argument("--to", required=True); s.add_argument("--title", required=True)
    s.add_argument("--body"); s.add_argument("--re"); s.add_argument("--push", action="store_true"); s.set_defaults(f=cmd_send)
    s = sub.add_parser("ack"); s.add_argument("id"); s.add_argument("--note", default="")
    s.add_argument("--push", action="store_true"); s.set_defaults(f=cmd_ack)
    s = sub.add_parser("inbox"); s.add_argument("--all", action="store_true"); s.set_defaults(f=cmd_inbox)
    s = sub.add_parser("read"); s.add_argument("id"); s.set_defaults(f=cmd_read)
    s = sub.add_parser("lease"); s.add_argument("action", choices=["acquire", "release", "check", "list"])
    s.add_argument("paths", nargs="*"); s.add_argument("--ttl", type=int, default=120, help="minutes")
    s.add_argument("--note", default=""); s.add_argument("--push", action="store_true"); s.set_defaults(f=cmd_lease)
    sub.add_parser("sync").set_defaults(f=sync)
    sub.add_parser("status").set_defaults(f=cmd_status)
    s = sub.add_parser("handoff"); [s.add_argument(f"--{k}") for k in ("task", "done", "next", "to")]
    s.set_defaults(f=cmd_handoff)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
