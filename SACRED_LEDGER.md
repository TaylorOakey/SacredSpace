# S∆CR3DSP∆CE OS — SACRED LEDGER

**Last updated:** 2026-06-10 (session 9b)
**Seat:** AURORA (Claude Code)
**Canon:** In lakesh alakin. ∆

---

## System Status — Phase 3 + Council Infrastructure

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| FastAPI Spine | :8888 | ✅ LIVE | v2.0.0 — 14 routes incl. /mcp |
| MCP Server (Hermes) | :8888/mcp | ✅ LIVE | 8 tools active — direct calls, no HTTP self-loop; initialize + tools/list + tools/call verified |
| Mission Control | :3001 | ✅ LIVE | v2.0.1 — Node v24.16.0 + pnpm 11.5.3 in WSL2 |
| OmniParse | :8001 | ⚠️ DOWN (dormant) | Not started this session; parse endpoints dormant — `--web` blocked (no Chrome), `--documents` deferred (Florence-2 ~1GB not cached) |
| ChromaDB (embedded) | — | ✅ 169 docs | `sacredspace_canon` collection |
| SQLite Memory | — | ✅ 12KB | `05_MEMORY_ENGINE/sacred_memory.db` |
| Ollama | :11434 | ✅ 3 models | sacred-coder, qwen2.5-coder, moondream — Windows host via auto-detected gateway |
| FastAPI→Ollama bridge | — | ✅ ONLINE | Fixed s6 — was broken (localhost fallback); now reads gateway from /etc/resolv.conf |
| free-claude-code proxy | :8082 | ✅ Running | Routes Claude Code → local NIM |
| Obsidian REST | :27123 | ✅ RESPONDING | Detected live s6 — Obsidian may be running |
| Redis | :6379 | ⚠️ OFFLINE | Optional, not yet configured |
| CopyQ | — | ⚠️ INSTALLED | v16.0.0 binary at 02_COUNCIL_GROVE/tools/copyq/, bridge+routes built, server not running |
| Intelligent Terminal | — | ❌ BLOCKED | Win10 Build 19045 — requires Windows 11 |
| OpenCode Plugins | — | ✅ 10 active | 11 packages in npm registry (see OpenCode Plugin Inventory) |

## Pillar Inventory

| Pillar | Files | Notes |
|--------|-------|-------|
| 01_OBSIDIAN_VAULTS | 105 | SacredSpace_Vault with 00_CANON, 00_INBOX, ARCHIVE/CODEXIUM_ERA (46 files recovered) |
| 02_COUNCIL_GROVE | 3+ | mission-control/ (MC v2.0.1), handoff_ritual.py, logs/ |
| 03_NEURAL_FOREST | 1+ | omniparse/ (venv at ~/.venvs/omniparse, torch 2.11+CUDA) |
| 04_SACRED_CODEX | 12 | Scripts, ingest tools, prep_notebooklm.py, briefing doc, sigil terminal docs |
| 05_MEMORY_ENGINE | 1 | sacred_memory.db (SQLite) |
| 06_AGENT_LAYER | 19992 | Hermes agent + IRIS + chroma_db (1.7MB) |
| 07_SOCIAL_MOTHERSHIP | 6362+ | Discord/Telegram bridge code (vendored); CREATION_LAB/IMAGE_ARCHIVE/GEMINI/ (68 Gemini PNGs) |
| 08_LEARNING_PATH | 0 | Empty — NotebookLM handles curricula |
| 09_SACRED_MARKET | 0 | Empty — design phase |

## FastAPI Spine Routes

```
GET /                → System root + docs link
GET /health/         → Service health + 9-pillar disk check
GET /health/ollama   → Ollama bridge status + model list
GET /pillars/status  → Per-pillar file counts
GET /memory/status   → SQLite + ChromaDB health
POST /memory/mote    → Store memory mote
GET /memory/motes    → List stored motes
GET /vault/status    → Obsidian REST proxy status
GET /vault/search    → Search vault via Obsidian REST
GET /hermes/status   → Hermes agent path check
GET /inference/status → Ollama inference health
POST /inference/complete → Run inference via Ollama
POST /mcp            → MCP JSON-RPC endpoint (8 tools)
GET /mcp             → MCP server info / tool manifest
```

