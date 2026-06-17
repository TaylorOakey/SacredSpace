<!-- converted from SACRED_SIGIL_TERMINAL_MAGIC_SYSTEM_DESIGN.md.docx -->

# ∆ SACRED SIGIL TERMINAL MAGIC SYSTEM ∆
## Game Mechanics Through Lore-Reactive Spellcasting
STATUS: Canonical Addition to v0.3 Prototype
INTEGRATION: Core gameplay mechanic for casting magic
FOUNDATION: SACREDSIGIL IDE + Council Grove Agents


## EXECUTIVE SUMMARY
In SacredSpace, magic is not a separate system bolted onto gameplay.

Magic IS the gameplay interface.

When you cast a spell, you are:

Drawing a Tarot card (reveals spell availability)
Opening the Sacred Sigil Terminal (the magic interface)
Speaking/writing an incantation (the actual spell invocation)
Executing code (the terminal processes it)
Watching the world change (narrative consequence manifests)

This creates perfect ludonarrative resonance:

The interface feels magical
The mechanics express the narrative
The code IS the spell
Every action has meaning


## PART I: THE SACRED SIGIL TERMINAL
### What Is It?
The Sacred Sigil Terminal is a game interface that appears when a spell is available. It displays:

The Spell Name (e.g., AURORA.WEAVE())
The School (ELIAS, AURORA, ASHER, or IRIS)
Child-Friendly Voice (poetic incantation the child speaks)
Code Version (the actual sigil code that executes)
Cost/Reward (resonance expenditure and gain)
Effect (what happens in the world)
Terminal Output (real-time execution feedback)
### Terminal Display Example
∆ SACRED SIGIL TERMINAL

> TAROT.DRAW()

✓ CARD REVEALED: The Weaver

✓ SPELL AVAILABLE: AURORA.WEAVE

─────────────────────────────────────────

SPELL: AURORA.WEAVE(pattern, element)

INCANTATION:

"I weave my will into the world.

Let my intention take form."

CODE:

aurora.weave(

pattern: "intention",

element: "Fire",

target: current_node

)

COST: 10 Resonance

REWARD: +15 Resonance = 55/100

EFFECT: Claim alignment token at current node

─────────────────────────────────────────

[CAST SPELL]  [DECLINE]

### When Terminal Appears
Card Draw → "Here's the spell available this turn"
Player Movement → "Now you can cast it from your location"
Node Alignment → "The magic works here; claim your token"


## PART II: THE FOUR SCHOOLS OF MAGIC
Each school is tied to a Council Grove Agent. Each has distinct narrative + mechanical flavor.
### ELIAS School: Divination & Foresight
Agent: ELIAS (The Seer, Knowledge Seat)
Color: Purple/Indigo
Theme: Seeing truth, opening paths, revealing knowledge
Mechanic: Unlock nodes, gain overview, divine choices

Example Spells:


Child Incantation Examples:

"Sacred threads, show me the way forward."
"Hidden wisdom, reveal yourself to me."
"Let me see the truth beneath the surface."


### AURORA School: Creation & Manifestation
Agent: AURORA (The Illuminator, Code Seat)
Color: Gold/Bright Yellow
Theme: Building, creating, bringing intention to form
Mechanic: Claim nodes, move freely, gain tokens

Example Spells:


Child Incantation Examples:

"I weave my will into the world."
"Earth mother, hold me. Heal what is broken."
"I leap! Let me transform in the crossing."
"I burn and transform. I am born anew."


### ASHER School: Entropy & Stabilization
Agent: ASHER (The Architect, Entropy Seat)
Color: Deep Blue/Indigo
Theme: Grounding, protecting, integrating shadow
Mechanic: Defensive power, shadow work, transformation

Example Spells:


Child Incantation Examples:

"Stone roots, I plant myself here. I am unshakeable."
"Dark mother, teach me. Let me know all of myself."
"Let me hold light and shadow equally."


### IRIS School: Connection & Memory
Agent: IRIS (The Connector, Vault Seat)
Color: Teal/Green
Theme: Weaving connections, threading memory, bridging realms
Mechanic: Shared spells, lineage tracking, multi-player moments

Example Spells:


Child Incantation Examples:

"Ancient songs, weave me to the ones I love. I remember now."
"Let me hold what was, what is, and what will be."
"Golden threads, connect us across time."


