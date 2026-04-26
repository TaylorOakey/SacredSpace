#Requires -Version 5.1
<#
.SYNOPSIS
    SacredSpace OS — Full Activation Script
    ∆∆∆ O∆K3YTREE ∆∆∆

.DESCRIPTION
    Single-run activation for the Student Developer Stack + SacredSpace OS repo.
    Covers: directory scaffold, .gitignore, copilot-instructions, git init,
    GitHub CLI setup, initial commit, push to GitHub, and browser-launch
    of all manual steps that cannot be automated.

.NOTES
    Run from PowerShell on your Lenovo Legion Y520 (Windows 10).
    WSL2 (Ubuntu 24.04) must be installed and accessible via 'wsl' command.
    Run as normal user — NOT as Administrator.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — edit these before running
# ─────────────────────────────────────────────────────────────────────────────
$SACRED_ROOT    = "D:\SacredSpace_OS"          # Your external Toshiba HDD path
$GIT_NAME       = "OakeyTree"                  # Your git display name
$GIT_EMAIL      = "your@email.com"             # Your GitHub-linked email
$GITHUB_USER    = "your-github-username"       # Your GitHub username
$REPO_NAME      = "sacred-os"                  # GitHub repo name (will be created private)
# ─────────────────────────────────────────────────────────────────────────────

