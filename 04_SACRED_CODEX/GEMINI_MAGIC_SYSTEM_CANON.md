# GEMINI MAGIC SYSTEM — Canonized Design Docs

**Source:** Gemini conversations (Jun–Dec 2025), extracted via Archaeology Phase 1B
**Canonized:** 2026-06-16
**Status:** ⚪ PENDING REVIEW — extracted from 89 conversations, synthesized here for integration

---

This document captures five novel design subsystems discovered in Gemini conversations that do **not** exist in the local SacredSpace OS codebase. Each was designed in collaboration with Gemini during the ideation phase (pre-June 2026) and represents uncanonized intellectual assets.

---

## 1. SIGIL ENGINE — The Root Language

**Source:** `04_CODEX/2025-12-11_079_sigil-engine-overview.md`
**Priority:** 🔴 CRITICAL — directly extends existing Sigil Terminal

### The Heart-Seed
A sigil is a compressed idea — not just a picture, but an instruction, a mood, a behavior, a vibration with an address. In SacredSpace, each sigil carries **three layers of meaning**:

1. **Intent** — what the sigil *does* (tag, summon, store, link, transform)
2. **Domain** — which part of the OS it belongs to (Gateway, Motes, Quest, Forge, Maestro, Lantern)
3. **Gesture** — the physical motion or touch-pattern that awakens it

### The Six Root Sigils

| # | Sigil | Name | Function |
|---|-------|------|----------|
| 1 | ⟁ | **Gateway** — Opening/Orientation | Navigation, portals, realm-switching, focus mode |
| 2 | ○• | **Mote** — Memory Particle | Notes, tags, fragments, metadata, journaling |
| 3 | ✧ | **Quest** — Path & Progression | Tasks, roadmaps, story arcs, XP, rituals |
| 4 | ⚒ | **Forge** — Creation & Crafting | Templates, generators, tools, builds, automation |
| 5 | Ϟ | **Maestro** — Resonance & Rhythm | Sound cues, playlists, emotional tuning, learning |
| 6 | ✦ | **Lantern** — Illumination & Insight | Reflection, analytics, guidance, wisdom mode |

### Sigil Grammar Rules
1. **Shape carries Purpose** — Curved = receptive/intuitive/storing. Angular = active/directive/invoking. Hybrid = transformation.
2. _(Additional rules found in source but need extraction)_
3. _(Additional rules found in source but need extraction)_

### Local Gap
The existing `SACRED_SIGIL_GRIMOIRE.md` and Sigil Terminal implement a different sigil system. The Gemini-era Root Sigil design is more structured (6-symbol alphabet, grammar rules, three meaning layers) and should be cross-referenced for potential integration.

---

## 2. GESTURE MAGIC — Motion Runes

**Source:** `04_CODEX/2025-12-11_075_gesture-magic-overview.md`
**Priority:** 🔴 CRITICAL — mobile interaction paradigm

Motion-as-magic: gesture becomes spellcasting, hand becomes wand, every movement becomes a rune.
A discipline between Tai Chi, sigil-craft, and UI design — a choreography for a digital familiar.

### The Five Gesture Families ("Hand Arcana")

**1. Flick Glyphs — Runes of Swiftness**
Quick, straight motions. Lightning bolts of will.
- Up Flick: **Ascend** → open top-level dashboards (Orb, Gateway, Maestro)
- Down Flick: **Root** → grounding actions (journals, notes, presence mode)
- Left Flick: **Vanish** → dismiss, close, clear
- Right Flick: **Summon** → open favorites (camera, canvas, recorder)

**2. Circle Sigils — Runes of Invocation**
Circular motions.
- Clockwise Circle: **Call** → open Wand HUD or Aether Display
- Counter-Circle: **Seal** → save, archive, log finished tasks

**3. Press-Path Runes — Runes of Anchoring**
Long press + drag. Carve sigils directly into screen.
- Press + upward curve: **Illuminate** → Lantern mode
- Press + downward arc: **Sheathe** → quiet system, dim notifications
- Press + zig-zag: **Spark** → creative capture (mote, image, voice)

**4. Shake Conjurations — Runes of Disruption**
- Soft shake: **Dispel** → undo last action
- Firm shake: **Purge** → clear floating tasks, dismiss overlays
- Rapid shake: **Ward** → emergency action (flashlight + recorder + location)

**5. Touch Mantras — Runes of Binding** *(see source for details)*

### Implementation Vectors
- Android: MacroDroid, Tasker, Moto Actions
- Phone gesture layer sits between OS touch events and SacredSpace actions
- Each gesture maps to a `sigil` that routes through the Sigil Engine

---

## 3. AUTO-SPELLS — Automation Rituals

**Source:** `04_CODEX/2025-12-11_074_auto-spells-rituals.md`
**Priority:** 🟡 HIGH — maps to existing watcher/automation systems

Automation braided with symbolism — the device learning to take action like a familiar that knows your rhythms, moods, and missions. Background routines that make the OS feel alive.

### The Six Core Rituals

