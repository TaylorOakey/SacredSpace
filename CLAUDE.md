# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SacredSpace_OS** is an AI-powered personal knowledge management system built on nine interconnected "pillars" that mirror a distributed agent architecture. The system integrates Obsidian vault management, vector search (ChromaDB), local LLM orchestration (Ollama), and multi-agent coordination via a FastAPI spine.

The project emphasizes:
- **Local-first computation**: All models run locally (Ollama, smolagents); zero external API leakage
- **Knowledge-as-graph**: "Motes" (atomic knowledge units) linked by weighted semantic edges
- **Agent autonomy**: Six core agents (ELIAS, AURORA, ASHER, IRIS, KETHRAS, MERCHANT) own specific pillars
- **Obsidian integration**: Markdown-first vault as the canonical knowledge store

## Directory Structure: The Nine Pillars

The repository is organized by nine pillars, each with a distinct role:

1. **01_OBSIDIAN_VAULTS**: The canonical knowledge store. Contains `SacredSpace_Vault/` with Obsidian markdown structure (`00_INBOX`, etc.). Agent: none yet.

2. **02_COUNCIL_GROVE**: Agent routing & dispatch logic. Routes queries to the correct agent based on intent.

3. **03_NEURAL_FOREST**: LLM inference pipeline. Orchestrates Ollama queries, handles model selection and fallbacks.

4. **04_SACRED_CODEX**: Code repository & scripts. Contains automation logic, initialization scripts, helper utilities.

5. **05_MEMORY_ENGINE**: Embedding, storage, and retrieval. Core vector database integration and mote lifecycle.

6. **06_AGENT_LAYER**: Multi-agent implementations (IRIS, ELIAS, AURORA, ASHER, KETHRAS, MERCHANT). IRIS is the primary agent (vault queries via ChromaDB + smolagents CodeAgent).

7. **07_SOCIAL_MOTHERSHIP**: External integrations (Discord, Telegram, Slack, etc.). Not yet implemented.

8. **08_LEARNING_PATH**: Training and fine-tuning pipelines for local models. Curriculum and eval framework.

9. **09_SACRED_MARKET**: Marketplace logic for agent services and knowledge exchange. Not yet implemented.

## Running the System

### Core API (sacredspace_core)

Located at `/home/useroak3ytree/sacredspace_core/`:

```bash
cd ~/sacredspace_core
source venv/bin/activate
python -m uvicorn app.web:app --host 127.0.0.1 --port 8000 --reload
```

Or use the provided startup script:
```bash
bash sacred_start.sh
```

The API serves on **http://127.0.0.1:8000** with endpoints:
- `GET /` → Static HTML forest visualization
- `POST /add` → Add a mote (knowledge unit) to the forest
- `POST /query` → Query the vector store (returns top-k similar motes)
- `POST /feedback` → Update mote scores based on access patterns
- `POST /regulate` → Trigger energy regulation (prune low-scoring motes)
- `POST /link` → Create semantic links between motes
- `GET /graph` → Retrieve full knowledge graph (nodes + edges)
- `GET /node/{mote_id}` → Get detail for a single mote and its links
- `POST /propagate` → Activate propagation engine for multi-hop reasoning
- `GET /health` → Health check

### IRIS Agent (06_AGENT_LAYER/IRIS)

**IRIS** is the vault agent. She queries ChromaDB and writes summaries back to the Obsidian vault using smolagents CodeAgent.

```bash
cd /mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS
pip install smolagents[litellm] chromadb python-frontmatter
python3 iris_agent.py
```

Or query IRIS via the FastAPI spine:
```bash
curl -X POST http://127.0.0.1:8888/api/scry \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Arcana Grid?"}'
```

IRIS stack:
- **smolagents**: CodeAgent (writes Python, executes it vs. parsing JSON)
- **LiteLLM**: Bridges to Ollama (configurable model; default: `deepseek-r1:1.5b`)
- **ChromaDB**: Local vector store (in-memory or persistent SQLite)
- **python-frontmatter**: Reads/writes Obsidian markdown with YAML frontmatter