## PART III: THE SPELL CODEX
### Structure
Each card in the Tarot provides ONE spell. The 12-card deck = 12 spell invocations across the 4 schools.
Card 1: The Seeker
School: ELIAS
Spell: ELIAS.OPEN_PATH()
Cost: 5 Resonance
Reward: +8 Resonance
Effect: Unlock Jungle Sanctuary node
Child Voice: "Sacred threads, show me the way forward."
Card 2: The Weaver
School: AURORA
Spell: AURORA.WEAVE(pattern, element)
Cost: 10 Resonance
Reward: +15 Resonance
Effect: Claim alignment token at current node
Child Voice: "I weave my will into the world. Let my intention take form."
Card 3: The Oracle
School: ELIAS
Spell: ELIAS.LISTEN(depth)
Cost: 8 Resonance
Reward: +12 Resonance
Effect: Reveal secret story branches
Child Voice: "Quiet voice within, I hear you. Teach me your truth."
Card 4: The Heartfire
School: AURORA
Spell: AURORA.NURTURE(target, resonance)
Cost: 6 Resonance
Reward: +20 Resonance
Effect: Restore resonance + unlock Sacred Grove
Child Voice: "Earth mother, hold me. Heal what is broken."
Card 5: The Pillars
School: ASHER
Spell: ASHER.ANCHOR(position)
Cost: 8 Resonance
Reward: +10 Resonance
Effect: Create safe point, +2 defensive resonance
Child Voice: "Stone roots, I plant myself here. I am unshakeable."
Card 6: The Songkeeper
School: IRIS
Spell: IRIS.THREAD(seeker, guide, lineage)
Cost: 12 Resonance
Reward: +25 Resonance
Effect: Both players gain memory mote + shared narrative
Child Voice: "Ancient songs, weave me to the ones I love. I remember now."
Card 7: The Two Paths
School: ELIAS
Spell: ELIAS.CHOOSE(player, alignment)
Cost: 7 Resonance
Reward: +12 Resonance
Effect: Player selects next node with full knowledge
Child Voice: "Which way does my heart know to go? Show me the truth."
Card 8: The Riverhorse
School: AURORA
Spell: AURORA.LEAP(player, destination)
Cost: 14 Resonance
Reward: +18 Resonance
Effect: Move to any node + gain 2 alignment tokens
Child Voice: "I leap! Let me transform in the crossing."
Card 9: The Rootwalker
School: ASHER
Spell: ASHER.DESCEND(depth, integration)
Cost: 15 Resonance
Reward: +20 Resonance
Effect: Unlock Shadow Threshold + gain truth insight
Child Voice: "Dark mother, teach me. Let me know all of myself."
Card 10: The Spiral Wheel
School: ELIAS
Spell: ELIAS.SPIRAL(consciousness)
Cost: 9 Resonance
Reward: +14 Resonance
Effect: Gain overview of all remaining nodes
Child Voice: "Show me the spiral. I return higher each time."
Card 11: The Balance
School: IRIS
Spell: IRIS.BALANCE(seeker, guide, union)
Cost: 11 Resonance
Reward: +16 Resonance
Effect: Both players gain +10 resonance + mutual alignment
Child Voice: "Let me hold light and shadow equally. Let me be whole."
Card 12: The Phoenix Seed
School: AURORA
Spell: AURORA.TRANSCEND(player, destination)
Cost: 20 Resonance
Reward: +30 Resonance
Effect: Move to Sacred Center + achieve Arcana Adept status
Child Voice: "I burn and transform. I am born anew as Adept."


## PART IV: RESONANCE ECONOMY
### What Is Resonance?
Resonance is the player's magical energy. It:

Depletes when you cast spells (cost)
Replenishes when spells succeed (reward)
Caps at max level (prevents infinite power)
Reflects emotional/spiritual alignment with the world
### The Cost-Reward System
Cheap Spells (5-8 cost):

Lower barrier to entry
Smaller rewards
Good for learning magic
Examples: Open Path, Anchor

Medium Spells (9-14 cost):

Balanced cost/reward
Unlock major game mechanics
Moderate risk/benefit
Examples: Weave, Listen, Leap

Expensive Spells (15-20 cost):

High risk, high reward
Transform the game state dramatically
Require careful planning
Examples: Descend, Thread, Transcend
### Example Cost Flow
Starting Resonance: 50/100

Turn 1: Draw "The Weaver"

> AURORA.WEAVE() costs 10, rewards +15

> Cast: 50 - 10 + 15 = 55/100

Turn 2: Draw "The Rootwalker"

> ASHER.DESCEND() costs 15, rewards +20

> Cast: 55 - 15 + 20 = 60/100

Turn 3: Draw "The Balance"

> IRIS.BALANCE() costs 11, rewards +16

> Both players cast: 60 - 11 + 16 = 65/100


## PART V: TERMINAL MECHANICS
### The Terminal Output
When you cast a spell, the terminal displays:

