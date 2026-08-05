#!/usr/bin/env python3
"""Hermes — MCP Server. Exposes 3 tools: ask (local Ollama query), vault_search (grep-based, no catalog dependency), status.

Built 2026-07-27 to resolve a dead config reference: claude_desktop_config.json already pointed
at this exact path (/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/hermes/hermes_mcp.py) expecting
SACREDSPACE_ROOT, OBSIDIAN_VAULT, and OLLAMA_MODEL env vars — but no file existed here at all.
This is a real implementation of those three env vars' evident intent, not a bridge to the
separate "Hermes" CLI tool referenced in 02_COUNCIL_GROVE/docs/agent-setup.md (~/.hermes/skills/),
which is not installed on this machine (~/.hermes is a dangling symlink to a path that doesn't
exist). If that other tool is ever actually installed, this script should be reconsidered against
it rather than assumed to be the same thing.
"""
import json, os, sys, urllib.request, urllib.error, subprocess
from pathlib import Path

ASYNC_MODE = False
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
    ASYNC_MODE = True
except ImportError:
    ASYNC_MODE = False

SACREDSPACE_ROOT = os.environ.get("SACREDSPACE_ROOT", "/mnt/d/SacredSpace_OS")
OBSIDIAN_VAULT = os.environ.get("OBSIDIAN_VAULT", f"{SACREDSPACE_ROOT}/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

# ─── Tool Implementations ───

def do_ask(args: dict) -> dict:
    prompt = args.get("prompt", "")
    model = args.get("model", OLLAMA_MODEL)
    if not prompt:
        return {"error": "prompt required"}
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    try:
        req = urllib.request.Request(f"{OLLAMA_URL}/api/generate", data=payload,
                                      headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
        return {"model": model, "response": result.get("response", ""), "done": result.get("done", False)}
    except urllib.error.URLError as e:
        return {"error": f"Ollama unreachable at {OLLAMA_URL}: {e}", "hint": "Is `ollama serve` running?"}
    except Exception as e:
        return {"error": str(e)}

def do_vault_search(args: dict) -> list:
    query = args.get("query", "")
    limit = min(args.get("limit", 15), 50)
    if not query:
        return [{"error": "query required"}]
    if not Path(OBSIDIAN_VAULT).exists():
        return [{"error": f"Vault path not found: {OBSIDIAN_VAULT}"}]
    try:
        # Deliberately independent of the Akashic catalog (SQLite index can go stale) —
        # this is a live grep over the actual files, always current, no build step.
        proc = subprocess.run(
            ["grep", "-rli", "--include=*.md", query, OBSIDIAN_VAULT],
            capture_output=True, text=True, timeout=20,
        )
        paths = [p for p in proc.stdout.splitlines() if p][:limit]
        results = []
        for p in paths:
            try:
                text = Path(p).read_text(encoding="utf-8", errors="ignore")
                idx = text.lower().find(query.lower())
                snippet = text[max(0, idx - 80):idx + 160].replace("\n", " ") if idx >= 0 else text[:160]
            except Exception:
                snippet = ""
            results.append({"path": p, "snippet": snippet.strip()})
        return results
    except subprocess.TimeoutExpired:
        return [{"error": "grep timed out after 20s — query may be too broad"}]
    except Exception as e:
        return [{"error": str(e)}]

def do_status(args: dict = None) -> dict:
    vault_exists = Path(OBSIDIAN_VAULT).exists()
    vault_file_count = None
    if vault_exists:
        try:
            vault_file_count = sum(1 for _ in Path(OBSIDIAN_VAULT).rglob("*.md"))
        except Exception:
            vault_file_count = None
    ollama_reachable = False
    ollama_models = []
    try:
        with urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=5) as resp:
            data = json.loads(resp.read())
        ollama_reachable = True
        ollama_models = [m["name"] for m in data.get("models", [])]
    except Exception:
        pass
    return {
        "sacredspace_root": SACREDSPACE_ROOT,
        "sacredspace_root_exists": Path(SACREDSPACE_ROOT).exists(),
        "obsidian_vault": OBSIDIAN_VAULT,
        "obsidian_vault_exists": vault_exists,
        "obsidian_vault_md_files": vault_file_count,
        "ollama_url": OLLAMA_URL,
        "ollama_reachable": ollama_reachable,
        "configured_model": OLLAMA_MODEL,
        "configured_model_available": OLLAMA_MODEL in ollama_models,
        "ollama_models_available": ollama_models,
    }

HANDLERS = {"ask": do_ask, "vault_search": do_vault_search, "status": do_status}

# ─── Async MCP Mode ───
if ASYNC_MODE:
    server = Server("hermes")

    @server.list_tools()
    async def handle_list_tools():
        return [
            types.Tool(name="hermes_ask", description="Query the local Ollama model configured for this SacredSpace install",
                       inputSchema={"type": "object", "properties": {"prompt": {"type": "string"}, "model": {"type": "string"}}, "required": ["prompt"]}),
            types.Tool(name="hermes_vault_search", description="Live grep search across the Obsidian vault (no catalog build step, always current)",
                       inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 15}}, "required": ["query"]}),
            types.Tool(name="hermes_status", description="Health check: vault path, Ollama reachability, configured model availability",
                       inputSchema={"type": "object", "properties": {}}),
        ]

    @server.call_tool()
    async def handle_call_tool(name: str, arguments: dict):
        tool_name = name.replace("hermes_", "")
        if tool_name in HANDLERS:
            result = HANDLERS[tool_name](arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
        return [types.TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    async def main():
        async with mcp.server.stdio.stdio_server() as (rs, ws):
            await server.run(rs, ws, InitializationOptions(
                server_name="hermes", server_version="0.1.0",
                capabilities=server.get_capabilities(notification_options=NotificationOptions(), experimental_capabilities={}),
            ))

    if __name__ == "__main__":
        import asyncio; asyncio.run(main())

else:
    print("⚠ MCP SDK not installed. Run: pip install mcp", file=sys.stderr)
    sys.exit(1)