## Startup Commands

```bash
# ★ FULL SESSION IGNITION (all 5 services)
bash /mnt/d/SacredSpace_OS/boot_sacred.sh

# Individual services:

# FastAPI spine (background) — reliable single-command form
SACRED_ROOT=/mnt/d/SacredSpace_OS OLLAMA_BASE=http://$(grep nameserver /etc/resolv.conf | awk '{print $2}' | head -1):11434 PYTHONPATH=/mnt/d/SacredSpace_OS/systems/fastapi nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8888 > /tmp/sacredspace_api.log 2>&1 &

# Mission Control (Council Grove dashboard — :3001)
cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/mission-control && PORT=3001 pnpm dev

# OmniParse (document/image/media/web parser — :8001)
cd /mnt/d/SacredSpace_OS/03_NEURAL_FOREST/omniparse
~/.venvs/omniparse/bin/python server.py --port 8001 --documents --media --web

# free-claude-code proxy
sacredproxy                                       # alias

# IRIS vault agent
iris                                              # alias

# OpenCode with ICARIS agents
opencode-sacred                                   # alias
opencode --agent aurora
opencode --agent elias
```

## OmniParse — Model Loading Checklist

To activate parse endpoints, restart with flags:

```bash
# Documents + images only (needs ~1GB Florence-2 download first run):
~/.venvs/omniparse/bin/python server.py --port 8001 --documents

# + media (Whisper small ~150MB):
~/.venvs/omniparse/bin/python server.py --port 8001 --documents --media

# + web crawler (BLOCKED — requires Chrome/Chromium):
sudo apt-get install chromium-browser chromium-driver
~/.venvs/omniparse/bin/python server.py --port 8001 --documents --media --web
```

## Known Issues

- **WSL2 9p cache** — Heavy filesystem ops on `/mnt/d` can cause the 9p connection to drop (Invalid argument). Writes since last flush are lost on `wsl --shutdown`. Mitigation: keep Python venvs on ext4 (`~/.venvs/`), not on D:.
- **Mission Control gateway status** — `sacred-spine` shows `unknown` (expected); MC health-checks use OpenClaw WebSocket protocol, FastAPI spine is HTTP/REST.
- **OmniParse gradio** — System gradio 6.15 is incompatible with OmniParse (needs 4.x); server.py patched to run REST-API-only without demo UI.
- **Intelligent Terminal v0.1** — Windows 11 only; machine is Win10 Build 19045.
- **Obsidian REST :27123** — Run Obsidian desktop, enable Obsidian REST API plugin
- **Ollama on WSL2** — Gateway IP auto-detected from `/etc/resolv.conf` at runtime (config.py + start.sh both read it); current session gateway: 172.17.0.1
- **Memory motes table** — Empty (0 rows); populated via POST /memory/mote or IRIS agent
- **08_LEARNING_PATH** — Curricula managed in NotebookLM (Google), not local files
- **09_SACRED_MARKET** — Design phase; 8-source kit being built in NotebookLM

## OpenCode Plugin Inventory

| Plugin | Version | Status | Function |
|--------|---------|--------|----------|
| opencode-mem | 2.17.0 | ✅ ACTIVE | Session memory, cross-restart persistence |
| envsitter-guard | 0.0.4 | ✅ ACTIVE | .env secret guard |
| @tarquinen/opencode-dcp | 3.1.12 | ✅ ACTIVE | Context pruning, token limit management |
| opencode-notify | 0.3.1 | ✅ ACTIVE | OS notifications for background tasks |
| oh-my-opencode-slim | 1.1.1 | ✅ ACTIVE | Automation bundle (LSP/AST, MCP orchestration) |
| opencode-worktree | 0.4.1 | ✅ ACTIVE | Isolated git worktree branches |
| opencode-fff-search | 0.7.0 | ✅ ACTIVE | Ultra-fast fuzzy file search |
| opencode-obsidian | 1.0.7 | ✅ ACTIVE | Obsidian vault R/W from agent runtime |
| opencode-browser | 1.2.3 | 🔲 CONFIGURED | Browser MCP — awaits Chrome extension (Phase 2) |
| opencode-supermemory | 2.0.6 | 🔲 INSTALLED | Cloud memory — requires SUPERMEMORY_API_KEY |
| ~~opencode-antigravity-auth~~ | — | ❌ REMOVED | ToS risk, uninstalled per user direction |

