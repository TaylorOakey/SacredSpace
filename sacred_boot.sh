#!/usr/bin/env bash
# ∆ SacredSpace OS Boot Script
set -euo pipefail

LOG="/home/useroak3ytree/sacredspace/boot.log"
SPINE="/home/useroak3ytree/sacredspace/06_AGENT_LAYER/sacred_spine_v2.py"
OLLAMA_HOST="192.168.240.1"
OLLAMA_PORT="11434"

log() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

log "∆∆∆ SACRED SPACE OS BOOT ∆∆∆"

# ∆ 1 — Ollama
if curl -sf "http://${OLLAMA_HOST}:${OLLAMA_PORT}/api/tags" > /dev/null 2>&1; then
    log "✓ Ollama reachable at ${OLLAMA_HOST}:${OLLAMA_PORT}"
else
    log "⚠  Ollama not reachable — start 'ollama serve' on Windows first"
fi

# ∆ 2 — Tailscale
if command -v tailscale &>/dev/null; then
    STATUS=$(tailscale status --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print('up' if d.get('BackendState')=='Running' else 'down')" 2>/dev/null || echo "unknown")
    log "∆ Tailscale: ${STATUS}"
fi

# ∆ 3 — FastAPI Spine
if lsof -ti:8888 > /dev/null 2>&1; then
    log "✓ Spine already running on :8888"
else
    log "∆ Starting Sacred Spine v2 on :8888..."
    nohup python3 "$SPINE" >> "$LOG" 2>&1 &
    SPINE_PID=$!
    sleep 2
    if kill -0 "$SPINE_PID" 2>/dev/null; then
        log "✓ Spine started (PID ${SPINE_PID})"
    else
        log "✗ Spine failed to start — check ${LOG}"
    fi
fi

# ∆ 4 — Summary
log "∆∆∆ BOOT COMPLETE ∆∆∆"
log "  Spine:   http://localhost:8888"
log "  Docs:    http://localhost:8888/docs"
log "  Health:  http://localhost:8888/health"
log "  Ollama:  http://${OLLAMA_HOST}:${OLLAMA_PORT}"
