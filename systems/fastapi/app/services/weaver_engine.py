"""Sacred Sigil Terminal — Weaver Engine (Spell Execution)
Executes sigil spells by coordinating across dimensions.
Uses the Sigil Grammar Engine for affinity-based cost calculation.
In lakesh alakin. ∆
"""
import json
import os
from typing import Optional
from pathlib import Path
from app.services import story_engine
from app.services.sigil_grammar import (
    get_affinity,
    calculate_cost,
    parse,
    get_all_macros,
    load_custom_macros,
)

SACRED_ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))

# Macros → spell mapping: macro IDs → spell IDs
_MACRO_SPELL_MAP: dict[str, str] = {
    "aurora_weave": "aurora_weave",
    "elias_open_path": "elias_open_path",
    "iris_thread": "iris_thread",
    "asher_shadow": "asher_shadow",
    "scribe_record": "scribe_record",
    "lore_unveil": "lore_unveil",
}

# Sigil compositions for each spell (from SACRED_SIGIL_STACK.md)
_SPELL_COMPOSITIONS: dict[str, str] = {
    "aurora_weave": "∆+⊙:✦+╻",       # Forest + Codex : Lantern + Gateway
    "elias_open_path": "✧+╻",         # Quest + Gateway
    "iris_thread": "⊗:⚒+╻",           # Social : Forge + Gateway
    "asher_shadow": "✦:⚒",            # Lantern : Forge
    "scribe_record": "○•:⚒",          # Mote : Forge
    "lore_unveil": "♰:✦",             # Lore : Lantern
}


def _get_affinity_discount(dimensions: list[str], operations: list[str]) -> float:
    """Calculate resonance discount multiplier based on affinities.
    
    full affinity → 25% discount (multiply cost by 0.75)
    resonant → 10% discount (multiply cost by 0.90)
    neutral → no discount (multiply cost by 1.0)
    
    Uses worst-case (highest cost) across all operation×dimension pairs.
    """
    if not dimensions or not operations:
        return 1.0
    
    # Best discount wins (lowest multiplier)
    best_multiplier = 1.0
    for op in operations:
        for dim in dimensions:
            level = get_affinity(op, dim)
            if level == "full":
                best_multiplier = min(best_multiplier, 0.75)
            elif level == "resonant":
                best_multiplier = min(best_multiplier, 0.90)
    
    return best_multiplier


def _get_reward_multiplier(dimensions: list[str], operations: list[str]) -> float:
    """Calculate reward multiplier based on affinities.
    
    full affinity → +25% reward
    resonant → +10% reward
    neutral → +0%
    
    Uses best-case across all operation×dimension pairs.
    """
    if not dimensions or not operations:
        return 1.0
    
    mult = 1.0
    for op in operations:
        for dim in dimensions:
            level = get_affinity(op, dim)
            if level == "full":
                mult = max(mult, 1.25)
            elif level == "resonant":
                mult = max(mult, 1.10)
    
    return mult


# ── Spell Catalog (with grammar-backed costs) ─────────────────────────────

