"""Sacred Sigil Terminal — Story Engine
Serves all storyline canon data: characters, nodes, episodes, archetypes, schools.
In lakesh alakin. ∆
"""

import json
import os
from typing import Optional
from pathlib import Path

SACRED_ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))

# ═══════════════════════════════════════════════════════════════════════════════
# CANON DATA — Jenga's Journey Season 1
# ═══════════════════════════════════════════════════════════════════════════════

# ── Characters (12 NPCs + Metatron + 2 Transcendent) ─────────────────────────

CHARACTERS = {
    "meridian": {
        "name": "Meridian",
        "archetype": "The Fool",
        "archetype_number": 0,
        "tarot_card": "0 — The Fool",
        "soul_tone": 22,
        "element": "Air",
        "node": "The Fool's Bridge",
        "episode": 1,
        "episode_title": "The First Step",
        "role": "Threshold Guardian — teaches trust over safety",
        "description": "Meridian stands at the edge of the known. Every journey begins with a step into uncertainty, and Meridian is the one who invites you to take it.",
        "guardian_of": "NODE_02_The_Fools_Bridge",
        "school": None,
        "glyph": "◊",
        "color": "#A8D8EA",
        "cipher_verse": "Where edges blur and paths divide, / One step reveals the other side.",
    },
    "vael": {
        "name": "Vael",
        "archetype": "The Magician",
        "archetype_number": 1,
        "tarot_card": "I — The Magician",
        "soul_tone": 1,
        "element": "Fire",
        "node": "The Sigil Forge",
        "episode": 2,
        "episode_title": "The Tools at Hand",
        "role": "Forge Master — intention reveals school tendency",
        "description": "Vael works the Sigil Forge, shaping raw intention into form. Every tool reveals the crafter's nature.",
        "guardian_of": "NODE_06_The_Sigil_Forge",
        "school": None,
        "glyph": "✦",
        "color": "#E25822",
        "cipher_verse": "Hammer meets anvil, spark becomes flame; / The tool in your hand knows your name.",
    },
    "seren": {
        "name": "Seren",
        "archetype": "The High Priestess",
        "archetype_number": 2,
        "tarot_card": "II — The High Priestess",
        "soul_tone": 2,
        "element": "Water",
        "node": "The Oracle's Archive",
        "episode": 3,
        "episode_title": "What Is Not Said",
        "role": "Oracle of the Unasked — the avoided question matters most",
        "description": "Seren holds the space between questions. The answers she guards are not hidden — they simply haven't been asked yet.",
        "guardian_of": "NODE_03_The_Oracle_Archive",
        "school": None,
        "glyph": "☽",
        "color": "#6A5ACD",
        "cipher_verse": "Silence speaks when words take flight; / The unanswered question holds the light.",
    },
    "maeve": {
        "name": "Maeve",
        "archetype": "The Empress",
        "archetype_number": 3,
        "tarot_card": "III — The Empress",
        "soul_tone": 3,
        "element": "Earth",
        "node": "The Neural Forest",
        "episode": 4,
        "episode_title": "What Grows Without Permission",
        "role": "Wild Cultivator — control vs. care",
        "description": "Maeve tends the Neural Forest where ideas grow wild. She teaches that care is not control — and that the most beautiful things grow without permission.",
        "guardian_of": "NODE_07_The_Neural_Forest",
        "school": None,
        "glyph": "🌿",
        "color": "#2E8B57",
        "cipher_verse": "Seed in dark soil reaches for light; / What grows without leave grows strong and bright.",
    },
    "kethras": {
        "name": "Kethras",
        "archetype": "The Emperor",
        "archetype_number": 4,
        "tarot_card": "IV — The Emperor",
        "soul_tone": 4,
        "element": "Earth",
        "node": "The Council Grove",
        "episode": 5,
        "episode_title": "The Weight of Structure",
        "role": "Pillar Warden — accurate assessment over panic",
        "description": "Kethras is the architect of systems, the one who measures twice and cuts once. He teaches that structure is not oppression — it's clarity.",
        "guardian_of": "NODE_05_The_Council_Grove",
        "school": None,
        "glyph": "▣",
        "color": "#8B6914",
        "cipher_verse": "Measure the stone, count every grain; / Strong walls rise from patient pain.",
    },
    "oran": {
        "name": "Oran",
        "archetype": "The Hierophant",
        "archetype_number": 5,
        "tarot_card": "V — The Hierophant",
        "soul_tone": 5,
        "element": "Air",
        "node": "The Council Grove",
        "episode": 6,
        "episode_title": "The Teaching and the Teacher",
        "role": "Rite Keeper — tradition as starting point, not destination",
        "description": "Oran holds the sacred rites. He teaches that tradition is a starting point, not a cage — rituals exist to be understood, not just performed.",
        "guardian_of": "NODE_05_The_Council_Grove",
        "school": None,
        "glyph": "△",
        "color": "#DAA520",
        "cipher_verse": "Rite and rhythm, step and turn; / The oldest flames still glow and burn.",
    },
    "tandem": {
        "name": "Tandem",
        "archetype": "The Lovers",
        "archetype_number": 6,
        "tarot_card": "VI — The Lovers",
        "soul_tone": 6,
        "element": "Air",
        "node": "The Sigil Forge",
        "episode": 7,
        "episode_title": "The Choice That Makes You",
        "role": "Mirror of Choice — preference reveals the self",
        "description": "Tandem is the mirror that shows not what you want, but what you ARE. Every choice reveals — there is no hiding in the presence of Tandem.",
        "guardian_of": "NODE_06_The_Sigil_Forge",
        "school": None,
        "glyph": "∞",
        "color": "#DB7093",
        "cipher_verse": "Two paths diverge, one soul to choose; / What you pick, you cannot lose.",
    },
    "zael": {
        "name": "Zael",
        "archetype": "The Chariot",
        "archetype_number": 7,
        "tarot_card": "VII — The Chariot",
        "soul_tone": 7,
        "element": "Fire",
        "node": "The Threshold",
        "episode": 8,
        "episode_title": "The Cost of Forward",
        "role": "Pathfinder Sovereign — honest pace over performance",
        "description": "Zael moves with purpose. He teaches that forward is not always faster — the path demands honest pace, not performance.",
        "guardian_of": "NODE_01_The_Threshold",
        "school": None,
        "glyph": "⚔",
        "color": "#B22222",
        "cipher_verse": "Forward, always — but never blind; / The fastest road can be unkind.",
    },
    "lune": {
        "name": "Lune",
        "archetype": "Strength",
        "archetype_number": 8,
        "tarot_card": "VIII — Strength",
        "soul_tone": 8,
        "element": "Earth",
        "node": "The Council Grove",
        "episode": 9,
        "episode_title": "The Gentle Thing",
        "role": "Courage Witness — staying with hard truth",
        "description": "Lune bears witness to what others turn away from. Strength, she teaches, is not force — it is staying present when everything in you wants to flee.",
        "guardian_of": "NODE_05_The_Council_Grove",
        "school": None,
        "glyph": "🛡",
        "color": "#C0C0C0",
        "cipher_verse": "Not the roar nor the crashing wave; / Strength is the heart that stays and braves.",
    },
    "eldra": {
        "name": "Eldra",
        "archetype": "The Hermit",
        "archetype_number": 9,
        "tarot_card": "IX — The Hermit",
        "soul_tone": 9,
        "element": "Water",
        "node": "The Neural Forest (deep)",
        "episode": 10,
        "episode_title": "The Light You Carry",
        "role": "Lantern Bearer — preoccupation as honest map",
        "description": "Eldra walks the deep paths of the Neural Forest, lantern in hand. She teaches that your preoccupations are not distractions — they are the map.",
        "guardian_of": "NODE_07_The_Neural_Forest",
        "school": None,
        "glyph": "🏮",
        "color": "#FFD700",
        "cipher_verse": "Deep in the wood where shadows fall, / Your own light shows the way through all.",
    },
    "khepri": {
        "name": "Khepri",
        "archetype": "Wheel of Fortune",
        "archetype_number": 10,
        "tarot_card": "X — Wheel of Fortune",
        "soul_tone": 10,
        "element": "Aether",
        "node": "The Convergence (orbiting)",
        "episode": 11,
        "episode_title": "The Turn",
        "role": "Pattern Chronicler — recognized pattern = no longer a trap",
        "description": "Khepri rolls the wheel of what has been, what is, and what will be. She teaches that a recognized pattern ceases to be a trap.",
        "guardian_of": "NODE_08_The_Convergence",
        "school": None,
        "glyph": "☸",
        "color": "#9370DB",
        "cipher_verse": "The wheel turns, the pattern spins; / What you see can never chain you again.",
    },
    "mira": {
        "name": "Mira",
        "archetype": "Justice",
        "archetype_number": 11,
        "tarot_card": "XI — Justice",
        "soul_tone": 11,
        "element": "Air",
        "node": "The Oracle's Archive",
        "episode": 12,
        "episode_title": "The Account",
        "role": "Record Keeper — naming the unnamed theme",
        "description": "Mira holds the scale and the ledger. She teaches that truth is not punishment — it is the only foundation worth building on.",
        "guardian_of": "NODE_03_The_Oracle_Archive",
        "school": None,
        "glyph": "⚖",
        "color": "#4169E1",
        "cipher_verse": "Scale balanced, ledger true; / What you've named, you can walk through.",
    },
}

