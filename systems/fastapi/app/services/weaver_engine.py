"""Sacred Sigil Terminal — Weaver Engine (Spell Execution)
Executes sigil spells by coordinating across dimensions.
In lakesh alakin. ∆
"""
import json
import os
from typing import Optional
from pathlib import Path

SACRED_ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))

# ── Spell Catalog ────────────────────────────────────────────────────────

SPELLS = {
    "aurora_weave": {
        "name": "AURORA.WEAVE()",
        "description": "Weave insights across all 9 dimensions",
        "cost": {"resonance": 10},
        "reward": {"insight": 15, "xp": 25},
        "dimensions": ["vault", "forest", "codex", "memory"],
        "effect": "Cross-dimensional knowledge synthesis",
    },
    "elias_open_path": {
        "name": "ELIAS.OPEN_PATH()",
        "description": "Find the shortest path between two concepts",
        "cost": {"resonance": 5},
        "reward": {"insight": 8, "xp": 12},
        "dimensions": ["forest", "path"],
        "effect": "Graph traversal concept pathfinding",
    },
    "iris_thread": {
        "name": "IRIS.THREAD()",
        "description": "Connect disparate knowledge across dimensions",
        "cost": {"resonance": 12},
        "reward": {"insight": 25, "xp": 40},
        "dimensions": ["vault", "grove", "social", "market"],
        "effect": "Cross-dimensional connection threading",
    },
    "asher_shadow": {
        "name": "ASHER.SHADOW()",
        "description": "Reveal hidden patterns and edge cases",
        "cost": {"resonance": 8},
        "reward": {"insight": 20, "xp": 30},
        "dimensions": ["forest", "codex"],
        "effect": "Adversarial pattern detection",
    },
    "scribe_record": {
        "name": "SCRIBE.RECORD()",
        "description": "Record a memory mote across dimensions",
        "cost": {"resonance": 3},
        "reward": {"insight": 5, "xp": 8},
        "dimensions": ["memory", "codex"],
        "effect": "Persist knowledge to memory store",
    },
}


def get_spells():
    """Return the full spell catalog."""
    return SPELLS


def execute_spell(spell_id: str, params: Optional[dict] = None):
    """Execute a sigil spell.

    Returns spell result with effect description and any output data.
    """
    spell = SPELLS.get(spell_id)
    if not spell:
        return {"error": f"Unknown spell: {spell_id}", "success": False}

    params = params or {}
    result = {
        "spell": spell["name"],
        "success": True,
        "effect": spell["effect"],
        "dimensions_touched": spell["dimensions"],
        "cost": spell["cost"],
        "reward": spell["reward"],
        "output": {},
    }

    ins = 0
    xp = 0
    res = 0

    if spell_id == "aurora_weave":
        ins, xp, res = 15, 25, -10
        result["output"]["insight"] = _ollama_infer(
            f"Synthesize knowledge across: {', '.join(spell['dimensions'])}. "
            f"Query: {params.get('query', 'reveal patterns')}"
        )
    elif spell_id == "elias_open_path":
        ins, xp, res = 8, 12, -5
        from_ = params.get("from", "SacredSpace OS")
        to_ = params.get("to", "Nine Pillars")
        result["output"]["path"] = _graphify_path(from_, to_)
    elif spell_id == "iris_thread":
        ins, xp, res = 25, 40, -12
        result["output"]["connections"] = _ollama_infer(
            f"Connect knowledge between {params.get('source', 'unknown')} "
            f"and {params.get('target', 'unknown')}. "
            f"Context: {params.get('context', '')}"
        )
    elif spell_id == "asher_shadow":
        ins, xp, res = 20, 30, -8
        result["output"]["edge_cases"] = _ollama_infer(
            f"Analyze {params.get('target', 'the system')} for hidden "
            f"patterns, edge cases, and adversarial vectors."
        )
    elif spell_id == "scribe_record":
        ins, xp, res = 5, 8, -3
        mote_text = params.get("text", "")
        mote_ns = params.get("namespace", "sigil_terminal")
        result["output"]["stored"] = _store_mote(mote_text, mote_ns)

    # Track costs/rewards in profile
    update_profile("spells_cast", 1)
    if ins: update_profile("insight", ins)
    if xp: update_profile("xp", xp)
    if res: update_profile("resonance", res)
    level_up = update_profile("xp", 0)  # check level-up without adding xp
    if level_up.get("level_up"):
        result["level_up"] = f"∆ LEVEL UP! You are now level {level_up['new_level']}"

    result["profile"] = get_profile()
    return result


