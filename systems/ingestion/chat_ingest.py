#!/usr/bin/env python3
"""SacredSpace Chat Ingest Engine — Phase 1a/1b
Ingests ChatGPT exports and Gemini archaeology into SQLite memory system.

Usage:
    python3 systems/ingestion/chat_ingest.py                    # Dry run
    python3 systems/ingestion/chat_ingest.py --write            # Actually store
    python3 systems/ingestion/chat_ingest.py --source gemini    # Only Gemini files
    python3 systems/ingestion/chat_ingest.py --source chatgpt   # Only ChatGPT files
    python3 systems/ingestion/chat_ingest.py --status           # Show processed count

In lakesh alakin. ∆
"""

import os, re, sys, json, hashlib, datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
SACRED_ROOT = Path("/mnt/d/SacredSpace_OS")
DB_PATH = SACRED_ROOT / "05_MEMORY_ENGINE" / "sacred_memory.db"
CHATGPT_DIR = SACRED_ROOT / "_RAW" / "chatgpt_sessions"
GEMINI_DIR = SACRED_ROOT / "_PENDING_REVIEW" / "GEMINI_ARCHAEOLOGY"

# Pillar name mapping: ChatGPT short → canonical
PILLAR_MAP = {
    "01_CORE": "01_OBSIDIAN_VAULTS",
    "02_SYSTEMS": "02_COUNCIL_GROVE",
    "03_NEURAL": "03_NEURAL_FOREST",
    "04_CODEX": "04_SACRED_CODEX",
    "05_MEMORY": "05_MEMORY_ENGINE",
    "06_AGENTS": "06_AGENT_LAYER",
    "07_SOCIAL": "07_SOCIAL_MOTHERSHIP",
    "08_LEARNING": "08_LEARNING_PATH",
    "09_MARKET": "09_SACRED_MARKET",
}

CHROMA_AVAILABLE = False
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    pass

# ── SQLite Helpers ─────────────────────────────────────────────────────────

def get_db():
    import sqlite3
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    # Ensure all tables exist
    conn.execute("""CREATE TABLE IF NOT EXISTS memory_motes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT NOT NULL,
        pillar TEXT,
        content TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'raw'
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS knowledge_artifacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        domain TEXT,
        content TEXT,
        source_conversation TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS ingested_files (
        path_hash TEXT PRIMARY KEY,
        filename TEXT,
        source TEXT,
        pillar TEXT,
        title TEXT,
        ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        mote_id INTEGER,
        artifact_id INTEGER
    )""")
    conn.commit()
    return conn

# ── Parsers ────────────────────────────────────────────────────────────────

def parse_chatgpt_file(filepath):
    """Parse a ChatGPT export file with YAML frontmatter."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Extract YAML frontmatter
    fm_match = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    metadata = {"title": "", "pillar": "", "stage": "raw", "tags": "", "date": ""}
    if fm_match:
        fm_text = fm_match.group(1)
        for line in fm_text.strip().split("\n"):
            if ":" in line:
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if key == "title":
                    metadata["title"] = val
                elif key == "pillar":
                    metadata["pillar"] = PILLAR_MAP.get(val.upper(), val)
                elif key == "stage":
                    metadata["stage"] = val
                elif key == "tags":
                    metadata["tags"] = val.strip("[]").replace('"', "").replace("'", "")
                elif key == "created":
                    metadata["date"] = val[:10] if val else ""

    # Extract body (after frontmatter)
    body = raw
    if fm_match:
        body = raw[fm_match.end():].strip()

    # Generate summary: first meaningful paragraph
    summary = _generate_summary(body, metadata)

    return metadata, body, summary

def parse_gemini_file(filepath):
    """Parse a Gemini archaeology export file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()

    # Extract title from first heading
    title_match = re.match(r"^#\s+(.+)", raw)
    title = title_match.group(1).strip() if title_match else filepath.stem

    # Extract date from catalog line
    date_match = re.search(r"Created:\s*(\d{4}-\d{2}-\d{2})", raw)
    date = date_match.group(1) if date_match else ""

    # Extract pillar from directory path
    pillar = ""
    for part in filepath.parts:
        for p in ["01_OBSIDIAN_VAULTS", "02_COUNCIL_GROVE", "03_NEURAL_FOREST",
                  "04_SACRED_CODEX", "05_MEMORY_ENGINE", "06_AGENT_LAYER",
                  "07_SOCIAL_MOTHERSHIP", "08_LEARNING_PATH", "09_SACRED_MARKET"]:
            if p in part:
                pillar = p
                break
        if pillar:
            break

    # Extract stage from tags/labels
    stage_match = re.search(r"Stage:\s*`?(\w+)", raw)
    stage = stage_match.group(1).lower() if stage_match else "raw"

    # Extract message count
    msg_match = re.search(r"\*\*(\d+)\s*messages?\*\*", raw)
    msg_count = int(msg_match.group(1)) if msg_match else 0

    # Extract tags
    tags_match = re.search(r"Tags:\s*(.+)", raw)
    tags = tags_match.group(1).strip() if tags_match else "gemini,archaeology"

    # Generate summary
    summary = _generate_gemini_summary(raw, title, msg_count)

    metadata = {
        "title": title, "pillar": pillar, "stage": stage,
        "tags": tags, "date": date, "message_count": msg_count
    }

    return metadata, raw, summary

