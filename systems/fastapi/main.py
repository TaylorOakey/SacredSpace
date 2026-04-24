"""SacredSpace OS — FastAPI Spine v2.0"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import memory, pillars, icaris

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

app.include_router(memory.router,  prefix="/memory",  tags=["Memory"])
app.include_router(pillars.router, prefix="/pillars", tags=["Pillars"])
app.include_router(icaris.router,  prefix="/icaris",  tags=["ICARIS"])

@app.get("/")
async def root():
    return {"status": "LIVE", "sigil": "∆∆∆ SACREDSPACE OS ∆∆∆"}

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0"}
