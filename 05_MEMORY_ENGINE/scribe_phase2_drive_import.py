#!/usr/bin/env python3
"""
SCRIBE Phase 2 — Google Drive Import Workflow
Routes 56 docs to canonical vault homes
"""

import json
from pathlib import Path
import shutil

def main():
    print("[SCRIBE Phase 2B] Google Drive Import Workflow\n")

    # Load drive index
    drive_index_path = Path("/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/scribe_drive_index.json")
    with open(drive_index_path) as f:
        drive_index = json.load(f)

    vault_path = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")

    print(f"Google Drive documents ready for import: {drive_index['total_docs']}")
    print(f"\nRouting breakdown:")

    for pillar, docs in sorted(drive_index["by_pillar"].items()):
        canonical_folder = vault_path / "00_CANON" / pillar.split("_")[1].upper()
        canonical_folder.mkdir(parents=True, exist_ok=True)

        print(f"\n  {pillar}: {len(docs)} documents")
        print(f"    → Canonical home: {canonical_folder.relative_to(vault_path)}/")

        for doc in docs[:2]:
            doc_name = doc["name"]
            print(f"      - {doc_name}")

        if len(docs) > 2:
            print(f"      - ... and {len(docs)-2} more")

    print(f"\n✅ Import workflow ready")
    print(f"\nNext steps:")
    print(f"  1. Copy Google Drive markdown files to vault")
    print(f"  2. Apply SACREDTAG frontmatter from templates")
    print(f"  3. Run: python3 sacred_scribe.py audit")
    print(f"  4. Verify: All 56 docs now in vault with pillar assignment")

if __name__ == "__main__":
    main()
