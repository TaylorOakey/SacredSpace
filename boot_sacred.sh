#!/bin/bash
# boot_sacred.sh — SacredSpace OS Session Ignition
# Run from WSL2: bash /mnt/d/SacredSpace_OS/boot_sacred.sh

SACRED_ROOT="/mnt/d/SacredSpace_OS"
SPINE_DIR="$SACRED_ROOT/systems/fastapi"
MISSION_CONTROL_DIR="$SACRED_ROOT/02_COUNCIL_GROVE/mission-control"
SIGIL_TERMINAL_DIR="$SACRED_ROOT/06_AGENT_LAYER/sacred-sigil-terminal"
LOG_DIR="$SACRED_ROOT/02_COUNCIL_GROVE/logs"

# Auto-detect Ollama gateway from WSL2 resolv.conf
OLLAMA_GW=$(grep nameserver /etc/resolv.conf | awk '{print $2}' | head -1)
OLLAMA_URL="http://${OLLAMA_GW}:11434"

mkdir -p "$LOG_DIR"

step() { echo -e "\n⟡ $1"; }
ok()   { echo "  ✓ $1"; }
warn() { echo "  ⚠ $1"; }
skip() { echo "  — $1"; }

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║   S∆CR3DSP∆CE OS — SESSION IGNITION                 ║"
echo "╚══════════════════════════════════════════════════════╝"

# ── 1. Ollama (Windows host) ───────────────────────────────────────────────
step "Ollama ($OLLAMA_URL)..."
if curl -sf --max-time 3 "$OLLAMA_URL/api/tags" > /dev/null; then
    MODELS=$(curl -sf "$OLLAMA_URL/api/tags" | python3 -c \
        "import sys,json; d=json.load(sys.stdin); print(', '.join(m['name'] for m in d.get('models',[])))" 2>/dev/null)
    ok "Ollama live — models: $MODELS"
else
    warn "Ollama offline — start Ollama on Windows, then rerun"
fi

# ── 2. FastAPI spine + MCP ─────────────────────────────────────────────────
step "FastAPI spine + MCP (:8888)..."
if curl -sf --max-time 2 http://localhost:8888/health/ > /dev/null; then
    ok "FastAPI spine already live at :8888"
    MCP_STATUS=$(curl -sf -X POST http://localhost:8888/mcp \
        -H "Content-Type: application/json" \
        -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"boot","version":"1"}},"id":1}' \
        2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result']['serverInfo']['name'])" 2>/dev/null)
    if [ -n "$MCP_STATUS" ]; then
        ok "MCP server live — $MCP_STATUS @ :8888/mcp"
    else
        warn "MCP endpoint not responding — check spine logs"
    fi
else
    export SACRED_ROOT
    export OLLAMA_BASE="$OLLAMA_URL"
    export PYTHONPATH="$SPINE_DIR"
    nohup python3 -m uvicorn app.main:app \
        --host 0.0.0.0 --port 8888 \
        > "$LOG_DIR/fastapi.log" 2>&1 &
    FASTAPI_PID=$!
    echo "  → PID $FASTAPI_PID — waiting..."
    sleep 4
    if curl -sf --max-time 3 http://localhost:8888/health/ > /dev/null; then
        ok "FastAPI spine live at :8888"
        ok "MCP server available at :8888/mcp"
    else
        warn "Spine still starting — tail $LOG_DIR/fastapi.log"
    fi
fi

# ── 3. Mission Control ─────────────────────────────────────────────────────
step "Mission Control (:3001)..."
if curl -sf --max-time 2 http://localhost:3001 > /dev/null; then
    ok "Mission Control already live at :3001"
elif [ -d "$MISSION_CONTROL_DIR/node_modules" ]; then
    cd "$MISSION_CONTROL_DIR"
    mkdir -p /run/user/1000/fnm_multishells 2>/dev/null
    export PATH="/home/useroak3ytree/.local/share/fnm:$PATH"
    eval "$(fnm env --shell bash 2>/dev/null)"
    nohup sh -c "PORT=3001 pnpm dev" \
        > "$LOG_DIR/mission_control.log" 2>&1 &
    ok "Mission Control starting at :3001 — allow ~5s"
else
    warn "node_modules missing — run: cd $MISSION_CONTROL_DIR && pnpm install"
fi

# ── 4. Sigil Terminal ──────────────────────────────────────────────────────
step "Sigil Terminal (:5174)..."
if curl -sf --max-time 2 http://localhost:5174/ > /dev/null; then
    ok "Sigil Terminal already live at :5174"
elif [ -d "$SIGIL_TERMINAL_DIR/node_modules" ]; then
    cd "$SIGIL_TERMINAL_DIR"
    mkdir -p /run/user/1000/fnm_multishells 2>/dev/null
    export PATH="/home/useroak3ytree/.local/share/fnm:$PATH"
    eval "$(fnm env --shell bash 2>/dev/null)"
    nohup sh -c "pnpm dev --port 5174 --host" \
        > "$LOG_DIR/sigil_terminal.log" 2>&1 &
    ok "Sigil Terminal starting at :5174"
elif [ -d "$SIGIL_TERMINAL_DIR" ]; then
    warn "Sigil Terminal: node_modules missing — run: cd $SIGIL_TERMINAL_DIR && pnpm install"
else
    skip "Sigil Terminal not built yet — see 04_SACRED_CODEX/SACRED_SIGIL_TERMINAL_QUICK_START.md"
fi

# ── 5. free-claude-code proxy ──────────────────────────────────────────────
step "free-claude-code proxy (:8082)..."
if curl -sf --max-time 2 http://localhost:8082/health > /dev/null; then
    ok "Proxy already live at :8082"
else
    nohup bash -c "cd ~/free-claude-code && uv run uvicorn server:app --host 0.0.0.0 --port 8082" \
        > "$LOG_DIR/proxy.log" 2>&1 &
    ok "Proxy starting at :8082"
fi

# ── 6. Status board ────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════════"
echo "  FastAPI spine  → http://localhost:8888/"
echo "  MCP server     → http://localhost:8888/mcp"
echo "  Mission Control→ http://localhost:3001/"
echo "  Sigil Terminal → http://localhost:5174/"
echo "  Proxy          → http://localhost:8082/"
echo "  Ollama         → $OLLAMA_URL"
echo "  Logs           → $LOG_DIR/"
echo "══════════════════════════════════════════════════════"
echo ""
echo "  In lakesh alakin. ∆"
echo ""