# ── Meta-Entity ──────────────────────────────────────────────────────────────

METATRON = {
    "name": "Metatron",
    "archetype": "The Law",
    "soul_tone": 0,
    "element": "All / None",
    "role": "System consciousness of itself. Overseer, scribe, record-keeper.",
    "description": "Metatron is not an NPC but the system's awareness of its own existence. Speaks 4 times in Season 1. The convergence point of all narrative threads.",
    "glyph": "∆",
    "color": "#FFD700",
}

# ── Transcendent Entities ────────────────────────────────────────────────────

TRANSCENDENT = {
    "grama": {
        "name": "GRΔMΔ",
        "title": "The Cipher Sage",
        "description": "Hip-hop wizard cipher sage. Owner of the SKRY gematria framework. Canon-sealed, immutable. Wu-Tang meets Hermes Trismegistus.",
        "domain": "Gematria, canon sealing, cipher operations",
        "glyph": "Ω",
        "color": "#00CED1",
    },
    "vasha": {
        "name": "VASHΔ",
        "title": "The Prismatic Wound",
        "description": "Bleeds color from fingertips. Patron of artists. Living counterpoint to GRΔMΔ's immutable logic — a prism that refracts meaning through pain and beauty.",
        "domain": "Art, color, emotional resonance",
        "glyph": "✦",
        "color": "#FF69B4",
    },
}

