Write-Host '=== SACRED HEALTH CHECK v1.0 ===' -ForegroundColor Cyan
 
# 1. Internet Check
$ping = Test-Connection -ComputerName 8.8.8.8 -Count 1 -Quiet
if ($ping) { Write-Host '[OK] Internet Connection' -ForegroundColor Green }
else { Write-Host '[FAIL] Internet Connection' -ForegroundColor Red }
 
# 2. Git Check
try { $git = git --version; Write-Host "[OK] $git" -ForegroundColor Green }
catch { Write-Host '[FAIL] Git not found in PATH' -ForegroundColor Red }
 
# 3. Ollama Check
try { 
    $ollama = Invoke-WebRequest http://127.0.0.1:11434 -UseBasicParsing -ErrorAction SilentlyContinue
    if ($ollama.StatusCode -eq 200) { Write-Host '[OK] Ollama Engine Active' -ForegroundColor Green }
} catch { Write-Host '[FAIL] Ollama Engine Offline' -ForegroundColor Red }
 
# 4. Pillar Check
python D:\SacredSpace_OS\core\genesis.py
 
# 5. Bridge Check
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($port8000) { Write-Host '[OK] FastAPI Bridge Heartbeat Detected' -ForegroundColor Green }
else { Write-Host '[WAIT] Bridge is currently resting.' -ForegroundColor Yellow }

Write-Host '=== CHECK COMPLETE ===' -ForegroundColor Cyan
