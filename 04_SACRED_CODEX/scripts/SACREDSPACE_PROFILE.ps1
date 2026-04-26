# ==============================================================================
# S∆CR3DSP∆C3 OS — PowerShell $PROFILE v2.0
# CANON ARCHITECTURE — Nine-Pillar Directory Structure
# Ground. Consolidate. Deploy. Document. Repeat. — In lakesh alakin.
# ==============================================================================
# To install: Copy contents into notepad $PROFILE
# To reload:  . $PROFILE
# ==============================================================================

# --- 1. ENCODING & STABILITY (Required for Hyperglyph rendering) ---
chcp 65001 > $null
[Console]::InputEncoding  = [System.Text.UTF8Encoding]::new()
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$OutputEncoding = [System.Text.UTF8Encoding]::new()

# --- 2. ROOT PATH — Single Source of Truth ---
$SACRED_ROOT  = "D:\SacredSpace_OS"
$VAULT_PATH   = "$SACRED_ROOT\01_OBSIDIAN_VAULTS\SacredSpace_Vault"
$GRAPH_PATH   = "$SACRED_ROOT\05_MEMORY_ENGINE\graph"
$CLI_PATH     = "$SACRED_ROOT\06_AGENT_LAYER\cli"
$STATE_FILE   = "$SACRED_ROOT\.sacred_state.json"

# --- 3. ANCHOR NAVIGATION ---
function sacred  { Set-Location $SACRED_ROOT }
function vault   { Set-Location $VAULT_PATH }
function forest  { Set-Location "$SACRED_ROOT\03_NEURAL_FOREST" }
function council { Set-Location "$SACRED_ROOT\02_COUNCIL_GROVE" }
function codex   { Set-Location "$SACRED_ROOT\04_SACRED_CODEX" }
function memory  { Set-Location "$SACRED_ROOT\05_MEMORY_ENGINE" }
function agents  { Set-Location "$SACRED_ROOT\06_AGENT_LAYER" }
function signal  { Set-Location "$SACRED_ROOT\07_SOCIAL_MOTHERSHIP" }
function learning{ Set-Location "$SACRED_ROOT\08_LEARNING_PATH" }
function market  { Set-Location "$SACRED_ROOT\09_SACRED_MARKET" }

# --- 4. NINE-PILLAR TELEPORTS (Numbered shortcuts) ---
function p1 { Set-Location "$SACRED_ROOT\01_OBSIDIAN_VAULTS" }    # CORE / Knowledge
function p2 { Set-Location "$SACRED_ROOT\02_COUNCIL_GROVE" }      # COUNCIL / Governance
function p3 { Set-Location "$SACRED_ROOT\03_NEURAL_FOREST" }      # FOREST / LLM Pipeline
function p4 { Set-Location "$SACRED_ROOT\04_SACRED_CODEX" }       # CODEX / Canon Ledger
function p5 { Set-Location "$SACRED_ROOT\05_MEMORY_ENGINE" }      # MEMORY / HME
function p6 { Set-Location "$SACRED_ROOT\06_AGENT_LAYER" }        # AGENTS / ICARIS Quartet
function p7 { Set-Location "$SACRED_ROOT\07_SOCIAL_MOTHERSHIP" }  # SIGNAL / Brand
function p8 { Set-Location "$SACRED_ROOT\08_LEARNING_PATH" }      # LEARNING / Maestro AAS
function p9 { Set-Location "$SACRED_ROOT\09_SACRED_MARKET" }      # MARKET / Revenue

# --- 5. HYPERGLYPH COMMAND LAYER ---
# Usage: glyph ∆  |  glyph ◇  |  glyph ⚙
function glyph {
    param([string]$g)
    switch ($g) {
        "∆"  { Write-Host "∆ — Consciousness / AI. Pillar: AGENTS" -ForegroundColor Cyan
               Set-Location "$SACRED_ROOT\06_AGENT_LAYER" }
        "◇"  { Write-Host "◇ — Knowledge Vault. Opening Obsidian..." -ForegroundColor Yellow
               Start-Process "obsidian://open?vault=SacredSpace_Vault" }
        "✶"  { Write-Host "✶ — Ritual / Signal. Pillar: SOCIAL" -ForegroundColor Magenta
               Set-Location "$SACRED_ROOT\07_SOCIAL_MOTHERSHIP" }
        "⚙"  { Write-Host "⚙ — Engineering. Pillar: NEURAL FOREST" -ForegroundColor Green
               Set-Location "$SACRED_ROOT\03_NEURAL_FOREST" }
        "∞"  { Write-Host "∞ — Memory / Lineage. Pillar: MEMORY ENGINE" -ForegroundColor DarkCyan
               Set-Location "$SACRED_ROOT\05_MEMORY_ENGINE" }
        "⬡"  { Write-Host "⬡ — Network / Council. Pillar: COUNCIL GROVE" -ForegroundColor Blue
               Set-Location "$SACRED_ROOT\02_COUNCIL_GROVE" }
        "◉"  { Write-Host "◉ — Core / Presence. Pillar: OBSIDIAN VAULTS" -ForegroundColor White
               Set-Location "$SACRED_ROOT\01_OBSIDIAN_VAULTS" }
        "⟁"  { Write-Host "⟁ — Learning Path. Pillar: LEARNING" -ForegroundColor DarkYellow
               Set-Location "$SACRED_ROOT\08_LEARNING_PATH" }
        "√"  { Write-Host "√ — Root / Market. Pillar: SACRED MARKET" -ForegroundColor Gray
               Set-Location "$SACRED_ROOT\09_SACRED_MARKET" }
        default { Write-Host "Unknown glyph: $g  |  Use: ∆ ◇ ✶ ⚙ ∞ ⬡ ◉ ⟁ √" -ForegroundColor Red }
    }
}

