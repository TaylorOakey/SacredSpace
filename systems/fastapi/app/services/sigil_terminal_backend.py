"""Sacred Sigil Terminal — 9-Dimension Query Backend
In lakesh alakin. ∆
"""
import os
import json
import sqlite3
from pathlib import Path
from typing import Optional
from datetime import datetime

SACRED_ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))

# ── Dimension Definitions ──────────────────────────────────────────────────

DIMENSIONS = {
    "vault": {
        "name": "∞ VAULT",
        "description": "Your Obsidian knowledge & memories",
        "source": "ChromaDB vector search on vault",
        "color": "#8B5A8F",
        "icon": "📚",
    },
    "grove": {
        "name": "◊ GROVE",
        "description": "Council Grove — Agent routing & council records",
        "source": "SQLite council records + ChromaDB",
        "color": "#2D5016",
        "icon": "🌳",
    },
    "forest": {
        "name": "∆ FOREST",
        "description": "Neural Forest — Pattern discovery & lore",
        "source": "ChromaDB on 03_NEURAL graph outputs",
        "color": "#3A5C3A",
        "icon": "🌲",
    },
    "codex": {
        "name": "⊙ CODEX",
        "description": "Sacred Codex — Canonical rules & truth",
        "source": "ChromaDB on 04_CODEX",
        "color": "#8B7355",
        "icon": "📖",
    },
    "memory": {
        "name": "≈ MEMORY",
        "description": "Memory Engine — Persistent state & history",
        "source": "SQLite sacred_memory.db",
        "color": "#5A5A8F",
        "icon": "💎",
    },
    "agent": {
        "name": "♦ AGENT",
        "description": "Agent Layer — Spells & invocations",
        "source": "Hermes MCP tools + agent prompts",
        "color": "#8F5A5A",
        "icon": "✨",
    },
    "social": {
        "name": "⊗ SOCIAL",
        "description": "Social Mothership — Community & creation",
        "source": "ChromaDB on 07_SOCIAL",
        "color": "#5A8F8F",
        "icon": "👥",
    },
    "market": {
        "name": "⊜ MARKET",
        "description": "Sacred Market — Artifacts & exchange",
        "source": "SQLite + local market data",
        "color": "#8F8F5A",
        "icon": "🛍️",
    },
    "path": {
        "name": "Λ PATH",
        "description": "Learning Path — Growth & progress",
        "source": "Ollama inference / graphify path",
        "color": "#5A8F5A",
        "icon": "🎓",
    },
    "lore": {
        "name": "♰ LORE",
        "description": "Storyline Canon — Characters, nodes, episodes & archetypes",
        "source": "Story Engine — structured canon data from 01_CORE + 04_CODEX",
        "color": "#FF6B35",
        "icon": "📜",
    },
}


def get_dimensions():
    """Return all 9 dimension definitions."""
    return DIMENSIONS


def query_dimension(dimension_id: str, query: str, limit: int = 10):
    """Query a single dimension and return results.

    Real implementation hooks into the actual data sources.
    Falls back to file-scoped search when ChromaDB is unavailable.
    """
    dim = DIMENSIONS.get(dimension_id)
    if not dim:
        return {"error": f"Unknown dimension: {dimension_id}", "results": []}

    # Special handling for lore dimension — search story engine
    if dimension_id == "lore":
        from app.services import story_engine
        story_results = story_engine.search_story(query, limit)
        flat_results = []
        for category, items in story_results.get("results", {}).items():
            for item in items:
                flat_results.append({
                    "title": item.get("name", item.get("title", "")),
                    "path": f"lore/{category}/{item.get('id', '')}",
                    "preview": f"[{category}] {item.get('archetype', '') or item.get('role', '') or item.get('core_lesson', '') or item.get('description', '')[:100]}",
                    "dimension": "lore",
                    "score": 0.9,
                    "source": "story_engine",
                    "category": category,
                })
        return {
            "dimension": dimension_id,
            "dimension_name": dim["name"],
            "query": query,
            "results": flat_results,
            "total": len(flat_results),
        }

    results = _chroma_search(dimension_id, query, limit) or _file_search(dimension_id, query, limit)
    return {
        "dimension": dimension_id,
        "dimension_name": dim["name"],
        "query": query,
        "results": results,
        "total": len(results),
    }


