# apply_registry_migration.ps1
# SacredSpace OS — Registry v1.1.0 migration
# Run from: D:\SacredSpace_OS\
# Usage: .\apply_registry_migration.ps1

$ErrorActionPreference = "Stop"
$ROOT = "D:\SacredSpace_OS"
$DB   = "$ROOT\05_MEMORY_ENGINE\omni_ledger.db"
$SQL  = "$ROOT\05_MEMORY_ENGINE\migrations\registry_v1_1_0.sql"

Write-Host "`n=== SacredSpace Registry v1.1.0 Migration ===" -ForegroundColor Cyan

# ── STEP 1: Fetch migration file from GitHub ──────────────────────────────────
Write-Host "`n[1/4] Fetching migration file from origin/main..." -ForegroundColor Yellow
Push-Location $ROOT
git fetch origin main
git checkout origin/main -- 05_MEMORY_ENGINE/migrations/registry_v1_1_0.sql
Pop-Location

if (-not (Test-Path $SQL)) {
    Write-Error "Migration file not found after fetch: $SQL"
    exit 1
}
Write-Host "      OK — $SQL" -ForegroundColor Green

# ── STEP 2: Ensure sqlite3 is available ──────────────────────────────────────
Write-Host "`n[2/4] Checking for sqlite3..." -ForegroundColor Yellow
$sqlite = Get-Command sqlite3 -ErrorAction SilentlyContinue

if (-not $sqlite) {
    Write-Host "      sqlite3 not found — installing via winget..." -ForegroundColor Yellow
    winget install --id SQLite.SQLite --silent --accept-package-agreements --accept-source-agreements
    # Refresh PATH for this session
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH","Machine") + ";" +
                [System.Environment]::GetEnvironmentVariable("PATH","User")
    $sqlite = Get-Command sqlite3 -ErrorAction SilentlyContinue
    if (-not $sqlite) {
        Write-Error "sqlite3 still not found after install. Restart PowerShell and rerun."
        exit 1
    }
}
Write-Host "      OK — $($sqlite.Source)" -ForegroundColor Green

# ── STEP 3: Apply migration ───────────────────────────────────────────────────
Write-Host "`n[3/4] Applying migration to omni_ledger.db..." -ForegroundColor Yellow

if (-not (Test-Path $DB)) {
    Write-Host "      omni_ledger.db not found — will be created fresh." -ForegroundColor Yellow
}

sqlite3 $DB ".read $SQL"
Write-Host "      OK — migration applied." -ForegroundColor Green

# ── STEP 4: Verify 7 registry tables ─────────────────────────────────────────
Write-Host "`n[4/4] Verifying registry tables..." -ForegroundColor Yellow

$tables = sqlite3 $DB ".tables" | ForEach-Object { $_ -split '\s+' } | Where-Object { $_ -like "registry_*" } | Sort-Object

$expected = @(
    "registry_agents",
    "registry_artifacts",
    "registry_identities",
    "registry_links",
    "registry_lore",
    "registry_nodes",
    "registry_projects"
)

$missing = $expected | Where-Object { $tables -notcontains $_ }

if ($missing) {
    Write-Error "Missing tables: $($missing -join ', ')"
    exit 1
}

foreach ($t in $tables) { Write-Host "      ✓ $t" -ForegroundColor Green }

Write-Host "`n=== Registry v1.1.0 applied successfully ===" -ForegroundColor Cyan
Write-Host "    In lakesh alakin. ∆`n" -ForegroundColor Magenta