## Priority Items — 2026-06-10

| Priority | Item | Blocker |
|----------|------|---------|
| 🔴 HIGH | Run parsers against real exports (Claude, ChatGPT, Takeout) | Takeout ZIPs downloading from Google Drive — drop in `_RAW/` when ready |
| 🟡 MED | CopyQ Windows server launch | Manual step — launch CopyQ.exe on Windows side |
| 🟡 MED | `api-start` alias broken (exit 144 on compound shell) | Use boot_sacred.sh or single nohup command directly |
| 🟡 MED | ChatGPT export ZIP at `_RAW/chatgpt_export.zip` is actually HTML | Rename to .html and run through chatgpt parser HTML path |
| 🟡 MED | Sigil Terminal not yet built | Docs in 04_SACRED_CODEX/SACRED_SIGIL_TERMINAL_QUICK_START.md; boot_sacred.sh will auto-launch once built at 06_AGENT_LAYER/sacred-sigil-terminal/ |
| 🟢 LOW | Obsidian REST — registered at :27124 (not :27123) | obsidian MCP plugin registered but failing to connect — Obsidian + REST plugin must be running |
| 🟢 LOW | ChromaDB — 169 docs but 0 motes in SQLite | Pipeline motes via POST /memory/mote or IRIS agent |

## Recent Wins

