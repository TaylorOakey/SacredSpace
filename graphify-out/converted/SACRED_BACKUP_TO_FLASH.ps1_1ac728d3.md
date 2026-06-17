<!-- converted from SACRED_BACKUP_TO_FLASH.ps1.docx -->

# ============================================================
# SACRED_BACKUP_TO_FLASH.ps1
# SacredSpace OS — Flash Drive Archive Protocol
# Target: E:\ (Flash Drive)
# Owner Agent: AURORA (code) + ASHER (integrity)
# ============================================================

$TIMESTAMP     = Get-Date -Format "yyyy-MM-dd_HH-mm"
$FLASH_ROOT    = "E:\06_BACKUPS"
$LOG_DIR       = "$FLASH_ROOT\_LOGS"
$LOG_FILE      = "$LOG_DIR\backup_$TIMESTAMP.log"

$SOURCES = @(
@{ Label = "SacredSpace_OS";     Src = "D:\SacredSpace_OS" },
@{ Label = "Obsidian_Vault";     Src = "D:\01_VAULT\SacredSpace_Vault" },
@{ Label = "Obsidian_AltVault";  Src = "D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault" },
@{ Label = "06_BACKUPS";         Src = "D:\06_BACKUPS" }
)

# ─── Sigil Banner ────────────────────────────────────────────
function Write-Banner {
Write-Host ""
Write-Host "  ∆∆∆ SACREDSPACE FLASH ARCHIVE PROTOCOL ∆∆∆" -ForegroundColor Cyan
Write-Host "  Target Drive  : E:\" -ForegroundColor Yellow
Write-Host "  Backup Root   : $FLASH_ROOT" -ForegroundColor Yellow
Write-Host "  Timestamp     : $TIMESTAMP" -ForegroundColor Yellow
Write-Host "  In Lakesh — Alakin." -ForegroundColor DarkCyan
Write-Host ""
}

# ─── Logger ──────────────────────────────────────────────────
function Write-Log {
param([string]$Message, [string]$Level = "INFO")
$entry = "[$TIMESTAMP][$Level] $Message"
Write-Host $entry
Add-Content -Path $LOG_FILE -Value $entry
}

