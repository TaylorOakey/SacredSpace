#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  CHATGPT EXPORT PARSER — SacredSpace OS              ║
║  Converts ChatGPT ZIP export → Obsidian-ready .md    ║
║  Routes by pillar keyword, tags for canon pipeline   ║
╚══════════════════════════════════════════════════════╝
Usage:
    python3 chatgpt_export_parser.py --zip "D:/path/to/export.zip"
    # Or if already unzipped:
    python3 chatgpt_export_parser.py --json "D:/path/to/conversations.json"
    # Custom output:
    python3 chatgpt_export_parser.py --zip "..." --output "D:/SacredSpace_OS/_RAW/chatgpt_sessions"

WSL usage:
    python3 chatgpt_export_parser.py --zip "/mnt/d/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/CREATION_LAB/IMAGE_ARCHIVE/GEMINI/export.zip"
"""

import os
import json
import zipfile
import argparse
import re
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# PILLAR ROUTING — keyword → pillar folder
# ─────────────────────────────────────────────

PILLAR_MAP = {
    "01_OBSIDIAN_VAULTS": [
        "obsidian vault", "obsidian note", "obsidian plugin", "obsidian canvas",
        "obsidian graph", "vault note", "vault file", "vault folder",
        "daily note", "backlink", "wikilink", "[[", "obsidian rest",
        "vault search", "dataview", "templater",
    ],
    "02_COUNCIL_GROVE": [
        "council grove", "mission control", "council session", "handoff ritual",
        "sacred ledger", "icaris quartet", "council seat", "agent quartet",
        "asher", "elias", "aurora", "iris", "multi-agent", "ai workflow",
        "opencode",
    ],
    "03_NEURAL_FOREST": [
        "neural forest", "omniparse", "neural network", "machine learning",
        "florence", "whisper model", "torch", "pytorch", "hugging face",
        "transformer", "embedding model", "fine-tune", "training run",
        "model weights", "inference engine", "cuda", "gpu training",
    ],
    "04_SACRED_CODEX": [
        "sacred codex", "codex entry", "canon gate", "canon entry",
        "source of truth", "lock in", "make official", "make this official",
        "canonize", "is confirmed", "final decision", "we decided",
        "architecture decision", "sacredspace os", "nine pillar",
        "system design", "immutable", "icaris",
    ],
    "05_MEMORY_ENGINE": [
        "memory engine", "memory mote", "chromadb", "chroma db",
        "sqlite", "sacred memory", "vector store", "rag pipeline",
        "long-term memory", "mote", "store memory", "memory system",
        "chroma collection",
    ],
    "06_AGENT_LAYER": [
        "agent layer", "hermes", "fastapi", "api route", "api endpoint",
        "claude code", "agent config", "mcp server", "tool use",
        "bash script", "python script", "deploy script",
        "wsl2 setup", "docker", "uvicorn", "sacred spine",
    ],
    "07_SOCIAL_MOTHERSHIP": [
        "social mothership", "instagram", "twitter", "tiktok",
        "discord", "telegram", "social media", "content strategy",
        "broadcast", "audience", "community building", "sacred sounds",
        "platform strategy",
    ],
    "08_LEARNING_PATH": [
        "learning path", "notebooklm", "study plan", "course outline",
        "curriculum", "lesson plan", "tutorial", "ai engineering",
        "how does", "what is", "explain this", "maestro", "aas",
        "learning spine", "study session",
    ],
    "09_SACRED_MARKET": [
        "sacred market", "revenue", "crowdfund", "pricing model",
        "etsy", "printify", "gelato", "business model", "product listing",
        "market strategy", "kickstarter", "indiegogo", "storefront",
    ],
}

PILLAR_COLORS = {
    "01_OBSIDIAN_VAULTS":   "#A78BFA",
    "02_COUNCIL_GROVE":     "#533AB7",
    "03_NEURAL_FOREST":     "#1D9E75",
    "04_SACRED_CODEX":      "#7F77DD",
    "05_MEMORY_ENGINE":     "#BA7517",
    "06_AGENT_LAYER":       "#0F6E56",
    "07_SOCIAL_MOTHERSHIP": "#D4537E",
    "08_LEARNING_PATH":     "#639922",
    "09_SACRED_MARKET":     "#D85A30",
}

CANON_TRIGGER_WORDS = [
    "canon", "canonize", "lock in", "make this official",
    "sacredspace os", "nine pillar", "arcana grid", "1111 flow",
    "source of truth", "immutable", "architecture", "is confirmed",
    "final decision", "we decided", "grama", "gematria",
    "neural forest", "icaris", "sacred messages", "jenga",
    "holographic memory", "learning spine",
]

RAW_TRIGGER_WORDS = [
    "draft", "rough", "brainstorm", "explore", "idea",
    "maybe", "what if", "thinking about", "considering",
    "not sure", "could we", "help me think",
]


# ─────────────────────────────────────────────
# PARSE conversations.json
# ─────────────────────────────────────────────

def extract_messages(conversation: dict) -> list[dict]:
    """Extract ordered messages from ChatGPT conversation mapping."""
    mapping = conversation.get("mapping", {})
    messages = []

    for node_id, node in mapping.items():
        msg = node.get("message")
        if not msg:
            continue
        role = msg.get("author", {}).get("role", "")
        if role not in ("user", "assistant", "system"):
            continue
        content = msg.get("content", {})
        parts = content.get("parts", [])
        text_parts = []
        for p in parts:
            if isinstance(p, str):
                text_parts.append(p)
            elif isinstance(p, dict) and p.get("content_type") == "text":
                text_parts.append(p.get("text", ""))
        text = "\n".join(text_parts).strip()
        if not text:
            continue
        create_time = msg.get("create_time") or 0
        messages.append({
            "role": role,
            "text": text,
            "time": create_time,
        })

    messages.sort(key=lambda m: m["time"])
    return messages


def detect_pillar(title: str, messages: list[dict]) -> str:
    """Score conversation against each pillar's keywords."""
    combined = (title + " " + " ".join(m["text"][:300] for m in messages[:6])).lower()
    scores = {}
    for pillar, keywords in PILLAR_MAP.items():
        score = sum(combined.count(kw) for kw in keywords)
        if score > 0:
            scores[pillar] = score
    if not scores:
        return "04_SACRED_CODEX"
    return max(scores, key=scores.get)


