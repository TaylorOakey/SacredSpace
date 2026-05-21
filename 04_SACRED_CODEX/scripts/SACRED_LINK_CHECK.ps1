#Requires -Version 5.1
<#
.SYNOPSIS
    S∆CR3D SP∆CE — Flash Drive Link Health Check v1.0
    ∆∆∆ O∆K3YTREE ∆∆∆

.DESCRIPTION
    Verifies all critical paths on the Sacred Flash Drive.
    Outputs a PASS/FAIL/WARN table and writes a timestamped log.

.NOTES
    In Lakesh Alakin. ∆∆∆
#>

param([string]$Drive = "E")

$FLASH     = "${Drive}:"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_DIR   = "$FLASH\_LOGS"
$LOG_FILE  = "$LOG_DIR\linkcheck_$TIMESTAMP.log"
$RESULTS   = [System.Collections.Generic.List[PSCustomObject]]::new()

New-Item -ItemType Directory -Force -Path $LOG_DIR -ErrorAction SilentlyContinue | Out-Null

function Check {
    param([string]$Label, [string]$Path, [string]$Type = "Leaf", [bool]$Critical = $true)
    $exists = if ($Type -eq "Leaf") { Test-Path $Path -PathType Leaf } else { Test-Path $Path -PathType Container }
    $status = if ($exists) { "PASS" } elseif ($Critical) { "FAIL" } else { "WARN" }
    $color  = switch ($status) { "PASS" { "Green" } "FAIL" { "Red" } "WARN" { "Yellow" } }
    $obj    = [PSCustomObject]@{ Status=$status; Label=$Label; Path=$Path }
    $script:RESULTS.Add($obj)
    $pad    = $Label.PadRight(42)
    Write-Host "  [$status]  $pad  $Path" -ForegroundColor $color
    Add-Content -Path $LOG_FILE -Value "[$status] $Label :: $Path" -Encoding UTF8 -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor DarkCyan
Write-Host "  ∆  S∆CR3D FLASH DRIVE — LINK HEALTH CHECK       ∆" -ForegroundColor DarkCyan
Write-Host "  ∆  Drive: ${Drive}:\   Time: $(Get-Date -Format 'HH:mm:ss')                ∆" -ForegroundColor DarkCyan
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  Status  Check                                      Path" -ForegroundColor DarkGray
Write-Host "  ------  -----------------------------------------  ----" -ForegroundColor DarkGray

# ── Core Drive ────────────────────────────────────────────
Check "Flash drive root"              "$FLASH\"                                          Container
Check "00_BOOT dir"                   "$FLASH\00_BOOT"                                   Container
Check "SACRED_ENV.env"                "$FLASH\00_BOOT\SACRED_ENV.env"                    Leaf
Check "00_HANDOFF dir"                "$FLASH\00_HANDOFF"                                Container $false

# ── Portal ────────────────────────────────────────────────
Check "PORTAL dir"                    "$FLASH\PORTAL"                                    Container
Check "PORTAL\index.html"             "$FLASH\PORTAL\index.html"                         Leaf
Check "PORTAL\images.json"            "$FLASH\PORTAL\images.json"                        Leaf       $false

# ── Council Grove ─────────────────────────────────────────
Check "02_COUNCIL_GROVE dir"          "$FLASH\02_COUNCIL_GROVE"                          Container
Check "obsidian_links.json"           "$FLASH\02_COUNCIL_GROVE\obsidian_links.json"      Leaf
Check "CLAUDE.md in grove"            "$FLASH\02_COUNCIL_GROVE\CLAUDE.md"                Leaf       $false

# ── Vault ────────────────────────────────────────────────
Check "01_VAULT dir"                  "$FLASH\01_VAULT"                                  Container
Check "SacredSpace_Vault root"        "$FLASH\01_VAULT\SacredSpace_Vault"                Container
Check "00_INBOX dir"                  "$FLASH\01_VAULT\SacredSpace_Vault\00_INBOX"       Container
Check "vault_portal_sync.md"          "$FLASH\01_VAULT\SacredSpace_Vault\00_INBOX\vault_portal_sync.md" Leaf $false

# ── Sacred Codex Scripts ──────────────────────────────────
Check "04_SACRED_CODEX\scripts"       "$FLASH\04_SACRED_CODEX\scripts"                  Container
Check "SACRED_FLASH_SCAFFOLD.ps1"     "$FLASH\04_SACRED_CODEX\scripts\SACRED_FLASH_SCAFFOLD.ps1"  Leaf
Check "SACRED_FLASH_POPULATE.ps1"     "$FLASH\04_SACRED_CODEX\scripts\SACRED_FLASH_POPULATE.ps1"  Leaf
Check "SACRED_ARCANA_POPULATE.ps1"    "$FLASH\04_SACRED_CODEX\scripts\SACRED_ARCANA_POPULATE.ps1" Leaf
Check "SACRED_LINK_CHECK.ps1"         "$FLASH\04_SACRED_CODEX\scripts\SACRED_LINK_CHECK.ps1"      Leaf

# ── Arcana Landscapes ─────────────────────────────────────
Check "ARCANA_LANDSCAPES root"        "$FLASH\ARCANA_LANDSCAPES"                         Container
Check "ARCANA_LANDSCAPES\SIGILS"      "$FLASH\ARCANA_LANDSCAPES\SIGILS"                  Container
Check "ARCANA_LANDSCAPES\CHARACTERS"  "$FLASH\ARCANA_LANDSCAPES\CHARACTERS"              Container
Check "ARCANA_LANDSCAPES\ENVIRONMENTS" "$FLASH\ARCANA_LANDSCAPES\ENVIRONMENTS"           Container
Check "ARCANA_LANDSCAPES\ARCANA_GRID" "$FLASH\ARCANA_LANDSCAPES\ARCANA_GRID"             Container
Check "ARCANA_LANDSCAPES\BRAND"       "$FLASH\ARCANA_LANDSCAPES\BRAND"                   Container
Check "ARCANA_LANDSCAPES\GRAMA"       "$FLASH\ARCANA_LANDSCAPES\GRAMA"                   Container
Check "ARCANA_LANDSCAPES\PORTAL_WALLPAPERS" "$FLASH\ARCANA_LANDSCAPES\PORTAL_WALLPAPERS" Container

# ── Shared Space ──────────────────────────────────────────
Check "SHARED_SPACE root"             "$FLASH\SHARED_SPACE"                              Container
Check "SHARED_SPACE\ACTIVE"           "$FLASH\SHARED_SPACE\ACTIVE"                       Container
Check "SHARED_SPACE\CANON"            "$FLASH\SHARED_SPACE\CANON"                        Container
Check "SHARED_SPACE\LETTERS"          "$FLASH\SHARED_SPACE\LETTERS"                      Container

# ── Chrome Extension ─────────────────────────────────────
Check "CHROME_EXTENSION dir"          "$FLASH\CHROME_EXTENSION\sacred-chrome"            Container  $false
Check "manifest.json"                 "$FLASH\CHROME_EXTENSION\sacred-chrome\manifest.json" Leaf    $false

# ── Memory Engine ─────────────────────────────────────────
Check "05_MEMORY_ENGINE dir"          "$FLASH\05_MEMORY_ENGINE"                          Container  $false
Check "sacred_memory.sqlite"          "$FLASH\05_MEMORY_ENGINE\sacred_memory.sqlite"     Leaf       $false

# ── Summary ───────────────────────────────────────────────
$passed = ($RESULTS | Where-Object { $_.Status -eq "PASS" }).Count
$failed = ($RESULTS | Where-Object { $_.Status -eq "FAIL" }).Count
$warned = ($RESULTS | Where-Object { $_.Status -eq "WARN" }).Count
$total  = $RESULTS.Count

Write-Host ""
Write-Host "  +-----------------------------------------+" -ForegroundColor DarkCyan
Write-Host "  |  SACRED LINK CHECK — SUMMARY            |" -ForegroundColor DarkCyan
Write-Host "  +-----------------------------------------+" -ForegroundColor DarkCyan
Write-Host ("  |  PASS  : {0,-5}                           |" -f $passed) -ForegroundColor Green
Write-Host ("  |  FAIL  : {0,-5}                           |" -f $failed) -ForegroundColor $(if($failed -gt 0){"Red"}else{"White"})
Write-Host ("  |  WARN  : {0,-5}                           |" -f $warned) -ForegroundColor $(if($warned -gt 0){"Yellow"}else{"White"})
Write-Host ("  |  TOTAL : {0,-5}                           |" -f $total) -ForegroundColor White
Write-Host "  +-----------------------------------------+" -ForegroundColor DarkCyan

if ($failed -eq 0) {
    Write-Host "  |  STATUS: ALL CRITICAL CHECKS PASS      |" -ForegroundColor Green
} else {
    Write-Host "  |  STATUS: $failed CRITICAL CHECK(S) FAILED     |" -ForegroundColor Red
    Write-Host "  |  Run SACRED_FLASH_POPULATE.ps1 to fix  |" -ForegroundColor Yellow
}
Write-Host "  |  Log: $_LOGS\linkcheck_$TIMESTAMP.log |" -ForegroundColor DarkGray
Write-Host "  +-----------------------------------------+" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  ∆∆∆ In Lakesh Alakin ∆∆∆" -ForegroundColor Magenta
Write-Host ""

Add-Content -Path $LOG_FILE -Value "=== RESULT: PASS=$passed FAIL=$failed WARN=$warned ===" -Encoding UTF8 -ErrorAction SilentlyContinue
