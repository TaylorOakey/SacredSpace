#Requires -Version 5.1
<#
.SYNOPSIS
    S∆CR3D SP∆CE — Arcana Landscapes Populate v1.0
    ∆∆∆ O∆K3YTREE ∆∆∆

.DESCRIPTION
    Sorts art assets from E:\ARCANA_LANDSCAPES\UNSORTED\ (or a source path)
    into category subdirectories by filename prefix, then generates
    _INDEX.md in each category and images.json for the portal gallery.

    Prefix mapping:
      SIG_   -> SIGILS
      CHAR_  -> CHARACTERS
      ENV_   -> ENVIRONMENTS
      GRID_  -> ARCANA_GRID
      BRAND_ -> BRAND
      GRAMA_ -> GRAMA
      WP_    -> PORTAL_WALLPAPERS

.NOTES
    In Lakesh Alakin. ∆∆∆
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Continue"

param(
    [string]$Drive  = "E",
    [string]$Source = ""   # override unsorted source dir
)

$FLASH     = "${Drive}:"
$ARCANA    = "$FLASH\ARCANA_LANDSCAPES"
$PORTAL    = "$FLASH\PORTAL"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$LOG_DIR   = "$FLASH\_LOGS"
$LOG_FILE  = "$LOG_DIR\arcana_$TIMESTAMP.log"

New-Item -ItemType Directory -Force -Path $LOG_DIR | Out-Null

function Write-Sacred { param($msg) Write-Host "`n∆ $msg" -ForegroundColor Cyan }
function Write-Done   { param($msg) Write-Host "  OK  $msg" -ForegroundColor Green }
function Write-Warn   { param($msg) Write-Host "  !   $msg" -ForegroundColor Yellow }
function Log          { param($lvl,$msg) Add-Content -Path $LOG_FILE -Value "[$(Get-Date -Format 'HH:mm:ss')][$lvl] $msg" -Encoding UTF8 }

$PREFIX_MAP = @{
    'SIG_'   = 'SIGILS'
    'CHAR_'  = 'CHARACTERS'
    'ENV_'   = 'ENVIRONMENTS'
    'GRID_'  = 'ARCANA_GRID'
    'BRAND_' = 'BRAND'
    'GRAMA_' = 'GRAMA'
    'WP_'    = 'PORTAL_WALLPAPERS'
}

$IMAGE_EXTS = @('.jpg','.jpeg','.png','.gif','.webp','.svg','.bmp')

Write-Host ""
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor Magenta
Write-Host "  ∆  S∆CR3D ARCANA LANDSCAPES — POPULATE  ∆" -ForegroundColor Magenta
Write-Host "  ∆  Drive: ${Drive}:\ARCANA_LANDSCAPES\   ∆" -ForegroundColor Magenta
Write-Host "  ∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆∆" -ForegroundColor Magenta
Write-Host ""

# ── Ensure category dirs exist ────────────────────────────
Write-Sacred "Ensuring ARCANA_LANDSCAPES category dirs..."
$CATEGORIES = $PREFIX_MAP.Values | Sort-Object -Unique
foreach ($cat in $CATEGORIES) {
    $path = "$ARCANA\$cat"
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Force -Path $path | Out-Null
        Write-Done "Created: $cat"
    } else {
        Write-Host "  --  Exists: $cat" -ForegroundColor DarkGray
    }
}

# ── Sort from UNSORTED (if present) ──────────────────────
$unsortedDir = if ($Source) { $Source } else { "$ARCANA\UNSORTED" }
$sortedCount = 0

if (Test-Path $unsortedDir) {
    Write-Sacred "Sorting from: $unsortedDir"
    $files = Get-ChildItem -Path $unsortedDir -File -ErrorAction SilentlyContinue |
             Where-Object { $IMAGE_EXTS -contains $_.Extension.ToLower() }

    foreach ($f in $files) {
        $matched = $false
        foreach ($prefix in $PREFIX_MAP.Keys) {
            if ($f.Name.StartsWith($prefix, [System.StringComparison]::OrdinalIgnoreCase)) {
                $cat  = $PREFIX_MAP[$prefix]
                $dest = "$ARCANA\$cat\$($f.Name)"
                Copy-Item -Path $f.FullName -Destination $dest -Force
                Write-Done "Sorted: $($f.Name) -> $cat\"
                Log "OK" "Sorted: $($f.Name) -> $cat"
                $sortedCount++
                $matched = $true
                break
            }
        }
        if (-not $matched) {
            Write-Warn "No prefix match: $($f.Name) — left in UNSORTED"
            Log "WARN" "No prefix: $($f.Name)"
        }
    }
    Write-Done "Sorted $sortedCount files from UNSORTED"
} else {
    Write-Host "  --  No UNSORTED dir found — skipping sort step" -ForegroundColor DarkGray
    Write-Host "      Place images in ${Drive}:\ARCANA_LANDSCAPES\UNSORTED\ with prefix naming:" -ForegroundColor DarkGray
    foreach ($kv in $PREFIX_MAP.GetEnumerator() | Sort-Object Key) {
        Write-Host "      $($kv.Key)* -> $($kv.Value)" -ForegroundColor DarkGray
    }
}

