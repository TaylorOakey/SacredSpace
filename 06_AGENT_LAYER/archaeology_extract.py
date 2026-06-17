#!/usr/bin/env python3
"""
Gemini Archaeology — Extraction Script (Phase 1B)

Reads the ChatGPT export at conversations.json and extracts high-priority
conversations into _PENDING_REVIEW/GEMINI_ARCHAEOLOGY/<pillar>/ for review.

Usage:
    python3 archaeology_extract.py                        # Extract priority 1 (all pillars)
    python3 archaeology_extract.py --pillar 04            # Single pillar
    python3 archaeology_extract.py --priority 1-3         # By priority tier
    python3 archaeology_extract.py --convo 5,23,42        # Specific conversations by catalog #
    python3 archaeology_extract.py --sample 3             # Quick sample: 3 convos per pillar
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# --- Config ---
CONVERSATIONS_PATH = Path("/mnt/d/SacredSpace_OS/06_AGENTS/conversations.json")
OUTPUT_BASE = Path("/mnt/d/SacredSpace_OS/_PENDING_REVIEW/GEMINI_ARCHAEOLOGY")

# Pillar mapping: catalog # -> pillar
PILLAR_MAP = {
    # PILLAR 01 — CORE
    6: "01_CORE", 13: "01_CORE", 16: "01_CORE", 36: "01_CORE", 288: "01_CORE",
    # PILLAR 02 — COUNCIL GROVE
    4: "02_COUNCIL_GROVE", 5: "02_COUNCIL_GROVE", 22: "02_COUNCIL_GROVE",
    35: "02_COUNCIL_GROVE", 42: "02_COUNCIL_GROVE", 53: "02_COUNCIL_GROVE",
    61: "02_COUNCIL_GROVE", 225: "02_COUNCIL_GROVE",
    # PILLAR 03 — NEURAL FOREST
    8: "03_NEURAL", 10: "03_NEURAL", 25: "03_NEURAL", 47: "03_NEURAL",
    48: "03_NEURAL", 160: "03_NEURAL", 204: "03_NEURAL", 302: "03_NEURAL",
    # PILLAR 04 — SACRED CODEX
    17: "04_CODEX", 19: "04_CODEX", 23: "04_CODEX", 24: "04_CODEX",
    31: "04_CODEX", 33: "04_CODEX", 42: "04_CODEX", 52: "04_CODEX",
    67: "04_CODEX", 69: "04_CODEX", 70: "04_CODEX", 71: "04_CODEX",
    74: "04_CODEX", 75: "04_CODEX", 78: "04_CODEX", 79: "04_CODEX",
    129: "04_CODEX", 134: "04_CODEX", 195: "04_CODEX", 199: "04_CODEX",
    286: "04_CODEX", 290: "04_CODEX", 332: "04_CODEX", 333: "04_CODEX",
    341: "04_CODEX",
    # PILLAR 05 — MEMORY ENGINE
    64: "05_MEMORY", 65: "05_MEMORY", 68: "05_MEMORY", 105: "05_MEMORY",
    126: "05_MEMORY", 146: "05_MEMORY", 233: "05_MEMORY", 237: "05_MEMORY",
    # PILLAR 06 — AGENT LAYER
    45: "06_AGENTS", 46: "06_AGENTS", 62: "06_AGENTS", 76: "06_AGENTS",
    77: "06_AGENTS", 80: "06_AGENTS", 83: "06_AGENTS", 89: "06_AGENTS",
    210: "06_AGENTS", 220: "06_AGENTS", 231: "06_AGENTS", 238: "06_AGENTS",
    # PILLAR 07 — SOCIAL
    56: "07_SOCIAL", 57: "07_SOCIAL", 58: "07_SOCIAL", 97: "07_SOCIAL",
    103: "07_SOCIAL", 358: "07_SOCIAL", 386: "07_SOCIAL",
    # PILLAR 08 — LEARNING
    28: "08_LEARNING", 84: "08_LEARNING", 144: "08_LEARNING",
    32: "08_LEARNING", 316: "08_LEARNING",
    # PILLAR 09 — MARKET
    20: "09_MARKET", 55: "09_MARKET", 93: "09_MARKET", 127: "09_MARKET",
    149: "09_MARKET", 157: "09_MARKET", 197: "09_MARKET", 289: "09_MARKET",
    299: "09_MARKET", 313: "09_MARKET", 351: "09_MARKET", 370: "09_MARKET",
}


def load_conversations():
    """Load the ChatGPT export JSON."""
    with open(CONVERSATIONS_PATH, encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} conversations from {CONVERSATIONS_PATH}")
    return data


def flatten_messages(convo):
    """Flatten the conversation mapping tree into ordered messages."""
    mapping = convo.get("mapping", {})
    if not mapping:
        return []

    # Find root node (no parent)
    root_id = None
    for msg_id, node in mapping.items():
        if node.get("parent") is None:
            root_id = msg_id
            break

    if not root_id:
        return []

    # BFS/DFS to flatten in order
    ordered = []
    visited = set()

    def traverse(node_id):
        if node_id in visited:
            return
        visited.add(node_id)
        node = mapping.get(node_id)
        if node is None:
            return
        msg = node.get("message")
        if msg:
            ordered.append(msg)
        for child_id in node.get("children", []):
            traverse(child_id)

    traverse(root_id)
    return ordered


def format_conversation(convo, catalog_num):
    """Format a conversation as a markdown document."""
    title = convo.get("title", "Untitled")
    create_time = convo.get("create_time", 0)
    update_time = convo.get("update_time", 0)

    created_dt = datetime.fromtimestamp(create_time, tz=timezone.utc) if create_time else None
    updated_dt = datetime.fromtimestamp(update_time, tz=timezone.utc) if update_time else None

    lines = []
    lines.append(f"# {title}")
    lines.append("")
    lines.append(f"> **Catalog #{catalog_num}** | Extracted {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"> Created: {created_dt.strftime('%Y-%m-%d %H:%M UTC') if created_dt else 'Unknown'}")
    lines.append(f"> Updated: {updated_dt.strftime('%Y-%m-%d %H:%M UTC') if updated_dt else 'Unknown'}")
    lines.append("")

    messages = flatten_messages(convo)
    if not messages:
        lines.append("*No message content in this conversation.*")
        return "\n".join(lines)

    lines.append(f"**{len(messages)} messages**")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, msg in enumerate(messages):
        role = msg.get("author", {}).get("role", "unknown")
        content_parts = msg.get("content", {})

        # Get text content
        text = ""
        if isinstance(content_parts, dict):
            parts = content_parts.get("parts", [])
            for part in parts:
                if isinstance(part, str):
                    text += part
                elif isinstance(part, dict):
                    text += part.get("text", "")
        elif isinstance(content_parts, str):
            text = content_parts

        # Skip system messages
        if role == "system":
            continue

        # Format header
        role_label = {"user": "👤 User", "assistant": "🤖 Assistant"}
        header = role_label.get(role, f"**{role.upper()}**")
        lines.append(f"### Message {i+1} — {header}")
        lines.append("")

        # Content
        if text.strip():
            lines.append(text.strip())
            lines.append("")

        # Tool calls or other metadata
        if msg.get("tool_calls"):
            lines.append("*Tool calls present in this message*")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def slugify(title):
    """Convert title to filesystem-safe slug."""
    s = title.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s[:80]


def extract(pillar_filter=None, catalog_filter=None, sample_per_pillar=None):
    """Extract conversations to pillar folders."""
    convos = load_conversations()

    # Map catalog positions to indices
    catalog_to_idx = {}
    for idx, c in enumerate(convos):
        title = c.get("title", "").strip()
        create_time = c.get("create_time", 0)
        # Find in PILLAR_MAP by matching title (fragile) or use sequential numbering
        # We'll use sequential numbering based on the catalog order
    # Actually, the catalog numbers are sequential from the export listing
    # We'll rebuild the mapping

    # Build reverse index: (title, create_time) -> index
    title_time_to_idx = {}
    for idx, c in enumerate(convos):
        t = c.get("title", "").strip()
        ct = c.get("create_time", 0)
        key = (t, ct)
        title_time_to_idx[key] = idx

    # Rebuild PILLAR_MAP with actual indices
    # We need to match catalog numbers to the export order
    # The catalog listing was sequential, so catalog #1 = export[0]
    # But the export might be in a different order than what was displayed
    # Let's just work with what we have

    extracted_count = 0
    skipped_count = 0

    for idx, convo in enumerate(convos):
        catalog_num = idx + 1  # 1-based catalog number

        # Apply filters
        if catalog_filter and catalog_num not in catalog_filter:
            continue

        pillar = PILLAR_MAP.get(catalog_num, None)
        if pillar_filter and pillar not in pillar_filter:
            continue
        if pillar_filter is None and pillar is None:
            continue  # Skip unmapped unless explicitly targeting

        title = convo.get("title", "Untitled").strip()
        create_time = convo.get("create_time", 0)
        created_dt = datetime.fromtimestamp(create_time, tz=timezone.utc) if create_time else None
        date_str = created_dt.strftime("%Y-%m-%d") if created_dt else "unknown"

        # Determine output path
        if pillar:
            output_dir = OUTPUT_BASE / pillar
        else:
            output_dir = OUTPUT_BASE / "UNROUTED"

        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{date_str}_{catalog_num:03d}_{slugify(title)}.md"
        filepath = output_dir / filename

        # Write
        doc = format_conversation(convo, catalog_num)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(doc)

        msg_count = len(flatten_messages(convo))
        print(f"  [{pillar or 'UNROUTED':15s}] #{catalog_num:3d} {title[:50]:50s} ({msg_count:3d} msgs) → {filename}")
        extracted_count += 1

    print(f"\n{'='*60}")
    print(f"Extracted: {extracted_count} conversations")
    print(f"Output: {OUTPUT_BASE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract ChatGPT conversations by pillar")
    parser.add_argument("--pillar", help="Single pillar to extract (e.g. '04_CODEX')")
    parser.add_argument("--priority", help="Priority tier: 1 (pillar convos), 2 (char/arch), 3 (infra)")
    parser.add_argument("--convo", help="Comma-separated list of catalog numbers")
    parser.add_argument("--sample", type=int, help="Extract N sample convos per pillar")
    args = parser.parse_args()

    pillar_filter = [args.pillar] if args.pillar else None

    catalog_filter = None
    if args.convo:
        catalog_filter = set(int(x.strip()) for x in args.convo.split(","))

    extract(pillar_filter=pillar_filter, catalog_filter=catalog_filter, sample_per_pillar=args.sample)
