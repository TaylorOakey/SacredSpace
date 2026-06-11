---
tags:
  - systems
  - langgraph
  - fastapi
  - orchestration
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# LangGraph + FastAPI Orchestration Spine

> Status: DEPLOYED Â· The nervous system of SacredSpace OS

## Role

The orchestration spine connects:
- Local inference (Ollama)
- Memory (ChromaDB / pgvector)
- Agents (ICARIS Quartet)
- Presentation (Open WebUI / Sacred Fiahfox)

## Architecture

```
User Input
    â†“
FastAPI Gateway (:8000 or :8001)
    â†“
LangGraph State Machine
    â”œâ”€â”€ ELIAS (Knowledge / Similarity)
    â”œâ”€â”€ AURORA (Evolution / Generation)
    â”œâ”€â”€ ASHER (Entropy / Audit)
    â””â”€â”€ IRIS (Integrity / Archive)
    â†“
Memory Router
    â”œâ”€â”€ Query ChromaDB (RAW)
    â”œâ”€â”€ Query pgvector (CANON)
    â””â”€â”€ Write back on promotion
    â†“
Response
```

## LangGraph State Schema

```python
class SacredState(TypedDict):
    messages: list
    pillar: str
    tier: Literal["RAW", "DISTILLED", "CANON"]
    agent: str
    canon_candidates: list
    entropy_score: float
    session_id: str
```

## Cross-references

- [[6_COUNCIL/ICARIS_Quartet|ICARIS Quartet agents]]
- [[1_SYSTEMS/Memory_Pipeline_Technical|Memory Pipeline]]
- [[_CODEXIUM/Codexium_Integration|Codexium Integration]]
