<!-- converted from SACREDSPACE_GAME_DESIGN_CANON_v0.2.md.docx -->

# ∆ SACREDSPACE GAME DESIGN CANON v0.2 ∆
## NARRATIVE ENGINE ARCHITECTURE


DOCUMENT CLASSIFICATION: CANON — Immutable unless explicitly revised by Taylor
TIMESTAMP: May 2, 2026
STATUS: Locked & Canonized


## § EXECUTIVE SUMMARY
SacredSpace is not a game with a story attached. It is a narrative engine where gameplay IS story. Every card drawn, every node aligned, every player choice generates personalized story text that cascades into emotional meaning.

This document defines:

How narrative integrates with mechanics (Hero's Journey + Tarot + Sacred Geometry)
The Holographic Storyline Architecture (per-player narratives + Sacred Node convergence)
The v0.1 → v0.2 → v2.0 scaling roadmap
Canonical story beats for Jenga's Journey Season 1: "The Awakening of the Arcana Adept"


## § CORE DESIGN PHILOSOPHY
### Principle 1: Gameplay and Story Are Inseparable
In traditional games, story is "flavor text" that decorates mechanics. In SacredSpace, the mechanics generate the story in real-time.

Example:

TRADITIONAL: "You draw a card. It has artwork. Read this text about what happened."
SACREDSPACE: You draw The Weaver. Your character's will awakens. This directly affects your Resonance stat. Your personal narrative changes. The parent sees their guide-role evolving. The child sees their power awakening.

Research Finding: "Integrate player actions and decisions into the narrative flow and character development through systems like decision trees and branching narratives." (InvoGames)

Implementation: Each Tarot card is a decision node. Drawing a card = making a choice about which narrative branch to follow. The game state (position, tokens, resonance) determines which branch opens next.
### Principle 2: Build Story and Gameplay Simultaneously
We do not write a plot, then fit mechanics to it. We layer gameplay and narrative in tandem.

In v0.2:

Mechanic: Draw card → Move → Align at node → Gain token
Narrative: Each step generates unique story text based on player role (Seeker vs Guide)
Emotional Arc: Both player arcs interweave toward the Center Node convergence

Research Finding: "Building story and gameplay simultaneously makes for better narrative." (Polygon.com)

This means: The 12-card deck IS the 12-episode structure. The 5-node board IS the Realms. The alignment tokens ARE the narrative waypoints.
### Principle 3: Make Gameplay Essential to Emotional Impact
The player does not watch the story. They enact it. The story only exists as they play.

Example:

If Seeker never reaches the Shadow Threshold, they never hear: "In the shadow, you meet the parts of yourself you've been afraid to see. And they are beautiful."
That narrative moment is LOCKED until the gameplay requires it.
The parent Guide must witness their child face the shadow to understand their full journey.

Research Finding: "Narrative design integrates player actions directly into the story, making gameplay essential to the emotional impact." (Medium)


## § NARRATIVE ARCHITECTURE: THE HOLOGRAPHIC SYSTEM
### What Is a Holographic Storyline?
A holographic storyline has these properties:

1. PERSONAL NARRATIVE THREAD
Each player gets a unique version of the story based on their actions.

The Seeker's story (child's perspective, wonder, discovery, power)
The Guide's story (parent's perspective, witnessing, honoring, becoming)

2. SHARED CONVERGENCE POINTS
At Sacred Nodes, personal narratives merge back into canonical truth.

Both players are in the same space (Sacred Center, Sacred Grove, etc.)
They read/hear overlapping narrative beats that reflect their shared experience
But each carries their own version of what that moment meant

