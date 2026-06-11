---
tags:
  - archive
  - canon-gate
  - protocol
  - integrity
pillar: ARCHIVE
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# Canon Gate Protocol

> Status: CANON â€” The governing law of knowledge promotion.

## The Law

**Nothing enters CANON without passing through the Gate.**

The Canon Gate is the boundary between the ephemeral and the permanent. It is the difference between a thought and a book.

## Promotion Criteria

A piece of knowledge may be promoted to CANON when ALL of the following are true:

1. **Coherence**: It does not contradict existing CANON without explicit supersession
2. **Completeness**: It is not a stub â€” it says what it needs to say
3. **Attribution**: Its source is traceable (session, model, document)
4. **Utility**: It will be referenced again â€” it is not a one-use fact
5. **Integrity**: Its hash matches its content (no silent mutation)

## Gate Keepers

- **IRIS** (agent) â€” automated validation, hash assignment
- **OakeyTree** (operator) â€” final human approval for major promotions
- **Council Grove** â€” group review for contested promotions

## The Three Tiers

```
RAW      â†’ Captured, unvalidated. Lives in ChromaDB. 30-day retention.
DISTILLED â†’ Validated, structured. Lives in pgvector/Supabase.
CANON    â†’ Promoted, immutable (except through explicit new version).
             Lives in THIS VAULT.
```

## What happens at the Gate

```
1. IRIS receives promotion request
2. Coherence check against CANON graph
3. Duplication scan (ELIAS)
4. Entropy score (ASHER)
5. If passes: assign canon_hash, write to vault, emit CanonPromoted event
6. If fails: return to DISTILLED with failure reason
7. AURORA may refactor the artifact to meet Canon standard
```

## Immutability Principle

CANON is never deleted. It is superseded. Every CANON note that becomes outdated gets a `superseded_by` field and remains visible in the vault as historical record.

This is the event sourcing principle applied to knowledge.
