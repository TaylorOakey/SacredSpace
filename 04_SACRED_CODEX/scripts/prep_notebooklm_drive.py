#!/usr/bin/env python3
"""
prep_notebooklm_drive.py — SacredSpace OS Drive-Source Notebook Stager
Stages local pillar content into NOTEBOOKLM_STAGING for notebooks 05-08.
Companion to prep_notebooklm.py (which handles vault/codex notebooks 01-04).

Also syncs local content → Drive (rclone) to establish cloud sources.

Output: /mnt/d/SacredSpace_OS/NOTEBOOKLM_STAGING/
"""

import shutil, subprocess, sys, os
from pathlib import Path

ROOT = Path("/mnt/d/SacredSpace_OS")
STAGING = ROOT / "NOTEBOOKLM_STAGING"
RCLONE_REMOTE = "gdrive:SacredSpace_OS_CLOUD"

NOTEBOOKS = {
    "05_FAMILY_LEGACY":   STAGING / "05_FAMILY_LEGACY",
    "06_CREATION_LAB":    STAGING / "06_CREATION_LAB",
    "07_SACRED_SIGNAL":   STAGING / "07_SACRED_SIGNAL",
    "08_SACRED_MARKET":   STAGING / "08_SACRED_MARKET",
}

def safe_name(stem: str) -> str:
    """Clean a filename stem for staging convention."""
    out = stem.replace("_", " ").replace("－", "-").replace("／", " & ")
    out = " ".join(out.split())  # collapse whitespace
    return out.strip()

def stage(src: Path, notebook_key: str, domain: str, type_tag: str,
          version: int, manifest: list, ext: str = None):
    """Copy a single file into the staging notebook folder."""
    if not src.exists():
        return
    dest_dir = NOTEBOOKS[notebook_key]
    dest_dir.mkdir(parents=True, exist_ok=True)
    ext = ext or src.suffix
    name = safe_name(src.stem)
    dest_name = f"{domain} — {type_tag} — {name} — v{version}{ext}"
    dest_path = dest_dir / dest_name
    if not dest_path.exists():
        shutil.copy2(src, dest_path)
    manifest.append({
        "notebook": notebook_key,
        "staged_as": dest_name,
        "source": str(src.relative_to(ROOT)),
    })

