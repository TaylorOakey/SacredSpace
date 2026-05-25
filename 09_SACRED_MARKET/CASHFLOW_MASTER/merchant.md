---
title: "merchant"
source: "/mnt/d/SacredSpace_OS/04_SACRED_CODEX/CODE_CANON/entries/merchant.md"
keyword_count: 5
keywords_found: [etsy, gelato, merchant, price, printify]
pillar: "04_SACRED_CODEX"
date_indexed: "2026-05-21"
cashflow_rank: 50
---

# merchant.py

## Sacred Function
Economy and Sacred Bazaar logic. Manages artifact catalog records (`name, gematria_value, soul_tone_hz, pillar, price`), handles Etsy/Printify/Gelato integration hooks, and exposes the Sacred Market API surface. The MERCHANT agent was the first activated artifact in the canon economy layer.

## Pillar
[[02_COUNCIL_GROVE]]

## Sacred System
[[Sacred Bazaar]] · [[09_SACRED_MARKET]]

## Canonical Path
`02_COUNCIL_GROVE/merchant.py`

## FastAPI Route
`app.include_router(merchant.router, prefix="/merchant-sacred-artifacts")`

## Status
Active

## Canonized
2026-05-06 · Commit: `2391c042`

## Change Log
| Date | Change | Commit |
|------|--------|--------|
| 2026-05-06 | MERCHANT activated — Artifact #1 OAK OF THE SACRED VOID FORGED | `2391c042` |
| 2026-05-06 | Entered Code Canon Registry | HEAD |
