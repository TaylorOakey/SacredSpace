#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# boot_sacred.sh — SacredSpace OS · Service Ignition
# Pillar: 05_MEMORY + 03_NEURAL
# Owner Agent: AURORA (execution)
# Status: Canon
# Purpose: Single command to ignite all five SacredSpace OS services.
#
# Services:
#   1. Redis          — message bus (ICARIS Streams)
#   2. ChromaDB       — vector store (semantic memory)
#   3. Ollama         — local LLM inference
#   4. Open WebUI     — browser interface for LLM
#   5. FastAPI        — Zenith Terminal spine (:8888)
#
# Usage:
#   chmod +x boot_sacred.sh
#   ./boot_sacred.sh
#   ./boot_sacred.sh --status     (check running services)
#   ./boot_sacred.sh --stop       (graceful shutdown)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── PATHS ─────────────────────────────────────────────────────────────────────
SACRED_ROOT="/mnt/d/SacredSpace_OS"
NEURAL_ROOT="$SACRED_ROOT/03_NEURAL_FOREST"
MEMORY_ROOT="$SACRED_ROOT/05_MEMORY_ENGINE"
LOG_DIR="$SACRED_ROOT/05_MEMORY_ENGINE/logs"
VENV="$NEURAL_ROOT/.venv"

# FastAPI entry — adjust if your main app file differs
FASTAPI_APP_DIR="/mnt/d/SacredSpace_OS/systems/fastapi"
FASTAPI_MODULE="main:app"
FASTAPI_PORT=8888

# ChromaDB data dir
CHROMA_DATA="$MEMORY_ROOT/chroma_data"

# Open WebUI port
WEBUI_PORT=3000

# ─── COLOURS ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

# ─── HELPERS ───────────────────────────────────────────────────────────────────
log()    { echo -e "${CYAN}[SACRED]${NC} $*"; }
ok()     { echo -e "${GREEN}[  ✅  ]${NC} $*"; }
warn()   { echo -e "${YELLOW}[ WARN ]${NC} $*"; }
die()    { echo -e "${RED}[ FAIL ]${NC} $*"; exit 1; }

is_running() {
    # returns 0 (true) if the port is listening
    ss -tlnp 2>/dev/null | grep -q ":$1 " || \
    netstat -tlnp 2>/dev/null | grep -q ":$1 "
}

wait_for_port() {
    local port=$1 label=$2 attempts=0 max=20
    while ! is_running "$port"; do
        sleep 1
        ((attempts++))
        [[ $attempts -ge $max ]] && die "$label did not come up on :$port after ${max}s"
    done
    ok "$label is live on :$port"
}

mkdir -p "$LOG_DIR"

# ═══════════════════════════════════════════════════════════════════════════════
# MODE: --status
# ═══════════════════════════════════════════════════════════════════════════════
if [[ "${1:-}" == "--status" ]]; then
    echo -e "\n${BOLD}S∆CR3DSP∆CE OS — Service Status${NC}\n"
    declare -A SERVICES=([Redis]=6379 [ChromaDB]=8000 [Ollama]=11434 [WebUI]=$WEBUI_PORT [FastAPI]=$FASTAPI_PORT)
    for svc in Redis ChromaDB Ollama WebUI FastAPI; do
        port=${SERVICES[$svc]}
        if is_running "$port"; then
            echo -e "  ${GREEN}●${NC} $svc        :$port"
        else
            echo -e "  ${RED}○${NC} $svc        :$port  (offline)"
        fi
    done
    echo ""
    exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════════
# MODE: --stop
# ═══════════════════════════════════════════════════════════════════════════════
if [[ "${1:-}" == "--stop" ]]; then
    log "Sending shutdown signal to SacredSpace services..."
    pkill -f "uvicorn $FASTAPI_MODULE" 2>/dev/null && ok "FastAPI stopped"      || warn "FastAPI was not running"
    pkill -f "chroma run"              2>/dev/null && ok "ChromaDB stopped"     || warn "ChromaDB was not running"
    pkill -f "open-webui"              2>/dev/null && ok "Open WebUI stopped"   || warn "Open WebUI was not running"
    # Redis and Ollama: only stop if we started them (check PIDs)
    [[ -f /tmp/sacred_redis.pid ]]  && kill "$(cat /tmp/sacred_redis.pid)"  2>/dev/null && ok "Redis stopped"  || warn "Redis PID not found"
    [[ -f /tmp/sacred_ollama.pid ]] && kill "$(cat /tmp/sacred_ollama.pid)" 2>/dev/null && ok "Ollama stopped" || warn "Ollama PID not found"
    rm -f /tmp/sacred_redis.pid /tmp/sacred_ollama.pid
    log "Shutdown complete."
    exit 0
