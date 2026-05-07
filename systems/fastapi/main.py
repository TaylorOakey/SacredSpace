"""SacredSpace OS — FastAPI Spine v2.0"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from routers import memory, pillars, icaris, inference
from kethras      import router as kethras_router,   init_kethras_db
from merchant     import router as merchant_router,   init_merchant_db
from vault_watcher import router as vault_router,     init_vault_watcher, trigger_harvest
from lore_engine  import router as lore_router,       init_lore_engine
from reconcile    import reconcile

log = logging.getLogger("spine")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ── Startup ───────────────────────────────────────────────
    init_kethras_db()
    init_merchant_db()
    init_vault_watcher()
    init_lore_engine()

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


@app.get("/")
async def root():
    return {
        "spine":     "systems/fastapi/main.py:8888",
        "status":    "LIVE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agents":    ["ELIAS", "AURORA", "ASHER", "IRIS"],
        "cascade":   ["ollama", "gemini", "mock"],
        "seal":      "∆∆∆ In lakesh alakin ∆∆∆",
    }

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

@app.post("/harvest")
async def harvest(background_tasks: BackgroundTasks):
    background_tasks.add_task(trigger_harvest)
    return {"status": "harvest queued"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
