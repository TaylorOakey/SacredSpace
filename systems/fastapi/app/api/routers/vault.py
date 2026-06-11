from fastapi import APIRouter
from app.config import OBSIDIAN_REST, OBSIDIAN_API_KEY
import httpx

router = APIRouter(prefix="/vault", tags=["vault"])

@router.get("/status")
async def vault_status():
    try:
        headers = {}
        if OBSIDIAN_API_KEY:
            headers["Authorization"] = f"Bearer {OBSIDIAN_API_KEY}"
        async with httpx.AsyncClient(timeout=3) as c:
            r = await c.get(f"{OBSIDIAN_REST}/vault/", headers=headers)
            return {"status": "online", "files": len(r.json().get("files", []))}
    except Exception as e:
        return {"status": "offline", "error": str(e)}

@router.get("/search")
async def vault_search(query: str):
    try:
        headers = {}
        if OBSIDIAN_API_KEY:
            headers["Authorization"] = f"Bearer {OBSIDIAN_API_KEY}"
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.post(f"{OBSIDIAN_REST}/search/simple/",
                            params={"query": query}, headers=headers)
            return {"results": r.json()}
    except Exception as e:
        return {"error": str(e)}
