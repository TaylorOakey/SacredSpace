"""
Business Hub builder: one auto-updated index of every SacredSpace document about
cash flow, business, nonprofit/grants, marketing, branding and culture.

It indexes files where they already live (it never copies or moves them), so the
originals stay the single source of truth and the hub can't drift out of date.
Each run rewrites:
  HUB/INDEX.md   what you read: ledger snapshot, recent changes, one section per domain
  HUB/index.json the same data for agents (Claude, OpenCode, a future FastAPI route)

Config (roots, domains, keywords): 09_SACRED_MARKET/HUB/hub_config.json
Schedule it with 09_SACRED_MARKET/tools/install_hub_cron.sh (WSL2 cron).

Usage (repo root):
  python3 09_SACRED_MARKET/tools/hub_build.py
  python3 09_SACRED_MARKET/tools/hub_build.py --roots .          # this repo only
  python3 09_SACRED_MARKET/tools/hub_build.py --out /some/dir    # write elsewhere
"""

import argparse
import hashlib
import html
import json
import os
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
HUB = REPO / "09_SACRED_MARKET" / "HUB"
VAULT_MARKERS = ("01_VAULT", "SacredSpace_Vault", "01_OBSIDIAN_VAULTS")
TAG_RE = re.compile(r"<(script|style|head)\b.*?</\1>|<[^>]+>", re.S | re.I)


def compile_domains(domains: dict) -> dict:
    return {
        name: re.compile(r"(?<![A-Za-z0-9])(" + "|".join(re.escape(k) for k in
                         sorted(d["keywords"], key=len, reverse=True)) + r")(?![A-Za-z0-9])", re.I)
        for name, d in domains.items()
    }


def native_path(r: str) -> Path:
    """Accept both spellings in the config: /mnt/d/x on WSL and D:/x (or D:\\x) on Windows."""
    r = os.path.expanduser(r)
    win = re.match(r"^([A-Za-z]):[\\/](.*)", r)
    wsl = re.match(r"^/mnt/([a-z])(?:/(.*))?$", r)
    if os.name != "nt" and win:
        return Path(f"/mnt/{win.group(1).lower()}", win.group(2).replace("\\", "/"))
    if os.name == "nt" and wsl:
        return Path(f"{wsl.group(1).upper()}:/", wsl.group(2) or "")
    return Path(r)


def load_config(path: Path) -> dict:
    """hub_config.json, plus an optional gitignored hub_config.local.json beside it.
    Local lists (roots, skip_dirs, extensions) extend the shared ones; local scalars override."""
    cfg = json.loads(path.read_text(encoding="utf-8"))
    local = path.with_name(path.stem + ".local.json")
    if local.exists():
        for k, v in json.loads(local.read_text(encoding="utf-8")).items():
            if k.startswith("_"):
                continue
            if isinstance(v, list) and isinstance(cfg.get(k), list):
                cfg[k] = cfg[k] + [x for x in v if x not in cfg[k]]
            else:
                cfg[k] = v
        print(f"local overrides: {local}")
    return cfg


def resolve_roots(raw: list) -> list:
    roots, seen = [], set()
    for r in raw:
        p = native_path(r)
        p = (REPO / p) if not p.is_absolute() else p
        if not p.exists():
            print(f"skip (not found): {p}")
            continue
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            roots.append(rp)
    return roots


def walk(root: Path, cfg: dict):
    exts = set(cfg["text_ext"]) | set(cfg["name_only_ext"])
    skip = set(cfg["skip_dirs"])
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in skip and not d.startswith("."))
        for fn in sorted(filenames):
            if Path(fn).suffix.lower() in exts and not fn.startswith((".", "~$")):
                yield Path(dirpath) / fn


def read_text(path: Path, raw: bytes) -> str:
    text = raw.decode("utf-8", errors="replace")
    if path.suffix.lower() in (".html", ".htm"):
        title = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        body = html.unescape(TAG_RE.sub(" ", text))
        text = (f"# {title.group(1).strip()}\n" if title else "") + body
    return text


def summarize(text: str) -> tuple[str, str]:
    """(title, first real sentence), skipping YAML front matter, rules and code fences."""
    lines = text.splitlines()
    title, blurb, fence = "", "", False
    if lines and lines[0].strip() == "---":
        end = next((i for i, l in enumerate(lines[1:], 1) if l.strip() == "---"), 0)
        for l in lines[1:end]:
            m = re.match(r"\s*(title|name|TITLE)\s*:\s*(.+)", l)
            if m and not title:
                title = m.group(2).strip().strip("'\"")
        lines = lines[end + 1:]
    for l in lines:
        s = l.strip()
        if s.startswith("```"):
            fence = not fence
            continue
        if fence or not s or set(s) <= set("-=*_|:#> "):
            continue
        if s.startswith("#"):
            title = title or s.lstrip("# ").strip()
            continue
        if not blurb:
            blurb = re.sub(r"\s+", " ", re.sub(r"\*\*|__|`|\[\[|\]\]", "", s).lstrip(">*- ").strip())
        if title and blurb:
            break
    blurb = blurb if len(blurb) <= 140 else blurb[:137].rstrip() + "…"
    return title[:100], blurb


