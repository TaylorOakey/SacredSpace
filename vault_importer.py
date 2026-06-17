#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  VAULT IMPORTER — SacredSpace OS                     ║
║  Bridges parser output into Obsidian vault inbox     ║
║  Sources: chatgpt_sessions, claude_sessions,          ║
║           GEMINI_ARCHAEOLOGY                          ║
║  Target: 01_CORE/SacredSpace_Vault/00_INBOX/AI_CHATS ║
╚══════════════════════════════════════════════════════╝
Usage:
    python3 vault_importer.py                                      # Import all sources
    python3 vault_importer.py --source chatgpt                     # Single source
    python3 vault_importer.py --dry-run                            # Preview only
    python3 vault_importer.py --source claude --dry-run            # Preview single source
"""

import os
import re
import shutil
import json
import argparse
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────
SACREDSPACE_ROOT = Path("/mnt/d/SacredSpace_OS")
VAULT_INBOX = SACREDSPACE_ROOT / "01_CORE" / "SacredSpace_Vault" / "00_INBOX" / "AI_CHATS"
VAULT_INDEX = VAULT_INBOX / "_INDEX.md"

SOURCES = {
    "chatgpt": {
        "path": SACREDSPACE_ROOT / "_RAW" / "chatgpt_sessions",
        "label": "ChatGPT Export",
        "exists_check": lambda p: p.exists() and any(p.iterdir()),
    },
    "claude": {
        "path": SACREDSPACE_ROOT / "_RAW" / "claude_sessions",
        "label": "Claude.ai Export",
        "exists_check": lambda p: p.exists() and any(p.iterdir()),
    },
    "archaeology": {
        "path": SACREDSPACE_ROOT / "_PENDING_REVIEW" / "GEMINI_ARCHAEOLOGY",
        "label": "Gemini Archaeology (Phase 1B)",
        "exists_check": lambda p: p.exists() and any(p.iterdir()),
    },
}

# ── Pillar label mapping ──────────────────────────
PILLAR_LABELS = {
    "01_CORE": "◇ Obsidian Vaults",
    "02_COUNCIL_GROVE": "⬡ Council Grove",
    "02_SYSTEMS": "⬡ Council Grove",
    "03_NEURAL": "⚙ Neural Forest",
    "04_CODEX": "☽ Sacred Codex",
    "05_MEMORY": "∞ Memory Engine",
    "06_AGENTS": "∆ Agent Layer",
    "07_SOCIAL": "✶ Social Mothership",
    "08_LEARNING": "⊕ Learning Path",
    "09_MARKET": "√ Sacred Market",
}

CANONICAL_PILLAR_NAMES = [
    "01_CORE", "02_COUNCIL_GROVE", "02_SYSTEMS", "03_NEURAL", "04_CODEX",
    "05_MEMORY", "06_AGENTS", "07_SOCIAL", "08_LEARNING", "09_MARKET",
]


# ── Helpers ────────────────────────────────────────

def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown text."""
    fm = {}
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if m:
        for line in m.group(1).strip().split('\n'):
            if ':' in line:
                key, _, val = line.partition(':')
                fm[key.strip()] = val.strip().strip('"').strip("'")
    return fm


def detect_source_type(filepath: Path) -> str:
    """Detect which parser produced a file from its content."""
    text = filepath.read_text(encoding="utf-8", errors="replace")[:500]
    fm = parse_frontmatter(text)
    src = fm.get("source", "")
    if src == "chatgpt":
        return "chatgpt"
    elif src == "claude":
        return "claude"
    # Archaeology files lack frontmatter; detect by path
    if "GEMINI_ARCHAEOLOGY" in str(filepath):
        return "archaeology"
    return "unknown"


def count_importable(filepath: Path) -> dict:
    """Count files per pillar per source."""
    stats = {}
    for source_name, source_cfg in SOURCES.items():
        source_path = source_cfg["path"]
        if not source_path.exists():
            continue
        stats[source_name] = {"total": 0, "by_pillar": {}}
        for pillar_dir in source_path.iterdir():
            if not pillar_dir.is_dir():
                continue
            pillar = pillar_dir.name
            files = list(pillar_dir.glob("*.md"))
            n = len(files)
            stats[source_name]["total"] += n
            if n > 0:
                stats[source_name]["by_pillar"][pillar] = n
    return stats


# ── Import ─────────────────────────────────────────