# ── Generate _INDEX.md per category ──────────────────────
Write-Sacred "Writing category _INDEX.md files..."
foreach ($cat in $CATEGORIES) {
    $catPath = "$ARCANA\$cat"
    $imgs = Get-ChildItem -Path $catPath -File -ErrorAction SilentlyContinue |
            Where-Object { $IMAGE_EXTS -contains $_.Extension.ToLower() }
    $indexPath = "$catPath\_INDEX.md"
    $lines = @(
        "# ARCANA_LANDSCAPES\$cat",
        "",
        "> *In Lakesh Alakin. ∆∆∆*",
        "",
        "**Category:** $cat",
        "**Asset count:** $($imgs.Count)",
        "**Last indexed:** $(Get-Date -Format 'yyyy-MM-dd HH:mm')",
        "",
        "## Assets",
        ""
    )
    if ($imgs.Count -eq 0) {
        $lines += "*(empty — add images with prefix matching this category)*"
    } else {
        foreach ($img in $imgs) { $lines += "- $($img.Name)" }
    }
    [System.IO.File]::WriteAllText($indexPath, ($lines -join "`r`n"))
    Write-Done "_INDEX.md — $cat ($($imgs.Count) assets)"
}

# ── Generate images.json for portal gallery ───────────────
Write-Sacred "Generating images.json for portal gallery..."
$imageEntries = [System.Collections.Generic.List[string]]::new()

foreach ($cat in $CATEGORIES) {
    $catPath = "$ARCANA\$cat"
    $imgs = Get-ChildItem -Path $catPath -File -ErrorAction SilentlyContinue |
            Where-Object { $IMAGE_EXTS -contains $_.Extension.ToLower() }
    foreach ($img in $imgs) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($img.Name) -replace '_',' '
        $entry = "  {""name"":""$name"",""category"":""$cat"",""path"":""$cat/$($img.Name)""}"
        $imageEntries.Add($entry)
    }
}

$jsonPath = "$PORTAL\images.json"
if ($imageEntries.Count -gt 0) {
    $json = "[\n" + ($imageEntries -join ",`n") + "`n]"
    [System.IO.File]::WriteAllText($jsonPath, $json)
    Write-Done "images.json — $($imageEntries.Count) entries -> $jsonPath"
    Log "OK" "images.json: $($imageEntries.Count) entries"
} else {
    $json = "[]"
    [System.IO.File]::WriteAllText($jsonPath, $json)
    Write-Host "  --  images.json written as empty [] (no assets yet)" -ForegroundColor DarkGray
    Log "INFO" "images.json: empty (no assets in ARCANA_LANDSCAPES)"
}

Log "INFO" "=== ARCANA POPULATE COMPLETE — $TIMESTAMP ==="

Write-Host ""
Write-Host "  +----------------------------------------+" -ForegroundColor DarkCyan
Write-Host "  |  ARCANA LANDSCAPES — POPULATE COMPLETE |" -ForegroundColor DarkCyan
Write-Host "  +----------------------------------------+" -ForegroundColor DarkCyan
Write-Host ("  |  Files sorted : {0,-5}                   |" -f $sortedCount) -ForegroundColor White
Write-Host ("  |  Gallery items: {0,-5}                   |" -f $imageEntries.Count) -ForegroundColor White
Write-Host "  |  images.json written to PORTAL\        |" -ForegroundColor White
Write-Host "  +----------------------------------------+" -ForegroundColor DarkCyan
Write-Host ""
Write-Host "  ∆∆∆ In Lakesh Alakin ∆∆∆" -ForegroundColor Magenta
Write-Host ""
