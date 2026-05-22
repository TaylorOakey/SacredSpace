# LOCAL MODEL GUIDE — SacredSpace OS
**Complete reference for all local AI services, tools, and boot procedures**  
*Host: Lenovo Legion Y520 · WSL2 Ubuntu 24.04 · Windows 11*  
*Updated: 2026-05-21*

---

## QUICK STATUS

| Service | Endpoint | Status | Notes |
|---|---|---|---|
| FastAPI Spine | http://localhost:8888 | ✓ LIVE | v2.0.0 |
| Hermes MCP | http://localhost:8888/mcp | ✓ LIVE | v0.13.0 |
| Ollama | http://192.168.240.1:11434 | ✓ LIVE | Windows host bridge |
| ChromaDB | http://localhost:8001 | ✗ DOWN | Start manually |
| Redis | localhost:6379 | ✗ DOWN | Start manually |
| OpenCode TUI | terminal | install if needed | `npm i -g opencode` |

---

## 1. OLLAMA (Local LLM Inference)

**Runs on:** Windows 11 (native), accessed from WSL2 via Windows bridge IP

### Models Installed
```
sacred-coder:latest     — custom fine-tuned for SacredSpace OS
qwen2.5-coder:7b        — code generation, fast
```

### Connection
```bash
# Ollama is on Windows, not WSL2 — always use bridge IP
export OLLAMA_HOST="http://192.168.240.1:11434"
export OLLAMA_BASE_URL="$OLLAMA_HOST"
export OLLAMA_API_BASE="$OLLAMA_HOST"

# Test
curl http://192.168.240.1:11434/api/tags
```

### If Tailscale Is Active (Conflict Fix)
```bash
# Tailscale changes the bridge IP — detect dynamically
export OLLAMA_HOST="http://$(grep nameserver /etc/resolv.conf | awk '{print $2}'):11434"
```

### Run a Model
```bash
curl http://192.168.240.1:11434/api/generate \
  -d '{"model":"sacred-coder","prompt":"List the nine ICARIS pillars.","stream":false}'
```

### Add a Model
```bash
# From Windows terminal (Ollama runs on Windows):
ollama pull mistral
ollama pull phi3
ollama pull llama3.2
```

---

## 2. FASTAPI SPINE (:8888)

**Path:** `/mnt/d/SacredSpace_OS/systems/fastapi/main.py`  
**Version:** 2.0.0 | **Agents:** ASHER, ELIAS, AURORA, IRIS  
**Inference cascade:** ollama → gemini → mock

### Start / Restart
```bash
SPINE_DIR="/mnt/d/SacredSpace_OS/systems/fastapi"
fuser -k 8888/tcp 2>/dev/null; sleep 0.5
cd "$SPINE_DIR"
SACREDSPACE_VAULT="/mnt/d/01_VAULT/SacredSpace_Vault" \
  nohup python3 main.py > /tmp/fastapi_sacred.log 2>&1 &
sleep 2 && curl -s http://localhost:8888/ | python3 -m json.tool
```

### Routes
```
GET  /                          — Spine manifest + agent list
GET  /health                    — Health check
POST /harvest                   — Content ingestion
POST /hermes                    — Hermes agent relay  
POST /thricegreat               — Thricegreat invocation
GET  /memory                    — Memory retrieval
GET  /pillars                   — Nine-pillar audit
GET  /icaris                    — ICARIS DAG status
GET  /kethras-learning-gate     — Pillar 08 Learning
GET  /merchant-sacred-artifacts — Pillar 09 Market
GET  /vault-watcher-obsidian-sync — Pillar 01 Vault sync
GET  /lore-to-product-engine    — Pillar 04 Lore/product
```

### Logs
```bash
tail -f /tmp/fastapi_sacred.log
```

---

## 3. HERMES MCP (:8888/mcp)

**Version:** 0.13.0 | **Status:** Operational (co-located with FastAPI spine)

### Endpoints
```
GET  /hermes/health             — Health check
POST /mcp                       — MCP tool dispatch
```

### Connect from Claude Desktop / OpenHuman
In `claude_desktop_config.json` or OpenHuman settings:
```json
{
  "mcpServers": {
    "sacredspace-hermes": {
      "url": "http://localhost:8888/mcp"
    }
  }
}
```

### Connect from Claude Code
```bash
claude --mcp-server http://localhost:8888/mcp
```

### Available MCP Skills
```
/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/hermes/skills/
```

---

