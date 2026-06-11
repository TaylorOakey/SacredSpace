#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  GOOGLE TAKEOUT PARSER — SacredSpace OS              ║
║  Routes Google Takeout exports → nine pillars        ║
║  Platforms: Drive · Gmail · YouTube · Keep · Photos  ║
╚══════════════════════════════════════════════════════╝
Usage:
    python3 google_takeout_parser.py --zip  "/mnt/d/path/to/takeout.zip"
    python3 google_takeout_parser.py --dir  "/mnt/d/path/to/Takeout/"
    python3 google_takeout_parser.py --dir  "..." --platforms drive,gmail,youtube,keep
    python3 google_takeout_parser.py --dir  "..." --output "/mnt/d/SacredSpace_OS/_RAW/takeout_sessions"

Sequencing note (from FORGE):
    Run Drive first — it sets the canonical folder structure.
    Run Photos last — 252GB+ requires manual triage gate.
"""

import os
import re
import json
import zipfile
import argparse
import mailbox
import mimetypes
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# PILLAR ROUTING — same map as claude/chatgpt parsers
# VAULT RULE: bare "vault" does NOT route to 01.
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

CANON_TRIGGER_WORDS = [
    "canon", "canonize", "lock in", "make this official",
    "sacredspace os", "nine pillar", "arcana grid", "1111 flow",
    "source of truth", "immutable", "architecture", "is confirmed",
    "final decision", "we decided", "grama", "gematria",
    "neural forest", "icaris", "sacred messages", "learning spine",
]

RAW_TRIGGER_WORDS = [
    "draft", "rough", "brainstorm", "explore", "idea",
    "maybe", "what if", "thinking about", "not sure", "help me think",
]

# Drive folders that map directly to a pillar (checked before keyword scoring)
DRIVE_FOLDER_OVERRIDES = {
    "01_obsidian": "01_OBSIDIAN_VAULTS",
    "obsidian":    "01_OBSIDIAN_VAULTS",
    "02_council":  "02_COUNCIL_GROVE",
    "council":     "02_COUNCIL_GROVE",
    "03_neural":   "03_NEURAL_FOREST",
    "neural":      "03_NEURAL_FOREST",
    "04_codex":    "04_SACRED_CODEX",
    "codex":       "04_SACRED_CODEX",
    "05_memory":   "05_MEMORY_ENGINE",
    "06_agent":    "06_AGENT_LAYER",
    "07_social":   "07_SOCIAL_MOTHERSHIP",
    "08_learning": "08_LEARNING_PATH",
    "09_market":   "09_SACRED_MARKET",
    "sacred market": "09_SACRED_MARKET",
}


# ─────────────────────────────────────────────
# ROUTING HELPERS
# ─────────────────────────────────────────────

def detect_pillar(text: str, folder_hint: str = "") -> str:
    """Score text against nine pillars. Folder hint checked first for Drive files."""
    if folder_hint:
        hint_lower = folder_hint.lower()
        for key, pillar in DRIVE_FOLDER_OVERRIDES.items():
            if key in hint_lower:
                return pillar

    combined = text.lower()
    scores = {}
    for pillar, keywords in PILLAR_MAP.items():
        score = sum(combined.count(kw) for kw in keywords)
        if score > 0:
            scores[pillar] = score
    if not scores:
        return "04_SACRED_CODEX"
    return max(scores, key=scores.get)


def detect_stage(text: str) -> str:
    combined = text.lower()
    canon = sum(combined.count(kw) for kw in CANON_TRIGGER_WORDS)
    raw = sum(combined.count(kw) for kw in RAW_TRIGGER_WORDS)
    if canon >= 3:
        return "CANON_CANDIDATE"
    if raw >= 2:
        return "RAW"
    return "DISTILLED_CANDIDATE"


def sanitize(s: str, maxlen: int = 80) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', s)
    s = re.sub(r'\s+', '_', s.strip())
    return s[:maxlen] or "Untitled"


def ts_to_dt(ts) -> datetime | None:
    if not ts:
        return None
    if isinstance(ts, (int, float)):
        try:
            return datetime.fromtimestamp(float(ts) / (1000 if float(ts) > 1e10 else 1))
        except Exception:
            return None
    if isinstance(ts, str):
        for fmt in ("%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ",
                    "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
            try:
                return datetime.strptime(ts.replace("+00:00", "Z").replace("Z", ""), fmt.replace("Z", ""))
            except Exception:
                pass
    return None


def fmt_date(ts) -> str:
    dt = ts_to_dt(ts)
    return dt.strftime("%Y-%m-%d") if dt else "0000-00-00"


def fmt_ts(ts) -> str:
    dt = ts_to_dt(ts)
    return dt.strftime("%Y-%m-%d %H:%M") if dt else "unknown"


def write_md(out_path: Path, content: str):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    counter = 1
    final = out_path
    while final.exists():
        final = out_path.with_stem(f"{out_path.stem}_{counter}")
        counter += 1
    with open(final, "w", encoding="utf-8") as f:
        f.write(content)
    return final


def frontmatter(title, source, date, pillar, stage, extra: dict = None) -> str:
    lines = [
        "---",
        f'title: "{title}"',
        f"source: {source}",
        f"created: {date}",
        f"pillar: {pillar}",
        f"stage: {stage}",
        f"tags: [takeout, {source}, {stage.lower().replace('_','-')}]",
    ]
    if extra:
        for k, v in extra.items():
            lines.append(f"{k}: {v}")
    lines += ["---", "", f"# {title}", ""]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# PLATFORM PARSERS
# ─────────────────────────────────────────────

def parse_drive(takeout_dir: Path, out_root: Path) -> dict:
    """
    Google Drive: parse all .gdoc/.gsheet/.gslide metadata JSON files
    and any .txt / .md / .html content files. Routes by folder name first,
    then content keyword scoring.
    """
    print("\n[∆] DRIVE — scanning...")
    drive_root = takeout_dir / "Google Drive"
    if not drive_root.exists():
        print("  ⚠ Google Drive folder not found in Takeout — skipping")
        return {}

    counts = {p: 0 for p in PILLAR_MAP}
    processed = 0
    skipped = 0

    for meta_file in drive_root.rglob("*.json"):
        try:
            with open(meta_file, encoding="utf-8", errors="replace") as f:
                meta = json.load(f)
        except Exception:
            skipped += 1
            continue

        title = meta.get("title") or meta.get("name") or meta_file.stem
        created = meta.get("createdTime") or meta.get("created", "")
        modified = meta.get("modifiedTime") or meta.get("modified", "")
        doc_url = meta.get("url") or meta.get("alternateLink") or ""
        mime = meta.get("mimeType", "")

        # Try to load paired content file (.txt, .md, .html)
        content = ""
        for ext in (".txt", ".md", ".html", ".csv"):
            sibling = meta_file.with_suffix(ext)
            if sibling.exists():
                try:
                    content = sibling.read_text(encoding="utf-8", errors="replace")[:2000]
                except Exception:
                    pass
                break

        folder_hint = str(meta_file.relative_to(drive_root).parent)
        score_text = f"{title} {folder_hint} {content}"
        pillar = detect_pillar(score_text, folder_hint)
        stage = detect_stage(score_text)

        date_str = fmt_date(created)
        fm = frontmatter(title, "google-drive", fmt_ts(created), pillar, stage,
                         {"modified": fmt_ts(modified), "mime": mime, "url": doc_url})
        body = f"{fm}\n> **Drive path:** `{folder_hint}`\n\n"
        if content:
            body += f"## Content Preview\n\n{content[:1500]}\n"

        out_file = out_root / pillar / f"{date_str}_{sanitize(title)}.md"
        write_md(out_file, body)
        counts[pillar] += 1
        processed += 1

    print(f"  Processed: {processed} | Skipped: {skipped}")
    return counts


def parse_gmail(takeout_dir: Path, out_root: Path) -> dict:
    """
    Gmail: parse .mbox files. Each email thread → one markdown file.
    Routes by subject + body snippet.
    """
    print("\n[∆] GMAIL — scanning...")
    mail_root = takeout_dir / "Mail"
    if not mail_root.exists():
        print("  ⚠ Mail folder not found in Takeout — skipping")
        return {}

    counts = {p: 0 for p in PILLAR_MAP}
    processed = 0

    for mbox_file in mail_root.rglob("*.mbox"):
        try:
            mbox = mailbox.mbox(str(mbox_file))
        except Exception as e:
            print(f"  ⚠ Could not open {mbox_file.name}: {e}")
            continue

        for msg in mbox:
            try:
                subject = str(msg.get("Subject", "No Subject"))
                date_str = str(msg.get("Date", ""))
                sender = str(msg.get("From", ""))

                # Extract text body
                body_text = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            try:
                                body_text = part.get_payload(decode=True).decode(
                                    part.get_content_charset() or "utf-8", errors="replace")[:2000]
                                break
                            except Exception:
                                pass
                else:
                    try:
                        body_text = msg.get_payload(decode=True).decode(
                            msg.get_content_charset() or "utf-8", errors="replace")[:2000]
                    except Exception:
                        pass

                score_text = f"{subject} {body_text[:500]}"
                pillar = detect_pillar(score_text)
                stage = detect_stage(score_text)

                # Parse date for filename
                from email.utils import parsedate_to_datetime
                try:
                    dt = parsedate_to_datetime(date_str)
                    file_date = dt.strftime("%Y-%m-%d")
                    created_fmt = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    file_date = "0000-00-00"
                    created_fmt = date_str

                fm = frontmatter(subject, "gmail", created_fmt, pillar, stage,
                                 {"from": f'"{sender}"'})
                body = f"{fm}\n**From:** {sender}\n\n## Body\n\n{body_text}\n"

                out_file = out_root / pillar / f"{file_date}_{sanitize(subject)}.md"
                write_md(out_file, body)
                counts[pillar] += 1
                processed += 1

            except Exception:
                continue

    print(f"  Processed: {processed} emails")
    return counts


def parse_youtube(takeout_dir: Path, out_root: Path) -> dict:
    """
    YouTube: parse watch-history.json and search-history.json.
    Groups by month. Defaults to 08_LEARNING_PATH; social content → 07.
    """
    print("\n[∆] YOUTUBE — scanning...")
    yt_root = takeout_dir / "YouTube and YouTube Music" / "history"
    if not yt_root.exists():
        # Try alternate path
        yt_root = takeout_dir / "YouTube" / "history"
    if not yt_root.exists():
        print("  ⚠ YouTube history folder not found — skipping")
        return {}

    counts = {p: 0 for p in PILLAR_MAP}
    processed = 0

    for hist_file in yt_root.glob("*.json"):
        try:
            with open(hist_file, encoding="utf-8", errors="replace") as f:
                entries = json.load(f)
        except Exception:
            continue

        if not isinstance(entries, list):
            continue

        hist_type = "watch" if "watch" in hist_file.name.lower() else "search"

        # Group entries by month
        by_month: dict[str, list] = {}
        for entry in entries:
            ts = entry.get("time", "")
            month = ts[:7] if ts else "0000-00"
            by_month.setdefault(month, []).append(entry)

        for month, items in sorted(by_month.items()):
            titles = [e.get("title", "") or e.get("titleUrl", "") for e in items[:50]]
            combined = " ".join(titles)
            pillar = detect_pillar(combined) if combined.strip() else "08_LEARNING_PATH"
            # YouTube defaults to learning unless content signals social
            if pillar == "04_SACRED_CODEX":
                pillar = "08_LEARNING_PATH"

            stage = "RAW"
            lines = [
                f"---",
                f"title: \"YouTube {hist_type.title()} History — {month}\"",
                f"source: youtube",
                f"created: {month}-01",
                f"pillar: {pillar}",
                f"stage: {stage}",
                f"tags: [takeout, youtube, {hist_type}]",
                f"---",
                f"",
                f"# YouTube {hist_type.title()} History — {month}",
                f"> {len(items)} entries",
                f"",
                f"## Entries",
                f"",
            ]
            for e in items:
                title = e.get("title", e.get("titleUrl", "Unknown"))
                url = e.get("titleUrl", "")
                time = e.get("time", "")[:16].replace("T", " ")
                lines.append(f"- [{title}]({url}) — {time}")

            out_file = out_root / pillar / f"{month}_youtube_{hist_type}.md"
            write_md(out_file, "\n".join(lines))
            counts[pillar] += 1
            processed += 1

    print(f"  Processed: {processed} monthly bundles")
    return counts


def parse_keep(takeout_dir: Path, out_root: Path) -> dict:
    """
    Google Keep: parse JSON note files. Each note → one markdown file.
    """
    print("\n[∆] KEEP — scanning...")
    keep_root = takeout_dir / "Keep"
    if not keep_root.exists():
        print("  ⚠ Keep folder not found in Takeout — skipping")
        return {}

    counts = {p: 0 for p in PILLAR_MAP}
    processed = 0

    for note_file in keep_root.glob("*.json"):
        try:
            with open(note_file, encoding="utf-8", errors="replace") as f:
                note = json.load(f)
        except Exception:
            continue

        title = note.get("title", "") or note_file.stem
        text_content = note.get("textContent", "")
        created_usec = note.get("createdTimestampUsec", 0)
        edited_usec = note.get("userEditedTimestampUsec", 0)
        is_pinned = note.get("isPinned", False)
        labels = [l.get("name", "") for l in note.get("labels", [])]
        is_archived = note.get("isArchived", False)
        is_trashed = note.get("isTrashed", False)

        if is_trashed:
            continue

        created_ts = int(created_usec) / 1_000_000 if created_usec else 0
        edited_ts = int(edited_usec) / 1_000_000 if edited_usec else 0

        score_text = f"{title} {' '.join(labels)} {text_content[:500]}"
        pillar = detect_pillar(score_text)
        stage = detect_stage(score_text)

        date_str = fmt_date(created_ts)
        created_fmt = fmt_ts(created_ts)
        edited_fmt = fmt_ts(edited_ts)

        # List items from Keep checklists
        list_items = note.get("listContent", [])
        checklist = ""
        if list_items:
            lines_cl = []
            for item in list_items:
                check = "x" if item.get("isChecked") else " "
                lines_cl.append(f"- [{check}] {item.get('text', '')}")
            checklist = "\n".join(lines_cl)

        fm = frontmatter(title or "Untitled Note", "google-keep", created_fmt, pillar, stage, {
            "edited": edited_fmt,
            "pinned": str(is_pinned).lower(),
            "archived": str(is_archived).lower(),
            "labels": f"[{', '.join(labels)}]" if labels else "[]",
        })

        body = fm
        if text_content:
            body += f"{text_content}\n"
        if checklist:
            body += f"\n## Checklist\n\n{checklist}\n"

        out_file = out_root / pillar / f"{date_str}_{sanitize(title or 'note')}.md"
        write_md(out_file, body)
        counts[pillar] += 1
        processed += 1

    print(f"  Processed: {processed} notes")
    return counts


def parse_photos(takeout_dir: Path, out_root: Path) -> dict:
    """
    Google Photos: index metadata JSON sidecars only. Does NOT copy image files.
    Each album → one markdown index. Manual triage gate required for 252GB+.
    """
    print("\n[∆] PHOTOS — indexing metadata only (no image copy)...")
    photos_root = takeout_dir / "Google Photos"
    if not photos_root.exists():
        print("  ⚠ Google Photos folder not found — skipping")
        return {}

    counts = {p: 0 for p in PILLAR_MAP}
    albums_indexed = 0
    total_photos = 0

    for album_dir in photos_root.iterdir():
        if not album_dir.is_dir():
            continue

        album_name = album_dir.name
        photo_meta = []

        for meta_file in album_dir.glob("*.json"):
            try:
                with open(meta_file, encoding="utf-8", errors="replace") as f:
                    m = json.load(f)
                photo_meta.append({
                    "title": m.get("title", meta_file.stem),
                    "description": m.get("description", ""),
                    "taken": m.get("photoTakenTime", {}).get("formatted", ""),
                    "url": m.get("url", ""),
                })
            except Exception:
                continue

        if not photo_meta:
            continue

        score_text = album_name + " " + " ".join(p["description"] for p in photo_meta[:10])
        pillar = detect_pillar(score_text)
        # Photos with no strong signal → archive under 01 (vault imagery)
        if pillar == "04_SACRED_CODEX":
            pillar = "01_OBSIDIAN_VAULTS"

        lines = [
            "---",
            f'title: "Photos — {album_name}"',
            "source: google-photos",
            f"pillar: {pillar}",
            "stage: RAW",
            "tags: [takeout, photos, triage-required]",
            "---",
            "",
            f"# Photos — {album_name}",
            f"> {len(photo_meta)} photos | **⚠ TRIAGE REQUIRED** — images not copied",
            "",
            "## Photo Index",
            "",
        ]
        for p in photo_meta:
            lines.append(f"- **{p['title']}** — {p['taken']}")
            if p["description"]:
                lines.append(f"  {p['description']}")

        out_file = out_root / pillar / f"PHOTOS_{sanitize(album_name)}.md"
        write_md(out_file, "\n".join(lines))
        counts[pillar] += 1
        albums_indexed += 1
        total_photos += len(photo_meta)

    print(f"  Albums indexed: {albums_indexed} | Photos catalogued: {total_photos}")
    print("  ⚠ Images NOT copied — manual triage required before moving 252GB+")
    return counts


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────

PLATFORM_PARSERS = {
    "drive":   parse_drive,
    "gmail":   parse_gmail,
    "youtube": parse_youtube,
    "keep":    parse_keep,
    "photos":  parse_photos,
}

# Canonical run order — Drive first (sets folder structure), Photos last
DEFAULT_ORDER = ["drive", "gmail", "youtube", "keep", "photos"]


def run(zip_path: str = None, dir_path: str = None,
        platforms: list[str] = None, output_root: str = None):

    # ── Locate Takeout root ──
    if zip_path:
        zp = Path(zip_path)
        if not zp.exists():
            print(f"[ERROR] ZIP not found: {zp}")
            return
        import tempfile, shutil
        tmp = Path(tempfile.mkdtemp(prefix="takeout_"))
        print(f"[∆] Extracting ZIP to {tmp} ...")
        with zipfile.ZipFile(zp, "r") as z:
            z.extractall(tmp)
        # Takeout ZIPs contain a top-level "Takeout/" folder
        takeout_dir = tmp / "Takeout"
        if not takeout_dir.exists():
            takeout_dir = tmp
        source = zp
    elif dir_path:
        takeout_dir = Path(dir_path)
        if not takeout_dir.exists():
            print(f"[ERROR] Directory not found: {takeout_dir}")
            return
        # Accept both bare dir and dir/Takeout/
        if (takeout_dir / "Takeout").exists():
            takeout_dir = takeout_dir / "Takeout"
        source = takeout_dir
    else:
        print("[ERROR] Provide --zip or --dir")
        return

    print(f"[∆] Takeout root: {takeout_dir}")

    # ── Output root ──
    if output_root:
        out_root = Path(output_root)
    else:
        out_root = Path(source).parent / "_RAW" / "takeout_sessions"

    for pillar in PILLAR_MAP:
        (out_root / pillar).mkdir(parents=True, exist_ok=True)

    # ── Select platforms ──
    active = platforms if platforms else DEFAULT_ORDER
    active = [p.lower().strip() for p in active]
    unknown = [p for p in active if p not in PLATFORM_PARSERS]
    if unknown:
        print(f"[WARN] Unknown platforms: {unknown} — valid: {list(PLATFORM_PARSERS)}")
    active = [p for p in active if p in PLATFORM_PARSERS]

    # ── Run each platform in order ──
    total_counts = {p: 0 for p in PILLAR_MAP}
    for platform in active:
        counts = PLATFORM_PARSERS[platform](takeout_dir, out_root)
        for pillar, n in counts.items():
            total_counts[pillar] += n

    # ── Summary ──
    grand_total = sum(total_counts.values())
    print("\n" + "═" * 52)
    print("  ∆ GOOGLE TAKEOUT PARSE COMPLETE")
    print("═" * 52)
    print(f"  Platforms run:   {', '.join(active)}")
    print(f"  Total documents: {grand_total}")
    print(f"  Output root:     {out_root}\n")
    print("  BY PILLAR:")
    for pillar, count in total_counts.items():
        if count > 0:
            bar = "█" * min(count, 30)
            print(f"    {pillar:<28} {bar} {count}")
    print("\n  NEXT STEPS:")
    print("  1. Review CANON_CANDIDATE files → promote to Obsidian vault")
    print("  2. Upload Drive docs to Google Drive canonical folders")
    print("  3. Index into ChromaDB: POST /memory/mote for each CANON_CANDIDATE")
    print("  4. Photos: manual triage before moving — do NOT bulk-copy 252GB+")
    print("═" * 52 + "\n")

    # ── Write index ──
    index_lines = [
        "# Google Takeout Index",
        f"> Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"> Platforms: {', '.join(active)}",
        f"> Total documents: {grand_total}",
        "",
        "## By Pillar",
        "",
    ]
    for pillar, count in total_counts.items():
        if count > 0:
            index_lines.append(f"- [[{pillar}/]] — {count} documents")
    with open(out_root / "_TAKEOUT_INDEX.md", "w", encoding="utf-8") as f:
        f.write("\n".join(index_lines))
    print(f"  Index written: {out_root / '_TAKEOUT_INDEX.md'}")


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Google Takeout → SacredSpace OS Markdown Parser")
    parser.add_argument("--zip",       type=str, help="Path to takeout-*.zip")
    parser.add_argument("--dir",       type=str, help="Path to extracted Takeout/ folder")
    parser.add_argument("--platforms", type=str,
                        help=f"Comma-separated platforms to run (default: all). "
                             f"Options: {','.join(DEFAULT_ORDER)}")
    parser.add_argument("--output",    type=str, help="Output root directory")
    args = parser.parse_args()

    platforms = [p.strip() for p in args.platforms.split(",")] if args.platforms else None

    if not args.zip and not args.dir:
        print("╔══════════════════════════════════════════════╗")
        print("║  SacredSpace OS — Google Takeout Parser      ║")
        print("╚══════════════════════════════════════════════╝")
        print(f"  Platforms: {', '.join(DEFAULT_ORDER)}")
        print()
        path = input("Drop your Takeout ZIP or folder path here: ").strip().strip('"')
        p = Path(path)
        if p.is_dir():
            run(dir_path=path, platforms=platforms)
        elif p.suffix == ".zip":
            run(zip_path=path, platforms=platforms)
        else:
            print("[ERROR] Provide a .zip or a Takeout/ directory path.")
    else:
        run(zip_path=args.zip, dir_path=args.dir,
            platforms=platforms, output_root=args.output)
