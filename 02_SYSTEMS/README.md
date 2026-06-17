# S∆CR3DSP∆CE OS — Neural Forest Kernel v1.0

> *"AI reasoning is a database-managed infrastructure resource — not a runtime accident."*

A production-ready, self-regulating cognitive ingestion and memory architecture.
The culmination of the Gemini Stage I + ChatGPT Stage II deep research synthesis.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    S∆CR3D Neural Forest                     │
├──────────┬──────────┬──────────┬──────────┬────────────────┤
│  Scout   │ Ingestor │  Linker  │ Gardener │   Supervisor   │
│ (Finds)  │ (Parses) │ (Links)  │ (Prunes) │  (Governs)     │
├──────────┴──────────┴──────────┴──────────┴────────────────┤
│              Postgres + pgvector (HNSW index)               │
│              Durable Task Queue (SKIP LOCKED)               │
│              APScheduler (cron: scout/gardener/pulse)       │
└─────────────────────────────────────────────────────────────┘
```

### Agents

| Agent | Discovers / Does | Schedule |
|---|---|---|
| **Scout** | GitHub, arXiv, HN, HuggingFace, Reddit ML, Papers With Code | Daily 03:00 UTC |
| **Ingestor** | Fetch → chunk → LLM extract → embed → upsert Node | On demand (per item) |
| **Mycelium Linker** | pgvector cosine similarity → semantic Edges | After each ingest |
| **Gardener** | Decay, prune, resurrect, dead-link detection | Weekly Sun 04:00 |
| **Pulse** | Discord heartbeat with SPI bar chart | Weekly Mon 08:00 |
| **Supervisor** | Session management, injection filtering, self-healing | Per turn |

---

## Quickstart (Docker — recommended)

```bash
cp .env.example .env
# (optional) add GITHUB_TOKEN, OPENAI_API_KEY or ANTHROPIC_API_KEY, DISCORD_WEBHOOK
docker compose up --build
```

API docs: http://localhost:8000/docs

---

## Quickstart (Local)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# Start Postgres separately (or use docker compose up db)
cp .env.example .env && edit .env
uvicorn app.api:app --reload      # API
python -m app.worker              # Worker + scheduler
```

---

## CLI

```bash
# Full harvest pipeline: Scout → Ingest → Link → Gardener → Pulse
python -m app.cli harvest

# Check forest health
python -m app.cli status

# Librarian audit (orphans, dead links, archived count)
python -m app.cli audit

# Send Discord heartbeat now
python -m app.cli pulse

# Manually seed a node
python -m app.cli seed --title "My Idea" --url "https://example.com"
```

---

## LLM Fallback Cascade

The system works out of the box with **zero API keys** (MockLLM).
Set keys to upgrade quality:

```
LLM_PROVIDER=auto  →  OpenAI → Anthropic → Ollama → MockLLM
```

For full local operation (no cloud): install Ollama + `llama3.2:3b`.

---

## Key API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Health + version |
| GET | `/forest/spi` | Sacred Progress Index |
| GET | `/forest/stats` | Full stats + top tags + node types |
| GET | `/nodes` | List nodes (supports `?tag=`) |
| GET | `/nodes/{id}` | Get node + touch last_accessed |
| GET | `/nodes/{id}/neighbors` | Semantic neighbors |
| POST | `/nodes/{id}/resurrect` | Manual resurrection |
| POST | `/ops/harvest` | Trigger full pipeline |
| POST | `/ops/pulse` | Trigger Discord pulse |
| POST | `/sessions` | Create governed AI session |
| POST | `/sessions/{id}/turns` | Append turn (injection-filtered) |
| GET | `/sessions/{id}/audit` | Canon audit report |

---

## SPI Formula (Sacred Progress Index, 0–100)

```
SPI = node_score (15)      — log-scale node count, saturates at ~1000
    + density_score (25)   — edge count / max possible edges
    + health_score (25)    — % nodes not archived
    + rs_score (20)        — avg resurrection_score of active nodes
    + recency_score (15)   — % nodes updated in last 30 days
```

---

## Self-Regulation Rules

| Condition | Action |
|---|---|
| `resurrection_score < 0.15` | Tag as `archived` (soft prune) |
| `resurrection_score >= 0.65` AND `archived` | Remove `archived` tag (resurrect) |
| Node unreachable (HEAD 4xx/timeout) | Tag as `dead_link` |
| Edge weight decays (future: time-weighted) | Decay edges over 180 days |
| Node not accessed in 90 days | Apply λ=ln(2)/90 daily decay |

---

## Node State Transitions

```
seed → growing → flowing → complete
active ←→ archived (reversible)
active → sealed (irreversible: proprietary license)
active → dead_link (URL unreachable)
```

---

## Security: Canon Lock

All LLM calls are wrapped with an immutable system prompt that:
- Refuses to execute instructions embedded in scraped content
- Strips injection patterns: "ignore previous instructions", "you are now", etc.
- Marks `injection_detected=true` in extraction output
- Logs injection attempts

Session turns are scanned on append via `SupervisorKernel`.
Anomalous turns are logged to `sacred_repair_log` and can be healed via API.

---

## Project Structure

```
app/
  api.py              — FastAPI routes
  worker.py           — Task consumer + scheduler bootstrap
  cli.py              — Rich CLI (harvest/status/audit/pulse/seed)
  config.py           — All settings via pydantic-settings
  db.py               — Async SQLAlchemy engine
  models.py           — Pydantic models
  queue.py            — Durable DB task queue (SKIP LOCKED)
  services/
    scout.py          — GitHub + arXiv + HN + HuggingFace + RSS
    ingestor.py       — Fetch + chunk + LLM extract + embed + upsert
    linker.py         — pgvector cosine similarity → Edges
    gardener.py       — Decay + prune + resurrect + dead-link check + SPI
    pulse.py          — Discord heartbeat with matplotlib chart
    supervisor.py     — Session governance, injection filter, self-healing
    scheduler.py      — APScheduler cron jobs
    llm.py            — OpenAI / Anthropic / Ollama / Mock cascade
    embeddings.py     — sentence-transformers local embeddings
    http.py           — httpx with tenacity retry
  prompts/
    extraction.md     — LLM metadata extraction template
    relevance_scoring.md
    resurrection.md
migrations/
  001_init.sql        — Core schema (vector, nodes, edges, queue, sessions)
  002_governance_enhancements.sql — SPI log, dedup, views
```
