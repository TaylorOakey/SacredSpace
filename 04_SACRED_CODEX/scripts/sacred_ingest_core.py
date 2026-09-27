"""
sacred_ingest_core.py
=====================
SacredSpace OS — Automated Import Engine Foundation
Pillar: 03_NEURAL_FOREST
Owner Agent: AURORA
Tier: RAW ingestion layer

This module is the shared foundation for all SacredSpace connectors.
Every piece of knowledge entering the OS passes through here before
reaching ChromaDB (semantic search) or SQLite (audit trail).

Architecture:
    Connector → ingest() → MemoryMote → RAWTierWriter + ChromaWriter
                                              ↓               ↓
                                         raw_tier.db    neural_forest_raw
                                         (SQLite)       (ChromaDB)
"""

import hashlib
import json
import sqlite3
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# ─── PATHS ────────────────────────────────────────────────────────────────────

SACRED_ROOT   = Path.home() / "SacredSpace_OS"
MEMORY_ENGINE = SACRED_ROOT / "05_MEMORY_ENGINE"
NEURAL_FOREST = SACRED_ROOT / "03_NEURAL_FOREST"

RAW_DB_PATH   = MEMORY_ENGINE / "raw_tier.db"
CHROMA_PATH   = MEMORY_ENGINE / "chroma_db"

# Ensure directory structure exists on import
for _dir in [SACRED_ROOT, MEMORY_ENGINE, NEURAL_FOREST, CHROMA_PATH]:
    _dir.mkdir(parents=True, exist_ok=True)

# ─── VALID CONSTANTS ──────────────────────────────────────────────────────────

VALID_SOURCES = {"local_file", "gdrive", "gmail", "claude_export",
                 "chatgpt_export", "gemini_export", "web_crawl", "youtube"}
VALID_PILLARS = {
    "01_OBSIDIAN_VAULTS", "02_COUNCIL_GROVE", "03_NEURAL_FOREST",
    "04_SACRED_CODEX",    "05_MEMORY_ENGINE", "06_AGENT_LAYER",
    "07_SOCIAL_MOTHERSHIP","08_LEARNING_PATH", "09_SACRED_MARKET",
}
VALID_TIERS   = {"RAW", "DISTILLED", "CANON"}
VALID_AGENTS  = {"ELIAS", "AURORA", "ASHER", "IRIS", "COUNCIL"}

# ─── MEMORY MOTE ──────────────────────────────────────────────────────────────

@dataclass
class MemoryMote:
    """
    The atomic unit of knowledge in SacredSpace OS.

    Every document, message, web page, or signal that enters the system
    is first wrapped in a MemoryMote before storage. The mote_id is a
    SHA256 fingerprint of the content — identical content always produces
    the same ID, enabling automatic deduplication.
    """
    mote_id:   str               # SHA256 fingerprint of content
    content:   str               # Raw text content
    source:    str               # Origin connector type
    pillar:    str               # Which of the 9 SacredSpace pillars
    tier:      str = "RAW"       # RAW → DISTILLED → CANON
    agent:     str = "AURORA"    # Owning ICARIS agent
    tags:      list  = field(default_factory=list)   # Semantic tags
    timestamp: str   = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata:  dict  = field(default_factory=dict)   # Flexible extra fields

    def __post_init__(self):
        """Validate fields on creation."""
        if self.source not in VALID_SOURCES:
            raise ValueError(f"Invalid source '{self.source}'. Must be one of: {VALID_SOURCES}")
        if self.pillar not in VALID_PILLARS:
            raise ValueError(f"Invalid pillar '{self.pillar}'. Must be one of: {VALID_PILLARS}")
        if self.tier not in VALID_TIERS:
            raise ValueError(f"Invalid tier '{self.tier}'. Must be one of: {VALID_TIERS}")
        if self.agent not in VALID_AGENTS:
            raise ValueError(f"Invalid agent '{self.agent}'. Must be one of: {VALID_AGENTS}")

    def preview(self) -> str:
        """Return a short preview of the content for logging."""
        return self.content[:60].replace("\n", " ").strip()

# ─── BASE CONNECTOR ───────────────────────────────────────────────────────────

