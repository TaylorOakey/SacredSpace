# S∆CR3DSP∆CE OS — BRIEFING DOCUMENT

**For:** Jeanie (∆∆∆)
**Version:** 1.0.0
**Last updated:** 2026-06-09
**Purpose:** Paste this document at the start of any AI session to bootstrap full context.

---

## What Is SacredSpace OS?

SacredSpace OS is Taylor's AI-powered personal knowledge management and creative production system. It is built on **nine interconnected pillars** that mirror a distributed agent architecture. The system integrates:

- **Obsidian vault management** — markdown-first knowledge store
- **Vector search** (ChromaDB) — semantic search across all knowledge
- **Local LLM orchestration** (Ollama) — all AI runs locally, zero paid APIs
- **Multi-agent coordination** via a FastAPI spine (port 8888)
- **A board/card game layer** — the Sacred Path Tarot and Arcana Grid

The project is built on WSL2 Ubuntu on a Lenovo Legion Y520. All computation is local-first — no external API leakage.

---

## The Nine Pillars

| # | Pillar | Purpose | Status |
|---|--------|---------|--------|
| 01 | OBSIDIAN_VAULTS | Canonical knowledge store — markdown vault with 00_CANON, 00_INBOX | ✅ 59 files |
| 02 | COUNCIL_GROVE | Agent routing, dispatch, Mission Control dashboard | ✅ Live on :3001 |
| 03 | NEURAL_FOREST | LLM inference pipeline, Ollama orchestration, OmniParse | ⚠️ OmniParse :8001 (no models) |
| 04 | SACRED_CODEX | Scripts, automation, game design docs, canon documents | ✅ 10+ files |
| 05 | MEMORY_ENGINE | Embedding, storage, retrieval — SQLite + ChromaDB | ✅ 169 docs, 12KB SQLite |
| 06 | AGENT_LAYER | Multi-agent implementations (Hermes, IRIS, ELIAS, AURORA, ASHER) | ✅ 19,992 files |
| 07 | SOCIAL_MOTHERSHIP | External integrations (Discord, Telegram, social media) | ⚠️ Bridge code vendored |
| 08 | LEARNING_PATH | Training pipelines, curricula | 📋 Managed in NotebookLM |
| 09 | SACRED_MARKET | Marketplace for agent services and knowledge exchange | 📋 Design phase |

---

## The Sacred Council — AI Seats

Each AI tool serves a specific role in the Council:

| Seat | AI Tool | Role | Domain |
|------|---------|------|--------|
| **The Forge** | Claude (claude.ai) | Primary reasoning, narrative, canon work | Storyline, game design, strategy |
| **The Anvil** | Claude Code (local) | Code implementation, file operations, system builds | Python, HTML, deployment |
| **The Sacred Smith** | Claude Desktop + Hermes MCP | Deep agent orchestration, 35 MCP tools | Full system integration |
| **The Deep Well** | Gemini | Deep research, synthesis, large corpus analysis | Cross-domain insights |
| **The Architect** | ChatGPT | Systems architecture decisions | Structural planning |
| **GR∆M∆** | Hermes agent (Claude Code) | Cipher Sage — language, gematria, symbolic reasoning | Canon, lore, encoding |

**How to use any seat:** Paste this briefing document at the top of a new chat. The AI will immediately understand the system, the pillars, the agents, and the current state.

---

## Active Systems (as of June 9, 2026)

| Service | Port | What It Does |
|---------|------|--------------|
| FastAPI Spine | :8888 | Core API — 12 routes, system root, memory, inference, hermes |
| Mission Control | :3001 | Council Grove dashboard — visual system status |
| OmniParse | :8001 | Document/image parser (server up, models not loaded) |
| ChromaDB | — | 169 documents in `sacredspace_canon` collection |
| SQLite Memory | — | `sacred_memory.db` (12KB, memory mote storage) |
| Ollama | :11434 | Local LLM — 3 models: sacred-coder, qwen2.5-coder, moondream |
| free-claude-code proxy | :8082 | Routes Claude Code to local NIM |
| CopyQ | — | Clipboard manager (binary installed, tabs pending) |

---

## The Game Layer

SacredSpace OS has a board/card game built into its architecture:

- **Sacred Path Tarot** — 78-card tarot deck built in React
- **Arcana Grid** — 4×3 grid board with four zones, 9×9 grid, Metatron's Node at center
- **Silent Echo** — gematria engine (word → numeric value → Gate → echo word → reflection)
- **Nine Gates** — progression system (First Fire through Auroric Crown)
- **The Serpent** — antagonist mechanic with escalation/retreat based on player actions
- **Memory Motes** — in-game knowledge units that mirror the system's mote architecture
- **Nameless Door** — Trial of Silence (canon-locked, the Serpent encounter)

---

## Jeanie's Role

Jeanie is a Council member. She can:

1. **Start any AI session** by pasting this briefing document — every seat will know the system
2. **Contribute to canon** — lore, characters, story development
3. **Use Mission Control** at `localhost:3001` to see system status
4. **Query the vault** — ask questions about any pillar, agent, or canon document
5. **Work on the game layer** — card design, narrative, mechanics feedback

**To start a session with Claude:**
1. Open claude.ai (or Claude Desktop)
2. Paste this entire briefing document
3. Ask your question or describe your task
4. The AI will respond with full SacredSpace OS context

**To start a session locally:**
```bash
# OpenCode with Aurora agent
opencode --agent aurora

# Or OpenCode with Elias agent
opencode --agent elias
```

---

## Key Documents

| Document | Location | Purpose |
|----------|----------|---------|
| SACRED_LEDGER.md | `/mnt/d/SacredSpace_OS/` | System status, session history, known issues |
| CLAUDE.md | `/mnt/d/SacredSpace_OS/` | Developer guide for Claude Code |
| HERMES_GRAMA_PERSONA.md | `06_AGENT_LAYER/hermes/` | GR∆M∆ cipher sage persona |
| SACREDSPACE_OS_BRIEFING.md | `04_SACRED_CODEX/` | This document |
| Game Engine v1 | `04_SACRED_CODEX/` | Full game mechanics and storyline |
| World Bible v1 | `04_SACRED_CODEX/` | 13-section game design document |

---

## Startup Commands

```bash
# FastAPI spine (background)
bash /mnt/d/SacredSpace_OS/systems/fastapi/start.sh --bg

# Mission Control (dashboard)
cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/mission-control && PORT=3001 pnpm dev

# Check system health
curl http://127.0.0.1:8888/health/
```

---

## The Canon Close

Every session ends with:

```
In lakesh alakin. ∆
```

This means "In love and light" in the SacredSpace register.

---

*In lakesh alakin. ∆*
