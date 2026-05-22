# OPENHUMAN — MANUAL INSTALL GUIDE
**SacredSpace OS · Pillar 06 · Agent Layer**
*Last updated: 2026-05-21*

---

## What Is OpenHuman

OpenHuman is an open-source desktop AI assistant (by tinyhumansai) that integrates local and cloud LLMs with MCP server tooling. It connects to your local FastAPI spine and Hermes MCP endpoint, enabling persistent memory, vault awareness, and agent orchestration from a native desktop app.

**Repo:** https://github.com/tinyhumansai/openhuman  
**Releases:** https://github.com/tinyhumansai/openhuman/releases

---

## Prerequisites

| Requirement | Status | Notes |
|---|---|---|
| Windows 11 | ✓ Required | Native install (not WSL2) |
| WSL2 Ubuntu 24.04 | ✓ Present | Legion host |
| FastAPI spine :8888 | ✓ Live | `systems/fastapi/main.py` |
| Hermes MCP :8888/mcp | ✓ Live | v0.13.0 operational |
| Ollama :11434 | Check | Windows bridge host |

---

## Step 1 — Download

Go to: **https://github.com/tinyhumansai/openhuman/releases**

Download the Windows installer: `OpenHuman-Setup-x.x.x.exe`

---

## Step 2 — Install

1. Run `OpenHuman-Setup-x.x.x.exe` as Administrator
2. Default install path: `%LOCALAPPDATA%\OpenHuman\`
3. Accept defaults — no additional components required

---

## Step 3 — Configure MCP Connection

OpenHuman reads its config from `%APPDATA%\OpenHuman\config.json`.

Copy the contents of `02_COUNCIL_GROVE/openhuman_config.json` to that path, **or** launch OpenHuman and paste the settings below in Settings → MCP Servers.

**MCP endpoint:** `http://localhost:8888/mcp`  
**Agent memory endpoint:** `http://localhost:8888/mcp`  
**Vault path:** `D:\01_VAULT\SacredSpace_Vault`

---

## Step 4 — Verify Connection

Once OpenHuman is running, check the MCP status indicator in the bottom bar. It should show **Connected** with green indicator.

Test from WSL2:
```bash
curl -s http://localhost:8888/hermes/health
# Expected: {"hermes":"0.13.0","status":"operational","mcp":"/mcp",...}
```

---

## Step 5 — Wire to ICARIS Agents

In OpenHuman Settings → System Prompt, paste:

```
You are connected to SacredSpace OS via Hermes MCP.
Vault: D:\01_VAULT\SacredSpace_Vault
Spine: http://localhost:8888
Agents: ASHER (audit), ELIAS (analyze), AURORA (deploy), IRIS (record)
Memory endpoint: http://localhost:8888/mcp
Run ASHER before any write. Run IRIS after every deployment.
```

---

## Fallback — If Installer Unavailable

Check if Claude Desktop is a viable alternative:
```
%LOCALAPPDATA%\AnthropicClaude\Claude.exe
```
Claude Desktop also supports MCP servers via `claude_desktop_config.json`.

**Claude Desktop MCP config path:**
`%APPDATA%\Claude\claude_desktop_config.json`

Add to `mcpServers`:
```json
{
  "mcpServers": {
    "sacredspace-hermes": {
      "command": "curl",
      "args": ["-s", "http://localhost:8888/mcp"]
    }
  }
}
```

---

## Troubleshooting

| Issue | Fix |
|---|---|
| MCP shows Disconnected | Verify FastAPI spine: `curl http://localhost:8888/hermes/health` |
| Vault not found | Check D: mounted: `ls /mnt/d/01_VAULT/` |
| Ollama timeout | `export OLLAMA_HOST="$(grep nameserver /etc/resolv.conf \| awk '{print $2}'):11434"` |
| OpenHuman won't launch | Run as Administrator, check `%LOCALAPPDATA%\OpenHuman\` exists |

---

*SacredSpace OS · ∆∆∆O∆K3YTREE∆∆∆ · In lakesh alakin.*
