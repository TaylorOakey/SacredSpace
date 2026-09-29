#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# start_claude.sh — SacredSpace OS · Claude Code Ignition
# Pillar: 06_AGENT_LAYER
# Owner Agent: AURORA (execution)
# Purpose: One command to get from a fresh Ubuntu/WSL2 terminal into Claude Code,
#          rooted in the SacredSpace project.
#
# Usage:
#   chmod +x start_claude.sh
#   ./start_claude.sh                  (opens in SacredSpace_OS root)
#   ./start_claude.sh /some/other/dir  (opens elsewhere)
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; NC='\033[0m'

log()  { echo -e "${CYAN}[CLAUDE]${NC} $*"; }
ok()   { echo -e "${GREEN}[  ✅  ]${NC} $*"; }
warn() { echo -e "${YELLOW}[ WARN ]${NC} $*"; }

# ─── 1. D: drive (WSL2 only — skip cleanly if not applicable) ────────────────
if grep -qi microsoft /proc/version 2>/dev/null; then
    if ! ls /mnt/d/ >/dev/null 2>&1; then
        log "Mounting D: drive..."
        sudo mkdir -p /mnt/d
        sudo mount -t drvfs D: /mnt/d && ok "D: mounted" || warn "D: mount failed — continuing without it"
    else
        ok "D: drive accessible"
    fi
fi

# ─── 2. Claude Code CLI ───────────────────────────────────────────────────────
if ! command -v claude >/dev/null 2>&1; then
    log "Claude Code not found — installing..."
    if ! command -v node >/dev/null 2>&1; then
        curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
        sudo apt install -y nodejs
    fi
    npm install -g @anthropic-ai/claude-code
    ok "Claude Code installed"
else
    ok "Claude Code present ($(claude --version 2>/dev/null || echo 'version unknown'))"
fi

# ─── 3. Ollama / Tailscale DNS conflict fix ───────────────────────────────────
# Only needed if Ollama lives on the Windows host, not localhost.
if [[ "${SACRED_OLLAMA_ON_WINDOWS:-0}" == "1" ]]; then
    export OLLAMA_HOST="$(grep nameserver /etc/resolv.conf | awk '{print $2}'):11434"
    log "OLLAMA_HOST set to Windows host bridge: ${OLLAMA_HOST}"
fi

# ─── 4. Launch ─────────────────────────────────────────────────────────────────
TARGET_DIR="${1:-$(dirname "$(readlink -f "$0")")}"
cd "$TARGET_DIR"
log "Launching Claude Code in $(pwd)"
exec claude
