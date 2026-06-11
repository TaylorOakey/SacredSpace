#!/usr/bin/env python3
"""
prep_notebooklm.py — SacredSpace OS Canon Migration Tool
Scans the Obsidian vault, renames files per Sacred naming convention,
and stages them into per-notebook folders for NotebookLM upload.

Run: python3 prep_notebooklm.py
Output: /mnt/d/SacredSpace_OS/NOTEBOOKLM_STAGING/
"""

import shutil
import re
from pathlib import Path

VAULT = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
CODEX = Path("/mnt/d/SacredSpace_OS/04_SACRED_CODEX")
STAGING = Path("/mnt/d/SacredSpace_OS/NOTEBOOKLM_STAGING")

# Notebook staging subdirs
NOTEBOOKS = {
    "01_SACRED_CORE":   STAGING / "01_SACRED_CORE",
    "02_LORE_VAULT":    STAGING / "02_LORE_VAULT",
    "03_GAME_SYSTEMS":  STAGING / "03_GAME_SYSTEMS",
    "04_KNOWLEDGE_VAULT": STAGING / "04_KNOWLEDGE_VAULT",
    "05_FAMILY_LEGACY": STAGING / "05_FAMILY_LEGACY",
    "06_CREATION_LAB":  STAGING / "06_CREATION_LAB",
}

def clean_name(stem: str) -> str:
    """Convert ARCHETYPE_01_THE_FOOL → The Fool, METATRON_LAW → Metatron Law"""
    # Strip leading type prefix + optional number (ARCHETYPE_01_, NODE_02_, SCHOOL_)
    stem = re.sub(r'^(ARCHETYPE|NODE|SCHOOL|EPISODE)_\d*_?', '', stem)
    # Replace underscores with spaces, title case
    return stem.replace('_', ' ').title()


# Routing rules: (glob_pattern, notebook_key, DOMAIN, TYPE)
ROUTING = [
    # Archetypes → LORE.VAULT as CHARACTERS
    (VAULT / "00_CANON/GAME_SYSTEM/ARCHETYPES",  "02_LORE_VAULT",    "LORE", "CHARACTER"),
    # Sacred Nodes → GAME.SYSTEMS as MAP
    (VAULT / "00_CANON/GAME_SYSTEM/NODES",        "03_GAME_SYSTEMS",  "GAME", "MAP"),
    # Spell Schools → GAME.SYSTEMS as SYSTEM
    (VAULT / "00_CANON/GAME_SYSTEM/SCHOOLS",      "03_GAME_SYSTEMS",  "GAME", "SYSTEM"),
    # Episodes → LORE.VAULT as STORY
    (VAULT / "00_CANON/GAME_SYSTEM/EPISODES",     "02_LORE_VAULT",    "LORE", "STORY"),
    # Game System INDEX → SACRED.CORE as SYSTEM
    (VAULT / "00_CANON/GAME_SYSTEM",              "01_SACRED_CORE",   "CORE", "SYSTEM"),
    # Sacred Codex docs → KNOWLEDGE.VAULT as PROTOCOL
    (CODEX,                                        "04_KNOWLEDGE_VAULT", "KNOW", "PROTOCOL"),
]

def make_staged_name(domain: str, type_tag: str, name: str, version: int = 1) -> str:
    return f"{domain} — {type_tag} — {name} — v{version}.md"


def stage_folder(src_dir: Path, notebook_key: str, domain: str, type_tag: str,
                 manifest: list, exclude_subdirs: bool = False):
    if not src_dir.exists():
        return
    dest = NOTEBOOKS[notebook_key]
    dest.mkdir(parents=True, exist_ok=True)

    pattern = "*.md" if not exclude_subdirs else None
    files = []
    if pattern:
        files = list(src_dir.glob(pattern))

    for src in sorted(files):
        name = clean_name(src.stem)
        dest_name = make_staged_name(domain, type_tag, name)
        dest_path = dest / dest_name
        shutil.copy2(src, dest_path)
        manifest.append({
            "source": str(src.relative_to(VAULT.parent.parent)),
            "staged_as": dest_name,
            "notebook": notebook_key,
        })


