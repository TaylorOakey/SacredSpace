# Graph Report - .  (2026-06-10)

## Corpus Check
- Corpus is ~9,642 words - fits in a single context window. You may not need a graph.

## Summary
- 104 nodes · 123 edges · 16 communities (8 shown, 8 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 7 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_CopyQ Tab System|CopyQ Tab System]]
- [[_COMMUNITY_Data Ingestion Pipeline|Data Ingestion Pipeline]]
- [[_COMMUNITY_Game Layer Mechanics|Game Layer Mechanics]]
- [[_COMMUNITY_Flash Drive Infrastructure|Flash Drive Infrastructure]]
- [[_COMMUNITY_Sacred Sigil Terminal|Sacred Sigil Terminal]]
- [[_COMMUNITY_NotebookLM Canon Migration|NotebookLM Canon Migration]]
- [[_COMMUNITY_Council Grove & Neural Forest|Council Grove & Neural Forest]]
- [[_COMMUNITY_Hermes & GR∆M∆ Cipher|Hermes & GR∆M∆ Cipher]]
- [[_COMMUNITY_AURORA & CopyQ|AURORA & CopyQ]]
- [[_COMMUNITY_Canon Close Ritual|Canon Close Ritual]]
- [[_COMMUNITY_The Forge Seat|The Forge Seat]]
- [[_COMMUNITY_The Deep Well Seat|The Deep Well Seat]]
- [[_COMMUNITY_The Architect Seat|The Architect Seat]]
- [[_COMMUNITY_ELIAS Agent|ELIAS Agent]]
- [[_COMMUNITY_ASHER Agent|ASHER Agent]]
- [[_COMMUNITY_CopyQ Bridge Script|CopyQ Bridge Script]]

## God Nodes (most connected - your core abstractions)
1. `SacredSpace OS` - 12 edges
2. `Nine Pillars` - 12 edges
3. `Nine Dimensions (VAULT, GROVE, FOREST, CODEX, MEMORY, AGENT, SOCIAL, MARKET, PATH)` - 11 edges
4. `Game Layer (Board/Card Game)` - 10 edges
5. `Sacred Sigil Terminal v2.0` - 9 edges
6. `CopyQ Tab System (FORGE, CODEX, VAULT, COUNCIL, MARKET, LEARNING, MEMORY, INBOX)` - 9 edges
7. `Supabase Schema (Players, Tarot, Spells, Artifacts)` - 8 edges
8. `Notebook Routing Rules (6 notebooks)` - 7 edges
9. `05 MEMORY_ENGINE` - 6 edges
10. `ChromaDB Ingestion Pipeline (ingest_game_system.py)` - 6 edges

## Surprising Connections (you probably didn't know these)
- `Nine-Pillar Directory Tree on Flash Drive` --mirrors--> `Nine Pillars`  [EXTRACTED]
  scripts/SACRED_FLASH_SCAFFOLD.ps1 → SACREDSPACE_OS_BRIEFING.md
- `ChromaDB Ingestion Pipeline (ingest_game_system.py)` --reads_from--> `01 OBSIDIAN_VAULTS`  [EXTRACTED]
  ingest_game_system.py → SACREDSPACE_OS_BRIEFING.md
- `NotebookLM Canon Migration (prep_notebooklm.py)` --reads_from--> `01 OBSIDIAN_VAULTS`  [EXTRACTED]
  scripts/prep_notebooklm.py → SACREDSPACE_OS_BRIEFING.md
- `NotebookLM Canon Migration (prep_notebooklm.py)` --reads_from--> `04 SACRED_CODEX`  [EXTRACTED]
  scripts/prep_notebooklm.py → SACREDSPACE_OS_BRIEFING.md
- `ChromaDB Ingestion Pipeline (ingest_game_system.py)` --uses--> `IRIS Agent`  [EXTRACTED]
  ingest_game_system.py → SACREDSPACE_OS_BRIEFING.md

## Hyperedges (group relationships)
- **The Sacred Council (AI Seats)** — council_the_forge, council_the_anvil, council_sacred_smith, council_deep_well, council_the_architect, council_grama [EXTRACTED 1.00]
- **Agent Layer Implementation Agents** — agent_iris, agent_aurora, agent_elias, agent_asher, agent_hermes [EXTRACTED 1.00]
- **Sacred Sigil Terminal Frontend** — sst_react_component, sst_pwa, sst_chrome_extension, sst_cmdk [EXTRACTED 1.00]
- **Game Layer Core Mechanics** — sacred_path_tarot, arcana_grid, silent_echo, nine_gates, the_serpent, memory_motes, nameless_door [EXTRACTED 1.00]
- **Flash Drive Infrastructure Protocol** — flash_drive_scaffold, flash_drive_populate, flash_drive_backup, flash_arcana_populate, flash_link_check [EXTRACTED 1.00]
- **Data Persistence Layer** — supabase_schema, chromadb_vector, sqlite_memory, sacredspace_canon_collection, chroma_ingestion [INFERRED 0.85]
- **CopyQ Pillar-Mapped Tab System** — copyq_tab_forge, copyq_tab_codex, copyq_tab_vault, copyq_tab_council, copyq_tab_market, copyq_tab_learning, copyq_tab_memory, copyq_tab_inbox [EXTRACTED 1.00]