def _generate_summary(body, metadata):
    """Extract first meaningful paragraph as summary."""
    lines = body.strip().split("\n")
    summary_parts = []
    in_code_block = False
    for line in lines:
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        stripped = line.strip()
        # Skip empty lines, headers, blockquotes, separators
        if not stripped or stripped.startswith("#") or stripped.startswith(">") or stripped.startswith("---"):
            if summary_parts and stripped == "":
                break  # Stop at first blank line after we have content
            continue
        summary_parts.append(stripped)
        if len(summary_parts) >= 5:  # First 5 meaningful lines
            break

    summary = " ".join(summary_parts) if summary_parts else metadata.get("title", "No summary")
    # Truncate
    if len(summary) > 500:
        summary = summary[:497] + "..."
    return summary

def _generate_gemini_summary(raw, title, msg_count):
    """Extract key content from Gemini archaeology file."""
    # Get first meaningful user message
    lines = raw.split("\n")
    summary_parts = []
    capture = False
    for i, line in enumerate(lines):
        if "Message" in line and "User" in line:
            capture = True
            continue
        if "Message" in line and "Assistant" in line:
            break
        if capture and line.strip() and not line.startswith("```"):
            summary_parts.append(line.strip())
            if len(summary_parts) >= 8:
                break

    summary = " ".join(summary_parts) if summary_parts else title
    if len(summary) > 500:
        summary = summary[:497] + "..."
    if msg_count:
        summary = f"[{msg_count} msgs] {summary}"
    return summary

# ── Storage ────────────────────────────────────────────────────────────────

def store_ingested(conn, metadata, body, summary, source, filepath, dry_run=True):
    """Store parsed content in memory system."""
    path_hash = hashlib.sha256(str(filepath).encode()).hexdigest()[:16]

    # Check if already ingested
    existing = conn.execute("SELECT mote_id, artifact_id FROM ingested_files WHERE path_hash=?", (path_hash,)).fetchone()
    if existing:
        return {"status": "skipped", "reason": "already ingested", "mote_id": existing["mote_id"]}

    now = datetime.datetime.utcnow().isoformat()
    title = metadata.get("title", filepath.stem)
    pillar = metadata.get("pillar", "UNKNOWN")
    tags = metadata.get("tags", source)
    date = metadata.get("date", now[:10])
    stage = metadata.get("stage", "raw")

    # Create entity name from title and date
    entity_name = f"{source.upper()}_{date}_{_safe_entity_name(title)}"

    # Store as memory_mote
    mote_id = None
    if not dry_run:
        cursor = conn.execute(
            "INSERT INTO memory_motes (entity, pillar, content, tags, status) VALUES (?, ?, ?, ?, ?)",
            (entity_name, pillar, summary, tags, stage)
        )
        mote_id = cursor.lastrowid

    # Store as knowledge_artifact for full body
    artifact_id = None
    body_preview = body[:5000]  # Store first 5000 chars
    if not dry_run:
        cursor = conn.execute(
            "INSERT INTO knowledge_artifacts (title, domain, content, source_conversation, tags) VALUES (?, ?, ?, ?, ?)",
            (title, pillar, body_preview, f"{source}: {filepath.name}", f"{tags},full-body")
        )
        artifact_id = cursor.lastrowid

    # Record in ingested_files
    if not dry_run:
        conn.execute(
            "INSERT INTO ingested_files (path_hash, filename, source, pillar, title, mote_id, artifact_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (path_hash, filepath.name, source, pillar, title, mote_id, artifact_id)
        )

    return {
        "status": "ingested" if not dry_run else "dry-run",
        "entity": entity_name,
        "pillar": pillar,
        "mote_id": mote_id,
        "artifact_id": artifact_id,
        "title": title,
        "date": date
    }

def _safe_entity_name(title):
    """Convert title to a safe entity name."""
    name = re.sub(r"[^a-zA-Z0-9\s]", " ", title)
    name = re.sub(r"\s+", "_", name.strip())
    return name[:60].upper()

# ── Scanner ────────────────────────────────────────────────────────────────

