#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  CLAUDE EXPORT PARSER — SacredSpace OS               ║
║  Converts Claude.ai export → Obsidian-ready .md      ║
║  Supports: .zip (conversations.json), raw .json,     ║
║            archive_browser.html (best-effort)        ║
║  Routes to real nine SacredSpace OS pillars          ║
╚══════════════════════════════════════════════════════╝
Usage:
    python3 claude_export_parser.py --zip "/mnt/d/path/to/export.zip"
    python3 claude_export_parser.py --json "/mnt/d/path/to/conversations.json"
    python3 claude_export_parser.py --html "/mnt/d/path/to/archive_browser.html"
    python3 claude_export_parser.py --zip "..." --output "/mnt/d/SacredSpace_OS/_RAW/claude_sessions"

WSL usage:
    python3 claude_export_parser.py --zip "/mnt/d/SacredSpace_OS/_RAW/claude_export.zip"
"""

import os
import json
import zipfile
import argparse
import re
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# PILLAR ROUTING — keyword → real nine pillars
# ─────────────────────────────────────────────
# VAULT RULE: bare "vault" is too broad — it matches finance, storage, and
# generic references across conversations. Only compound phrases that tie
# directly to Obsidian note-taking context route to 01_CORE.

PILLAR_MAP = {
    "01_CORE": [
        "obsidian vault", "obsidian note", "obsidian plugin", "obsidian canvas",
        "obsidian graph", "vault note", "vault file", "vault folder",
        "daily note", "backlink", "wikilink", "[[", "obsidian rest",
        "vault search", "dataview", "templater",
    ],
    "02_SYSTEMS": [
        "council grove", "mission control", "council session", "handoff ritual",
        "sacred ledger", "icaris quartet", "council seat", "agent quartet",
        "asher", "elias", "aurora", "iris", "multi-agent", "ai workflow",
        "opencode",
    ],
    "03_NEURAL": [
        "neural forest", "omniparse", "neural network", "machine learning",
        "florence", "whisper model", "torch", "pytorch", "hugging face",
        "transformer", "embedding model", "fine-tune", "training run",
        "model weights", "inference engine", "cuda", "gpu training",
    ],
    "04_CODEX": [
        "sacred codex", "codex entry", "canon gate", "canon entry",
        "source of truth", "lock in", "make official", "make this official",
        "canonize", "is confirmed", "final decision", "we decided",
        "architecture decision", "sacredspace os", "nine pillar",
        "system design", "immutable", "icaris",
    ],
    "05_MEMORY": [
        "memory engine", "memory mote", "chromadb", "chroma db",
        "sqlite", "sacred memory", "vector store", "rag pipeline",
        "long-term memory", "mote", "store memory", "memory system",
        "chroma collection",
    ],
    "06_AGENTS": [
        "agent layer", "hermes", "fastapi", "api route", "api endpoint",
        "claude code", "agent config", "mcp server", "tool use",
        "bash script", "python script", "deploy script",
        "wsl2 setup", "docker", "uvicorn", "sacred spine",
    ],
    "07_SOCIAL": [
        "social mothership", "instagram", "twitter", "tiktok",
        "discord", "telegram", "social media", "content strategy",
        "broadcast", "audience", "community building", "sacred sounds",
        "platform strategy",
    ],
    "08_LEARNING": [
        "learning path", "notebooklm", "study plan", "course outline",
        "curriculum", "lesson plan", "tutorial", "ai engineering",
        "how does", "what is", "explain this", "maestro", "aas",
        "learning spine", "study session",
    ],
    "09_MARKET": [
        "sacred market", "revenue", "crowdfund", "pricing model",
        "etsy", "printify", "gelato", "business model", "product listing",
        "market strategy", "kickstarter", "indiegogo", "storefront",
    ],
}

PILLAR_COLORS = {
    "01_CORE":   "#A78BFA",
    "02_SYSTEMS":     "#533AB7",
    "03_NEURAL":     "#1D9E75",
    "04_CODEX":      "#7F77DD",
    "05_MEMORY":     "#BA7517",
    "06_AGENTS":       "#0F6E56",
    "07_SOCIAL": "#D4537E",
    "08_LEARNING":     "#639922",
    "09_MARKET":     "#D85A30",
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
# PARSE Claude.ai conversations.json
# ─────────────────────────────────────────────

def extract_messages(conversation: dict) -> list[dict]:
    """Extract ordered messages from a Claude.ai conversation dict."""
    result = []
    for m in conversation.get("chat_messages", []):
        sender = m.get("sender", "")
        if sender not in ("human", "assistant"):
            continue
        # Primary: top-level "text" string
        text = m.get("text", "")
        # Fallback: "content" array of typed blocks
        if not text:
            for block in m.get("content", []):
                if isinstance(block, dict) and block.get("type") == "text":
                    text += block.get("text", "")
        text = text.strip()
        if not text:
            continue
        result.append({
            "role": "user" if sender == "human" else "assistant",
            "text": text,
            "time": m.get("created_at", ""),
        })
    return result  # Claude exports preserve message order


def detect_pillar(title: str, messages: list[dict]) -> str:
    """Score conversation against each pillar's keywords.
    Unmatched conversations default to 04_CODEX."""
    combined = (title + " " + " ".join(m["text"][:300] for m in messages[:6])).lower()
    scores = {}
    for pillar, keywords in PILLAR_MAP.items():
        score = sum(combined.count(kw) for kw in keywords)
        if score > 0:
            scores[pillar] = score
    if not scores:
        return "04_CODEX"
    return max(scores, key=scores.get)


def detect_pipeline_stage(title: str, messages: list[dict]) -> str:
    """Classify as RAW, DISTILLED_CANDIDATE, or CANON_CANDIDATE."""
    combined = (title + " " + " ".join(m["text"][:500] for m in messages)).lower()
    canon_score = sum(combined.count(kw) for kw in CANON_TRIGGER_WORDS)
    raw_score = sum(combined.count(kw) for kw in RAW_TRIGGER_WORDS)
    if canon_score >= 3:
        return "CANON_CANDIDATE"
    elif raw_score >= 2:
        return "RAW"
    return "DISTILLED_CANDIDATE"


# ─────────────────────────────────────────────
# TIMESTAMP HELPERS — Claude uses ISO 8601 strings
# ─────────────────────────────────────────────

def _parse_ts(ts) -> datetime | None:
    if not ts:
        return None
    if isinstance(ts, (int, float)):
        try:
            return datetime.fromtimestamp(float(ts))
        except Exception:
            return None
    if isinstance(ts, str):
        try:
            return datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
        except Exception:
            pass
    return None


def format_timestamp(ts) -> str:
    dt = _parse_ts(ts)
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "unknown"


def format_date(ts) -> str:
    dt = _parse_ts(ts)
    return dt.strftime("%Y-%m-%d") if dt else "0000-00-00"


def sanitize_filename(s: str) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '_', s.strip())
    return s[:80] or "Untitled"


# ─────────────────────────────────────────────
# MARKDOWN BUILDER
# ─────────────────────────────────────────────

def build_markdown(conversation: dict, messages: list[dict], pillar: str, stage: str) -> str:
    title = conversation.get("name", "Untitled")
    create_time = conversation.get("created_at")
    update_time = conversation.get("updated_at")
    conv_id = conversation.get("uuid", "")

    date_str = format_date(create_time)
    created_at = format_timestamp(create_time)
    updated_at = format_timestamp(update_time)

    lines = [
        "---",
        f'title: "{title}"',
        f"source: claude",
        f"id: {conv_id[:16]}",
        f"created: {created_at}",
        f"updated: {updated_at}",
        f"pillar: {pillar}",
        f"stage: {stage}",
        f"tags: [claude, export, {stage.lower().replace('_', '-')}]",
        "---",
        "",
        f"# {title}",
        f"> **Source:** Claude.ai  |  **Date:** {date_str}  |  **Stage:** `{stage}`  |  **Pillar:** `{pillar}`",
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
        role_label = "∆ **HUMAN**" if msg["role"] == "user" else "⚙ **CLAUDE**"
        time_label = format_timestamp(msg["time"])
        lines.append(f"### {role_label} — {time_label}\n")
        lines.append(msg["text"])
        lines.append("\n---\n")

    return "\n".join(lines)


# ─────────────────────────────────────────────
# HTML PARSER — archive_browser.html (best-effort)
# ─────────────────────────────────────────────

def parse_html_export(html_path: Path) -> list[dict]:
    """Extract conversations from Claude.ai HTML archive. Best-effort:
    1. Tries to pull embedded JSON (window.__CONVERSATIONS__ or similar).
    2. Falls back to BeautifulSoup structural parse.
    3. Falls back to regex extraction."""
    content = html_path.read_text(encoding="utf-8", errors="replace")

    # Attempt 1: embedded JSON blob (common in Claude archive pages)
    for pattern in [
        r'window\.__(?:DATA|CONVERSATIONS|EXPORT)__\s*=\s*(\[.+?\]);',
        r'<script[^>]*>\s*var conversations\s*=\s*(\[.+?\]);\s*</script>',
        r'"conversations"\s*:\s*(\[.+?\])\s*[,}]',
    ]:
        m = re.search(pattern, content, re.DOTALL)
        if m:
            try:
                data = json.loads(m.group(1))
                if isinstance(data, list) and data:
                    print(f"[∆] Extracted {len(data)} conversations from embedded JSON")
                    return data
            except Exception:
                pass

    # Attempt 2: BeautifulSoup structural parse
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")
        conversations = []
        for conv_el in soup.select(".conversation, [data-testid='conversation']"):
            title_el = conv_el.select_one("h1, h2, .title, .conversation-title")
            title = title_el.get_text(strip=True) if title_el else "Untitled"
            msgs = []
            for msg_el in conv_el.select(".message, [data-role]"):
                role = msg_el.get("data-role", "") or (
                    "human" if "human" in msg_el.get("class", []) else "assistant"
                )
                text = msg_el.get_text(separator="\n", strip=True)
                if text:
                    msgs.append({"sender": role, "text": text, "created_at": ""})
            if msgs:
                conversations.append({"name": title, "uuid": "", "chat_messages": msgs,
                                       "created_at": "", "updated_at": ""})
        if conversations:
            print(f"[∆] BeautifulSoup extracted {len(conversations)} conversations")
            return conversations
    except ImportError:
        print("[⚠] BeautifulSoup not installed — skipping structural parse.")
        print("    Install with: pip install beautifulsoup4")

    # Attempt 3: regex text extraction (last resort)
    print("[⚠] Falling back to regex extraction — output may be incomplete.")
    titles = re.findall(r'<(?:h1|h2)[^>]*>([^<]{3,120})</(?:h1|h2)>', content)
    conversations = []
    for t in titles:
        conversations.append({
            "name": t.strip(),
            "uuid": "",
            "chat_messages": [],
            "created_at": "",
            "updated_at": "",
        })
    return conversations


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

def run(zip_path: str = None, json_path: str = None, html_path: str = None,
        output_root: str = None):
    conversations = []

    if zip_path:
        zp = Path(zip_path)
        if not zp.exists():
            print(f"[ERROR] ZIP not found: {zp}")
            return
        print(f"[∆] Extracting ZIP: {zp.name}")
        with zipfile.ZipFile(zp, "r") as z:
            names = z.namelist()
            json_name = next((n for n in names if n.endswith("conversations.json")), None)
            if not json_name:
                print(f"[ERROR] No conversations.json in ZIP. Found: {names}")
                return
            conversations = json.loads(z.read(json_name))
        source = zp

    elif json_path:
        jp = Path(json_path)
        if not jp.exists():
            print(f"[ERROR] JSON not found: {jp}")
            return
        with open(jp, "r", encoding="utf-8") as f:
            conversations = json.load(f)
        source = jp

    elif html_path:
        hp = Path(html_path)
        if not hp.exists():
            print(f"[ERROR] HTML not found: {hp}")
            return
        print(f"[∆] Parsing HTML archive: {hp.name}")
        conversations = parse_html_export(hp)
        source = hp

    else:
        print("[ERROR] Provide --zip, --json, or --html")
        return

    print(f"[∆] Found {len(conversations)} conversations")

    out_root = Path(output_root) if output_root else source.parent / "_RAW" / "claude_sessions"

    pillar_dirs = {}
    for pillar in PILLAR_MAP.keys():
        d = out_root / pillar
        d.mkdir(parents=True, exist_ok=True)
        pillar_dirs[pillar] = d

    counts = {p: 0 for p in pillar_dirs}
    stages = {"CANON_CANDIDATE": 0, "DISTILLED_CANDIDATE": 0, "RAW": 0}
    errors = []

    for i, conv in enumerate(conversations):
        try:
            title = conv.get("name", "Untitled")
            messages = extract_messages(conv)
            if not messages:
                continue

            pillar = detect_pillar(title, messages)
            stage = detect_pipeline_stage(title, messages)
            md = build_markdown(conv, messages, pillar, stage)

            date_prefix = format_date(conv.get("created_at"))
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
            errors.append((conv.get("name", "?"), str(e)))

    print("\n" + "═" * 52)
    print("  ∆ CLAUDE EXPORT PARSE COMPLETE")
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

    index_lines = [
        "# Claude.ai Export Index",
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
    parser = argparse.ArgumentParser(description="Claude.ai Export → SacredSpace OS Markdown Parser")
    parser.add_argument("--zip",    type=str, help="Path to Claude.ai export .zip file")
    parser.add_argument("--json",   type=str, help="Path to conversations.json (if already unzipped)")
    parser.add_argument("--html",   type=str, help="Path to archive_browser.html (best-effort)")
    parser.add_argument("--output", type=str, help="Output root directory (default: auto-detected next to input)")
    args = parser.parse_args()

    if not args.zip and not args.json and not args.html:
        print("╔══════════════════════════════════════════════╗")
        print("║  SacredSpace OS — Claude.ai Export Parser    ║")
        print("╚══════════════════════════════════════════════╝")
        print()
        path = input("Drop your ZIP, JSON, or HTML path here: ").strip().strip('"')
        if path.endswith(".zip"):
            run(zip_path=path)
        elif path.endswith(".json"):
            run(json_path=path)
        elif path.endswith(".html"):
            run(html_path=path)
        else:
            print("[ERROR] Unrecognized file type. Provide a .zip, .json, or .html path.")
    else:
        run(zip_path=args.zip, json_path=args.json, html_path=args.html,
            output_root=args.output)
