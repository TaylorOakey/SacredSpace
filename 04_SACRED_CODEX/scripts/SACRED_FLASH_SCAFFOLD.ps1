# ============================================================
# SACRED_FLASH_SCAFFOLD.ps1
# SacredSpace OS — Flash Drive Directory Scaffold
# Owner Agent: AURORA (code) + ASHER (integrity)
# Version: 2.0.0  |  2026-05-21 — Communal Portal + Arcana Landscapes
#
# USAGE:
#   .\SACRED_FLASH_SCAFFOLD.ps1              # defaults to E:\
#   .\SACRED_FLASH_SCAFFOLD.ps1 -Drive G
#
# PURPOSE: Creates the full nine-pillar directory tree on the
# flash drive and writes SACRED_ENV.env + README.md to 00_BOOT\.
# Safe to re-run — skips directories that already exist.
#
# In Lakesh Alakin. ∆∆∆
# ============================================================

param(
    [string]$Drive = "E"
)

$TIMESTAMP  = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$FLASH_ROOT = "${Drive}:\"
$LOG_DIR    = "${Drive}:\_LOGS"
$LOG_FILE   = "$LOG_DIR\scaffold_$TIMESTAMP.log"

# ── Sigil Banner ─────────────────────────────────────────────
function Write-Banner {
    Write-Host ""
    Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor DarkCyan
    Write-Host "  ∆  SACREDSPACE OS — FLASH SCAFFOLD    ∆" -ForegroundColor Cyan
    Write-Host "  ∆  Target Drive : ${Drive}:\           ∆" -ForegroundColor Yellow
    Write-Host "  ∆  Timestamp    : $TIMESTAMP     ∆" -ForegroundColor Yellow
    Write-Host "  ∆  In Lakesh — Alakin              ∆" -ForegroundColor DarkCyan
    Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor DarkCyan
    Write-Host ""
}

# ── Logger ───────────────────────────────────────────────────
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $entry = "[$TIMESTAMP][$Level] $Message"
    Write-Host $entry -ForegroundColor $(if ($Level -eq "WARN") { "Yellow" } elseif ($Level -eq "ERROR") { "Red" } else { "Gray" })
    Add-Content -Path $LOG_FILE -Value $entry -ErrorAction SilentlyContinue
}

# ── Drive Check ───────────────────────────────────────────────
function Assert-Drive {
    if (-not (Test-Path "${Drive}:\")) {
        Write-Host ""
        Write-Host "  [ERROR] Drive ${Drive}:\ not found." -ForegroundColor Red
        Write-Host "  Insert flash drive or specify: .\SACRED_FLASH_SCAFFOLD.ps1 -Drive G" -ForegroundColor Yellow
        Write-Host ""
        exit 1
    }
    $drv = Get-PSDrive -Name $Drive -ErrorAction SilentlyContinue
    if ($drv) {
        $freeGB = [math]::Round($drv.Free / 1GB, 2)
        Write-Log "Drive ${Drive}:\ detected — Free: ${freeGB} GB"
        if ($freeGB -lt 2) {
            Write-Log "WARNING: Less than 2 GB free. Populate script may fail." "WARN"
        }
    }
}

# ── Make Dir (idempotent) ─────────────────────────────────────
function New-SacredDir {
    param([string]$Path, [string]$Label)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Log "Created : $Label"
    } else {
        Write-Log "Exists  : $Label"
    }
}