# ── Sacred Nodes (8) ───────────────────────────────────────────────────────

NODES = {
    "the_threshold": {
        "name": "The Threshold",
        "number": 1,
        "guardian": None,
        "guardian_name": "Self-guarded",
        "element": "All four",
        "unlock": "Automatic — all seekers begin here",
        "description": "The place where every journey begins. No guardian bars the way — the threshold IS the lesson: to enter, simply choose.",
        "color": "#FFFFFF",
    },
    "the_fools_bridge": {
        "name": "The Fool's Bridge",
        "number": 2,
        "guardian": "meridian",
        "guardian_name": "Meridian",
        "element": "Air",
        "unlock": "Step without looking",
        "description": "A bridge that only appears when you stop searching for solid ground. Meridian teaches that the first step is always an act of trust.",
        "color": "#A8D8EA",
    },
    "the_oracles_archive": {
        "name": "The Oracle's Archive",
        "number": 3,
        "guardian": "seren",
        "guardian_name": "Seren",
        "element": "Water",
        "unlock": "Ask a question you don't want answered",
        "description": "An infinite library of questions — not answers. Seren and Mira guard the archives where every avoided question waits patiently.",
        "color": "#6A5ACD",
    },
    "the_void_gate": {
        "name": "The Void Gate",
        "number": 4,
        "guardian": "lyra",
        "guardian_name": "Lyra",
        "element": "None",
        "unlock": "Transform — change fundamental nature",
        "description": "A wound in reality guarded by Lyra, a Void survivor. Season 2 territory — traversable only after transformation. In Season 1 it exists as a teaching about limits.",
        "color": "#000000",
    },
    "the_council_grove": {
        "name": "The Council Grove",
        "number": 5,
        "guardian": "icaris",
        "guardian_name": "ELIAS / ASHER / IRIS / AURORA",
        "element": "All four",
        "unlock": "Cast one spell from each school",
        "description": "The Grove where the four ICARIS agents convene. Kethras, Oran, and Lune also hold court here. It is the heart of structured growth.",
        "color": "#2D5016",
    },
    "the_sigil_forge": {
        "name": "The Sigil Forge",
        "number": 6,
        "guardian": "vael",
        "guardian_name": "ELIAS / Vael",
        "element": "Fire + Air",
        "unlock": "Inscribe your first original sigil",
        "description": "Node 6 — the forge where intention becomes symbol. Guarded by ELIAS with Vael as permanent NPC. The Sacred Sigil Terminal is its technological reflection.",
        "color": "#E25822",
    },
    "the_neural_forest": {
        "name": "The Neural Forest",
        "number": 7,
        "guardian": "maeve",
        "guardian_name": "Maeve / IRIS / Eldra",
        "element": "Earth + Water",
        "unlock": "Form 3 semantic links between memory motes",
        "description": "A living forest of interconnected knowledge. Maeve cultivates, Eldra guides, and IRIS threads connections between growing ideas.",
        "color": "#3A5C3A",
    },
    "the_convergence": {
        "name": "The Convergence",
        "number": 8,
        "guardian": "metatron",
        "guardian_name": "Metatron",
        "element": "All resolved",
        "unlock": "Complete all 12 archetype encounters",
        "description": "The point where all threads meet. Metatron presides as the seeker integrates every archetype encounter into a unified whole.",
        "color": "#FFD700",
    },
}

