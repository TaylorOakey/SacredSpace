---
tags:
  - systems
  - overview
  - infrastructure
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# âš™ SYSTEMS â€” Technical Infrastructure

All deployed technical systems, stacks, agents, and orchestration layers live here.

## Deployed Stack

| Service | Port | Status | Notes |
|---------|------|--------|-------|
| Ollama | 11434 | RUNNING | Local LLM inference |
| ChromaDB | 8000 | RUNNING | Vector store (RAW tier) |
| Open WebUI | 8080 | RUNNING | SacredSpace OS UI layer |
| PostgreSQL | 5432 | RUNNING | Supabase + pgvector |
| Tailscale | â€” | RUNNING | Node 100.117.9.101 |
| Codexium vâˆž | â€” | PENDING | Event-driven station |

## See also

- [[1_SYSTEMS/Infrastructure_Stack|Infrastructure Stack]]
- [[1_SYSTEMS/Codexium_Integration|Codexium Integration]]
- [[1_SYSTEMS/Sacred_Fiahfox_v2|Sacred Fiahfox v2]]
- [[1_SYSTEMS/Memory_Pipeline_Technical|Memory Pipeline Technical]]
- [[_CODEXIUM/Codexium_Architecture|Codexium vâˆž Architecture]]