## Communities (16 total, 8 thin omitted)

### Community 0 - "CopyQ Tab System"
Cohesion: 0.13
Nodes (22): Tab: CODEX (Canon/Spells), Tab: FORGE (Active Session), Tab: INBOX (Raw Catch-All), Tab: LEARNING (Study Notes), Tab: MARKET (Social/Listings), Tab: MEMORY (Mote Candidates), Tab: VAULT (Obsidian Clips), CopyQ Tab System (FORGE, CODEX, VAULT, COUNCIL, MARKET, LEARNING, MEMORY, INBOX) (+14 more)

### Community 1 - "Data Ingestion Pipeline"
Cohesion: 0.12
Nodes (18): IRIS Agent, Markdown Section Chunking Strategy, YAML Frontmatter Parser, ChromaDB Ingestion Pipeline (ingest_game_system.py), ChromaDB Vector Search, The Anvil (Claude Code), Jeanie (Council Member), Local-First Architecture (Zero Paid APIs) (+10 more)

### Community 2 - "Game Layer Mechanics"
Cohesion: 0.14
Nodes (16): Arcana Grid (4x3 Board, 9x9 Grid, Metatron's Node), Game Layer (Board/Card Game), Nameless Door (Trial of Silence), Nine Gates Progression System, Sacred Path Tarot (78-card), Silent Echo Gematria Engine, Weaver Engine (Spell Execution), artifacts table (Sacred Bazaar) (+8 more)

### Community 3 - "Flash Drive Infrastructure"
Cohesion: 0.18
Nodes (7): ARCANA_LANDSCAPES Art Asset Directory, Asset Prefix Mapping (SIG_, CHAR_, ENV_, etc), Communal Portal (PORTAL/), Flash Drive Link Health Check Protocol, Nine-Pillar Directory Tree on Flash Drive, SACRED_ENV.env Configuration, SHARED_SPACE (Taylor x Jeanie)

### Community 4 - "Sacred Sigil Terminal"
Cohesion: 0.22
Nodes (9): copyq_routes.py, FastAPI Spine (port 8888), Sacred Sigil Terminal v2.0, sigil_terminal_backend FastAPI, Chrome Extension (v3), Cmd+K Keyboard Shortcut, PWA (Service Worker + Manifest), Query Parser (Keyword-Based NLP) (+1 more)

### Community 5 - "NotebookLM Canon Migration"
Cohesion: 0.22
Nodes (9): Notebook: 01_SACRED_CORE, Notebook: 02_LORE_VAULT, Notebook: 03_GAME_SYSTEMS, Notebook: 04_KNOWLEDGE_VAULT, Notebook: 05_FAMILY_LEGACY, Notebook: 06_CREATION_LAB, NotebookLM Canon Migration (prep_notebooklm.py), Notebook Routing Rules (6 notebooks) (+1 more)

### Community 6 - "Council Grove & Neural Forest"
Cohesion: 0.33
Nodes (6): Tab: COUNCIL (AI Outputs), Ollama Local LLM Orchestration, 02 COUNCIL_GROVE, 03 NEURAL_FOREST, Dimension: FOREST (Neural), Dimension: GROVE (Council)

### Community 7 - "Hermes & GR∆M∆ Cipher"
Cohesion: 0.67
Nodes (3): Hermes Agent, GR∆M∆ (Hermes Cipher Sage), The Sacred Smith (Claude Desktop + Hermes MCP)

## Knowledge Gaps
- **50 isolated node(s):** `WSL2 Ubuntu on Lenovo Legion Y520`, `Mission Control Dashboard (port 3001)`, `OmniParse Document Parser (port 8001)`, `In Lakesh Alakin (Canon Closing)`, `The Forge (Claude)` (+45 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Nine Pillars` connect `CopyQ Tab System` to `Data Ingestion Pipeline`, `Flash Drive Infrastructure`, `Sacred Sigil Terminal`, `Council Grove & Neural Forest`?**
  _High betweenness centrality (0.410) - this node is a cross-community bridge._
- **Why does `SacredSpace OS` connect `Data Ingestion Pipeline` to `CopyQ Tab System`, `Game Layer Mechanics`, `Sacred Sigil Terminal`, `Council Grove & Neural Forest`?**
  _High betweenness centrality (0.262) - this node is a cross-community bridge._
- **Why does `Game Layer (Board/Card Game)` connect `Game Layer Mechanics` to `Data Ingestion Pipeline`?**
  _High betweenness centrality (0.199) - this node is a cross-community bridge._
- **What connects `Local-First Architecture (Zero Paid APIs)`, `WSL2 Ubuntu on Lenovo Legion Y520`, `Mission Control Dashboard (port 3001)` to the rest of the system?**
  _51 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CopyQ Tab System` be split into smaller, more focused modules?**
  _Cohesion score 0.1341991341991342 - nodes in this community are weakly interconnected._
- **Should `Data Ingestion Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.11764705882352941 - nodes in this community are weakly interconnected._
- **Should `Game Layer Mechanics` be split into smaller, more focused modules?**
  _Cohesion score 0.14166666666666666 - nodes in this community are weakly interconnected._