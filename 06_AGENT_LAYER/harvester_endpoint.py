"""
council/harvester_endpoint.py
FastAPI route: POST /council/harvester/ingest
Bridges the Node UI Harvester Terminal → sacred_harvester.py engine.

Mount in your main FastAPI app:
    from council.harvester_endpoint import router as harvester_router
    app.include_router(harvester_router, prefix="/council")
"""

from fastapi import APIRouter, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional
import sys
import os

# Add parent directory to path so sacred_harvester is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sacred_harvester import SacredHarvester, SIGNAL_TYPES

router = APIRouter()

# ── Shared harvester instance (one DB connection per worker)
_harvester = None

def get_harvester() -> SacredHarvester:
    global _harvester
    if _harvester is None:
        _harvester = SacredHarvester()
    return _harvester


# ── Request / Response models ────────────────────

class HarvestRequest(BaseModel):
    url: HttpUrl
    signal_type: Optional[str] = None

class HarvestResponse(BaseModel):
    signal_id: str
    signal_type: str
    source_url: str
    title: str
    core_value: str
    pillar_path: str
    pillar_tags: list[str]
    confidence_score: float
    content_hash: str
    status: str
    next_action: str
    scrape_timestamp: str
    obsidian_file: str


# ── Routes ───────────────────────────────────────

@router.post("/harvester/ingest", response_model=HarvestResponse)
async def ingest_signal(req: HarvestRequest):
    """
    Trigger the full harvest ritual for a given URL.
    Called by the Node UI Harvester Terminal.
    """
    if req.signal_type and req.signal_type not in SIGNAL_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown signal_type: {req.signal_type}. Valid: {list(SIGNAL_TYPES.keys())}"
        )

    harvester = get_harvester()
    signal = harvester.harvest(str(req.url), req.signal_type or None)

    if signal is None:
        raise HTTPException(
            status_code=422,
            detail="Harvest failed — ethics gate, quality gate, or duplicate content."
        )

    obsidian_file = f"SIGNAL_{signal['signal_id'].replace('-', '_')}.md"

    return HarvestResponse(
        **{k: v for k, v in signal.items() if k != "raw_text_preview"},
        obsidian_file=obsidian_file
    )


@router.get("/harvester/status")
async def harvester_status():
    """Health check — also confirms the harvester is initialized."""
    return {
        "agent":  "∆SSH∆ SacredSignal Harvester",
        "status": "ONLINE",
        "version": "1.0",
    }


@router.get("/harvester/signal_types")
async def list_signal_types():
    """Return all valid signal types and their pillar paths."""
    return {"signal_types": SIGNAL_TYPES}