def _ollama_infer(prompt: str) -> dict:
    """Run inference via local Ollama."""
    import urllib.request

    ollama_url = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
    payload = json.dumps({
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 256},
    }).encode()

    try:
        req = urllib.request.Request(
            f"{ollama_url}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            return {"response": data.get("response", ""), "model": "llama3.2", "source": "ollama"}
    except Exception as e:
        return {"response": f"[Weaver offline: {e}]", "source": "fallback"}


def _graphify_path(from_node: str, to_node: str) -> dict:
    """Find shortest path between two nodes in the knowledge graph."""
    neural_graph = SACRED_ROOT / "03_NEURAL" / "graphify-out" / "graph.json"
    if not neural_graph.exists():
        # Try alternative locations
        for alt in ["04_CODEX/graphify-out/graph.json", "graphify-out/graph.json"]:
            p = SACRED_ROOT / alt
            if p.exists():
                neural_graph = p
                break
        else:
            return {"error": "No knowledge graph found", "path": []}

    try:
        data = json.loads(neural_graph.read_text())
        nodes = {n["id"]: n for n in data.get("nodes", [])}
        edges = data.get("edges", [])

        adjacency = {}
        for edge in edges:
            s, t = edge.get("source"), edge.get("target")
            adjacency.setdefault(s, []).append(t)
            adjacency.setdefault(t, []).append(s)

        from_id = _find_node_id(nodes, from_node)
        to_id = _find_node_id(nodes, to_node)
        if not from_id or not to_id:
            return {"error": f"Node not found: '{from_node}' or '{to_node}'", "path": []}

        queue = [(from_id, [from_id])]
        visited = {from_id}
        while queue:
            current, path = queue.pop(0)
            if current == to_id:
                return {
                    "path": [{"id": nid, "label": nodes[nid].get("label", nid)} for nid in path],
                    "hops": len(path) - 1,
                }
            for neighbor in adjacency.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return {"error": "No path found", "path": []}
    except Exception as e:
        return {"error": str(e), "path": []}


def _find_node_id(nodes: dict, label_or_id: str) -> Optional[str]:
    """Find node ID by label or ID."""
    label_lower = label_or_id.lower()
    for nid, node in nodes.items():
        if nid == label_or_id or node.get("label", "").lower() == label_lower:
            return nid
    for nid, node in nodes.items():
        if label_lower in nid or label_lower in node.get("label", "").lower():
            return nid
    return None


# ── Profile / Gamification ──────────────────────────────────────────────────

def get_profile():
    """Return the sigil caster's profile (resonance, xp, insight, level)."""
    try:
        conn = _profile_db()
        rows = conn.execute("SELECT key, value FROM sigil_profile").fetchall()
        conn.close()
        return {r["key"]: r["value"] for r in rows}
    except Exception:
        return {"resonance": 50, "xp": 0, "insight": 0, "level": 1, "queries_cast": 0, "spells_cast": 0}


def update_profile(key: str, delta: int = 1):
    """Update a profile stat by delta."""
    try:
        conn = _profile_db()
        conn.execute(
            "UPDATE sigil_profile SET value = value + ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?",
            (delta, key),
        )
        conn.commit()
        # Check level-up
        xp_row = conn.execute("SELECT value FROM sigil_profile WHERE key = 'xp'").fetchone()
        level_row = conn.execute("SELECT value FROM sigil_profile WHERE key = 'level'").fetchone()
        conn.close()
        if xp_row and level_row:
            xp = xp_row["value"]
            level = level_row["value"]
            next_level = level * 100
            if xp >= next_level:
                conn = _profile_db()
                conn.execute("UPDATE sigil_profile SET value = value + 1, updated_at = CURRENT_TIMESTAMP WHERE key = 'level'")
                conn.execute("UPDATE sigil_profile SET value = 0, updated_at = CURRENT_TIMESTAMP WHERE key = 'xp'")
                conn.commit()
                conn.close()
                return {"level_up": True, "new_level": level + 1}
        return {"level_up": False}
    except Exception:
        return {"level_up": False}


def _profile_db():
    """Get SQLite connection with sigil_profile table."""
    import sqlite3
    db_path = SACRED_ROOT / "05_MEMORY" / "sacred_memory.db"
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS sigil_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""INSERT OR IGNORE INTO sigil_profile (key, value) VALUES
        ('resonance', 50), ('xp', 0), ('insight', 0), ('level', 1),
        ('queries_cast', 0), ('spells_cast', 0)
    """)
    conn.commit()
    return conn


def _store_mote(text: str, namespace: str) -> dict:
    """Store a memory mote to the sacred memory database."""
    if not text:
        return {"error": "No text provided", "stored": False}
    try:
        motes_path = SACRED_ROOT / "05_MEMORY" / "motes"
        motes_path.mkdir(parents=True, exist_ok=True)
        from datetime import datetime
        mote_file = motes_path / f"sigil_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        mote_file.write_text(json.dumps({
            "text": text,
            "namespace": namespace,
            "timestamp": datetime.now().isoformat(),
            "source": "sigil_terminal",
        }, indent=2))
        return {"stored": True, "path": str(mote_file.relative_to(SACRED_ROOT))}
    except Exception as e:
        return {"error": str(e), "stored": False}