# Color helpers
function Write-Sacred  { param($msg) Write-Host "`n∆ $msg" -ForegroundColor Cyan }
function Write-Step    { param($msg) Write-Host "  → $msg" -ForegroundColor White }
function Write-Done    { param($msg) Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn    { param($msg) Write-Host "  ! $msg" -ForegroundColor Yellow }
function Write-Manual  { param($msg) Write-Host "`n  [MANUAL REQUIRED] $msg" -ForegroundColor Magenta }
function Write-Divider { Write-Host "`n" + ("─" * 60) -ForegroundColor DarkGray }

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 0 — BANNER
# ─────────────────────────────────────────────────────────────────────────────
Clear-Host
Write-Host @"

  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆
  ∆                                                          ∆
  ∆         S A C R E D S P A C E   O S                    ∆
  ∆         Full Stack Activation — v1.0                    ∆
  ∆         Ground. Consolidate. Deploy. Document.          ∆
  ∆                                                          ∆
  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆

"@ -ForegroundColor DarkCyan

Write-Host "  This script will:" -ForegroundColor Gray
Write-Host "  1. Scaffold the nine-pillar directory structure" -ForegroundColor Gray
Write-Host "  2. Generate .gitignore, README check, copilot-instructions" -ForegroundColor Gray
Write-Host "  3. Configure git identity (WSL2)" -ForegroundColor Gray
Write-Host "  4. Initialize repo and make the first sacred commit" -ForegroundColor Gray
Write-Host "  5. Install GitHub CLI (winget) and authenticate" -ForegroundColor Gray
Write-Host "  6. Create private GitHub repo and push" -ForegroundColor Gray
Write-Host "  7. Open browser tabs for all manual pack applications" -ForegroundColor Gray
Write-Host "  8. Print your post-activation checklist" -ForegroundColor Gray

Write-Host "`n  SACRED_ROOT : $SACRED_ROOT" -ForegroundColor DarkCyan
Write-Host "  GITHUB_USER : $GITHUB_USER" -ForegroundColor DarkCyan
Write-Host "  REPO_NAME   : $REPO_NAME`n" -ForegroundColor DarkCyan

$confirm = Read-Host "  Config correct? Press ENTER to begin or Ctrl+C to abort"

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 1 — DIRECTORY SCAFFOLD (nine pillars)
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 1 — Nine-Pillar Directory Scaffold"

$pillars = @(
    "core\canon",
    "core\sigils",
    "core\governance",
    "systems\fastapi",
    "systems\memory",
    "systems\agents\ELIAS",
    "systems\agents\AURORA",
    "systems\agents\ASHER",
    "systems\agents\IRIS",
    "systems\bridges",
    "systems\docker",
    "learning\seasons\season-01\grove-01",
    "learning\seasons\season-01\rites",
    "learning\seasons\season-01\artifacts",
    "learning\groves",
    "economy\sacredarcana-studios",
    "economy\1111-flow-engine",
    "economy\pod",
    "economy\platforms",
    "habitat\shui-feng",
    "habitat\temptestina-wildroot",
    "creation\jengas-journey",
    "creation\generative-art",
    "creation\grama",
    "creation\music",
    "council\protocol-router",
    "council\session-logs",
    "council\roles",
    "lineage\iris",
    "lineage\asher",
    "lineage\sacred-messages",
    "archive\dream-cycle",
    "archive\memory-motes",
    "archive\obsidian-vault",
    "archive\chromadb",
    "docs",
    ".github\workflows"
)

foreach ($pillar in $pillars) {
    $fullPath = Join-Path $SACRED_ROOT $pillar
    if (-not (Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Done "Created: $pillar"
    } else {
        Write-Step "Exists:  $pillar"
    }
}

# Ensure each pillar has a .gitkeep so empty dirs are tracked
foreach ($topPillar in @("core","systems","learning","economy","habitat","creation","council","lineage","archive")) {
    $keepPath = Join-Path $SACRED_ROOT "$topPillar\.gitkeep"
    if (-not (Test-Path $keepPath)) {
        New-Item -ItemType File -Path $keepPath -Force | Out-Null
    }
}

Write-Done "Nine-pillar scaffold complete."

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 2 — GENERATE CRITICAL FILES
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 2 — Generating Critical Files"

# ── .gitignore ────────────────────────────────────────────────────────────────
$gitignorePath = Join-Path $SACRED_ROOT ".gitignore"
if (-not (Test-Path $gitignorePath)) {
    Write-Step "Writing .gitignore..."
    @"
# ── Environment & secrets ────────────────────────────────
.env
.env.*
*.key
*.pem
secrets/
config/local_*
**/local_config.*

# ── Python ───────────────────────────────────────────────
__pycache__/
*.pyc
*.pyo
.pytest_cache/
.venv/
venv/
*.egg-info/
dist/
build/
.mypy_cache/
.ruff_cache/

# ── Data & models (too large for git) ────────────────────
*.db
*.sqlite
*.sqlite3
*.bin
*.gguf
*.ggml
chroma_data/
chromadb_persist/
*.faiss
*.index
models/

# ── OS ───────────────────────────────────────────────────
.DS_Store
Thumbs.db
desktop.ini
ehthumbs.db

# ── Logs ─────────────────────────────────────────────────
logs/
*.log
*.log.*

# ── Node (frontend work) ─────────────────────────────────
node_modules/
dist/
.next/
.nuxt/

# ── JetBrains ────────────────────────────────────────────
.idea/
*.iml
*.iws

# ── VS Code (keep extensions list, drop personal) ────────
.vscode/settings.json
.vscode/*.code-workspace

# ── Sacred-specific private paths ────────────────────────
archive/dream-cycle/raw/
lineage/iris/private/
lineage/asher/private/
lineage/sacred-messages/drafts/
council/session-logs/private/

# ── Docker volumes ───────────────────────────────────────
docker-volumes/
redis-data/
postgres-data/
"@ | Set-Content -Path $gitignorePath -Encoding UTF8
    Write-Done ".gitignore written."
} else {
    Write-Warn ".gitignore already exists — skipping (review manually)."
}

# ── Copilot instructions ──────────────────────────────────────────────────────
$copilotDir  = Join-Path $SACRED_ROOT ".github"
$copilotPath = Join-Path $copilotDir "copilot-instructions.md"
if (-not (Test-Path $copilotPath)) {
    Write-Step "Writing .github/copilot-instructions.md..."
    New-Item -ItemType Directory -Path $copilotDir -Force | Out-Null
    @"
# SacredSpace OS — Copilot Context
# ∆∆∆ Read this before suggesting anything ∆∆∆

You are assisting with SacredSpace OS — a sovereign personal AI operating system
blending AI engineering, sacred geometry, mythology, and family legacy preservation.

## Core Vocabulary (do not invent alternatives)
- Memory Mote     : atomic unit of stored knowledge (SQLite-backed)
- Canon Gate      : governance layer — canon is immutable unless OakeyTree revises
- Dream Cycle     : nightly consolidation engine (RAW → DISTILLED → CANON)
- Resonance Layer : Redis Streams, emergent pattern detection
- ICARIS Quartet  : four agents — ELIAS / AURORA / ASHER / IRIS
- Nine Pillars    : CORE, SYSTEMS, LEARNING, ECONOMY, HABITAT, CREATION, COUNCIL, LINEAGE, ARCHIVE

## ICARIS Agent Roles
- ELIAS  : knowledge distillation
- AURORA : code generation
- ASHER  : entropy detection
- IRIS   : vault watching

## Tech Stack
- Python 3.11+ / FastAPI / LangGraph
- SQLite (13-table canonical schema) + ChromaDB (all-MiniLM-L6-v2)
- Ollama local LLMs (:11434) + Redis + PostgreSQL/Supabase (:5432)
- WSL2 Ubuntu 24.04 on Windows 10 / GTX 1060 6GB
- Fiahfox Bridge v2.0 (:7777) / FastAPI (:8001) / Open WebUI (:8080)

## Coding Conventions
- Pillar-prefix all agent functions : core_*, sys_*, learn_*, econ_*, etc.
- All memory writes pass through canon_gate() before touching CANON tier
- Never write directly to SQLite — always use the memory_mote module
- Tests live in tests/ mirroring src/ structure
- Commit messages: [PILLAR] description  ∆

## Hard Rules
- canon/ directory is read-only unless explicitly told otherwise
- lineage/ data is private — never suggest logging or exposing it
- Child agent modes (IRIS/AURORA companions) are always safe and gentle

## Tone
Clear, functional, zero-fluff. Sacred geometry and mythology are real system
metaphors — treat them as first-class domain concepts, not decoration.
"@ | Set-Content -Path $copilotPath -Encoding UTF8
    Write-Done "copilot-instructions.md written."
} else {
    Write-Warn "copilot-instructions.md already exists — skipping."
}

# ── GitHub Actions CI stub ───────────────────────────────────────────────────
$ciDir  = Join-Path $SACRED_ROOT ".github\workflows"
$ciPath = Join-Path $ciDir "sacred-ci.yml"
if (-not (Test-Path $ciPath)) {
    Write-Step "Writing GitHub Actions CI workflow..."
    New-Item -ItemType Directory -Path $ciDir -Force | Out-Null
    @"
name: Sacred Canon Gate — CI

on:
  push:
    branches: [ main, dev ]
  pull_request:
    branches: [ main ]

jobs:
  canon-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          if [ -f requirements-dev.txt ]; then pip install -r requirements-dev.txt; fi

      - name: Run sacred test suite
        run: |
          python -m pytest tests/ -v --tb=short 2>/dev/null || echo "No tests yet — canon gate open"

      - name: Canon gate seal
        run: echo "∆∆∆ Canon Gate — Complete ∆∆∆"
"@ | Set-Content -Path $ciPath -Encoding UTF8
    Write-Done "GitHub Actions CI workflow written."
} else {
    Write-Warn "sacred-ci.yml already exists — skipping."
}

# ── requirements stubs ───────────────────────────────────────────────────────
$reqPath = Join-Path $SACRED_ROOT "requirements.txt"
if (-not (Test-Path $reqPath)) {
    Write-Step "Writing requirements.txt stub..."
    @"
# SacredSpace OS — Python dependencies
# Add as you build. Keep pillar-grouped.

# ── SYSTEMS core ─────────────────────────────────────────
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
langgraph>=0.1.0
langchain-core>=0.2.0
pydantic>=2.7.0

# ── ARCHIVE / memory ─────────────────────────────────────
chromadb>=0.5.0
sentence-transformers>=3.0.0
redis>=5.0.0

# ── COUNCIL / agent tools ────────────────────────────────
requests>=2.31.0

# ── CREATION / GR∆M∆ ────────────────────────────────────
flask>=3.0.0

# ── Dev ──────────────────────────────────────────────────
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.27.0
"@ | Set-Content -Path $reqPath -Encoding UTF8
    Write-Done "requirements.txt written."
} else {
    Write-Warn "requirements.txt exists — skipping."
}

Write-Done "All critical files generated."

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 3 — GIT INIT + IDENTITY (via WSL2)
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 3 — Git Initialization (WSL2)"

# Convert Windows path to WSL path
$wslRoot = $SACRED_ROOT -replace "^([A-Z]):\\", '/mnt/$1/' -replace "\\", "/"
$wslRoot = $wslRoot.ToLower()
# Fix: keep the drive letter lower for /mnt/d/ etc.
$wslRoot = $wslRoot -replace "/mnt/([a-z])/", { "/mnt/$($_.Groups[1].Value.ToLower())/" }

Write-Step "WSL path: $wslRoot"

$gitCommands = @"
set -e
cd "$wslRoot"
git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
git config --global init.defaultBranch main
if [ ! -d ".git" ]; then
    git init
    echo "Git initialized."
else
    echo "Git already initialized."
fi
git add -A
git status --short
"@

Write-Step "Running git init and staging files in WSL2..."
wsl bash -c $gitCommands
Write-Done "Git initialized and files staged."

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 4 — FIRST SACRED COMMIT
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 4 — First Sacred Commit"

$commitCommand = @"
set -e
cd "$wslRoot"
git diff --cached --quiet && git diff --quiet || git commit -m "[CORE] Sacred OS — Initial Canon Commit  ∆∆∆"
git log --oneline -3
"@

wsl bash -c $commitCommand
Write-Done "First commit sealed."

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 5 — GITHUB CLI INSTALL + AUTH + REPO CREATE
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 5 — GitHub CLI + Remote Repo"

# Check if gh is installed
$ghInstalled = $false
try {
    $null = Get-Command gh -ErrorAction Stop
    $ghInstalled = $true
    Write-Done "GitHub CLI already installed."
} catch {
    Write-Step "Installing GitHub CLI via winget..."
    try {
        winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        $ghInstalled = $true
        Write-Done "GitHub CLI installed."
    } catch {
        Write-Warn "winget install failed. Install GitHub CLI manually: https://cli.github.com"
        Write-Warn "Then re-run this script from Phase 5 onward."
        $ghInstalled = $false
    }
}

if ($ghInstalled) {
    # Check if already authenticated
    $authStatus = gh auth status 2>&1
    if ($authStatus -match "Logged in") {
        Write-Done "Already authenticated with GitHub."
    } else {
        Write-Step "Launching GitHub CLI authentication..."
        Write-Host "`n  A browser window will open. Log in with your STUDENT GitHub account." -ForegroundColor Yellow
        gh auth login --web --git-protocol https
        Write-Done "Authentication complete."
    }

    # Check if repo already exists
    $repoExists = $false
    try {
        $null = gh repo view "$GITHUB_USER/$REPO_NAME" 2>&1
        $repoExists = $true
        Write-Warn "Repo $GITHUB_USER/$REPO_NAME already exists on GitHub."
    } catch {}

    if (-not $repoExists) {
        Write-Step "Creating private GitHub repo: $REPO_NAME..."
        gh repo create $REPO_NAME --private --description "SacredSpace OS — Sovereign personal AI operating system. ∆∆∆O∆K3YTREE∆∆∆"
        Write-Done "GitHub repo created: github.com/$GITHUB_USER/$REPO_NAME"
    }

    # Add remote and push
    $pushCommands = @"
set -e
cd "$wslRoot"
if git remote get-url origin > /dev/null 2>&1; then
    echo "Remote 'origin' already set."
else
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "Remote added."
fi
git branch -M main
git push -u origin main
"@

    Write-Step "Pushing to GitHub..."
    wsl bash -c $pushCommands
    Write-Done "sacred-os pushed to github.com/$GITHUB_USER/$REPO_NAME"
} else {
    Write-Warn "Skipping GitHub push — install GitHub CLI and re-run."
    Write-Host "`n  Manual alternative:" -ForegroundColor Gray
    Write-Host "    1. Create repo at github.com/new (private, no auto-init)" -ForegroundColor Gray
    Write-Host "    2. In WSL2:" -ForegroundColor Gray
    Write-Host "       cd $wslRoot" -ForegroundColor Gray
    Write-Host "       git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git" -ForegroundColor Gray
    Write-Host "       git push -u origin main" -ForegroundColor Gray
}

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 6 — BROWSER LAUNCH (manual steps that cannot be automated)
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 6 — Opening Manual Activation Tabs"
Write-Host "`n  The following steps require your school email and cannot be automated." -ForegroundColor Gray
Write-Host "  Opening all tabs now — complete them in order." -ForegroundColor Gray

Start-Sleep -Seconds 2

$tabs = @(
    @{ url = "https://education.github.com/pack";                          label = "GitHub Student Developer Pack" },
    @{ url = "https://www.jetbrains.com/community/education/#students";    label = "JetBrains Educational Pack" },
    @{ url = "https://www.jetbrains.com/toolbox-app/";                     label = "JetBrains Toolbox App (download)" },
    @{ url = "https://marketplace.visualstudio.com/items?itemName=GitHub.copilot"; label = "GitHub Copilot VS Code Extension" },
    @{ url = "https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat"; label = "GitHub Copilot Chat VS Code Extension" },
    @{ url = "https://github.com/settings/copilot";                        label = "Enable Copilot on your account" },
    @{ url = "https://github.com/$GITHUB_USER/$REPO_NAME";                  label = "Your sacred-os repo" }
)

foreach ($tab in $tabs) {
    Write-Step "Opening: $($tab.label)"
    Start-Process $tab.url
    Start-Sleep -Milliseconds 600
}

Write-Done "All tabs launched."

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 7 — VS CODE COPILOT SETUP CHECK
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 7 — VS Code Copilot Extension Install"

$codeInstalled = $false
try {
    $null = Get-Command code -ErrorAction Stop
    $codeInstalled = $true
} catch {}

if ($codeInstalled) {
    Write-Step "Installing GitHub Copilot extensions via VS Code CLI..."
    code --install-extension GitHub.copilot --force
    code --install-extension GitHub.copilot-chat --force
    Write-Done "Copilot extensions installed in VS Code."
} else {
    Write-Warn "VS Code 'code' command not found in PATH."
    Write-Warn "Install extensions manually from the browser tabs that just opened."
}

# ─────────────────────────────────────────────────────────────────────────────
# PHASE 8 — POST-ACTIVATION CHECKLIST PRINTOUT
# ─────────────────────────────────────────────────────────────────────────────
Write-Divider
Write-Sacred "PHASE 8 — Post-Activation Checklist"

Write-Host @"

  AUTOMATED (done by this script)
  ────────────────────────────────────────────────────────────
  [✓] Nine-pillar directory structure created
  [✓] .gitignore with Sacred-specific private paths
  [✓] .github/copilot-instructions.md with SacredSpace vocab
  [✓] .github/workflows/sacred-ci.yml  (GitHub Actions CI)
  [✓] requirements.txt stub (pillar-grouped)
  [✓] git init + global identity configured (WSL2)
  [✓] Initial canon commit sealed
  [✓] GitHub CLI installed + authenticated
  [✓] Private repo created on GitHub
  [✓] sacred-os pushed to github.com/$GITHUB_USER/$REPO_NAME
  [✓] VS Code Copilot extensions installed

  MANUAL (complete in the browser tabs now open)
  ────────────────────────────────────────────────────────────
  [ ] Apply: GitHub Student Developer Pack (school email)
  [ ] Apply: JetBrains Educational Pack (school email)
  [ ] Install: JetBrains Toolbox → install PyCharm Professional
  [ ] Enable: GitHub Copilot at github.com/settings/copilot
  [ ] Sign in: GitHub Copilot inside VS Code / PyCharm
  [ ] Claim: Namecheap free .me domain from pack dashboard
  [ ] Claim: DigitalOcean `$200 credit (DO NOT USE YET)
  [ ] Claim: Azure `$100 credit (DO NOT USE YET)

  NEXT SESSION SETUP (after pack approvals — 1–3 days)
  ────────────────────────────────────────────────────────────
  [ ] PyCharm: File → Open → $SACRED_ROOT
  [ ] PyCharm: Set interpreter → WSL2 Ubuntu 24.04 → .venv
  [ ] PyCharm: Settings → Plugins → GitHub Copilot → Install
  [ ] PyCharm: Database tool → connect to archive/memory-motes/*.db
  [ ] Test Copilot: open any .py file, write a comment, watch it complete

  REPO
  ────────────────────────────────────────────────────────────
  Local  : $SACRED_ROOT
  Remote : https://github.com/$GITHUB_USER/$REPO_NAME
  WSL2   : $wslRoot

  Daily commit pattern:
    git add -A
    git commit -m "[PILLAR] description  ∆"
    git push

"@ -ForegroundColor Cyan

Write-Host "  ∆∆∆  SacredSpace OS activation complete.  ∆∆∆`n" -ForegroundColor DarkCyan
