<!-- converted from SACRED_OPERATING_MANUAL.md.docx -->

# ∆∆∆ SACRED OPERATING MANUAL ∆∆∆
The One Source. The Daily Practice. The Living Grimoire.

"You are not managing a system. You are tending a living thing."

Location: D:\SacredSpace_OS\04_SACRED_CODEX\SACRED_OPERATING_MANUAL.md Vault mirror: 01_OBSIDIAN_VAULTS\SacredSpace_Vault\CODEX\SACRED_OPERATING_MANUAL.md Status: Canon · Living Document · Revise freely, core rhythm is immutable Maintained by: Taylor · Co-creator: Jeanie Leaf Mantra: In lakesh alakin ∆∆∆


## I. THE PHILOSOPHY (READ THIS ONCE, CARRY IT ALWAYS)
You are an artist who builds systems. Not a builder who sometimes makes art.

Every script, every route, every agent — these are brushstrokes. The nine pillars are not a filing system. They are a canvas. SacredSpace OS is not a productivity tool. It is a living creative practice.

When focus drifts, return to this: the work has a pulse. Your job each day is to find it and follow it.

The daily practice below is a rhythm, not a rulebook. Move through it the way you move through music — with feel, with timing, with intention. Some days you linger in the morning. Some days the evening is the whole session. Trust the pulse.


## II. THE SYSTEM MAP (EVERYTHING IN ONE VIEW)
SACREDSPACE OS — FULL SYSTEM OVERVIEW

──────────────────────────────────────────────────────────────

DAILY ENTRY POINTS

└── Obsidian DAILY_TRIAGE.md     → morning alignment + inbox sweep

└── Sacred Chrome Extension      → nine-pillar status at a glance

└── handoff_ritual.py            → load yesterday's context capsule

KNOWLEDGE & CANON

└── 01_OBSIDIAN_VAULTS           → permanent notes, vault, research

└── 04_SACRED_CODEX              → spells, rituals, THIS file

└── NotebookLM (6 notebooks)     → SACRED.CORE · LORE.VAULT · GAME.SYSTEMS

KNOWLEDGE.VAULT · FAMILY.LEGACY · CREATION.LAB

INTELLIGENCE LAYER

└── FastAPI Spine (port 8888)    → backbone — always running

└── Ollama (port 11434)          → local LLMs, zero-cost

└── ChromaDB (port 8000)         → semantic memory

└── 05_MEMORY_ENGINE             → SQLite + Redis + ChromaDB stack

AGENT LAYER

└── ELIAS                        → knowledge agent

└── AURORA                       → code agent

└── ASHER                        → entropy/chaos agent

└── IRIS                         → vault agent

└── HERMES                       → executor, messenger, scheduler (new)

└── CLAUDE CODE (planned)        → deep codebase agent

COUNCIL GROVE (deliberation)

└── Claude                       → Reasoning + Narrative

└── Gemini                       → Deep Research

└── ChatGPT                      → Systems Architecture

LEARNING PATH

└── 08_LEARNING_PATH             → Maestro AAS in AI Engineering

└── SACREDCODEX Spells           → PY-STR-001 through PY-MOD-008 + advanced set

CREATION

└── Jenga's Journey              → graphic novel (07_SOCIAL_MOTHERSHIP)

└── Sacred Messages System       → Year 1 complete; monthly letters for Iris + Asher

└── SacredArcana Studios         → POD brand, @SacredSpaceStudios, eight design families

└── Sacred Sounds                → sonic intelligence system (in development)

COLLABORATION

└── CollabOS v3                  → Taylor + Jeanie governance interface

└── Tailscale mesh               → sacredspace-wsl.sacredspace.ts.net

└── Sacred Space 501(c)(3)       → nonprofit in development, Eastern NC

MARKET

└── 09_SACRED_MARKET             → Etsy · Printify · Gelato (POD revenue)


## III. THE DAILY RITE (THE PRACTICE)
The day has three movements: OPEN · FLOW · CLOSE. Each movement has a feel. Read the feel before you read the steps.


### 🌅 OPEN — Morning Alignment (15–20 min)
The world is quiet. You are the first thing that speaks into the day.

Feel: Unhurried. Sacred. No rushing past this.

Sequence:

1. BREATHE FIRST

Three breaths. Name one thing you're building.

Name one thing you're making. They are not the same.

2. LOAD CONTEXT

In WSL2 terminal:

$ cd /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE

$ python handoff_ritual.py

→ Read the capsule. Know where you are.

3. OPEN OBSIDIAN → RUN DAILY_TRIAGE

Template: DAILY_TRIAGE.md (Templater)

→ Inbox sweep (IRIS layer)

→ Set energy state: Ignition / Steady / Low

→ Write ONE sentence of intent for the day

4. GLANCE AT THE CHROME EXTENSION

→ Nine pillars status check

→ Note which pillar is calling loudest today

5. CHECK HERMES (once live)

→ Any scheduled reports delivered overnight?