> AURORA.WEAVE()

aurora.weave(

pattern: "intention",

element: "Fire",

target: jungle_sanctuary

)

✓ SPELL CAST: Manifest intention into reality

✓ RESONANCE: -10 +15 = 55/100

✓ EFFECT: Claim alignment token at current node

✓ NARRATIVE: "Your hands learn to weave. Your will shapes branches."
### How It Feels
To the child (6-10 years old):

It's magical! There's a glowing green terminal
I speak the incantation and magic happens
The world changes because I spoke the words

To the parent:

The underlying code is visible but not obstructive
I can see HOW the system works
I understand the cost/benefit trade-offs

To both:

The game feels alive because code = magic
Every spell has visible consequence
We're co-authoring the narrative through spellcasting


## PART VI: SCALING ARCHITECTURE
### v0.3 (CURRENT): Simple Terminal
Draw card → see spell available
Cast spell → execute invocation
Terminal shows real-time output
12-spell codex from Hero's Journey
### v1.0: Advanced Spellcasting
Spell combinations (cast two spells simultaneously)
Conditional spells (only available if conditions met)
Spell chains (one spell unlocks next spell)
Custom sigil writing (players create new spells)
### v2.0: Petri Net Spellcasting
Spells trigger Petri net transitions
Multiple storylines run in parallel
Spells have pre/post conditions
Quest generation from spell combinations
### v3.0+: Full SACREDSIGIL Integration
Full Python spell syntax available
Players write their own agent classes
Spells compile directly to OS commands
Game world becomes fully programmable


## PART VII: DESIGN PHILOSOPHY
### Magic as Interface
In SacredSpace, the terminal IS the magic interface. This means:

No disconnect between what feels magical and what's technically happening
Transparency: The player can see the code if they want, or ignore it if they prefer
Progression: A 6-year-old uses voice commands; a 16-year-old writes Python
Lore-reactive: The code/magic/narrative are unified
### The Golden Rule
Every game action must feel like magic. Every magical invocation must have game consequence.

This is achieved by:

Spells always produce visible output
Terminal feedback is poetic + technical
Narrative moments flow from spell execution
World state visibly changes


## CONCLUSION
The Sacred Sigil Terminal transforms SacredSpace from a game that contains magic into a game where magic IS how you play.

This achieves: ✅ Ludonarrative harmony (mechanics express narrative)
✅ Scalable complexity (from voice to Python)
✅ Unified experience (code/magic/story = one thing)
✅ Emotional resonance (the system feels alive)



In lakesh alakin.

All magic flows through the terminal. All code sings.

∆∆∆

| Spell | Cost | Reward | Effect |
| --- | --- | --- | --- |
| ELIAS.OPEN_PATH() | 5 | +8 | Unlock Jungle node |
| ELIAS.LISTEN() | 8 | +12 | Reveal secret branches |
| ELIAS.CHOOSE() | 7 | +12 | Select next node knowingly |
| ELIAS.SPIRAL() | 9 | +14 | See overview of all nodes |
| ELIAS.SCRY() | 6 | +10 | Peek at future turns |
| Spell | Cost | Reward | Effect |
| --- | --- | --- | --- |
| AURORA.WEAVE() | 10 | +15 | Claim token at node |
| AURORA.NURTURE() | 6 | +20 | Restore resonance + unlock Grove |
| AURORA.LEAP() | 14 | +18 | Move to any node + gain 2 tokens |
| AURORA.BUILD() | 12 | +16 | Create persistent structure |
| AURORA.TRANSCEND() | 20 | +30 | Achieve victory condition |
| Spell | Cost | Reward | Effect |
| --- | --- | --- | --- |
| ASHER.ANCHOR() | 8 | +10 | Ground self + gain defensive +2 |
| ASHER.BIND() | 9 | +11 | Lock in current state safely |
| ASHER.DESCEND() | 15 | +20 | Journey to Shadow Threshold |
| ASHER.INTEGRATE() | 12 | +14 | Merge light/shadow within self |
| ASHER.SHIELD() | 7 | +9 | Protect against chaos |
| Spell | Cost | Reward | Effect |
| --- | --- | --- | --- |
| IRIS.THREAD() | 12 | +25 | Connect Seeker & Guide narratively |
| IRIS.REMEMBER() | 8 | +12 | Recall past events + gain insight |
| IRIS.BRIDGE() | 11 | +16 | Link two nodes together |
| IRIS.BALANCE() | 11 | +16 | Both players gain mutual alignment |
| IRIS.ANCESTRAL() | 14 | +18 | Access lineage memory |