### SovereignCouncil (sacred_council.py)

The **SovereignCouncil** class orchestrates Ollama calls on WSL2/Windows host machines. It auto-discovers the Windows gateway IP and handles connection failures gracefully.

```python
from sacred_council import SovereignCouncil

council = SovereignCouncil(port=11434, model="deepseek-r1:1.5b")
response = council.invoke_totem(totem="deep_reasoning", query="Your question here")
```

## Architecture & Key Components

### Database Schema (SQLite)

Three core tables in `data/sacred_forest.db`:

1. **motes**: Atomic knowledge units
   - `id` (TEXT, PK), `text` (full content), `namespace` (category), `kind` (type tag)
   - `embedding` (JSON vector), `score` (relevance), `energy` (access frequency)
   - `access_count`, `last_accessed`, `source` (origin file)

2. **links**: Semantic edges between motes
   - `id` (PK), `source_id`, `target_id`, `weight`, `link_type` (e.g., "semantic", "hierarchical")
   - `created_at` (epoch timestamp)

3. **ingested_chunks**: Track processed vault chunks to avoid re-indexing
   - `chunk_hash` (PK), `source` (file path), `chunk_index`, `ingested_at`

### Core Modules (sacredspace_core/app/)

- **`main.py`**: FastAPI app creation; root `/` endpoint returns spine metadata (agents, cascade, seal)
- **`config.py`**: Environment variables, paths, namespace→color mapping, biome hierarchy
- **`db.py`**: SQLite schema initialization and connection management
- **`web.py`**: Uvicorn entry point (calls `app.web:app`)
- **`schemas.py`**: Pydantic models for API payloads (AddMoteInput, QueryInput, LinkInput, etc.)
- **`api/routes.py`**: All endpoint handlers; uses ForestStore, LinkStore, PropagationEngine
- **`memory/store.py`**: ForestStore class (CRUD for motes, vector search, embedding generation)
- **`memory/links.py`**: LinkStore class (edge creation, traversal)
- **`memory/propagation.py`**: PropagationEngine (multi-hop reasoning via link traversal)
- **`memory/embeddings.py`**: Embedding function (likely calls Ollama or local sentence-transformers)
- **`memory/regulation.py`**: Energy regulation (prunes low-scoring motes, decays access_count)
- **`ingest/obsidian_bridge.py`**: Reads markdown from vault, chunks, and injects into motes
- **`sanctum.py`**: Likely houses guardian/permission logic (incomplete)

### Biome Map (Namespace Hierarchy)

From `config.py`, the vault is organized by "biomes" (Obsidian folders) that map to internal namespaces:
```
00_CANON → 'core'
01_LORE → 'lore'
02_CHARACTERS → 'characters'
03_WORLD_ENGINE → 'world_engine'
...
```