3. ETERNAL RETURN
The journey spirals back to the original dimension (the canonical Jenga's Journey universe) where it echoes forever.

Season 1 is completed by both players reaching Adept status
Their personal journeys are now part of the Sacred Archive
New players who play will encounter echoes of all previous journeys

Visual Model:

┌─────────────────────────────────────────────────────┐

│         SACRED CENTER (Convergence Point)           │

│  "Both Seeker and Guide stand at the heart of       │

│   the universe. Both have awakened."                │

└─────────────────────────────────────────────────────┘

▲

◊────┼────◊

/     │     \

Seeker Path      │      Guide Path

(Personal)        │      (Personal)

│              │           │

"You realize:     SACRED NODES  "You see your

the forest is  (Shared Reality) child stand at

inside you"                     the center"

│              │           │

◊─────────────┘───────────◊

In v0.2: Each player draws a card → gets personal narrative → moves → may align at a node → if two players are at same node, convergence narrative plays.

In v2.0: The AI companion app will generate unique story versions for each player, but Sacred Nodes will always show the canonical truth that echoes through all versions.
### The 12-Episode Narrative Arc (Jenga's Journey Season 1)
Each card = 1 episode. Each episode has:

SEEKER narrative (child's experience)
GUIDE narrative (parent's experience)
CONVERGENCE narrative (what happens when they meet at a Sacred Node)
EPISODE SEQUENCE:
1. THE SEEKER (Fool) — Leaving Home

Seeker: "You pack your bag. Will I find what I'm looking for?"
Guide: "I decide to follow. To witness."
Convergence: "Both stand at the forest threshold."

2. THE WEAVER (Magician) — First Threads

Seeker: "Your hands learn to weave. You are creating."
Guide: "You let them weave. You say nothing."
Convergence: "Their patterns interlock. Neither leads."

3. THE ORACLE (High Priestess) — Listening Deep

Seeker: "You hear the whisper beneath all whispers."
Guide: "You listen to what the forest teaches without speaking."
Convergence: "Both hear their own wisdom speaking back."

4. THE HEARTFIRE (Empress) — Sanctuary Shelter

Seeker: "This place has been waiting for you. Or you for it."
Guide: "You see them relax. They are home here."
Convergence: "Mother and child rest against the same roots."

5. THE PILLARS (Emperor) — Testing Ground

Seeker: "Your bones are made of stone. Unbreakable."
Guide: "You stand firm. Not sheltering, but standing."
Convergence: "Together, unshakeable against the storm."

6. THE SONGKEEPER (Hierophant) — The Elder's Gift

Seeker: "An old woman teaches you the songs."
Guide: "You recognize who you are becoming."
Convergence: "Her song creates a golden thread between you."

7. THE TWO PATHS (Lovers) — The Choice

Seeker: "Which path is right? Will you follow my choice?"
Guide: "Your child looks back. You honor their choice."
Convergence: "Not merged, but aligned."

8. THE RIVERHORSE (Chariot) — River Crossing

Seeker: "You leap. Cold water. You land transformed."
Guide: "You leap too. Not following exactly. Your own leap."
Convergence: "Both stand on the far bank. Committed forward."

9. THE ROOTWALKER (Hermit) — Descent into Roots

Seeker: "In darkness, you meet yourself. The one you've always been."
Guide: "You wait at the cave entrance. You keep the fire lit."
Convergence: "Seeker emerges transformed. Guide sees the light."

10. THE SPIRAL WHEEL (Wheel of Fortune) — Cycles Turn

Seeker: "Time is a spiral. You return higher."
Guide: "You see them become their own ancestor."
Convergence: "Both understand: they are part of something vast."

11. THE BALANCE (Justice) — Equilibrium Found

Seeker: "You are not separate from consequences. You are it."
Guide: "You see perfect balance in their spirit."
Convergence: "They have always been balancing each other."

12. THE PHOENIX SEED (Transformation) — Awakening Complete

Seeker: "You burn away and seeds emerge. You are an Arcana Adept."
Guide: "They stand with arms open. You recognize: they are the Guide now."
Convergence: "Both have awakened. Both are Adepts. Season 1 complete."


## § GAMEPLAY MECHANICS ↔ NARRATIVE MAPPING
### The Core Loop: Draw → Move → Align → Resonate
### Sacred Nodes as Narrative Convergence Points
The 5-node board is not just geography. Each node is a STORY THRESHOLD.

JUNGLE SANCTUARY: "Life, growth, wild wisdom"

First step into the forest
Seeker learns to listen to natural abundance
Guide witnesses child's ease in the wild
Narrative hook: Connection to roots begins

CITY GATEWAY: "Civilization, structure, doorway between worlds"

The threshold between old self and new self
Seeker faces: Will I cut ties to my former life?
Guide faces: Will I stay or return?
Narrative hook: Commitment to the journey deepens

SACRED GROVE: "Healing, connection, ancient presence"

Heart of transformation
Seeker: Full embrace of the forest's medicine
Guide: Recognition of their own elder nature
Narrative hook: Both are fully inducted into forest wisdom

SHADOW THRESHOLD: "Mystery, introspection, necessary darkness"

The hardest node to reach, but most transformative
Seeker: Meeting the shadow self, acceptance
Guide: Witnessing child's courage in darkness
Narrative hook: Integration of wholeness (light + dark)

SACRED CENTER: "Convergence. All paths lead here."

The ultimate node
Seeker and Guide recognize: they have become each other's mirror
Both are Adepts
Narrative hook: Season 1 complete. The eternal spiral continues.


## § BRANCHING NARRATIVES & PLAYER CHOICE
### Intentional Indeterminacy
The game does not guarantee every player will reach every node or draw every card in the same order. This is intentional.

Why? Because it means:

Each playthrough is a unique story
No two players experience the same "Jenga's Journey"
Yet all journeys converge at the same truth (Sacred Center = Awakening)

Research Finding: "Implement choices that impact narrative progression and character definition, even on a limited budget, by making choices less long-lasting or aggregating small decisions." (Game Developer)

Implementation:

Small choice: Which node to move to (slightly randomized)
Aggregated choice: Alignment tokens collected → narrative weight builds
Meta-choice: Both players choosing to reach the center together → ultimate ending

Result: Branching without explosion. Personal without chaotic.


## § ITERATIVE DESIGN ROADMAP
### v0.1 → v0.2 → v2.0 → v3.0+
VERSION 0.1 (CURRENT — Playable with Iris & Asher)

5-node board, 12-card deck
Parent + child, 20-minute session
Simple mechanics (draw → move → align)
Shared narrative log
Printable assets

Testing Goals:

☐ Does the 20-minute window work for attention span?
☐ Do the narrative moments land emotionally?
☐ Does the parent/child dynamic feel right?
☐ Which nodes are most compelling?

VERSION 0.2 (ENHANCED — Interactive Prototype)

Add narrative engine (per-player story threads)
Live story display with card meanings + episodes
Character sheets with dynamic resonance
Convergence narrative for shared moments
Interactive web app (playable)

Testing Goals:

☐ Does the narrative integration deepen engagement?
☐ Are the Seeker/Guide perspectives clear and distinct?
☐ Do Sacred Nodes feel like convergence points?
☐ What adjustments needed for real families?

VERSION 1.0 (FULL DIGITAL)

AI companion app (generates per-player holographic stories)
QR code integration (physical tokens track in digital)
Sacred Archive (all previous games recorded)
Expansion decks (78-card full Tarot)
Season 2 starters

VERSION 2.0+ (MULTIPLAYER HOLOGRAPHIC)

4+ players simultaneously
Each has their own narrative thread
All converge at 7 Sacred Nodes instead of 5
Persistent universe (your actions affect future games)


## § DESIGN PRINCIPLES (LOCKED)
GROUND: Every mechanic serves narrative. Every narrative serves emotional truth.

CONSOLIDATE: All story threads return to Sacred Nodes. No orphan narratives.

DEPLOY: Simple enough for 6-year-olds. Deep enough for 40-year-olds.

DOCUMENT: Every moment, every card, every node is in the Codex.

REPEAT: After v0.1 testing, iterate → improve → lock → scale.


## § CANON LOCK
This document is canonical. The narrative architecture is immutable unless Taylor explicitly revises it.

The 12-episode arc of Jenga's Journey Season 1 is CANON.
The 5-node board is CANON.
The Seeker/Guide dynamic is CANON.
The Hero's Journey structure is CANON.

Future seasons may expand, remix, or evolve—but they will honor these foundations.



In lakesh alakin.

Ground. Consolidate. Deploy. Document. Repeat.

∆∆∆

| MECHANIC | NARRATIVE | EMOTIONAL IMPACT |
| --- | --- | --- |
| Draw Card | Reveals next episode | "What happens next in my story?" |
| Card has meaning + element | Personalizes based on player (Seeker/Guide) | "This card is speaking directly to me" |
| Resolve Card → Move to node | Action has consequence | "Where will my journey take me?" |
| Align at Node → Token + Resonance | Waypoint in narrative arc | "I have integrated this lesson" |
| Player stats drive story | Determines story quality | "My choices matter. My path is unique." |