# ─── Verify Flash Drive ───────────────────────────────────────
function Test-FlashDrive {
if (-not (Test-Path "E:\")) {
Write-Host ""
Write-Host "  [ERROR] Flash drive not detected at E:\" -ForegroundColor Red
Write-Host "  Insert flash drive and re-run this script." -ForegroundColor Red
Write-Host ""
exit 1
}

$drive = Get-PSDrive -Name E -ErrorAction SilentlyContinue
if ($drive) {
$freeGB = [math]::Round($drive.Free / 1GB, 2)
Write-Log "Flash drive detected at E:\ — Free space: ${freeGB} GB"
if ($freeGB -lt 1) {
Write-Host "  [WARNING] Less than 1 GB free on E:\ — backup may be incomplete." -ForegroundColor Yellow
}
}
}

# ─── Create Output Structure ──────────────────────────────────
function Initialize-BackupRoot {
$dirs = @(
$FLASH_ROOT,
$LOG_DIR,
"$FLASH_ROOT\SacredSpace_OS",
"$FLASH_ROOT\Obsidian_Vault",
"$FLASH_ROOT\06_BACKUPS",
"$FLASH_ROOT\CANON_EXPORTS"
)
foreach ($d in $dirs) {
if (-not (Test-Path $d)) {
New-Item -ItemType Directory -Path $d -Force | Out-Null
Write-Log "Created directory: $d"
}
}
}

# ─── Robocopy Mirror ──────────────────────────────────────────
function Invoke-SacredCopy {
param([string]$Label, [string]$Src, [string]$Dst)

if (-not (Test-Path $Src)) {
Write-Log "SKIPPED [$Label] — Source not found: $Src" "WARN"
return
}

Write-Host ""
Write-Host "  ∆ Copying [$Label]..." -ForegroundColor Cyan
Write-Host "    From : $Src" -ForegroundColor DarkGray
Write-Host "    To   : $Dst" -ForegroundColor DarkGray

# Robocopy flags:
#   /MIR  = mirror (adds + removes to match source)
#   /R:2  = 2 retries on fail
#   /W:3  = 3 sec wait between retries
#   /NP   = no progress % (cleaner output)
#   /LOG+ = append to log
#   /XD   = exclude directories (.git, .venv, __pycache__, node_modules)
#   /XF   = exclude files (*.pyc, *.log)

robocopy $Src $Dst /MIR /R:2 /W:3 /NP /TEE `
/LOG+:"$LOG_FILE" `
/XD ".git" ".venv" "__pycache__" "node_modules" ".obsidian\plugins" `
/XF "*.pyc" "*.log" "Thumbs.db" "desktop.ini"

$exit = $LASTEXITCODE
if ($exit -le 7) {
Write-Log "[$Label] Copy complete (robocopy exit: $exit)" "OK"
} else {
Write-Log "[$Label] Copy may have errors (robocopy exit: $exit)" "WARN"
}
}

# ─── Write Manifest ───────────────────────────────────────────
function Write-Manifest {
$manifest = "$FLASH_ROOT\BACKUP_MANIFEST_$TIMESTAMP.txt"
$lines = @(
"============================================",
"  SacredSpace Flash Drive Backup Manifest",
"  Generated : $TIMESTAMP",
"  Operator  : Taylor (∆∆∆O∆K3YTREE∆∆∆)",
"  Seal      : In Lakesh — Alakin",
"============================================",
"",
"SOURCE PATHS ATTEMPTED:"
)
foreach ($s in $SOURCES) {
$exists = if (Test-Path $s.Src) { "FOUND" } else { "NOT FOUND" }
$lines += "  [$($s.Label)] $($s.Src) — $exists"
}
$lines += ""
$lines += "BACKUP ROOT : $FLASH_ROOT"
$lines += "LOG FILE    : $LOG_FILE"
$lines += ""
$lines += "NINE PILLARS BACKED UP (from SacredSpace_OS):"
$pillars = @(
"01_OBSIDIAN_VAULTS", "02_COUNCIL_GROVE", "03_NEURAL_FOREST",
"04_SACRED_CODEX",   "05_MEMORY_ENGINE", "06_AGENT_LAYER",
"07_SOCIAL_MOTHERSHIP", "08_LEARNING_PATH", "09_SACRED_MARKET"
)
foreach ($p in $pillars) {
$path = "D:\SacredSpace_OS\$p"
$status = if (Test-Path $path) { "✓" } else { "—" }
$lines += "  $status $p"
}
$lines += ""
$lines += "CIPHER: S∆CR3DS!G∆L"
$lines += "SIGIL GRAMMAR: ∆∆∆"

[System.IO.File]::WriteAllText($manifest, ($lines -join "`r`n"))
Write-Log "Manifest written: $manifest"
}

# ─── Summary ──────────────────────────────────────────────────
function Write-Summary {
$size = (Get-ChildItem -Path $FLASH_ROOT -Recurse -ErrorAction SilentlyContinue |
Measure-Object -Property Length -Sum).Sum
$sizeGB = [math]::Round($size / 1GB, 3)

Write-Host ""
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
Write-Host "  ∆ BACKUP COMPLETE" -ForegroundColor Green
Write-Host "  Total archived : ~${sizeGB} GB on E:\" -ForegroundColor White
Write-Host "  Log saved at   : $LOG_FILE" -ForegroundColor DarkGray
Write-Host "  In Lakesh — Alakin. ∆∆∆" -ForegroundColor DarkCyan
Write-Host "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkCyan
Write-Host ""
}

# ═══════════════════════════════════════════════════════
#  MAIN EXECUTION
# ═══════════════════════════════════════════════════════

Write-Banner
Test-FlashDrive
Initialize-BackupRoot

# Copy each source to its labeled folder on E:\
Invoke-SacredCopy -Label "SacredSpace_OS"    -Src "D:\SacredSpace_OS"                                      -Dst "$FLASH_ROOT\SacredSpace_OS"
Invoke-SacredCopy -Label "Obsidian_Vault_D1" -Src "D:\01_VAULT\SacredSpace_Vault"                          -Dst "$FLASH_ROOT\Obsidian_Vault"
Invoke-SacredCopy -Label "Obsidian_Vault_D2" -Src "D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault" -Dst "$FLASH_ROOT\Obsidian_Vault"
Invoke-SacredCopy -Label "06_BACKUPS"        -Src "D:\06_BACKUPS"                                          -Dst "$FLASH_ROOT\06_BACKUPS"

Write-Manifest
Write-Summary