def detect_pipeline_stage(title: str, messages: list[dict]) -> str:
    """Heuristic: RAW, DISTILLED_CANDIDATE, or CANON_CANDIDATE."""
    combined = (title + " " + " ".join(m["text"][:500] for m in messages)).lower()
    canon_score = sum(combined.count(kw) for kw in CANON_TRIGGER_WORDS)
    raw_score = sum(combined.count(kw) for kw in RAW_TRIGGER_WORDS)

    if canon_score >= 3:
        return "CANON_CANDIDATE"
    elif raw_score >= 2:
        return "RAW"
    else:
        return "DISTILLED_CANDIDATE"


def sanitize_filename(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '_', s.strip())
    return s[:80] or "Untitled"


def format_timestamp(ts) -> str:
    if not ts:
        return "unknown"
    try:
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d %H:%M")
    except Exception:
        return "unknown"


def format_date(ts) -> str:
    if not ts:
        return "0000-00-00"
    try:
        return datetime.fromtimestamp(float(ts)).strftime("%Y-%m-%d")
    except Exception:
        return "0000-00-00"


def build_markdown(conversation: dict, messages: list[dict], pillar: str, stage: str) -> str:
    """Render a conversation as Obsidian-ready markdown."""
    title = conversation.get("title", "Untitled")
    create_time = conversation.get("create_time")
    update_time = conversation.get("update_time")
    conv_id = conversation.get("id", "")

    date_str = format_date(create_time)
    created_at = format_timestamp(create_time)
    updated_at = format_timestamp(update_time)

    lines = [
        "---",
        f'title: "{title}"',
        f"source: chatgpt",
        f"id: {conv_id[:16]}",
        f"created: {created_at}",
        f"updated: {updated_at}",
        f"pillar: {pillar}",
        f"stage: {stage}",
        f"tags: [chatgpt, council-grove, {stage.lower().replace('_', '-')}]",
        "---",
        "",
        f"# {title}",
        f"> **Source:** ChatGPT  |  **Date:** {date_str}  |  **Stage:** `{stage}`  |  **Pillar:** `{pillar}`",
        "",
        "---",
        "",
    ]

    if stage == "CANON_CANDIDATE":
        lines += [
            "> [!important] CANON CANDIDATE",
            "> This conversation contains potential canon material. Review and distill before promoting.",
            "",
        ]
    elif stage == "RAW":
        lines += [
            "> [!note] RAW",
            "> This is raw exploration. Distill key insights before referencing.",
            "",
        ]

    lines.append("## Transcript\n")
    for msg in messages:
        role_label = "∆ **USER**" if msg["role"] == "user" else "⚙ **ASSISTANT**"
        time_label = format_timestamp(msg["time"])
        lines.append(f"### {role_label} — {time_label}\n")
        lines.append(msg["text"])
        lines.append("\n---\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def run(zip_path: str = None, json_path: str = None, output_root: str = None):
    # ── Locate conversations.json ──
    if zip_path:
        zip_path = Path(zip_path)
        if not zip_path.exists():
            print(f"[ERROR] ZIP not found: {zip_path}")
            return
        print(f"[∆] Extracting ZIP: {zip_path.name}")
        with zipfile.ZipFile(zip_path, "r") as z:
            names = z.namelist()
            json_name = next((n for n in names if n.endswith("conversations.json")), None)
            if not json_name:
                print(f"[ERROR] No conversations.json in ZIP. Found: {names}")
                return
            raw_json = z.read(json_name)
        conversations = json.loads(raw_json)
    elif json_path:
        json_path = Path(json_path)
        if not json_path.exists():
            print(f"[ERROR] JSON not found: {json_path}")
            return
        with open(json_path, "r", encoding="utf-8") as f:
            conversations = json.load(f)
    else:
        print("[ERROR] Provide --zip or --json")
        return

    print(f"[∆] Found {len(conversations)} conversations")

    # ── Output root ──
    if output_root:
        out_root = Path(output_root)
    else:
        source = Path(zip_path or json_path)
        out_root = source.parent / "_RAW" / "chatgpt_sessions"

    # ── Create pillar subdirs ──
    pillar_dirs = {}
    for pillar in PILLAR_MAP.keys():
        d = out_root / pillar
        d.mkdir(parents=True, exist_ok=True)
        pillar_dirs[pillar] = d

    # ── Summary tracking ──
    counts = {p: 0 for p in pillar_dirs}
    stages = {"CANON_CANDIDATE": 0, "DISTILLED_CANDIDATE": 0, "RAW": 0}
    errors = []

    # ── Process each conversation ──
    for i, conv in enumerate(conversations):
        try:
            title = conv.get("title", "Untitled")
            messages = extract_messages(conv)
            if not messages:
                continue

            pillar = detect_pillar(title, messages)
            stage = detect_pipeline_stage(title, messages)
            md = build_markdown(conv, messages, pillar, stage)

            date_prefix = format_date(conv.get("create_time"))
            safe_title = sanitize_filename(title)
            filename = f"{date_prefix}_{safe_title}.md"
            out_path = pillar_dirs[pillar] / filename

            counter = 1
            while out_path.exists():
                out_path = pillar_dirs[pillar] / f"{date_prefix}_{safe_title}_{counter}.md"
                counter += 1

            with open(out_path, "w", encoding="utf-8") as f:
                f.write(md)

            counts[pillar] += 1
            stages[stage] += 1

            if (i + 1) % 50 == 0:
                print(f"  ... processed {i + 1}/{len(conversations)}")

        except Exception as e:
            errors.append((conv.get("title", "?"), str(e)))

    # ── Print summary ──
    print("\n" + "═" * 52)
    print("  ∆ CHATGPT EXPORT PARSE COMPLETE")
    print("═" * 52)
    print(f"  Total conversations: {len(conversations)}")
    print(f"  Output root: {out_root}\n")
    print("  BY PILLAR:")
    for pillar, count in counts.items():
        if count > 0:
            bar = "█" * min(count, 30)
            print(f"    {pillar:<28} {bar} {count}")
    print("\n  BY PIPELINE STAGE:")
    for stage, count in stages.items():
        print(f"    {stage:<28} {count}")
    if errors:
        print(f"\n  ERRORS ({len(errors)}):")
        for title, err in errors[:10]:
            print(f"    - {title[:40]}: {err}")
    print("\n  NEXT STEPS:")
    print("  1. Review CANON_CANDIDATE files → distill → promote to Obsidian vault")
    print("  2. Upload to Google Drive for NotebookLM ingestion")
    print("  3. Run: grep -r 'CANON_CANDIDATE' <output_root> for quick hit list")
    print("═" * 52 + "\n")

    # ── Write index ──
    index_lines = [
        "# ChatGPT Export Index",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> Total conversations: {len(conversations)}",
        "",
        "## By Pillar",
        "",
    ]
    for pillar, count in counts.items():
        if count > 0:
            index_lines.append(f"- [[{pillar}/]] — {count} conversations")
    index_lines += [
        "",
        "## By Stage",
        "",
        f"- CANON_CANDIDATE: {stages['CANON_CANDIDATE']}",
        f"- DISTILLED_CANDIDATE: {stages['DISTILLED_CANDIDATE']}",
        f"- RAW: {stages['RAW']}",
    ]
    with open(out_root / "_INDEX.md", "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))
    print(f"  Index written: {out_root / '_INDEX.md'}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ChatGPT Export → SacredSpace OS Markdown Parser")
    parser.add_argument("--zip",    type=str, help="Path to ChatGPT export .zip file")
    parser.add_argument("--json",   type=str, help="Path to conversations.json (if already unzipped)")
    parser.add_argument("--output", type=str, help="Output root directory (default: auto-detected next to input)")
    args = parser.parse_args()

    if not args.zip and not args.json:
        print("╔══════════════════════════════════════════════╗")
        print("║  SacredSpace OS — ChatGPT Export Parser      ║")
        print("╚══════════════════════════════════════════════╝")
        print()
        path = input("Drop your ZIP or JSON path here: ").strip().strip('"')
        if path.endswith(".zip"):
            run(zip_path=path)
        elif path.endswith(".json"):
            run(json_path=path)
        else:
            print("[ERROR] Unrecognized file type. Provide a .zip or conversations.json path.")
    else:
        run(zip_path=args.zip, json_path=args.json, output_root=args.output)
