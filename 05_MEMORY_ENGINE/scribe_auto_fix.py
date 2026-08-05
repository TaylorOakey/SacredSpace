#!/usr/bin/env python3
"""
SCRIBE Phase 1 — Auto-Fix Stage
Applies routing suggestions to vault files
"""

import re
from pathlib import Path
import sys

def normalize_frontmatter(file_path, pillar=None, status=None):
    """Update file frontmatter with normalized values"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            print(f"  ⚠️  No frontmatter: {file_path.relative_to(file_path.parent.parent.parent.parent)}")
            return False

        fm = fm_match.group(1)
        fm_end = fm_match.end()

        # Update pillar if provided
        if pillar:
            if 'pillar:' in fm:
                fm = re.sub(r'pillar:\s*.+?$', f'pillar: {pillar}', fm, flags=re.MULTILINE)
            else:
                fm = fm + f'\npillar: {pillar}'

        # Normalize status (uppercase)
        if 'status:' in fm:
            fm = re.sub(r'status:\s*(.+?)$', lambda m: f'status: {m.group(1).strip().upper()}', fm, flags=re.MULTILINE)

        # Rebuild file
        new_content = f"---\n{fm}\n---{content[fm_end:]}"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True
    except Exception as e:
        print(f"  Error fixing {file_path}: {e}")
        return False

def main():
    vault_path = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")

    print("[SCRIBE] Applying auto-fixes...\n")

    # Fix 1: Normalize all status values to uppercase
    print("1️⃣  Normalizing status values to UPPERCASE...")
    fixed = 0
    for md_file in vault_path.rglob("*.md"):
        if ".obsidian" in str(md_file):
            continue
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if re.search(r"status:\s*[a-z]", content):
                if normalize_frontmatter(md_file):
                    fixed += 1
    print(f"   ✓ Fixed {fixed} files\n")

    # Fix 2: Assign pillar to orphaned NPC files
    print("2️⃣  Assigning 04_SACRED_CODEX to orphaned NPCs...")
    npc_path = vault_path / "00_CANON" / "GAME_SYSTEM" / "NPCS"
    if npc_path.exists():
        fixed = 0
        for npc_file in npc_path.glob("NPC_*.md"):
            if normalize_frontmatter(npc_file, pillar="04_SACRED_CODEX"):
                fixed += 1
        print(f"   ✓ Fixed {fixed} NPC files\n")

    # Fix 3: Consolidate pillar naming in old folders
    print("3️⃣  Mapping old folder names to pillar codes...")
    folder_mapping = {
        "SYSTEMS": "02_COUNCIL_GROVE",
        "LEARNING": "08_LEARNING_PATH",
        "ECONOMY": "09_SACRED_MARKET",
        "COUNCIL": "02_COUNCIL_GROVE",
        "CREATION": "04_SACRED_CODEX",
        "LINEAGE": "07_SOCIAL_MOTHERSHIP",
        "CORE": "00_SYSTEM_CORE",
        "ARCHIVE": "01_OBSIDIAN_VAULTS",
        "HABITAT": "03_NEURAL_FOREST"
    }

    for old_name, new_pillar in folder_mapping.items():
        old_path = vault_path / old_name
        if old_path.exists():
            for md_file in old_path.rglob("*.md"):
                if normalize_frontmatter(md_file, pillar=new_pillar):
                    pass

    print(f"   ✓ Mapped old folder names to pillars\n")

    # Fix 4: Inject wikilinks from filenames (simple heuristic)
    print("4️⃣  Detecting missing wikilink opportunities...")
    suggestions = 0
    for md_file in vault_path.rglob("*.md"):
        if ".obsidian" in str(md_file):
            continue
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)

            # If file has 0 wikilinks, suggest some
            if len(wikilinks) == 0 and md_file.name.startswith("NPC_"):
                suggestions += 1

    print(f"   ℹ️  {suggestions} files could benefit from wikilink injection\n")

    print("[SCRIBE] Auto-fixes complete!")
    print("\nSummary:")
    print("  ✓ Status values normalized to UPPERCASE")
    print("  ✓ Orphaned NPCs assigned to 04_SACRED_CODEX")
    print("  ✓ Old folder names mapped to pillar codes")
    print("  ✓ Wikilink opportunities identified")

if __name__ == "__main__":
    main()