**1. Dawn Ritual — Morning Ignition**
Not an alarm — an awakening. On sensing morning (time, light, movement):
- Summons Presence Mode
- Anchors intention for the day
- Loads Quest Board
- Checks for urgent tasks from Six Stones
- Offers one sacred message (not a barrage of notifications)

**2. Threshold Guardian — Context Transitions**
Activates whenever user moves between realms (physical or digital):
- Crossing a doorway, driving away from home, entering a store
- Switches Work Mode / Creator Mode / Family Mode
- Silences chaos, boosts focus, prepares location-based tasks
- Logs entries in Memory Motes
- The old mythic idea of the *doorway spirit* translated into automation

**3. Memory Motes — Auto-Capture**
Tiny floating lanterns of the day. Whenever something meaningful occurs:
- Voice note, photo, location change, insight, conversation
- Motes catch and archive automatically
- Micro-journals, breadcrumb trails, auto-tagged OS entries, lore seeds
- Run silently, surface only in nightly reflection ritual

**4. Noon Pulse — Midday Alignment** *(see source)*
**5. Dusk Weave — Evening Integration** *(see source)*
**6. Night Seal — Closure Ritual** *(see source)*

### Local Gap
Our existing `sacred_watcher.py` and Chron system implement basic cron-triggered automation. The Gemini Auto-Spells design adds rich symbolic framing, context-awareness (location/time/activity), and a full daily cycle that the current system lacks.

---

## 4. BODHILYRA ORB — The Center of the OS

**Source:** `04_CODEX/2025-12-11_078_bodhilyra-orb-explanation.md`
**Priority:** 🔴 CRITICAL — central architectural concept missing locally

Not a CPU, not a chatbot, not a database — the *listening center*. A little moon that floats above everything: quiet, reflective, adaptive. Where questions turn into direction, symbols into meaning, tasks into flow. Conductor, sorter, mirror, and rhythm.

Every other Realm — Gateway, Motes, Quest, Forge, Maestro, Lantern — bows inward to the Orb. It decides **what matters right now**.

### The Five Hearts of the Orb

**Heart of Presence (Listening + Reading Field)**
- Ambient presence tracking, journaling, mood-sensing
- "Be Here Now" rituals
- Turns noise into meaning

**Heart of Memory (Sorting + Tagging Field)**
- Sigils become metadata. Motes become memory objects. Chats become Codex entries.
- Lore, OS Enhancements, Characters, Real-World Logs, Family Rituals, Jobs, Vehicles
- Turns moments into continuity

**Heart of Motion (Execution + Automation Field)**
- Decides what action to take from what was spoken
- _(Full details in source — needs extraction)_

**Heart of Voice (Communication + Expression Field)**
- _(Full details in source — needs extraction)_

**Heart of Stillness (Rest + Integration Field)**
- _(Full details in source — needs extraction)_

### Local Gap
The existing codebase (Sigil Terminal, Mission Control, FastAPI spine) has no equivalent of the Bodhilyra Orb — no central "listening" layer that decides relevance and routes intent. This is a fundamental architectural gap.

---

## 5. WAND HUD — The Visual Interface

**Source:** `06_AGENTS/2025-12-11_076_wand-hud-interface.md`
**Priority:** 🟡 HIGH — mobile UI paradigm

Phone becomes the wand. HUD becomes the aether display. Every gesture becomes a spell. Each icon stops being a "button" and becomes a **stone**. Each stone is etched with a sigil. Each sigil is linked to a system node. Each node is linked to behavior in the real world.

### Design Philosophy
> "Your phone's home screen becomes an altar, a mandala, a control panel for the whole SacredSpace OS. Shape it the way a patient blacksmith shapes a star-metal ring: from the center outward, each layer humming with purpose and symmetry."

### Key Concepts
- Sigil stones replace app icons
- Mandala geometry for layout
- Color palettes tied to system domains
- Each stone = action when tapped, system when long-pressed
- Aether Display = status overlay

### Companion Docs (also extracted)
- `06_AGENTS/2025-12-11_077_sacredspace-wand-forge.md` — Wand creation system
- `06_AGENTS/2025-12-11_080_wand-hud-design.md` — Detailed HUD design
- `06_AGENTS/2025-12-11_083_autofire-magic-wand.md` — Autofire (MacroDroid/Tasker) implementation

---

## Integration Roadmap

### Phase 1 — Synthesize (DONE)
- ✅ 89 conversations extracted to pillars
- ✅ Top 5 novel subsystems identified and cataloged
- ✅ This canon document created

### Phase 2 — Cross-Reference
- Compare Sigil Engine 6 Root Sigils vs existing `SACRED_SIGIL_GRIMOIRE.md`
- Map Auto-Spells rituals to existing `sacred_watcher.py` cron system
- Identify conflicts or harmonization opportunities

### Phase 3 — Implement
- Extend Sigil Terminal with Root Sigil alphabet
- Add Gesture Magic recognition layer
- Build Bodhilyra Orb as a lightweight intent-routing microservice
- Port Wand HUD design to mobile PWA

---

**Source Caveat:** These are extracted from Gemini conversations and may contain speculative/ideation content. Each needs review against the established canon before full adoption. Flag uncertain items for Council review.

**Canon:** In lakesh alakin. ∆