def run():
    print("⟡ SacredSpace Drive-Source Notebook Stager ⟡\n")
    manifest = []

    # — 05 FAMILY.LEGACY — from _PERSONAL/NOTEBOOKLM_SAFE —
    safe = ROOT / "_PERSONAL/NOTEBOOKLM_SAFE"
    if safe.exists():
        print("→ 05_FAMILY_LEGACY")
        stage(safe / "Monthly Sacred Messages Index (Year 1–5).docx",
              "05_FAMILY_LEGACY", "FAMILY", "INDEX", 1, manifest)
        stage(safe / "Sacred_Messages_Iris/Child Ritual Card – Iris.docx",
              "05_FAMILY_LEGACY", "FAMILY", "MESSAGE", 1, manifest)
        stage(safe / "Sacred_Messages_Asher/Child Ritual Card – Asher.docx",
              "05_FAMILY_LEGACY", "FAMILY", "MESSAGE", 1, manifest)
        stage(safe / "Northeast_Academy/School Year Overview (2025–2026).docx",
              "05_FAMILY_LEGACY", "FAMILY", "ACADEMY", 1, manifest)
        stage(safe / "Northeast_Academy/Morning ／ Evening Rhythms.docx",
              "05_FAMILY_LEGACY", "FAMILY", "RITUAL", 1, manifest)

    # — 06 CREATION.LAB — from 07_SOCIAL/CREATION_LAB —
    # (only image assets currently; no text docs to stage)
    clab = ROOT / "07_SOCIAL/CREATION_LAB"
    if clab.exists():
        # Check if any non-image text files exist
        text_files = list(clab.rglob("*"))
        text_files = [f for f in text_files
                      if f.is_file() and f.suffix.lower() in (".md", ".txt", ".docx", ".pdf")]
        if text_files:
            print("→ 06_CREATION_LAB")
            for f in text_files:
                stage(f, "06_CREATION_LAB", "CREATE", "SEED", 1, manifest)
        else:
            print("→ 06_CREATION_LAB — only image assets, no text docs to stage")

    # — 07 SACRED.SIGNAL — from 07_SOCIAL (root + SACRED_THEMES_COMPONENTS) —
    social = ROOT / "07_SOCIAL"
    signal_docs = [
        (social / "sacredarcana_brand_bible_v3.docx", "BRAND", 3),
        (social / "SACREDSPACESTUDIOS SOCIAL MEDIA ACCOUNTS .docx", "SOCIAL", 1),
        (social / "[TEMPLATE] Creative Drop Zone Intake V2.docx", "TEMPLATE", 2),
        (social / "SACRED_THEMES_COMPONENTS/SACRED_WORD_BANK.md", "CONTENT", 1),
        (social / "SACRED_THEMES_COMPONENTS/SUBSYSTEM_MANIFEST.md", "SYSTEM", 1),
    ]
    signal_count = 0
    for path, typ, ver in signal_docs:
        if path.exists():
            if signal_count == 0:
                print("→ 07_SACRED_SIGNAL")
                signal_count = 1
            stage(path, "07_SACRED_SIGNAL", "SIGNAL", typ, ver, manifest)
    if not signal_count:
        print("→ 07_SACRED_SIGNAL — no docs found")

    # — 08 SACRED.MARKET — from 09_MARKET —
    market = ROOT / "09_MARKET"
    if market.exists():
        print("→ 08_SACRED_MARKET")
        stage(market / "SacredSpace_GrantCopyMatrix_v1.docx",
              "08_SACRED_MARKET", "MARKET", "GRANT", 1, manifest)
        stage(market / "SacredSpace_NeuralForest_GrantProposal_v2.docx",
              "08_SACRED_MARKET", "MARKET", "GRANT", 2, manifest)
        stage(market / "Sacred_Sprouts/Business Plans/Sprouts Business Model v1.docx",
              "08_SACRED_MARKET", "MARKET", "BUSINESS", 1, manifest)
        stage(market / "Sacred_Sprouts/Pricing & Inventory/Inventory Sheet (Editable).docx",
              "08_SACRED_MARKET", "MARKET", "INVENTORY", 1, manifest)

    # — Print summary —
    staged_count = len(manifest)
    print(f"\n✓ {staged_count} files staged from Drive-sourced pillars")

    for nb_key, nb_dir in NOTEBOOKS.items():
        files = sorted(nb_dir.glob("*"))
        if files:
            print(f"  [{nb_key}] — {len(files)} file(s)")
            for f in files:
                print(f"    {f.name}")

    # — Update manifest (merge: keep existing, append Drive-sourced sections) —
    manifest_path = STAGING / "UPLOAD_MANIFEST.md"
    existing_content = ""
    if manifest_path.exists():
        # Read existing, strip out any sections we're replacing (05-08)
        import re
        lines = manifest_path.read_text().split("\n")
        in_our_section = False
        kept = []
        for line in lines:
            if re.match(r'^## (0[5678])_', line):
                in_our_section = True
                continue
            elif re.match(r'^## \d', line):
                in_our_section = False
            if not in_our_section:
                kept.append(line)
        existing_content = "\n".join(kept).rstrip() + "\n\n"

    with open(manifest_path, "w") as f:
        f.write(existing_content)
        # Append our Drive-sourced entries
        current_nb = None
        for entry in manifest:
            if entry["notebook"] != current_nb:
                current_nb = entry["notebook"]
                f.write(f"\n## {current_nb}\n\n")
            f.write(f"- **{entry['staged_as']}**  \n  _source: {entry['source']}_\n")
    print(f"\nManifest → {manifest_path}")
    print("\nIn Lakesh — Alakin.")

    return staged_count


def sync_to_drive():
    """Push staged content up to Drive to establish cloud source."""
    print("\n⟡ Syncing staging → Drive...")
    for nb_key, nb_dir in NOTEBOOKS.items():
        if not nb_dir.exists():
            continue
        cloud_path = None
        if nb_key == "05_FAMILY_LEGACY":
            cloud_path = "_PERSONAL/NOTEBOOKLM_SAFE"
        elif nb_key == "06_CREATION_LAB":
            cloud_path = "07_SOCIAL/CREATION_LAB"
        elif nb_key == "07_SACRED_SIGNAL":
            cloud_path = "07_SOCIAL/SIGNAL"
        elif nb_key == "08_SACRED_MARKET":
            cloud_path = "09_MARKET"
        if cloud_path:
            dest = f"{RCLONE_REMOTE}/{cloud_path}"
            result = subprocess.run(
                ["rclone", "copy", str(nb_dir), dest, "--progress"],
                capture_output=True, text=True, timeout=120
            )
            if result.returncode == 0:
                print(f"  ✓ {nb_key} → {cloud_path}")
            else:
                print(f"  ✗ {nb_key} sync failed: {result.stderr.strip()[:200]}")
    print("Drive sync complete.")


if __name__ == "__main__":
    staged = run()
    if "--sync" in sys.argv:
        sync_to_drive()
