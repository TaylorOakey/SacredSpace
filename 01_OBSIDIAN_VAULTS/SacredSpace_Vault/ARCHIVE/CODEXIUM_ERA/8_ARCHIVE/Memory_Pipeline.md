---
tags:
  - archive
  - memory
  - pipeline
  - rag
  - canon
pillar: ARCHIVE
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Memory Pipeline

> The three-tier knowledge progression system.

## Overview

```
All Input
    â†“
RAW (ChromaDB :8000)
  Unvalidated, auto-embedded, timestamped
  30-day default retention
  Access: all agents, read/write
    â†“
Canon Gate Review
    â†“
DISTILLED (PostgreSQL + pgvector)
  Validated, structured, linked
  Indefinite retention
  Access: agents read, IRIS writes
    â†“
Canon Gate Promotion
    â†“
CANON (Obsidian Vault â€” THIS FILE'S HOME)
  Immutable, versioned, sovereign
  Access: read-only (humans + agents)
  Write: IRIS only, on promotion
```

## Event Flow

Every promotion emits events captured in Supabase `events_log`:

```sql
-- RAW capture
INSERT INTO events_log (event_type, payload) 
VALUES ('KnowledgeCaptured', '{"tier": "RAW", "source": "session"}');

-- Distillation
INSERT INTO events_log (event_type, payload)
VALUES ('KnowledgeDistilled', '{"tier": "DISTILLED", "canon_candidate": true}');

-- Canon promotion
INSERT INTO events_log (event_type, payload)
VALUES ('CanonPromoted', '{"tier": "CANON", "vault_path": "...", "hash": "..."}');
```

## Codexium Alignment

The Codexium vâˆž node lifecycle maps perfectly:
- `NodeCreated` = RAW capture
- `EntropyCalculated + SimilarityComputed` = DISTILLED evaluation
- `EvolutionTriggered â†’ stable` = CANON promotion

The memory pipeline IS the Codexium lifecycle, generalized beyond code to all knowledge types.

## See also

- [[8_ARCHIVE/Canon_Gate_Protocol|Canon Gate Protocol]]
- [[1_SYSTEMS/Memory_Pipeline_Technical|Memory Pipeline Technical]]
- [[_CODEXIUM/Codexium_Architecture|Codexium vâˆž]]
