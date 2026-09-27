# kethras.py

## Sacred Function
Keeper of Thresholds. Routes incoming requests across the Council Grove, enforces gate logic (who may pass, what may be invoked), and maintains council session state. Acts as the gatekeeper layer between the FastAPI spine and the agent ensemble.

## Pillar
[[02_COUNCIL_GROVE]]

## Sacred System
[[Council Grove]]

## Canonical Path
`02_COUNCIL_GROVE/kethras.py`

## FastAPI Route
`POST /agent/kethras` via `app.include_router(kethras.router, prefix="/kethras-learning-gate")`

## Status
Active

## Canonized
2026-05-06 · Commit: `03ce3bd`

## Change Log
| Date | Change | Commit |
|------|--------|--------|
| 2026-05-06 | Entered Code Canon Registry | HEAD |
