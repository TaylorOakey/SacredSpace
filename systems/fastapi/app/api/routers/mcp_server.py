"""SacredSpace OS — MCP Server (Hermes bridge)
Implements MCP Streamable HTTP transport directly as FastAPI routes.
Avoids FastMCP ASGI lifecycle issues when embedded in an existing app.
Tools: system_health, query_memory, store_mote, read_ledger,
       pillar_status, run_inference, vault_search, list_anvil_missions,
       sigil_query, sigil_execute_spell
"""

import json
import glob
import os
import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from app.config import SACRED_ROOT, OLLAMA_BASE, NINE_PILLARS
from app.db import get_sqlite, get_chroma_client
from app.services import sigil_terminal_backend, weaver_engine, sigil_grammar

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


# ── Sigil Terminal MCP tools ──────────────────────────────────────────────────

def tool_sigil_query(args: dict) -> str:
    """Query the Sacred Sigil Terminal across one or all dimensions."""
    try:
        query = args.get("query", "")
        dimension = args.get("dimension", None)
        limit = int(args.get("limit", 10))
        if not query:
            return "Error: query is required"
        if dimension and dimension != "all":
            result = sigil_terminal_backend.query_dimension(dimension, query, limit)
        else:
            result = sigil_terminal_backend.cross_dimension_search(query, limit)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Sigil query failed: {e}"


def tool_sigil_execute_spell(args: dict) -> str:
    """Execute a Sigil Terminal spell (weaver engine)."""
    try:
        spell_id = args.get("spell_id", "")
        params = args.get("params", {})
        if not spell_id:
            spells = weaver_engine.get_spells()
            names = ", ".join(f"{k}: {v['name']}" for k, v in spells.items())
            return f"Available spells: {names}"
        result = weaver_engine.execute_spell(spell_id, params)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Spell execution failed: {e}"


def tool_sigil_parse(args: dict) -> str:
    """Parse a sigil string using the Sacred Sigil Grammar Engine."""
    try:
        sigil = args.get("sigil", "")
        if not sigil:
            return "Error: sigil string is required"
        parsed = sigil_grammar.parse(sigil)
        cost = sigil_grammar.calculate_cost(parsed)
        description = sigil_grammar.describe_sigil(parsed)
        return json.dumps({
            "parsed": parsed.to_dict(),
            "cost": cost,
            "description": description,
        }, indent=2, default=str)
    except Exception as e:
        return f"Sigil parse failed: {e}"


def tool_sigil_lint(args: dict) -> str:
    """Lint a sigil string for validity and affinity warnings."""
    try:
        sigil = args.get("sigil", "")
        if not sigil:
            return "Error: sigil string is required"
        result = sigil_grammar.lint(sigil)
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Sigil lint failed: {e}"


def tool_sigil_library(_args: dict) -> str:
    """Return the full sigil grammar reference library."""
    try:
        lib = sigil_grammar.get_library()
        lib["all_macros"] = sigil_grammar.get_all_macros()
        return json.dumps(lib, indent=2, default=str)
    except Exception as e:
        return f"Sigil library failed: {e}"


def tool_sigil_create_macro(args: dict) -> str:
    """Create a custom sigil macro."""
    try:
        from app.db import get_sqlite
        name = args.get("name", "")
        composition = args.get("composition", "")
        if not name or not composition:
            return "Error: both 'name' and 'composition' are required"
        parsed = sigil_grammar.parse(composition)
        if parsed.errors:
            return f"Invalid composition: {'; '.join(parsed.errors)}"
        conn = get_sqlite()
        sigil_grammar.load_custom_macros(conn)
        macro = sigil_grammar.add_custom_macro(
            conn, name, composition,
            args.get("description", ""),
            args.get("agent", "CUSTOM"),
        )
        conn.close()
        return json.dumps(macro, indent=2, default=str)
    except Exception as e:
        return f"Create macro failed: {e}"


def tool_sigil_list_macros(_args: dict) -> str:
    """List all macros (built-in + custom)."""
    try:
        from app.db import get_sqlite
        conn = get_sqlite()
        sigil_grammar.load_custom_macros(conn)
        conn.close()
        all_macros = sigil_grammar.get_all_macros()
        return json.dumps({
            "macros": [{"id": k, **v} for k, v in all_macros.items()],
            "total": len(all_macros),
        }, indent=2, default=str)
    except Exception as e:
        return f"List macros failed: {e}"


def tool_sigil_delete_macro(args: dict) -> str:
    """Delete a custom sigil macro by ID."""
    try:
        from app.db import get_sqlite
        macro_id = int(args.get("macro_id", 0))
        if not macro_id:
            return "Error: 'macro_id' (int) is required"
        conn = get_sqlite()
        sigil_grammar.load_custom_macros(conn)
        deleted = sigil_grammar.delete_custom_macro(conn, macro_id)
        conn.close()
        return json.dumps({"deleted": deleted, "macro_id": macro_id}, indent=2)
    except Exception as e:
        return f"Delete macro failed: {e}"