def _build_spells() -> dict:
    """Build the spell catalog with grammar-calculated costs and affinities."""
    spells = {
        "aurora_weave": {
            "name": "AURORA.WEAVE()",
            "description": "Weave insights across all 9 dimensions",
            "cost": {"resonance": 10},
            "reward": {"insight": 15, "xp": 25},
            "dimensions": ["vault", "forest", "codex", "memory"],
            "operations": ["lantern", "gateway"],
            "effect": "Cross-dimensional knowledge synthesis",
        },
        "elias_open_path": {
            "name": "ELIAS.OPEN_PATH()",
            "description": "Find the shortest path between two concepts",
            "cost": {"resonance": 5},
            "reward": {"insight": 8, "xp": 12},
            "dimensions": ["forest", "path"],
            "operations": ["quest", "gateway"],
            "effect": "Graph traversal concept pathfinding",
        },
        "iris_thread": {
            "name": "IRIS.THREAD()",
            "description": "Connect disparate knowledge across dimensions",
            "cost": {"resonance": 12},
            "reward": {"insight": 25, "xp": 40},
            "dimensions": ["vault", "grove", "social", "market"],
            "operations": ["forge", "gateway"],
            "effect": "Cross-dimensional connection threading",
        },
        "asher_shadow": {
            "name": "ASHER.SHADOW()",
            "description": "Reveal hidden patterns and edge cases",
            "cost": {"resonance": 8},
            "reward": {"insight": 20, "xp": 30},
            "dimensions": ["forest", "codex"],
            "operations": ["lantern", "forge"],
            "effect": "Adversarial pattern detection",
        },
        "scribe_record": {
            "name": "SCRIBE.RECORD()",
            "description": "Record a memory mote across dimensions",
            "cost": {"resonance": 3},
            "reward": {"insight": 5, "xp": 8},
            "dimensions": ["memory", "codex"],
            "operations": ["mote", "forge"],
            "effect": "Persist knowledge to memory store",
        },
        "lore_unveil": {
            "name": "LORE.UNVEIL()",
            "description": "Reveal storyline connections between characters, nodes, and episodes",
            "cost": {"resonance": 6},
            "reward": {"insight": 18, "xp": 22},
            "dimensions": ["lore", "codex", "forest"],
            "operations": ["lantern"],
            "effect": "Storyline connection mapping",
        },
    }
    
    # Auto-calculate costs from grammar engine
    for spell_id, spell in spells.items():
        composition = _SPELL_COMPOSITIONS.get(spell_id)
        if composition:
            parsed = parse(composition)
            gram_cost = calculate_cost(parsed)
            dims = spell.get("dimensions", [])
            ops = spell.get("operations", [])
            discount = _get_affinity_discount(dims, ops)
            base_cost = gram_cost.get("total", spell["cost"]["resonance"])
            discounted = max(1, round(base_cost * discount))
            spell["cost"]["resonance"] = discounted
            spell["cost"]["base_grammar"] = base_cost
            spell["cost"]["affinity_discount"] = f"{int((1 - discount) * 100)}%"
            
            # Apply affinity multiplier to rewards
            reward_mult = _get_reward_multiplier(dims, ops)
            if reward_mult > 1.0:
                for rk in ("insight", "xp"):
                    if rk in spell["reward"]:
                        original = {
                            "aurora_weave": (15, 25),
                            "elias_open_path": (8, 12),
                            "iris_thread": (25, 40),
                            "asher_shadow": (20, 30),
                            "scribe_record": (5, 8),
                            "lore_unveil": (18, 22),
                        }[spell_id]
                        idx = 0 if rk == "insight" else 1
                        base_reward = original[idx]
                        boosted = round(base_reward * reward_mult)
                        spell["reward"][rk] = boosted
                        spell["reward"][f"{rk}_affinity_bonus"] = f"+{int((reward_mult - 1) * 100)}%"
    
    return spells


# Initialize catalog with grammar engine
SPELLS = _build_spells()


def get_spells():
    """Return the full spell catalog."""
    return SPELLS


def get_spell_composition(spell_id: str) -> Optional[str]:
    """Return the sigil composition string for a spell."""
    return _SPELL_COMPOSITIONS.get(spell_id)


def calculate_spell_resonance(spell_id: str) -> dict:
    """Calculate resonance cost using the grammar engine for a spell.
    
    Returns dict with base_cost, affinity_discount, effective_cost.
    """
    spell = SPELLS.get(spell_id)
    if not spell:
        return {"error": f"Unknown spell: {spell_id}"}
    return spell.get("cost", {})


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
        "composition": _SPELL_COMPOSITIONS.get(spell_id, ""),
        "output": {},
    }

    # Read costs/rewards from grammar-backed spell data
    cost = spell["cost"]
    reward = spell["reward"]
    ins = reward.get("insight", 0)
    xp = reward.get("xp", 0)
    res = -cost.get("resonance", 5)

    if spell_id == "aurora_weave":
        result["output"]["insight"] = _ollama_infer(
            f"Synthesize knowledge across: {', '.join(spell['dimensions'])}. "
            f"Query: {params.get('query', 'reveal patterns')}"
        )
    elif spell_id == "elias_open_path":
        from_ = params.get("from", "SacredSpace OS")
        to_ = params.get("to", "Nine Pillars")
        result["output"]["path"] = _graphify_path(from_, to_)
    elif spell_id == "iris_thread":
        result["output"]["connections"] = _ollama_infer(
            f"Connect knowledge between {params.get('source', 'unknown')} "
            f"and {params.get('target', 'unknown')}. "
            f"Context: {params.get('context', '')}"
        )
    elif spell_id == "asher_shadow":
        result["output"]["edge_cases"] = _ollama_infer(
            f"Analyze {params.get('target', 'the system')} for hidden "
            f"patterns, edge cases, and adversarial vectors."
        )
    elif spell_id == "scribe_record":
        mote_text = params.get("text", "")
        mote_ns = params.get("namespace", "sigil_terminal")
        result["output"]["stored"] = _store_mote(mote_text, mote_ns)
    elif spell_id == "lore_unveil":
        entity_a = params.get("entity", "")
        entity_b = params.get("related", None)
        if not entity_a:
            return {"error": "LORE.UNVEIL() requires at least one entity name", "success": False}
        result["output"]["unveiling"] = story_engine.lore_unveil(entity_a, entity_b)

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

        # NetworkX JSON export uses "links" for edges
        if not edges:
            edges = data.get("links", [])
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
