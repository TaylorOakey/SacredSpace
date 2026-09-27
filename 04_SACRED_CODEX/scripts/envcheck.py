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