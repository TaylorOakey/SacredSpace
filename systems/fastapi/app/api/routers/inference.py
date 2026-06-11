from fastapi import APIRouter
from pydantic import BaseModel
from app.config import OLLAMA_BASE
import httpx

router = APIRouter(prefix="/inference", tags=["inference"])

class InferRequest(BaseModel):
    prompt: str
    model: str = "qwen2.5-coder:7b"
    stream: bool = False

@router.get("/status")
async def inference_status():
    try:
        async with httpx.AsyncClient(timeout=3) as c:
            r = await c.get(f"{OLLAMA_BASE}/api/tags")
            models = [m["name"] for m in r.json().get("models", [])]
            return {"status": "online", "ollama": OLLAMA_BASE, "models": models}
    except Exception as e:
        return {"status": "offline", "ollama": OLLAMA_BASE, "error": str(e)}

@router.post("/complete")
async def complete(req: InferRequest):
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post(f"{OLLAMA_BASE}/api/generate",
                json={"model": req.model, "prompt": req.prompt, "stream": False})
            return {"response": r.json().get("response", ""), "model": req.model}
    except Exception as e:
        return {"error": str(e)}
