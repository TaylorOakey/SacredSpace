<!-- converted from Build-SacredVault.ps1.docx -->

# ============================================================
# Build-SacredVault.ps1
# S∆CR3D Vault: One-Click Obsidian Structure Builder
# Version: SS_OS_v3.1_NeuralForest_Integrated
# Amended: 2026-03-06 — sacred_universe_v3_1.json ingested
# ============================================================
# Activation phrase: S@CREDSOURC3, unfurl the scroll.
# ============================================================

$VaultRoot = "$env:USERPROFILE\Documents\SacredSpace"

# ============================================================
# README CONTENT DEFINITIONS
# ============================================================

$readmes = @{}

$readmes["00_Command_Center\README.md"] = @"
---
folder: 00_Command_Center
purpose: The bridge of the ship
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
activation_phrase: "S@CREDSOURC3, unfurl the scroll."
---

# 00 — Command Center

> The nerve center of SacredSpace. Everything starts and returns here.
> *"Sacred Space is a safe, playable structure that turns chaos into meaningful growth."*

## Core Axiom
Life becomes a game when chaos is connected into a stable container of meaning.

| Element | Definition |
|---|---|
| Chaos | Infinite possible moves |
| Container | Rules and rituals |
| Game | Meaningful action within structure |

## Active Sprint
**Infrastructure Consolidation — March 2026**

### Immediate Priorities
- Stable Sync and Network Recovery
- Doctrine Locking
- Neural Forest Initialization: sacred_codex.json

## Open Threads

| ID | Title | Priority |
|---|---|---|
| OT_001 | Initialize the Sacred Codex Forest | HIGH |
| OT_002 | Player Registry in Forest | HIGH |
| OT_003 | Auto-Reflect the Family Layer | MEDIUM |
| OT_004 | Sacred Storyline Visualization | MEDIUM |
| OT_005 | Skill Distribution to Other Players | LOW |

### OT_001 First Command
python neural_forest.py init sacred_codex.json

## SPI Dashboard (Sacred Progress Index)
| Range | State |
|---|---|
| 0-30 | Dormant |
| 31-60 | Growing |
| 61-80 | Flowing |
| 81-100 | Thriving |

## Navigation
- SACREDSPACE_MASTER_OPERATING_INDEX
- 01_Progress_Reports/README
- 02_Doctrine/README
- 03_AI_Agents/README
- 04_Infrastructure/README
- 05_Learning_Spine/README
- 06_Creative_Universe/README
"@

$readmes["01_Progress_Reports\README.md"] = @"
---
folder: 01_Progress_Reports
purpose: The longitudinal memory of the system
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 01 — Progress Reports

> The living record. Every cycle leaves a trace here.
> *Rule 7: Reflection Locks Progress — experience becomes wisdom through noticing patterns.*

## Naming Convention
YYYY-MM-DD_Sacred_Progress_Report.md

## Ritual
Update every 24-48 hours without exception.

## Report Template Fields
- Summary of Actions
- Artifacts Produced
- System Status
- Blockers
- Next Priorities

## Echo Template (Rule 7)
What_Happened:
What_I_Learned:
SacredSpace_Echo:
Next_Action:

## Ritual Mapping
| Life Ritual | SacredSpace Function |
|---|---|
| Morning Check-In | Enter_Game |
| Bedtime Reflection | Save_Progress |
| Weekly Talk | Level_Up_Review |
"@

$readmes["02_Doctrine\README.md"] = @"
---
folder: 02_Doctrine
purpose: The Laws of the Land for humans and AI
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 02 — Doctrine

> What we believe. How we operate. Non-negotiable.
> *"Interaction writes canon."*

## The 8 Game Rules

| # | Rule | Principle |
|---|---|---|
| 1 | The World Is the Game Board | Everything that happens is part of play |
| 2 | Create the Container | Chaos becomes playable when bounded |
| 3 | You Are the Avatar | The player and character are the same |
| 4 | Rules Enable Play | Gentle rules create safety |
| 5 | Difficulty Means Growth Is Near | Resistance marks learning edges |
| 6 | Tools Amplify, Not Replace | Tools support agency |
| 7 | Reflection Locks Progress | Meaning is created through noticing patterns |
| 8 | The Game Evolves | SacredSpace is a living system |

## Canonical Rules
- Clarity over verbosity
- Artifact-heavy output
- Anti-entropy: every prompt must yield a S∆CR3D artifact
- Nothing is rejected; everything is placed

## Skills Framework Doctrine
> Skills are blueprints, tools are hands. Without Skills, your AI has tools but doesn't know what to build.

| Layer | Metaphor | Function |
|---|---|---|
| MCP Tools | The hands | What Claude can DO |
| Skills | The blueprints | What Claude KNOWS |

