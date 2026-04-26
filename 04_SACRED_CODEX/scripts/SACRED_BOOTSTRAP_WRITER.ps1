# SACRED_BOOTSTRAP_WRITER.ps1
# Writes sacred_stabilize.ps1 and envcheck.py directly to D:
# No downloads needed. Run once, then delete this file.
# Usage: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass; .\SACRED_BOOTSTRAP_WRITER.ps1

$SCRIPTS = "D:\SacredSpace_OS\04_SACRED_CODEX\scripts"

Write-Host "Writing sacred_stabilize.ps1..." -ForegroundColor Yellow

$stabilizer = @'
param([switch]$Repair,[switch]$Silent,[string]$LogPath="D:\SacredSpace_OS\04_SACRED_CODEX\STABILIZER_LOG.txt")
$ESC=[char]27;$AMBER="$ESC[38;2;255;176;0m";$FOREST="$ESC[38;2;80;180;100m";$RED="$ESC[38;2;220;60;60m";$DIM="$ESC[38;2;100;100;100m";$RESET="$ESC[0m"
function W($t,$c=$AMBER){if(-not $Silent){Write-Host "$c$t$RESET"}}
function C($label,$pass,$detail=""){
    $icon=if($pass){"${FOREST}[PASS]"}else{"${RED}[FAIL]"}
    $d=if($detail){" ${DIM}-> $detail$RESET"}else{""}
    if(-not $Silent){Write-Host "  $icon$RESET $AMBER$label$RESET$d"}
    return $pass
}
$pass=0;$fail=0;$log=[System.Collections.Generic.List[string]]::new();$ts=Get-Date -Format "yyyy-MM-dd HH:mm:ss"
if(-not $Silent){Clear-Host;W "`n  S∆CR3D ST∆BIL!Z3R v1.0  |  SacredSpace OS  |  $ts`n  ∆OAK9∂ | Ground. Consolidate. Deploy. Document. Repeat.`n"}

W "  [1] PILLAR DIRECTORIES"
@("01_OBSIDIAN_VAULTS","02_COUNCIL_GROVE","03_NEURAL_FOREST","04_SACRED_CODEX","05_MEMORY_ENGINE","06_AGENT_LAYER","07_SOCIAL_MOTHERSHIP","08_LEARNING_PATH","09_SACRED_MARKET")|%{
    $p="D:\SacredSpace_OS\$_";$ok=Test-Path $p
    if(C "Pillar: $_" $ok){$pass++}else{$fail++;if($Repair){New-Item -ItemType Directory -Path $p -Force|Out-Null}}
    $log.Add("[$ts] PILLAR $_ | $(if($ok){'OK'}else{'MISSING'})")
}

W "`n  [2] WSL2 BRIDGE"
$wsl=$false;try{$o=wsl --list --running 2>&1;$wsl=($o -match "Ubuntu")}catch{}
if(C "WSL2 Ubuntu running" $wsl){$pass++}else{$fail++;if($Repair){Start-Process wsl -ArgumentList "-d Ubuntu" -WindowStyle Hidden}}
$log.Add("[$ts] WSL2 | $(if($wsl){'ACTIVE'}else{'INACTIVE'})")
$mnt=$false;if($wsl){try{wsl -- test -d /mnt/d/SacredSpace_OS 2>&1|Out-Null;$mnt=($LASTEXITCODE -eq 0)}catch{}}
if(C "WSL2 /mnt/d mount" $mnt){$pass++}else{$fail++}
$log.Add("[$ts] WSL2_MOUNT | $(if($mnt){'OK'}else{'UNREACHABLE'})")

W "`n  [3] SERVICE PORTS"
function TP($h,$p){try{$t=[System.Net.Sockets.TcpClient]::new();$a=$t.BeginConnect($h,$p,$null,$null);$w=$a.AsyncWaitHandle.WaitOne(1500,$false);if($w -and $t.Connected){$t.Close();return $true};$t.Close();return $false}catch{return $false}}
@(@{N="FastAPI :8888";P=8888},@{N="Ollama :11434";P=11434},@{N="ChromaDB :8000";P=8000},@{N="Redis :6379";P=6379},@{N="WebUI :3000";P=3000})|%{
    $ok=TP "localhost" $_.P
    if(C $_.N $ok){$pass++}else{$fail++}
    $log.Add("[$ts] PORT_$($_.P) | $(if($ok){'OPEN'}else{'CLOSED'})")
}

W "`n  [4] PYTHON + VENV"
$pyok=$false;$pyver="";if($wsl){try{$v=wsl -- python3 --version 2>&1;$pyok=($v -match "Python 3");$pyver=$v}catch{}}
if(C "Python 3 (WSL2)" $pyok $pyver){$pass++}else{$fail++}
$venv=Test-Path "D:\SacredSpace_OS\.venv\Scripts\python.exe"
if(C ".venv present" $venv){$pass++}else{$fail++;if($Repair){try{wsl -- python3 -m venv /mnt/d/SacredSpace_OS/.venv 2>&1|Out-Null}catch{}}}
$log.Add("[$ts] PYTHON | $(if($pyok){$pyver}else{'MISSING'}) | VENV=$(if($venv){'YES'}else{'NO'})")

