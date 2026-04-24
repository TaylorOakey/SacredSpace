"""Memory Mote router — RAW / DISTILLED / CANON tiers"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Literal
import sqlite3, json, time, uuid

router = APIRouter()
DB = "D:/SacredSpace_OS/archive/memory-motes/sacred.db"

class MemoryMote(BaseModel):
    content:   str
    pillar:    str
    tier:      Literal["RAW", "DISTILLED", "CANON"] = "RAW"
    agent:     str = "SYSTEM"
    sigil_tag: str = ""

@router.post("/mote")
async def store_mote(mote: MemoryMote):
    mote_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO memory_motes VALUES (?,?,?,?,?,?,?)",
        (mote_id, mote.content, mote.pillar, mote.tier,
         mote.agent, mote.sigil_tag, int(time.time()))
    )
    conn.commit(); conn.close()
    return {"id": mote_id, "status": "stored", "tier": mote.tier}

@router.get("/motes")
async def list_motes(pillar: str = None, tier: str = None):
    conn = sqlite3.connect(DB)
    q = "SELECT * FROM memory_motes WHERE 1=1"
    params = []
    if pillar: q += " AND pillar=?";  params.append(pillar)
    if tier:   q += " AND tier=?";    params.append(tier)
    rows = conn.execute(q, params).fetchall()
    conn.close()
    cols = ["id","content","pillar","tier","agent","sigil_tag","ts"]
    return [dict(zip(cols, r)) for r in rows]
