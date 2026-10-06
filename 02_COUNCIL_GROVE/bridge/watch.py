#!/usr/bin/env python3
"""watch.py — laptop-side bridge watcher. Stdlib only, never edits your working tree.

Polls origin/<branch>, reads bridge messages straight from git objects (no pull,
no checkout, no autostash — safe while you're mid-edit), and tells you when a
new message addressed to you arrives.

  python3 watch.py [--as opencode] [--interval 60] [--once]
                   [--senders claude] [--notify-cmd CMD] [--wake-cmd CMD] [--dry-run]

Actions on a new message (all optional; default is just a terminal bell + line):
  --notify-cmd CMD   run CMD with BRIDGE_TITLE / BRIDGE_FROM / BRIDGE_ID in its environment
                     (read them as $BRIDGE_TITLE, %BRIDGE_TITLE% in cmd.exe, or $env:BRIDGE_TITLE in
                     PowerShell). No string formatting or quoting is applied to your command, so braces,
                     quotes and ${...} in it are safe on any shell.
  --wake-cmd CMD     run CMD to wake OpenCode, e.g. 'opencode run --dir C:\\path\\to\\repo "Check the bridge inbox and ask me before acting."'
                     The command is fixed text; message bodies are NEVER put into it or its environment.
  --wake-cwd DIR     directory to run the wake command in (default: the bridge directory)

Safety: only senders in --senders (default: claude) are acted on; everything else is
shown as "ignored sender". A message is a request, not authority — OpenCode's own
permission prompts still gate what it does. Seen-state lives outside the repo.
"""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent


def git(*a):
    r = subprocess.run(["git", *a], cwd=HERE, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def meta(text):
    m = {}
    if text.startswith("---\n"):
        for line in text[4:].partition("\n---\n")[0].splitlines():
            k, _, v = line.partition(":"); m[k.strip()] = v.strip()
    return m


def remote_files(ref, rel, ext):
    rc, out, _ = git("ls-tree", "--full-tree", "-r", "--name-only", ref, "--", rel)
    return [f for f in out.splitlines() if f.endswith(ext)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--as", dest="who", default=os.environ.get("BRIDGE_AGENT", "opencode"))
    ap.add_argument("--branch"); ap.add_argument("--interval", type=int, default=60)
    ap.add_argument("--once", action="store_true"); ap.add_argument("--backlog", action="store_true", help="on first run, notify for existing unread too"); ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--senders", default="claude", help="comma list of senders to act on")
    ap.add_argument("--notify-cmd"); ap.add_argument("--wake-cmd"); ap.add_argument("--wake-cwd")
    ap.add_argument("--state", default=str(Path.home() / ".cache/sacredspace-bridge/seen.json"))
    a = ap.parse_args()

    branch = a.branch or os.environ.get("BRIDGE_BRANCH") or git("branch", "--show-current")[1].strip()
    prefix = git("rev-parse", "--show-prefix")[1].strip()          # e.g. 02_COUNCIL_GROVE/bridge/
    ref, who, senders = f"origin/{branch}", a.who.lower(), {s.strip().lower() for s in a.senders.split(",")}
    state = Path(a.state); state.parent.mkdir(parents=True, exist_ok=True)
    first_run = not state.exists()
    seen = set(json.loads(state.read_text())) if state.exists() else set()
    print(f"watching {ref} as {who} every {a.interval}s (acting on: {', '.join(sorted(senders))})", file=sys.stderr)

    while True:
        rc, _, err = git("fetch", "origin", branch)
        if rc:
            print(f"fetch failed: {err.strip()[:120]}", file=sys.stderr)
        else:
            acks = {Path(f).name for f in remote_files(ref, prefix + "acks", ".ack")}
            fresh = []
            for f in sorted(remote_files(ref, prefix + "msgs", ".md")):
                mid = Path(f).stem
                if mid in seen:
                    continue
                m = meta(git("show", f"{ref}:{f}")[1])
                if m.get("to") not in (who, "all") or f"{mid}.{who}.ack" in acks:
                    seen.add(mid); continue
                seen.add(mid)
                if first_run and not a.backlog:
                    continue
                if m.get("from", "").lower() not in senders:
                    print(f"ignored sender {m.get('from')!r}: {m.get('title')}", file=sys.stderr); continue
                fresh.append((mid, m))
            for mid, m in fresh:
                print(f"\a[bridge] {m['from']} -> {who}: {m.get('title')}  ({mid})")
                if a.notify_cmd and not a.dry_run:
                    env = {**os.environ, "BRIDGE_TITLE": m.get("title", ""), "BRIDGE_FROM": m["from"], "BRIDGE_ID": mid}
                    subprocess.run(a.notify_cmd, shell=True, env=env)
            if fresh and a.wake_cmd:
                print(f"[bridge] waking: {a.wake_cmd}")
                if not a.dry_run:
                    subprocess.run(a.wake_cmd, shell=True, cwd=a.wake_cwd or HERE)
            if first_run and not a.backlog:
                print(f"first run: marked {len(seen)} existing message(s) as seen (--backlog to be notified of them)", file=sys.stderr)
            if not a.dry_run:
                state.write_text(json.dumps(sorted(seen)))
            first_run = False
        if a.once:
            return
        time.sleep(a.interval)


if __name__ == "__main__":
    main()
