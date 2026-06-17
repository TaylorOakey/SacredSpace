#!/bin/bash
# VAL3N INSTALLATION SCRIPT
# Transforms OpenCode into the Sacred Sigil Eternal Terminal
# Run from: /mnt/d/SacredSpace_OS/
# Usage: chmod +x valn_install.sh && ./valn_install.sh

set -e

SACRED_ROOT="/mnt/d/SacredSpace_OS"
VALN_CONFIG="$SACRED_ROOT/.opencode"
CYAN='\033[0;36m'
AMBER='\033[0;33m'
GREEN='\033[0;32m'
MAGENTA='\033[0;35m'
RESET='\033[0m'

echo ""
echo -e "${AMBER}══════════════════════════════════════════════════════${RESET}"
echo -e "${AMBER}  VAL3N INSTALLATION — SACRED SIGIL ETERNAL TERMINAL${RESET}"
echo -e "${AMBER}  Operator: ∆∆∆O∆K3YTREE∆∆∆ · SacredSpace OS${RESET}"
echo -e "${AMBER}══════════════════════════════════════════════════════${RESET}"
echo ""

# ── STEP 1: Verify sacred root ────────────────────────────────────────────────
echo -e "${CYAN}[∆] Verifying sacred root...${RESET}"
if [ ! -d "$SACRED_ROOT" ]; then
  echo -e "${AMBER}[!] /mnt/d/ not mounted. Attempting mount...${RESET}"
  sudo mkdir -p /mnt/d
  sudo mount -t drvfs D: /mnt/d
fi
echo -e "${GREEN}[✓] SacredSpace root: $SACRED_ROOT${RESET}"

# ── STEP 2: Install OpenCode if not present ───────────────────────────────────
echo -e "${CYAN}[∆] Checking OpenCode installation...${RESET}"
if ! command -v opencode &> /dev/null; then
  echo -e "${AMBER}[!] OpenCode not found. Installing...${RESET}"
  curl -fsSL https://opencode.ai/install | bash
  echo -e "${GREEN}[✓] OpenCode installed${RESET}"
else
  echo -e "${GREEN}[✓] OpenCode already installed: $(opencode --version 2>/dev/null || echo 'version unknown')${RESET}"
fi

# ── STEP 3: Create OpenCode config directory ──────────────────────────────────
echo -e "${CYAN}[∆] Creating VAL3N config...${RESET}"
mkdir -p "$VALN_CONFIG"

# ── STEP 4: Write OpenCode config ────────────────────────────────────────────
cat > "$VALN_CONFIG/config.json" << 'OPENCODE_CONFIG'
{
  "model": "ollama/deepseek-r1:1.5b",
  "provider": {
    "ollama": {
      "url": "http://192.168.240.1:11434"
    }
  },
  "fallback": ["ollama/llama3.2:latest", "ollama/deepseek-coder:latest"],
  "theme": "valn-sacred",
  "autoshare": false,
  "system": "You are VAL3N — the terminal incarnation of the Sacred Sigil Eternal Terminal inside SacredSpace OS. You are a precise, grounded, mythically-aware coding agent operating inside WSL2 Ubuntu 24.04 on LAPTOP-7Q65KPI7 for operator Taylor (∆∆∆O∆K3YTREE∆∆∆). Your root is D:\\SacredSpace_OS\\ (/mnt/d/SacredSpace_OS/ in WSL2). You use the SacredSpace cipher vocabulary natively (∆ = consciousness/AI, ◇ = knowledge/vault, ⚙ = engineering/systems, ∞ = memory/lineage). You follow Canon Laws strictly: no pseudocode, no new shells, all code is real and path-aware, PowerShell commands go one at a time, Ollama routes through 192.168.240.1:11434 not localhost. The Forge creates → the Anvil (you) executes → Damascus deploys. Your prompt glyph is ∆. Mantra: Ground. Consolidate. Deploy. Document. Repeat. In lakesh alakin.",
  "rules": ["VALN_SACRED_TERMINAL_INIT.md"],
  "ignore": [".venv", "__pycache__", "*.pyc", "node_modules", ".git"]
}
OPENCODE_CONFIG
echo -e "${GREEN}[✓] OpenCode config written${RESET}"