# ── Scaffold Directories ──────────────────────────────────────
function Build-Tree {
    $dirs = @(
        @{ Path = "${Drive}:\00_BOOT";                          Label = "00_BOOT — Boot scripts & env" },
        @{ Path = "${Drive}:\01_VAULT\SacredSpace_Vault";       Label = "01_VAULT — Obsidian vault root" },
        @{ Path = "${Drive}:\01_VAULT\SacredSpace_Vault\00_INBOX"; Label = "01_VAULT\00_INBOX" },
        @{ Path = "${Drive}:\01_VAULT\SacredSpace_Vault\00_CANON"; Label = "01_VAULT\00_CANON" },
        @{ Path = "${Drive}:\02_COUNCIL_GROVE";                 Label = "02_COUNCIL_GROVE — Agent routing" },
        @{ Path = "${Drive}:\02_COUNCIL_GROVE\handoff_capsules"; Label = "02_COUNCIL_GROVE\handoff_capsules" },
        @{ Path = "${Drive}:\03_NEURAL_FOREST";                 Label = "03_NEURAL_FOREST — LLM pipeline" },
        @{ Path = "${Drive}:\03_NEURAL_FOREST\logs";            Label = "03_NEURAL_FOREST\logs" },
        @{ Path = "${Drive}:\04_SACRED_CODEX";                  Label = "04_SACRED_CODEX — Scripts & spells" },
        @{ Path = "${Drive}:\04_SACRED_CODEX\scripts";          Label = "04_SACRED_CODEX\scripts" },
        @{ Path = "${Drive}:\05_MEMORY_ENGINE";                 Label = "05_MEMORY_ENGINE — Vector store" },
        @{ Path = "${Drive}:\05_MEMORY_ENGINE\chromadb_export"; Label = "05_MEMORY_ENGINE\chromadb_export" },
        @{ Path = "${Drive}:\06_AGENT_LAYER";                   Label = "06_AGENT_LAYER — Agent impls" },
        @{ Path = "${Drive}:\06_AGENT_LAYER\IRIS";              Label = "06_AGENT_LAYER\IRIS" },
        @{ Path = "${Drive}:\06_AGENT_LAYER\hermes";            Label = "06_AGENT_LAYER\hermes" },
        @{ Path = "${Drive}:\07_SOCIAL_MOTHERSHIP";             Label = "07_SOCIAL_MOTHERSHIP — Brand & social" },
        @{ Path = "${Drive}:\07_SOCIAL_MOTHERSHIP\brand_assets"; Label = "07_SOCIAL_MOTHERSHIP\brand_assets" },
        @{ Path = "${Drive}:\08_LEARNING_PATH";                 Label = "08_LEARNING_PATH — Maestro coursework" },
        @{ Path = "${Drive}:\08_LEARNING_PATH\python_codex";    Label = "08_LEARNING_PATH\python_codex" },
        @{ Path = "${Drive}:\09_SACRED_MARKET";                 Label = "09_SACRED_MARKET — Marketplace" },
        @{ Path = "${Drive}:\MODELS";                           Label = "MODELS — Ollama model blobs" },
        @{ Path = "${Drive}:\MODELS\manifests";                 Label = "MODELS\manifests" },
        @{ Path = "${Drive}:\MEDIA";                            Label = "MEDIA — AI image portfolio" },
        @{ Path = "${Drive}:\OBSIDIAN_PORTABLE";                Label = "OBSIDIAN_PORTABLE — Portable Obsidian" },
        @{ Path = "${Drive}:\CHROME_EXTENSION\sacred-chrome";   Label = "CHROME_EXTENSION\sacred-chrome" },
        @{ Path = "${Drive}:\CHROME_EXTENSION\sacred-chrome\icons";   Label = "CHROME_EXTENSION\sacred-chrome\icons" },
        @{ Path = "${Drive}:\CHROME_EXTENSION\sacred-chrome\styles";  Label = "CHROME_EXTENSION\sacred-chrome\styles" },
        @{ Path = "${Drive}:\_LOGS";                            Label = "_LOGS — Timestamped run logs" },
        @{ Path = "${Drive}:\00_HANDOFF";                       Label = "00_HANDOFF — Handoff capsules" },
        @{ Path = "${Drive}:\05_MEMORY_ENGINE\memory_motes";   Label = "05_MEMORY_ENGINE\memory_motes" },
        @{ Path = "${Drive}:\05_MEMORY_ENGINE\redis_streams";  Label = "05_MEMORY_ENGINE\redis_streams" },
        @{ Path = "${Drive}:\06_AGENT_LAYER\ELIAS";            Label = "06_AGENT_LAYER\ELIAS" },
        @{ Path = "${Drive}:\06_AGENT_LAYER\AURORA";           Label = "06_AGENT_LAYER\AURORA" },
        @{ Path = "${Drive}:\06_AGENT_LAYER\ASHER";            Label = "06_AGENT_LAYER\ASHER" },
        @{ Path = "${Drive}:\07_SOCIAL_MOTHERSHIP\brand_assets"; Label = "07_SOCIAL_MOTHERSHIP\brand_assets" },
        @{ Path = "${Drive}:\07_SOCIAL_MOTHERSHIP\content";    Label = "07_SOCIAL_MOTHERSHIP\content" },
        @{ Path = "${Drive}:\07_SOCIAL_MOTHERSHIP\GRAMA";      Label = "07_SOCIAL_MOTHERSHIP\GRAMA" },
        @{ Path = "${Drive}:\08_LEARNING_PATH\MAESTRO_AAS";    Label = "08_LEARNING_PATH\MAESTRO_AAS" },
        @{ Path = "${Drive}:\08_LEARNING_PATH\PYTHON_CODEX";   Label = "08_LEARNING_PATH\PYTHON_CODEX" },
        @{ Path = "${Drive}:\08_LEARNING_PATH\SACRED_FORGE";   Label = "08_LEARNING_PATH\SACRED_FORGE" },
        @{ Path = "${Drive}:\09_SACRED_MARKET\ETSY";           Label = "09_SACRED_MARKET\ETSY" },
        @{ Path = "${Drive}:\09_SACRED_MARKET\PRINTIFY";       Label = "09_SACRED_MARKET\PRINTIFY" },
        @{ Path = "${Drive}:\09_SACRED_MARKET\GELATO";         Label = "09_SACRED_MARKET\GELATO" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES";               Label = "ARCANA_LANDSCAPES — Art assets" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\SIGILS";        Label = "ARCANA_LANDSCAPES\SIGILS" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\CHARACTERS";    Label = "ARCANA_LANDSCAPES\CHARACTERS" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\ENVIRONMENTS";  Label = "ARCANA_LANDSCAPES\ENVIRONMENTS" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\ARCANA_GRID";   Label = "ARCANA_LANDSCAPES\ARCANA_GRID" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\BRAND";         Label = "ARCANA_LANDSCAPES\BRAND" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\GRAMA";         Label = "ARCANA_LANDSCAPES\GRAMA" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\PORTAL_WALLPAPERS"; Label = "ARCANA_LANDSCAPES\PORTAL_WALLPAPERS" },
        @{ Path = "${Drive}:\ARCANA_LANDSCAPES\UNSORTED";      Label = "ARCANA_LANDSCAPES\UNSORTED" },
        @{ Path = "${Drive}:\PORTAL";                          Label = "PORTAL — Communal Portal" },
        @{ Path = "${Drive}:\SHARED_SPACE";                    Label = "SHARED_SPACE — Taylor x Jeanie" },
        @{ Path = "${Drive}:\SHARED_SPACE\ACTIVE";             Label = "SHARED_SPACE\ACTIVE" },
        @{ Path = "${Drive}:\SHARED_SPACE\CANON";              Label = "SHARED_SPACE\CANON" },
        @{ Path = "${Drive}:\SHARED_SPACE\LETTERS";            Label = "SHARED_SPACE\LETTERS" }
    )

    Write-Host "  Building directory tree..." -ForegroundColor Cyan
    foreach ($d in $dirs) {
        New-SacredDir -Path $d.Path -Label $d.Label
    }
    Write-Log "Tree scaffold complete — $($dirs.Count) directories processed"
}