def import_source(source_name: str, source_cfg: dict, dry_run: bool = False) -> dict:
    """Import all files from one source into the vault inbox."""
    source_path = source_cfg["path"]
    label = source_cfg["label"]
    result = {"source": source_name, "label": label, "copied": 0, "skipped": 0, "errors": 0, "by_pillar": {}}

    if not source_path.exists():
        print(f"  [⚠] Source path not found: {source_path}")
        return result

    # Find all pillar subdirectories
    pillar_dirs = [d for d in source_path.iterdir() if d.is_dir() and d.name in CANONICAL_PILLAR_NAMES]
    if not pillar_dirs:
        # Fallback: scan for pillar dirs with different naming
        pillar_dirs = [d for d in source_path.iterdir() if d.is_dir()]

    for pillar_dir in sorted(pillar_dirs, key=lambda d: d.name):
        pillar = pillar_dir.name
        markdown_files = sorted(pillar_dir.glob("*.md"))

        if not markdown_files:
            continue

        # Target: AI_CHATS/<source>/<pillar>/
        target_dir = VAULT_INBOX / source_name / pillar
        if not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)

        count = 0
        for fpath in markdown_files:
            # Skip index files
            if fpath.name.startswith("_INDEX") or fpath.name.startswith("_README"):
                continue

            # Skip files that are just templates/empty
            content = fpath.read_text(encoding="utf-8", errors="replace").strip()
            if len(content) < 50:
                if dry_run:
                    print(f"    [∼] Skipped (too small): {fpath.name}")
                result["skipped"] += 1
                continue

            target_path = target_dir / fpath.name

            if target_path.exists():
                # Skip duplicates
                result["skipped"] += 1
                continue

            if not dry_run:
                shutil.copy2(fpath, target_path)

            count += 1
            result["copied"] += 1

        if count > 0:
            result["by_pillar"][pillar] = count
            if dry_run:
                pillar_label = PILLAR_LABELS.get(pillar, pillar)
                print(f"    [{pillar_label}] → {count} files to {target_dir}")

    return result


def write_import_index(results: list[dict]):
    """Generate a comprehensive index of all imported AI chat files."""
    total_copied = sum(r["copied"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)
    total_errors = sum(r["errors"] for r in results)

    lines = [
        "# ∆ AI Chats — Vault Index",
        "",
        f"> **Last imported:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> **Total files imported:** {total_copied} ({total_skipped} skipped, {total_errors} errors)",
        "",
        "---",
        "",
        "## By Source",
        "",
    ]

    for r in results:
        if r["copied"] == 0:
            continue
        lines.append(f"### {r['label']}")
        lines.append(f"**{r['copied']} files**")
        lines.append("")
        for pillar, count in sorted(r["by_pillar"].items()):
            pillar_label = PILLAR_LABELS.get(pillar, pillar)
            lines.append(f"- **{pillar_label}**: {count} conversations")
        lines.append("")

    lines += [
        "---",
        "",
        "## Next Steps",
        "",
        "1. Review files in each pillar directory",
        "2. Promote CANON_CANDIDATE files → 04_CODEX",
        "3. Distill key insights into Codex entries",
        "4. Archive raw exploration after distillation",
        "",
        "---",
        "",
        "_In lakesh alakin. ∆_",
    ]

    VAULT_INBOX.mkdir(parents=True, exist_ok=True)
    VAULT_INDEX.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  Index written: {VAULT_INDEX}")


# ── Main ───────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SacredSpace OS — Vault Importer")
    parser.add_argument("--source", choices=["chatgpt", "claude", "archaeology", "all"], default="all",
                        help="Which source to import (default: all)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview what would be imported without copying")
    args = parser.parse_args()

    print("╔══════════════════════════════════════════════╗")
    print("║  ∆ VAULT IMPORTER — SacredSpace OS           ║")
    print("╚══════════════════════════════════════════════╝")
    print()

    if args.dry_run:
        print("  [∆] DRY RUN — no files will be copied\n")

    print(f"  Target: {VAULT_INBOX}\n")

    # Select sources
    if args.source == "all":
        selected_sources = SOURCES.items()
    else:
        selected_sources = [(args.source, SOURCES[args.source])]

    results = []
    for source_name, source_cfg in selected_sources:
        print(f"  [{source_cfg['label']}]")
        result = import_source(source_name, source_cfg, dry_run=args.dry_run)
        if result["copied"] > 0:
            print(f"    → {result['copied']} files imported")
        elif not args.dry_run:
            print(f"    → No new files (skipped {result['skipped']})")
        results.append(result)
        print()

    # Summary
    total = sum(r["copied"] for r in results)
    skipped = sum(r["skipped"] for r in results)
    print("═" * 52)
    if args.dry_run:
        print(f"  DRY RUN: {total} files ready to import ({skipped} would be skipped)")
    else:
        print(f"  ∆ Import complete: {total} files imported ({skipped} skipped)")
        write_import_index(results)
    print("═" * 52 + "\n")


if __name__ == "__main__":
    main()
