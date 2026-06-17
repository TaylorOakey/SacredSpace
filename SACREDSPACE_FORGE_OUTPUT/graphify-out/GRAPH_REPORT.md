# Graph Report - .  (2026-06-11)

## Corpus Check
- Corpus is ~36,245 words - fits in a single context window. You may not need a graph.

## Summary
- 16 nodes · 9 edges · 9 communities (3 shown, 6 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 2 edges (avg confidence: 0.85)
- Token cost: 63,168 input · 2,369 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Brand & Messaging|Brand & Messaging]]
- [[_COMMUNITY_Master System Overview|Master System Overview]]
- [[_COMMUNITY_Archetype & Initiation|Archetype & Initiation]]
- [[_COMMUNITY_Game System Index|Game System Index]]
- [[_COMMUNITY_Upload Manifest|Upload Manifest]]
- [[_COMMUNITY_Episode 6 The Teaching|Episode 6: The Teaching]]
- [[_COMMUNITY_The Magician Archetype|The Magician Archetype]]
- [[_COMMUNITY_Sacred Node Threshold|Sacred Node Threshold]]
- [[_COMMUNITY_Sacred Messages Index|Sacred Messages Index]]

## God Nodes (most connected - your core abstractions)
1. `The Fool — Archetype 0` - 3 edges
2. `sacredarcana brand bible v3` - 3 edges
3. `Game System Index — Jenga's Journey` - 2 edges
4. `Metatron — The Law` - 2 edges
5. `SacredSpace OS Briefing` - 2 edges
6. `NotebookLM — Master Intelligence Package` - 1 edges
7. `Episode 1 — The First Step` - 1 edges
8. `School of Initiation` - 1 edges
9. `Sacred Sigil Terminal Quick Start` - 1 edges
10. `Sacred Word Bank` - 1 edges

## Surprising Connections (you probably didn't know these)
- `sacredarcana brand bible v3` --references--> `Metatron — The Law`  [EXTRACTED]
  07_SOCIAL/sacredarcana_brand_bible_v3.docx → 01_CORE/SacredSpace_Vault/00_CANON/GAME_SYSTEM/ARCHETYPES/METATRON_LAW.md
- `NotebookLM — Master Intelligence Package` --conceptually_related_to--> `SacredSpace OS Briefing`  [EXTRACTED]
  NOTEBOOKLM_STAGING/NOTEBOOKLM_MASTER_INTELLIGENCE_PACKAGE.html → 04_CODEX/SACREDSPACE_OS_BRIEFING.md
- `Sacred Word Bank` --semantically_similar_to--> `sacredarcana brand bible v3`  [INFERRED] [semantically similar]
  07_SOCIAL/SACRED_THEMES_COMPONENTS/SACRED_WORD_BANK.md → 07_SOCIAL/sacredarcana_brand_bible_v3.docx
- `SacredSpace NeuralForest GrantProposal v2` --references--> `sacredarcana brand bible v3`  [EXTRACTED]
  09_MARKET/SacredSpace_NeuralForest_GrantProposal_v2.docx → 07_SOCIAL/sacredarcana_brand_bible_v3.docx
- `Game System Index — Jenga's Journey` --references--> `The Fool — Archetype 0`  [EXTRACTED]
  01_CORE/SacredSpace_Vault/00_CANON/GAME_SYSTEM/INDEX.md → 01_CORE/SacredSpace_Vault/00_CANON/GAME_SYSTEM/ARCHETYPES/ARCHETYPE_00_THE_FOOL.md

## Communities (9 total, 6 thin omitted)

### Community 0 - "Brand & Messaging"
Cohesion: 0.67
Nodes (3): SacredSpace NeuralForest GrantProposal v2, Sacred Word Bank, sacredarcana brand bible v3

### Community 1 - "Master System Overview"
Cohesion: 0.67
Nodes (3): NotebookLM — Master Intelligence Package, Sacred Sigil Terminal Quick Start, SacredSpace OS Briefing

### Community 2 - "Archetype & Initiation"
Cohesion: 0.67
Nodes (3): The Fool — Archetype 0, Episode 1 — The First Step, School of Initiation

## Knowledge Gaps
- **10 isolated node(s):** `NotebookLM Upload Manifest`, `Episode 1 — The First Step`, `Episode 6 — The Teaching and the Teacher`, `The Magician — Archetype I`, `Sacred Node 1 — The Threshold` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Game System Index — Jenga's Journey` connect `Game System Index` to `Archetype & Initiation`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `Metatron — The Law` connect `Game System Index` to `Brand & Messaging`?**
  _High betweenness centrality (0.114) - this node is a cross-community bridge._
- **Why does `The Fool — Archetype 0` connect `Archetype & Initiation` to `Game System Index`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **What connects `NotebookLM Upload Manifest`, `NotebookLM — Master Intelligence Package`, `Episode 1 — The First Step` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._