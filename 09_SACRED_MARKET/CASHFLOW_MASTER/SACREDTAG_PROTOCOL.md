---
title: "SACREDTAG_PROTOCOL"
source: "/mnt/d/01_VAULT/SacredSpace_Vault/00_SACRED_SPINE/SACREDTAG_PROTOCOL.md"
keyword_count: 4
keywords_found: [etsy, gelato, printify, revenue]
pillar: "01_VAULT"
date_indexed: "2026-05-21"
cashflow_rank: 72
---


# SACREDTAG — Unified Tagging Protocol

## 🧭 Domain
Core

## 🧩 Type
Protocol / System

## 🌱 Description
SACREDTAG is the universal metadata schema for all SacredSpace OS work products —
chat sessions, Obsidian notes, NotebookLM source documents, Google Drive files,
and git commits. It enforces consistent date, pillar, mode, topic, keyword, status,
and agent attribution across every system.

## 🔥 Purpose
SacredSpace generates enormous output across Claude, Gemini, GPT, Obsidian, Drive,
and NotebookLM. Without a shared tagging grammar, sessions become unsearchable and
pillar routing breaks down. SACREDTAG is the connective tissue — it makes every
artifact findable, classifiable, and Codex-ready from the moment it's created.

## ⚙️ Mechanics / Function

### Core Fields

| Field    | Description                                                        |
|----------|--------------------------------------------------------------------|
| DATE     | ISO 8601 — YYYY-MM-DD. Always full date, never relative.           |
| PILLAR   | One of the nine canonical directories. CROSS_PILLAR if multi.      |
| MODE     | Session type — see Mode Table below.                               |
| TOPIC    | One sentence. What is this session/doc actually about?             |
| KEYWORDS | 3–7 lowercase slugs, comma-separated.                              |
| STATUS   | ACTIVE on open → resolved to CANON / DISTILL / VOID on close.     |
| AGENTS   | AI council members present: CLAUDE, GEMINI, GPT, OLLAMA.           |

### Session Modes

| Mode     | Use When                                     | Default Status |
|----------|----------------------------------------------|----------------|
| BUILD    | Infrastructure, code, deployment             | DISTILL        |
| LEARN    | Study, Codex, AAS path                       | DISTILL        |
| LORE     | Story, narrative, world-building             | DISTILL        |
| STRATEGY | Mission, nonprofit, market                   | DISTILL        |
| COUNCIL  | Multi-agent coordination                     | CANON          |
| RITUAL   | Opening, closing, ceremony                   | CANON          |
| DEBUG    | Troubleshooting                              | VOID           |
| VISION   | Philosophy, ideas, conceptual mapping        | DISTILL        |

### Nine Pillars

| Code | Directory            | Domain                          |
|------|----------------------|---------------------------------|
| P01  | 01_OBSIDIAN_VAULTS   | Canonical knowledge store       |
| P02  | 02_COUNCIL_GROVE     | Multi-AI governance, handoff    |
| P03  | 03_NEURAL_FOREST     | LLM pipeline, Scout, Gardener   |
| P04  | 04_SACRED_CODEX      | Canon ledger, spells, rituals   |
| P05  | 05_MEMORY_ENGINE     | SQLite, Redis, ChromaDB         |
| P06  | 06_AGENT_LAYER       | ICARIS — ELIAS, AURORA, ASHER, IRIS |
| P07  | 07_SOCIAL_MOTHERSHIP | Content, publishing, brand      |
| P08  | 08_LEARNING_PATH     | Maestro AAS, Rites, Artifacts   |
| P09  | 09_SACRED_MARKET     | Revenue, Etsy, Printify, Gelato |

---

### Format A — Full Block
For: top of every Obsidian note, NotebookLM source doc, Drive doc.

```
∆∆∆ SACREDTAG ∆∆∆
DATE:     YYYY-MM-DD
PILLAR:   [pillar]
MODE:     [mode]
TOPIC:    [one sentence]
KEYWORDS: [slug, slug, slug]
STATUS:   CANON | DISTILL | VOID
AGENTS:   CLAUDE
∆∆∆ IN LAKESH ∆∆∆
```

### Format B — Chat Opener Block
For: first message of every Claude / Gemini / GPT session.

```
∆∆∆ SESSION OPEN ∆∆∆
DATE:     YYYY-MM-DD
PILLAR:   [pillar]
MODE:     [mode]
TOPIC:    [one sentence]
KEYWORDS: [slug, slug, slug]
STATUS:   ACTIVE → [resolve on close]
AGENTS:   CLAUDE
∆∆∆
```

### Format C — Compact Inline
For: chat title rename, git commit prefix, file name prefix.

```
[YYYY-MM-DD | P0X | MODE] Topic description #keyword1 #keyword2 ∆
```

### Format D — Obsidian Hashtags
For: note body, bottom of any text doc.

```
#sacredspace/[pillar]/[keyword] #mode/[mode] #status/[status]
```

---

## 🔗 Connections
- `04_SACRED_CODEX/SACREDCODEX_INVOCATION_LEDGER` — spells use same pillar routing
- `02_COUNCIL_GROVE/handoff_ritual.py` — context capsules should include SACREDTAG block
- `01_OBSIDIAN_VAULTS/SacredSpace_Vault` — all vault notes adopt Format A as header
- NotebookLM naming: `[DOMAIN] — [TYPE] — [NAME] — v[VERSION]` aligns with TOPIC field
- CLAUDE.md — session rules should reference SACREDTAG as session-open requirement

## 🧠 Insights
- STATUS as a lifecycle field (ACTIVE → resolved) turns every session into a triage artifact
- MODE + PILLAR together define routing without ambiguity — no two combinations map to the same place
- The compact inline format makes bulk chat renaming mechanical, not creative
- DEBUG → VOID by default saves significant triage time; most debugging chats have zero extractable canon

## 🚀 Evolution Potential
- `sacred_watcher.py` could auto-detect SACREDTAG blocks in new files and index to SQLite
- FastAPI route `POST /codex/tag` could accept a SACREDTAG payload and create the Obsidian note automatically
- Gemini Gem (Sacred Guide) should be prompted to request SACREDTAG fields at session open if not provided
- Chrome extension could surface the tag generator as a sidebar panel

## 🏷 Tags
#sacredspace/04_sacred_codex/protocol #mode/ritual #status/canon #tagging #metadata #pillar-routing #session-open