def tool_sigil_spell_cost(args: dict) -> str:
    """Get grammar-backed spell cost breakdown for a spell."""
    try:
        spell_id = args.get("spell_id", "")
        if not spell_id:
            spells = weaver_engine.get_spells()
            names = ", ".join(spells.keys())
            return f"Available spells: {names}"
        cost = weaver_engine.calculate_spell_resonance(spell_id)
        composition = weaver_engine.get_spell_composition(spell_id)
        result = {"spell_id": spell_id, "cost": cost}
        if composition:
            parsed = sigil_grammar.parse(composition)
            result["composition"] = composition
            result["parsed"] = parsed.to_dict()
        return json.dumps(result, indent=2, default=str)
    except Exception as e:
        return f"Spell cost failed: {e}"


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
    "sigil_query": {
        "fn": tool_sigil_query,
        "description": "Query the Sacred Sigil Terminal across any of the 9 dimensions (vault, grove, forest, codex, memory, agent, social, market, path) or all.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language search query"},
                "dimension": {"type": "string", "description": "Dimension filter: vault|grove|forest|codex|memory|agent|social|market|path|all (default: all)"},
                "limit": {"type": "integer", "description": "Max results per dimension (default: 10)"},
            },
            "required": ["query"],
        },
    },
    "sigil_execute_spell": {
        "fn": tool_sigil_execute_spell,
        "description": "Execute a Sigil Terminal spell. Spells: aurora_weave (cross-dimensional synthesis), elias_open_path (graph pathfinding), iris_thread (knowledge connection), asher_shadow (adversarial analysis), scribe_record (memory storage).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "spell_id": {"type": "string", "description": "Spell name: aurora_weave|elias_open_path|iris_thread|asher_shadow|scribe_record"},
                "params": {"type": "object", "description": "Spell-specific parameters (query, from, to, target, text, etc.)"},
            },
            "required": ["spell_id"],
        },
    },
    "sigil_parse": {
        "fn": tool_sigil_parse,
        "description": "Parse a sigil string into its structured components using the Sacred Sigil Grammar Engine. Supports dimension glyphs (∞◊∆⊙≈♦⊗⊜Λ♰), root sigils (╻○•✧⚒Ϟ✦), affixes (!+~>*), macros (AURORA.WEAVE, etc.), and #N limits.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sigil": {"type": "string", "description": "Sigil string to parse, e.g. '∆:⚒' or 'AURORA.WEAVE' or '∞+⊙:✦+╻*#10'"},
            },
            "required": ["sigil"],
        },
    },
    "sigil_lint": {
        "fn": tool_sigil_lint,
        "description": "Lint a sigil string for grammar validity, affinity warnings, and composition rules.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sigil": {"type": "string", "description": "Sigil string to lint, e.g. '≈:✦#5' or '∆:⚒'"},
            },
            "required": ["sigil"],
        },
    },
    "sigil_library": {
        "fn": tool_sigil_library,
        "description": "Return the full Sacred Sigil Grammar reference including all dimensions, root sigils, macros, and affixes.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "sigil_create_macro": {
        "fn": tool_sigil_create_macro,
        "description": "Create a custom sigil macro with a name, composition string, and optional description.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Macro name, e.g. 'MY_CUSTOM.WEAVE'"},
                "composition": {"type": "string", "description": "Sigil composition string, e.g. '∆:✦+╻'"},
                "description": {"type": "string", "description": "Optional description of what the macro does"},
                "agent": {"type": "string", "description": "Optional agent name (default: CUSTOM)"},
            },
            "required": ["name", "composition"],
        },
    },
    "sigil_list_macros": {
        "fn": tool_sigil_list_macros,
        "description": "List all macros including built-in and custom user-created macros.",
        "inputSchema": {"type": "object", "properties": {}, "required": []},
    },
    "sigil_delete_macro": {
        "fn": tool_sigil_delete_macro,
        "description": "Delete a custom sigil macro by its numeric ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "macro_id": {"type": "integer", "description": "Numeric ID of the custom macro to delete"},
            },
            "required": ["macro_id"],
        },
    },
    "sigil_spell_cost": {
        "fn": tool_sigil_spell_cost,
        "description": "Get the grammar-backed cost breakdown for any spell, including composition parse, affinity discount, and effective resonance cost.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "spell_id": {"type": "string", "description": "Spell ID: aurora_weave|elias_open_path|iris_thread|asher_shadow|scribe_record|lore_unveil"},
            },
            "required": [],
        },
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