W "`n  [5] GIT STATE"
$gitok=Test-Path "D:\SacredSpace_OS\.git"
if(C "Git initialized" $gitok){$pass++}else{$fail++}
if($gitok){try{$s=git -C "D:\SacredSpace_OS" status --short 2>&1;$dirty=($s.Trim().Length -gt 0);if(C "Working tree clean" (-not $dirty) $(if($dirty){"$($s.Split("`n").Count) change(s)"}else{"clean"})){$pass++}else{$fail++}}catch{}}
$log.Add("[$ts] GIT | $(if($gitok){'INIT'}else{'UNINIT'})")

W "`n  [6] DISK HEALTH"
@("D","E")|%{try{$d=Get-PSDrive -Name $_ -ErrorAction Stop;$u=[math]::Round($d.Used/1GB,1);$f=[math]::Round($d.Free/1GB,1);$t=[math]::Round(($d.Used+$d.Free)/1GB,1);$p=[math]::Round($d.Used/($d.Used+$d.Free)*100,0);$ok=($p -lt 90);if(C "${_}: drive" $ok "${u}GB/${t}GB (${p}%)"){$pass++}else{$fail++};$log.Add("[$ts] DISK_$_ | ${p}% used")}catch{if(C "${_}: drive" $false "not found"){$pass++}else{$fail++}}}

W "`n  [7] CANON SCRIPTS"
@("sacred_triage.ps1","SacredActivate.ps1","SACREDSPACE_PROFILE.ps1","sacred_cli.py","sacred_harvester.py","sacred_ingest_core.py","sacred_doc_crawler.py")|%{
    $ok=Test-Path "$SCRIPTS\$_"
    if(C "script: $_" $ok){$pass++}else{$fail++}
}

$total=$pass+$fail;$pct=if($total -gt 0){[math]::Round($pass/$total*100,0)}else{0}
$sc=if($pct -ge 90){$FOREST}elseif($pct -ge 70){$AMBER}else{$RED}
$sl=if($pct -ge 90){"SACRED — STABLE"}elseif($pct -ge 70){"CAUTIONARY"}else{"CRITICAL — UNSTABLE"}
if(-not $Silent){W "`n  ─────────────────────────────────────────────";W "  ◈ SEAL: $sl" $sc;Write-Host "  ${AMBER}Passed: ${FOREST}$pass$RESET  ${AMBER}Failed: ${RED}$fail$RESET  ${AMBER}Score: ${sc}${pct}%$RESET";W "  ∆OAK9∂ | In Lakesh Alakin`n"}
try{$log.Add("SEAL | $sl | $pass/$total");[System.IO.File]::AppendAllLines($LogPath,$log)}catch{}
exit $fail
'@

[System.IO.File]::WriteAllText("$SCRIPTS\sacred_stabilize.ps1", $stabilizer)
Write-Host "  [OK] sacred_stabilize.ps1 written" -ForegroundColor Green

Write-Host "Writing envcheck.py..." -ForegroundColor Yellow

$envcheck = @'
import sys,os,json,socket,sqlite3,subprocess,argparse,importlib.util
from pathlib import Path
from datetime import datetime

A="\033[38;2;255;176;0m";F="\033[38;2;80;180;100m";R="\033[38;2;220;60;60m";D="\033[38;2;100;100;100m";X="\033[0m"
ROOT=Path("/mnt/d/SacredSpace_OS");TS=datetime.now().strftime("%Y-%m-%d %H:%M:%S");results=[]

def chk(label,passed,detail="",q=False):
    ic=f"{F}[PASS]{X}" if passed else f"{R}[FAIL]{X}"
    dt=f"  {D}-> {detail}{X}" if detail else ""
    if not q: print(f"  {ic} {A}{label}{X}{dt}")
    results.append({"label":label,"passed":passed,"detail":detail})
    return passed

def port_open(h,p,t=1.5):
    try:
        with socket.create_connection((h,p),timeout=t): return True
    except: return False

def pkg_ok(p): return importlib.util.find_spec(p) is not None

parser=argparse.ArgumentParser()
parser.add_argument("--repair",action="store_true")
parser.add_argument("--json",action="store_true")
parser.add_argument("--quiet",action="store_true")
args=parser.parse_args()
q=args.quiet

if not q:
    print(f"\n{A}  S∆CR3D ENV CH3CK v1.0  |  {TS}{X}")
    print(f"{D}  Python Service Health Companion — AURORA Agent{X}\n")

print(f"{A}  [1] PYTHON PACKAGES{X}") if not q else None
pkgs={"fastapi":"FastAPI","uvicorn":"ASGI","chromadb":"ChromaDB","redis":"Redis","anthropic":"Anthropic SDK","sqlalchemy":"SQLAlchemy","apscheduler":"APScheduler","rich":"Rich CLI","aiohttp":"Async HTTP","pydantic":"Pydantic","requests":"Requests","numpy":"NumPy"}
miss=[]
for p,d in pkgs.items():
    ok=pkg_ok(p);chk(f"pkg: {p}",ok,d,q)
    if not ok: miss.append(p)
if args.repair and miss:
    for p in miss:
        r=subprocess.run([sys.executable,"-m","pip","install",p,"-q"],capture_output=True)
        if not q: print(f"  {'[OK]' if r.returncode==0 else '[FAIL]'} installed {p}")

print(f"\n{A}  [2] SERVICE PORTS{X}") if not q else None
for h,p,n in [("localhost",8888,"FastAPI"),("localhost",11434,"Ollama"),("localhost",8000,"ChromaDB"),("localhost",6379,"Redis"),("localhost",3000,"WebUI")]:
    chk(f"{n} (:{p})",port_open(h,p),"up" if port_open(h,p) else "down",q)

print(f"\n{A}  [3] OLLAMA MODELS{X}") if not q else None
try:
    import urllib.request
    with urllib.request.urlopen("http://localhost:11434/api/tags",timeout=3) as r:
        data=json.loads(r.read());models=[m["name"] for m in data.get("models",[])]
        chk("Ollama API",True,f"{len(models)} model(s)",q)
        for m in models: chk(f"  model: {m}",True,"",q)
except Exception as e: chk("Ollama API",False,str(e),q)

print(f"\n{A}  [4] SQLITE SCHEMA{X}") if not q else None
dbs=[ROOT/"05_MEMORY_ENGINE/sacredspace.db",ROOT/"05_MEMORY_ENGINE/memory.db",ROOT/"sacredspace.db"]
found=False
for db in dbs:
    if db.exists():
        found=True;chk("SQLite DB",True,str(db),q)
        try:
            c=sqlite3.connect(str(db));t=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")];c.close()
            chk(f"Tables ({len(t)})",len(t)>0,", ".join(t[:5]),q);chk("13-table schema",len(t)>=13,f"found {len(t)}",q)
        except Exception as e: chk("Schema readable",False,str(e),q)
        break
if not found: chk("SQLite DB",False,"not found",q)

print(f"\n{A}  [5] ENVIRONMENT VARS{X}") if not q else None
for v in ["ANTHROPIC_API_KEY","SACREDSPACE_ROOT","OLLAMA_API_BASE"]:
    val=os.environ.get(v);ok=bool(val)
    chk(f"env: {v}",ok,f"{val[:6]}..." if ok and len(val)>6 else ("SET" if ok else "NOT SET"),q)

total=len(results);passed=sum(1 for r in results if r["passed"]);failed=total-passed
pct=round(passed/total*100) if total>0 else 0
sc=F if pct>=90 else (A if pct>=70 else R)
sl="SACRED — STABLE" if pct>=90 else ("CAUTIONARY" if pct>=70 else "CRITICAL — UNSTABLE")

if not q:
    print(f"\n{A}  ─────────────────────────────────────────────{X}")
    print(f"  {sc}{sl}{X}")
    print(f"  {A}Passed: {F}{passed}{X}  {A}Failed: {R}{failed}{X}  {A}Score: {sc}{pct}%{X}")
    print(f"  {D}∆OAK9∂ | In Lakesh Alakin{X}\n")

if args.json: print(json.dumps({"timestamp":TS,"status":sl,"pct":pct,"passed":passed,"failed":failed,"checks":results},indent=2))

log=ROOT/"04_SACRED_CODEX/PYTHON_STABILIZER_LOG.txt"
try:
    log.parent.mkdir(parents=True,exist_ok=True)
    with open(log,"a") as f:
        f.write(f"\n[{TS}] {sl} | {passed}/{total}\n")
        for r in results: f.write(f"  [{'PASS' if r['passed'] else 'FAIL'}] {r['label']}{(' -> '+r['detail']) if r['detail'] else ''}\n")
        f.write("─"*60+"\n")
except: pass

sys.exit(failed)
'@

[System.IO.File]::WriteAllText("$SCRIPTS\envcheck.py", $envcheck)
Write-Host "  [OK] envcheck.py written" -ForegroundColor Green

Write-Host "`nBoth files written. Now run:" -ForegroundColor Yellow
Write-Host "  .\sacred_stabilize.ps1" -ForegroundColor Cyan
Write-Host "  wsl python3 /mnt/d/SacredSpace_OS/04_SACRED_CODEX/scripts/envcheck.py" -ForegroundColor Cyan
