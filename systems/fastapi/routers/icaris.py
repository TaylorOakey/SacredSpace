"""ICARIS Quartet router — signal intake & dispatch"""
from fastapi import APIRouter
from pydantic import BaseModel
router = APIRouter()

AGENTS = {
    "ELIAS":  {"role": "knowledge_distillation", "pillar": "LEARNING"},
    "AURORA": {"role": "code_generation",        "pillar": "CREATION"},
    "ASHER":  {"role": "entropy_detection",      "pillar": "SYSTEMS"},
    "IRIS":   {"role": "vault_watching",         "pillar": "ARCHIVE"},
}

class Signal(BaseModel):
    content: str
    context: str = ""

@router.get("/agents")
async def list_agents():
    return AGENTS

@router.post("/dispatch")
async def dispatch(signal: Signal):
    text = signal.content.lower()
    if any(w in text for w in ["code","build","generate","script"]):
        agent = "AURORA"
    elif any(w in text for w in ["learn","study","research","explain"]):
        agent = "ELIAS"
    elif any(w in text for w in ["error","chaos","broken","fix","entropy"]):
        agent = "ASHER"
    else:
        agent = "IRIS"
    return {
        "signal":    signal.content,
        "routed_to": agent,
        "agent":     AGENTS[agent],
        "sigil":     "∆∆∆ SIGNAL RECEIVED ∆∆∆"
    }
