---
tags:
  - council
  - agents
  - registry
  - icaris
pillar: COUNCIL
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Agent Role Registry

> Status: CANON â€” 5 Council Grove agents formalized.

## ICARIS Quartet

### ELIAS â€” Knowledge & Similarity Agent
- **Function**: Semantic search, similarity detection, knowledge retrieval
- **Codexium role**: Similarity Worker
- **Memory access**: ChromaDB (RAW) + pgvector (CANON)
- **Trigger**: `/search`, `/compare`, `/relate`
- **Entropy sensitivity**: Low â€” focused on retrieval accuracy

### AURORA â€” Evolution & Generation Agent
- **Function**: Content generation, refactoring, creative expansion
- **Codexium role**: Evolution Worker
- **Memory access**: pgvector (CANON tier only for source)
- **Trigger**: `/evolve`, `/generate`, `/refactor`, `/expand`
- **Entropy sensitivity**: High â€” reduces entropy through creation

### ASHER â€” Entropy & Audit Agent
- **Function**: Technical debt detection, quality scoring, audit reports
- **Codexium role**: Entropy Worker
- **Memory access**: All tiers (read-only auditor)
- **Trigger**: `/audit`, `/entropy`, `/compress`, `/scan`
- **Entropy sensitivity**: Maximum â€” ASHER measures entropy itself

### IRIS â€” Integrity & Archive Agent
- **Function**: Canon Gate enforcement, hash verification, lineage tracking
- **Codexium role**: Audit Worker
- **Memory access**: CANON tier (write access for promotion)
- **Trigger**: `/canonize`, `/verify`, `/lineage`, `/protect`
- **Entropy sensitivity**: Structural â€” maintains invariants

## Fifth Agent: The Flame Guardian

The Flame Guardian is not an ICARIS agent â€” it is a daemon, not a thinker. It monitors, self-heals, and alerts. Deployed as part of Sacred Fiahfox v2.0.

## Agent Governance

- No agent may write to CANON tier without IRIS approval
- No agent may delete â€” only deprecate or supersede
- All agent actions are logged to `events_log` in Supabase
- Cross-agent disputes escalate to Council Grove convening