# --- 6. S∆CR3DS!G∆L KEYBOARD CODEX (Sigilify shortcuts) ---
# Add these to Gboard Personal Dictionary or any text-expander for system-wide use.
# Usage here: type 'sigil <shortcode>' to see expansion
$SIGIL_CODEX = @{
    "ss"    = "S∆CR3DSP∆C3"
    "sso"   = "S∆CR3DSP∆C3 0S"
    "sig"   = "S!G∆L"
    "src"   = "S0URC3"
    "frst"  = "F0R3ST"
    "cncl"  = "C0UNC!L"
    "arc"   = "∆RC∆N∆"
    "rite"  = "R!T3"
    "gate"  = "G∆T3"
    "lore"  = "L0R3"
    "mote"  = "M3M0RY M0T3"
    "spine" = "SP!N3"
    "vault" = "V∆ULT"
    "boot"  = "B00TSTR∆P"
    "scr"   = "SCR!P7"
    "mod"   = "M0DUL3"
    "fn"    = "FUNCT!0N"
    "sch"   = "SCH3M∆"
    "open"  = "0P3N TH3 G∆T3"
    "seal"  = "S3∆L TH3 SP∆C3"
    "init"  = "!N!T!∆T3 TH3 R!T3"
    "call"  = "C∆LL TH3 C0UNC!L"
    "root"  = "R00T !N S0URC3"
    "sync"  = "SYNC TH3 C0D3X"
    "aina"  = "∆LL !N ∆LL • ∆Y3 N ∆Y3"
    "ilal"  = "!N L∆K3SH ∆L∆K!N"
}

function sigil {
    param([string]$code)
    if ($code -eq "") {
        Write-Host "`nS!G!L C0D3X — All Shortcuts:" -ForegroundColor Cyan
        $SIGIL_CODEX.GetEnumerator() | Sort-Object Key | ForEach-Object {
            Write-Host ("  {0,-8} → {1}" -f $_.Key, $_.Value) -ForegroundColor Yellow
        }
        return
    }
    if ($SIGIL_CODEX.ContainsKey($code)) {
        $expansion = $SIGIL_CODEX[$code]
        Write-Host "$code → $expansion" -ForegroundColor Amber
        Set-Clipboard -Value $expansion
        Write-Host "(Copied to clipboard)" -ForegroundColor Gray
    } else {
        Write-Host "Unknown sigil code: $code" -ForegroundColor Red
    }
}