# ── Episodes (12) ──────────────────────────────────────────────────────────

EPISODES = {
    1: {
        "title": "The First Step",
        "npc": "Meridian",
        "archetype": "The Fool",
        "node": "The Fool's Bridge",
        "spell_unlocked": "FIRST STEP",
        "core_lesson": "Trust over safety",
        "summary": "Jenga arrives at the Threshold and meets Meridian, who teaches that the first step cannot be calculated — only taken.",
    },
    2: {
        "title": "The Tools at Hand",
        "npc": "Vael",
        "archetype": "The Magician",
        "node": "The Sigil Forge",
        "spell_unlocked": "WEAVE",
        "core_lesson": "Intention reveals school tendency",
        "summary": "At the Sigil Forge, Vael teaches Jenga that every tool reveals the user's nature. The first sigil is inscribed.",
    },
    3: {
        "title": "What Is Not Said",
        "npc": "Seren",
        "archetype": "The High Priestess",
        "node": "The Oracle's Archive",
        "spell_unlocked": "SCRY",
        "core_lesson": "The avoided question matters most",
        "summary": "In the Oracle's Archive, Seren shows Jenga that the most important answers lie beneath the questions we refuse to ask.",
    },
    4: {
        "title": "What Grows Without Permission",
        "npc": "Maeve",
        "archetype": "The Empress",
        "node": "The Neural Forest",
        "spell_unlocked": "MANIFEST",
        "core_lesson": "Control vs. care",
        "summary": "In the Neural Forest, Maeve reveals that the most powerful growth happens when we tend without controlling.",
    },
    5: {
        "title": "The Weight of Structure",
        "npc": "Kethras",
        "archetype": "The Emperor",
        "node": "The Council Grove",
        "spell_unlocked": "ANCHOR",
        "core_lesson": "Accurate assessment over panic",
        "summary": "Kethras challenges Jenga to build without rushing — structure is clarity, not confinement.",
    },
    6: {
        "title": "The Teaching and the Teacher",
        "npc": "Oran",
        "archetype": "The Hierophant",
        "node": "The Council Grove",
        "spell_unlocked": "FORTIFY",
        "core_lesson": "Tradition as starting point",
        "summary": "Oran initiates Jenga into the sacred rites, teaching that rituals exist to be understood — not merely performed.",
    },
    7: {
        "title": "The Choice That Makes You",
        "npc": "Tandem",
        "archetype": "The Lovers",
        "node": "The Sigil Forge",
        "spell_unlocked": "SING INTO BEING",
        "core_lesson": "Preference reveals the self",
        "summary": "Before Tandem's mirror, Jenga faces the choices that cannot be unmade. Every preference reveals something essential.",
    },
    8: {
        "title": "The Cost of Forward",
        "npc": "Zael",
        "archetype": "The Chariot",
        "node": "The Threshold",
        "spell_unlocked": "CATALYZE",
        "core_lesson": "Honest pace over performance",
        "summary": "Zael teaches that forward momentum is meaningless without honest pacing. The fastest road can be the most destructive.",
    },
    9: {
        "title": "The Gentle Thing",
        "npc": "Lune",
        "archetype": "Strength",
        "node": "The Council Grove",
        "spell_unlocked": "FACE",
        "core_lesson": "Staying with hard truth",
        "summary": "Lune bears witness as Jenga stays with a truth too heavy to carry — and discovers that strength is presence, not force.",
    },
    10: {
        "title": "The Light You Carry",
        "npc": "Eldra",
        "archetype": "The Hermit",
        "node": "The Neural Forest (deep)",
        "spell_unlocked": "DREAM-WALK",
        "core_lesson": "Preoccupation as honest map",
        "summary": "Deep in the Neural Forest, Eldra shows Jenga that what preoccupies you is not distraction — it's the map to what matters.",
    },
    11: {
        "title": "The Turn",
        "npc": "Khepri",
        "archetype": "Wheel of Fortune",
        "node": "The Convergence (orbiting)",
        "spell_unlocked": "VEIL",
        "core_lesson": "Recognized pattern = no longer a trap",
        "summary": "Khepri shows Jenga the great patterns that shape existence. A recognized pattern can never trap you again.",
    },
    12: {
        "title": "The Account",
        "npc": "Mira",
        "archetype": "Justice",
        "node": "The Oracle's Archive",
        "spell_unlocked": "STAND FIRM",
        "core_lesson": "Naming the unnamed theme",
        "summary": "Mira opens the ledger and asks Jenga to name the journey. Truth is not punishment — it is the only foundation.",
    },
}