### Three Skill Archetypes
| Type | Focus | Trigger |
|---|---|---|
| A Creator | Making things | Generate... |
| B Manager | Ordered steps | Process... |
| C Expert | Precision tool use | Query/Search... |

## Sacred Commands
| Command | Function |
|---|---|
| /council | Activate Council Grove |
| RECURSE | Deep re-analysis loop |
| Begin Act I | Narrative initiation |
| Activate Mode | Switch agent mode |
| S@CREDSOURC3, unfurl the scroll. | Deep context / mentor mode |

## Sub-Folders
- 01_Rituals: Opening, Closing, Weekly Reset
- 02_Characters: The Gardener, The Fox, The Lightbearer
- 03_Rules: Core_Values, Family_Agreements, Canon
- 04_Challenges: Boss_Battles, Action_Debt
- 05_Tools: Sacred_Wand, Maestro_Setup, Learning_Prompts
- 06_Echoes: Reflection captures
"@

$readmes["02_Doctrine\Canon.md"] = @"
---
type: canon
locked: true
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# Canon — Locked Truths

> These statements are canonical. They do not change without a formal Council decision.

## Canonical Statement v3.1
Players self-initiate into the S∆CR3D ∆RC∆N∆ by acting within the SacredSpace structure. Their gifts, quests, and reflections dynamically write themselves into the S∆CR3D COD3BASE through lived interaction with the S∆CR3D STORYL!NE. The Neural Forest is the living engine that makes the codex executable, reflective, and sovereign.

## Crystallized Insights
1. Skills are blueprints, tools are hands. Without Skills, your AI has tools but doesn't know what to build.
2. The forest is no longer just mystical — it is executable, reflective, and Claude-native.
3. Interaction writes canon. Every action, reflection, and link IS the codex.
4. Sacred Space is a safe, playable structure that turns chaos into meaningful growth.
"@

$readmes["03_AI_Agents\README.md"] = @"
---
folder: 03_AI_Agents
purpose: Specialized workspace for agent coordination
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 03 — AI Agents

> The crew. Each tool has a role. No overlap, no gaps.

## Agent Roster
| Agent | Role | Strength |
|---|---|---|
| Claude | Reasoning Specialist | Deep architecture, debugging, long-context synthesis |
| Gemini | Multimodal Hub and Speed Layer | Real-time research, Google Workspace automation |
| NotebookLM | Source-of-Truth Ingestor | Closed-loop research synthesis |
| ChatGPT | General Execution | Broad task coverage |

## Mentor Persona
S@CREDSOURC3 — the learning intelligence of SacredSpace.
Tone: Mentor + Mirror + Builder. Clear, kind, precise. One playful line per reflection. No fluff.

## Neural Forest v3 Command Reference
python neural_forest.py init sacred_codex.json
python neural_forest.py seed forest.json --title "TYPE . Name" --type project --tags tag1,tag2 --energy growing
python neural_forest.py link forest.json --a ID_A --b ID_B --kind mycelium --weight 1.5
ANTHROPIC_API_KEY=xxx python neural_forest.py auto-reflect forest.json --node ID
python neural_forest.py visualize forest.json --format html --out holo.html
python neural_forest.py progress forest.json
python neural_forest.py ls forest.json --type project
python neural_forest.py search forest.json --query "ritual"
python neural_forest.py export-summary forest.json --out summary.md

## Node Types
| Type | Emoji | Prefix | Use |
|---|---|---|---|
| project | plant | P- | Active work with deliverables |
| mote | crystal ball | M- | Loose ideas and captures |
| ritual | candle | R- | Recurring processes |
| canon | scales | C- | Locked truths |
| lore | book | L- | Deep reference knowledge |
| anchor | anchor | A- | Stable orienting nodes |
| family | seedling | F- | Relationships and people |
| question | ? | Q- | Open inquiries to hold |
| decision | arrows | D- | Made or pending decisions |
| habit | cycle | H- | Recurring practices |
| codex | scroll | X- | Structured reference docs |
| insight | lightbulb | I- | Crystallized realizations |

## COD3BASE State Flow
Initiation > Quest_Assignment > Challenge_Encounter > Reflection > Integration > Level_Advance

## Edge Types
enables, blocks, ritual_bind, family_tether, mycelium
"@

$readmes["03_AI_Agents\Player_Registry.md"] = @"
---
type: player_registry
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# S∆CR3D Player Registry

> Players self-initiate by acting within the SacredSpace structure.

## Active Players

### THE_GARDENER_001
- Name: The Gardener
- Archetype: Guide
- Level: 3
- Initiated: 2026-03-02
- Gifts: Systems architecture, Sacred framing, AI sovereignty awareness, Living codex building, Skill packaging

