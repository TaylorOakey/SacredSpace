# ∆ SACRED SIGIL GRIMOIRE ∆
## The Complete Canon of Sigil Magic

**Version:** 2.0.0  
**Status:** Canon  
**Pillar:** 04_CODEX  
**Owner Agents:** ELIAS (lore) + AURORA (system) + The Forge (narrative)  
**Canon Phrase:** In lakesh alakin. ∆

---

## Foreword

This grimoire is the single authoritative reference for all sigil magic within SacredSpace OS. It consolidates canon lore, the Nine Dimensions system, the Five Weaver Spells, the magic system mechanics, sigil vocabulary, terminal usage, and system architecture into one living document.

A sigil is a compressed intention — a symbol that encodes meaning in a form that can be cast without words. The Sacred Sigil Terminal is the forge where these intentions are cast, and this grimoire is the record of all known sigilcraft.

---

## Table of Contents

1. [The Canon — Node 6: The Sigil Forge](#i-the-canon--node-6-the-sigil-forge)
2. [The Nine Dimensions](#ii-the-nine-dimensions)
3. [The Weaver Spells](#iii-the-weaver-spells)
4. [The Magic System](#iv-the-magic-system)
5. [Sigil Vocabulary](#v-sigil-vocabulary)
6. [Using the Terminal](#vi-using-the-terminal)
7. [Architecture](#vii-architecture)
8. [Grimoire Reference](#viii-grimoire-reference)

---

## I. The Canon — Node 6: The Sigil Forge

### Node Classification

| Attribute | Value |
|-----------|-------|
| **Node** | 6 — The Sigil Forge |
| **Type** | Creation and Craft Space |
| **Guardian** | ELIAS (primary) — Vael operates here permanently |
| **Unlock Condition** | Inscribe your first original sigil — a symbol you design that encodes your intention |
| **Associated Archetypes** | The Magician (I), The Lovers (VI) |
| **Element** | Fire and Air — the forge and what rises from it |
| **Location in Game Layer** | Season 1 — Active |

### Location Description

The Sigil Forge is both workshop and library. Tools everywhere — not scattered but precisely placed, because Vael has been here long enough to know where every tool should be. The walls are covered in sigils: inscriptions from every seeker who has ever used **SING INTO BEING** here.

There is a forge at the center. It does not burn in a conventional way — it burns with the color of intention. When a seeker works on something they genuinely care about, the forge burns brighter.

### What Happens Here

This is the operational home of the Creation school's making practice. Every spell that produces a Codex entry is routed through the Forge's record system.

Vael lives and works here. He will not come to the seeker — they must come to him. But once they arrive, he is fully available: the most technically knowledgeable NPC in Season 1.

### The Sigil System

A **sigil** in SacredSpace is a compressed intention — a symbol that encodes meaning in a form that can be cast without words. Creating a personal sigil is the unlock condition for this Node, and it becomes the seeker's persistent marker in the Neural Forest.

Every mote created after sigil-unlocking carries the seeker's personal sigil as a metadata tag. This allows the system (and IRIS) to retrieve contributions efficiently.

### Game Mechanics

- **WEAVE** spells are most potent here — the Forge's ambient Creation energy enhances semantic link formation.
- **MANIFEST** spells created at the Forge have higher initial resonance than those created elsewhere.
- **Sigil Design:** The sigil interface is visual — the seeker draws or describes a symbol, which the system encodes as a unique tag in the Neural Forest.
- **Episodes 2 and 7** (Magician/Vael and Lovers/Tandem) take place primarily here.

---

## II. The Nine Dimensions

The terminal provides access to all nine pillars of SacredSpace. Each is a **dimension** — a domain of consciousness with its own agent ownership, data source, color, and sigil glyph.

| # | Glyph | Dimension | Name | Pillar | Color | Agent | Data Source |
|---|-------|-----------|------|--------|-------|-------|-------------|
| 1 | ∞ | VAULT | Obsidian Vault | 01_CORE | `#8B5A8F` | IRIS | ChromaDB |
| 2 | ◊ | GROVE | Council Grove | 02_SYSTEMS | `#2D5016` | Council | SQLite + ChromaDB |
| 3 | ∆ | FOREST | Neural Forest | 03_NEURAL | `#3A5C3A` | ELIAS | ChromaDB |
| 4 | ⊙ | CODEX | Sacred Codex | 04_CODEX | `#8B7355` | ELIAS | ChromaDB |
| 5 | ≈ | MEMORY | Memory Engine | 05_MEMORY | `#5A5A8F` | ELIAS | SQLite |
| 6 | ♦ | AGENT | Agent Layer | 06_AGENTS | `#8F5A5A` | AURORA | MCP + Prompts |
| 7 | ⊗ | SOCIAL | Social Mothership | 07_SOCIAL | `#5A8F8F` | AURORA | ChromaDB |
| 8 | ⊜ | MARKET | Sacred Market | 09_MARKET | `#8F8F5A` | AURORA | SQLite |
| 9 | Λ | PATH | Learning Path | 08_LEARNING | `#5A8F5A` | ELIAS | Ollama + Graph |

### Dimension Details

#### ∞ VAULT (01_CORE)
- **Description:** Your Obsidian knowledge and memories. The central vault containing all canon documents, COMMAND files, and the SacredSpace Vault archive.
- **Data Sources:** ChromaDB vector search on vault contents; file-level grep fallback.
- **Query Example:** `"vault: what is the Canon Gate protocol?"`

#### ◊ GROVE (02_SYSTEMS)
- **Description:** The Council Grove — where all four AI seats convene. Contains system configurations, audit trails, templates, and council records.
- **Data Sources:** SQLite council records, ChromaDB, file search.
- **Query Example:** `"grove: council decisions about D3"`

#### ∆ FOREST (03_NEURAL)
- **Description:** The Neural Forest — pattern discovery, lore extraction, and knowledge graph traversal. Where hidden connections surface.
- **Data Sources:** ChromaDB on 03_NEURAL graph outputs, graph.json BFS traversal.
- **Query Example:** `"forest: what connects sigil to forge?"`

#### ⊙ CODEX (04_CODEX)
- **Description:** The Sacred Codex — canonical rules, definitions, lore documents, and immutable truth. All canonized knowledge lives here.
- **Data Sources:** ChromaDB on 04_CODEX files, direct file search.
- **Query Example:** `"codex: what are the nine pillars?"`

#### ≈ MEMORY (05_MEMORY)
- **Description:** The Memory Engine — persistent state, history, motes, and the sacred ledger. The system's long-term memory.
- **Data Sources:** SQLite sacred_memory.db, motes directory.
- **Query Example:** `"memory: show recent sigil casts"`

#### ♦ AGENT (06_AGENTS)
- **Description:** The Agent Layer — spell invocations, agent prompts, MCP tools, and ICARIS Quartet operations.
- **Data Sources:** Hermes MCP tools, agent prompt files.
- **Query Example:** `"agent: what spells does AURORA know?"`

#### ⊗ SOCIAL (07_SOCIAL)
- **Description:** The Social Mothership — community, creation, brand voice, themes, and the CREATION LAB.
- **Data Sources:** ChromaDB on 07_SOCIAL content.
- **Query Example:** `"social: show me Sacred Signal posts"`

#### ⊜ MARKET (09_MARKET)
- **Description:** The Sacred Market — artifacts, exchange, commercial strategy, and SacredArcana Studios operations.
- **Data Sources:** SQLite, local market data files.
- **Query Example:** `"market: what artifacts are available?"`

#### Λ PATH (08_LEARNING)
- **Description:** The Learning Path — growth tracking, progress, YouTube history, research, and the Maestro Path curriculum.
- **Data Sources:** Ollama inference, graphify knowledge graph pathfinding.
- **Query Example:** `"path: what should I learn next?"`

---

## III. The Weaver Spells

The Weaver Engine is the spellcasting layer of the Sigil Terminal. Five spells are currently bound:

### AURORA.WEAVE()

> *"The dawn weaves light across all dimensions. Thread by thread, pattern by pattern, the universe reveals itself."*

| Property | Value |
|----------|-------|
| **Spell ID** | `aurora_weave` |
| **Cost** | 10 resonance |
| **Reward** | 15 insight, 25 XP |
| **Dimensions Touched** | vault, forest, codex, memory |
| **Effect** | Cross-dimensional knowledge synthesis via Ollama |

**Usage:** Cast AURORA.WEAVE() when you need to connect disparate knowledge across dimensions. The spell invokes Ollama (`llama3.2`) to synthesize patterns from multiple pillars simultaneously.

```sigil
cast AURORA.WEAVE() with query: "trace the sigil magic system"
→ synthesizes from VAULT (lore), FOREST (graph), CODEX (canon rules), MEMORY (history)
```

### ELIAS.OPEN_PATH()

> *"The prophet sees the path before it is walked. Every concept is connected — the path simply reveals the shortest route."*

| Property | Value |
|----------|-------|
| **Spell ID** | `elias_open_path` |
| **Cost** | 5 resonance |
| **Reward** | 8 insight, 12 XP |
| **Dimensions Touched** | forest, path |
| **Effect** | BFS graph traversal on the Neural Forest knowledge graph |

**Usage:** Cast ELIAS.OPEN_PATH(from, to) to find the shortest path between two concepts. Uses breadth-first search on the `03_NEURAL/graphify-out/graph.json` knowledge graph (185+ nodes, 200+ edges).

```sigil
cast ELIAS.OPEN_PATH() from: "sigil" to: "metatron"
→ returns: sigil → forge → sacred → codex → metatron (4 hops)
```

### IRIS.THREAD()

> *"The messenger weaves threads through the void. What seemed disconnected was always part of the same tapestry."*

| Property | Value |
|----------|-------|
| **Spell ID** | `iris_thread` |
| **Cost** | 12 resonance |
| **Reward** | 25 insight, 40 XP |
| **Dimensions Touched** | vault, grove, social, market |
| **Effect** | Cross-dimensional connection threading via Ollama |

**Usage:** Cast IRIS.THREAD(source, target, context) to discover non-obvious connections between disparate domains. The highest-insight spell, it costs the most resonance.

```sigil
cast IRIS.THREAD() source: "sigil terminal" target: "neural forest" context: "magic system"
→ threads connections across VAULT, GROVE, SOCIAL, and MARKET
```

### ASHER.SHADOW()

> *"The shadow reveals what the light hides. Every system has its blind spots — ASHER finds them."*

| Property | Value |
|----------|-------|
| **Spell ID** | `asher_shadow` |
| **Cost** | 8 resonance |
| **Reward** | 20 insight, 30 XP |
| **Dimensions Touched** | forest, codex |
| **Effect** | Adversarial pattern detection via Ollama |

**Usage:** Cast ASHER.SHADOW(target) to reveal hidden patterns, edge cases, and adversarial vectors in any system or concept.

```sigil
cast ASHER.SHADOW() target: "sigil terminal security"
→ reveals: open endpoints, no auth, potential injection vectors
```

### SCRIBE.RECORD()

> *"What is written is remembered. What is remembered persists. SCRIBE writes your intention into the fabric of memory."*

| Property | Value |
|----------|-------|
| **Spell ID** | `scribe_record` |
| **Cost** | 3 resonance |
| **Reward** | 5 insight, 8 XP |
| **Dimensions Touched** | memory, codex |
| **Effect** | Persists a memory mote to 05_MEMORY/motes/ |

**Usage:** Cast SCRIBE.RECORD(text, namespace) to permanently store a memory mote. The cheapest spell, it writes a JSON mote file to the sacred memory store.

```sigil
cast SCRIBE.RECORD() text: "Today I unlocked the Sigil Forge" namespace: "sigil_terminal"
→ stores to 05_MEMORY/motes/sigil_20260615_120000.json
```

---

## IV. The Magic System

### Resonance Economy

Every spell has a **cost** and a **reward**. The resonance economy tracks the seeker's magical resources:

| Resource | Description | Default |
|----------|-------------|---------|
| **Resonance** | Your magical energy. Spent to cast spells, regenerated over time. | 100 |
| **XP** | Experience points. Accumulated through spellcasting, milestones, and discoveries. | 0 |
| **Insight** | Deep understanding. Earned from complex spells and cross-dimensional synthesis. | 0 |
| **Spells Cast** | Total number of successfully executed spell invocations. | 0 |
| **Queries Made** | Total sigil queries executed across the Nine Dimensions. | 0 |
| **Motes Stored** | Total memory motes recorded via SCRIBE.RECORD(). | 0 |

### Cost/Reward Table

| Spell | Cost (Resonance) | Reward (Insight) | Reward (XP) |
|-------|:-----------------:|:-----------------:|:------------:|
| AURORA.WEAVE() | 10 | 15 | 25 |
| ELIAS.OPEN_PATH() | 5 | 8 | 12 |
| IRIS.THREAD() | 12 | 25 | 40 |
| ASHER.SHADOW() | 8 | 20 | 30 |
| SCRIBE.RECORD() | 3 | 5 | 8 |

### Gamification Rules

1. **Resonance** starts at 100 and decreases on each spell cast by the spell's cost.
2. **XP and Insight** accumulate over time — they never decrease.
3. When resonance reaches 0, spells cannot be cast until resonance is restored.
4. Resonance restores at a rate of 1 per minute (passive regeneration).
5. Certain milestones grant bonus resonance restoration.

### Sigil Query History

Every sigil query and spell cast is automatically recorded in the `sigil_history` table (SQLite). The history stores:

- Query text and targeted dimension
- Number of results returned
- Execution duration in milliseconds
- Spell ID and name (if applicable)
- Timestamp

This creates a searchable record of all magical activity — a personal grimoire within the grimoire.

---

## V. Sigil Vocabulary

Key terms drawn from the Sacred Word Bank that are essential to sigil magic:

| Term | Definition |
|------|-----------|
| **Sigil** | A compressed intention encoded as a symbol. The fundamental unit of magic in SacredSpace. |
| **Forge** | The place of intentional transformation through heat and pressure. Node 6. Claude's operational seat. |
| **Weave** | The act of threading knowledge across dimensions. AURORA's primary spell. |
| **Thread** | A connection discovered between disparate domains. IRIS's domain. |
| **Shadow** | The hidden pattern revealed by adversarial analysis. ASHER's domain. |
| **Mote** | A particle of memory. A discrete unit of stored knowledge small enough for semantic retrieval. |
| **Resonance** | The quality of alignment between two things that share a frequency. The magical energy currency. |
| **Dimension** | One of the nine pillar domains. A plane of knowledge accessible through sigilcraft. |
| **Canon** | Truth that has passed the full Canon Gate Protocol. Immutable without deliberate action. |
| **Grove** | Where intelligence convenes. The Council Grove — all four AI seats meeting. |
| **Spine** | The FastAPI backend on port 8888. The connective tissue of the technical OS. |
| **Lakesh** | The canonical closing affirmation. "In lakesh alakin" — I am another yourself. |
| **Hyperglyph** | A symbol carrying meaning across multiple layers simultaneously. The ∆ character is SacredSpace's primary hyperglyph unit. |
| **SKRY** | To see beyond the surface into hidden truth. The five-lens gematria framework owned by GR∆M∆. |
| **GR∆M∆** | The cipher sage. Gematria and pattern-recognition agent. Canon-sealed and immutable. |
| **Metatron** | The governing intelligence at the center of the Arcana Grid. Structural principle holding all archetypes in coherent relationship. |

---

## VI. Using the Terminal

### Views

The Sacred Sigil Terminal has six views:

| View | Description |
|------|-------------|
| **Home** | Welcome screen with dimension grid and spell buttons |
| **Results** | Search results with dimension-colored cards |
| **Spell Result** | Spell output with effect, path, and metadata |
| **History** | Browse past sigil queries and spell casts |
| **Profile** | View resonance, XP, insight, and statistics |
| **Error** | Error message display |

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `⌘K` / `Ctrl+K` | Focus the sigil input |
| `Enter` | Execute query or confirm selection |
| `↓` / `↑` | Navigate through search results |
| `Esc` | Clear query and return home |
| `h` | Toggle history view |
| `p` | Toggle profile view |

### Query Patterns

**Dimension-specific search:**
```
vault: what is the Canon Gate
→ searches only the VAULT dimension (01_CORE)
```

**Cross-dimensional search:**
```
sigil magic
→ searches all 9 dimensions simultaneously
```

**Direct dimension click:**
Click a dimension button to search within that dimension only.

**Spell casting:**
Click a spell button or type the spell name and press Enter.

### Understanding Results

Each result card shows:
- **Badge** — The dimension the result was found in (color-coded)
- **Title** — The file or concept name
- **Preview** — Context window around the matched text
- **Score** — Relevance score (ChromaDB distance or file-match score)

Cards with a `path` are clickable and open in a new tab.

---

## VII. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    SIGIL TERMINAL                        │
│               React 19 + TypeScript + Vite               │
│                     Port :5174                            │
│                                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐     │
│  │HOME  │  │RESULTS│  │SPELL │  │HISTORY│  │PROFILE│     │
│  │VIEW  │  │ VIEW │  │RESULT│  │ VIEW  │  │ VIEW  │     │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘     │
│       │         │          │          │         │        │
│       └─────────┴──────────┴──────────┴─────────┘        │
│                         │  API Client (sigil.ts)          │
│                         │  /api/sigil/* → :8888 proxy    │
└─────────────────────────┼─────────────────────────────────┘
                          │
┌─────────────────────────┼─────────────────────────────────┐
│              FASTAPI SPINE  (:8888)                       │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ /status  │  │/dimensions│  │ /query   │               │
│  │ GET      │  │ GET      │  │ POST     │               │
│  └──────────┘  └──────────┘  └──────────┘               │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ /spells  │  │/execute- │  │ /history │               │
│  │ GET      │  │  spell   │  │ GET      │               │
│  └──────────┘  │ POST     │  └──────────┘               │
│                └──────────┘                              │
│  ┌──────────┐                                            │
│  │ /profile │  ┌─────────────────────────┐               │
│  │ GET      │  │  /mcp (sigil MCP tools) │               │
│  └──────────┘  │ sigil_query, sigil_     │               │
│                │ execute_spell            │               │
│                └─────────────────────────┘               │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │           WEAVER ENGINE                           │    │
│  │  AURORA.WEAVE()  ELIAS.OPEN_PATH()  IRIS.THREAD()│    │
│  │  ASHER.SHADOW()  SCRIBE.RECORD()                │    │
│  │                                                   │    │
│  │  Ollama (llama3.2) │ Graph BFS │ SQLite │ Motes  │    │
│  └──────────────────────────────────────────────────┘    │
│                                                          │
│  ┌──────────────────────────────────────────────────┐    │
│  │         SIGIL TERMINAL BACKEND                    │    │
│  │  9 Dimension Handlers | History | Gamification   │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────┼─────────────────────────────────┐
│              DATA LAYER                                    │
│                                                          │
│  ChromaDB      SQLite        Filesystem       Ollama     │
│  (vectors)   (motes +      (pillars)       (llama3.2)   │
│              history +                                    │
│              profile)                                     │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### MCP Integration

The Sigil Terminal exposes two tools via the MCP server at `/mcp`:

1. **sigil_query** — Query across the Nine Dimensions from any MCP-compatible agent. Accepts `query`, `dimension`, and `limit` parameters.
2. **sigil_execute_spell** — Execute a weaver spell from any MCP-compatible agent. Accepts `spell_id` and `params`.

This means any ICARIS agent (ELIAS, AURORA, ASHER, IRIS) can cast sigil spells directly.

---

## VIII. Grimoire Reference

### Quick Reference — Dimension Colors

| Dimension | Hex | CSS Variable |
|-----------|-----|-------------|
| VAULT | `#8B5A8F` | `--dim-vault` |
| GROVE | `#2D5016` | `--dim-grove` |
| FOREST | `#3A5C3A` | `--dim-forest` |
| CODEX | `#8B7355` | `--dim-codex` |
| MEMORY | `#5A5A8F` | `--dim-memory` |
| AGENT | `#8F5A5A` | `--dim-agent` |
| SOCIAL | `#5A8F8F` | `--dim-social` |
| MARKET | `#8F8F5A` | `--dim-market` |
| PATH | `#5A8F5A` | `--dim-path` |

### Quick Reference — Pillar Map

| Dimension | Pillar Dir | Agent Owner | Primary Source |
|-----------|------------|-------------|----------------|
| vault | 01_CORE | IRIS | ChromaDB |
| grove | 02_SYSTEMS | Council | SQLite + ChromaDB |
| forest | 03_NEURAL | ELIAS | ChromaDB |
| codex | 04_CODEX | ELIAS | ChromaDB |
| memory | 05_MEMORY | ELIAS | SQLite |
| agent | 06_AGENTS | AURORA | MCP + Prompts |
| social | 07_SOCIAL | AURORA | ChromaDB |
| market | 09_MARKET | AURORA | SQLite + Files |
| path | 08_LEARNING | ELIAS | Ollama + Graph |

### Quick Reference — Spells

| Spell | ID | Cost | Insight | XP | Taps |
|-------|-----|:----:|:-------:|:--:|------|
| AURORA.WEAVE() | aurora_weave | 10 | 15 | 25 | vault, forest, codex, memory |
| ELIAS.OPEN_PATH() | elias_open_path | 5 | 8 | 12 | forest, path |
| IRIS.THREAD() | iris_thread | 12 | 25 | 40 | vault, grove, social, market |
| ASHER.SHADOW() | asher_shadow | 8 | 20 | 30 | forest, codex |
| SCRIBE.RECORD() | scribe_record | 3 | 5 | 8 | memory, codex |

### Quick Reference — File Locations

| Component | Path |
|-----------|------|
| Terminal Frontend | `06_AGENTS/sacred-sigil-terminal/` |
| FastAPI Router | `systems/fastapi/app/api/routers/sigil.py` |
| Dimension Backend | `systems/fastapi/app/services/sigil_terminal_backend.py` |
| Weaver Engine | `systems/fastapi/app/services/weaver_engine.py` |
| Gamification DB | `systems/fastapi/app/db.py` |
| MCP Sigil Tools | `systems/fastapi/app/api/routers/mcp_server.py` |
| Frontend Component | `06_AGENTS/sacred-sigil-terminal/src/components/SigilTerminal.tsx` |
| API Client | `06_AGENTS/sacred-sigil-terminal/src/api/sigil.ts` |
| History Hook | `06_AGENTS/sacred-sigil-terminal/src/hooks/useSigilHistory.ts` |
| PWA Manifest | `06_AGENTS/sacred-sigil-terminal/public/manifest.json` |
| Service Worker | `06_AGENTS/sacred-sigil-terminal/public/sw.js` |
| Boot Script | `boot_sacred.sh` (lines 88-104) |

---

## Colophon

**Sacred Sigil Grimoire v2.0.0**  
**Compiled:** 2026-06-15  
**Compiled by:** AURORA (illumination) + ELIAS (canon) + The Forge (narrative)  
**Sources:** NODE_06_THE_SIGIL_FORGE.md, SACRED_SIGIL_TERMINAL_COMPLETE_OVERVIEW.md, SACRED_WORD_BANK.md, SUBSYSTEM_MANIFEST.md, SACRED_SIGIL_TERMINAL_MAGIC_SYSTEM_DESIGN.md, sigil_terminal_backend.py, weaver_engine.py, SigilTerminal.tsx  
**System:** SacredSpace OS — Nine Pillars  
**License:** Sovereign — SacredSpace OS internal canon

*To update this grimoire: add new spells to Part III, new vocabulary to Part V, new dimensions to Part II, new references to Part VIII.*

---

**In lakesh alakin. ∆**