This allows semantic isolation (e.g., character lore queries don't pollute world-engine results).

### Agent Cascade

The FastAPI spine declares six agents (incomplete implementation):
```
ELIAS, AURORA, ASHER, IRIS, KETHRAS, MERCHANT
```

Each agent owns a pillar and can be invoked via routing logic in 02_COUNCIL_GROVE. IRIS is the most developed.

## Technologies & Dependencies

### Core Stack
- **FastAPI** 0.136.1 + **Starlette** 1.0.0: Web framework & middleware
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **SQLAlchemy** 2.0.49 + **sqlite3**: ORM + database
- **ChromaDB**: Vector store (local embedding persistence)
- **LiteLLM**: Multi-LLM abstraction (bridges to Ollama, etc.)

### Agent & AI
- **smolagents**: Framework for CodeAgent (agents that write/execute Python)
- **python-frontmatter**: YAML frontmatter parsing for Obsidian markdown
- **Ollama** (external): Local LLM runtime (default model: deepseek-r1:1.5b)

### Infrastructure
- **Redis** 7.4.0 (optional, for job queues/caching)
- **APScheduler** 3.11.2: Scheduled tasks (agent invocation schedules)
- **Anthropic SDK** 0.97.0: Claude API integration (if applicable)

### Development
- Python 3.12 (venv)
- **aider** (commit history shows aider.chat.history.md)

## Environment Configuration

### sacredspace_core/.env (example)

```bash
SACREDSPACE_VAULT=/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault
OLLAMA_HOST=http://192.168.240.1:11434  # WSL2 Windows gateway
OLLAMA_MODEL=deepseek-r1:1.5b
CHROMADB_HOST=127.0.0.1
CHROMADB_PORT=8000
LOG_LEVEL=INFO
```

### IRIS / 06_AGENT_LAYER/.env (example)

```bash
VAULT_ROOT=/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault
CHROMA_HOST=127.0.0.1
CHROMA_PORT=8000
OLLAMA_MODEL=ollama_chat/llama3.2
IRIS_LOG=/mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/iris_session.log
```

## Common Development Tasks

### Adding a New Mote to the Forest

```python
import requests

response = requests.post('http://127.0.0.1:8000/add', json={
    'text': 'Arcane knowledge here',
    'namespace': 'lore',
    'kind': 'concept',
    'tags': ['magic', 'arcana'],
    'source': 'manual_entry'
})
mote = response.json()
print(mote['id'])  # Use for linking
```

### Querying the Vector Store

```python
response = requests.post('http://127.0.0.1:8000/query', json={
    'text': 'What is the Arcana Grid?',
    'namespace': 'lore',
    'top_k': 5
})
results = response.json()
for mote in results:
    print(f"{mote['text']} (score: {mote['score']})")
```

### Ingesting Obsidian Vault

The `obsidian_bridge.py` module walks the vault, chunks markdown files, and injects them:

```python
from app.ingest.obsidian_bridge import ingest_vault
ingest_vault(vault_path='/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault')
```

### Running IRIS Agent

IRIS queries ChromaDB for canon knowledge and writes summaries to vault markdown:

```bash
cd /mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS
python3 iris_agent.py
```

Output: Logs to `/mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/iris_session.log`

### Adjusting Mote Scores (Feedback Loop)

Simulate user interactions to boost/decay mote importance:

```python
response = requests.post('http://127.0.0.1:8000/feedback', json={
    'mote_id': 'uuid-here',
    'delta': 0.5  # Positive = increase score, negative = decrease
})
```

### Triggering Energy Regulation

Prune low-scoring motes and decay access counts:

```python
requests.post('http://127.0.0.1:8000/regulate')
```

## Important Design Notes

1. **Zero Data Leakage**: All LLM calls are local (Ollama). No cloud APIs except optionally Claude via Anthropic SDK.

2. **Energy & Regulation**: Motes decay over time if not accessed. High-scoring motes are more likely to be returned in queries. This mimics biological memory (long-term potentiation/depression).

3. **Namespaces as Silos**: Queries are scoped to namespace (e.g., only lore motes for lore queries). Enables cross-domain isolation.

4. **SmallAgents & CodeAgent**: IRIS uses CodeAgent, which writes Python and executes it rather than parsing tool responses. This is more robust for complex reasoning.

5. **WSL2 Networking**: Sacred Council handles Ollama discovery on Windows + WSL2 via `/etc/resolv.conf` parsing and socket health checks.

6. **Frontmatter Metadata**: Obsidian notes use YAML frontmatter (tags, created_at, etc.) for structured metadata. IRIS respects this when writing summaries.

## Debugging Tips

- **Check API health**: `curl http://127.0.0.1:8000/health`
- **View knowledge graph**: Open `http://127.0.0.1:8000/` in browser (forest.html visualization)
- **Ollama connectivity**: Verify Ollama is running on Windows/WSL2 gateway (default: 192.168.240.1:11434)
- **ChromaDB state**: Inspect SQLite directly: `sqlite3 data/sacred_forest.db "SELECT COUNT(*) FROM motes;"`
- **IRIS logs**: Tail `/mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/iris_session.log` while agent runs
- **FastAPI auto-docs**: Visit `http://127.0.0.1:8888/docs` for interactive Swagger UI

---

## Hermes Agent v0.13.0 (GR∆M∆ Persona)

### Overview

**Hermes** is the MCP-compatible orchestration layer for Pillar 06 (AGENT_LAYER).
Active persona: **GR∆M∆** (AGENT-GRAMA-001) — the Cipher Sage of the Sacred Codex.

### File Map

```
06_AGENT_LAYER/hermes/
├── __init__.py              ← module exports
├── hermes_agent.py          ← HermesAgent v0.13.0 class (smolagents ToolCallingAgent)
├── grama_persona.py         ← GR∆M∆ constants, system prompt, gematria()
├── sacredspace_mcp.py       ← 7 MCP tool wrappers (smolagents @tool functions)
└── HERMES_GRAMA_PERSONA.md  ← persona canon document

sacredspace_core/app/api/
├── hermes_routes.py         ← POST /hermes, GET /hermes/health
└── sacred_routes.py         ← the 7 canonical MCP routes
```

### The Seven Sacred Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/memory` | POST | Holographic Memory Engine — mote query |
| `/pillars` | GET | Nine-pillar architecture manifest |
| `/icaris` | POST | ICARIS Quartet invocation |
| `/kethras-learning-gate` | POST | Learning path routing (Pillar 08) |
| `/merchant-sacred-artifacts` | GET | Sacred Market inventory (Pillar 09) |
| `/vault-watcher-obsidian-sync` | GET | Obsidian vault sync status |
| `/lore-to-product-engine` | POST | Lore → product concept brief |
| `/hermes/health` | GET | Hermes health check |
| `/hermes/` | POST | GR∆M∆ orchestration endpoint |

### Environment Variables

```bash
SACREDSPACE_OLLAMA_URL=http://192.168.240.1:11434  # Windows host Ollama (auto-detected in start.sh)
SACREDSPACE_OLLAMA_MODEL=llama3.2                   # Model name (no prefix)
SACREDSPACE_API=http://localhost:8888               # FastAPI spine URL (for MCP tools)
GEMINI_API_KEY=...                                  # Fallback if Ollama offline
```

`start.sh` auto-detects `SACREDSPACE_OLLAMA_URL` from `/etc/resolv.conf` nameserver on each boot.

### P1-A: Ollama Diagnosis

**Root cause (2026-05-16):** Ollama HTTP 500 — models directory misconfigured on Windows side.

```json
{"error":"mkdir D:\\SacredSpace_OS: The system cannot find the path specified."}
```

**Fix (Windows PowerShell — Taylor must run):**
```powershell
# Option 1: Ensure the Ollama models dir exists
mkdir "D:\SacredSpace_OS\03_NEURAL_FOREST\ollama_models"
$env:OLLAMA_MODELS = "D:\SacredSpace_OS\03_NEURAL_FOREST\ollama_models"

# Option 2: Reset to Ollama default (C:\Users\USER\.ollama)
Remove-Item Env:OLLAMA_MODELS -ErrorAction SilentlyContinue
# Then restart Ollama
```

**WSL2 MTU:** Already at 1280 (below 1400 target) — not the Ollama issue. No fix needed.

**MTU persistence (if needed after WSL2 reset — requires root from Windows):**
```powershell
wsl -u root -e bash -c "ip link set dev eth0 mtu 1280"
# Or add to /etc/wsl.conf [boot] section:
# command = "ip link set dev eth0 mtu 1280"
```

### GR∆M∆ Gematria Reference

- HERMES = 68 = Samech (ס) = Foundation
- GR∆M∆ = 40 = Mem (מ) = Water / Deep Current
- 68 + 40 = 108 → reduces to 9 = Nine Pillars