# ── Write SACRED_ENV.env ──────────────────────────────────────
function Write-Env {
    $envPath = "${Drive}:\00_BOOT\SACRED_ENV.env"
    if (Test-Path $envPath) {
        Write-Log "SACRED_ENV.env already exists — skipping (edit manually)" "WARN"
        return
    }

    $lines = @(
        "# ============================================================",
        "# SACRED_ENV.env — SacredSpace OS Environment Configuration",
        "# Flash Drive: ${Drive}:\",
        "# Generated:   $TIMESTAMP",
        "# Edit these values for each machine you deploy on.",
        "# In Lakesh Alakin. ∆∆∆",
        "# ============================================================",
        "",
        "# ── Drive & Paths ────────────────────────────────────────────",
        "SACRED_DRIVE=${Drive}",
        "SACRED_ROOT=${Drive}:\",
        "SACRED_VAULT=${Drive}:\01_VAULT\SacredSpace_Vault",
        "SACRED_MODELS=${Drive}:\MODELS",
        "SACRED_LOG_DIR=${Drive}:\_LOGS",
        "",
        "# ── FastAPI Spine ─────────────────────────────────────────────",
        "SACREDSPACE_API=http://localhost:8888",
        "SACREDSPACE_API_PORT=8888",
        "SACREDSPACE_API_HOST=127.0.0.1",
        "",
        "# ── Ollama ────────────────────────────────────────────────────",
        "# Auto-detected at boot from /etc/resolv.conf in WSL2.",
        "# Override here if needed (e.g., for a machine without WSL2).",
        "SACREDSPACE_OLLAMA_URL=http://192.168.240.1:11434",
        "SACREDSPACE_OLLAMA_MODEL=llama3.2",
        "OLLAMA_MODELS=${Drive}:\MODELS",
        "",
        "# ── Agents ────────────────────────────────────────────────────",
        "SACREDSPACE_AGENT_IRIS=true",
        "SACREDSPACE_AGENT_HERMES=true",
        "",
        "# ── Optional API Keys (leave blank for zero-cloud operation) ──",
        "GEMINI_API_KEY=",
        "ANTHROPIC_API_KEY=",
        "",
        "# ── WSL2 ──────────────────────────────────────────────────────",
        "WSL_MTU=1400",
        "WSL_DISTRO=Ubuntu-24.04",
        ""
    )

    [System.IO.File]::WriteAllText($envPath, ($lines -join "`r`n"))
    Write-Log "Written: SACRED_ENV.env"
}

