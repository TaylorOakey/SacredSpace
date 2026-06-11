from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.db import get_sqlite, get_chroma_client
import json

router = APIRouter(prefix="/memory", tags=["memory"])

class MemoryMote(BaseModel):
    entity: str
    pillar: Optional[str] = None
    content: str
    tags: Optional[str] = None
    status: Optional[str] = "raw"

@router.get("/status")
async def memory_status():
    try:
        conn = get_sqlite()
        count = conn.execute("SELECT COUNT(*) FROM memory_motes").fetchone()[0]
        conn.close()
        chroma = get_chroma_client()
        chroma_status = "online" if chroma else "offline"
        return {"sqlite": "online", "motes": count, "chromadb": chroma_status}
    except Exception as e:
        return {"error": str(e)}

@router.post("/mote")
async def store_mote(mote: MemoryMote):
    try:
        conn = get_sqlite()
        conn.execute(
            "INSERT INTO memory_motes (entity, pillar, content, tags, status) VALUES (?,?,?,?,?)",
            (mote.entity, mote.pillar, mote.content, mote.tags, mote.status)
        )
        conn.commit()
        conn.close()
        return {"status": "stored", "entity": mote.entity}
    except Exception as e:
        raise HTTPException(500, str(e))

@router.get("/motes")
async def list_motes(limit: int = 20):
    conn = get_sqlite()
    rows = conn.execute("SELECT * FROM memory_motes ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
    conn.close()
    return {"motes": [dict(r) for r in rows]}
