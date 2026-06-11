from fastapi import APIRouter
from pydantic import BaseModel
import subprocess, json, os
from app.config import SACRED_ROOT

router = APIRouter(prefix="/hermes", tags=["hermes"])

@router.get("/status")
async def hermes_status():
    hermes_path = f"{SACRED_ROOT}/06_AGENT_LAYER/hermes"
    return {
        "path": hermes_path,
        "exists": os.path.isdir(hermes_path),
        "version": "v0.15.0"
    }
