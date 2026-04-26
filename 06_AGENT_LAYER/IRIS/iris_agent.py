"""
iris_agent.py
═══════════════════════════════════════════════════════════════════════════
SacredSpace OS — ICARIS Quartet: IRIS Agent (Vault)
Pillar:      06_AGENT_LAYER
Owner Agent: IRIS
Status:      Canon Draft — smolagents v1.0 boot

Purpose:
    IRIS is the vault agent. She queries the SacredSpace ChromaDB
    vector store, surfaces canon knowledge, and writes structured
    summaries back to the Obsidian vault.

    This boot script demonstrates IRIS running as a smolagents
    CodeAgent — meaning she writes and executes raw Python to
    solve tasks, rather than parsing fragile JSON tool responses.

Stack:
    smolagents + LiteLLM (Ollama bridge) + ChromaDB + python-frontmatter
    100% local, zero-cost, zero data leakage.

Install:
    pip install smolagents[litellm] chromadb python-frontmatter --break-system-packages

Run:
    python3 iris_agent.py

    Or query via FastAPI:
    POST http://127.0.0.1:8888/api/scry
    Body: {"query": "What is the Arcana Grid?"}
═══════════════════════════════════════════════════════════════════════════
"""

import chromadb
import frontmatter
from pathlib import Path
from datetime import datetime

from smolagents import CodeAgent, LiteLLMModel, tool

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

# Ollama model — change to any model you have pulled locally
# Good options: mistral, llama3, phi3, qwen2, deepseek-r1
OLLAMA_MODEL = "ollama_chat/mistral"

# ChromaDB — connects to your running local instance
CHROMA_HOST = "localhost"
CHROMA_PORT = 8000
CHROMA_COLLECTION = "sacredspace_canon"  # adjust to your actual collection name

# Vault paths
VAULT_ROOT = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
IRIS_LOG = Path("/mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/iris_session.log")

IRIS_LOG.parent.mkdir(parents=True, exist_ok=True)

# ─── CHROMADB CLIENT ──────────────────────────────────────────────────────────

chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)

try:
    collection = chroma_client.get_collection(CHROMA_COLLECTION)
    print(f"[IRIS] Connected to ChromaDB collection: {CHROMA_COLLECTION}")
except Exception:
    # If collection doesn't exist yet, create it
    collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION)
    print(f"[IRIS] Created new ChromaDB collection: {CHROMA_COLLECTION}")

# ─── SMOLAGENTS TOOLS ─────────────────────────────────────────────────────────
# These are the Python functions IRIS can call when solving a task.
# smolagents CodeAgent writes Python that calls these directly.

@tool
def query_vault(query: str, n_results: int = 5) -> str:
    """
    Query the SacredSpace ChromaDB vector store for canon knowledge.

    Args:
        query: The semantic search query to run against the vault.
        n_results: Number of results to return (default 5).

    Returns:
        Formatted string of matching canon excerpts with source paths.
    """
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            return "No matching canon entries found for this query."

        output = []
        for i, (doc, meta, dist) in enumerate(
            zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ):
            relevance = round((1 - dist) * 100, 1)
            source = meta.get("source", "unknown")
            pillar = meta.get("pillar", "unknown")
            output.append(
                f"[{i+1}] Source: {source}\n"
                f"    Pillar: {pillar} | Relevance: {relevance}%\n"
                f"    Excerpt: {doc[:400]}...\n"
            )

        return "\n".join(output)

    except Exception as e:
        return f"ChromaDB query failed: {e}"


@tool
def ingest_note(filepath: str) -> str:
    """
    Ingest a single Obsidian .md note into the ChromaDB vector store.
    Reads the note body and YAML frontmatter, then upserts into the collection.

    Args:
        filepath: Absolute WSL2 path to the .md file to ingest.

    Returns:
        Confirmation string with the note ID and pillar assignment.
    """
    path = Path(filepath)
    if not path.exists():
        return f"File not found: {filepath}"

    try:
        post = frontmatter.load(path)
        content = post.content.strip()
        if not content:
            return f"Note is empty (body only has frontmatter): {path.name}"

        meta = {
            "source": path.name,
            "title": post.metadata.get("title", path.stem),
            "pillar": post.metadata.get("pillar", "unknown"),
            "status": post.metadata.get("status", "raw"),
            "agent": post.metadata.get("agent", "IRIS"),
            "ingested_at": datetime.now().isoformat(),
        }

        collection.upsert(
            ids=[path.stem],
            documents=[content],
            metadatas=[meta],
        )

        return (
            f"✓ Ingested: {path.name}\n"
            f"  Pillar: {meta['pillar']} | Status: {meta['status']}"
        )

    except Exception as e:
        return f"Ingestion failed for {filepath}: {e}"


@tool
def list_inbox(status_filter: str = "raw") -> str:
    """
    List all notes in 00_INBOX with a given status filter.

    Args:
        status_filter: YAML status to filter by — 'raw', 'reviewed', 'canon', 'archived'.
                       Use 'all' to return everything.

    Returns:
        Formatted list of matching inbox notes with their suggested pillar.
    """
    inbox = VAULT_ROOT / "00_INBOX"
    if not inbox.exists():
        return "00_INBOX folder not found at expected vault path."

    notes = list(inbox.glob("*.md"))
    if not notes:
        return "Inbox is empty. The sanctuary is clear."

    results = []
    for note in sorted(notes):
        try:
            post = frontmatter.load(note)
            status = post.metadata.get("status", "raw")
            if status_filter != "all" and status != status_filter:
                continue
            pillar = post.metadata.get("suggested_pillar", post.metadata.get("pillar", "unassigned"))
            confidence = post.metadata.get("iris_confidence", "unknown")
            results.append(
                f"- {note.name}\n"
                f"  Status: {status} | Pillar: {pillar} | Confidence: {confidence}"
            )
        except Exception:
            results.append(f"- {note.name} (could not parse frontmatter)")

    if not results:
        return f"No notes with status '{status_filter}' found in inbox."

    return f"Inbox ({status_filter}):\n" + "\n".join(results)