def score(name: str, text: str, patterns: dict, name_weight: int = 6) -> dict:
    """Per domain: name_weight per keyword in the filename + 1 per distinct keyword in the content.
    The filename is the author's own label, so it outweighs incidental words in the body."""
    out = {}
    name = name.replace("_", " ").replace("-", " ")
    for dom, pat in patterns.items():
        body = {m.group(1).lower() for m in pat.finditer(text)}
        title = {m.group(1).lower() for m in pat.finditer(name)}
        s = name_weight * len(title) + len(body)
        if s:
            out[dom] = {"score": s, "keywords": sorted(title | body)[:6]}
    return out


def ledger_snapshot(db: Path) -> dict | None:
    if not db.exists():
        return None
    try:
        conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)
        q = lambda sql, *a: conn.execute(sql, a).fetchall()
        product_net = q("SELECT COALESCE(SUM(net_usd),0) FROM sales WHERE kind IN ('PRODUCT','REFUND')")[0][0]
        net_all = q("SELECT COALESCE(SUM(net_usd),0) FROM sales")[0][0]
        exp = q("SELECT COALESCE(SUM(amount_usd),0) FROM expenses")[0][0]
        months = q("SELECT substr(sale_date,1,7) m, ROUND(SUM(net_usd),2), COUNT(*) FROM sales "
                   "GROUP BY m ORDER BY m DESC LIMIT 6")
        today = date.today().isoformat()
        soon = (date.today() + timedelta(days=30)).isoformat()
        grants = q("SELECT funder, program, status, deadline FROM grants WHERE deadline BETWEEN ? AND ? "
                   "AND status NOT IN ('AWARDED','DECLINED','WITHDRAWN','CLOSED') ORDER BY deadline", today, soon)
        pipeline = q("SELECT status, COUNT(*) FROM grants GROUP BY status")
        conn.close()
    except sqlite3.Error as e:
        return {"error": str(e)}
    return {"first_flame_net": round(product_net, 2), "net_all": round(net_all, 2),
            "expenses": round(exp, 2), "cash_position": round(net_all - exp, 2),
            "by_month": months, "grants_due_30d": grants, "grant_pipeline": dict(pipeline)}


def usd(x: float) -> str:
    return f"{'-' if x < 0 else ''}${abs(x):,.2f}"