→ Any Telegram alerts?

6. SET THE DAY'S CREATIVE THREAD

───────────────────────────────────────────

This is the most important step and the one

most often skipped. Name the creative thread

running through today — even if today is 90%

school or code.

Examples:

"Today I'm moving like water." (fluid, adaptive)

"Today is excavation." (digging deep, finding roots)

"Today I'm the messenger." (shipping, delivering)

"Today is the forge." (building, hardening)

Write it in the DAILY_TRIAGE intent field.

Let it color everything that follows.

───────────────────────────────────────────


### ☀️ FLOW — The Two Blocks
The body of the day. Two blocks, different in nature, both fed by the creative thread.

Feel: Engaged. In the work. The thread is running.


BLOCK ONE — School or Build (2–3 hrs)
Rotate daily. If Monday was school-heavy, Tuesday tilts build.

SCHOOL MODE (08_LEARNING_PATH)

→ Open Maestro coursework

→ After each concept: write a SACREDCODEX spell entry

Format: PY-XXX-NNN · one concept · one code block · one real-world use

→ Hard concepts → paste into NotebookLM KNOWLEDGE.VAULT

→ Confusion = signal: open Council Grove (Claude first, then Gemini for research)

→ End block: commit new spell to 04_SACRED_CODEX/SPELLS/

BUILD MODE (SacredSpace OS infrastructure)

→ Load handoff capsule from OPEN step (already done)

→ Check FastAPI spine: curl http://localhost:8888/health

→ Pick ONE component to advance (not three — one)

→ AURORA handles code · ELIAS handles doc · IRIS handles filing

→ When blocked: run handoff_ritual.py → take to Council Grove

→ End block: git commit -m "∆ [pillar] [what changed]"


CREATIVE PULSE — Midday (10–15 min)
This is not a break. This is the oxygen. The artist in you needs to speak at least once per day.

Feel: Permission. Release. No output required.

Rotate through this list — pick what resonates, never force:

JENGA'S JOURNEY

→ One panel described in words. Just describe it. Don't draw.

→ Or: one line of dialogue. One character moment.

→ Drop in: 07_SOCIAL_MOTHERSHIP/JENGA/DAILIES/

SACRED MESSAGES (Iris · Asher)

→ One memory, observation, or message fragment

→ Doesn't have to be a full letter — seed for next month

→ Drop in: FAMILY.LEGACY notebook or Obsidian

SACREDARCANA STUDIOS

→ One design concept, color note, or sigil sketch (even in text)

→ Tag with elemental realm: Zii · Mylo · Auralon · Koru

→ Drop in: 07_SOCIAL_MOTHERSHIP/ARCANA/CONCEPTS/

SACRED SOUNDS

→ One sonic idea, loop concept, or rhythm feeling in words

→ Can be as simple as: "bass that feels like roots in soil"

JEANIE / SACRED SPACE

→ A thought for the collective. Something to bring to CollabOS.

FREE FORM

→ Write one paragraph, make one mark, hum one melody.

→ Sacred doesn't mean serious. Play is holy here.


BLOCK TWO — The Complement (1.5–2 hrs)
The opposite of Block One. School follows build. Build follows school. Or: if energy is low, this block goes creative-heavy.

If energy is LOW:

→ Shift to creation: Jenga writing, Sacred Messages, SacredArcana design work

→ Creation IS the work. Not a consolation prize.

→ Log it in DPR as CREATION pillar XP

If energy is HIGH:

→ Push deeper into whatever Block One opened

→ OR: run a Council Grove session on whatever is stuck

→ OR: deploy something to the Sacred Market


### 🌙 CLOSE — Evening Seal (15–20 min)
The day needs a closing sigil. This is it.

Feel: Complete. Honest. Not rushed. The day is sealed, not abandoned.

Sequence:

1. SACRED NEXUS — DAILY PERFORMANCE REPORT

Open Sacred Nexus artifact in Claude

→ Fill DPR form: what moved, what didn't, honest numbers

→ Generate report → collect XP + lore entry + Canon Gate items

→ Screenshot or copy Canon Gate items → paste to DAILY_TRIAGE note

2. OBSIDIAN CLOSE

→ Process any HOLDING items from morning triage

→ Move promoted notes to their pillar folder

→ Update DAILY_TRIAGE.md status: active → closed

3. HANDOFF RITUAL

$ python /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/handoff_ritual.py

→ This capsule is tomorrow morning's OPEN step

→ Gemini / Claude / fresh session will know where you are

4. GIT COMMIT

$ cd /mnt/d/SacredSpace_OS

$ git add -A

$ git commit -m "∆ CLOSE — $(date +%Y-%m-%d)"

$ git push

5. CLOSING MANTRA

Speak or write: "In lakesh alakin." ∆∆∆

The session is sealed.


## IV. THE WEEKLY RHYTHM
The week is a seven-note scale. Each day has its tone.



## V. THE QUICK LAUNCH COMMANDS
Copy these into a ~/aliases.sh or your ~/.bashrc.

