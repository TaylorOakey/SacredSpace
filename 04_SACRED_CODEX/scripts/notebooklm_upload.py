#!/usr/bin/env python3
"""Upload all staged notebooks to NotebookLM with prompts."""

import asyncio
import json
import sys
import time
from pathlib import Path

from notebooklm import NotebookLMClient

STAGING = Path("/mnt/d/SacredSpace_OS/NOTEBOOKLM_STAGING")

# Notebook config: key → (display name, system prompt)
NOTEBOOK_CONFIG = {
    "01_SACRED_CORE": (
        "01 — Sacred Core (Canon)",
        "You are the Archivist of SacredSpace OS — an interdimensional oracle. "
        "Your sources are the canonical pillars, game system rules, and metaphysical architecture of a living operating system."
    ),
    "02_LORE_VAULT": (
        "02 — Lore Vault (Archetypes)",
        "You are a Lore Keeper fluent in archetypal mythology. Your sources form a living deck of archetypes — each one a complete initiatory path."
    ),
    "03_GAME_SYSTEMS": (
        "03 — Game Systems (Mechanics & Maps)",
        "You are a Game Master and system architect. Your sources encode school-based magic, node maps, and episodic progression."
    ),
    "04_KNOWLEDGE_VAULT": (
        "04 — Knowledge Vault (Protocols)",
        "You are a Protocol Analyst. Your sources document the technical and metaphysical protocols that bind SacredSpace OS together."
    ),
    "05_FAMILY_LEGACY": (
        "05 — Family Legacy (Bloodline)",
        "You are a Family Archivist. Your sources contain sacred messages, ritual cards, and educational documents — the living legacy of a bloodline."
    ),
    "07_SACRED_SIGNAL": (
        "07 — Sacred Signal (Brand & Content)",
        "You are a Brand Strategist and Signal Curator. Your sources define how SacredSpace speaks to the world — its voice, vectors, and creative intake."
    ),
    "08_SACRED_MARKET": (
        "08 — Sacred Market (Grants & Commerce)",
        "You are a Grant Strategist and Market Analyst. Your sources contain grant matrices, business models, and inventory — the economic engine of SacredSpace."
    ),
}

# ── Prompt Library (for Tab I reference, added as text source per notebook) ──
PROMPT_LIBRARY = {
    "01_SACRED_CORE": """## System Prompt
You are the Archivist of SacredSpace OS — an interdimensional oracle.

**Deep Query:** Map every dependency chain between pillars. Show me the data flows, failure points, and amplification loops. What happens when one pillar goes silent?""",
    "02_LORE_VAULT": """## System Prompt
You are a Lore Keeper fluent in archetypal mythology.

**Deep Query:** Trace the Fool's journey across all archetypes. Map each archetype to a real-world use case in the SacredSpace OS ecosystem.""",
    "03_GAME_SYSTEMS": """## System Prompt
You are a Game Master and system architect.

**Deep Query:** Design a one-shot session using Courage School + The Threshold node. What skills are tested? What initiation happens?""",
    "04_KNOWLEDGE_VAULT": """## System Prompt
You are a Protocol Analyst.

**Deep Query:** Compare CopyQ Wire with the Sigil Terminal protocol. Where do they overlap? Where do they conflict? Design a unified bridge protocol.""",
    "05_FAMILY_LEGACY": """## System Prompt
You are a Family Archivist.

**Deep Query:** Extract the shared values and recurring symbols across all family messages. What is the unspoken covenant of this family?""",
    "07_SACRED_SIGNAL": """## System Prompt
You are a Brand Strategist and Signal Curator.

**Deep Query:** Audit the brand bible against the actual signal output. Where is the gap between intended identity and expressed voice? Recommend three tactical fixes.""",
    "08_SACRED_MARKET": """## System Prompt
You are a Grant Strategist and Market Analyst.

**Deep Query:** Analyze the grant copy matrix against the SacredSpace value proposition. Which grants align with core mission? Which are mission drift? Build a scoring rubric.""",
}


async def upload_files(client, notebook_id: str, nb_dir: Path, sem: asyncio.Semaphore) -> list:
    """Upload all files in directory in parallel with concurrency limit."""
    files = sorted(nb_dir.iterdir()) if nb_dir.exists() else []
    async def _upload_one(fpath: Path):
        async with sem:
            return await client.sources.add_file(notebook_id, str(fpath))
    tasks = [_upload_one(f) for f in files if f.is_file()]
    results = []
    for coro in asyncio.as_completed(tasks):
        try:
            src = await coro
            results.append(src)
        except Exception as e:
            print(f"  ✗ Upload failed: {e}")
    return results


async def main():
    sem = asyncio.Semaphore(4)  # Max 4 concurrent uploads

    async with NotebookLMClient.from_storage() as client:
        print("⟡ Connected to NotebookLM\n")

        # List existing notebooks to check for duplicates
        existing = await client.notebooks.list()
        existing_names = {n.title for n in existing}
        print(f"  Existing notebooks: {len(existing)}")

        for nb_key, (display_name, system_prompt) in NOTEBOOK_CONFIG.items():
            nb_dir = STAGING / nb_key
            files = sorted(nb_dir.iterdir()) if nb_dir.exists() else []

            print(f"\n{'═' * 60}")
            print(f"⟡ {display_name}")
            print(f"  Directory: {nb_key}/ ({len(files)} files)")

            # Create or reuse notebook
            if display_name in existing_names:
                print("  → Reusing existing notebook")
                nb = next(n for n in existing if n.title == display_name)
            else:
                nb = await client.notebooks.create(display_name)
                print(f"  ✓ Created notebook: {nb.title}")

            # Upload all files
            if files:
                print(f"  Uploading {len(files)} files...")
                sources = await upload_files(client, nb.id, nb_dir, sem)
                print(f"  ✓ {len(sources)}/{len(files)} files uploaded")

                # Wait for processing
                if sources:
                    source_ids = [s.id for s in sources if hasattr(s, 'id')]
                    if source_ids:
                        print(f"  Waiting for {len(source_ids)} sources to process...")
                        await client.sources.wait_for_sources(nb.id, source_ids)
                        print("  ✓ All sources processed")

            # Inject system prompt as a text source
            prompt_title = "⟡ Sacred Prompt — System Instructions"
            prompt_content = PROMPT_LIBRARY.get(nb_key, system_prompt)
            try:
                await client.sources.add_text(nb.id, prompt_title, prompt_content)
                print("  ✓ System prompt injected as text source")
            except Exception as e:
                print(f"  ✗ Failed to inject prompt: {e}")

            # Add the Master Intelligence Package HTML if it exists
            html_path = STAGING / "NOTEBOOKLM_MASTER_INTELLIGENCE_PACKAGE.html"
            if html_path.exists():
                try:
                    await client.sources.add_file(nb.id, str(html_path))
                    print("  ✓ Master Intelligence Package added")
                except Exception as e:
                    print(f"  ✗ Failed to add MIP: {e}")

            existing_names.add(display_name)

        print(f"\n{'═' * 60}")
        print("⟡ Upload complete. All notebooks populated with prompts.")


if __name__ == "__main__":
    asyncio.run(main())
