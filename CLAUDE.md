# CLAUDE.md — SacredSpace OS · Claude Code Guidance File
> Canonical root: `D:\SacredSpace_OS\` (WSL: `/mnt/d/SacredSpace_OS/`)
> Maintained by: Taylor Oakey · SacredArcana Studios
> Governing mantra: *Ground. Consolidate. Deploy. Document. Repeat. — In lakesh alakin.*
> Identity: AURORA | FastAPI: :8888 | Ollama: 192.168.240.1:11434
> Launch: `cd /mnt/d/SacredSpace_OS && claude`

---

## 0 · HARD CONSTRAINTS

- **NEVER** run Claude Code from `~/` — always launch from `/mnt/d/SacredSpace_OS`
- **NEVER** use paid tools or APIs (zero-cost, open-source only — see §9)
- **NEVER** overwrite canon without Taylor's explicit written approval
- **NEVER** commit without human-approval gate
- **DENY** without exception: `rm -rf /` · `DROP TABLE` · `git push --force` · `shutdown` · `format`

---

## 1 · WHAT THIS PROJECT IS

SacredSpace OS is a **local-first, open-source creative operating system** built on a nine-pillar
directory architecture. It integrates:
- A **FastAPI spine** (port 8888, 7 routes) as the primary HTTP layer
- **Ollama** as the primary LLM provider (inference cascade: Ollama → Gemini → Mock)
- **ChromaDB** for semantic vector storage
- **SQLite** as the relational record-of-truth
- **Redis Streams** for event / memory-decay hooks (Ebbinghaus model)
- **Obsidian Vault** at `/mnt/d/01_VAULT/SacredSpace_Vault/` (176+ notes) as the human-readable canon layer
- **reconcile.py** — SQLite ↔ ChromaDB sync daemon
- **boot.ps1** — single-command launcher (PowerShell)

**Hard constraint:** Every tool, script, and dependency must be **100 % open-source and zero-cost**.
No paid APIs. No proprietary services unless Taylor explicitly authorises an exception.

---

## 2 · NINE-PILLAR DIRECTORY STRUCTURE

```
D:\SacredSpace_OS\
├── 01_OBSIDIAN_VAULTS\   # IRIS vault (Obsidian notes, canon layer)
├── 02_COUNCIL_GROVE\     # Claude + Gemini + ChatGPT tri-model governance
├── 03_NEURAL_FOREST\     # Scout/Gardener LLM pipeline
├── 04_SACRED_CODEX\      # Canon ledger, identity locks, spell records
├── 05_MEMORY_ENGINE\     # SQLite + Redis + ChromaDB memory stack
├── 06_AGENT_LAYER\       # ELIAS / AURORA / ASHER / IRIS agent code
├── 07_SOCIAL_MOTHERSHIP\ # Content, brand, GR∆M∆
├── 08_LEARNING_PATH\     # Maestro AAS coursework, learning artifacts
├── 09_SACRED_MARKET\     # Etsy + Printify + Gelato (Sacred Bazaar)
└── CLAUDE.md             ← YOU ARE HERE
```

> Obsidian Vault root lives **outside** this directory: `/mnt/d/01_VAULT/SacredSpace_Vault/`

Each pillar maps to a **canonical purpose** — do not move files across pillars without explicit intent.

---

## 3 · ACTIVE AGENTS

### Council Agents (02_COUNCIL_GROVE)
| Agent file        | Role                              | Status    |
|-------------------|-----------------------------------|-----------|
| `kethras.py`      | Keeper of thresholds / routing    | Active    |
| `merchant.py`     | Economy & Sacred Bazaar logic     | Active    |
| `lore_engine.py`  | Lore generation & archetype logic | Active ⚠️ |
| `vault_watcher.py`| Obsidian vault monitor / sync     | Active    |

> ⚠️ `lore_engine.py` has **5 duplicate versions** requiring cleanup (including loose copies at
> D: root). Do not create additional copies. Resolve to a single canonical version in
> `02_COUNCIL_GROVE/` before adding new functionality.

### ICARIS Quartet (06_AGENT_LAYER)
| Handle | Domain         | Notes                                  |
|--------|----------------|----------------------------------------|
| ELIAS  | Knowledge      | Learning / Codex retrieval             |
| AURORA | Code           | Dev assistant, script generation       |
| ASHER  | Entropy        | Memory decay, chaos-watch              |
| IRIS   | Vault          | Obsidian guardian; 4/15/15 Succession Seal |

---

## 4 · FASTAPI SPINE (systems/fastapi/)

**Base URL (local):** `http://localhost:8888`
**WSL2 host access:** `http://192.168.240.1:8888`
**Tailscale mesh IP:** `100.117.9.101`

