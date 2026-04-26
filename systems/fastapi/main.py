"""SacredSpace OS — FastAPI Spine v2.0"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import memory, pillars, icaris

from kethras      import router as kethras_router,   init_kethras_db
from merchant     import router as merchant_router,   init_merchant_db
from vault_watcher import router as vault_router,     init_vault_watcher
from lore_engine  import router as lore_router,       init_lore_engine

app = FastAPI(
    title="SacredSpace OS",
    description="∆∆∆ Architecting the SacredSpace ∆∆∆",
    version="2.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Existing routers ──────────────────────────────────────────
app.include_router(memory.router,  prefix="/memory",  tags=["Memory"])
app.include_router(pillars.router, prefix="/pillars", tags=["Pillars"])
app.include_router(icaris.router,  prefix="/icaris",  tags=["ICARIS"])

# ── New systems ───────────────────────────────────────────────
init_kethras_db()
app.include_router(kethras_router)

init_merchant_db()
app.include_router(merchant_router)

init_vault_watcher()
app.include_router(vault_router)

init_lore_engine()
app.include_router(lore_router)

@app.get("/")
async def root():
    return {"status": "LIVE", "sigil": "∆∆∆ SACREDSPACE OS ∆∆∆"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
