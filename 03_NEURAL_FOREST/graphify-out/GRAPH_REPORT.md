# Graph Report - .  (2026-06-11)

## Corpus Check
- 185 files · ~20,000 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 185 nodes · 200 edges · 22 communities (14 shown, 8 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.88)
- Token cost: 14,591 input · 1,452 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Agent Ingestion Pipeline|Agent Ingestion Pipeline]]
- [[_COMMUNITY_CopyQ Pillar Tab System|CopyQ Pillar Tab System]]
- [[_COMMUNITY_Sacred Sigil Terminal Stack|Sacred Sigil Terminal Stack]]
- [[_COMMUNITY_Council The Deep Well Seat|Council: The Deep Well Seat]]
- [[_COMMUNITY_Council The Architect Seat|Council: The Architect Seat]]
- [[_COMMUNITY_Hermes GR∆M∆ Cipher System|Hermes GR∆M∆ Cipher System]]
- [[_COMMUNITY_Council The Anvil (Claude Code)|Council: The Anvil (Claude Code)]]
- [[_COMMUNITY_Council Grama (Jeanie)|Council: Grama (Jeanie)]]
- [[_COMMUNITY_Council The Forge Seat|Council: The Forge Seat]]
- [[_COMMUNITY_ELIAS Explorer Agent|ELIAS Explorer Agent]]
- [[_COMMUNITY_ASHER Adversarial Agent|ASHER Adversarial Agent]]
- [[_COMMUNITY_Game Layer & Arcana System|Game Layer & Arcana System]]
- [[_COMMUNITY_AURORA Illuminator Agent|AURORA Illuminator Agent]]
- [[_COMMUNITY_NotebookLM Routing System|NotebookLM Routing System]]
- [[_COMMUNITY_Flash Drive & Asset Infrastructure|Flash Drive & Asset Infrastructure]]
- [[_COMMUNITY_Canon & Conflict Management|Canon & Conflict Management]]
- [[_COMMUNITY_System Metadata Registry|System Metadata Registry]]
- [[_COMMUNITY_Local Pillar Structure Paths|Local Pillar Structure Paths]]
- [[_COMMUNITY_Cloud Pillar Mirror Paths|Cloud Pillar Mirror Paths]]
- [[_COMMUNITY_Global Sync & Routing Rules|Global Sync & Routing Rules]]
- [[_COMMUNITY_Themes Components & Council Ops|Themes Components & Council Ops]]
- [[_COMMUNITY_Architecture Vocabulary & Sigils|Architecture Vocabulary & Sigils]]