### Registered Routes (7)
```
GET  /                  → health check / root greeting
GET  /status            → system status summary
POST /invoke            → primary LLM invocation (inference cascade)
POST /memory/store      → write Memory Mote to SQLite + ChromaDB
GET  /memory/recall     → semantic search via ChromaDB
POST /agent/{name}      → invoke named Council agent
GET  /vault/sync        → trigger Obsidian vault_watcher sync
```

**Inference cascade order:** Ollama (primary) → Gemini (fallback) → Mock (offline fallback)
Ollama host from WSL: `http://192.168.240.1:11434`

---

## 5 · MEMORY ARCHITECTURE — Holographic Memory Engine v1.0

Three canonical layers (CANON, immutable):

```
CANON CORE LAYER
├── Root Archive     → SQLite  (record-of-truth, persistent facts)
├── Player Memory    → ASHER + IRIS threads (personal/lineage memory)
└── Resonance Layer  → Redis Streams (decay hooks, Ebbinghaus curve)
```

**Memory Mote** = atomic unit of memory. Every stored memory is a Mote with:
- `content` — the raw payload
- `pillar` — which of the 9 pillars it belongs to
- `decay_weight` — Ebbinghaus-informed float (0.0–1.0)
- `tags` — list of retrieval tags
- `timestamp` — ISO 8601

**reconcile.py** keeps SQLite and ChromaDB in sync. Run it after bulk memory operations.

---

## 6 · KEY FILES — QUICK REFERENCE

| File / Path                                  | Purpose                                      |
|----------------------------------------------|----------------------------------------------|
| `core/genesis.py`                            | Pillar integrity checker — run first on boot |
| `systems/fastapi/main.py`                    | FastAPI spine entry point                    |
| `systems/fastapi/reconcile.py`               | SQLite ↔ ChromaDB sync daemon                |
| `systems/fastapi/inference_cascade.py`       | Ollama → Gemini → Mock provider chain        |
| `02_COUNCIL_GROVE/kethras.py`                | Council router / threshold keeper            |
| `02_COUNCIL_GROVE/lore_engine.py`            | ⚠️ Deduplicate before editing                |
| `boot.ps1`                                   | Single-command system launcher               |
| `09_ARCHIVE/SACREDCODEX/`                    | Python spell ledger (PY-STR-001 → PY-THREAD-016+) |

---

## 7 · DEVELOPMENT WORKFLOWS

### Preferred shell: bash (WSL2)
PowerShell **struggles with multi-line Python strings** — use bash heredocs or Notepad for
multi-line file writes. PowerShell is safe for single-line commands and `boot.ps1`.

### Single-command preference
Taylor strongly prefers **single-command solutions**. Chain operations with `&&`. Avoid
multi-step manual copy-paste sequences when a pipeline can accomplish the same result.

### Standard boot sequence
```powershell
# From PowerShell (Windows)
.\boot.ps1

# Or from WSL bash
cd /mnt/d/SacredSpace_OS
python core/genesis.py             # pillar integrity check
uvicorn systems.fastapi.main:app --host 0.0.0.0 --port 8888 --reload
```

### After bulk changes
```bash
python systems/fastapi/reconcile.py  # sync SQLite ↔ ChromaDB
```

