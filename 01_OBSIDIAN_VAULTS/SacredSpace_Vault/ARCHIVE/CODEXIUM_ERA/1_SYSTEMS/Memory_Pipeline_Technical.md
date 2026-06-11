---
tags:
  - systems
  - memory
  - pipeline
  - rag
pillar: SYSTEMS
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Memory Pipeline â€” Technical

> Three-tier pipeline: RAW â†’ DISTILLED â†’ CANON

## Architecture

```
Input (any source)
    â†“
[RAW TIER]
  ChromaDB :8000
  Unvalidated embeddings
  Auto-tagged, timestamped
  Retention: 30 days default
    â†“
[Canon Gate Review]
  Human or agent validation
  Coherence check
  Duplication scan
    â†“
[DISTILLED TIER]
  PostgreSQL + pgvector
  Validated, structured
  Linked to knowledge graph
  Retention: indefinite
    â†“
[Canon Gate Promotion]
  Final editorial review
  Integrity hash assigned
    â†“
[CANON TIER]
  Obsidian vault (THIS VAULT)
  Immutable once CANON
  Git-mirrorable
  The Lost Libraries
```

## Canon Gate Protocol

A piece of knowledge reaches CANON when:
1. It has been validated by at least one agent review
2. Its integrity hash is recorded in `canon_registry`
3. It has been written as a `.md` file in this vault
4. No contradicting CANON entry exists without explicit supersession

## Episodic Memory Schema (Supabase)

```sql
CREATE TABLE episodic_memory (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id  TEXT NOT NULL,
    timestamp   TIMESTAMPTZ DEFAULT NOW(),
    tier        TEXT CHECK (tier IN ('RAW','DISTILLED','CANON')),
    content     TEXT,
    embedding   VECTOR(384),
    tags        TEXT[],
    pillar      TEXT,
    canon_hash  TEXT
);
```
