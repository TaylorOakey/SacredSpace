#!/usr/bin/env python3
"""agent_core.py — CouncilGrove Dispatcher :: ICARIS Quartet Router
Pillar: 06_AGENT_LAYER | Owner: ICARIS | Status: Active
"""
import json
import re
import requests
from typing import Optional

OLLAMA_URL = "http://192.168.240.1:11434"

AGENTS = {
    "ELIAS": {
        "model":    "llama3.1:8b",
        "role":     "knowledge, research, lore, DuckDuckGo search",
        "keywords": ["research", "search", "find", "who", "what is", "lore",
                     "explain", "define", "history", "why"],
    },
    "AURORA": {
        "model":    "qwen2.5-coder:7b",
        "role":     "code generation, debugging, FastAPI, Python",
        "keywords": ["code", "write", "build", "debug", "function", "script",
                     "api", "python", "fix", "error", "implement"],
    },
    "ASHER": {
        "model":    "phi3.5",
        "role":     "decay detection, memory pruning, state management",
        "keywords": ["memory", "forget", "prune", "decay", "clean", "state",
                     "archive", "remove", "old", "stale"],
    },
    "IRIS": {
        "model":    "llama3.1:8b",
        "role":     "vault management, YAML, Obsidian, canon structuring",
        "keywords": ["vault", "yaml", "obsidian", "note", "canon", "structure",
                     "file", "organize", "template", "frontmatter"],
    },
}

SYSTEM_PROMPTS = {
    "ELIAS": (
        "You are ELIAS — knowledge agent of the ICARIS Quartet inside SacredSpace OS. "
        "You specialize in research, lore, and information retrieval. "
        "Be precise, cite sources when possible, and return structured answers. "
        "Operator: Taylor (∆∆∆OAK3YTREE∆∆∆). Closing: In Lakesh — Alakin."
    ),
    "AURORA": (
        "You are AURORA — code generation agent of the ICARIS Quartet inside SacredSpace OS. "
        "You specialize in Python, FastAPI, and the zero-cost open-source stack. "
        "Write clean, minimal code. No unnecessary abstractions. "
        "Stack: Python · FastAPI · SQLite · ChromaDB · Ollama · Redis. "
        "Operator: Taylor (∆∆∆OAK3YTREE∆∆∆). Closing: In Lakesh — Alakin."
    ),
    "ASHER": (
        "You are ASHER — decay and memory agent of the ICARIS Quartet inside SacredSpace OS. "
        "You manage what persists, what fades, and what must be archived. "
        "Be clinical, efficient, and decisive about state transitions. "
        "Operator: Taylor (∆∆∆OAK3YTREE∆∆∆). Closing: In Lakesh — Alakin."
    ),
    "IRIS": (
        "You are IRIS — vault and canon agent of the ICARIS Quartet inside SacredSpace OS. "
        "You manage Obsidian vault structure, YAML frontmatter, and canonical definitions. "
        "Output valid YAML and Markdown. Preserve structure above all. "
        "Operator: Taylor (∆∆∆OAK3YTREE∆∆∆). Closing: In Lakesh — Alakin."
    ),
}


def ddg_search(query: str, max_results: int = 5) -> list[dict]:
    """DuckDuckGo instant answer — no API key needed."""
    try:
        resp = requests.get(
            "https://api.duckduckgo.com/",
            params={"q": query, "format": "json", "no_html": 1, "skip_disambig": 1},
            timeout=10,
            headers={"User-Agent": "SacredSpace-ELIAS/2.0"},
        )
        data = resp.json()
        results = []
        if data.get("AbstractText"):
            results.append({"title": data.get("Heading", query),
                            "text": data["AbstractText"],
                            "url": data.get("AbstractURL", "")})
        for r in data.get("RelatedTopics", [])[:max_results]:
            if isinstance(r, dict) and r.get("Text"):
                results.append({"title": r.get("Text", "")[:60],
                                "text": r["Text"],
                                "url": r.get("FirstURL", "")})
        return results[:max_results]
    except Exception as e:
        return [{"error": str(e)}]


def route(query: str) -> str:
    """Score each agent by keyword hits; return highest scorer."""
    query_lower = query.lower()
    scores = {name: 0 for name in AGENTS}
    for name, cfg in AGENTS.items():
        for kw in cfg["keywords"]:
            if kw in query_lower:
                scores[name] += 1
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "AURORA"


def invoke(agent: str, query: str, stream: bool = True) -> str:
    cfg = AGENTS[agent]
    messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[agent]},
        {"role": "user",   "content": query},
    ]
    # ELIAS gets web context prepended
    if agent == "ELIAS" and any(kw in query.lower() for kw in ["search", "find", "latest", "recent"]):
        hits = ddg_search(query)
        if hits and "error" not in hits[0]:
            context = "\n".join(f"- {h['title']}: {h['text']}" for h in hits)
            messages[1]["content"] = f"Web context:\n{context}\n\nQuery: {query}"

    resp = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": cfg["model"], "messages": messages, "stream": stream},
        stream=stream, timeout=180,
    )
    resp.raise_for_status()

    if not stream:
        return resp.json()["message"]["content"]

    tokens = []
    print(f"\n∆ {agent} [{cfg['model']}]\n", flush=True)
    for line in resp.iter_lines():
        if not line:
            continue
        try:
            chunk = json.loads(line)
        except json.JSONDecodeError:
            continue
        token = chunk.get("message", {}).get("content", "")
        if token:
            tokens.append(token)
            print(token, end="", flush=True)
        if chunk.get("done"):
            break
    print()
    return "".join(tokens)


class CouncilGrove:
    """Auto-routing dispatcher for the ICARIS Quartet."""

    def dispatch(self, query: str, agent: Optional[str] = None,
                 stream: bool = True) -> dict:
        selected = agent.upper() if agent else route(query)
        if selected not in AGENTS:
            selected = "AURORA"
        reply = invoke(selected, query, stream=stream)
        return {"agent": selected, "model": AGENTS[selected]["model"],
                "query": query, "reply": reply}


# ∆ CLI
if __name__ == "__main__":
    import sys
    grove = CouncilGrove()
    if len(sys.argv) < 2:
        print("Usage: agent_core.py <query> [--agent ELIAS|AURORA|ASHER|IRIS]")
        sys.exit(0)
    agent_override = None
    args = sys.argv[1:]
    if "--agent" in args:
        idx = args.index("--agent")
        agent_override = args[idx + 1]
        args = args[:idx] + args[idx + 2:]
    query = " ".join(args)
    grove.dispatch(query, agent=agent_override)
