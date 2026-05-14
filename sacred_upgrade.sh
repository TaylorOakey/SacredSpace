#!/usr/bin/env bash
# ∆ Sacred Stack Upgrade — pull new model fleet
set -euo pipefail

OLLAMA_HOST="192.168.240.1"
OLLAMA_PORT="11434"
LOG="/home/useroak3ytree/sacredspace/upgrade.log"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "∆∆∆ SACRED STACK UPGRADE INITIATED ∆∆∆"

# Verify Ollama reachable
if ! curl -sf "http://${OLLAMA_HOST}:${OLLAMA_PORT}/api/tags" > /dev/null; then
    log "✗ Ollama not reachable at ${OLLAMA_HOST}:${OLLAMA_PORT}"
    log "  Start it on Windows: ollama serve"
    exit 1
fi
log "✓ Ollama reachable"

MODELS=(
    "llama3.1:8b"         # primary — current, smarter, same VRAM as llama3
    "qwen2.5-coder:7b"    # AURORA code model
    "nomic-embed-text"    # embeddings — ChromaDB semantic search
    "phi3.5"              # fast reasoning / triage
)

# Pull via HTTP API — avoids CLI WSL path issues and CRC write errors
pull_model() {
    local model="$1"
    log "∆ Pulling ${model} via API..."
    curl -sf -X POST "http://${OLLAMA_HOST}:${OLLAMA_PORT}/api/pull" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"${model}\"}" \
        --no-buffer | python3 -u -c "
import sys, json
for line in sys.stdin:
    try:
        d = json.loads(line)
        status = d.get('status','')
        if 'pulling' in status and d.get('total'):
            pct = int(d.get('completed',0) / d.get('total',1) * 100)
            print(f'  {status}: {pct}%', flush=True)
        elif status:
            print(f'  {status}', flush=True)
    except: pass
" 2>&1 | tee -a "$LOG"
    log "✓ ${model} ready"
}

for model in "${MODELS[@]}"; do
    pull_model "$model"
done

log "∆∆∆ MODEL FLEET UPGRADED ∆∆∆"
log "Fleet: ${MODELS[*]}"
