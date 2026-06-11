"""SacredSpace OS — MCP Server (Hermes bridge)
Implements MCP Streamable HTTP transport directly as FastAPI routes.
Avoids FastMCP ASGI lifecycle issues when embedded in an existing app.
Tools: system_health, query_memory, store_mote, read_ledger,
       pillar_status, run_inference, vault_search, list_anvil_missions
"""

import json
import glob
import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.config import SACRED_ROOT, OLLAMA_BASE, NINE_PILLARS
from app.db import get_sqlite, get_chroma_client

router = APIRouter(tags=["mcp"])

MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "sacredspace"
SERVER_VERSION = "1.0.0"


# ── Ollama helper (only external call needed) ─────────────────────────────────

def _ollama_complete(prompt: str, model: str) -> str:
    try:
        with httpx.Client(base_url=OLLAMA_BASE, timeout=30.0) as c:
            r = c.post("/api/generate", json={"model": model, "prompt": prompt, "stream": False})
            r.raise_for_status()
            return r.json().get("response", "")
    except Exception as e:
        return f"Inference failed: {e}"


def _obsidian_search(query: str) -> dict:
    try:
        with httpx.Client(base_url="http://localhost:27123", timeout=5.0) as c:
            r = c.get("/search/simple/", params={"query": query})
            r.raise_for_status()
            return r.json()
    except Exception as e:
        return {"error": str(e)}


# ── Tool implementations — direct calls, no HTTP self-loop ────────────────────

def tool_system_health(_args: dict) -> str:
    # Pillar disk check
    pillar_status = {}
    for p in NINE_PILLARS:
        path = f"{SACRED_ROOT}/{p}"
        if os.path.isdir(path):
            files = sum(len(f) for _, _, f in os.walk(path))
            pillar_status[p] = {"exists": True, "files": files}
        else:
            pillar_status[p] = {"exists": False, "files": 0}

    # Memory check
    try:
        conn = get_sqlite()
        mote_count = conn.execute("SELECT COUNT(*) FROM memory_motes").fetchone()[0]
        conn.close()
        chroma = get_chroma_client()
        memory = {"sqlite": "online", "motes": mote_count,
                  "chromadb": "online" if chroma else "offline"}
    except Exception as e:
        memory = {"error": str(e)}

    # Ollama check
    try:
        with httpx.Client(base_url=OLLAMA_BASE, timeout=5.0) as c:
            r = c.get("/api/tags")
            models = [m["name"] for m in r.json().get("models", [])]
        ollama = {"status": "online", "models": models}
    except Exception as e:
        ollama = {"status": "offline", "error": str(e)}

    return json.dumps({
        "spine": "live",
        "ollama": ollama,
        "memory": memory,
        "pillars": pillar_status,
    }, indent=2)


def tool_query_memory(args: dict) -> str:
    try:
        conn = get_sqlite()
        limit = int(args.get("top_k", 5))
        query = args.get("query", "").lower()
        rows = conn.execute(
            "SELECT * FROM memory_motes WHERE LOWER(content) LIKE ? ORDER BY created_at DESC LIMIT ?",
            (f"%{query}%", limit)
        ).fetchall()
        conn.close()
        if not rows:
            return "No motes found. The Neural Forest is silent."
        return "\n\n".join(f"[{r['pillar'] or '?'}] {r['content'][:300]}" for r in rows)
    except Exception as e:
        return f"Memory query failed: {e}"


def tool_store_mote(args: dict) -> str:
    try:
        conn = get_sqlite()
        conn.execute(
            "INSERT INTO memory_motes (entity, pillar, content, tags, status) VALUES (?,?,?,?,?)",
            (args.get("namespace", "general"), args.get("namespace", "general"),
             args.get("text", ""), None, args.get("kind", "note"))
        )
        conn.commit()
        conn.close()
        return json.dumps({"status": "stored", "namespace": args.get("namespace", "general")})
    except Exception as e:
        return f"Store failed: {e}"


def tool_read_ledger(_args: dict) -> str:
    ledger = os.path.join(SACRED_ROOT, "SACRED_LEDGER.md")
    try:
        with open(ledger, "r") as f:
            return f.read()
    except Exception as e:
        return f"Ledger read failed: {e}"


def tool_pillar_status(_args: dict) -> str:
    lines = []
    for p in NINE_PILLARS:
        path = f"{SACRED_ROOT}/{p}"
        if os.path.isdir(path):
            files = sum(len(f) for _, _, f in os.walk(path))
            lines.append(f"✅ {p}: {files} files")
        else:
            lines.append(f"❌ {p}: missing")
    return "\n".join(lines)


def tool_run_inference(args: dict) -> str:
    return _ollama_complete(args.get("prompt", ""), args.get("model", "sacred-coder"))


