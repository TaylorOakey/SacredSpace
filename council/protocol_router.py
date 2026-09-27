import json
from datetime import datetime
from pathlib import Path

KEYWORDS = {
    "systems": ["code", "build", "api", "fastapi", "bridge", "agent"],
    "archive": ["memory", "recall", "store", "save", "log"],
    "creation": ["art", "story", "design", "jenga"],
    "lineage": ["iris", "asher", "family", "legacy"]
}

def route(signal):
    signal_low = signal.lower()
    target_pillar = "core"
    for pillar, keys in KEYWORDS.items():
        if any(k in signal_low for k in keys):
            target_pillar = pillar
            break
    
    result = {
        "signal": signal,
        "pillar": target_pillar,
        "seat": "CHATGPT" if target_pillar == "systems" else "CLAUDE",
        "timestamp": datetime.now().isoformat()
    }
    
    # Log to session-logs
    log_path = Path("D:/SacredSpace_OS/council/session-logs/routes.jsonl")
    with open(log_path, "a") as f:
        f.write(json.dumps(result) + "\n")
    
    return result
