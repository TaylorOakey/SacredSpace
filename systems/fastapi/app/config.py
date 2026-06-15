"""SacredSpace OS — FastAPI Spine Configuration"""

import os

SACRED_ROOT = os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS")

def _detect_ollama():
    override = os.environ.get("OLLAMA_BASE")
    if override:
        return override
    # WSL2: Ollama runs on Windows host — read gateway from /etc/resolv.conf
    try:
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    ip = line.split()[1].strip()
                    return f"http://{ip}:11434"
    except Exception:
        pass
    return "http://localhost:11434"

OLLAMA_BASE = _detect_ollama()
OBSIDIAN_REST = os.environ.get("OBSIDIAN_REST", "http://localhost:27123")
OBSIDIAN_API_KEY = os.environ.get("OBSIDIAN_API_KEY", "")
CHROMA_PATH = os.environ.get("CHROMA_PATH", f"{SACRED_ROOT}/06_AGENTS/IRIS/chroma_db")
SQLITE_PATH = os.environ.get("SQLITE_PATH", f"{SACRED_ROOT}/05_MEMORY/sacred_memory.db")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

NINE_PILLARS = [
    "01_CORE", "02_SYSTEMS", "03_NEURAL",
    "04_CODEX", "05_MEMORY", "06_AGENTS",
    "07_SOCIAL", "08_LEARNING", "09_MARKET"
]
