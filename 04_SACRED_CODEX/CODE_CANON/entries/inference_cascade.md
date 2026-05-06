# inference_cascade.py

## Sacred Function
Three-tier LLM provider chain: Ollama (local, primary) → Gemini (cloud fallback) → Mock (offline safe). Ensures SacredSpace OS always has inference available regardless of network or GPU state. Zero-cost-safe — Gemini only fires if Ollama is unreachable.

## Pillar
[[02_COUNCIL_GROVE]]

## Sacred System
[[Council Grove]] · [[Neural Forest]]

## Status
Active

## Canonical Path
`systems/fastapi/inference_cascade.py`

## Canonized
2026-05-06 · Commit: 03ce3bd3

## Change Log
| Date | Change |
|------|--------|
| 2026-05-06 | Path corrected from 02_SYSTEMS/inference_cascade.py → systems/fastapi/ during pillar rename |
| 2026-05-06 | Gemini cascade confirmed zero-cost-safe fallback (P2 requirement) |
