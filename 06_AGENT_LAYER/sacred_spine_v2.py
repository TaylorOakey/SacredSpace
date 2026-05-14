#!/usr/bin/env python3
"""sacred_spine_v2.py — FastAPI Spine v2 :: SacredSpace OS Central API
Pillar: 06_AGENT_LAYER | Owner: AURORA | Status: Active
Port: 8888
"""
import json
import requests
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from agent_core import CouncilGrove, AGENTS, ddg_search
    _GROVE = True
except ImportError:
    _GROVE = False

OLLAMA_URL = "http://192.168.240.1:11434"

app = FastAPI(
    title="SacredSpace OS — Sacred Spine v2",
    description="Central API for the 9-pillar OS. Zero-cost. Open-source.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

grove = CouncilGrove() if _GROVE else None


# ∆ MODELS

class InvokeRequest(BaseModel):
    query: str
    agent: Optional[str] = None
    stream: bool = False

class LoreRequest(BaseModel):
    lore: str
    style: Optional[str] = "product listing"

class SearchRequest(BaseModel):
    query: str
    max_results: int = 5


# ∆ HEALTH

@app.get("/")
def root():
    return {"status": "∆ Sacred Spine v2 is alive", "timestamp": datetime.now().isoformat()}

@app.get("/health")
def health():
    ollama_ok = False
    models = []
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        ollama_ok = True
    except Exception:
        pass
    return {
        "spine":  "v2",
        "ollama": ollama_ok,
        "models": models,
        "grove":  _GROVE,
        "timestamp": datetime.now().isoformat(),
    }


# ∆ COUNCIL GROVE

@app.post("/api/grove/invoke")
def invoke_agent(req: InvokeRequest):
    if not grove:
        raise HTTPException(500, "agent_core not loaded")
    result = grove.dispatch(req.query, agent=req.agent, stream=False)
    return result

@app.get("/api/grove/agents")
def list_agents():
    return {name: {"model": cfg["model"], "role": cfg["role"]}
            for name, cfg in AGENTS.items()}


# ∆ LORE-TO-PRODUCT ENGINE

@app.post("/api/lore/to-product")
def lore_to_product(req: LoreRequest):
    prompt = (
        f"You are a sacred marketplace copywriter for SacredSpace OS.\n"
        f"Convert this lore into a compelling {req.style}.\n"
        f"Include: title, description (2-3 sentences), price suggestion, tags.\n"
        f"Format as JSON.\n\n"
        f"LORE:\n{req.lore}"
    )
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": "llama3.1:8b", "prompt": prompt, "stream": False},
            timeout=60,
        )
        resp.raise_for_status()
        raw = resp.json().get("response", "")
        # attempt to extract JSON block
        match = __import__("re").search(r"\{.*\}", raw, __import__("re").DOTALL)
        if match:
            return {"product": json.loads(match.group()), "raw": raw}
        return {"product": None, "raw": raw}
    except Exception as e:
        raise HTTPException(500, str(e))


# ∆ ELIAS SEARCH

@app.post("/api/search")
def web_search(req: SearchRequest):
    results = ddg_search(req.query, req.max_results) if _GROVE else []
    return {"query": req.query, "results": results}


# ∆ OLLAMA PASSTHROUGH

@app.get("/api/models")
def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        return r.json()
    except Exception as e:
        raise HTTPException(503, f"Ollama unreachable: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("sacred_spine_v2:app", host="0.0.0.0", port=8888, reload=True)