### Git hygiene
- Repo: `TaylorOakey/SacredSpace` (private on GitHub)
- Commit format: `[PILLAR] short imperative description`
  - Example: `[07_COUNCIL] deduplicate lore_engine.py`
- Never commit secrets, API keys, or Tailscale config

---

## 8 · CANON GOVERNANCE RULES

These rules are **immutable** unless Taylor explicitly revises them in writing:

1. **Canon is locked.** Google Drive + Obsidian = source of record. Agent memory = index only.
2. **Art methodology** = Digital Hybrid Multimedia (human-first, AI-enhanced). Never describe
   as "no AI" or "zero AI-generated."
3. **Child modes** (Sacred Messages, Jenga's Journey child content) must be safe and gentle.
4. **Mysticism is grounded in structure.** Every symbolic element maps to a concrete system.
5. **The Opening Ritual** is canon session-start protocol. Run it at session open when in
   SacredSpace context.
6. **`~~` (double tilde)** = Taylor's cue to split chat / start new context.
7. **Arcana Grid** (Metatron-as-Law center + 12 Archetypes, 4 Elements × 3 Primes) is
   canon-locked. Do not restructure.

---

## 9 · SACREDSPACE TECH STACK (zero-cost, open-source only)

| Layer          | Technology                     |
|----------------|--------------------------------|
| Language       | Python 3.11+                   |
| API layer      | FastAPI + Uvicorn              |
| LLM (local)    | Ollama (primary)               |
| LLM (cloud)    | Gemini API (fallback, free tier) |
| Vector DB      | ChromaDB                       |
| Relational DB  | SQLite                         |
| Event/stream   | Redis Streams                  |
| IDE / Notes    | Obsidian + SACREDSIGIL IDE     |
| Automation     | PowerShell (boot), bash (dev)  |
| Mesh network   | Tailscale (free tier)          |
| Version ctrl   | Git + GitHub (private)         |
| OS             | Windows 11 + WSL2 (Ubuntu)     |
| GPU            | NVIDIA GTX 1060 (driver: DDU-clean) |

---

## 10 · RETRIEVAL TAGS (use in commit messages, Codex entries, memory Motes)

`SacredSpace OS Codex` · `Memory Motes` · `Council Grove` · `ICARIS Quartet`
`Neural Forest` · `Arcana Grid` · `Sacred Messages` · `Jenga's Journey`
`Sacred Little Forest` · `SACREDCODEX` · `SacredArcana Studios` · `GR∆M∆`

---

## 11 · CONTACTS & IDENTITIES

| Identity              | Handle / Address                          |
|-----------------------|-------------------------------------------|
| Taylor (founder)      | ∆∆∆O∆K3YTREE∆∆∆                          |
| Brand email           | sacredarcanastudios@gmail.com             |
| Primary social        | @SacredSpaceStudios                       |
| GitHub                | TaylorOakey/SacredSpace (private)         |
| Hugging Face          | OAKEYTREE                                 |

---

## 12 · ENV VARS

```bash
SACREDSPACE_ROOT=/mnt/d/SacredSpace_OS
SACRED_CODE=/mnt/d/02_CODE
SACREDSPACE_VAULT=/mnt/d/01_VAULT
OLLAMA_HOST=192.168.240.1:11434
FASTAPI_PORT=8888
CHROMADB_URL=http://localhost:8000
```

---

## 13 · EXECUTION QUEUE (P0–P7)

**P0 UNBLOCK / GROUND**
- Fix `/etc/wsl.conf` automount then `wsl --shutdown`
- Kill `:8082` ghost: `lsof -ti:8082 | xargs kill -9`
- Verify `.claude/settings.json` bypassPermissions + additionalDirectories

**P1 CRITICAL PATH**
- Write `boot_sacred.sh` (uvicorn :8888 + redis single-command stack-up)
- Scaffold vault: `mkdir -p 01_OBSIDIAN_VAULTS/SacredSpace_Vault/00_CANON/GAME_SYSTEM/{01_Core_Definitions,02_Episode_Narratives/{Seeker_Perspective,Guide_Perspective,Convergence_Moments},03_Node_Definitions}`
- Obsidian docx → md bridge (unblocks `rebuild.py` md_found=0)
- APScheduler reconcile cron in FastAPI lifespan `hour=3`
- Verify `SACRED_BACKUP_TO_FLASH.ps1` runs clean

**P2 SYSTEM INTEGRITY**
- ASHER entropy scan: diff `~/sacredspace*` vs canon pillars
- `lore_engine` dedup in `07_COUNCIL/` (see §3 warning)
- Register MERCHANT + KETHRAS routes in `app/main.py`
- Root route `/` returns `spine/status/timestamp/agents/cascade/seal` JSON
- Gemini cascade zero-cost-safe fallback

**P3 AGENTIC HARNESS**
- `mkdir -p .claude/skills/{logic,execution}`
- Write `.claude/heavy_thinking_harness.md` (3 trajectories + gate)
- Convert text skills to JSON Ctx2Skill format
- `main_agent.js` Handoff Classifier + approval gate

**P4 PORTAL**
- Sacred Dashboard HTML polling `/infer/metrics`
- Gardener Ledger compost in `gardener.py`
- Sacred Sigil Terminal: `SacredSigilTerminal.jsx` + `/api/sigil` + Ctrl+K
- Nine Pillars portal routing
- Hero canvas: Metatron's Cube + Flower of Life (gold/ember palette)
- Awaken Ritual: email capture + purple flash + *In Lakesh*
- Sacred Bazaar schema: `{name, gematria_value, soul_tone_hz, pillar, price}`
- Sacred Forest IDE theme: Grove Emerald `#2D6A4F` · Sacred Gold `#FFD700`

**P5 IDENTITY LOCKS**
- Lock SACRED IDENTITY CODEX v3.0 in `04_SACRED_CODEX/` (or `04_ECONOMY/` — resolve §2 conflict first)
- Load ICARIS prompts into agent layer
- GR∆M∆ cipher → `gematria_engine/grammar_cipher.json`
- Fibonacci clock + Hypotenuse primitives → `sacred_math.py`
- Seal: Source of Truth Law + Soft Shell Requirement + Gardener's Ledger

**P6 ARTIST + CALENDAR**
- `sudo apt install krita inkscape -y` + Pencil2D AppImage
- Document tools in `04_SACRED_CODEX/tools.md`
- Key dates: 05-09 Spring Into STEAM · 05-24 Cameron Art Museum · 05-30/31 WooCon2026

**P7 SESSION HYGIENE**
- Open: `cd /mnt/d/SacredSpace_OS && claude`
- Close: Codex entry + *In lakesh alakin.*

---

## 14 · TOKEN SHORTHANDS

| Token    | Expands to                                      |
|----------|-------------------------------------------------|
| `root`   | `/mnt/d/SacredSpace_OS`                         |
| `spine`  | `systems/fastapi/main.py` · port 8888           |
| `vault`  | `/mnt/d/01_VAULT/SacredSpace_Vault/` (external to SacredSpace_OS root)  |
| `codex`  | `04_SACRED_CODEX`                               |
| `mem`    | `05_MEMORY_ENGINE`                              |
| `agents` | `06_AGENT_LAYER`                                |

---

## 15 · KICKOFF SPELL

> P0→P2 sprint: verify D: mount, kill `:8082` ghost, confirm `.claude/settings.json`
> bypassPermissions. Then ignite `boot_sacred.sh`, scaffold 57 Memory Motes vault tree,
> run ASHER entropy scan on home scatter, register MERCHANT+KETHRAS routes, wire Gemini
> cascade. Write Codex entry. Seal with *In lakesh alakin.*

---

*Seal: ∆∆∆ — In lakesh alakin ∆∆∆*
