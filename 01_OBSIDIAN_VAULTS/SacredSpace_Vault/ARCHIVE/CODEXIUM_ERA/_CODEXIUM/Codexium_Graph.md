---
tags:
  - codexium
  - graph
  - relationships
  - edges
pillar: SYSTEMS
status: EXPERIMENTAL
created: 2026-03-15
session: 2026-03-15 23:44
---

# Codexium Graph â€” Relationship Map

> graph.json is the machine-readable edge store.
> This document is the human-readable relationship map.

## Current Graph

```json
{
  "nodes": ["PY.DATA.function.0001.v1"],
  "edges": []
}
```

*Graph will grow as nodes are ingested and relationships are discovered.*

## Relationship Types

| Type | Meaning |
|------|---------|
| `derives_from` | This node was created from / inspired by another |
| `improves` | This node is a superior replacement for another |
| `overlaps_with` | These nodes share functionality (merge candidate) |
| `conflicts_with` | These nodes do incompatible things (deliberate divergence) |
| `depends_on` | This node requires another to function |
| `composes` | This node is part of a larger system node |

## Compression Thresholds

- Cosine similarity > 0.85 â†’ Merge candidate
- Cosine similarity 0.70â€“0.85 â†’ Version increment candidate
- Cosine similarity 0.55â€“0.70 â†’ Abstraction opportunity
- Cosine similarity < 0.55 â†’ Distinct node
