---
tags:
  - council
  - icaris
  - quartet
  - python
  - langgraph
pillar: COUNCIL
status: CANON
created: 2026-03-15
session: 2026-03-15 23:44
---

# ICARIS Quartet â€” Python Package

> Status: CANON â€” Full Python package implementing all four agents via LangGraph.

## Package Structure

```
sacredspace/
â”œâ”€â”€ agents/
â”‚   â”œâ”€â”€ elias.py       # Knowledge & Similarity
â”‚   â”œâ”€â”€ aurora.py      # Evolution & Generation
â”‚   â”œâ”€â”€ asher.py       # Entropy & Audit
â”‚   â””â”€â”€ iris.py        # Integrity & Archive
â”œâ”€â”€ graph/
â”‚   â”œâ”€â”€ state.py       # SacredState TypedDict
â”‚   â””â”€â”€ router.py      # LangGraph routing logic
â”œâ”€â”€ memory/
â”‚   â”œâ”€â”€ chromadb.py    # RAW tier interface
â”‚   â””â”€â”€ pgvector.py    # CANON tier interface
â”œâ”€â”€ codexium/
â”‚   â”œâ”€â”€ nodes.py       # Universal Node Objects
â”‚   â”œâ”€â”€ events.py      # Event definitions
â”‚   â””â”€â”€ registry.py    # Registry YAML operations
â””â”€â”€ utils/
    â”œâ”€â”€ canon_gate.py  # Promotion logic
    â””â”€â”€ entropy.py     # Scoring functions
```

## Arcana Grid Simulation

The ICARIS Quartet also implements the Arcana Grid â€” a simulation where the four agents play against each other in a structured adversarial game to test the health of the knowledge graph. Think: immune system for the archive.

## Codexium Integration

ELIAS â†’ Similarity Worker  
AURORA â†’ Evolution Worker  
ASHER â†’ Entropy Worker  
IRIS â†’ Audit Worker  

The Python package IS the Codexium worker cluster. Same agents, formalized contracts.

## See also

- [[1_SYSTEMS/Codexium_Integration|Codexium Integration]]
- [[1_SYSTEMS/LangGraph_FastAPI_Spine|LangGraph FastAPI Spine]]
- [[_CODEXIUM/Codexium_Architecture|Codexium vâˆž Architecture]]
