"""Sacred Sigil Terminal — FastAPI Router
Mount at /api/sigil/*
In lakesh alakin. ∆
"""
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services import sigil_terminal_backend
from app.services import weaver_engine

router = APIRouter(prefix="/api/sigil", tags=["sigil"])


# ── Request/Response Models ──────────────────────────────────────────────

class QueryRequest(BaseModel):
    query: str
    dimension: Optional[str] = None
    limit: int = 10


class ExplainRequest(BaseModel):
    query: str
    result: Optional[dict] = None


class SpellRequest(BaseModel):
    spell_id: str
    params: Optional[dict] = None


# ── Status ──────────────────────────────────────────────────────────────

@router.get("/status")
async def sigil_status():
    """Terminal health + dimension status."""
    dims = sigil_terminal_backend.get_dimensions()
    return {
        "status": "live",
        "terminal": "Sacred Sigil Terminal v2.0",
        "dimensions": len(dims),
        "dimension_list": list(dims.keys()),
        "canon": "In lakesh alakin. ∆",
    }


# ── Dimensions ──────────────────────────────────────────────────────────

@router.get("/dimensions")
async def list_dimensions():
    """List all 9 dimensions with metadata."""
    dims = sigil_terminal_backend.get_dimensions()
    return {
        "dimensions": [{"id": k, **v} for k, v in dims.items()],
        "total": len(dims),
    }


# ── Query ────────────────────────────────────────────────────────────────

@router.post("/query")
async def sigil_query(req: QueryRequest):
    """Execute a sigil query across one or all dimensions."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    if req.dimension and req.dimension != "all":
        result = sigil_terminal_backend.query_dimension(req.dimension, req.query, req.limit)
    else:
        result = sigil_terminal_backend.cross_dimension_search(req.query, req.limit)

    # Auto-record to history
    sigil_terminal_backend.record_query(
        query=req.query,
        dimension=req.dimension or "all",
        result_count=result.get("total", 0),
        source="api",
    )
    # Track queries_cast in profile
    weaver_engine.update_profile("queries_cast", 1)

    return result


# ── Explain ──────────────────────────────────────────────────────────────

@router.post("/explain")
async def sigil_explain(req: ExplainRequest):
    """Explain a sigil query result with context."""
    prompt = f"Explain the following sigil query and its significance: '{req.query}'"
    if req.result:
        prompt += f"\nResult context: {json.dumps(req.result, indent=2)[:500]}"

    explanation = weaver_engine._ollama_infer(prompt)
    return {
        "query": req.query,
        "explanation": explanation.get("response", "No explanation available."),
        "source": explanation.get("source", "fallback"),
    }


# ── Spells ────────────────────────────────────────────────────────────────

@router.get("/spells")
async def list_spells():
    """List all available sigil spells."""
    spells = weaver_engine.get_spells()
    return {
        "spells": [{"id": k, **v} for k, v in spells.items()],
        "total": len(spells),
    }


@router.post("/execute-spell")
async def execute_spell(req: SpellRequest):
    """Execute a sigil spell."""
    result = weaver_engine.execute_spell(req.spell_id, req.params or {})
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "Spell execution failed"))
    return result


# ── History ──────────────────────────────────────────────────────────────────

@router.get("/history")
async def sigil_history(limit: int = 20):
    """Return recent sigil query history."""
    history = sigil_terminal_backend.get_query_history(limit)
    return {"history": history, "total": len(history)}


# ── Profile ──────────────────────────────────────────────────────────────────

@router.get("/profile")
async def sigil_profile():
    """Return the sigil caster profile (resonance, xp, insight, level)."""
    profile = weaver_engine.get_profile()
    return {"profile": profile}
