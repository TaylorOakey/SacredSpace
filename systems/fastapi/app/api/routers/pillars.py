from fastapi import APIRouter
from app.config import SACRED_ROOT, NINE_PILLARS
import os

router = APIRouter(prefix="/pillars", tags=["pillars"])

@router.get("/status")
async def pillars_status():
    result = {}
    for p in NINE_PILLARS:
        path = f"{SACRED_ROOT}/{p}"
        if os.path.isdir(path):
            files = sum(len(f) for _, _, f in os.walk(path))
            result[p] = {"exists": True, "files": files}
        else:
            result[p] = {"exists": False, "files": 0}
    return result