def cross_dimension_search(query: str, limit: int = 20):
    """Search across all 9 dimensions."""
    all_results = []
    for dim_id in DIMENSIONS:
        result = query_dimension(dim_id, query, limit // len(DIMENSIONS))
        all_results.extend(result.get("results", []))
    all_results.sort(key=lambda r: r.get("score", 0), reverse=True)
    return {"query": query, "results": all_results[:limit], "total": min(len(all_results), limit)}


# ── Internal Search Implementations ─────────────────────────────────────

def _file_search(dimension_id: str, query: str, limit: int) -> list:
    """Search files in the corresponding pillar directory for keyword matches."""
    pillar_map = {
        "vault": "01_CORE", "grove": "02_SYSTEMS", "forest": "03_NEURAL",
        "codex": "04_CODEX", "memory": "05_MEMORY", "agent": "06_AGENTS",
        "social": "07_SOCIAL", "market": "09_MARKET", "path": "08_LEARNING",
        "lore": "04_CODEX",
    }
    pillar = pillar_map.get(dimension_id)
    if not pillar:
        return []

    search_dir = SACRED_ROOT / pillar
    if not search_dir.exists():
        return []

    results = []
    query_lower = query.lower()
    text_exts = {".md", ".txt", ".py", ".js", ".ts", ".jsx", ".tsx", ".json", ".yaml", ".yml", ".html", ".css"}

    try:
        for file_path in search_dir.rglob("*"):
            if not file_path.is_file():
                continue
            if file_path.suffix.lower() not in text_exts:
                continue
            if file_path.stat().st_size > 50000:
                continue
            try:
                text = file_path.read_text(errors="ignore")
                if query_lower in text.lower():
                    idx = text.lower().find(query_lower)
                    start = max(0, idx - 60)
                    end = min(len(text), idx + len(query) + 60)
                    preview = text[start:end].replace("\n", " ")
                    rel_path = str(file_path.relative_to(SACRED_ROOT))
                    results.append({
                        "title": file_path.stem,
                        "path": rel_path,
                        "preview": preview.strip(),
                        "dimension": dimension_id,
                        "score": 0.5,
                        "source": "file_search",
                    })
            except (UnicodeDecodeError, PermissionError):
                continue
    except Exception:
        pass

    results.sort(key=lambda r: r.get("score", 0), reverse=True)
    return results[:limit]


def _chroma_search(dimension_id: str, query: str, limit: int) -> Optional[list]:
    """Attempt ChromaDB vector search. Returns None if unavailable."""
    try:
        import chromadb
        from chromadb.config import Settings

        chroma_path = SACRED_ROOT / "06_AGENTS" / "IRIS" / "chroma_db"
        if not chroma_path.exists():
            return None

        client = chromadb.PersistentClient(path=str(chroma_path), settings=Settings(anonymized_telemetry=False))
        collection_name = f"pillar_{dimension_id}"
        try:
            collection = client.get_collection(collection_name)
        except Exception:
            return None

        raw = collection.query(query_texts=[query], n_results=limit)
        results = []
        if raw.get("ids") and raw["ids"][0]:
            for i, doc_id in enumerate(raw["ids"][0]):
                metadata = (raw.get("metadatas") or [{}])[0][i] if raw.get("metadatas") else {}
                doc_text = (raw.get("documents") or [""])[0][i] if raw.get("documents") else ""
                results.append({
                    "title": metadata.get("title", doc_id),
                    "path": metadata.get("path", doc_id),
                    "preview": doc_text[:200],
                    "dimension": dimension_id,
                    "score": (raw.get("distances") or [[0]])[0][i] if raw.get("distances") else 0,
                    "source": "chromadb",
                })
        return results
    except ImportError:
        return None
    except Exception:
        return None


# ── Query History ──────────────────────────────────────────────────────────

def record_query(query: str, dimension: str = None, result_count: int = 0, source: str = "api"):
    """Record a sigil query in history."""
    try:
        conn = sqlite3.connect(SACRED_ROOT / "05_MEMORY" / "sacred_memory.db")
        conn.execute("""CREATE TABLE IF NOT EXISTS sigil_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            dimension TEXT,
            result_count INTEGER DEFAULT 0,
            source TEXT DEFAULT 'api',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        conn.execute(
            "INSERT INTO sigil_history (query, dimension, result_count, source) VALUES (?,?,?,?)",
            (query, dimension, result_count, source),
        )
        conn.commit()
        conn.close()
        return True
    except Exception:
        return False


def get_query_history(limit: int = 20):
    """Return recent sigil query history."""
    try:
        conn = sqlite3.connect(SACRED_ROOT / "05_MEMORY" / "sacred_memory.db")
        conn.row_factory = sqlite3.Row
        conn.execute("""CREATE TABLE IF NOT EXISTS sigil_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            dimension TEXT,
            result_count INTEGER DEFAULT 0,
            source TEXT DEFAULT 'api',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        rows = conn.execute(
            "SELECT * FROM sigil_history ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception:
        return []