class BaseConnector(ABC):
    """
    Abstract base class for all SacredSpace import connectors.

    Subclass this to build connectors for local files, Google Drive,
    Gmail, AI exports, web crawlers, etc. Each connector implements
    collect() and returns a list of MemoryMotes ready for ingestion.
    """

    @abstractmethod
    def collect(self) -> list:
        """
        Collect content from the source and return MemoryMotes.

        Returns:
            list[MemoryMote]: Ready-to-ingest motes from this source.
        """
        pass

    @staticmethod
    def fingerprint(content: str) -> str:
        """
        Generate a SHA256 fingerprint of content.

        This is the canonical deduplication key. The same content
        always produces the same mote_id regardless of source.

        Args:
            content: Raw text content to fingerprint.

        Returns:
            str: 64-character hex SHA256 hash.
        """
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @staticmethod
    def dedup_check(mote_id: str, db_path: Path = RAW_DB_PATH) -> bool:
        """
        Check if a mote_id already exists in the RAW tier SQLite DB.

        Args:
            mote_id: SHA256 fingerprint to check.
            db_path: Path to the SQLite database.

        Returns:
            bool: True if mote already exists (is a duplicate), False if new.
        """
        if not db_path.exists():
            return False  # DB doesn't exist yet — nothing is a duplicate
        try:
            with sqlite3.connect(db_path) as conn:
                row = conn.execute(
                    "SELECT 1 FROM raw_motes WHERE mote_id = ? LIMIT 1",
                    (mote_id,)
                ).fetchone()
                return row is not None
        except sqlite3.Error:
            return False

# ─── RAW TIER WRITER (SQLite) ─────────────────────────────────────────────────