def md_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", type=Path, default=HUB / "hub_config.json")
    ap.add_argument("--roots", nargs="*", help="override the config's roots")
    ap.add_argument("--out", type=Path, default=HUB)
    ap.add_argument("--allow-vault", action="store_true",
                    help="permit --out inside the Obsidian vault (source of record)")
    a = ap.parse_args()

    if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252 and choke on ∆
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    cfg = load_config(a.config)
    if any(m in str(a.out) for m in VAULT_MARKERS) and not a.allow_vault:
        ap.error(f"--out {a.out} is inside the Obsidian vault; pass --allow-vault to confirm")
    patterns = compile_domains(cfg["domains"])
    roots = resolve_roots(a.roots if a.roots is not None else cfg["roots"])
    out = a.out.resolve()
    recent_cut = datetime.now() - timedelta(days=cfg["recent_days"])

    docs, seen_hash, seen_path, scanned, dupes = [], {}, set(), 0, 0
    for root in roots:
        print(f"scanning: {root}")
        for f in walk(root, cfg):
            rp = f.resolve()
            if rp in seen_path or out in rp.parents:
                continue
            seen_path.add(rp)
            scanned += 1
            try:
                raw = rp.read_bytes()
            except OSError as e:
                print(f"  skip {f}: {e}")
                continue
            name_only = rp.suffix.lower() in cfg["name_only_ext"]
            text = "" if name_only else read_text(rp, raw)
            doms = score(rp.stem, text, patterns, cfg.get("filename_weight", 6))
            doms = {d: v for d, v in doms.items() if v["score"] >= cfg["min_score"]}
            if not doms:
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen_hash:
                dupes += 1
                seen_hash[digest]["duplicates"].append(str(rp))
                continue
            title, blurb = ("", "(binary — matched by filename)") if name_only else summarize(text)
            mtime = datetime.fromtimestamp(rp.stat().st_mtime)
            primary = max(doms, key=lambda d: doms[d]["score"])
            doc = {"path": str(rp), "root": str(root), "rel": str(rp.relative_to(root)),
                   "title": title or rp.stem, "summary": blurb, "modified": mtime.strftime("%Y-%m-%d"),
                   "recent": mtime >= recent_cut, "primary": primary, "domains": doms,
                   "sha256": digest, "duplicates": []}
            seen_hash[digest] = doc
            docs.append(doc)

    ledger = ledger_snapshot(native_path(cfg["ledger_db"]))
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.json").write_text(json.dumps(
        {"generated": stamp, "roots": [str(r) for r in roots], "scanned": scanned,
         "duplicates_folded": dupes, "ledger": ledger, "documents": docs}, indent=2), encoding="utf-8")

    def link(d):
        label = ("REPO/" if Path(d["root"]) == REPO else Path(d["root"]).name + "/") + d["rel"]
        try:
            target = os.path.relpath(d["path"], out)
        except ValueError:  # Windows: file on another drive (C: vault vs D: hub) has no relative path
            target = Path(d["path"]).as_uri()
        return f"[{md_cell(label)}](<{target}>)"

    L = [f"# ∆ SacredSpace Business Hub", "",
         f"*Auto-generated {stamp} by `09_SACRED_MARKET/tools/hub_build.py`. Don't edit this file: "
         f"edit the source documents, or change domains and keywords in `hub_config.json`.*", "",
         f"**{len(docs)} documents** from {scanned} scanned (a document can appear under more than one topic) · {dupes} exact duplicates folded · "
         f"roots: {', '.join(f'`{r}`' for r in roots)}", ""]
    def in_domain(d, dom):
        """Primary domain, or a secondary one scoring at least secondary_ratio of the primary."""
        s = d["domains"].get(dom, {}).get("score", 0)
        return dom == d["primary"] or s >= cfg.get("secondary_ratio", 0.5) * d["domains"][d["primary"]]["score"]

    counts = {d: sum(1 for x in docs if in_domain(x, d)) for d in cfg["domains"]}
    L += ["| " + " | ".join(f"[{cfg['domains'][d]['label']}](#{d})" for d in counts) + " |",
          "|" + "---|" * len(counts), "| " + " | ".join(str(c) for c in counts.values()) + " |", ""]

    L += ["## Ledger snapshot", ""]
    if not ledger:
        L += [f"*No ledger database at `{cfg['ledger_db']}` yet. It appears once the first sale or "
              f"expense is posted to `/merchant/ledger` or `/merchant/expenses`.*", ""]
    elif "error" in ledger:
        L += [f"*Ledger unreadable: {ledger['error']}*", ""]
    else:
        L += [f"- **First Flame:** {usd(ledger['first_flame_net'])} of $1,111 product net",
              f"- **Net income (all kinds):** {usd(ledger['net_all'])} · **expenses:** {usd(ledger['expenses'])}"
              f" · **cash position:** {usd(ledger['cash_position'])}"]
        if ledger["by_month"]:
            L += ["- **Last months:** " + " · ".join(f"{m} {usd(n)} ({c})" for m, n, c in ledger["by_month"])]
        L += ["- **Grant pipeline:** " + (", ".join(f"{k} {v}" for k, v in ledger["grant_pipeline"].items())
                                          or "empty")]
        for f_, p, s, dl in ledger["grants_due_30d"]:
            L += [f"  - ⏰ {dl} · {f_}{' — ' + p if p else ''} ({s})"]
        L += [""]

    recent = sorted((d for d in docs if d["recent"]), key=lambda d: d["modified"], reverse=True)
    L += [f"## Changed in the last {cfg['recent_days']} days", ""]
    L += [f"- {d['modified']} · **{md_cell(d['title'])}** · {cfg['domains'][d['primary']]['label']} · {link(d)}"
          for d in recent[:25]] or ["*Nothing.*"]
    L += [""]

    for dom, meta in cfg["domains"].items():
        rows = sorted((d for d in docs if in_domain(d, dom)),
                      key=lambda d: (d["primary"] != dom, -d["domains"][dom]["score"], d["rel"]))
        L += [f'<a id="{dom}"></a>', f"## {meta['label']} ({len(rows)})", ""]
        if not rows:
            L += ["*No documents yet.*", ""]
            continue
        L += ["| Document | What it is | Also in (**main**) | Keywords | Modified |", "|---|---|---|---|---|"]
        for d in rows[:cfg["per_domain_limit"]]:
            also = ", ".join(("**" + x + "**" if x == d["primary"] else x) for x in d["domains"] if x != dom)
            dup = f" (+{len(d['duplicates'])} copies)" if d["duplicates"] else ""
            L += [f"| **{md_cell(d['title'])}**<br>{link(d)}{dup} | {md_cell(d['summary'])} | {also} | "
                  f"{', '.join(d['domains'][dom]['keywords'])} | {d['modified']} |"]
        if len(rows) > cfg["per_domain_limit"]:
            L += ["", f"*…and {len(rows) - cfg['per_domain_limit']} more in `index.json`.*"]
        L += [""]

    L += ["---", "*Layer: RAW index. Nothing here is CANON; promotion goes through the Canon Gate.*"]
    (out / "INDEX.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"\n∆ hub: {len(docs)} documents ({dupes} duplicates folded) of {scanned} scanned → {out / 'INDEX.md'}")


if __name__ == "__main__":
    main()
