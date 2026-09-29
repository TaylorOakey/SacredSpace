"""
council_grove_runner.py
SacredSpace OS | 02_COUNCIL_GROVE
Executes the Claude seat in CODE MODE for Council Grove sessions.
Reads context, queries memory, generates input, writes to session file.
"""

import sys
import json
import sqlite3
import datetime
import requests
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────
SACREDSPACE_ROOT = Path(r"D:\SacredSpace_OS")
SESSIONS_DIR     = SACREDSPACE_ROOT / "02_COUNCIL_GROVE" / "sessions"
CODEX_DIR        = SACREDSPACE_ROOT / "04_SACRED_CODEX"
CLAUDE_MD        = SACREDSPACE_ROOT / "CLAUDE.md"
FASTAPI_BASE     = "http://localhost:8888"
SQLITE_DB        = SACREDSPACE_ROOT / "05_MEMORY_ENGINE" / "sacred_memory.db"

SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


# ── Context Loading ────────────────────────────────────────────────────────────
def load_claude_md(max_lines: int = 60) -> str:
    try:
        lines = CLAUDE_MD.read_text(encoding="utf-8").splitlines()[:max_lines]
        return "\n".join(lines)
    except FileNotFoundError:
        return "[CLAUDE.md not found]"


def query_pillar_health() -> dict:
    try:
        resp = requests.get(f"{FASTAPI_BASE}/pillars", timeout=3)
        return resp.json()
    except Exception as e:
        return {"error": str(e), "status": "FastAPI unreachable — stack may be down"}


def load_recent_codex_entries(n: int = 5) -> list[str]:
    try:
        entries = sorted(
            CODEX_DIR.rglob("*.md"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )[:n]
        return [str(e.relative_to(SACREDSPACE_ROOT)) for e in entries]
    except Exception:
        return ["[Codex scan failed]"]


def query_memory_engine(topic_keywords: str) -> list[dict]:
    results = []
    try:
        conn = sqlite3.connect(str(SQLITE_DB))
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM memory_motes "
            "WHERE content LIKE ? ORDER BY created_at DESC LIMIT 3",
            (f"%{topic_keywords}%",)
        )
        for row in cursor.fetchall():
            results.append({"id": row[0], "content": row[1][:200], "created_at": row[2]})
        conn.close()
    except Exception as e:
        results.append({"error": str(e)})
    return results


# ── Claude Seat Input Generator ───────────────────────────────────────────────
def generate_claude_seat_input(session_topic: str, session_id: str) -> dict:
    prompt = f"""You are the Claude seat in a SacredSpace Council Grove session.
Role: Reasoning and Narrative.
Operating mantra: Ground. Consolidate. Deploy. Document. Repeat.
Canon is immutable — your output is DISTILLED, not canon.

Session topic: {session_topic}

Provide:
1. Core reasoning on the question
2. Narrative or symbolic thread if present
3. Tensions or unresolved logic
4. One clear Reasoning Verdict
5. Suggested next build step (pillar-tagged, specific)
6. Any canon conflicts detected

Be direct. Flag canon candidates — do not make canon decisions."""

    try:
        resp = requests.post(
            f"{FASTAPI_BASE}/icaris",
            json={"agent": "CLAUDE_SEAT", "prompt": prompt},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
    except Exception:
        pass

    try:
        resp = requests.post(
            "http://192.168.240.1:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False},
            timeout=60
        )
        if resp.status_code == 200:
            return {"content": resp.json().get("response", ""), "source": "ollama"}
    except Exception:
        pass

    return {
        "content": "[LLM unreachable — manual input required for Claude seat]",
        "source": "fallback"
    }


# ── Session File Writer ───────────────────────────────────────────────────────
def write_session_file(session_id: str, payload: dict) -> Path:
    session_file = SESSIONS_DIR / f"{session_id}.md"
    timestamp = datetime.datetime.now().isoformat()

    block = f"""
## [CLAUDE — Reasoning / Narrative] — CODE MODE
Generated: {timestamp}
Context Loaded: {json.dumps(payload.get('context_loaded', {}), indent=2)}

Topic: {payload.get('topic', session_id)}
Input:
{payload.get('content', '[No content generated]')}

Reasoning Verdict: {payload.get('verdict', '[See input above]')}
Suggested Next Build Step: {payload.get('next_step', '[See input above]')}
Canon Conflict Flags: {payload.get('canon_conflicts', 'NONE')}
Source: {payload.get('source', 'unknown')}
---
"""
    with open(session_file, "a", encoding="utf-8") as f:
        f.write(block)
    return session_file


def post_to_memory_engine(session_id: str, content: str) -> None:
    try:
        requests.post(
            f"{FASTAPI_BASE}/memory",
            json={
                "source": "council_grove_runner",
                "session_id": session_id,
                "content": content[:1000],
                "tags": ["council", "claude_seat", "code_mode"]
            },
            timeout=5
        )
    except Exception:
        pass


# ── Main Entry ────────────────────────────────────────────────────────────────
def run(session_id: str, session_topic: str, topic_keywords: str = "") -> None:
    print(f"\n{'═'*60}")
    print(f"  CLAUDE SEAT — CODE MODE")
    print(f"  Session: {session_id}")
    print(f"{'═'*60}\n")

    print("[1/5] Loading context files...")
    claude_md_snippet = load_claude_md()
    pillar_health     = query_pillar_health()
    codex_entries     = load_recent_codex_entries()
    memory_motes      = query_memory_engine(topic_keywords or session_topic[:30])

    context_loaded = {
        "claude_md_lines": claude_md_snippet[:200] + "...",
        "pillar_health": pillar_health,
        "recent_codex": codex_entries,
        "memory_motes_found": len(memory_motes),
        "memory_sample": memory_motes[:2]
    }
    print(f"  Pillar health: {pillar_health}")
    print(f"  Recent codex entries: {codex_entries}")
    print(f"  Memory motes matched: {len(memory_motes)}\n")

    print("[2/5] Generating Claude seat reasoning...")
    llm_result = generate_claude_seat_input(session_topic, session_id)
    llm_result["context_loaded"] = context_loaded
    llm_result["topic"] = session_topic
    print(f"  Source: {llm_result.get('source', 'unknown')}\n")

    print("[3/5] Writing to session file...")
    session_file = write_session_file(session_id, llm_result)
    print(f"  Written: {session_file}\n")

    print("[4/5] Posting to Memory Engine...")
    post_to_memory_engine(session_id, str(llm_result.get("content", "")))
    print("  Done.\n")

    print("[5/5] CLAUDE SEAT OUTPUT:")
    print(f"{'─'*60}")
    print(llm_result.get("content", "[No content]"))
    print(f"{'─'*60}")
    print(f"\n  Session file: {session_file}")
    print(f"  In lakesh alakin. ∆.\n")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python council_grove_runner.py <SESSION_ID> <TOPIC> [KEYWORDS]")
        print("Example: python council_grove_runner.py CG-2026-05-19-001 'MCP endpoint layer design' 'MCP FastAPI'")
        sys.exit(1)

    sid     = sys.argv[1]
    topic   = sys.argv[2]
    kwords  = sys.argv[3] if len(sys.argv) > 3 else ""
    run(sid, topic, kwords)
