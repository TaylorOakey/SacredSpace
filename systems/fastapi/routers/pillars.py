"""Pillar status router"""
from fastapi import APIRouter
router = APIRouter()

PILLARS = ["CORE","SYSTEMS","LEARNING","ECONOMY",
           "HABITAT","CREATION","COUNCIL","LINEAGE","ARCHIVE"]

@router.get("/")
async def list_pillars():
    return {"pillars": PILLARS, "count": len(PILLARS)}

@router.get("/{name}")
async def get_pillar(name: str):
    name = name.upper()
    if name not in PILLARS:
        return {"error": f"{name} not in canon"}
    return {"pillar": name, "status": "ACTIVE", "sigil": "∆∆∆"}
