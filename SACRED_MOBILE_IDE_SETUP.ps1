# SACRED_MOBILE_IDE_SETUP.ps1
# Sets up a mobile-accessible web IDE for SacredSpace OS
# Dev server: localhost:5173 (Vite default)
# Run from D:\SacredSpace_OS with ExecutionPolicy Bypass

param(
    [string]$ProjectName = "sacred-mobile-ide",
    [string]$RootDir     = "D:\SacredSpace_OS\04_SACRED_CODEX"
)

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "    [OK] $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    [!]  $msg" -ForegroundColor Yellow }

# ── 1. Prereqs ────────────────────────────────────────────────────────────────
Write-Step "Checking prerequisites"

foreach ($cmd in @("node", "npm", "git")) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Error "$cmd not found. Install it and re-run."
    }
    $ver = & $cmd --version 2>&1
    Write-OK "$cmd $ver"
}

$nodeMajor = [int](& node -e "process.stdout.write(process.versions.node.split('.')[0])")
if ($nodeMajor -lt 18) {
    Write-Error "Node 18+ required (found $nodeMajor). Update via https://nodejs.org"
}

# ── 2. Scaffold with Vite ─────────────────────────────────────────────────────
Write-Step "Scaffolding Vite + React project"

$target = Join-Path $RootDir $ProjectName
if (Test-Path $target) {
    Write-Warn "$target already exists — skipping scaffold"
} else {
    Push-Location $RootDir
    npm create vite@latest $ProjectName -- --template react
    Pop-Location
    Write-OK "Scaffolded at $target"
}

# ── 3. Install dependencies ───────────────────────────────────────────────────
Write-Step "Installing dependencies"
Push-Location $target
npm install
Write-OK "Base deps installed"

# Mobile IDE extras: Monaco editor + Tailwind
npm install @monaco-editor/react
npm install -D tailwindcss @tailwindcss/vite
Write-OK "Monaco + Tailwind installed"
Pop-Location

# ── 4. Patch vite.config.js for network (mobile) access ──────────────────────
Write-Step "Patching vite.config.js for mobile network access"

$viteConfig = Join-Path $target "vite.config.js"
$configContent = @'
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',   // accessible from phone on same network
    port: 5173,
    strictPort: true,
  },
})
'@
Set-Content -Path $viteConfig -Value $configContent -Encoding UTF8
Write-OK "vite.config.js patched (host=0.0.0.0, port=5173)"

# ── 5. Patch tailwind CSS entry ───────────────────────────────────────────────
Write-Step "Patching src/index.css for Tailwind"
$cssEntry = Join-Path $target "src\index.css"
$tailwindDirective = "@import 'tailwindcss';`n"
$existing = Get-Content $cssEntry -Raw -ErrorAction SilentlyContinue
if ($existing -notmatch "@import 'tailwindcss'") {
    $tailwindDirective + $existing | Set-Content $cssEntry -Encoding UTF8
    Write-OK "Tailwind @import prepended to index.css"
} else {
    Write-Warn "Tailwind @import already present"
}

# ── 6. Done ───────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host "  SacredSpace Mobile IDE ready" -ForegroundColor Magenta
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Magenta
Write-Host ""
Write-Host "  To start:" -ForegroundColor White
Write-Host "    cd $target" -ForegroundColor Gray
Write-Host "    npm run dev" -ForegroundColor Gray
Write-Host ""
Write-Host "  Local:   http://localhost:5173" -ForegroundColor White
Write-Host "  Network: http://<your-LAN-IP>:5173  (phone / tablet)" -ForegroundColor White
Write-Host ""
