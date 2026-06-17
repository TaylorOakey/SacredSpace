<!-- converted from link_sacred_codex.ps1.docx -->

# ============================================================
# link_sacred_codex.ps1
# S∆CR3D COD3BASE — Mycelium Link Weaver
# Version: SS_OS_v3.1
# Run AFTER seed_sacred_codex.ps1
# ============================================================
# IMPORTANT: Replace all ID placeholders below with real IDs.
# Get IDs by running:
#   python neural_forest.py ls sacred_codex.json
# ============================================================

$forest = "sacred_codex.json"
$py = "python neural_forest.py"

# --------------------------------------------------------
# PASTE YOUR IDs HERE after running: ls sacred_codex.json
# --------------------------------------------------------
$ANCHOR_CORE       = "REPLACE_A-SacredSpace_Core"
$ANCHOR_SPI        = "REPLACE_A-SPI"

$RULE_1            = "REPLACE_C-Rule1"
$RULE_2            = "REPLACE_C-Rule2"
$RULE_3            = "REPLACE_C-Rule3"
$RULE_4            = "REPLACE_C-Rule4"
$RULE_5            = "REPLACE_C-Rule5"
$RULE_6            = "REPLACE_C-Rule6"
$RULE_7            = "REPLACE_C-Rule7"
$RULE_8            = "REPLACE_C-Rule8"

$GARDENER          = "REPLACE_F-Gardener"
$FOX               = "REPLACE_F-Fox"
$LIGHTBEARER       = "REPLACE_F-Lightbearer"

$RITUAL_OPEN       = "REPLACE_R-Opening"
$RITUAL_CLOSE      = "REPLACE_R-Closing"
$RITUAL_WEEKLY     = "REPLACE_R-Weekly"

$QUEST_NF          = "REPLACE_P-NF_Integration"
$QUEST_AI          = "REPLACE_P-Sovereign_AI"
$QUEST_INFRA       = "REPLACE_P-Infra_Sprint"
$OT_001            = "REPLACE_P-OT001"
$OT_002            = "REPLACE_P-OT002"
$OT_003            = "REPLACE_P-OT003"
$OT_004            = "REPLACE_P-OT004"

$INSIGHT_SKILLS    = "REPLACE_I-Skills"
$INSIGHT_CANON     = "REPLACE_I-Canon"
$INSIGHT_FOREST    = "REPLACE_I-Forest"

$CODEX_AI_PACK     = "REPLACE_X-AIInstructionPack"
$CODEX_SKILLS      = "REPLACE_X-SkillsFramework"
$CODEX_MOI         = "REPLACE_X-MOI"

$BOSS_NETWORK      = "REPLACE_P-BOSS-Network"
$BOSS_SPRAWL       = "REPLACE_P-BOSS-Sprawl"
$BOSS_FRAG         = "REPLACE_P-BOSS-Fragmentation"

# ============================================================
Write-Host "`n🌿 Weaving mycelium links...`n" -ForegroundColor Cyan

# All rules link back to core anchor
Write-Host "--- Rules > Core Anchor ---" -ForegroundColor DarkCyan
foreach ($rule in @($RULE_1,$RULE_2,$RULE_3,$RULE_4,$RULE_5,$RULE_6,$RULE_7,$RULE_8)) {
& cmd /c "$py link $forest --a $rule --b $ANCHOR_CORE --kind mycelium --weight 1.5"
}

# SPI anchors to core
& cmd /c "$py link $forest --a $ANCHOR_SPI --b $ANCHOR_CORE --kind mycelium --weight 2.0"

# Family tethers
Write-Host "`n--- Family Tethers ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $GARDENER --b $ANCHOR_CORE --kind family_tether --weight 2.0"
& cmd /c "$py link $forest --a $FOX --b $GARDENER --kind family_tether --weight 1.5"
& cmd /c "$py link $forest --a $LIGHTBEARER --b $GARDENER --kind family_tether --weight 1.5"

# Rituals bind to Rule 2 (Create the Container)
Write-Host "`n--- Ritual Binds ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $RITUAL_OPEN --b $RULE_2 --kind ritual_bind --weight 1.5"
& cmd /c "$py link $forest --a $RITUAL_CLOSE --b $RULE_2 --kind ritual_bind --weight 1.5"
& cmd /c "$py link $forest --a $RITUAL_WEEKLY --b $RULE_7 --kind ritual_bind --weight 1.5"

# Gardener owns active quests
Write-Host "`n--- Gardener > Active Quests ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $GARDENER --b $QUEST_NF --kind enables --weight 2.0"
& cmd /c "$py link $forest --a $GARDENER --b $QUEST_AI --kind enables --weight 2.0"
& cmd /c "$py link $forest --a $GARDENER --b $QUEST_INFRA --kind enables --weight 1.5"

# Open threads connect to parent quests
Write-Host "`n--- Open Threads ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $OT_001 --b $QUEST_NF --kind enables --weight 2.0"
& cmd /c "$py link $forest --a $OT_002 --b $QUEST_NF --kind enables --weight 1.5"
& cmd /c "$py link $forest --a $OT_003 --b $FOX --kind enables --weight 1.0"
& cmd /c "$py link $forest --a $OT_003 --b $LIGHTBEARER --kind enables --weight 1.0"
& cmd /c "$py link $forest --a $OT_003 --b $GARDENER --kind enables --weight 1.0"
& cmd /c "$py link $forest --a $OT_004 --b $OT_001 --kind enables --weight 1.5"

# Insights link to canon and quests
Write-Host "`n--- Insights > Canon ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $INSIGHT_SKILLS --b $CODEX_SKILLS --kind mycelium --weight 2.0"
& cmd /c "$py link $forest --a $INSIGHT_CANON --b $ANCHOR_CORE --kind mycelium --weight 2.0"
& cmd /c "$py link $forest --a $INSIGHT_FOREST --b $QUEST_NF --kind mycelium --weight 2.0"

# Codex nodes anchor to core
Write-Host "`n--- Codex > Core ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $CODEX_AI_PACK --b $ANCHOR_CORE --kind mycelium --weight 1.5"
& cmd /c "$py link $forest --a $CODEX_SKILLS --b $RULE_6 --kind mycelium --weight 1.5"
& cmd /c "$py link $forest --a $CODEX_MOI --b $ANCHOR_CORE --kind mycelium --weight 2.0"

# Boss battles link to Rule 5 (Difficulty = Growth)
Write-Host "`n--- Boss Battles > Rule 5 ---" -ForegroundColor DarkCyan
& cmd /c "$py link $forest --a $BOSS_NETWORK --b $RULE_5 --kind mycelium --weight 1.5"
& cmd /c "$py link $forest --a $BOSS_SPRAWL --b $RULE_5 --kind mycelium --weight 1.5"
& cmd /c "$py link $forest --a $BOSS_FRAG --b $RULE_5 --kind mycelium --weight 1.5"

# Boss battles block active quests
& cmd /c "$py link $forest --a $BOSS_NETWORK --b $QUEST_INFRA --kind blocks --weight 1.0"
& cmd /c "$py link $forest --a $BOSS_FRAG --b $CODEX_MOI --kind blocks --weight 1.0"

# ============================================================
Write-Host "`n--- FINAL PROGRESS ---" -ForegroundColor Cyan
& cmd /c "$py progress $forest"

Write-Host "`n✅ Mycelium woven. The forest is alive.`n" -ForegroundColor Green
Write-Host "Visualize now:" -ForegroundColor White
Write-Host "  python neural_forest.py visualize sacred_codex.json --format html --out holo.html" -ForegroundColor Yellow
