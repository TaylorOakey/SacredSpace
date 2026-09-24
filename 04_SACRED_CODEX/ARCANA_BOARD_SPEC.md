# ∆∆∆ THE ARCANA BOARD — MECHANICAL SPEC & REALITY LAYER ∆∆∆
## ARCANA-BOARD-001 · Game, Board, and Physical/Digital Bridge

**Status:** DISTILLED — Reported, largely unverified · Not a Canon Gate ruling
**Sourced from:** Two "architect session" outputs pasted directly into this session on 2026-09-23/24 (the ARCANA-BOARD-001 synthesis and its eight-version build history), a second independent session ("Claude Desktop," reporting local disk access to `04_SACRED_CODEX/game/`), and a "SacredSpace Reality Layer" exploration prompt pasted alongside them. None of these three sources are this session — I have not read the underlying engine files (`deck.py`, `arcana_board.py`, `grid.py`, `trials.py`, `classes.py`, `conflicts.json`, `UNFURLING_THE_INFINITE_VISION.md`, `cipher_engine.py`) myself. They live under `04_SACRED_CODEX/game/` on a machine or repo not attached to this session (this repo, `TaylorOakey/SacredSpace`, does not contain them — checked 2026-09-24).
**Consolidated:** 2026-09-24
**Canonical Path:** `04_SACRED_CODEX/ARCANA_BOARD_SPEC.md`
**Machine-readable companion:** `09_SACRED_MARKET/arcana_grid/game_data.json` (`arcana_board_reported` block)
**Related canon:** `04_SACRED_CODEX/SACRED_STORYLINE_CANON.md` (narrative canon — §0 ledger items 4, 5, and new items 14–15 cross-reference this doc) · `03_NEURAL_FOREST/skills/sacredspace-arcana-grid/SKILL.md` (locked 12-Archetype Grid — distinct from the 9×9/12×12 board topology described here)

---

## Canon Gate Check (per `sacredspace-canon-gate`)

| Check | Result | Notes |
|---|---|---|
| **Named** | ✓ Pass | "The Arcana Board" / "ARCANA-BOARD-001." Stable across the two architect-session outputs. |
| **Sourced** | ⚠ Partial | Traceable to specific pasted sessions and, where cited, specific file:line references (`conflicts.json:53-108`, `deck.py:45`, `trials.py:182-228`, `classes.py:65-180`, `UNFURLING_THE_INFINITE_VISION.md:73`). None of those citations have been independently read by me — this is a report of a report in most cases, sometimes a report of a report of a report. Treat every citation below as **reported, not verified**, until someone with the actual files confirms it. |
| **Bounded** | ⚠ Partial | The mechanical spine (draw → seed → place → qualify → echo; 9×9 tactical / 12×12 confluence layers; eight Trials) is bounded and internally consistent across sources. The Reality Layer section is explicitly a menu of unresolved design options (ontology, narrative binding, state architecture), not a bounded spec — see that section. |
| **Tested** | ✗ Fail | Nothing here has been run, played, or built against in this repo. The one piece confirmed live elsewhere is the Game Interface artboard on Taylor's Design canvas (Oracle draw → Trial resolution), which is outside this repo's reach. |
| **Compatible** | ⚠ Partial | Confirmed compatible with existing canon: the 78-card deck (22 Major/56 Minor), Metatron as a structural presence, four named elemental companions (though see the companion tangle below), and the 12-Archetype Grid as the deeper structural law underneath the board. **Not yet reconciled**: Sacred Class names (8: Flamebearer/Echowalker/Grovekeeper/Veilsmith/Harmonic/Lanternborn/Tidecaller/Ashen Witness) vs. the canon-locked 12 Archetypes (4×3) — two different cardinalities describing what may be the same slot. |
| **Stored** | ✓ Pass (as of this doc) | Previously scattered across at least four separate AI sessions' outputs, pasted into chat. Now stored at `04_SACRED_CODEX/`. |

**Verdict:** Gate does not pass — **stored as DISTILLED**, well below CANON. Treat this document as an organized index of claims to verify, not a ruling on any of them. Where this doc's claims conflict with `SACRED_STORYLINE_CANON.md`, that document's existing resolutions stand; this doc adds detail and new open items rather than overriding anything already gated.

---

## Ground-Truth Note

One of the source sessions did independently verify several claims against real Google Drive documents (the "[03] SacredSpace Game Integration" export, the "Arcana Grid: game idea" concept doc, "SACREDSPACE: MASTER COMPILATION," and the earliest known design document, "A SACREDSPACE — The Blueprint for the SACRED GAME," dated 2025-10-31). That verification is *not* the same as this session verifying it — I have not read those Drive documents myself in this pass. What that source reports as confirmed-by-direct-read:
- The core loop **"Receive Guidance → Take the Journey → Face the Consequence."**
- The 78-card deck.
- Three named victory paths: **Awakening, Harmony, Dominance.**
- The Act I Starter Set's jungle hex-grid, crystal/herb/wood/clay tokens, and QR-linked lore, matching a real document word-for-word.