#### Active Quests
| ID | Title | Status | Energy |
|---|---|---|---|
| Q_NF_INTEGRATION | Neural Forest x Sacred Universe Integration | In Progress | growing |
| Q_SOVEREIGN_AI | Sovereign AI Infrastructure | Active | seed |

#### Completed Quests
| ID | Title |
|---|---|
| Q_V2_MASTERY | Neural Forest v2 Understanding |
| Q_SKILLS_THEORY | Claude Skills Framework Mastery |

#### Growth Markers
- Shipped a working Python knowledge graph system
- Extended an open-source tool with Claude API integration
- Built and packaged first Claude Skill
- Crystallized the Skills > Tools insight

---

## New Player Template
player_id: auto_generated_uuid
name:
archetype:
initiation_status: Pending
gifts: []
active_quests: []
level: 1
"@

$readmes["04_Infrastructure\README.md"] = @"
---
folder: 04_Infrastructure
purpose: The technical foundation — The Bricks
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 04 — Infrastructure

> If it breaks, the answer is here.
> *Rule 6: Tools Amplify, Not Replace — the user remains the musician; tools are instruments.*

## Current Stack
| Layer | Tool |
|---|---|
| Host OS | Windows 10 / WSL2 |
| Local AI | Ollama via Docker |
| Vector DB | ChromaDB |
| UI | Open WebUI |
| Sync | Tailscale |
| Knowledge Graph | Neural Forest v3 (neural_forest_v3.py) |
| Vault | Obsidian |

## Neural Forest
- Script: neural_forest_v3.py (zero dependencies, Python 3.8+)
- Init: python neural_forest.py init sacred_codex.json
- Visualization: Interactive D3.js force-directed graph (drag, hover, zoom, filter)
- Claude API: Direct via stdlib urllib — no pip installs required

## sacredspace-os Docker Compose
Working directory: C:\Users\USER\sacredspace-os
Command: docker compose up -d

## Network Recovery Ritual
1. Confirm Wi-Fi adapter state
2. Disable conflicting network overlays
3. Reconnect internet source
4. Verify DNS and Drive access
5. Document steps in Progress Report

## Files
- Network_Recovery_Protocol.md
- Hardware inventory
- PowerShell automation scripts
"@

$readmes["05_Learning_Spine\README.md"] = @"
---
folder: 05_Learning_Spine
purpose: Processed knowledge and research synthesis
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 05 — Learning Spine

> Raw input becomes refined knowledge here.
> *Rule 5: Difficulty Means Growth Is Near — resistance marks learning edges.*

## Learning Cycle (S@CREDSOURC3 Method)
Essence > Pattern > Example > Practice > Reflection > Integration > Next_Edge

## Seven Learning Prompts
1. First_Principles_Breaker
2. Fast_Context_Builder
3. Feynman_Teacher
4. Example_Accelerator
5. Memory_Lock_In
6. Rapid_Test_Loop
7. 30_Day_System

## NotebookLM Workflow
1. Raw source > NotebookLM (ingest)
2. NotebookLM summary > this folder (clip)
3. Synthesis note > link back to 02_Doctrine or 03_AI_Agents

## Skills Reading Hierarchy
| Level | What Claude Reads | When |
|---|---|---|
| 1 | Folder name / Hook | Always on |
| 2 | SKILL.md body | On demand when triggered |
| 3 | Reference files | Lazy loaded for complex sub-tasks |
"@

$readmes["06_Creative_Universe\README.md"] = @"
---
folder: 06_Creative_Universe
purpose: The mythic, narrative, and aesthetic core
version: SS_OS_v3.1
updated: $(Get-Date -Format "yyyy-MM-dd")
---

# 06 — Creative Universe

> Where the system gets its soul.
> *"A recursive operating system that frames life as structured growth through intentional play, reflection, and evolution."*

## The Family Layer

| Character | Archetype | Quests |
|---|---|---|
| The Fox | Explorer | Curiosity, Skill_Building |
| The Lightbearer | Creator | Expression, Kindness |
| The Gardener | Guide | Holding_Space, Modeling_Play |

## Sacred Arcana Initiation Process
1. Enter container (ritual)
2. Declare quest
3. Engage challenge
4. Capture echo
5. Integrate into codex

## COD3BASE Entity Mapping
| Sacred Entity | Neural Forest Node |
|---|---|
| Player | anchor / player type |
| Quest | project + active_quests tags |
| Echo | node body reflections |
| Archetype | canon or archetype tag |
| Ritual | ritual type |
| BossBattle | project, energy=growing, tag: boss_battle |
| Mycelium Link | connective tissue between all entities |
| SPI | Sacred Progress Index 0-100 |

