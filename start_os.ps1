Write-Host "∆∆∆ SACREDSPACE OS — BOOT SEQUENCE ∆∆∆" -ForegroundColor Cyan

# 1. Check for Ollama
if (!(Get-Process "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "! Ollama is not running. Awakening the engine..." -ForegroundColor Yellow
    Start-Process "ollama app"
    Start-Sleep -Seconds 5
}

# 2. Activate Environment and Start Bridge
Write-Host "✓ Neural Bridge Awakening..." -ForegroundColor Green
.\.venv\Scripts\python.exe systems\fastapi\bridge.py