Same source also reports the Blueprint **complicates** two things this spec otherwise treats as settled: the board was never fixed at 9×9 there — it floats 7×7, 9×9, and 19×19/13×13 Go-style options without choosing — and Metatron appears there only once, as card-art geometry, not as a rule or a never-drawn Throne card. That framing is a later addition somewhere downstream of the earliest document, not traceable to it.

---

## Purpose

The Arcana Board is reported as one surface functioning simultaneously as tarot table, tactical game, story engine, ritual interface, and memory portal, with tarot as procedural authority (it drives state changes) rather than decorative flavor. Archetypal spine: **Root → Threshold → Return** — one draw, one placement, one consequence, one Echo, at every scale from a single card scan to a full campaign.

## Player Interaction — The Loop

**Draw → Seed → Place & Shape → Qualify → Echo.**

- A draw comes from the 78-card deck (physical or digital), via one of several named spreads: Three-Fold (learning), Four Realms (balance check), Arcana Quest's Call→Return (campaign), Silent Echo's Spark→Echo (ritual play).
- The first three cards drawn seed the board deterministically — terrain, then special-cell count/kind, then an encounter near the Throne.
- Players then claim cells, spend Realm resources, and trace geometry; the board grades the resulting pattern by deviation rather than pass/fail.
- Passage through **the Nameless Door (Trial 6)** is reported to require states of being, not a score: a specific tone known, at least one healed Scar carried, no unsealed Fracture held, and approach without fear. (Cited to `trials.py:182-228` — reported, unverified.)
- Every draw, placement, and decision logs as an **Echo** (session, player, timestamp, location, draw, decision) so the board can recognize repeat visits.

This maps onto the Pulse → Step → Rite → Seal language already in the footer of the Game Interface board on Taylor's Design canvas.

## Rules

