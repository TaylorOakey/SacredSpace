#Requires -Version 5.1
<#
.SYNOPSIS
    S∆CR3D SP∆CE — Flash Drive Populate v2.0
    ∆∆∆ O∆K3YTREE ∆∆∆

.DESCRIPTION
    Copies files from D:\SacredSpace_OS\ to E:\ (Sacred Flash Drive).
    Copies portal, obsidian_links.json, vault nav note, brand assets
    to SHARED_SPACE, then calls SACRED_ARCANA_POPULATE.ps1.

.NOTES
    Source: D:\SacredSpace_OS\
    Dest:   E:\
    In Lakesh Alakin. ∆∆∆
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$SOURCE    = "D:\SacredSpace_OS"
$FLASH     = "E:"
$LOG_DIR   = "$FLASH\_LOGS"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_FILE  = "$LOG_DIR\populate_$TIMESTAMP.log"

function Write-Sacred { param($msg) Write-Host "`n∆ $msg" -ForegroundColor Cyan }
function Write-Done   { param($msg) Write-Host "  ✓ $msg" -ForegroundColor Green }
function Write-Warn   { param($msg) Write-Host "  ! $msg" -ForegroundColor Yellow }

function Log {
    param($level, $msg)
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [$level] $msg"
    Add-Content -Path $LOG_FILE -Value $line -Encoding UTF8
}

function CopyFile {
    param([string]$Src, [string]$Dest, [string]$Label = "")
    $disp = if ($Label) { $Label } else { (Split-Path $Dest -Leaf) }
    if (-not (Test-Path $Src -PathType Leaf)) {
        Write-Warn "Source not found — $Src"
        Log "WARN" "Source not found: $Src"
        return $false
    }
    $destDir = Split-Path $Dest -Parent
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    Copy-Item -Path $Src -Destination $Dest -Force
    Write-Done "COPY  $disp"
    Log "OK" "File: $Src -> $Dest"
    return $true
}

function CopyDir {
    param([string]$Src, [string]$Dest, [string]$Label = "")
    $disp = if ($Label) { $Label } else { "$Src -> $Dest" }
    if (-not (Test-Path $Src)) {
        Write-Warn "Source dir not found — $Src"
        Log "WARN" "Source dir not found: $Src"
        return 0
    }
    New-Item -ItemType Directory -Force -Path $Dest | Out-Null
    $files = Get-ChildItem -Path $Src -Recurse -File -ErrorAction SilentlyContinue
    $count = 0
    foreach ($f in $files) {
        $rel  = $f.FullName.Substring($Src.Length).TrimStart('\')
        $dest = Join-Path $Dest $rel
        $ddir = Split-Path $dest -Parent
        New-Item -ItemType Directory -Force -Path $ddir | Out-Null
        Copy-Item -Path $f.FullName -Destination $dest -Force
        $count++
    }
    Write-Done "COPY  $disp ($count files)"
    Log "OK" "Dir: $Src -> $Dest ($count files)"
    return $count
}

Write-Host ""
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor Magenta
Write-Host "  ∆  S∆CR3D FL∆SH DR1V3 — POPUL∆T3 v2.0           ∆" -ForegroundColor Magenta
Write-Host "  ∆  Communal Portal Build · Taylor x Jeanie       ∆" -ForegroundColor Magenta
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor Magenta
Write-Host ""

if (-not (Test-Path $FLASH)) {
    Write-Host "  [ERROR] Flash drive not found at $FLASH" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path $SOURCE)) {
    Write-Warn "Source root not found: $SOURCE — some copies will be skipped"
}

New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null
Log "INFO" "=== SACRED FLASH POPULATE v2.0 — $TIMESTAMP ==="
Log "INFO" "Source: $SOURCE | Flash: $FLASH"

$TOTAL_FILES = 0

Write-Sacred "Communal Portal"
$r = CopyFile "$SOURCE\PORTAL\index.html" "$FLASH\PORTAL\index.html" "index.html -> E:\PORTAL\"
if ($r) { $TOTAL_FILES++ }