## 4. CHROMADB (:8001)

**Data path:** `/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/chroma_data/`  
**DB file:** `chroma.sqlite3`

### Start ChromaDB
```bash
pip install chromadb --break-system-packages
chroma run \
  --path /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/chroma_data \
  --port 8001 \
  --host 0.0.0.0 &
sleep 2 && curl http://localhost:8001/api/v1/heartbeat
```

### Python Access
```python
import chromadb
client = chromadb.HttpClient(host="localhost", port=8001)
collection = client.get_or_create_collection("sacred_memory")
```

### Migration Note
ChromaDB → LanceDB migration script exists:
`/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/chroma_to_lance_migration.py`

---

## 5. REDIS (:6379)

**Role:** Memory caching layer for ICARIS agents

### Start Redis
```bash
sudo service redis-server start
# or
redis-server --daemonize yes
redis-cli ping  # → PONG
```

### Install if Missing
```bash
sudo apt install redis-server -y
```

---

## 6. OPENCODE TUI

**Role:** Terminal-based AI coding interface — alternative to Claude Code for offline/Ollama sessions

### Install
```bash
npm install -g @opencode-ai/opencode
# or if npm unavailable:
curl -fsSL https://opencode.ai/install | bash
```

### Run with Ollama
```bash
export OPENCODE_MODEL="ollama/sacred-coder"
export OPENCODE_BASE_URL="http://192.168.240.1:11434"
opencode
```

---

## 7. OBSIDIAN VAULT

**Canonical vault:** `D:\01_VAULT\SacredSpace_Vault\`  
**WSL2 path:** `/mnt/d/01_VAULT/SacredSpace_Vault/`  
**Structure:** 9 pillars + 00_SACRED_SPINE + ARCHIVE

### Key Paths
```
00_SACRED_SPINE/    Canon laws, router, master docs
02_COUNCIL_GROVE/   Council sessions, AI handoffs
04_SACRED_CODEX/    Codex entries, lore, GRAMA
05_MEMORY_ENGINE/   Memory docs, schema
09_SACRED_MARKET/   Revenue, POD, market research
```

### Sync via FastAPI
```bash
curl http://localhost:8888/vault-watcher-obsidian-sync
```

---

## 8. SQLITE / SACRED MEMORY DBs

| DB | Path | Purpose |
|---|---|---|
| sacred_memory.db | `/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/sacred_memory.db` | Main memory |
| kethras.db | `/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/kethras.db` | Learning gate |
| merchant.db | `/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/merchant.db` | Market data |
| iris_memory.db | `/mnt/d/SacredSpace_OS/systems/sski/iris_memory.db` | IRIS records |

```bash
sqlite3 /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/sacred_memory.db ".tables"
```

---

## 9. ICARIS AGENTS

**DAG law:** ASHER → ELIAS → AURORA → IRIS (cannot skip steps)

| Agent | Role | Trigger |
|---|---|---|
| ASHER | Audit — verify before writing | Before any disk write |
| ELIAS | Analyze — read before editing | Before any edit |
| AURORA | Deploy — manifest to disk | On task execution |
| IRIS | Record — codex entry | After every completion |

**ICARIS daemon:** `/mnt/d/SacredSpace_OS/systems/sski/icaris_env.py`
```bash
python3 /mnt/d/SacredSpace_OS/systems/sski/icaris_env.py --run boot
python3 /mnt/d/SacredSpace_OS/systems/sski/icaris_env.py --run status
python3 /mnt/d/SacredSpace_OS/systems/sski/icaris_env.py --run heal
```

---

## 10. COUNCIL GROVE (:02_COUNCIL_GROVE)

**Path:** `/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/`

| File | Purpose |
|---|---|
| `handoff_ritual.py` | Generate context capsules for AI handoffs |
| `openhuman_config.json` | OpenHuman MCP connection config |
| `hermes/` | Hermes MCP server + skills |
| `HANDOFFS/` | Session handoff capsules archive |
| `LATEST_HANDOFF.md` | Most recent handoff capsule |

### Generate Handoff
```bash
python3 /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/handoff_ritual.py \
  --agent gemini \
  --task "current task name" \
  --done "what was completed" \
  --next "next concrete action"