def tool_vault_search(args: dict) -> str:
    result = _obsidian_search(args.get("query", ""))
    if "error" in result:
        return f"Vault search failed: {result['error']}"
    return json.dumps(result, indent=2)


def tool_list_anvil_missions(_args: dict) -> str:
    anvil = "/mnt/d/CLAUDECODE.ANVIL"
    try:
        files = glob.glob(os.path.join(anvil, "*.md"))
        files += glob.glob(os.path.join(anvil, "ACTIVE", "*.md"))
        return "\n".join(os.path.basename(f) for f in files) if files else "ANVIL is clear."
    except Exception as e:
        return f"ANVIL read failed: {e}"


# ── Tool registry ─────────────────────────────────────────────────────────────

TOOLS = {
    "system_health": {
        "fn": tool_system_health,
        "description": "Return live status of all SacredSpace OS services and nine pillars.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "query_memory": {
        "fn": tool_query_memory,
        "description": "Search the SacredSpace ChromaDB memory store for relevant motes.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language query"},
                "top_k": {"type": "integer", "description": "Number of results (default 5)"},
            },
            "required": ["query"],
        },
    },
    "store_mote": {
        "fn": tool_store_mote,
        "description": "Store a memory mote in the SacredSpace memory engine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "text":      {"type": "string"},
                "namespace": {"type": "string", "description": "Pillar namespace"},
                "kind":      {"type": "string", "description": "note|canon|raw|decision"},
            },
            "required": ["text"],
        },
    },
    "read_ledger": {
        "fn": tool_read_ledger,
        "description": "Read SACRED_LEDGER.md — the canonical system state document.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "pillar_status": {
        "fn": tool_pillar_status,
        "description": "Return file counts for all nine SacredSpace OS pillars.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "run_inference": {
        "fn": tool_run_inference,
        "description": "Run a prompt through the local Ollama inference engine.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "model":  {"type": "string", "description": "Ollama model (default: sacred-coder)"},
            },
            "required": ["prompt"],
        },
    },
    "vault_search": {
        "fn": tool_vault_search,
        "description": "Search the Obsidian vault via the REST plugin.",
        "inputSchema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    "list_anvil_missions": {
        "fn": tool_list_anvil_missions,
        "description": "List all open ANVIL mission files in D:/CLAUDECODE.ANVIL/.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
}


# ── JSON-RPC helpers ──────────────────────────────────────────────────────────

def ok(id_, result):
    return {"jsonrpc": "2.0", "id": id_, "result": result}


def err(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


# ── MCP method handlers ───────────────────────────────────────────────────────

def handle_initialize(params, id_):
    return ok(id_, {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
    })


def handle_tools_list(params, id_):
    tools = [
        {
            "name": name,
            "description": info["description"],
            "inputSchema": info["inputSchema"],
        }
        for name, info in TOOLS.items()
    ]
    return ok(id_, {"tools": tools})


def handle_tools_call(params, id_):
    name = params.get("name", "")
    args = params.get("arguments", {})
    if name not in TOOLS:
        return err(id_, -32601, f"Unknown tool: {name}")
    try:
        result = TOOLS[name]["fn"](args)
        return ok(id_, {"content": [{"type": "text", "text": str(result)}]})
    except Exception as e:
        return err(id_, -32603, f"Tool error: {e}")


DISPATCH = {
    "initialize":             handle_initialize,
    "notifications/initialized": lambda p, id_: None,  # no response needed
    "tools/list":             handle_tools_list,
    "tools/call":             handle_tools_call,
}


# ── FastAPI route ─────────────────────────────────────────────────────────────

@router.post("/mcp")
async def mcp_endpoint(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(err(None, -32700, "Parse error"), status_code=400)

    # Support both single request and batch array
    batch = isinstance(body, list)
    requests_ = body if batch else [body]
    responses = []

    for req in requests_:
        id_ = req.get("id")
        method = req.get("method", "")
        params = req.get("params", {})

        handler = DISPATCH.get(method)
        if handler is None:
            if id_ is not None:  # notifications have no id, skip response
                responses.append(err(id_, -32601, f"Method not found: {method}"))
            continue

        response = handler(params, id_)
        if response is not None:
            responses.append(response)

    if not responses:
        return JSONResponse(None, status_code=204)
    return JSONResponse(responses if batch else responses[0])


@router.get("/mcp")
async def mcp_sse_info():
    """Basic info endpoint — SSE streaming not implemented (Claude Code uses POST)."""
    return {
        "server": SERVER_NAME,
        "version": SERVER_VERSION,
        "protocol": MCP_PROTOCOL_VERSION,
        "transport": "streamable-http",
        "tools": list(TOOLS.keys()),
    }