Write-Sacred "Council Grove — Link Registry"
$r = CopyFile "$SOURCE\02_COUNCIL_GROVE\obsidian_links.json" "$FLASH\02_COUNCIL_GROVE\obsidian_links.json" "obsidian_links.json -> E:\02_COUNCIL_GROVE\"
if ($r) { $TOTAL_FILES++ }

Write-Sacred "Vault — Portal Navigation Note"
$r = CopyFile "$SOURCE\01_OBSIDIAN_VAULTS\SacredSpace_Vault\00_INBOX\vault_portal_sync.md" "$FLASH\01_VAULT\SacredSpace_Vault\00_INBOX\vault_portal_sync.md" "vault_portal_sync.md -> Vault\00_INBOX\"
if ($r) { $TOTAL_FILES++ }

Write-Sacred "Sacred Codex — Scripts"
$TOTAL_FILES += CopyDir "$SOURCE\04_SACRED_CODEX\scripts" "$FLASH\04_SACRED_CODEX\scripts" "scripts\ -> E:\04_SACRED_CODEX\scripts\"

Write-Sacred "CLAUDE.md — Governance"
$r = CopyFile "$SOURCE\CLAUDE.md" "$FLASH\02_COUNCIL_GROVE\CLAUDE.md" "CLAUDE.md -> E:\02_COUNCIL_GROVE\"
if ($r) { $TOTAL_FILES++ }

Write-Sacred "Brand Assets -> Shared Space (Jeanie)"
$TOTAL_FILES += CopyDir "$SOURCE\07_SOCIAL_MOTHERSHIP\brand_assets" "$FLASH\SHARED_SPACE\ACTIVE\brand_assets" "brand_assets\ -> SHARED_SPACE\ACTIVE\"

Write-Sacred "Memory Engine — SQLite"
foreach ($db in @("05_MEMORY_ENGINE\sacred_memory.sqlite","05_MEMORY_ENGINE\memory.db")) {
    $r = CopyFile "$SOURCE\$db" "$FLASH\$db" $db
    if ($r) { $TOTAL_FILES++ }
}

Write-Sacred "Core OS Files"
foreach ($f in @("boot_sacred.sh","requirements.txt","sacredspace_ai_config.yaml")) {
    $r = CopyFile "$SOURCE\$f" "$FLASH\$f" $f
    if ($r) { $TOTAL_FILES++ }
}

Write-Sacred "Calling SACRED_ARCANA_POPULATE.ps1..."
$arcanaScript = "$FLASH\04_SACRED_CODEX\scripts\SACRED_ARCANA_POPULATE.ps1"
if (Test-Path $arcanaScript -PathType Leaf) {
    try {
        & powershell.exe -ExecutionPolicy Bypass -File $arcanaScript
        Log "OK" "SACRED_ARCANA_POPULATE.ps1 completed"
        Write-Done "Arcana populate complete"
    } catch {
        Write-Warn "SACRED_ARCANA_POPULATE.ps1 error: $_"
        Log "WARN" "Arcana populate error: $_"
    }
} else {
    Write-Warn "SACRED_ARCANA_POPULATE.ps1 not found at $arcanaScript"
    Log "WARN" "SACRED_ARCANA_POPULATE.ps1 not found"
}

Log "INFO" "=== POPULATE COMPLETE — $TOTAL_FILES files — $TIMESTAMP ==="

Write-Host ""
Write-Host "  +------------------------------------------------+" -ForegroundColor DarkCyan
Write-Host "  |  S∆CR3D FL∆SH — POPULATE COMPLETE             |" -ForegroundColor DarkCyan
Write-Host "  +------------------------------------------------+" -ForegroundColor DarkCyan
Write-Host ("  |  Files copied: {0,-5}                          |" -f $TOTAL_FILES) -ForegroundColor White
Write-Host "  +------------------------------------------------+" -ForegroundColor DarkCyan
Write-Host "  |  Open portal: file:///E:/PORTAL/index.html    |" -ForegroundColor Green
Write-Host "  +------------------------------------------------+" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  ∆∆∆ In Lakesh Alakin ∆∆∆" -ForegroundColor Magenta
Write-Host ""
