---
title: "APP_STATUS"
source: "/mnt/d/SacredSpace_OS/00_SACRED_SPINE/APP_STATUS.md"
keyword_count: 3
keywords_found: [merchant]
pillar: "00_SACRED_SPINE"
date_indexed: "2026-05-21"
cashflow_rank: 77
---

# APP STATUS — SacredSpace OS
**Generated:** 2026-05-21  
**Host:** Lenovo Legion Y520 · WSL2 Ubuntu 24.04 · Windows 11

---

## Core Services

| Service | Port | Status | Notes |
|---|---|---|---|
| FastAPI Spine | :8888 | ✓ LIVE | v2.0.0 — `systems/fastapi/main.py` |
| Hermes MCP | :8888/mcp | ✓ OPERATIONAL | v0.13.0 |
| Hermes Health | :8888/hermes/health | ✓ OK | Returns `{"status":"operational"}` |
| Ollama | :11434 | CHECK | Set `OLLAMA_HOST` to Windows bridge if Tailscale conflict |
| ChromaDB | :8001 | NOT CHECKED | `05_MEMORY_ENGINE/chroma_data/` |
| Redis | :6379 | NOT CHECKED | Required for memory caching |

## FastAPI Routes

```
GET  /                          Spine root + agent manifest
GET  /health                    Health check (v2.0.0)
POST /harvest                   Content harvest
POST /hermes                    Hermes agent relay
POST /thricegreat               Thricegreat invocation
GET  /memory                    Memory retrieval
GET  /pillars                   Nine-pillar status
GET  /icaris                    ICARIS DAG status
GET  /kethras-learning-gate     Pillar 08 — Learning
GET  /merchant-sacred-artifacts Pillar 09 — Market
GET  /vault-watcher-obsidian-sync Pillar 01 — Vault sync
GET  /lore-to-product-engine    Pillar 04 — Lore/product
```

## Desktop Apps

| App | Path | Status |
|---|---|---|
| Claude Desktop | `%LOCALAPPDATA%\AnthropicClaude\Claude.exe` | ✗ NOT INSTALLED |
| OpenHuman | `%LOCALAPPDATA%\OpenHuman\` | NOT CHECKED — see OPENHUMAN_MANUAL_INSTALL.md |
| Obsidian | `%LOCALAPPDATA%\Obsidian\` | ASSUMED LIVE (vault active) |
| Chrome | System | LIVE — Sacred Chrome extension deployed |

## ICARIS Agents

| Agent | Role | Status |
|---|---|---|
| ASHER | Audit | Active (ICARIS DAG law) |
| ELIAS | Analyze | Active |
| AURORA | Deploy | Active |
| IRIS | Record | Active |

Cascade: `ollama → gemini → mock`

## Nine Pillars

| Pillar | Path | Status |
|---|---|---|
| 01 OBSIDIAN_VAULTS | `/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/` | ✓ |
| 02 COUNCIL_GROVE | `/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/` | ✓ |
| 03 NEURAL_FOREST | `/mnt/d/SacredSpace_OS/03_NEURAL_FOREST/` | ✓ |
| 04 SACRED_CODEX | `/mnt/d/SacredSpace_OS/04_SACRED_CODEX/` | ✓ |
| 05 MEMORY_ENGINE | `/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/` | ✓ |
| 06 AGENT_LAYER | `/mnt/d/SacredSpace_OS/06_AGENT_LAYER/` | ✓ |
| 07 SOCIAL_MOTHERSHIP | `/mnt/d/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/` | ✓ |
| 08 LEARNING_PATH | `/mnt/d/SacredSpace_OS/08_LEARNING_PATH/` | ✓ |
| 09 SACRED_MARKET | `/mnt/d/SacredSpace_OS/09_SACRED_MARKET/` | ✓ |

## Open Queue

- P0: FastAPI :8888 — LIVE as of this report
- P1: NotebookLM — 5 notebooks unpopulated (NOTEBOOKLM_UPLOAD package building in T5)
- P2: Image asset inventory — `09_SACRED_MARKET/asset_inventory.md` pending

---

*SacredSpace OS · APP_STATUS · Auto-generated · In lakesh alakin.*