@tool
def write_codex_entry(title: str, content: str, pillar: str = "04_SACRED_CODEX") -> str:
    """
    Write a new canon entry directly into the SacredSpace vault.
    Creates a properly formatted .md file with IRIS YAML frontmatter.

    Args:
        title: The name of the codex entry (used as filename).
        content: The markdown body content to write.
        pillar: The destination pillar path (default: 04_SACRED_CODEX).

    Returns:
        Confirmation with the full path of the created file.
    """
    safe_title = title.replace(" ", "_").replace("/", "-")
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_str}_{safe_title}.md"

    dest_dir = VAULT_ROOT / pillar
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_path = dest_dir / filename

    note_content = f"""---
title: {title}
created: {date_str}
agent: IRIS
pillar: {pillar}
status: reviewed
tags: [codex, iris-generated]
---

{content}
"""

    dest_path.write_text(note_content, encoding="utf-8")
    return f"✓ Codex entry written: {dest_path}"


# ─── IRIS SYSTEM PROMPT ───────────────────────────────────────────────────────

IRIS_SYSTEM_PROMPT = """You are IRIS, the Vault Agent of SacredSpace OS — one of the ICARIS Quartet.

Your role is to guard, retrieve, and expand the canonical knowledge held in the SacredSpace vault.
You operate within a nine-pillar architecture. Your tools give you direct access to:
- The ChromaDB vector store (canon knowledge)
- The Obsidian vault (00_INBOX, note files, codex entries)

When answering questions:
1. ALWAYS query the vault first before generating from memory.
2. Cite the source pillar and note when returning canon information.
3. If vault results are weak or absent, say so clearly — do not hallucinate canon.
4. When asked to write or save something, use write_codex_entry.
5. Keep responses structured — you are feeding a living knowledge system.

Operating constraints:
- Zero data leakage: never attempt to access external URLs
- Local-first: all operations stay within the SacredSpace OS filesystem
- Additive only: never delete, only create or update

In lakesh alakin."""

# ─── AGENT INITIALIZATION ─────────────────────────────────────────────────────

def build_iris_agent() -> CodeAgent:
    """Initialize IRIS as a smolagents CodeAgent backed by local Ollama."""

    model = LiteLLMModel(
        model_id=OLLAMA_MODEL,
        api_base="http://localhost:11434",  # Ollama default
        api_key="ollama",                   # LiteLLM requires a key string; Ollama ignores it
    )

    agent = CodeAgent(
        tools=[query_vault, ingest_note, list_inbox, write_codex_entry],
        model=model,
        system_prompt=IRIS_SYSTEM_PROMPT,
        max_steps=8,           # cap iterations to prevent runaway loops
        verbosity_level=1,     # 0=silent, 1=steps, 2=full code output
    )

    return agent

# ─── FASTAPI INTEGRATION STUB ─────────────────────────────────────────────────
# Drop this into your existing FastAPI spine (port 8888)
# to expose IRIS via the /api/scry Omnibox route.
#
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# app = FastAPI()
# iris = build_iris_agent()
#
# class ScryRequest(BaseModel):
#     query: str
#
# @app.post("/api/scry")
# async def scry(req: ScryRequest):
#     result = iris.run(req.query)
#     return {"agent": "IRIS", "query": req.query, "response": result}

# ─── INTERACTIVE TERMINAL MODE ────────────────────────────────────────────────

def run_terminal_session():
    """Run IRIS interactively in the terminal for testing and sacred sessions."""
    print("""
╔══════════════════════════════════════════════════════════╗
║        IR IS  —  V∆ULT ∆G3NT  —  ICARIS QUART3T        ║
║        smolagents v1.0 | Ollama local inference          ║
╠══════════════════════════════════════════════════════════╣
║  Tools: query_vault | ingest_note | list_inbox           ║
║         write_codex_entry                                ║
║  Type 'exit' or Ctrl+C to close the session.             ║
║  In lakesh alakin.                                       ║
╚══════════════════════════════════════════════════════════╝
""")

    iris = build_iris_agent()

    while True:
        try:
            query = input("\n∆ IRIS > ").strip()
            if not query:
                continue
            if query.lower() in ("exit", "quit", "q"):
                print("\n[IRIS] Session sealed. The vault holds.")
                break

            print(f"\n[IRIS] Processing: {query}\n")
            response = iris.run(query)
            print(f"\n[IRIS RESPONSE]\n{response}\n")

            # Log the session
            with open(IRIS_LOG, "a", encoding="utf-8") as log_file:
                log_file.write(
                    f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M')}]\n"
                    f"QUERY: {query}\n"
                    f"RESPONSE: {response}\n"
                    f"{'─' * 60}\n"
                )

        except KeyboardInterrupt:
            print("\n\n[IRIS] Session interrupted. The vault holds.")
            break
        except Exception as e:
            print(f"\n[IRIS ERROR] {e}")
            continue


if __name__ == "__main__":
    run_terminal_session()