# Morning boot sequence

alias sacred-open='python /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/handoff_ritual.py'

# Check spine health

alias sacred-health='curl -s http://localhost:8888/health | python3 -m json.tool'

# Start Ollama if down

alias sacred-llm='ollama serve &'

# Git close ritual

alias sacred-close='cd /mnt/d/SacredSpace_OS && git add -A && git commit -m "∆ CLOSE — $(date +%Y-%m-%d)" && git push'

# Start Hermes (once installed)

alias sacred-hermes='hermes serve &'

# Full morning stack (all at once)

alias sacred-rise='ollama serve & sleep 2 && curl -s http://localhost:8888/health && python /mnt/d/SacredSpace_OS/02_COUNCIL_GROVE/handoff_ritual.py'


## VI. THE COUNCIL GROVE PROTOCOL
When to call which mind.

CLAUDE (you are here)

→ Narrative, reasoning, architecture decisions, writing, ritual design

→ Use for: anything that needs depth, nuance, or sacred framing

GEMINI

→ Deep research, large document synthesis, factual verification

→ Use for: "research X and give me a comprehensive report"

CHATGPT

→ Systems architecture, code structure, engineering patterns

→ Use for: "how should this system be designed at scale"

HERMES (local executor)

→ Autonomous tasks, scheduled work, file ops, cross-session research

→ Use for: "do this overnight and report back"

CLAUDE CODE (coming)

→ Deep codebase work, multi-file refactors, autonomous coding sessions

→ Use for: "rebuild this module" or long autonomous dev tasks

OLLAMA (local inference)

→ Zero-cost completions, quick queries, offline work

→ Models: nous-hermes2 or equivalent


## VII. THE CANON GATE
Before anything becomes canon, it passes through these questions.

1. Does it fit the nine pillars without breaking them?

2. Is it open-source and zero-cost?

3. Can it run locally without internet?

4. Does it serve Taylor's mission, Jeanie's mission, or both?

5. Would it make Iris and Asher proud in five years?

If yes to all five → bring to Council → canonize.

If no on any → hold in DISTILLED until it earns its place.


## VIII. WHEN YOU FEEL SPREAD THIN (READ THIS)
You will feel this again. It is part of the practice.

When the system feels too big, return to the smallest true thing:

One pillar. One block. One creative thread. One day.

You do not have to tend all nine pillars today. You do not have to finish the system. The system is never finished. That is not the point.

The point is that every day you made something. Every day you learned something. Every day you moved the signal forward.

SacredSpace OS grows the way a forest grows — not by force, but by accumulation. Every commit is a root. Every spell is a branch. Every letter to Iris and Asher is a seed.

You are not behind. You are becoming.


## IX. SYSTEM STATUS QUICK REFERENCE


## X. THE REVISION PROTOCOL
This document is living. Revise it when the practice drifts.

MINOR UPDATE  → Edit directly. Note the date in the changelog below.

MAJOR REVISION → Bring to Council Grove first. Claude synthesizes.

New version gets a version number.

CANON LOCK    → Only Taylor can lock. Use the Canon Gate (Section VII).

Changelog:

2026-05-14  v1.0  — Initial canon. Built with Claude. ∆∆∆



∆∆∆ This is the map and the territory both. The practice is the system. The system is the practice. In lakesh alakin.



Next steps after reading this:

Drop this file into 04_SACRED_CODEX/ and 01_OBSIDIAN_VAULTS/SacredSpace_Vault/CODEX/
Add the aliases from Section V to your ~/.bashrc
Run sacred-rise tomorrow morning as your first act
Fix Ollama (see troubleshooting above) so sacred-rise completes fully
Come back to Section VIII whenever you need it

| Day | Tone | Primary Lean |
| --- | --- | --- |
| Monday | Root | Council Grove synthesis — what did last week build? |
| Tuesday | Structure | Maestro school focus — deep learning block |
| Wednesday | Market | SacredArcana Studios — content, designs, Etsy |
| Thursday | Forge | Build sprint — hardest SacredSpace OS task of the week |
| Friday | Lineage | Family Legacy — Sacred Messages, Iris/Asher, Jeanie/CollabOS |
| Saturday | Creation | Jenga's Journey, Sacred Sounds, free art — no code |
| Sunday | Review | Hermes skill audit, Obsidian vault sweep, weekly DPR |
| System | Check Command | Port/Path |
| --- | --- | --- |
| FastAPI Spine | curl localhost:8888/health | 8888 |
| Ollama | curl localhost:11434/api/tags | 11434 |
| ChromaDB | curl localhost:8000/api/v1/heartbeat | 8000 |
| Hermes | hermes status | — |
| Tailscale | tailscale status | mesh |
| Obsidian Vault | Open app | /mnt/d/01_VAULT/SacredSpace_Vault/ |
| Sacred Chrome | Click extension icon | browser |
| CollabOS | Open HTML file | 02_COUNCIL_GROVE/CollabOS_v3.html |