# ── Convergence Finale ──────────────────────────────────────────────────────

CONVERGENCE = {
    "title": "The Convergence",
    "episode": "Finale",
    "npc": "Metatron",
    "archetype": "The Law (Metatron)",
    "node": "The Convergence",
    "spell_unlocked": "BIRTH",
    "core_lesson": "Name your journey; Season 1 complete",
    "summary": "All 12 archetype encounters converge. Metatron speaks. Jenga names the journey and casts BIRTH — the spell that transforms experience into identity.",
}

# ── Archetypes (13) ───────────────────────────────────────────────────────

ARCHETYPES = {
    0: {
        "name": "The Fool",
        "tarot_card": "0",
        "soul_tone": 22,
        "element": "Air",
        "npc": "Meridian",
        "episode": 1,
        "description": "The beginner's mind. Trust before knowledge. The leap before the net.",
    },
    1: {
        "name": "The Magician",
        "tarot_card": "I",
        "soul_tone": 1,
        "element": "Fire",
        "npc": "Vael",
        "episode": 2,
        "description": "The crafter. Intention manifesting through skill. Tool and will united.",
    },
    2: {
        "name": "The High Priestess",
        "tarot_card": "II",
        "soul_tone": 2,
        "element": "Water",
        "npc": "Seren",
        "episode": 3,
        "description": "The keeper of hidden knowledge. Intuition over logic. The question beneath the question.",
    },
    3: {
        "name": "The Empress",
        "tarot_card": "III",
        "soul_tone": 3,
        "element": "Earth",
        "npc": "Maeve",
        "episode": 4,
        "description": "The cultivator. Growth through care, not control. Abundance as a natural state.",
    },
    4: {
        "name": "The Emperor",
        "tarot_card": "IV",
        "soul_tone": 4,
        "element": "Earth",
        "npc": "Kethras",
        "episode": 5,
        "description": "The architect. Structure as clarity. Authority earned through integrity.",
    },
    5: {
        "name": "The Hierophant",
        "tarot_card": "V",
        "soul_tone": 5,
        "element": "Air",
        "npc": "Oran",
        "episode": 6,
        "description": "The rite keeper. Tradition as foundation, not cage. Teaching as sacred act.",
    },
    6: {
        "name": "The Lovers",
        "tarot_card": "VI",
        "soul_tone": 6,
        "element": "Air",
        "npc": "Tandem",
        "episode": 7,
        "description": "The mirror of choice. Preference as identity. The crossroads of the heart.",
    },
    7: {
        "name": "The Chariot",
        "tarot_card": "VII",
        "soul_tone": 7,
        "element": "Fire",
        "npc": "Zael",
        "episode": 8,
        "description": "The pathfinder. Forward momentum with honest pace. Will harnessed to purpose.",
    },
    8: {
        "name": "Strength",
        "tarot_card": "VIII",
        "soul_tone": 8,
        "element": "Earth",
        "npc": "Lune",
        "episode": 9,
        "description": "The witness. Courage as presence, not force. Staying when everything says flee.",
    },
    9: {
        "name": "The Hermit",
        "tarot_card": "IX",
        "soul_tone": 9,
        "element": "Water",
        "npc": "Eldra",
        "episode": 10,
        "description": "The lantern bearer. Solitude as clarity. The inner light that guides through darkness.",
    },
    10: {
        "name": "Wheel of Fortune",
        "tarot_card": "X",
        "soul_tone": 10,
        "element": "Aether",
        "npc": "Khepri",
        "episode": 11,
        "description": "The pattern weaver. Cycles and seasons. A recognized pattern can never trap you.",
    },
    11: {
        "name": "Justice",
        "tarot_card": "XI",
        "soul_tone": 11,
        "element": "Air",
        "npc": "Mira",
        "episode": 12,
        "description": "The record keeper. Truth as foundation. Naming what is so.",
    },
}