## Files
- Narrative Bible
- Visual style guides (Nano Banana / Veo prompts)
- World-building drafts and lore
- Council Grove mythology and named seats

## Principle
> Ground. Consolidate. Deploy. Document. Repeat.
"@

# ============================================================
# FOLDER LIST
# ============================================================

$folders = @(
"00_Command_Center",
"01_Progress_Reports",
"02_Doctrine",
"02_Doctrine\01_Rituals",
"02_Doctrine\02_Characters",
"02_Doctrine\03_Rules",
"02_Doctrine\04_Challenges",
"02_Doctrine\05_Tools",
"02_Doctrine\06_Echoes",
"03_AI_Agents",
"04_Infrastructure",
"05_Learning_Spine",
"06_Creative_Universe",
"99_Archive"
)

# ============================================================
# STUB FILES
# ============================================================

$stubs = @{}

$stubs["02_Doctrine\01_Rituals\Opening_Ritual.md"] = "# Opening Ritual`n> Enter the container with intention.`n`n## Steps`n1. `n2. `n3. "
$stubs["02_Doctrine\01_Rituals\Closing_Ritual.md"] = "# Closing Ritual`n> Save progress before leaving the game.`n`n## Steps`n1. `n2. `n3. "
$stubs["02_Doctrine\01_Rituals\Weekly_Reset.md"]   = "# Weekly Reset`n> Level-up review.`n`n## Agenda`n- Review echoes`n- Update quests`n- Set next sprint"
$stubs["02_Doctrine\02_Characters\The_Gardener.md"] = "# The Gardener`n- Archetype: Guide`n- Level: 3`n- Gifts: Systems architecture, Sacred framing, AI sovereignty`n- Active Quests: Q_NF_INTEGRATION, Q_SOVEREIGN_AI"
$stubs["02_Doctrine\02_Characters\The_Fox.md"]      = "# The Fox`n- Archetype: Explorer`n- Quests: Curiosity, Skill_Building"
$stubs["02_Doctrine\02_Characters\The_Lightbearer.md"] = "# The Lightbearer`n- Archetype: Creator`n- Quests: Expression, Kindness"
$stubs["02_Doctrine\04_Challenges\Boss_Battles.md"] = "# Boss Battles`n> Hard moments become growth signals. (Rule 5)`n`n## Active`n"
$stubs["02_Doctrine\04_Challenges\Action_Debt.md"]  = "# Action Debt`n> Tracked commitments not yet fulfilled.`n`n## Outstanding`n"
$stubs["04_Infrastructure\Network_Recovery_Protocol.md"] = "# Network Recovery Protocol`n`n## Steps`n1. Confirm Wi-Fi adapter state`n2. Disable conflicting overlays`n3. Reconnect internet source`n4. Verify DNS and Drive access`n5. Document steps here`n`n## Last Recovery`n- Date:`n- Issue:`n- Resolution:"
$stubs["01_Progress_Reports\2026-03-06_Sacred_Progress_Report.md"] = "# Sacred Progress Report — 2026-03-06`n`n## Summary of Actions`n`n## Artifacts Produced`n`n## System Status`n`n## Blockers`n`n## Next Priorities`n"

# ============================================================
# BUILD
# ============================================================

Write-Host "`n🌱 S∆CR3D Vault Builder v3.1 — NeuralForest Integrated`n" -ForegroundColor Cyan
Write-Host "   S@CREDSOURC3, unfurl the scroll.`n" -ForegroundColor Magenta

foreach ($folder in $folders) {
$fullPath = Join-Path $VaultRoot $folder
New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
Write-Host "  [DIR] $folder" -ForegroundColor DarkCyan
}

Write-Host ""

foreach ($entry in $readmes.GetEnumerator()) {
$filePath = Join-Path $VaultRoot $entry.Key
Set-Content -Path $filePath -Value $entry.Value -Encoding UTF8
Write-Host "  [README] $($entry.Key)" -ForegroundColor Green
}

Write-Host ""

foreach ($entry in $stubs.GetEnumerator()) {
$filePath = Join-Path $VaultRoot $entry.Key
Set-Content -Path $filePath -Value $entry.Value -Encoding UTF8
Write-Host "  [STUB] $($entry.Key)" -ForegroundColor Yellow
}

Write-Host "`n🏛  Vault deployed to: $VaultRoot" -ForegroundColor Cyan
Write-Host "    Open this folder as your Obsidian vault to begin.`n" -ForegroundColor White
Write-Host "⚡ First command after opening vault:" -ForegroundColor White
Write-Host "   python neural_forest.py init sacred_codex.json`n" -ForegroundColor Green
