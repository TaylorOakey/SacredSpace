from fastapi import APIRouter
from app.config import SACRED_ROOT, OLLAMA_BASE, NINE_PILLARS
import os, httpx

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def health():
    return {
        "status": "live",
        "sacred_root": SACRED_ROOT,
        "pillars_on_disk": [p for p in NINE_PILLARS if os.path.isdir(f"{SACRED_ROOT}/{p}")]
    }

@router.get("/ollama")
async def ollama_status():
    try:
        async with httpx.AsyncClient(timeout=3) as c:
            r = await c.get(f"{OLLAMA_BASE}/api/tags")
            return {"status": "online", "models": [m["name"] for m in r.json().get("models", [])]}
    except Exception as e:
        return {"status": "offline", "error": str(e)}