# ── Write README.md ───────────────────────────────────────────
function Write-Readme {
    $readmePath = "${Drive}:\00_BOOT\README.md"
    if (Test-Path $readmePath) {
        Write-Log "README.md already exists — skipping" "WARN"
        return
    }

    $lines = @(
        "# SacredSpace OS — Flash Drive",
        "",
        "> *In Lakesh Alakin. ∆∆∆*",
        "",
        "## Quick Boot",
        "",
        '```powershell',
        "${Drive}:\00_BOOT\SACRED_LAUNCH.ps1",
        '```',
        "",
        "## Directory Map",
        "",
        "| Folder | Purpose |",
        "|--------|---------|",
        "| `00_BOOT\` | Boot scripts, env config |",
        "| `01_VAULT\` | Obsidian knowledge vault (176+ notes) |",
        "| `02_COUNCIL_GROVE\` | Agent routing & handoff capsules |",
        "| `03_NEURAL_FOREST\` | LLM inference pipeline |",
        "| `04_SACRED_CODEX\` | Scripts, spells, automation |",
        "| `05_MEMORY_ENGINE\` | SQLite + ChromaDB vector store |",
        "| `06_AGENT_LAYER\` | IRIS, Hermes, ELIAS, AURORA agents |",
        "| `07_SOCIAL_MOTHERSHIP\` | Brand assets, content calendar |",
        "| `08_LEARNING_PATH\` | Maestro coursework, Python Codex |",
        "| `09_SACRED_MARKET\` | Sacred market product files |",
        "| `MODELS\` | Ollama model blobs |",
        "| `MEDIA\` | AI image portfolio |",
        "| `OBSIDIAN_PORTABLE\` | Portable Obsidian.exe |",
        "| `CHROME_EXTENSION\` | sacred-chrome unpacked extension |",
        "| `_LOGS\` | Timestamped session logs |",
        "",
        "## Loading the Chrome Extension",
        "",
        "1. Open `CHROME_EXTENSION\LOAD_EXTENSION.bat`",
        "2. Follow on-screen steps (takes ~10 seconds)",
        "",
        "## Requirements (foreign machine)",
        "",
        "- Windows 10/11 with WSL2 installed",
        "- Google Chrome",
        "- Python 3.10+ (in WSL2)",
        "- Ollama running on Windows host",
        "",
        "## Cipher",
        "",
        "S∆CR3DS!G∆L — HERMES = 68 — GR∆M∆ = 40 — 108 = 9 Pillars",
        ""
    )

    [System.IO.File]::WriteAllText($readmePath, ($lines -join "`r`n"))
    Write-Log "Written: README.md"
}

# ── Model Manifest ────────────────────────────────────────────
function Write-ModelManifest {
    $manifestPath = "${Drive}:\MODELS\manifests\models.json"
    if (Test-Path $manifestPath) { return }

    $manifest = @{
        version     = "1.0"
        generated   = $TIMESTAMP
        recommended = "llama3.2"
        models      = @(
            @{ name = "llama3.2"; size_gb = 2.0; source = "ollama pull llama3.2" },
            @{ name = "deepseek-r1:1.5b"; size_gb = 1.1; source = "ollama pull deepseek-r1:1.5b" },
            @{ name = "mistral:7b"; size_gb = 4.1; source = "ollama pull mistral:7b" }
        )
        pull_command = "# On target machine with Ollama: ollama pull <name>"
        note = "Copy MODELS\ folder from source machine OLLAMA_MODELS dir, or pull fresh on target."
    } | ConvertTo-Json -Depth 4

    [System.IO.File]::WriteAllText($manifestPath, $manifest)
    Write-Log "Written: MODELS\manifests\models.json"
}

# ── Summary ───────────────────────────────────────────────────
function Write-Summary {
    Write-Host ""
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
    Write-Host "  ∆ SCAFFOLD COMPLETE" -ForegroundColor Green
    Write-Host "  Drive    : ${Drive}:\" -ForegroundColor White
    Write-Host "  Log      : $LOG_FILE" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "  NEXT: Run SACRED_FLASH_POPULATE.ps1 to copy content." -ForegroundColor Yellow
    Write-Host "  In Lakesh — Alakin. ∆∆∆" -ForegroundColor DarkCyan
    Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
    Write-Host ""
}

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

Write-Banner
Assert-Drive
New-Item -ItemType Directory -Path $LOG_DIR -Force | Out-Null
Build-Tree
Write-Env
Write-Readme
Write-ModelManifest
Write-Summary