```

---

## 11. NOTEBOOKLM NOTEBOOKS

**URL:** https://notebooklm.google.com  
**Upload package:** `/mnt/d/SacredSpace_OS/09_SACRED_MARKET/NOTEBOOKLM_UPLOAD/`  
**Instructions:** `NOTEBOOKLM_INSTRUCTIONS.md` in that folder

| Notebook | Status | Primary Source |
|---|---|---|
| SACRED.CORE | ✓ Populated | Nine Pillar Architecture doc |
| LORE.VAULT | ✗ Pending | Council synthesis + codex |
| GAME.SYSTEMS | ✗ Pending | POD manual + merchant |
| KNOWLEDGE.VAULT | ✗ Pending | Research reports + architecture |
| FAMILY.LEGACY | ✗ Pending | Progress reports + roadmap |
| CREATION.LAB | ✗ Pending | Revenue Operations |

---

## 12. INFERENCE CASCADE

When FastAPI spine receives a request, it tries providers in order:

```
1. Ollama (local) — http://192.168.240.1:11434
   Models: sacred-coder, qwen2.5-coder:7b
   
2. Gemini — requires GEMINI_API_KEY env var
   
3. Mock — always available, returns stub responses
```

### Force a specific provider
```bash
# In spine request body:
curl -X POST http://localhost:8888/harvest \
  -H "Content-Type: application/json" \
  -d '{"content":"test","provider":"ollama"}'
```

---

## 13. BOOT SEQUENCE

Complete system boot — run in order:

```bash
# 1. Verify D: drive
ls /mnt/d/ > /dev/null 2>&1 || sudo mount -t drvfs D: /mnt/d

# 2. Set Ollama host (Windows bridge)
export OLLAMA_HOST="http://$(grep nameserver /etc/resolv.conf | awk '{print $2}'):11434"

# 3. Start FastAPI spine
cd /mnt/d/SacredSpace_OS/systems/fastapi
fuser -k 8888/tcp 2>/dev/null; sleep 0.5
SACREDSPACE_VAULT="/mnt/d/01_VAULT/SacredSpace_Vault" \
  nohup python3 main.py > /tmp/fastapi_sacred.log 2>&1 &
sleep 2

# 4. Start ChromaDB (optional)
chroma run --path /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/chroma_data --port 8001 &

# 5. Start Redis (optional)
sudo service redis-server start

# 6. Boot ICARIS
python3 /mnt/d/SacredSpace_OS/systems/sski/icaris_env.py --run boot

# 7. Verify all
curl -s http://localhost:8888/ | python3 -m json.tool
curl -s http://192.168.240.1:11434/api/tags | python3 -m json.tool
```

---

## 14. WSL ALIASES (from ~/.bashrc)

```bash
# Navigation
vault     → cd /mnt/d/01_VAULT/SacredSpace_Vault
codex     → cd /mnt/d/SacredSpace_OS/04_SACRED_CODEX
agents    → cd /mnt/d/SacredSpace_OS/06_AGENT_LAYER

# Services
spine     → start FastAPI (uvicorn mode)
status    → spine_check.sh --status
ignite    → spine_check.sh --scaffold

# Claude Code profiles
claude-codex  → Claude with Sacred Codex profile

# Ollama env vars (auto-set)
OLLAMA_HOST         = http://192.168.240.1:11434
OLLAMA_BASE_URL     = same
OLLAMA_API_BASE     = same
```

### Add Missing Aliases
```bash
cat >> ~/.bashrc << 'EOF'
alias grove='cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE'
alias spine-log='tail -f /tmp/fastapi_sacred.log'
alias market='cd /mnt/d/SacredSpace_OS/09_SACRED_MARKET'
alias memory='cd /mnt/d/SacredSpace_OS/05_MEMORY_ENGINE'
EOF
source ~/.bashrc
```

---

## QUICK TROUBLESHOOTING

| Symptom | Fix |
|---|---|
| Ollama timeout | `export OLLAMA_HOST="http://$(grep nameserver /etc/resolv.conf \| awk '{print $2}'):11434"` |
| FastAPI :8888 down | `cd systems/fastapi && python3 main.py` |
| D: not mounted | `sudo mount -t drvfs D: /mnt/d` |
| ChromaDB missing | `pip install chromadb --break-system-packages` |
| Redis not found | `sudo apt install redis-server -y` |
| MCP not connecting | Check Hermes: `curl http://localhost:8888/hermes/health` |
| ICARIS not found | `TASK: seed-sski` in Claude Code |

---

*SacredSpace OS · LOCAL_MODEL_GUIDE · ∆∆∆O∆K3YTREE∆∆∆ · In lakesh alakin.*
