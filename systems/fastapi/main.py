"""SacredSpace OS — FastAPI Spine v2.0"""
import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import os as _os
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from routers import memory, pillars, icaris, inference
from kethras      import router as kethras_router,   init_kethras_db
from merchant     import router as merchant_router,   init_merchant_db
from vault_watcher import router as vault_router,     init_vault_watcher, trigger_harvest
from lore_engine  import router as lore_router,       init_lore_engine
from reconcile    import reconcile
from grant_hunter import router as grant_router,    init_grant_db
from flow_tracker import router as flow_router,     init_flow_tracker

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../06_AGENT_LAYER"))
from hermes import generate_code, hermes_ping
from thricegreat import invoke as thricegreat_invoke

log = logging.getLogger("spine")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────
    init_kethras_db()
    init_merchant_db()
    init_vault_watcher()
    init_lore_engine()
    init_grant_db()
    init_flow_tracker()

    scheduler = BackgroundScheduler(timezone="UTC")
    scheduler.add_job(reconcile, CronTrigger(hour=3, minute=0), id="daily_reconcile", replace_existing=True)
    scheduler.start()
    log.info("Scheduler started — reconcile.py fires daily at 03:00 UTC")

    yield

    # ── Shutdown ──────────────────────────────────────────────
    scheduler.shutdown(wait=False)
    log.info("Scheduler shut down")


app = FastAPI(
    title="SacredSpace OS",
    description="∆∆∆ Architecting the SacredSpace ∆∆∆",
    version="2.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────
app.include_router(memory.router,  prefix="/memory",  tags=["Memory"])
app.include_router(pillars.router, prefix="/pillars", tags=["Pillars"])
app.include_router(icaris.router,  prefix="/icaris",  tags=["ICARIS"])
app.include_router(inference.router)
app.include_router(kethras_router)
app.include_router(merchant_router)
app.include_router(vault_router)
app.include_router(lore_router)
app.include_router(grant_router)
app.include_router(flow_router)


class HermesRequest(BaseModel):
    intent: str
    context: str = ""


class ThriceGreatRequest(BaseModel):
    intent: str
    mode: str = "code"


@app.post("/thricegreat")
async def thricegreat(req: ThriceGreatRequest):
    try:
        result = await asyncio.to_thread(thricegreat_invoke, intent=req.intent, mode=req.mode)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return result


@app.post("/hermes")
async def hermes(req: HermesRequest):
    if not hermes_ping():
        raise HTTPException(status_code=503, detail="☿ Hermes offline — Ollama unreachable")
    result = generate_code(prompt=req.intent, context=req.context)
    return result


@app.get("/")
async def root():
    return {
        "spine":     "systems/fastapi/main.py:8888",
        "status":    "LIVE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents":    ["ELIAS", "AURORA", "ASHER", "IRIS"],
        "cascade":   ["ollama", "gemini", "mock"],
        "routes": [
            "GET  /",
            "GET  /health",
            "POST /harvest",
            "POST /hermes",
            "POST /thricegreat",
            "GET  /memory",
            "GET  /pillars",
            "GET  /icaris",
            "GET  /kethras/status",
            "GET  /kethras/spells",
            "GET  /merchant/status",
            "GET  /merchant/artifacts",
            "GET  /vault-watcher-obsidian-sync",
            "GET  /lore-to-product-engine",
            "GET  /tools-manifest",
            "GET  /image-pipeline",
            "GET  /grant-hunter",
            "GET  /grant-hunter/report",
            "GET  /flow-tracker",
            "POST /flow-tracker",
            "GET  /flow-dashboard",
            "GET  /merchant/vaas",
            "POST /merchant/vaas",
        ],
        "seal":      "∆∆∆ In lakesh alakin ∆∆∆",
    }

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

@app.get("/tools-manifest", response_class=HTMLResponse)
async def tools_manifest():
    """Sacred Tools Manifest — interactive tool selector for SacredSpace OS."""
    html_path = _os.path.join(_os.path.dirname(__file__), "static", "tools-manifest.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/image-pipeline")
async def image_pipeline_status():
    """Sacred image pipeline status — [IMG-PIPE-001]."""
    import sqlite3
    db_path = "/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/sacred_memory.db"
    try:
        db = sqlite3.connect(db_path)
        cur = db.execute("""
            SELECT
                COUNT(*) as total,
                SUM(pod_ready) as pod_ready,
                SUM(social_queued) as social_queued,
                SUM(comfyui_copied) as comfyui_copied,
                SUM(lore_written) as lore_written
            FROM image_catalog
        """)
        row = cur.fetchone()
        db.close()
        return {
            "status": "active",
            "ref": "IMG-PIPE-001",
            "pillar": "07_SOCIAL_MOTHERSHIP",
            "script": "07_SOCIAL_MOTHERSHIP/CREATION_LAB/sacred_image_pipeline.py",
            "stats": {
                "total": row[0] or 0,
                "pod_ready": row[1] or 0,
                "social_queued": row[2] or 0,
                "comfyui_copied": row[3] or 0,
                "lore_written": row[4] or 0,
            }
        }
    except Exception as e:
        return {"status": "table_not_created_yet", "ref": "IMG-PIPE-001",
                "hint": "Run sacred_image_pipeline.py to create image_catalog table",
                "error": str(e)}

@app.post("/harvest")
async def harvest(background_tasks: BackgroundTasks):
    background_tasks.add_task(trigger_harvest)
    return {"status": "harvest queued"}

# ─── HERMES AGENT v0.13.0 — MCP MOUNT ────────────────────────────────────────
try:
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location(
        "hermes_mcp",
        "/mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/hermes/hermes_mcp.py",
    )
    _mod = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    _hermes_mcp = _mod.mcp
    app.mount("/mcp", _hermes_mcp.sse_app())

    @app.get("/hermes/health")
    async def _hermes_health():
        from fastapi.responses import JSONResponse
        from datetime import datetime
        return JSONResponse({
            "hermes": "0.13.0",
            "status": "operational",
            "mcp": "/mcp",
            "timestamp": datetime.now().isoformat(),
        })

    @app.get("/hermes/tools")
    async def _hermes_tools():
        from fastapi.responses import JSONResponse
        tools = [
            "vault_query", "obsidian_read", "obsidian_write", "obsidian_search",
            "agent_invoke", "hermes_route", "grama_encode", "grama_skry",
            "memory_store", "memory_recall", "pillar_status", "handoff_generate",
        ]
        return JSONResponse({"tools": tools, "count": len(tools)})

    print("[HERMES v0.13.0] ✓ Mounted at /mcp")
except Exception as _e:
    print(f"[HERMES] Mount failed: {_e}")
    import traceback; traceback.print_exc()
# ──────────────────────────────────────────────────────────────────────────────

# ─── EREBAT — DURABLE EXECUTION LOG ──────────────────────────────────────────
try:
    import importlib.util as _ilu_e
    _spec_e = _ilu_e.spec_from_file_location(
        "hermes_erebat",
        "/mnt/d/SacredSpace_OS/06_AGENT_LAYER/erebat/hermes_erebat.py",
    )
    _mod_e = _ilu_e.module_from_spec(_spec_e)
    _spec_e.loader.exec_module(_mod_e)
    _mod_e.register_erebat_routes(app)
    print("[EREBAT] ✓ Crash-recovery routes mounted at /erebat/*")
except Exception as _ee:
    print(f"[EREBAT] Mount skipped: {_ee}")
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