- 2026-06-10 (s8b): **68 Gemini images migrated** — moved from `E:/06_BACKUPS/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/CREATION_LAB/IMAGE_ARCHIVE/GEMINI/` → `D:/SacredSpace_OS/07_SOCIAL_MOTHERSHIP/CREATION_LAB/IMAGE_ARCHIVE/GEMINI/`; E: IMAGE_ARCHIVE cleared; CREATION_LAB folder structure created on D:
- 2026-06-10 (s8b): **E: drive audit** — E: mounted (`sudo mount -t drvfs E: /mnt/e`); 497 sacred art images confirmed NOT on E: or D: — still in Google Photos cloud, will arrive via Takeout ZIP; 68 Gemini PNGs were only image asset found; FileHistory and 06_BACKUPS are all that remain on E:
- 2026-06-10 (s8): **boot_sacred.sh rewritten** — 5-service ignition script: Ollama check → FastAPI spine + MCP → Mission Control → Sigil Terminal → free-claude-code proxy; auto-detects Ollama gateway via resolv.conf; graceful "already live" detection on re-run; Sigil Terminal section stubs safely if app not yet built; all logs → 02_COUNCIL_GROVE/logs/; status board printed at end
- 2026-06-09 (s4): Codexium vault recovery — 46 files copied from C:\Users\USER\Documents\SacredSpace_Vault\ to D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault\ARCHIVE\CODEXIUM_ERA\ (0_CORE through 8_ARCHIVE, _CODEXIUM, _INDEX preserved)
- 2026-06-09 (s4): SACREDSPACE_OS_BRIEFING.md built for Jeanie — 130-line onboarding doc covering nine pillars, Council seats, active systems, game layer, startup commands. Placed in 04_SACRED_CODEX/ and SACREDSPACE_FORGE_OUTPUT/
- 2026-06-09 (s4): CopyQ v16.0.0 binary confirmed working from WSL2; copyq_bridge.py and copyq_routes.py verified — BLOCKED on Windows server launch
- 2026-06-09 (s4): Session 4 audit — 32 open items tracked, 2 completed, 3 blocked (Google Drive folder, Day 1 post content, CopyQ Windows server)
- 2026-06-09 (s5): **OpenCode equip mission** — ICARIS Quartet agents deployed (ELIAS Pathfinder, AURORA Illuminator, ASHER Shadow, IRIS Messenger) with full agent configs at ~/.config/opencode/agents/
- 2026-06-09 (s5): Plugins installed — opencode-fff-search (fast file search via fff.nvim) and opencode-obsidian (vault integration)
- 2026-06-09 (s5): opencode.jsonc updated — plugin array expanded, summon + council commands added, MCP documented
- 2026-06-09 (s5): Shell ward deployed — sacred_status dashboard, exorcise_port utility, p1-p9 pillar navigation, sacredtag stamp function, chroma_query, spine_check. All appended to ~/.bashrc
- 2026-06-10 (s7): **google_takeout_parser.py created** — 5-platform Takeout parser (Drive, Gmail, YouTube, Keep, Photos); Drive-folder name override routing; Photos metadata-only (no image copy, triage gate enforced); canonical run order Drive→Gmail→YouTube→Keep→Photos; vault keyword fix consistent with other parsers
- 2026-06-10 (s7): **sacredspace MCP plugin registered** — `claude mcp add sacredspace http://localhost:8888/mcp`; confirmed ✔ Connected via `claude mcp list`; stored in ~/.claude.json (project: systems/fastapi); also discovered obsidian MCP registered at :27124
- 2026-06-10 (s7): **MCP server LIVE at :8888/mcp** — direct JSON-RPC FastAPI router (replaced FastMCP ASGI which had task group lifecycle issues); 8 tools verified: system_health, query_memory, store_mote, read_ledger, pillar_status, run_inference, vault_search, list_anvil_missions; tools use direct function calls, no HTTP self-loop
- 2026-06-10 (s7): **Node.js + pnpm in WSL2** — Node v24.16.0 activated via fnm (was installed, not in PATH); pnpm v11.5.3 installed globally; fnm duplicate bashrc block removed; /run/user/1000/fnm_multishells mkdir fix applied
- 2026-06-09 (s6): **claude_export_parser.py created** — parses Claude.ai ZIP/JSON/HTML exports → Obsidian-ready .md; routes to real nine pillars; ISO 8601 timestamp handling; three-tier HTML fallback (embedded JSON → BeautifulSoup → regex)
- 2026-06-09 (s6): **chatgpt_export_parser.py patched** — old pillar map (01_CORE_NEXUS, 04_ECONOMY_VAULT, etc.) replaced with real nine pillars; UNROUTED bucket removed; default unmatched → 04_SACRED_CODEX
- 2026-06-09 (s6): **Vault keyword fix (both parsers)** — bare "vault" removed from 01_OBSIDIAN_VAULTS keywords; only compound phrases now route there: "obsidian vault", "vault note", "vault file", "vault folder", "vault search"
- 2026-06-09 (s6): Ollama gateway IP fix — config.py `_detect_ollama()` and start.sh updated to auto-detect WSL2 gateway from /etc/resolv.conf; FastAPI→Ollama bridge now ONLINE (was broken on localhost fallback)
- 2026-06-09 (s6): Full health check — FastAPI, Mission Control, free-claude-code proxy, Ollama, ChromaDB, SQLite all confirmed live; Obsidian REST :27123 detected responding
- 2026-06-09 (s5): Note: npm install on WSL2 has UNC path issues with the Windows Node.js interop — skipped postinstall scripts, packages verified working
- 2026-06-10 (s9): **VALEN self-equip mission** — Agent config enhanced with Vision Cultivation Protocol (graphify query, obsidian-cli workflow, cross-session continuity, backlog triad); graphify plugin installed as OpenCode tool.execute.before hook
- 2026-06-10 (s9): **Knowledge graph built on SACRED_CODEX** — 104 nodes, 123 edges, 16 communities; god nodes: Nine Pillars (12 edges, betweenness 0.410), SacredSpace OS (12), Nine Dimensions (11), Game Layer (10), Sacred Sigil Terminal (9), CopyQ (9), Supabase Schema (8); surprising findings: flash drive scaffold mirrors nine pillars, ChromaDB ingestion pipeline reads from OBSIDIAN_VAULTS, NotebookLM migration cross-reads both VAULT and CODEX; outputs at `04_SACRED_CODEX/graphify-out/`
- 2026-06-10 (s9): **/cultivate custom command added** to opencode.jsonc — queries the knowledge graph, traces concept relationships, maps to pillars
- 2026-06-10 (s9): **50 isolated/weakly-connected nodes found** in SACRED_CODEX graph — documentation gaps in WSL2, Mission Control, OmniParse, The Forge, Canon Close; potential targets for enrichment
- 2026-06-10 (s9): **Phase 1 — opencode-browser v1.2.3 deployed** — Browser MCP plugin for Chrome/Chromium control via native messaging. Configured in opencode.jsonc as plugin + browsermcp MCP server. Awaits Browser MCP extension install in Chrome on Windows host (Phase 2).
- 2026-06-10 (s9): **Phase 3 — opencode-supermemory v2.0.6 installed** — Supermemory-powered persistent memory. Requires SUPERMEMORY_API_KEY for activation (cloud dependency — flagged against zero-paid-APIs constraint).
- 2026-06-10 (s9b): **Phase 5 — opencode-antigravity-auth v1.6.0 installed** — ❌ **REMOVED** per user direction. ToS risk flagged, plugin uninstalled.
- 2026-06-10 (s9): **Plugin array expanded** — 10 plugins now registered (opencode-mem, envsitter-guard, dcp, notify, oh-my-opencode-slim, worktree, fff-search, obsidian, browser, supermemory, antigravity-auth). SacredSpace ecosystem at 11 total npm packages.
- 2026-06-08 (s3): Complete cross-drive SacredSpace content audit — C: + D: drives inventoried for all storyline/Arcana material
- 2026-06-08 (s3): Discovered C: drive Codexium-era vault (Mar 2024) — 21 files with Hyperglyph System, ICARIS Quartet, Canon Gate Protocol, Mythic Timeline, Bodhilyra, SPI, 144 Principle — NOT mirrored on D:
- 2026-06-08 (s3): Found SACREDARCANA_VISUAL_STYLE_CODEX_v01_DISTILLED.md (7.9 KB) — 4 Realms (Zii, Mylo, Auralon, Koru), 8 Visual Laws — awaiting Canon Gate on D:
- 2026-06-08 (s3): Located full Sacred Chrome extension at C: ~/Downloads/sacred-chrome/ (8 files) — newtab with animated Metatron's Cube, side panel, terminal, portal, beam capture
- 2026-06-08 (s3): Recovered legacy WSL dev code — sacredspace_memory_engine_v1.py (Full Memory Engine with Ebbinghaus decay), obsidian_bridge.py, librarian.py
- 2026-06-08 (s3): Key finding — Gemini-era concepts (Serpent, Silent Echo, Alignment Tracker, Blessing Cards, Nine Gates, Victory Paths) exist ONLY in open-design repo; no analogues in existing SacredSpace_OS material
- 2026-06-08 (s3): Identified 12 episode files as stubs needing expansion, 6 canon subdirectories as stubs, 2 empty pillars (08, 09)
- 2026-06-08 (s2): OmniParse server live :8001 (no-model mode) — Fix B pattern resolved all segfaults; `--web` blocked (no Chrome/Selenium); `--documents` deferred (Florence-2 ~1GB download needed)
- 2026-06-08: Mission Control v2.0.1 deployed → 02_COUNCIL_GROVE/mission-control/ (:3001)
- 2026-06-08: OmniParse venv + patch deployed → 03_NEURAL_FOREST/omniparse/ — Fix B (deferred ML imports), gradio removed, marker-pdf 0.3, surya-ocr 0.4, moviepy<2, numba, tabled
- 2026-06-08: sacred-spine gateway registered in Mission Control → FastAPI :8888
- 2026-06-08: OmniParse ext4 venv built (~/.venvs/omniparse) — torch 2.11+CUDA
- 2026-06-08: FastAPI spine restructured to app/main.py (v2.0.0, 12 routes)
- 2026-06-05: FastAPI spine built from scratch (was documented but never existed)
- 2026-06-05: CLAUDE.md cleaned — stale home-dir refs removed
- 2026-06-05: Ollama bridge auto-detection fixed (config.py + start.sh + bashrc)
- 2026-06-05: Bashrc deduplicated — 8 duplicate aliases removed, sigil ghosts cleared
- 2026-06-05: Claude Code profiles created (sacredsmith, aurora, elias + 3 legacy)
- 2026-06-05: free-claude-code proxy auto-start added to bashrc

---

_In lakesh alakin._