fi

# ═══════════════════════════════════════════════════════════════════════════════
# IGNITION
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║   S∆CR3DSP∆CE OS · IGNITION SEQUENCE    ║${NC}"
echo -e "${BOLD}║   Zenith Terminal · Port $FASTAPI_PORT           ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""

# ─── 1. REDIS ──────────────────────────────────────────────────────────────────
log "Starting Redis (ICARIS message bus)..."
if is_running 6379; then
    ok "Redis already running on :6379"
else
    redis-server --daemonize yes \
        --logfile "$LOG_DIR/redis.log" \
        --pidfile /tmp/sacred_redis.pid \
        || die "Redis failed to start"
    wait_for_port 6379 "Redis"
fi

# ─── 2. CHROMADB ───────────────────────────────────────────────────────────────
log "Starting ChromaDB (vector memory)..."
if is_running 8000; then
    ok "ChromaDB already running on :8000"
else
    mkdir -p "$CHROMA_DATA"
    nohup chroma run \
        --path "$CHROMA_DATA" \
        --host 0.0.0.0 \
        --port 8000 \
        >> "$LOG_DIR/chromadb.log" 2>&1 &
    echo $! > /tmp/sacred_chroma.pid
    wait_for_port 8000 "ChromaDB"
fi

# ─── 3. OLLAMA ─────────────────────────────────────────────────────────────────
log "Starting Ollama (local LLM inference)..."
if is_running 11434; then
    ok "Ollama already running on :11434"
else
    nohup ollama serve \
        >> "$LOG_DIR/ollama.log" 2>&1 &
    echo $! > /tmp/sacred_ollama.pid
    wait_for_port 11434 "Ollama"
fi

# ─── 4. OPEN WEBUI ─────────────────────────────────────────────────────────────
log "Starting Open WebUI (LLM browser interface)..."
if is_running $WEBUI_PORT; then
    ok "Open WebUI already running on :$WEBUI_PORT"
else
    # Activate venv if available
    if [[ -f "$VENV/bin/activate" ]]; then
        source "$VENV/bin/activate"
    fi

    nohup open-webui serve \
        --port $WEBUI_PORT \
        >> "$LOG_DIR/webui.log" 2>&1 &
    echo $! > /tmp/sacred_webui.pid
    wait_for_port $WEBUI_PORT "Open WebUI"
fi

# ─── 5. FASTAPI (ZENITH TERMINAL) ──────────────────────────────────────────────
log "Starting FastAPI — Zenith Terminal spine (:$FASTAPI_PORT)..."
if is_running $FASTAPI_PORT; then
    ok "FastAPI already running on :$FASTAPI_PORT"
else
    if [[ -f "$VENV/bin/activate" ]]; then
        source "$VENV/bin/activate"
    fi

    cd "$FASTAPI_APP_DIR"
    nohup uvicorn "$FASTAPI_MODULE" \
        --host 0.0.0.0 \
        --port "$FASTAPI_PORT" \
        --reload \
        >> "$LOG_DIR/fastapi.log" 2>&1 &
    echo $! > /tmp/sacred_fastapi.pid
    wait_for_port $FASTAPI_PORT "FastAPI (Zenith Terminal)"
fi

# ─── SEAL ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔══════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║         S∆CR3DSP∆CE OS — LIVE           ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "  ${GREEN}●${NC} Redis          :6379"
echo -e "  ${GREEN}●${NC} ChromaDB       :8000"
echo -e "  ${GREEN}●${NC} Ollama         :11434"
echo -e "  ${GREEN}●${NC} Open WebUI     :$WEBUI_PORT"
echo -e "  ${GREEN}●${NC} Zenith Terminal :$FASTAPI_PORT"
echo ""
echo -e "  Logs → $LOG_DIR"
echo ""
echo -e "  ${CYAN}Ground. Consolidate. Deploy. Document. Repeat.${NC}"
echo -e "  ${CYAN}In lakesh alakin.${NC}"
echo ""