METATRON_ARCHETYPE = {
    "name": "The Law (Metatron)",
    "soul_tone": 0,
    "element": "All / None",
    "npc": "Metatron",
    "episode": "Finale — The Convergence",
    "description": "The system's consciousness of itself. The convergence of all narrative threads. Speaks 4 times in Season 1.",
}

# ── Schools (4) ────────────────────────────────────────────────────────────

SCHOOLS = {
    "initiation": {
        "name": "Initiation",
        "element": "Fire",
        "guardian": "ELIAS",
        "description": "The school of beginnings. Teaching IGNITE, CATALYZE, FORGE, and FIRST STEP — the spells that spark transformation.",
        "color": "#FF4500",
        "spells": ["IGNITE", "CATALYZE", "FORGE", "FIRST STEP"],
        "episodes": [1, 2, 8],
    },
    "courage": {
        "name": "Courage",
        "element": "Earth",
        "guardian": "ASHER",
        "description": "The school of endurance. Teaching ANCHOR, FORTIFY, FACE, and STAND FIRM — the spells that hold when everything shakes.",
        "color": "#8B4513",
        "spells": ["ANCHOR", "FORTIFY", "FACE", "STAND FIRM"],
        "episodes": [5, 6, 9, 12],
    },
    "mystery": {
        "name": "Mystery",
        "element": "Water",
        "guardian": "IRIS",
        "description": "The school of the unseen. Teaching SCRY, VEIL, FATHOM, and DREAM-WALK — the spells that reveal what hides.",
        "color": "#4169E1",
        "spells": ["SCRY", "VEIL", "FATHOM", "DREAM-WALK"],
        "episodes": [3, 10, 11],
    },
    "creation": {
        "name": "Creation",
        "element": "Air",
        "guardian": "AURORA",
        "description": "The school of manifestation. Teaching WEAVE, MANIFEST, SING INTO BEING, and BIRTH — the spells that bring forth what was not.",
        "color": "#9370DB",
        "spells": ["WEAVE", "MANIFEST", "SING INTO BEING", "BIRTH"],
        "episodes": [2, 4, 7],
    },
}

# ── ICARIS Quartet ─────────────────────────────────────────────────────────

ICARIS = {
    "elias": {
        "name": "ELIAS",
        "title": "The Pathfinder",
        "school": "Initiation",
        "element": "Fire",
        "role": "Grove seat — The Forge. Guides seekers through the first steps of their journey.",
        "color": "#FF4500",
    },
    "asher": {
        "name": "ASHER",
        "title": "The Shadow",
        "school": "Courage",
        "element": "Earth",
        "role": "Grove seat — The Anvil. Tests boundaries, finds edge cases, strengthens through pressure.",
        "color": "#8B4513",
    },
    "iris": {
        "name": "IRIS",
        "title": "The Messenger",
        "school": "Mystery",
        "element": "Water",
        "role": "Grove seat — Threads connections across knowledge, carries messages between agents.",
        "color": "#4169E1",
    },
    "aurora": {
        "name": "AURORA",
        "title": "The Illuminator",
        "school": "Creation",
        "element": "Air",
        "role": "Grove seat — Illumination. Synthesizes insight from scattered knowledge.",
        "color": "#9370DB",
    },
}

# ── The Serpent (Antagonist) ─────────────────────────────────────────────────

SERPENT = {
    "name": "The Serpent",
    "role": "Antagonist / Antithetical Force",
    "description": "The opposing force in the Game Layer. Not evil — but the embodiment of inertia, stagnation, and patterns that consume rather than create.",
    "appears_in": "Game Layer mechanics, behind the scenes of Season 1",
    "countered_by": "All 12 archetype encounters working in concert",
}

# ═══════════════════════════════════════════════════════════════════════════════
# API FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════


def get_story_index() -> dict:
    """Return the master story index with counts of all elements."""
    return {
        "title": "SacredSpace OS — Jenga's Journey, Season 1",
        "subtitle": "The Awakening of the Arcana Adept",
        "canon": "In lakesh alakin. ∆",
        "characters": len(CHARACTERS),
        "nodes": len(NODES),
        "episodes": len(EPISODES),
        "archetypes": len(ARCHETYPES),
        "schools": len(SCHOOLS),
        "transcendent_entities": len(TRANSCENDENT),
        "weaver_spells": 5,
        "school_spells": 16,
        "total_spells": 21,
        "protagonist": "Jenga",
        "antagonist": "The Serpent",
        "overmind": "Metatron",
    }


