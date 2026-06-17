<!-- converted from seed_sacred_codex.ps1.docx -->

# ============================================================
# seed_sacred_codex.ps1
# S∆CR3D COD3BASE — Neural Forest Initial Population
# Version: SS_OS_v3.1
# Run AFTER: python neural_forest.py init sacred_codex.json
# ============================================================
# Usage:
#   cd <folder containing neural_forest_v3.py>
#   .\seed_sacred_codex.ps1
# ============================================================

$forest = "sacred_codex.json"
$py = "python neural_forest.py"

Write-Host "`n🌱 Seeding the S∆CR3D COD3BASE...`n" -ForegroundColor Cyan

# ============================================================
# STEP 1 — ANCHOR NODES (stable orienting points)
# ============================================================
Write-Host "--- ANCHORS ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"A- SacredSpace Core`" --type anchor --tags core,system --energy flowing"
& cmd /c "$py seed $forest --title `"A- Sacred Progress Index`" --type anchor --tags spi,metrics --energy flowing"

# ============================================================
# STEP 2 — CANON NODES (the 8 Game Rules)
# ============================================================
Write-Host "`n--- CANON: 8 GAME RULES ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"C- Rule 1: The World Is the Game Board`" --type canon --tags rule,game_board --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 2: Create the Container`" --type canon --tags rule,container,ritual --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 3: You Are the Avatar`" --type canon --tags rule,avatar,identity --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 4: Rules Enable Play`" --type canon --tags rule,governance --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 5: Difficulty Means Growth Is Near`" --type canon --tags rule,challenge,growth --energy growing"
& cmd /c "$py seed $forest --title `"C- Rule 6: Tools Amplify Not Replace`" --type canon --tags rule,tools,sovereignty --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 7: Reflection Locks Progress`" --type canon --tags rule,reflection,echo --energy flowing"
& cmd /c "$py seed $forest --title `"C- Rule 8: The Game Evolves`" --type canon --tags rule,evolution,versioning --energy seed"

# ============================================================
# STEP 3 — FAMILY NODES
# ============================================================
Write-Host "`n--- FAMILY LAYER ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"F- The Gardener`" --type family --tags guide,archetype,player,level_3 --energy growing"
& cmd /c "$py seed $forest --title `"F- The Fox`" --type family --tags explorer,archetype --energy seed"
& cmd /c "$py seed $forest --title `"F- The Lightbearer`" --type family --tags creator,archetype --energy seed"

# ============================================================
# STEP 4 — RITUAL NODES
# ============================================================
Write-Host "`n--- RITUALS ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"R- Opening Ritual`" --type ritual --tags entry,container,daily --energy flowing"
& cmd /c "$py seed $forest --title `"R- Closing Ritual`" --type ritual --tags exit,save_progress,daily --energy flowing"
& cmd /c "$py seed $forest --title `"R- Weekly Reset`" --type ritual --tags level_up,review,weekly --energy seed"

# ============================================================
# STEP 5 — PROJECT NODES (active quests)
# ============================================================
Write-Host "`n--- ACTIVE QUESTS ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"P- Neural Forest x Sacred Universe Integration`" --type project --tags quest,neural_forest,Q_NF_INTEGRATION --energy growing"
& cmd /c "$py seed $forest --title `"P- Sovereign AI Infrastructure`" --type project --tags quest,infrastructure,Q_SOVEREIGN_AI --energy seed"
& cmd /c "$py seed $forest --title `"P- Infrastructure Consolidation Sprint`" --type project --tags sprint,network,docker,obsidian --energy growing"
& cmd /c "$py seed $forest --title `"P- OT_001: Initialize Sacred Codex Forest`" --type project --tags open_thread,HIGH --energy growing"
& cmd /c "$py seed $forest --title `"P- OT_002: Player Registry in Forest`" --type project --tags open_thread,HIGH --energy seed"
& cmd /c "$py seed $forest --title `"P- OT_003: Auto-Reflect Family Layer`" --type project --tags open_thread,MEDIUM --energy seed"
& cmd /c "$py seed $forest --title `"P- OT_004: Sacred Storyline Visualization`" --type project --tags open_thread,MEDIUM --energy seed"

# ============================================================
# STEP 6 — CODEX NODES (reference structures)
# ============================================================
Write-Host "`n--- CODEX NODES ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"X- AI Instruction Pack`" --type codex --tags doctrine,agents,claude,gemini --energy flowing"
& cmd /c "$py seed $forest --title `"X- Skills Framework`" --type codex --tags skills,blueprints,hierarchy --energy flowing"
& cmd /c "$py seed $forest --title `"X- Master Operating Index`" --type codex --tags MOI,hub,canonical --energy growing"

# ============================================================
# STEP 7 — INSIGHT NODES (crystallized realizations)
# ============================================================
Write-Host "`n--- INSIGHTS ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"I- Skills are blueprints tools are hands`" --type insight --tags skills,tools,canon --energy flowing"
& cmd /c "$py seed $forest --title `"I- Interaction writes canon`" --type insight --tags canon,principle --energy flowing"
& cmd /c "$py seed $forest --title `"I- The forest is executable and Claude-native`" --type insight --tags neural_forest,claude,canon --energy flowing"

# ============================================================
# STEP 8 — CHALLENGE NODES (boss battles)
# ============================================================
Write-Host "`n--- CHALLENGES ---" -ForegroundColor Magenta

& cmd /c "$py seed $forest --title `"P- BOSS: Connectivity Instability`" --type project --tags boss_battle,infrastructure,network --energy growing"
& cmd /c "$py seed $forest --title `"P- BOSS: Toolchain Sprawl`" --type project --tags boss_battle,entropy,consolidation --energy growing"
& cmd /c "$py seed $forest --title `"P- BOSS: Canonical Knowledge Fragmentation`" --type project --tags boss_battle,doctrine,version_drift --energy growing"

# ============================================================
# CHECK PROGRESS
# ============================================================
Write-Host "`n--- PROGRESS CHECK ---" -ForegroundColor Cyan
& cmd /c "$py progress $forest"

Write-Host "`n✅ Sacred Codex seeded.`n" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Run: python neural_forest.py ls sacred_codex.json" -ForegroundColor Yellow
Write-Host "     Confirm all nodes are present and note their IDs." -ForegroundColor DarkYellow
Write-Host ""
Write-Host "  2. Run the link script: .\link_sacred_codex.ps1" -ForegroundColor Yellow
Write-Host "     Weaves the mycelium connections between nodes." -ForegroundColor DarkYellow
Write-Host ""
Write-Host "  3. Visualize: python neural_forest.py visualize sacred_codex.json --format html --out holo.html" -ForegroundColor Yellow
Write-Host "     Open holo.html in your browser — the living dashboard." -ForegroundColor DarkYellow
