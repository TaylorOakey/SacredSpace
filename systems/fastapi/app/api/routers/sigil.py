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
from app.services import sigil_grammar
from app.services import story_engine
from app.db import get_sqlite

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


class MacroCreateRequest(BaseModel):
    name: str
    composition: str
    description: str = ""
    agent: str = "CUSTOM"


class MacroDeleteRequest(BaseModel):
    id: int


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

    # Auto-parse sigil strings: if query looks like a sigil, return grammar info
    grammar_info = None
    sigil_parsed = sigil_grammar.parse(req.query)
    if sigil_parsed and not sigil_parsed.errors and len(req.query) < 100:
        grammar_info = {
            "parsed": sigil_parsed.to_dict(),
            "cost": sigil_grammar.calculate_cost(sigil_parsed),
            "description": sigil_grammar.describe_sigil(sigil_parsed),
        }
    if grammar_info:
        result["sigil_grammar"] = grammar_info

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


# ── Grammar Parser ─────────────────────────────────────────────────────────────

class ParseRequest(BaseModel):
    sigil: str

class GrammarLintRequest(BaseModel):
    sigil: str

@router.post("/grammar/parse")
async def grammar_parse(req: ParseRequest):
    """Parse a sigil string into its structured components."""
    parsed = sigil_grammar.parse(req.sigil)
    cost = sigil_grammar.calculate_cost(parsed)
    return {
        "parsed": parsed.to_dict(),
        "cost": cost,
        "description": sigil_grammar.describe_sigil(parsed),
    }


@router.post("/grammar/lint")
async def grammar_lint(req: GrammarLintRequest):
    """Lint a sigil string for validity and affinity warnings."""
    result = sigil_grammar.lint(req.sigil)
    return result


@router.get("/grammar/library")
async def grammar_library():
    """Return the full grammar reference."""
    lib = sigil_grammar.get_library()
    # Also include any custom macros
    lib["all_macros"] = sigil_grammar.get_all_macros()
    return lib


@router.get("/grammar/spell-cost/{spell_id}")
async def grammar_spell_cost(spell_id: str):
    """Return grammar-engineered cost breakdown for a spell."""
    cost = weaver_engine.calculate_spell_resonance(spell_id)
    composition = weaver_engine.get_spell_composition(spell_id)
    if composition:
        parsed = sigil_grammar.parse(composition)
        return {
            "spell_id": spell_id,
            "composition": composition,
            "parsed": parsed.to_dict(),
            "cost": cost,
        }
    return {"spell_id": spell_id, "error": "No composition found"}


# ── Custom Macros ─────────────────────────────────────────────────────────────

@router.get("/macros")
async def list_custom_macros():
    """List all macros (built-in + custom)."""
    conn = get_sqlite()
    sigil_grammar.load_custom_macros(conn)
    conn.close()
    all_macros = sigil_grammar.get_all_macros()
    return {
        "macros": [{"id": k, **v} for k, v in all_macros.items()],
        "total": len(all_macros),
    }


@router.post("/macro")
async def create_custom_macro(req: MacroCreateRequest):
    """Create a custom sigil macro."""
    if not req.name.strip():
        raise HTTPException(status_code=400, detail="Macro name is required")
    if not req.composition.strip():
        raise HTTPException(status_code=400, detail="Sigil composition is required")
    
    # Validate composition
    parsed = sigil_grammar.parse(req.composition)
    if parsed.errors:
        raise HTTPException(status_code=400, detail=f"Invalid composition: {'; '.join(parsed.errors)}")
    
    conn = get_sqlite()
    sigil_grammar.load_custom_macros(conn)
    macro = sigil_grammar.add_custom_macro(conn, req.name, req.composition, req.description, req.agent)
    conn.close()
    return macro


@router.delete("/macro/{macro_id}")
async def remove_custom_macro(macro_id: int):
    """Delete a custom sigil macro (soft-delete)."""
    conn = get_sqlite()
    sigil_grammar.load_custom_macros(conn)
    deleted = sigil_grammar.delete_custom_macro(conn, macro_id)
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Custom macro #{macro_id} not found")
    return {"deleted": True, "macro_id": macro_id}


# ── Story ─────────────────────────────────────────────────────────────────────

@router.get("/story")
async def story_index():
    """Master story index — Jenga's Journey Season 1."""
    return story_engine.get_story_index()


@router.get("/story/characters")
async def story_characters(search: Optional[str] = None):
    """List all storyline characters."""
    chars = story_engine.get_characters(search)
    return {"characters": chars, "total": len(chars)}


@router.get("/story/characters/{character_id}")
async def story_character(character_id: str):
    """Get a single character by ID."""
    char = story_engine.get_character(character_id)
    if not char:
        raise HTTPException(status_code=404, detail=f"Character '{character_id}' not found")
    return char


@router.get("/story/nodes")
async def story_nodes(search: Optional[str] = None):
    """List all sacred game nodes."""
    nodes = story_engine.get_nodes(search)
    return {"nodes": nodes, "total": len(nodes)}


@router.get("/story/nodes/{node_id}")
async def story_node(node_id: str):
    """Get a single node by ID."""
    node = story_engine.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail=f"Node '{node_id}' not found")
    return node


@router.get("/story/episodes")
async def story_episodes(search: Optional[str] = None):
    """List all episodes of Jenga's Journey."""
    episodes = story_engine.get_episodes(search)
    return {"episodes": episodes, "total": len(episodes)}


@router.get("/story/episodes/{episode_number}")
async def story_episode(episode_number: int):
    """Get a single episode by number."""
    ep = story_engine.get_episode(episode_number)
    if not ep:
        raise HTTPException(status_code=404, detail=f"Episode {episode_number} not found")
    return ep


@router.get("/story/archetypes")
async def story_archetypes(search: Optional[str] = None):
    """List all major arcana archetypes."""
    archetypes = story_engine.get_archetypes(search)
    return {"archetypes": archetypes, "total": len(archetypes)}


@router.get("/story/schools")
async def story_schools(search: Optional[str] = None):
    """List all magical schools."""
    schools = story_engine.get_schools(search)
    return {"schools": schools, "total": len(schools)}