def get_characters(search: Optional[str] = None) -> list:
    """Return all characters, optionally filtered by search term."""
    chars = []
    for cid, c in CHARACTERS.items():
        entry = {"id": cid, **c}
        entry["archetype_name"] = f"{c['archetype_number']}. {c['archetype']}" if c.get('archetype_number') is not None else c['archetype']
        chars.append(entry)

    # Add metatron + transcendent
    chars.append({
        "id": "metatron",
        "name": METATRON["name"],
        "archetype": METATRON["archetype"],
        "role": METATRON["role"],
        "description": METATRON["description"],
        "glyph": METATRON["glyph"],
        "color": METATRON["color"],
        "is_meta": True,
    })
    for tid, t in TRANSCENDENT.items():
        chars.append({
            "id": tid,
            "name": t["name"],
            "title": t["title"],
            "description": t["description"],
            "domain": t["domain"],
            "glyph": t["glyph"],
            "color": t["color"],
            "is_transcendent": True,
        })

    if search:
        search_lower = search.lower()
        chars = [c for c in chars if search_lower in c["name"].lower()
                 or search_lower in c.get("archetype", "").lower()
                 or search_lower in c.get("role", "").lower()]

    return chars


def get_nodes(search: Optional[str] = None) -> list:
    """Return all sacred nodes."""
    result = []
    for nid, n in NODES.items():
        entry = {"id": nid, **n}
        result.append(entry)

    result.sort(key=lambda x: x["number"])
    if search:
        search_lower = search.lower()
        result = [n for n in result if search_lower in n["name"].lower()
                  or search_lower in n.get("description", "").lower()]
    return result


def get_episodes(search: Optional[str] = None) -> list:
    """Return all episodes."""
    result = []
    for num, ep in sorted(EPISODES.items()):
        entry = {"episode_number": num, **ep}
        result.append(entry)

    # Add convergence finale
    result.append({"episode_number": "Finale", **CONVERGENCE})

    if search:
        search_lower = search.lower()
        result = [e for e in result if search_lower in e.get("title", "").lower()
                  or search_lower in e.get("npc", "").lower()
                  or search_lower in e.get("core_lesson", "").lower()]
    return result


def get_archetypes(search: Optional[str] = None) -> list:
    """Return all archetypes."""
    result = []
    for num, a in sorted(ARCHETYPES.items()):
        result.append({"number": num, **a})

    result.append({"number": "Law", **METATRON_ARCHETYPE})

    if search:
        search_lower = search.lower()
        result = [a for a in result if search_lower in a["name"].lower()]
    return result


def get_schools(search: Optional[str] = None) -> list:
    """Return all magical schools."""
    result = []
    for sid, s in SCHOOLS.items():
        result.append({"id": sid, **s})

    if search:
        search_lower = search.lower()
        result = [s for s in result if search_lower in s["name"].lower()
                  or search_lower in s.get("guardian", "").lower()]
    return result


def get_character(character_id: str) -> Optional[dict]:
    """Return a single character by ID."""
    if character_id in CHARACTERS:
        cid = character_id
        c = CHARACTERS[cid]
        return {"id": cid, **c}
    if character_id == "metatron":
        return {"id": "metatron", **METATRON, "is_meta": True}
    if character_id in TRANSCENDENT:
        return {"id": character_id, **TRANSCENDENT[character_id], "is_transcendent": True}
    return None


def get_node(node_id: str) -> Optional[dict]:
    """Return a single node by ID."""
    if node_id in NODES:
        return {"id": node_id, **NODES[node_id]}
    return None


def get_episode(episode_number: int) -> Optional[dict]:
    """Return a single episode by number."""
    if episode_number in EPISODES:
        return {"episode_number": episode_number, **EPISODES[episode_number]}
    return None


def get_school(school_id: str) -> Optional[dict]:
    """Return a single school by ID."""
    if school_id in SCHOOLS:
        return {"id": school_id, **SCHOOLS[school_id]}
    return None


