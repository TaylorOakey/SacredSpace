"""SACREDSPACE OS — FastAPI Spine v1.0
Canonical root: /mnt/d/SacredSpace_OS
Port: 8888
In lakesh alakin. D
"""

import os, sys

expected = os.path.join(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"), "systems", "fastapi")
if os.path.abspath(os.getcwd()) != os.path.abspath(expected):
    os.chdir(expected)
    sys.path.insert(0, expected)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import health, memory, pillars, vault, hermes, inference, sigil
from app.api.routers.mcp_server import router as mcp_router

app = FastAPI(
    title="SACREDSPACE OS",
    description="Nine-pillar knowledge OS — FastAPI spine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(memory.router)
app.include_router(pillars.router)
app.include_router(vault.router)
app.include_router(hermes.router)
app.include_router(inference.router)
app.include_router(mcp_router)
app.include_router(sigil.router)

@app.get("/")
async def root():
    return {
        "system": "SACREDSPACE OS",
        "version": "1.0.0",
        "status": "live",
        "docs": "/docs",
        "canon": "In lakesh alakin. D"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8888, reload=True)