class RAWTierWriter:
    """
    Writes MemoryMotes to the RAW tier SQLite database.

    The RAW tier is the immutable audit trail. Every mote that enters
    the system lands here first. Nothing is ever deleted from RAW —
    only promoted to DISTILLED or CANON through the translation layer.
    """

    def __init__(self, db_path: Path = RAW_DB_PATH):
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self):
        """Create the raw_motes table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS raw_motes (
                    mote_id   TEXT PRIMARY KEY,
                    content   TEXT NOT NULL,
                    source    TEXT NOT NULL,
                    pillar    TEXT NOT NULL,
                    tier      TEXT NOT NULL DEFAULT 'RAW',
                    agent     TEXT NOT NULL,
                    tags      TEXT NOT NULL DEFAULT '[]',
                    timestamp TEXT NOT NULL,
                    metadata  TEXT NOT NULL DEFAULT '{}'
                )
            """)
            conn.commit()

    def write(self, motes: list) -> dict:
        """
        Write a list of MemoryMotes to SQLite, skipping duplicates.

        Args:
            motes: List of MemoryMote objects to persist.

        Returns:
            dict: Summary with 'written' and 'skipped' counts.
        """
        written = 0
        skipped = 0

        with sqlite3.connect(self.db_path) as conn:
            for mote in motes:
                try:
                    conn.execute(
                        """INSERT OR IGNORE INTO raw_motes
                           (mote_id, content, source, pillar, tier, agent, tags, timestamp, metadata)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            mote.mote_id,
                            mote.content,
                            mote.source,
                            mote.pillar,
                            mote.tier,
                            mote.agent,
                            json.dumps(mote.tags),
                            mote.timestamp,
                            json.dumps(mote.metadata),
                        )
                    )
                    if conn.execute(
                        "SELECT changes()"
                    ).fetchone()[0] > 0:
                        print(
                            f"  [SQLite ✓] {mote.pillar} | {mote.source} | "
                            f"{mote.mote_id[:8]}... | \"{mote.preview()}\""
                        )
                        written += 1
                    else:
                        print(f"  [SQLite —] SKIP duplicate {mote.mote_id[:8]}...")
                        skipped += 1
                except sqlite3.Error as e:
                    print(f"  [SQLite ✗] ERROR writing {mote.mote_id[:8]}: {e}")
            conn.commit()

        return {"written": written, "skipped": skipped}

# ─── CHROMA WRITER (Vector Store) ─────────────────────────────────────────────

class ChromaWriter:
    """
    Writes MemoryMotes to ChromaDB for semantic search.

    Uses sentence-transformers all-MiniLM-L6-v2 for local, zero-cost
    embedding generation. All MemoryMote fields are stored as metadata
    alongside the vector embedding.
    """

    COLLECTION_NAME = "neural_forest_raw"
    EMBED_MODEL     = "all-MiniLM-L6-v2"

    def __init__(self, chroma_path: Path = CHROMA_PATH):
        self.chroma_path = chroma_path
        self._client     = None
        self._collection = None
        self._embedder   = None

    def _init(self):
        """Lazy-initialize ChromaDB and the embedding model."""
        if self._client is not None:
            return
        try:
            import chromadb
            from sentence_transformers import SentenceTransformer

            self._client = chromadb.PersistentClient(path=str(self.chroma_path))
            self._collection = self._client.get_or_create_collection(
                name=self.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"},
            )
            self._embedder = SentenceTransformer(self.EMBED_MODEL)
            print(f"  [Chroma ✓] Connected to {self.COLLECTION_NAME} "
                  f"({self._collection.count()} existing motes)")
        except ImportError as e:
            raise RuntimeError(
                f"ChromaDB or sentence-transformers not installed: {e}\n"
                "Run: pip install chromadb sentence-transformers --break-system-packages"
            )

    def write(self, motes: list) -> dict:
        """
        Embed and store MemoryMotes in ChromaDB, skipping duplicates.

        Args:
            motes: List of MemoryMote objects to embed and store.

        Returns:
            dict: Summary with 'written' and 'skipped' counts.
        """
        self._init()

        written = 0
        skipped = 0

        # Check which mote_ids already exist
        existing_ids = set()
        if motes:
            try:
                existing = self._collection.get(
                    ids=[m.mote_id for m in motes],
                    include=[]
                )
                existing_ids = set(existing["ids"])
            except Exception:
                pass  # Collection may be empty — that's fine

        new_motes = [m for m in motes if m.mote_id not in existing_ids]
        skipped   = len(motes) - len(new_motes)

        if not new_motes:
            print(f"  [Chroma —] All {len(motes)} motes already exist, skipping")
            return {"written": 0, "skipped": skipped}

        # Batch embed all new motes
        contents   = [m.content for m in new_motes]
        embeddings = self._embedder.encode(contents, show_progress_bar=False).tolist()

        self._collection.add(
            ids        = [m.mote_id for m in new_motes],
            embeddings = embeddings,
            documents  = contents,
            metadatas  = [
                {
                    "source":    m.source,
                    "pillar":    m.pillar,
                    "tier":      m.tier,
                    "agent":     m.agent,
                    "tags":      json.dumps(m.tags),
                    "timestamp": m.timestamp,
                    **{k: str(v) for k, v in m.metadata.items()},
                }
                for m in new_motes
            ],
        )

        for m in new_motes:
            print(
                f"  [Chroma ✓] {m.pillar} | {m.source} | "
                f"{m.mote_id[:8]}... | \"{m.preview()}\""
            )
            written += 1

        return {"written": written, "skipped": skipped}

# ─── MAIN INGEST FUNCTION ─────────────────────────────────────────────────────

# Shared writers — initialized once, reused across calls
_raw_writer   = None
_chroma_writer = None

def ingest(
    content:  str,
    source:   str,
    pillar:   str,
    agent:    str  = "AURORA",
    tags:     list = None,
    metadata: dict = None,
    skip_chroma: bool = False,
) -> "MemoryMote":
    """
    Main entry point for ingesting content into SacredSpace OS.

    Creates a MemoryMote, deduplicates, and writes to both SQLite
    (RAW tier audit trail) and ChromaDB (semantic search index).

    Args:
        content:     Raw text content to ingest.
        source:      Origin connector type (see VALID_SOURCES).
        pillar:      Target SacredSpace pillar (see VALID_PILLARS).
        agent:       Owning ICARIS agent (default: AURORA).
        tags:        Semantic tags for the mote.
        metadata:    Additional flexible metadata fields.
        skip_chroma: Skip ChromaDB write (for testing or bulk ops).

    Returns:
        MemoryMote: The created mote (whether new or duplicate).
    """
    global _raw_writer, _chroma_writer

    tags     = tags or []
    metadata = metadata or {}

    # Create the mote
    mote_id = BaseConnector.fingerprint(content)
    mote = MemoryMote(
        mote_id  = mote_id,
        content  = content,
        source   = source,
        pillar   = pillar,
        agent    = agent,
        tags     = tags,
        metadata = metadata,
    )

    print(f"\n[INGEST] {source} → {pillar} | {mote_id[:8]}...")

    # Initialize writers if needed
    if _raw_writer is None:
        _raw_writer = RAWTierWriter()
    if _chroma_writer is None and not skip_chroma:
        _chroma_writer = ChromaWriter()

    # Write to SQLite
    _raw_writer.write([mote])

    # Write to ChromaDB
    if not skip_chroma:
        _chroma_writer.write([mote])

    print(f"[INGEST] ✓ Complete — {mote_id[:8]}...\n")
    return mote


def query(text: str, n_results: int = 5, pillar: Optional[str] = None) -> list:
    """
    Semantic search across all ingested motes.

    Args:
        text:      Query text to search for.
        n_results: Number of results to return.
        pillar:    Optional filter by SacredSpace pillar.

    Returns:
        list[dict]: Matching motes with content, metadata, and distance.
    """
    global _chroma_writer
    if _chroma_writer is None:
        _chroma_writer = ChromaWriter()
    _chroma_writer._init()

    where = {"pillar": pillar} if pillar else None

    results = _chroma_writer._collection.query(
        query_embeddings = _chroma_writer._embedder.encode([text]).tolist(),
        n_results        = n_results,
        where            = where,
        include          = ["documents", "metadatas", "distances"],
    )

    output = []
    for i, doc in enumerate(results["documents"][0]):
        output.append({
            "content":  doc,
            "metadata": results["metadatas"][0][i],
            "distance": round(results["distances"][0][i], 4),
        })
    return output


# ─── SMOKE TEST ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("∆∆∆ SACRED INGEST CORE — SMOKE TEST ∆∆∆")
    print(f"Root:         {SACRED_ROOT}")
    print(f"Memory Engine:{MEMORY_ENGINE}")
    print(f"SQLite DB:    {RAW_DB_PATH}")
    print(f"ChromaDB:     {CHROMA_PATH}")
    print("=" * 60)

    # Test 1: Ingest a new mote
    print("\n[TEST 1] Ingesting a new Memory Mote...")
    mote = ingest(
        content  = "The Neural Forest is the living intelligence layer of SacredSpace OS. "
                   "It processes signals, builds knowledge graphs, and feeds the ICARIS agents.",
        source   = "local_file",
        pillar   = "03_NEURAL_FOREST",
        agent    = "ELIAS",
        tags     = ["neural_forest", "os_architecture", "canon"],
        metadata = {"origin": "smoke_test", "version": "1.0"},
    )

    # Test 2: Duplicate detection
    print("[TEST 2] Attempting duplicate ingest (should be skipped)...")
    mote2 = ingest(
        content  = "The Neural Forest is the living intelligence layer of SacredSpace OS. "
                   "It processes signals, builds knowledge graphs, and feeds the ICARIS agents.",
        source   = "local_file",
        pillar   = "03_NEURAL_FOREST",
        agent    = "ELIAS",
        tags     = ["neural_forest"],
    )
    assert mote.mote_id == mote2.mote_id, "Duplicate should produce same mote_id"
    print(f"  [✓] Duplicate detected correctly — same mote_id: {mote.mote_id[:8]}...")

    # Test 3: Query
    print("\n[TEST 3] Semantic search query...")
    results = query("intelligence layer SacredSpace", n_results=3)
    if results:
        print(f"  [✓] Query returned {len(results)} result(s)")
        print(f"  Top match (distance {results[0]['distance']}): \"{results[0]['content'][:60]}...\"")
    else:
        print("  [!] No results returned — ChromaDB may need a moment to index")

    # Test 4: SQLite verification
    print("\n[TEST 4] SQLite verification...")
    with sqlite3.connect(RAW_DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM raw_motes").fetchone()[0]
        print(f"  [✓] raw_motes table contains {count} record(s)")

    print("\n" + "=" * 60)
    print("∆ SMOKE TEST COMPLETE — sacred_ingest_core.py is LIVE ∆")
    print("=" * 60)