- **Players:** 1–4 initiates plus an optional Guide.
- **Win/lose:** win by completing the called Trial or closing the Quest arc; lose by a grid-collapse condition (tied to Trial 5) or a Door refusal with no remaining path.
- **Turn structure:** draw-or-move, then two actions (place a resource node, shape a flow, or invoke a suit effect), then a Shadow Phase where board state decays on an exponential curve and re-bands into one of five states: Active, Recent, Stable, Fading, Decayed.
- **Tarot binding:** a Major drawn on a Gate cell triggers a reading and an Oversoul check; a Minor or Court card pays its Realm's effect at a fixed multiplier.
- **The Metatron constraint (reported absolute, all versions seen):** the Frame Card sits face-up at the Throne, is never shuffled into the deck, never drawn, never a waypoint. Any rule that would draw it is out of bounds. *(Contrast the Ground-Truth Note above: the earliest 2025-10-31 Blueprint doesn't support this framing — worth flagging to Taylor as a possible later invention rather than original design.)*
- **Reported, unverified:** stable configurations on the 9×9 tactical board can promote onto the 12×12 layer for additional scoring without replaying them. This is a *new* claim beyond the already-resolved dual-layer architecture (`SACRED_STORYLINE_CANON.md` §0 item 4) — needs Taylor's confirmation before anyone builds against it.

## Data Model

Reported as the shape the live engine already writes — **not** independently confirmed against the engine code, so treat field names as a build target to verify, not an implemented contract:

```json
{
  "board": {
    "layer": "tactical_9x9 | confluence_12x12",
    "cells": [
      {"x": 1, "y": 1, "state": "EMPTY|OCCUPIED|ENEMY|SCAR|GATE|THRONE", "biome": "neutral|order|chaos|harmony|void", "resonance": 0.83, "band": "ACTIVE", "last_touched": 12}
    ]
  },
  "seed": {
    "cards": [{"num": 9, "name": "The Lantern", "realm": "major", "element": "spirit"}],
    "terrain_from": 0,
    "specials_from": 1,
    "encounter_from": 2
  },
  "pattern": {"type": "pentagram", "cells": [[2, 7], [5, 2]], "deviation": 0.08},
  "trial": {"index": 6, "name": "The Nameless Door", "passed": false, "refusals": ["holds unsealed Fracture"]},
  "echo": {"session": "s-...", "player": "Initiate", "qr_ts": "...", "pulse": "arcana.card_drawn", "memory_ref": "mote-..."}
}
```

Engine keys named alongside it (reported, not read): `deck.DeckEngine`, `arcana_board` (9×9 state, pattern detectors, decay), `grid` (12×12 wells and ley lines), `trials` (Door predicates), plus `game_engine` events and `oversoul_engine.record_arcana_encounter`.

## Lore Hooks

Worth preserving regardless of whether every mechanic checks out:
- The Throne makes Metatron-as-Law *sittable* — occupying it means being witnessed, not winning.
- Open Major Arcana seats are framed as incoming, not missing — consistent with how the deck is talked about elsewhere in canon.
- Memory decay on an exponential curve is forgetting rendered as mechanic, with a named restoration card as counterweight — grace as mechanic, not just reading.
- Card-embedded Glyph Portals resolving to other living objects (a piece of lore, a song, an NPC, a prior Echo) rather than containing content themselves is consistent with the Reality-Layer cosmology (below): QR-carrying physical cards sit at the Threshold layer between the game's Experience layer and the real world.

## Production Priority (reported build order)

- **P1** — one-page rules card + scripted three-card seed demo on the existing tactical board. No art; unblocks a playtest.
- **P2** — playtest harness: full Trials, Door-refusal cases, decay-band assertions. Gates all further work.
- **P3** — physical pilot of the Act I Starter Set (jungle hex-grid, four-resource tabletop). Tracked as its own SKU, cross-referenced against this spec rather than merged into it — it's a genuinely different manifest (physical tabletop vs. digital tactical board).
- **P4** (gated on P2) — 12×12 Confluence layer + AR overlays.

The Game Interface artboard on Taylor's Design canvas already covers a slice of P1 in digital form (Oracle draw resolving a Trial step) — doesn't need rebuilding from scratch.

---

## Open Conflicts Carried Forward

None resolved by this document — surfaced for Taylor's Canon Gate, not decided here.

1. **Slot VIII naming — three-way, not two-way.** Two pasted sessions call it "Rootwalker" (one citing `deck.py:45` and `UNFURLING_THE_INFINITE_VISION.md:73`). Multiple uploaded documents from an earlier session say it has no name on record, deliberately unnamed. The real 2025-10-31 Blueprint — the earliest document on file — calls it **"The Flame,"** explicitly labeled there as a "Sample List — we can finalize with you later." None of the three agree, and the Blueprint's own hedge suggests even the earliest version never intended this as final. `deck.py:36-59` needs to actually be read before treating any of the three as settled.
2. **The 9×9/12×12 "seal" claim needs Taylor's direct confirmation.** This spec's source reports the board-topology split was "sealed on 2026-09-18" via Taylor's own delegation, bound by a `map_9_to_12` function, and cites `conflicts.json:53-108`. If real, this resolves something adjacent to (but distinct from) the already-resolved architecture question in `SACRED_STORYLINE_CANON.md` §0 item 4 — that item resolved *why* the board is dual-layer (an engineering ruling), not that a specific promotion function was since sealed. A pasted transcript reporting a seal event is not the same as Taylor confirming one happened. Also worth noting: at least one primary source (the Blueprint) uses "sealed" to mean a finished Codex/lore volume closed with a ritual seal — not a locked game rule — so even if this seal is real, confirm which sense of the word applies.
3. **Minor Arcana suit names — at least three lineages, not one.** (a) Leaves/Relics/Crystals/Shards (Jungle/City/Grove/Shadow) — confirmed by direct read in the Blueprint, the "[03] FULL EXPORT" chat, and the Master Compilation. (b) A second scheme in the *same* Blueprint document: Earth→Roots, Water→Flow, Fire→Sparks, Air→Winds. (c) A reported "sealed" Roots/Flames/Currents/Winds from a pasted session — close to (b) but not identical. Three names, not settled.
4. **Companion/animal-guide question is now a four-way tangle**, on top of the four canon Elemental Guides already locked in `SACRED_STORYLINE_CANON.md` §9 (Zii/Mylo/Auralon/Koru): the Blueprint's own archetype-animal cards (Eagle, Jaguar, Child, Sage, Trickster) match none of Zii/Mylo/Auralon/Koru, "Stag," or a reported "Rook" — and a Google Takeout export session reports yet another set (Wolf/Owl/Serpent/Deer). One thing *is* reported resolved cleanly by a second session: "Stag" isn't a fifth competing companion — it's Taylor's own **Oversoul tech-animal form**, a different register from the party's four elemental companions. That resolution is plausible and consistent with how Oversoul stages are described elsewhere, but is itself only reported, not verified against source.
5. **Sacred Class cardinality mismatch.** A reported eight Sacred Classes (Flamebearer, Echowalker, Grovekeeper, Veilsmith, Harmonic, Lanternborn, Tidecaller, Ashen Witness — cited to `classes.py:65-180`) sit alongside the canon-locked 12-Archetype Grid (4 Elements × 3 Primes). 8 ≠ 12; unclear whether Classes are a subset, a parallel system, or a draft that predates the Grid becoming canon-locked.
6. **A 53-symbol table is cited by name** in the source material but is reported as not present in the file it points to. Unresolved, not further investigated here.
7. **The Act I Starter Set's own mechanics**, beyond the resource-token blurb, remain unrecoverable from any source seen so far — a real proposal, not yet a spec.
8. **A newer Google Takeout extraction reports material not yet cross-checked against anything above**: a fuller 5-phase turn (Exploration Roll → Move → Tarot Phase → Shadow Phase → End Turn) that may supersede the simpler Pulse/Step/Rite framing; a worked resource economy (Life Herbs, Metal Relics, Spirit Crystals, Obsidian Shards, each with distinct spend-paths, plus three trader types); Catan-style number tokens driving production; a Master/Adept initiation layer; Silent Echo rules with explicit prohibitions (no advice, diagnosis, fixing, or shaming); a four-layer physical/narrative/symbolic/reflective model; and a full physical component list, from a fourth document ("[04] Sacred Game Artifact FULL EXPORT") not otherwise referenced here. Specific enough to read as genuine new material, not a restatement — but entirely unverified by this session, and the Major Arcana/realm/companion names in this same batch are yet another variant on top of items 1, 3, and 4 above. More pre-canon drafts, not resolutions.

---

## The Reality Layer — Exploration Prompt (design options, not a spec)

This section stays intentionally as a menu of unresolved choices, sourced from a "SacredSpace Reality Layer" exploration prompt pasted alongside the board spec. It presupposes an existing spine — Sigil Terminal Bridge, GR∆M∆ meaning engine, the Oversoul 4-stage system, Jenga's Journey, Glyph Cipher metadata, Gematria/432Hz frequency mapping — consistent with what's already in `SACRED_STORYLINE_CANON.md` §§9–11 and §15, and proposes making it physically manifest via QR codes, AR shrines, and real-world shrine-visiting.

**Ontological frame (pick one, or a hybrid) — what does it mean to enter the Sacred Universe from physical reality?**
- *Threshold Crossing:* physical and Sacred are separate domains; a QR scan is a gate between them.
- *Continuity/Overlay:* Sacred already permeates physical reality; the layer just makes it visible.
- *Co-Emergence:* physical and Sacred create each other — real interests birth archetypes that reshape how the physical world is seen.

**Narrative binding (pick one) — how does this relate to Jenga's Journey canon?**
- *A — Journey as Context:* canon already exists; you discover its truths; QR codes unlock canonical moments.
- *B — Journey as Outcome:* player choices generate the narrative that becomes canon; QR codes are waypoints recording decisions.
- *C — Parallel Emergence:* canon exists but stays open; player journeys are adjacent stories, optionally folded into future volumes.

**Mechanical layer (each needs its own choice):**
- QR payload: minimal (UUID + context type) vs. rich (full state serialization).
- Persistent state: local-first SQLite vs. cloud-sync (Obsidian/Logseq) vs. hybrid (local SQLite for gameplay + Obsidian for narrative + Sacred Pulse event bus for sync) — the hybrid option is explicitly framed against the systems already in this repo (FastAPI spine, ChromaDB, SQLite Memory Engine, Obsidian vault).
- Real→Sacred translation: explicit symbolic mapping, emergent discovery, deliberate co-creation ritual, or family-network overlap.
- Shrines: QR-only (no AR) vs. GPS-aware AR overlay vs. full multiplayer AR layer.

**GR∆M∆ worked example** (illustrates the proposed resonance formula, not confirmed against `GRAMA_Story_Arc.md`): character gematria × location gematria, mod 22, maps to a Major Arcana card — e.g. "AURORA" (56→11, Justice) at "Stone Circle" (123→6, Lovers) → (11×6) mod 22 = 0 → The Fool.

**Scenario sketches offered, not chosen:** The Shrine Map (MVP, Oversoul Stage 1 via physical shrine visits), Card as Mirror (physical tarot deck + spell practice, Stage 2–3), Nested Journey (family as fractal initiation circle across three initiates, Stage 4 teaching cycle). All three assume the Hybrid state architecture and are otherwise independent of which ontological frame or narrative-binding option gets chosen.

**Nothing in this section is decided.** It's included here, rather than left to scatter across further pasted sessions, because it names the actual decision points (ontology, binding, state architecture, translation method, shrine fidelity) precisely enough that Taylor can rule on each independently rather than accept or reject the whole prompt at once.

---

*In lakesh alakin.*