def run():
    print("⟡ SacredSpace NotebookLM Prep — Canon Migration Tool ⟡\n")

    # Clear and recreate staging
    if STAGING.exists():
        shutil.rmtree(STAGING)
    for nb_dir in NOTEBOOKS.values():
        nb_dir.mkdir(parents=True, exist_ok=True)

    manifest = []

    # --- 01 SACRED.CORE: INDEX.md only (not subdirs) ---
    index = VAULT / "00_CANON/GAME_SYSTEM/INDEX.md"
    if index.exists():
        dest = NOTEBOOKS["01_SACRED_CORE"]
        dest_name = make_staged_name("CORE", "SYSTEM", "Game System Index")
        shutil.copy2(index, dest / dest_name)
        manifest.append({"source": str(index.relative_to(VAULT.parent.parent)),
                         "staged_as": dest_name, "notebook": "01_SACRED_CORE"})

    # --- 02 LORE.VAULT: Archetypes + Episodes ---
    for src_dir, nb, domain, type_tag in [
        (VAULT / "00_CANON/GAME_SYSTEM/ARCHETYPES", "02_LORE_VAULT", "LORE", "CHARACTER"),
        (VAULT / "00_CANON/GAME_SYSTEM/EPISODES",   "02_LORE_VAULT", "LORE", "STORY"),
    ]:
        stage_folder(src_dir, nb, domain, type_tag, manifest)

    # --- 03 GAME.SYSTEMS: Nodes + Schools ---
    for src_dir, nb, domain, type_tag in [
        (VAULT / "00_CANON/GAME_SYSTEM/NODES",   "03_GAME_SYSTEMS", "GAME", "MAP"),
        (VAULT / "00_CANON/GAME_SYSTEM/SCHOOLS", "03_GAME_SYSTEMS", "GAME", "SYSTEM"),
    ]:
        stage_folder(src_dir, nb, domain, type_tag, manifest)

    # --- 04 KNOWLEDGE.VAULT: Sacred Codex .md docs ---
    for src in sorted(CODEX.glob("*.md")):
        name = src.stem.replace('_', ' ').title()
        dest_name = make_staged_name("KNOW", "PROTOCOL", name)
        dest = NOTEBOOKS["04_KNOWLEDGE_VAULT"]
        shutil.copy2(src, dest / dest_name)
        manifest.append({"source": str(src.relative_to(VAULT.parent.parent)),
                         "staged_as": dest_name, "notebook": "04_KNOWLEDGE_VAULT"})

    # --- Print manifest ---
    print(f"{'NOTEBOOK':<22} {'STAGED FILE':<55} SOURCE")
    print("-" * 110)
    for entry in manifest:
        print(f"{entry['notebook']:<22} {entry['staged_as']:<55} {entry['source']}")

    print(f"\n✓ {len(manifest)} files staged → {STAGING}")
    print("\nUpload order for NotebookLM:")
    for nb_key, nb_dir in NOTEBOOKS.items():
        files = list(nb_dir.glob("*.md"))
        if files:
            print(f"  [{nb_key}] — {len(files)} file(s)")

    # Write manifest to staging root
    manifest_path = STAGING / "UPLOAD_MANIFEST.md"
    with open(manifest_path, "w") as f:
        f.write("# NotebookLM Upload Manifest\n\n")
        f.write("Generated by prep_notebooklm.py\n\n")
        current_nb = None
        for entry in manifest:
            if entry["notebook"] != current_nb:
                current_nb = entry["notebook"]
                f.write(f"\n## {current_nb}\n\n")
            f.write(f"- **{entry['staged_as']}**  \n  _source: {entry['source']}_\n")
    print(f"\nManifest written → {manifest_path}")
    print("\nIn Lakesh — Alakin.")


if __name__ == "__main__":
    run()
