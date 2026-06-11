---
title: Game System Index — Jenga's Journey
pillar: 04_SACRED_CODEX
status: canon
agent: IRIS
tags: [game-system, index, jenga, season-1]
created: 2026-05-03
---

# Jenga's Journey — Sacred Codex Game System

SacredSpace is not a game you play. It is a game you *are*. The interface is the Oracle. The mechanics are the OS. Every spell cast echoes through the Neural Forest. Every archetype met is a part of Jenga already known.

## What This Is

**Jenga's Journey** is Season 1 of the SacredSpace interactive experience. The protagonist, Jenga, enters the SacredSpace to find her soul's truth. She travels through 12 archetypal encounters, each embodied by a living NPC, each tied to a Tarot card of the Major Arcana. Above them all stands Metatron — the Law — who neither plays nor loses but witnesses everything.

The game is the first human interface to SacredSpace OS. Every mechanic routes through IRIS. Every narrative is retrieved from this Codex. Every action taken by Jenga updates the Neural Forest graph.

## System Architecture

```
Player Action
    ↓
FastAPI Game Endpoints (/api/game/*)
    ↓
IRIS Agent (queries this Codex via ChromaDB)
    ↓
Narrative returned to player
    ↓
Memory Motes updated in Neural Forest
```

## The Four Schools

Jenga's power grows through four magical schools. Each is guarded by one of the SacredSpace agents.

| School | Guardian | Element | Core Truth |
|---|---|---|---|
| [[SCHOOLS/SCHOOL_INITIATION]] | ELIAS | Fire | The courage to begin |
| [[SCHOOLS/SCHOOL_COURAGE]] | ASHER | Earth | Facing what is real |
| [[SCHOOLS/SCHOOL_MYSTERY]] | IRIS | Water | Wisdom in the hidden |
| [[SCHOOLS/SCHOOL_CREATION]] | AURORA | Air | Making the invisible visible |

## The Thirteen Archetypes

Metatron holds the frame. Twelve archetypes embody the journey.

| Archetype | Card | NPC | Soul Tone |
|---|---|---|---|
| [[ARCHETYPES/METATRON_LAW]] | The Law | Metatron | 0 |
| [[ARCHETYPES/ARCHETYPE_00_THE_FOOL]] | 0 — The Fool | Meridian | 22 |
| [[ARCHETYPES/ARCHETYPE_01_THE_MAGICIAN]] | I — The Magician | Vael | 1 |
| [[ARCHETYPES/ARCHETYPE_02_THE_HIGH_PRIESTESS]] | II — The High Priestess | Seren | 2 |
| [[ARCHETYPES/ARCHETYPE_03_THE_EMPRESS]] | III — The Empress | Maeve | 3 |
| [[ARCHETYPES/ARCHETYPE_04_THE_EMPEROR]] | IV — The Emperor | Kethras | 4 |
| [[ARCHETYPES/ARCHETYPE_05_THE_HIEROPHANT]] | V — The Hierophant | Oran | 5 |
| [[ARCHETYPES/ARCHETYPE_06_THE_LOVERS]] | VI — The Lovers | Tandem | 6 |
| [[ARCHETYPES/ARCHETYPE_07_THE_CHARIOT]] | VII — The Chariot | Zael | 7 |
| [[ARCHETYPES/ARCHETYPE_08_STRENGTH]] | VIII — Strength | Lune | 8 |
| [[ARCHETYPES/ARCHETYPE_09_THE_HERMIT]] | IX — The Hermit | Eldra | 9 |
| [[ARCHETYPES/ARCHETYPE_10_WHEEL_OF_FORTUNE]] | X — Wheel of Fortune | Khepri | 10 |
| [[ARCHETYPES/ARCHETYPE_11_JUSTICE]] | XI — Justice | Mira | 11 |

## The Eight Sacred Nodes

Locations in the SacredSpace where archetypes manifest and convergence is possible.

| Node | Guardian | Unlock Condition |
|---|---|---|
| [[NODES/NODE_01_THE_THRESHOLD]] | The Threshold | Automatic — all seekers begin here |
| [[NODES/NODE_02_THE_FOOLS_BRIDGE]] | Meridian | Step without looking |
| [[NODES/NODE_03_THE_ORACLE_ARCHIVE]] | ORACLE-7 | Ask a question you don't want answered |
| [[NODES/NODE_04_THE_VOID_GATE]] | Lyra | Transform — change your fundamental nature |
| [[NODES/NODE_05_THE_COUNCIL_GROVE]] | All four school guardians | Master at least one spell from each school |
| [[NODES/NODE_06_THE_SIGIL_FORGE]] | ELIAS | Inscribe your first original sigil |
| [[NODES/NODE_07_THE_NEURAL_FOREST]] | IRIS | Form three semantic links between motes |
| [[NODES/NODE_08_THE_CONVERGENCE]] | Metatron | Complete all 12 archetype encounters |

## The Twelve Episodes

[[EPISODES/EPISODES_GUIDE]] — how each archetype appears in Jenga's Season 1 journey.

## Design Canon (Locked)

- **Courage failure:** Failure teaches the spell faster. Each failed cast leaves a scar that becomes power. (Option D)
- **Void safety:** Only those who have fundamentally transformed can survive the Void. Resistance kills. (Option C)
- **Shaman balance (Season 2):** Breadth costs attunement; Shamans cast all schools but slower and without depth bonuses. Specialists are Season 1; Shamans are Season 2 endgame. (Option A+D hybrid)

## In Lakesh

The game is not separate from SacredSpace OS. It is the way the OS teaches itself to be known.