# --- 7. STATE TRACKING ---
function Save-SacredState {
    param([string]$note = "")
    $state = @{
        last_location = (Get-Location).Path
        last_used     = (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
        note          = $note
    } | ConvertTo-Json
    [System.IO.File]::WriteAllText($STATE_FILE, $state)
}

function Show-SacredState {
    if (Test-Path $STATE_FILE) {
        $s = Get-Content $STATE_FILE | ConvertFrom-Json
        Write-Host "`nLast Location : $($s.last_location)" -ForegroundColor Cyan
        Write-Host "Last Used     : $($s.last_used)" -ForegroundColor Gray
        if ($s.note) { Write-Host "Note          : $($s.note)" -ForegroundColor Yellow }
    } else {
        Write-Host "No state file found. Run ignite to initialize." -ForegroundColor Yellow
    }
}

# --- 8. GIT OPERATIONS ---
function sacredstatus { git -C $SACRED_ROOT status }

function sacredpush {
    param([string]$msg = "")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    $commitMsg = if ($msg) { "∆ $msg — $timestamp" } else { "∆ SacredSpace Update — $timestamp" }
    git -C $SACRED_ROOT add .
    git -C $SACRED_ROOT commit -m $commitMsg
    git -C $SACRED_ROOT push
    Save-SacredState -note "Post-push"
    Write-Host "✓ Committed + pushed: $commitMsg" -ForegroundColor Green
}

function sacreddiff { git -C $SACRED_ROOT diff }
function sacredlog  { git -C $SACRED_ROOT log --oneline -20 }

# --- 9. SERVICE CHECKS ---
function sacred-services {
    Write-Host "`n── SERVICE STATUS ──────────────────────────────" -ForegroundColor Cyan

    # FastAPI :8888
    $api = Test-NetConnection -ComputerName localhost -Port 8888 -WarningAction SilentlyContinue
    if ($api.TcpTestSucceeded) {
        Write-Host "  [✓] FastAPI :8888        ACTIVE" -ForegroundColor Green
    } else {
        Write-Host "  [!] FastAPI :8888        OFFLINE" -ForegroundColor Yellow
    }

    # Ollama
    if (Get-Process "ollama" -ErrorAction SilentlyContinue) {
        Write-Host "  [✓] Ollama               ACTIVE" -ForegroundColor Green
    } else {
        Write-Host "  [!] Ollama               OFFLINE" -ForegroundColor Yellow
    }

    # WSL2
    $wsl = wsl --list --running 2>$null
    if ($wsl) {
        Write-Host "  [✓] WSL2                 ACTIVE" -ForegroundColor Green
    } else {
        Write-Host "  [!] WSL2                 OFFLINE" -ForegroundColor Yellow
    }

    # Python venv
    if ($env:VIRTUAL_ENV) {
        Write-Host "  [✓] Python Venv          ACTIVE ($env:VIRTUAL_ENV)" -ForegroundColor Green
    } else {
        Write-Host "  [!] Python Venv          NOT ACTIVATED" -ForegroundColor Yellow
    }

    Write-Host "────────────────────────────────────────────────`n" -ForegroundColor Cyan
}

# --- 10. IGNITION SEQUENCE ---
function Start-SacredSpace {
    Write-Host "`n══════════════════════════════════════════" -ForegroundColor DarkGreen
    Write-Host "  S∆CR3DSP∆C3 OS — Initialization Rite" -ForegroundColor Cyan
    Write-Host "══════════════════════════════════════════`n" -ForegroundColor DarkGreen

    # Verify root
    if (-not (Test-Path $SACRED_ROOT)) {
        Write-Error "Sacred root not found: $SACRED_ROOT  |  Check D: drive."
        return
    }
    Set-Location $SACRED_ROOT
    Write-Host "  [✓] Anchored at $SACRED_ROOT" -ForegroundColor Green

    # Python venv
    $venv = "$SACRED_ROOT\.venv\Scripts\Activate.ps1"
    if (Test-Path $venv) {
        & $venv
        Write-Host "  [✓] Council Grove Agents Active (Python Venv)" -ForegroundColor Green
    } else {
        Write-Host "  [!] .venv not found — run: python -m venv .venv" -ForegroundColor Yellow
    }

    # Obsidian
    try {
        Start-Process "obsidian://open?vault=SacredSpace_Vault"
        Write-Host "  [✓] Obsidian Vault Synchronized" -ForegroundColor DarkCyan
    } catch {
        Write-Host "  [!] Obsidian launch failed" -ForegroundColor Yellow
    }

    # Ollama
    if (Get-Process "ollama" -ErrorAction SilentlyContinue) {
        Write-Host "  [✓] Ollama (Local AI) Online" -ForegroundColor Magenta
    } else {
        Write-Host "  [!] Ollama Offline — run: ollama serve" -ForegroundColor Yellow
    }

    # Save boot state
    Save-SacredState -note "Boot"

    Write-Host "`n  Ground. Consolidate. Deploy. Document. Repeat." -ForegroundColor DarkYellow
    Write-Host "  In lakesh alakin.`n" -ForegroundColor Gray
    Write-Host "══════════════════════════════════════════`n" -ForegroundColor DarkGreen
}

# --- 11. UTILITY FUNCTIONS ---

# Build the memory graph (requires graph_builder.py)
function buildgraph {
    $script = "$SACRED_ROOT\05_MEMORY_ENGINE\graph\graph_builder.py"
    if (Test-Path $script) {
        python $script
    } else {
        Write-Host "graph_builder.py not found at: $script" -ForegroundColor Red
    }
}

# Query the graph (requires graph_query.py)
function querygraph {
    param([string]$node)
    $script = "$SACRED_ROOT\05_MEMORY_ENGINE\graph\graph_query.py"
    if (Test-Path $script) {
        python $script $node
    } else {
        Write-Host "graph_query.py not found at: $script" -ForegroundColor Red
    }
}

# Launch the SacredSpace CLI
function sacredcli {
    $script = "$SACRED_ROOT\06_AGENT_LAYER\cli\sacred_cli.py"
    if (Test-Path $script) {
        python $script
    } else {
        Write-Host "sacred_cli.py not found at: $script" -ForegroundColor Red
    }
}

# Start FastAPI spine
function start-api {
    $app = "$SACRED_ROOT\02_COUNCIL_GROVE\main.py"
    if (Test-Path $app) {
        Start-Process wt -ArgumentList "python -m uvicorn main:app --reload --port 8888"
    } else {
        Write-Host "main.py not found. Check 02_COUNCIL_GROVE." -ForegroundColor Yellow
    }
}

# --- 12. ALIASES ---
Set-Alias ignite   Start-SacredSpace
Set-Alias services sacred-services
Set-Alias sstate   Show-SacredState
Set-Alias g        glyph
Set-Alias ss       sacred
Set-Alias sv       vault
Set-Alias sb       buildgraph
Set-Alias sq       querygraph
Set-Alias sc       sacredcli

Write-Host "  S∆CR3DSP∆C3 OS Profile Loaded — type 'ignite' to begin." -ForegroundColor DarkGreen