def scan_files(source="all"):
    """Yield (metadata, body, summary, source_label, filepath) for each file."""
    files = []

    if source in ("all", "chatgpt"):
        if CHATGPT_DIR.exists():
            for pillar_dir in sorted(CHATGPT_DIR.iterdir()):
                if pillar_dir.is_dir():
                    for f in sorted(pillar_dir.glob("*.md")):
                        files.append((f, "chatgpt", parse_chatgpt_file))

    if source in ("all", "gemini"):
        if GEMINI_DIR.exists():
            for pillar_dir in sorted(GEMINI_DIR.iterdir()):
                if pillar_dir.is_dir():
                    for f in sorted(pillar_dir.glob("*.md")):
                        files.append((f, "gemini", parse_gemini_file))

    for filepath, source_label, parser in files:
        try:
            metadata, body, summary = parser(filepath)
            yield metadata, body, summary, source_label, filepath
        except Exception as e:
            print(f"  ⚠ Error parsing {filepath.name}: {e}", file=sys.stderr)

# ── ChromaDB Integration ───────────────────────────────────────────────────

def get_chroma():
    """Get ChromaDB collection for vector storage."""
    if not CHROMA_AVAILABLE:
        return None
    try:
        client = chromadb.PersistentClient(
            path=str(SACRED_ROOT / "06_AGENT_LAYER" / "IRIS" / "chroma_db")
        )
        return client.get_or_create_collection("sacredspace_canon")
    except Exception:
        return None

def store_in_chroma(collection, metadata, body, title, filepath, dry_run=True):
    """Store in ChromaDB for semantic search."""
    if collection is None or dry_run:
        return False
    try:
        doc_id = hashlib.sha256(str(filepath).encode()).hexdigest()[:32]
        # Check if exists
        existing = collection.get(ids=[doc_id])
        if existing and existing["ids"]:
            return False
        collection.add(
            documents=[body[:5000]],
            metadatas=[{
                "title": title,
                "pillar": metadata.get("pillar", ""),
                "source": filepath.name,
                "date": metadata.get("date", "")
            }],
            ids=[doc_id]
        )
        return True
    except Exception:
        return False

# ── Main ───────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Ingest chat exports into SacredSpace memory system")
    parser.add_argument("--write", action="store_true", help="Actually store data (default: dry-run)")
    parser.add_argument("--source", choices=["all", "chatgpt", "gemini"], default="all", help="Which source to process")
    parser.add_argument("--status", action="store_true", help="Show ingestion status")
    args = parser.parse_args()

    conn = get_db()

    # Status mode
    if args.status:
        ingested = conn.execute("SELECT source, COUNT(*) as c FROM ingested_files GROUP BY source").fetchall()
        total_motes = conn.execute("SELECT COUNT(*) FROM memory_motes").fetchone()[0]
        total_artifacts = conn.execute("SELECT COUNT(*) FROM knowledge_artifacts").fetchone()[0]
        print(f"\n📊 Ingestion Status")
        print(f"{'='*50}")
        print(f"  Total memory motes:     {total_motes}")
        print(f"  Total knowledge artifacts: {total_artifacts}")
        for row in ingested:
            print(f"  {row['source']}: {row['c']} files ingested")
        print(f"{'='*50}")
        conn.close()
        return

    dry_run = not args.write
    mode = "🧪 DRY RUN" if dry_run else "⚡ LIVE INGEST"
    source_label = args.source.upper()

    print(f"\n{mode} — Source: {source_label}")
    print(f"{'='*50}")

    # Setup ChromaDB if available and not dry run
    chroma = None
    if not dry_run:
        chroma = get_chroma()
        if chroma is not None:
            print("  ChromaDB: connected")
        else:
            print("  ChromaDB: unavailable (install chromadb for vector search)")

    # Scan and process files
    stats = {"total": 0, "ingested": 0, "skipped": 0, "errors": 0}
    for metadata, body, summary, source_label, filepath in scan_files(args.source):
        stats["total"] += 1
        result = store_ingested(
            conn, metadata, body, summary, source_label, filepath,
            dry_run=dry_run
        )
        if result["status"] == "skipped":
            stats["skipped"] += 1
        elif result["status"] == "ingested":
            stats["ingested"] += 1
            if chroma:
                store_in_chroma(chroma, metadata, body, metadata.get("title", ""), filepath, dry_run=dry_run)

        # Progress indicator
        if stats["total"] % 25 == 0:
            print(f"  ... {stats['total']} files scanned", end="\r")

    # Commit if live
    if not dry_run:
        conn.commit()

    conn.close()

    # Report
    print(f"\n\n📊 Results")
    print(f"{'='*50}")
    print(f"  Total files scanned:  {stats['total']}")
    print(f"  Newly ingested:       {stats['ingested']}")
    print(f"  Already ingested:     {stats['skipped']}")
    print(f"  Errors:               {stats['errors']}")
    if dry_run and stats["total"] > 0:
        print(f"\n  ▶ Run with --write to commit these changes")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
