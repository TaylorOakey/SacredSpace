"""
sacredspace_mcp.py — SacredSpace MCP Tool Bridge
MCP-compatible tool server wrapping the FastAPI spine's 7 canonical routes.
Hermes calls these as smolagents @tool functions.

Pillar: 06_AGENT_LAYER
Status: Canon | v0.13.0
"""

import os
import json
import httpx
from pathlib import Path
from smolagents import tool

SPINE_URL = os.getenv("SACREDSPACE_API", "http://localhost:8888")

_client = httpx.Client(base_url=SPINE_URL, timeout=10.0)


def _get(path: str, params: dict = None) -> dict:
    try:
        r = _client.get(path, params=params)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e), "path": path}


def _post(path: str, payload: dict) -> dict:
    try:
        r = _client.post(path, json=payload)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"error": str(e), "path": path}


@tool
def query_memory(query: str, namespace: str = "", top_k: int = 5) -> str:
    """
    Query the SacredSpace Holographic Memory Engine (Neural Forest mote store).
    Returns the top-k most semantically relevant motes for the given query.

    Args:
        query: Natural language query to search the memory store.
        namespace: Optional namespace filter (core, lore, characters, agents, etc.).
        top_k: Number of results to return.

    Returns:
        Formatted string of matching motes with scores.
    """
    payload = {"text": query, "top_k": top_k}
    if namespace:
        payload["namespace"] = namespace
    result = _post("/query", payload)
    if "error" in result:
        return f"Memory query failed: {result['error']}"
    motes = result if isinstance(result, list) else result.get("motes", [])
    if not motes:
        return "No motes found for this query. The Neural Forest is silent."
    lines = []
    for m in motes:
        lines.append(
            f"[{m.get('namespace', '?')}] {m.get('text', '')[:300]}\n"
            f"  Score: {m.get('score', 0):.2f} | Kind: {m.get('kind', '?')}"
        )
    return "\n\n".join(lines)


@tool
def read_pillars() -> str:
    """
    Return the SacredSpace OS nine-pillar architecture manifest.
    Use this to understand the system's structure before routing a query.

    Returns:
        JSON string describing all nine pillars with status and agent ownership.
    """
    result = _get("/pillars")
    if "error" in result:
        return f"Pillar read failed: {result['error']}"
    return json.dumps(result, indent=2)


@tool
def invoke_icaris(agent: str, query: str) -> str:
    """
    Invoke a member of the ICARIS Quartet (ELIAS, AURORA, ASHER, or IRIS).

    Args:
        agent: One of ELIAS, AURORA, ASHER, IRIS (case-insensitive).
        query: The task or question to send to this agent.

    Returns:
        Agent response string.
    """
    result = _post("/icaris", {"agent": agent.upper(), "query": query})
    if "error" in result:
        return f"ICARIS invoke failed for {agent}: {result['error']}"
    return result.get("response", json.dumps(result))


@tool
def query_learning_gate(topic: str) -> str:
    """
    Query the Kethras Learning Gate for curriculum and learning path information.
    Use when questions are about study paths, lesson plans, or Maestro coursework.

    Args:
        topic: The learning topic or skill to query.

    Returns:
        Learning path suggestions and relevant resources.
    """
    result = _post("/kethras-learning-gate", {"topic": topic})
    if "error" in result:
        return f"Learning gate query failed: {result['error']}"
    return json.dumps(result, indent=2)


@tool
def list_sacred_artifacts(filter_tag: str = "") -> str:
    """
    Browse the Sacred Market artifact inventory.
    Use when asked about available artifacts, products, or Sacred Market items.

    Args:
        filter_tag: Optional tag to filter artifacts (e.g., 'tarot', 'sigil', 'print').

    Returns:
        List of available artifacts with descriptions.
    """
    params = {"tag": filter_tag} if filter_tag else {}
    result = _get("/merchant-sacred-artifacts", params=params)
    if "error" in result:
        return f"Artifact fetch failed: {result['error']}"
    return json.dumps(result, indent=2)


@tool
def check_vault_sync() -> str:
    """
    Check the current sync status of the Obsidian vault (read-only).
    Returns canon file count, staging status, and any pending inbox notes.

    Returns:
        Vault sync report as formatted string.
    """
    result = _get("/vault-watcher-obsidian-sync")
    if "error" in result:
        return f"Vault watcher failed: {result['error']}"
    return json.dumps(result, indent=2)


@tool
def lore_to_product(lore_concept: str, product_type: str = "print") -> str:
    """
    Run a lore concept through the Lore-to-Product Engine.
    Transforms SacredSpace lore into a product concept brief (print, digital, apparel).

    Args:
        lore_concept: The lore entity, spell, or archetype to productize.
        product_type: Target product type: print, digital, apparel, or card.

    Returns:
        Product concept brief as formatted string.
    """
    result = _post("/lore-to-product-engine", {
        "concept": lore_concept,
        "product_type": product_type,
    })
    if "error" in result:
        return f"Lore-to-product pipeline failed: {result['error']}"
    return json.dumps(result, indent=2)


ALL_TOOLS = [
    query_memory,
    read_pillars,
    invoke_icaris,
    query_learning_gate,
    list_sacred_artifacts,
    check_vault_sync,
    lore_to_product,
]