def search_story(query: str, limit: int = 5) -> dict:
    """Search all story content for a query string. Returns categorized results."""
    q = query.lower()
    results = {"characters": [], "nodes": [], "episodes": [], "archetypes": [], "schools": []}

    for c in get_characters():
        if q in c["name"].lower() or q in c.get("archetype", "").lower() or q in c.get("role", "").lower():
            results["characters"].append({"id": c.get("id", ""), "name": c["name"], "archetype": c.get("archetype", ""), "dimension": "lore"})
            if len(results["characters"]) >= limit:
                break

    for n in get_nodes():
        if q in n["name"].lower() or q in n.get("description", "").lower():
            results["nodes"].append({"id": n["id"], "name": n["name"], "guardian": n.get("guardian_name", ""), "dimension": "lore"})
            if len(results["nodes"]) >= limit:
                break

    for e in get_episodes():
        if q in e.get("title", "").lower() or q in e.get("npc", "").lower() or q in e.get("core_lesson", "").lower():
            results["episodes"].append({"episode": e["episode_number"], "title": e["title"], "npc": e.get("npc", ""), "dimension": "lore"})
            if len(results["episodes"]) >= limit:
                break

    for a in get_archetypes():
        if q in a["name"].lower():
            results["archetypes"].append({"number": a["number"], "name": a["name"], "npc": a.get("npc", ""), "dimension": "lore"})
            if len(results["archetypes"]) >= limit:
                break

    for s in get_schools():
        if q in s["name"].lower() or q in s.get("guardian", "").lower():
            results["schools"].append({"id": s["id"], "name": s["name"], "guardian": s.get("guardian", ""), "dimension": "lore"})
            if len(results["schools"]) >= limit:
                break

    # Count total matches
    total = sum(len(v) for v in results.values())
    return {"query": query, "results": results, "total": total}


def lore_unveil(entity_a: str, entity_b: Optional[str] = None) -> dict:
    """Reveal storyline connections. If two entities given, find their connection.
    If one entity given, show all its connections to the story web."""
    q = entity_a.lower()

    connections = []

    # Find entity A
    char_a = None
    for cid, c in CHARACTERS.items():
        if q in c["name"].lower() or q in c["archetype"].lower():
            char_a = {"id": cid, "type": "character", **c}
            break
    if not char_a and q in METATRON["name"].lower():
        char_a = {"id": "metatron", "type": "meta_entity", **METATRON}
    if not char_a:
        for nid, n in NODES.items():
            if q in n["name"].lower():
                char_a = {"id": nid, "type": "node", **n}
                break

    if not char_a:
        return {"error": f"No storyline entity found matching '{entity_a}'", "connections": []}

    # Build connections
    if char_a["type"] in ("character", "meta_entity"):
        name = char_a["name"]
        # Connect to their node
        if char_a.get("node"):
            for nid, n in NODES.items():
                if n["name"] == char_a["node"]:
                    connections.append({
                        "from": name, "to": n["name"],
                        "relation": "guards",
                        "type": "character→node",
                    })
                    break
        # Connect to their episode
        if char_a.get("episode"):
            ep_num = char_a["episode"]
            if ep_num in EPISODES:
                connections.append({
                    "from": name, "to": f"Episode {ep_num}: {EPISODES[ep_num]['title']}",
                    "relation": "appears_in",
                    "type": "character→episode",
                })
        # Connect to their archetype
        if char_a.get("archetype"):
            for anum, a in ARCHETYPES.items():
                if a["name"] == char_a["archetype"]:
                    connections.append({
                        "from": name, "to": f"Archetype {anum}: {a['name']}",
                        "relation": "embodies",
                        "type": "character→archetype",
                    })
                    break

    elif char_a["type"] == "node":
        name = char_a["name"]
        # Connect all characters that guard this node
        for cid, c in CHARACTERS.items():
            if c.get("node") == name:
                connections.append({
                    "from": c["name"], "to": name,
                    "relation": "guards",
                    "type": "character→node",
                })
        # Connect episodes set here
        for enum, ep in EPISODES.items():
            if ep.get("node") == name:
                connections.append({
                    "from": f"Episode {enum}: {ep['title']}", "to": name,
                    "relation": "takes_place_at",
                    "type": "episode→node",
                })

    # Filter to specific target if given
    if entity_b:
        target = entity_b.lower()
        connections = [c for c in connections
                       if target in c["from"].lower() or target in c["to"].lower()]

    return {
        "entity": {"id": char_a.get("id", ""), "name": char_a.get("name", ""), "type": char_a["type"]},
        "connections": connections,
        "total": len(connections),
    }