## God Nodes (most connected - your core abstractions)
1. `SacredSpace OS` - 12 edges
2. `Nine Pillars` - 12 edges
3. `Nine Dimensions (VAULT, GROVE, FOREST, CODEX, MEMORY, AGENT, SOCIAL, MARKET, PATH)` - 11 edges
4. `Game Layer (Board/Card Game)` - 10 edges
5. `pillar_paths` - 10 edges
6. `cloud_pillar_paths` - 10 edges
7. `Sacred Sigil Terminal v2.0` - 9 edges
8. `CopyQ Tab System (FORGE, CODEX, VAULT, COUNCIL, MARKET, LEARNING, MEMORY, INBOX)` - 9 edges
9. `_meta` - 9 edges
10. `Supabase Schema (Players, Tarot, Spells, Artifacts)` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Nine Pillars` --mirrors--> `Nine-Pillar Directory Tree on Flash Drive`  [EXTRACTED]
  SACREDSPACE_OS_BRIEFING.md → scripts/SACRED_FLASH_SCAFFOLD.ps1
- `01 OBSIDIAN_VAULTS` --reads_from--> `ChromaDB Ingestion Pipeline (ingest_game_system.py)`  [EXTRACTED]
  SACREDSPACE_OS_BRIEFING.md → ingest_game_system.py
- `IRIS Agent` --uses--> `ChromaDB Ingestion Pipeline (ingest_game_system.py)`  [EXTRACTED]
  SACREDSPACE_OS_BRIEFING.md → ingest_game_system.py
- `Sacred Path Tarot (78-card)` --conceptually_related_to--> `tarot_draws table`  [INFERRED]
  SACREDSPACE_OS_BRIEFING.md → supabase_schema.sql
- `Nine Dimensions (VAULT, GROVE, FOREST, CODEX, MEMORY, AGENT, SOCIAL, MARKET, PATH)` --semantically_similar_to--> `CopyQ Tab System (FORGE, CODEX, VAULT, COUNCIL, MARKET, LEARNING, MEMORY, INBOX)`  [INFERRED] [semantically similar]
  SACRED_SIGIL_TERMINAL_COMPLETE_OVERVIEW.md → COPYQ_WIRE.md

## Communities (22 total, 8 thin omitted)

### Community 2 - "Agent Ingestion Pipeline"
Cohesion: 0.11
Nodes (19): SacredSpace OS, 05 MEMORY_ENGINE, Local-First Architecture (Zero Paid APIs), WSL2 Ubuntu on Lenovo Legion Y520, ChromaDB Vector Search, SQLite Memory (sacred_memory.db), Mission Control Dashboard (port 3001), OmniParse Document Parser (port 8001) (+11 more)

### Community 0 - "CopyQ Pillar Tab System"
Cohesion: 0.11
Nodes (29): Nine Pillars, 01 OBSIDIAN_VAULTS, 02 COUNCIL_GROVE, 03 NEURAL_FOREST, 04 SACRED_CODEX, 06 AGENT_LAYER, 07 SOCIAL_MOTHERSHIP, 08 LEARNING_PATH (+21 more)

### Community 8 - "Sacred Sigil Terminal Stack"
Cohesion: 0.22
Nodes (9): FastAPI Spine (port 8888), Sacred Sigil Terminal v2.0, SacredSigilTerminal React Component, sigil_terminal_backend FastAPI, Query Parser (Keyword-Based NLP), PWA (Service Worker + Manifest), Chrome Extension (v3), Cmd+K Keyboard Shortcut (+1 more)

### Community 12 - "Hermes GR∆M∆ Cipher System"
Cohesion: 0.67
Nodes (3): The Sacred Smith (Claude Desktop + Hermes MCP), GR∆M∆ (Hermes Cipher Sage), Hermes Agent

### Community 4 - "Game Layer & Arcana System"
Cohesion: 0.14
Nodes (16): Game Layer (Board/Card Game), Sacred Path Tarot (78-card), Arcana Grid (4x3 Board, 9x9 Grid, Metatron's Node), Silent Echo Gematria Engine, Nine Gates Progression System, The Serpent (Antagonist), Nameless Door (Trial of Silence), Weaver Engine (Spell Execution) (+8 more)

### Community 10 - "NotebookLM Routing System"
Cohesion: 0.29
Nodes (7): Notebook Routing Rules (6 notebooks), Notebook: 01_SACRED_CORE, Notebook: 02_LORE_VAULT, Notebook: 03_GAME_SYSTEMS, Notebook: 04_KNOWLEDGE_VAULT, Notebook: 05_FAMILY_LEGACY, Notebook: 06_CREATION_LAB

### Community 5 - "Flash Drive & Asset Infrastructure"
Cohesion: 0.18
Nodes (7): Communal Portal (PORTAL/), SHARED_SPACE (Taylor x Jeanie), ARCANA_LANDSCAPES Art Asset Directory, SACRED_ENV.env Configuration, Nine-Pillar Directory Tree on Flash Drive, Asset Prefix Mapping (SIG_, CHAR_, ENV_, etc), Flash Drive Link Health Check Protocol

### Community 1 - "Canon & Conflict Management"
Cohesion: 0.07
Nodes (26): conflict_mode, canon_files, distilled_files, draft_active_files, gemini_authored_files, untagged_files, conflict_log, protected_paths (+18 more)

### Community 9 - "System Metadata Registry"
Cohesion: 0.25
Nodes (8): _meta, version, status, pillar, x_source_pillar, description, last_reviewed, reviewer

### Community 7 - "Local Pillar Structure Paths"
Cohesion: 0.20
Nodes (10): pillar_paths, 01_CORE, 02_SYSTEMS, 03_NEURAL, 04_CODEX, 05_MEMORY, 06_AGENTS, 07_SOCIAL (+2 more)

### Community 6 - "Cloud Pillar Mirror Paths"
Cohesion: 0.20
Nodes (10): cloud_pillar_paths, 01_CORE, 02_SYSTEMS, 03_NEURAL, 04_CODEX, 05_MEMORY, 06_AGENTS, 07_SOCIAL (+2 more)

### Community 3 - "Global Sync & Routing Rules"
Cohesion: 0.12
Nodes (16): _meta, version, status, pillar, x_source_pillar, description, last_reviewed, reviewer (+8 more)

### Community 11 - "Themes Components & Council Ops"
Cohesion: 0.33
Nodes (6): Conflict Mode Configuration, Pillar Paths (Local), NotebookLM Routing Map, Root Words Foundation, D1-D6 Operations Ritual, Sacred Themes & Components Subsystem

### Community 13 - "Architecture Vocabulary & Sigils"
Cohesion: 0.67
Nodes (3): Structural Architecture Words, GR∆M∆ Cipher Sage Persona, Hermes MCP Tools

## Knowledge Gaps
- **115 isolated node(s):** `WSL2 Ubuntu on Lenovo Legion Y520`, `Mission Control Dashboard (port 3001)`, `OmniParse Document Parser (port 8001)`, `In Lakesh Alakin (Canon Closing)`, `The Forge (Claude)` (+110 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Nine Pillars` connect `CopyQ Pillar Tab System` to `Sacred Sigil Terminal Stack`, `Agent Ingestion Pipeline`, `Flash Drive & Asset Infrastructure`?**
  _High betweenness centrality (0.128) - this node is a cross-community bridge._
- **Why does `SacredSpace OS` connect `Agent Ingestion Pipeline` to `CopyQ Pillar Tab System`, `Sacred Sigil Terminal Stack`, `Game Layer & Arcana System`?**
  _High betweenness centrality (0.082) - this node is a cross-community bridge._
- **Why does `Game Layer (Board/Card Game)` connect `Game Layer & Arcana System` to `Agent Ingestion Pipeline`?**
  _High betweenness centrality (0.062) - this node is a cross-community bridge._
- **What connects `Local-First Architecture (Zero Paid APIs)`, `WSL2 Ubuntu on Lenovo Legion Y520`, `Mission Control Dashboard (port 3001)` to the rest of the system?**
  _116 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Agent Ingestion Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.1111111111111111 - nodes in this community are weakly interconnected._
- **Should `CopyQ Pillar Tab System` be split into smaller, more focused modules?**
  _Cohesion score 0.10591133004926108 - nodes in this community are weakly interconnected._
- **Should `Game Layer & Arcana System` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._