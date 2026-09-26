"""
Revenue consolidator — hardened version of the REVENUE_CONSOLIDATE.md Step 1 scan.

Finds money-related Markdown across the SacredSpace locations and writes a
MANIFEST first (dry run). Copies only with --copy, and never into the Obsidian
vault (the source of record) unless --allow-vault is also given.

Fixes over the original script:
  • whole-word keyword matching + a score threshold  ("pod" no longer matches
    "episode"/"podcast", "grant" no longer matches "granted")
  • skips the 140 GB SACREDSPACE_ARCHIVE, .git, node_modules, venvs, and every
    private path (_PERSONAL, NOTEBOOKLM_SAFE, Messages_*, .env)
  • de-duplicates by content hash (the May scan already produced ~25 dupes)
  • collision-safe copy names (REVENUE_<name>__<hash8>.md): same-named files
    from different folders no longer overwrite each other
  • default output is the 09 pillar on D:, not the vault

Usage (on the Legion, WSL2):
  python3 revenue_consolidate.py                    # dry run → manifest only
  python3 revenue_consolidate.py --copy             # also copy matched files
  python3 revenue_consolidate.py --roots /mnt/d/SacredSpace_OS --min-score 3
"""

import argparse
import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path

KEYWORDS = [
    "money", "cash", "cashflow", "cash flow", "revenue", "abundance", "bazaar",
    "grant", "grants", "funding", "budget", "profit", "capital", "income",
    "merchant", "treasury", "monetization", "monetize", "etsy", "printify",
    "gelato", "printful", "crowdfund", "crowdfunding", "kickstarter", "sales",
    "pricing", "subscription", "ko-fi", "gumroad", "print-on-demand",
    "print on demand", "pod", "501(c)(3)", "llc", "invoice", "royalty",
    "sacred market", "sacred cashflow", "first flame", "1111 flow",
]
# "market" and "ledger" dropped: they match SacredSpace system terms
# (Sacred Market pillar names, SACRED_LEDGER session logs) far more than money.
PATTERN = re.compile(
    r"(?<![A-Za-z0-9])(" + "|".join(re.escape(k) for k in KEYWORDS) + r")(?![A-Za-z0-9])",
    re.IGNORECASE,
)

ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))
DEFAULT_ROOTS = [
    ROOT,
    Path("/mnt/d/01_VAULT/SacredSpace_Vault"),
    Path("/mnt/c/01_OBSIDIAN_VAULTS/SacredSpace_Vault"),
    Path.home() / "sacredspace",
    Path.home() / "sacredspace_core",
]
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv", ".venvs", ".obsidian",
    "SACREDSPACE_ARCHIVE", "REVENUE_CONSOLIDATION",
    "_PERSONAL", "NOTEBOOKLM_SAFE", "Messages_Iris", "Messages_Asher",
}
VAULT_MARKERS = ("01_VAULT", "SacredSpace_Vault")


def score(name: str, text: str) -> tuple[int, dict]:
    """Filename hits count 3 each; distinct content keywords count 1 each."""
    hits = {}
    for m in PATTERN.finditer(text):
        k = m.group(1).lower()
        hits[k] = hits.get(k, 0) + 1
    name_hits = {m.group(1).lower() for m in PATTERN.finditer(name.replace("_", " "))}
    return 3 * len(name_hits) + len(hits), hits


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            if fn.lower().endswith(".md") and fn != ".env":
                yield Path(dirpath) / fn


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--roots", nargs="*", type=Path, default=DEFAULT_ROOTS)
    ap.add_argument("--out", type=Path, default=ROOT / "09_SACRED_MARKET" / "REVENUE_CONSOLIDATION")
    ap.add_argument("--min-score", type=int, default=3,
                    help="Minimum score to count as financial (default 3)")
    ap.add_argument("--copy", action="store_true", help="Copy matched files (default: manifest only)")
    ap.add_argument("--allow-vault", action="store_true",
                    help="Permit --out inside the Obsidian vault (source of record)")
    a = ap.parse_args()

    if any(m in str(a.out) for m in VAULT_MARKERS) and not a.allow_vault:
        ap.error(f"--out {a.out} is inside the Obsidian vault; pass --allow-vault to confirm")

    seen, rows, dupes, scanned = {}, [], 0, 0
    for root in a.roots:
        if not root.exists():
            print(f"skip (not found): {root}")
            continue
        print(f"scanning: {root}")
        for f in walk(root):
            if a.out in f.parents:
                continue
            scanned += 1
            try:
                raw = f.read_bytes()
            except OSError as e:
                print(f"  skip {f}: {e}")
                continue
            text = raw.decode("utf-8", errors="replace")
            s, hits = score(f.stem, text)
            if s < a.min_score:
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if digest in seen:
                dupes += 1
                seen[digest]["duplicates"].append(str(f))
                continue
            row = {
                "path": str(f), "size": len(raw),
                "modified": datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d"),
                "score": s, "top_keywords": sorted(hits, key=hits.get, reverse=True)[:6],
                "sha256": digest, "duplicates": [],
            }
            seen[digest] = row
            rows.append(row)

    rows.sort(key=lambda r: r["score"], reverse=True)
    a.out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    (a.out / "MANIFEST.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    lines = [f"# Revenue consolidation manifest · {stamp}", "",
             f"Scanned {scanned} .md files · {len(rows)} unique financial matches · "
             f"{dupes} duplicates folded · min score {a.min_score}", "",
             "| Score | Modified | Keywords | Path | Dupes |", "|---|---|---|---|---|"]
    lines += [f"| {r['score']} | {r['modified']} | {', '.join(r['top_keywords'])} | `{r['path']}` | {len(r['duplicates'])} |"
              for r in rows]
    (a.out / "MANIFEST.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    if a.copy:
        for r in rows:
            src = Path(r["path"])
            dest = a.out / f"REVENUE_{src.stem}__{r['sha256'][:8]}.md"
            text = src.read_text(encoding="utf-8", errors="replace")
            if not text.lstrip().startswith("---"):
                text = (f"---\nTITLE: {src.stem}\nSOURCE: {src}\nDATE_CONSOLIDATED: {stamp}\n"
                        f"PILLAR: 09_SACRED_MARKET\nTAGS: REVENUE, FINANCIAL_COHESION\n---\n\n") + text
            dest.write_text(text, encoding="utf-8")

    print(f"\n∆ {len(rows)} unique financial files ({dupes} duplicates folded) of {scanned} scanned")
    print(f"  manifest → {a.out / 'MANIFEST.md'}" + ("" if a.copy else "   (dry run: rerun with --copy to copy)"))


if __name__ == "__main__":
    main()