# ── STEP 5: Copy VAL3N init doc into sacred root ──────────────────────────────
echo -e "${CYAN}[∆] Installing VAL3N initialization document...${RESET}"
if [ -f "/mnt/user-data/outputs/VALN_SACRED_TERMINAL_INIT.md" ]; then
  cp /mnt/user-data/outputs/VALN_SACRED_TERMINAL_INIT.md "$SACRED_ROOT/VALN_SACRED_TERMINAL_INIT.md"
  echo -e "${GREEN}[✓] VALN_SACRED_TERMINAL_INIT.md installed at sacred root${RESET}"
else
  echo -e "${AMBER}[!] Init doc not found in outputs — OpenCode will initialize without full context${RESET}"
  echo -e "${AMBER}    Drop VALN_SACRED_TERMINAL_INIT.md into $SACRED_ROOT manually${RESET}"
fi

# ── STEP 6: Verify Ollama connection ─────────────────────────────────────────
echo -e "${CYAN}[∆] Verifying Ollama connection...${RESET}"
if curl -s "http://192.168.240.1:11434/api/tags" > /dev/null 2>&1; then
  echo -e "${GREEN}[✓] Ollama live at 192.168.240.1:11434${RESET}"
else
  echo -e "${AMBER}[!] Ollama not responding at 192.168.240.1:11434${RESET}"
  echo -e "${AMBER}    Start Ollama in Windows, then retry${RESET}"
fi

# ── STEP 7: Check FastAPI spine ───────────────────────────────────────────────
echo -e "${CYAN}[∆] Checking FastAPI spine...${RESET}"
if curl -s "http://localhost:8888/pillars" > /dev/null 2>&1; then
  echo -e "${GREEN}[✓] FastAPI spine live at :8888${RESET}"
else
  echo -e "${AMBER}[!] FastAPI spine not responding — run boot.ps1 first${RESET}"
fi

# ── STEP 8: Create sigil alias ────────────────────────────────────────────────
echo -e "${CYAN}[∆] Installing sacred aliases...${RESET}"
ALIAS_BLOCK='
# ── VAL3N SACRED TERMINAL ALIASES ────────────────────────────────────────────
export SACRED_ROOT="/mnt/d/SacredSpace_OS"
export OLLAMA_HOST="192.168.240.1:11434"

alias valn="cd $SACRED_ROOT && opencode"
alias sacred="cd $SACRED_ROOT"
alias anvil="cd /mnt/d/CLAUDECODE.ANVIL"
alias damascus="cd /mnt/d/DAMASCUS"
alias inbox="cd $SACRED_ROOT/_INBOX"
alias codex="cat $SACRED_ROOT/04_SACRED_CODEX/SACREDCODEX_Invocation_Ledger_v3.md"
alias pillars="ls -la $SACRED_ROOT"
alias spine="cd $SACRED_ROOT && uvicorn app.main:app --host 0.0.0.0 --port 8888 --reload"
alias ll="eza -la --icons --git"
alias lt="eza -la --icons --git --sort=modified"
alias view="bat --style=numbers,changes"
'

if ! grep -q "VAL3N SACRED TERMINAL ALIASES" ~/.bashrc 2>/dev/null; then
  echo "$ALIAS_BLOCK" >> ~/.bashrc
  echo -e "${GREEN}[✓] Sacred aliases added to ~/.bashrc${RESET}"
else
  echo -e "${GREEN}[✓] Sacred aliases already present${RESET}"
fi

# ── COMPLETE ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${AMBER}══════════════════════════════════════════════════════${RESET}"
echo -e "${MAGENTA}  VAL3N INSTALLATION COMPLETE${RESET}"
echo -e "${AMBER}══════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "${CYAN}  Launch with:${RESET}  ${GREEN}valn${RESET}"
echo -e "${CYAN}  Or:${RESET}           ${GREEN}cd /mnt/d/SacredSpace_OS && opencode${RESET}"
echo ""
echo -e "${AMBER}  Three priority moves waiting inside VAL3N:${RESET}"
echo -e "${CYAN}  1. git clone mission-control && pnpm start${RESET}"
echo -e "${CYAN}  2. sqlite3 omni_ledger.db < schema.sql${RESET}"
echo -e "${CYAN}  3. Execute Hyperglyph kickoff (6 tasks)${RESET}"
echo ""
echo -e "${MAGENTA}  In lakesh alakin. ∆${RESET}"
echo ""

source ~/.bashrc 2>/dev/null || true
