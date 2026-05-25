---
title: "CLAUDE(1)"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/ARCHIVE/sacredspace_os_2026_docs/00_SYSTEM_CORE/temp/CLAUDE(1).md"
keyword_count: 4
keywords_found: [merchant, pod, revenue]
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 70
---

# CLAUDE.md — SacredSpace OS · Claude Code Guidance File
> Canonical root: `D:\SacredSpace_OS\` (WSL: `/mnt/d/SacredSpace_OS/`)
> Maintained by: Taylor Oakey · SacredArcana Studios
> Governing mantra: *Ground. Consolidate. Deploy. Document. Repeat. — In lakesh alakin.*

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
├── 01_CORE\          # System config, genesis.py, pillar integrity checker
├── 02_SYSTEMS\       # FastAPI spine, inference cascade, reconcile.py
├── 03_LEARNING\      # AAS AI Engineering notes, Codex entries, learning artifacts
├── 04_ECONOMY\       # Sacred Bazaar pricing, revenue flywheel, POD framework
├── 05_HABITAT\       # Sacred Little Forest land docs, campground/nursery plans
├── 06_CREATION\      # Jenga's Journey scripts, Sacred Messages, lore, art
├── 07_COUNCIL\       # Council Grove agents, SRPE Engine, tri-model governance
├── 08_LINEAGE\       # Sacred Messages archive, children's legacy system
├── 09_ARCHIVE\       # Obsidian sync exports, NotebookLM sources, SACREDCODEX
└── CLAUDE.md         ← YOU ARE HERE
```

Each pillar maps to a **canonical purpose** — do not move files across pillars without explicit intent.

---

## 3 · ACTIVE AGENTS (07_COUNCIL)

| Agent file        | Role                              | Status    |
|-------------------|-----------------------------------|-----------|
| `kethras.py`      | Keeper of thresholds / routing    | Active    |
| `merchant.py`     | Economy & Sacred Bazaar logic     | Active    |
| `lore_engine.py`  | Lore generation & archetype logic | Active ⚠️ |
| `vault_watcher.py`| Obsidian vault monitor / sync     | Active    |

> ⚠️ `lore_engine.py` has **5 duplicate versions** requiring cleanup. Do not create additional
> copies. Resolve to a single canonical version before adding new functionality.

### ICARIS Quartet (in-universe agent identities)
| Handle | Domain         | Notes                                  |
|--------|----------------|----------------------------------------|
| ELIAS  | Knowledge      | Learning / Codex retrieval             |
| AURORA | Code           | Dev assistant, script generation       |
| ASHER  | Entropy        | Memory decay, chaos-watch              |
| IRIS   | Vault          | Obsidian guardian; 4/15/15 Succession Seal |

---

## 4 · FASTAPI SPINE (02_SYSTEMS)

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
| `01_CORE/genesis.py`                         | Pillar integrity checker — run first on boot |
| `02_SYSTEMS/main.py`                         | FastAPI spine entry point                    |
| `02_SYSTEMS/reconcile.py`                    | SQLite ↔ ChromaDB sync daemon                |
| `02_SYSTEMS/inference_cascade.py`            | Ollama → Gemini → Mock provider chain        |
| `07_COUNCIL/kethras.py`                      | Council router / threshold keeper            |
| `07_COUNCIL/lore_engine.py`                  | ⚠️ Deduplicate before editing                |
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
python 01_CORE/genesis.py          # pillar integrity check
uvicorn 02_SYSTEMS.main:app --host 0.0.0.0 --port 8888 --reload
```

### After bulk changes
```bash
python 02_SYSTEMS/reconcile.py     # sync SQLite ↔ ChromaDB
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

*Seal: ∆∆∆ — In lakesh alakin ∆∆∆*
