$root = "D:\SacredSpace_OS"
$vault = "$root\01_OBSIDIAN_VAULTS\SacredSpace_Vault"
$scripts = "$root\00_SYSTEM_CORE\scripts"

Write-Host ""
Write-Host "=========================================" -ForegroundColor DarkCyan
Write-Host " Sâˆ†CR3DSPâˆ†CE OS IGNITION SEQUENCE " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor DarkCyan
Write-Host ""

Write-Host "[1/4] Opening Obsidian vault..." -ForegroundColor Yellow
$obsidianExe = "$env:LOCALAPPDATA\Programs\Obsidian\Obsidian.exe"
if (Test-Path $obsidianExe) {
    Start-Process -FilePath $obsidianExe -ArgumentList """$vault"""
} else {
    Write-Host "Obsidian executable not found at $obsidianExe" -ForegroundColor Red
}

Write-Host "[2/4] Running Sacred sync..." -ForegroundColor Yellow
python "$scripts\sacred_sync.py" --render-only --root $root

Write-Host "[3/4] Running Sacred audit..." -ForegroundColor Yellow
python "$scripts\sacred_audit.py" --root $root

Write-Host "[4/4] Opening Sacred root..." -ForegroundColor Yellow
Start-Process explorer.exe $root

Write-Host ""
Write-Host "SacredSpace OS is online." -ForegroundColor Green
Write-Host ""
