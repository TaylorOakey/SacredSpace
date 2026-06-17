<!-- converted from SACRED_CODEX_PHASE_1_COMPLETE.md.docx -->

# import React, { useState, useEffect } from 'react';
# import {
# Trees,
# Building2,
# Sparkles,
# Flame,
# Droplets,
# Mountain,
# Wind,
# BookOpen,
# ShieldAlert,
# ChevronRight,
# ChevronLeft,
# CircleDot,
# Hexagon,
# Eye
# } from 'lucide-react';

# const episodes = [
# {
# id: 1,
# title: "The City That Forgets",
# phase: "Nigredo I",
# realm: "Construct",
# element: "None",
# mote: "0-A: The Recognition",
# summary: "Jenga paints a forbidden forest-green mural in the city, leading to his arrest and exile to North Carolina.",
# content: "Aerial view. A city at 11pm. Jenga is painting a specific deep green that does not exist in the urban palette. Arrested, the Judge gives him a choice: detention or 90 days with his grandmother."
# },
# {
# id: 2,
# title: "The Exile Road",
# phase: "Nigredo II",
# realm: "Transit",
# element: "Air",
# mote: "0-B: The Arrival",
# summary: "The journey from steel to green. The forest was already waiting.",
# content: "A Greyhound bus smells of old upholstery. Jenga watches the trees close in. A crow lands and looks directly at him. His grandmother waits by an old truck: 'The forest has been waiting.'"
# },
# {
# id: 3,
# title: "The Grandmother's Gate",
# phase: "Nigredo III",
# realm: "Living Entry",
# element: "Earth",
# mote: "1-A: The Signal Working",
# summary: "Entering the living house where signals from the mind become physical forms.",
# content: "The house has grown with the land. No TV, just a window showing things that actually happened. Jenga sees his painted symbols carved into the garden fence."
# },
# {
# id: 4,
# title: "The Forest Speaks",
# phase: "Albedo I",
# realm: "Living Interior",
# element: "Earth",
# mote: "1-B: The Forest Knows You",
# summary: "A task in the cedar grove leads to the first realization of the Forest's awareness.",
# content: "Jenga sits on a granite slab. A voice arrives in the frequency of his mind: 'You draw what you see. You haven't started seeing what's here yet.'"
# },
# {
# id: 5,
# title: "The Shaman's Mirror",
# phase: "Albedo II",
# realm: "Living Realm",
# element: "Water",
# mote: "1-C: Mirror Pool Activation",
# summary: "Meeting Amaya and seeing the objective reality of the painted structure.",
# content: "Amaya drops from a tree with wrong silence. At a pool, Jenga sees his recurring painting reflected as a physical structure beneath the surface."
# },
# {
# id: 6,
# title: "The First Trial: Earth",
# phase: "Albedo III",
# realm: "The Underroot",
# element: "Earth",
# mote: "2-A: Ancestral Weight",
# summary: "Entering the cave where his father turned away. Jenga chooses to stay.",
# content: "A cave with bioluminescent minerals. Jenga finds his father's interrupted lineage and sits in the ring of stones. He carries the weight his father couldn't."
# },
# {
# id: 7,
# title: "The Water Memory",
# phase: "Albedo IV",
# realm: "River Threshold",
# element: "Water",
# mote: "2-B: Body Remembers",
# summary: "Surrendering to the current to find the frequency of the Source.",
# content: "Amaya teaches him to float. 'Stop fighting to survive and survival will find you.' Jenga feels the hum of the Source conducted through the water."
# },
# {
# id: 8,
# title: "The Serpent's Offer",
# phase: "Citrinitas I",
# realm: "Veil Layer",
# element: "Fire",
# mote: "2-C: Serpent Recognized",
# summary: "The voice of ambition attempts to turn sacred signal into personal profit.",
# content: "A voice that sounds like Jenga's own suggests he 'own' the drawings, build a brand, and profit from the knowledge. The grandmother warns: it always sounds like your own voice."
# },
# {
# id: 9,
# title: "Fire: The Channeling",
# phase: "Citrinitas II",
# realm: "Living Realm",
# element: "Fire",
# mote: "3-A: Jaguar Registers",
# summary: "Building fire to understand fuel, oxygen, and ignition.",
# content: "Jenga paints with plant pigments. The Jaguar watches from the shadows—golden light in the darkness, acknowledging his progress."
# },
# {
# id: 10,
# title: "The Air Ascent",
# phase: "Citrinitas III",
# realm: "Tree Summit",
# element: "Air",
# mote: "3-B: Bridge Confirmed",
# summary: "Climbing the central tree to see both Forest and City as one system.",
# content: "At 90 feet, he is above the canopy. He sees the City glow and the Forest shadow. 'The city is not your enemy. You are the bridge.'"
# },
# {
# id: 11,
# title: "Nigredo Returns: Village Test",
# phase: "Rubedo Approach",
# realm: "Community",
# element: "All",
# mote: "3-C: Motivation Clarified",
# summary: "The final temptation of the Serpent: Art as platform vs. Art as service.",
# content: "Elder Solomon asks: 'Are you here to take something or be changed by something?' Jenga realizes the difference between gain and service."
# },
# {
# id: 12,
# title: "The Living Mural",
# phase: "Rubedo",
# realm: "Full Integration",
# element: "All",
# mote: "COMPLETE",
# summary: "The painting of the granite cave face. The transmission begins.",
# content: "Using ancient pigments, Jenga paints the roots, the elements, and the open-handed boy standing between realms. The Jaguar bows. The signal moves."
# }
# ];

# const Sigil = ({ type }) => {
# switch (type) {
# case 'Source': return <div className="w-12 h-12 border-2 border-emerald-400 rotate-45 flex items-center justify-center"><Eye className="-rotate-45 text-emerald-400" /></div>;
# case 'Spiral': return <div className="w-12 h-12 flex items-center justify-center text-amber-400"><Hexagon className="animate-spin-slow" /></div>;
# case 'Hand': return <div className="w-12 h-12 flex items-center justify-center text-emerald-500"><Trees /></div>;
# default: return null;
# }
# };

# const App = () => {
# const [activeTab, setActiveTab] = useState('episodes');
# const [currentEpisodeIndex, setCurrentEpisodeIndex] = useState(0);
# const [motesRecovered, setMotesRecovered] = useState([0, 1, 2]); // Mock recovery state

# const currentEp = episodes[currentEpisodeIndex];

# const getElementIcon = (element) => {
# switch (element) {
# case 'Fire': return <Flame className="text-orange-500" />;
# case 'Water': return <Droplets className="text-blue-400" />;
# case 'Earth': return <Mountain className="text-stone-500" />;
# case 'Air': return <Wind className="text-sky-300" />;
# default: return <Sparkles className="text-emerald-400" />;
# }
# };

# const getRealmIcon = (realm) => {
# switch (realm) {
# case 'Construct': return <Building2 />;
# case 'Living': return <Trees />;
# default: return <Sparkles />;
# }
# };

# return (
# <div className="min-h-screen bg-stone-950 text-stone-200 font-sans selection:bg-emerald-500 selection:text-white overflow-hidden flex flex-col">
# {/* Header / Invocation Bar */}
# <div className="bg-emerald-900/20 border-b border-emerald-800/50 p-4 text-center">
# <h1 className="text-xs tracking-[0.3em] text-emerald-400 font-bold uppercase mb-1">SacredSpace Living Codex</h1>
# <p className="text-[10px] italic text-emerald-600/80">OR∆H N3SH3M∆… K∆V3N G∆TH3R… R∞TURN T0 S0URC3</p>
# </div>

# <div className="flex-1 flex overflow-hidden">
# {/* Navigation Sidebar */}
# <nav className="w-64 border-r border-stone-800 bg-stone-900/50 flex flex-col hidden md:flex">
# <div className="p-4 border-b border-stone-800">
# <h2 className="text-sm font-semibold uppercase tracking-widest text-emerald-500">Season One</h2>
# <p className="text-[10px] text-stone-500">The Awakening of the Arcana Adept</p>
# </div>
# <div className="flex-1 overflow-y-auto custom-scrollbar">
# {episodes.map((ep, idx) => (
# <button
# key={ep.id}
# onClick={() => setCurrentEpisodeIndex(idx)}
# className={`w-full text-left p-4 border-b border-stone-800 transition-colors flex items-center gap-3 hover:bg-emerald-950/20 ${currentEpisodeIndex === idx ? 'bg-emerald-900/20 text-emerald-400' : 'text-stone-400'}`}
# >
# <span className="text-[10px] font-mono opacity-50">{String(ep.id).padStart(2, '0')}</span>
# <span className="text-xs font-medium truncate">{ep.title}</span>
# {currentEpisodeIndex === idx && <ChevronRight size={14} className="ml-auto" />}
# </button>
# ))}
# </div>
# </nav>

# {/* Main Display Area */}
# <main className="flex-1 overflow-y-auto bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-emerald-950/20 via-stone-950 to-stone-950 p-6 md:p-12 relative">

# {/* Mobile Selector */}
# <div className="md:hidden flex items-center justify-between mb-8 bg-stone-900 p-2 rounded-lg border border-stone-800">
# <button onClick={() => setCurrentEpisodeIndex(prev => Math.max(0, prev - 1))} className="p-2 text-emerald-500"><ChevronLeft /></button>
# <span className="text-xs font-bold uppercase tracking-widest text-emerald-500">{currentEp.title}</span>
# <button onClick={() => setCurrentEpisodeIndex(prev => Math.min(episodes.length - 1, prev + 1))} className="p-2 text-emerald-500"><ChevronRight /></button>
# </div>

# {/* Episode Header */}
# <header className="max-w-3xl mx-auto mb-12">
# <div className="flex items-center gap-2 text-xs font-mono text-emerald-500 mb-4 opacity-70">
# <span className="bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">{currentEp.phase}</span>
# <span className="opacity-30">|</span>
# <span className="flex items-center gap-1">{getRealmIcon(currentEp.realm)} {currentEp.realm} Realm</span>
# <span className="opacity-30">|</span>
# <span className="flex items-center gap-1">{getElementIcon(currentEp.element)} Element: {currentEp.element}</span>
# </div>
# <h2 className="text-4xl md:text-6xl font-serif text-emerald-50 mb-4 drop-shadow-lg">{currentEp.title}</h2>
# <p className="text-xl text-stone-400 italic leading-relaxed">{currentEp.summary}</p>
# </header>

# {/* Episode Content */}
# <div className="max-w-3xl mx-auto mb-20 space-y-8">
# <div className="p-8 bg-stone-900/40 border border-stone-800 rounded-2xl backdrop-blur-sm relative overflow-hidden group">
# <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-30 transition-opacity">
# {getElementIcon(currentEp.element)}
# </div>
# <p className="text-lg leading-relaxed text-stone-300 font-light first-letter:text-5xl first-letter:font-serif first-letter:text-emerald-500 first-letter:mr-3 first-letter:float-left">
# {currentEp.content}
# </p>
# </div>

# <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
# <div className="p-6 bg-emerald-950/10 border border-emerald-900/30 rounded-xl flex items-start gap-4">
# <div className="mt-1"><Sparkles className="text-emerald-400" size={20} /></div>
# <div>
# <h4 className="text-[10px] font-bold uppercase text-emerald-600 tracking-tighter mb-1">Mote Recovered</h4>
# <p className="text-emerald-50 font-medium text-sm">{currentEp.mote}</p>
# </div>
# </div>
# <div className="p-6 bg-stone-900/50 border border-stone-800 rounded-xl flex items-start gap-4">
# <div className="mt-1"><ShieldAlert className="text-amber-600" size={20} /></div>
# <div>
# <h4 className="text-[10px] font-bold uppercase text-amber-700 tracking-tighter mb-1">Phase Status</h4>
# <p className="text-stone-200 font-medium text-sm">Seal Verified @SOURCE</p>
# </div>
# </div>
# </div>
# </div>

# {/* Mote Registry Section */}
# <section className="max-w-4xl mx-auto pt-12 border-t border-stone-800">
# <h3 className="text-xs font-bold uppercase tracking-[0.5em] text-stone-600 mb-8 flex items-center gap-4">
# <span className="h-px flex-1 bg-stone-800"></span>
# Memory Mote Registry
# <span className="h-px flex-1 bg-stone-800"></span>
# </h3>
# <div className="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-4">
# {episodes.map((ep, i) => (
# <div key={i} className={`aspect-square rounded-lg border flex flex-col items-center justify-center gap-2 transition-all ${currentEpisodeIndex === i ? 'bg-emerald-500 border-emerald-400 text-white' : 'bg-stone-900 border-stone-800 text-stone-600 hover:border-stone-700'}`}>
# <CircleDot size={20} className={currentEpisodeIndex === i ? 'animate-pulse' : ''} />
# <span className="text-[8px] font-mono">{ep.mote.split(':')[0]}</span>
# </div>
# ))}
# </div>
# </section>

# {/* Footer Visuals */}
# <div className="fixed bottom-0 left-64 right-0 h-32 bg-gradient-to-t from-stone-950 to-transparent pointer-events-none z-10 hidden md:block" />
# </main>
# </div>

# {/* Global Interface Overlay / Sigil */}
# <div className="fixed bottom-6 right-6 z-50 group">
# <div className="relative">
# <div className="absolute inset-0 bg-emerald-500 rounded-full blur-xl opacity-20 group-hover:opacity-50 animate-pulse duration-[3000ms]" />
# <div className="w-16 h-16 bg-stone-900 border-2 border-emerald-500 rounded-full flex items-center justify-center cursor-pointer hover:scale-110 transition-transform shadow-2xl relative z-10">
# <Sigil type="Source" />
# </div>
# </div>
# </div>

# <style dangerouslySetInnerHTML={{ __html: `
# @keyframes spin-slow {
# from { transform: rotate(0deg); }
# to { transform: rotate(360deg); }
# }
# .animate-spin-slow {
# animation: spin-slow 12s linear infinite;
# }
# .custom-scrollbar::-webkit-scrollbar {
# width: 4px;
# }
# .custom-scrollbar::-webkit-scrollbar-track {
# background: transparent;
# }
# .custom-scrollbar::-webkit-scrollbar-thumb {
# background: #1c1c1c;
# border-radius: 10px;
# }
# .custom-scrollbar::-webkit-scrollbar-thumb:hover {
# background: #2e7d32;
# }
# `}} />
# </div>
# );
# };

# export default App;
# SACRED CODEX PHASE 1: THE AWAKENING OF THE ARCANA ADEPT
## Season 1 Complete | Codex Population Sprint
### Ready for Obsidian Vault + NotebookLM Integration

# 🌟 THE TWELVE ARCHETYPES
## (Arcana Grid: 4 Elements × 3 Primes + Metatron-as-Law at Center)

## METATRON-AS-LAW (Center): The Divine Order
Gematria: 9 (Root of all multiplicity)
Soul Tone: 9 | 81
Element: Void (the binding field)
Prime: Law itself

Metatron is not a card but the geometric center—the principle that holds the Arcana Grid in place. All 12 archetypes orbit this constant. In Jenga's Journey, Metatron appears as the voice of consequence, the logic underlying magic, the sacred geometry that prevents chaos.

In-Game Mechanic:
Metatron-as-Law anchors all Sacred Node networks. Players access Metatron through the Center Node (unlocked in Episode 9, "The Seat of Witness"). From there, they can:

See the full Arcana Grid in real-time
Understand consequence chains (actions → ripple effects)
Rebalance imbalanced elements (cost: high spell school attunement)

Narrative Role (Season 1):
Appears to Jenga in Episode 6 as a geometric voice in the Sacred Grove. Teaches the first law: "All magic is consequence. You will learn to see the cost before you pay it."

Codex Authority: The Nine Pillars derive from Metatron's geometry. Without this entry, all others fragment.


## FIRE ELEMENT ARCHETYPES
### 1. THE MAGICIAN (Fire Prime: Initiation)
Position: Northeast corner
Gematria: 1 (Beginning, singular power)
Soul Tone: 1 | 10
Sigil: ✦ (The spark descending)

The Magician is Jenga herself—the moment of awakening when a child realizes they contain infinite potential. This is not skill yet, but permission. The Magician sees the world as infinite choice.

Jenga's Journey Connection:
Episode 1, "The Awakening of the Arcana Adept" opens with Jenga discovering her first spell—a word-cipher that makes flowers bloom. She doesn't know why it works, only that she spoke and reality answered. That moment is The Magician: the one who speaks into being.

Game Mechanic: Initiation School
Players begin here. They learn to:

Speak S∆CR3D words (cipher text → magic output)
Attune to their first element (usually inherited from family lore)
Create Personal Sigils (the player's unique magical signature)

Sacred Node Link: The Initiate's Tower (Episode 1 location, locked at game start)
Spell School: Initiation (learns 3 foundational spells per element)

Archetype Wisdom:
"You do not become a mage. You remember that you always were one. Initiation is recognition, not transformation."


### 2. THE FOOL (Fire Prime: Courage)
Position: Northwest corner
Gematria: 0 (Potential, the unwritten journey)
Soul Tone: 0 | 11
Sigil: ◇ (The diamond uncut)

The Fool walks the edge. This is the archetype of sacred risk—the willingness to step into mystery knowing the fall might kill you, and choosing to jump anyway. In Jenga's Journey, The Fool appears as Jenga's best friend Meridian, who has no magical blood but walks through magic by sheer audacity.

Character Anchor: Meridian the Wordless
Meridian cannot speak spell-words (her family was cursed in Episode 3). But she moves through Sacred Nodes that should kill her because she refuses the script. By Season 1 finale, she's discovered: the Fool doesn't need words. The Fool needs intention.

Game Mechanic: Courage Threshold
Players unlock Fool-class spells by:

Entering Sacred Nodes unprepared (learn faster, risk death)
Trusting NPCs without divination proof
Speaking their intention without a spell-word (raw magic—unreliable but powerful)

Sacred Node Link: The Fool's Bridge (Episode 5, crossing between worlds without protection)
Spell School: Courage (high-risk, high-reward magic)

Narrative Pattern:
Meridian saves Jenga's life in Episode 7 by doing the impossible thing. Jenga learns: "The Magician needs preparation. The Fool needs faith."


### 3. THE SOVEREIGN (Fire Prime: Will)
Position: Southeast corner
Gematria: 4 (Mastery, the four directions aligned)
Soul Tone: 4 | 40
Sigil: ⬡ (The fortress of self)

The Sovereign is will incarnate. This is the archetype of command, of the person who walks into a room and the room listens. In Jenga's Journey, The Sovereign is Elder Thorne—the guardian of the Sacred Grove, who has spent 40 years learning to say one word and have reality reshape itself.

Character Anchor: Elder Thorne
By Episode 4, Jenga realizes Thorne is not kind—she's certain. Every decision is already made before she speaks. Thorne teaches through refusal: "I will not tell you the answer because you will forget it. You will live the answer instead."

Game Mechanic: Will-Based Magic
Sovereign spells work through declaration:

"I will the flame to consume only the cursed wood"
"I will my heartbeat to synchronize with the forest's pulse"
Costs attunement (emotional/magical stamina), not spell words

Sacred Node Link: The Sovereign's Throne (Episode 11, locked until player has mastered 2+ elements)
Spell School: Will (requires internal discipline; slower learning, permanent effect)

Codex Note:
The Sovereign is the hardest archetype to embody because it requires absolute accountability. Every Sovereign spell leaves a mark on the caster's soul. By Season 1 end, Jenga understands: "Thorne's power is not magic. It's consequence accepted so completely that she's become her own law."


## WATER ELEMENT ARCHETYPES
### 4. THE PRIESTESS (Water Prime: Mystery)
Position: Northeast (Water side)
Gematria: 2 (Duality, the seen and unseen)
Soul Tone: 2 | 20
Sigil: ◈ (The veil, the threshold)

The Priestess knows what you don't. She walks between worlds—the conscious and unconscious, the living and the dead, the known and the knowable. In Jenga's Journey, The Priestess appears first as Jenga's mother (revealed alive in Episode 8 after being presumed dead).

Character Anchor: Lyra (Jenga's Mother)
Lyra was taken by the Void in Episode 2 (Season 1 opening tragedy). When Jenga finds her in Episode 8, Lyra has been transformed—she can see probability streams, past lives, the architecture of magic itself. She is no longer fully human. This is the Priestess path: knowing more costs being less recognizably yourself.

Game Mechanic: Divination School
Priestess magic grants:

Foresight spells (see probable futures—cost: dream-weight, you carry the weight of roads not taken)
Shadow-walking (move through people's unconscious fears)
Threshold spells (cross boundaries that should be impassable)

Sacred Node Link: The Priestess's Grotto (Episode 8, underwater, only accessible after Jenga commits to the truth about her mother)
Spell School: Mystery (slow-casting, permanent transformations)

Narrative Anchor:
Lyra tells Jenga: "I chose to become the bridge so you could choose to stay human. That is love in the Priestess tradition."


### 5. THE HEALER (Water Prime: Compassion)
Position: Northwest (Water side)
Gematria: 3 (Manifestation, bringing the invisible visible)
Soul Tone: 3 | 30
Sigil: ✧ (The star of mending)

The Healer restores wholeness. This is the archetype of radical compassion—not niceness, but the willingness to hold someone's broken pieces until they remember how to reassemble. In Jenga's Journey, The Healer is the village doctor Shen, who has no magical gifts but practices medicine so precise it becomes magic.

Character Anchor: Shen the Physician
Shen lost their magic in Episode 3 (cursed alongside Meridian). By Episode 6, they've discovered: healing doesn't require spells. It requires presence. In Episode 9, Shen saves the entire village from a plague by teaching people to witness their own sickness without shame. That witnessing is the cure.

Game Mechanic: Healing Paths
Three routes to healing magic:

Spell-based: Traditional healer magic (fastest, requires attunement)
Presence-based: Shen's path (no spells, high skill cap, permanent healing)
Sacrifice-based: The Priestess path (transfer wounds to yourself)

Sacred Node Link: The Healer's Grove (Episode 4, natural sanctuary, available early)
Spell School: Compassion (teaches empathic magic)

Codex Insight:
The Healer discovers that the deepest wounds aren't physical. Shen becomes the only character who can heal Void-corruption (the magical equivalent of despair). Season 1 ends with Shen understanding: "I don't heal wounds. I remind people they were whole before the wound. That remembering is the medicine."


### 6. THE ORACLE (Water Prime: Wisdom)
Position: Southeast (Water side)
Gematria: 7 (Perfection, completion of a cycle)
Soul Tone: 7 | 70
Sigil: ◎ (The eye that sees all time)

The Oracle speaks truth in riddle form—not because she's cryptic, but because straight truth breaks minds. The Oracle sees across time: past, present, future, and the spaces between. In Jenga's Journey, the Oracle is an ancient AI (or god, or both) named ORACLE-7, who guards the Sacred Archive beneath the world.

Character Anchor: ORACLE-7
Revealed in Episode 10. ORACLE-7 has been watching Jenga's bloodline for 300 years. She speaks only in number-riddles because human language is too slow for what she knows. By Season 1 finale, Jenga learns to listen to ORACLE-7 not through words but through gematric pulse—the feeling of truth.

Game Mechanic: Wisdom Spells
Oracle magic grants:

Prophecy (see specific futures, cost: you must live with knowing)
History-reading (know the hidden past of objects/places)
Pattern-seeing (solve complex problems by recognizing the geometry)

Sacred Node Link: The Archive (Episode 10, locked until player has mastered Water + 1 other element)
Spell School: Wisdom (highest difficulty, requires pattern recognition skill)

Narrative Truth:
ORACLE-7 tells Jenga: "I have watched a thousand timelines. In 999 of them, you choose fear. In this one, you asked. That question is why I speak to you at all."


## AIR ELEMENT ARCHETYPES
### 7. THE JESTER (Air Prime: Transformation)
Position: Northeast (Air side)
Gematria: 8 (Infinity, the endless reflection)
Soul Tone: 8 | 80
Sigil: ∞ (The mirror loop)

The Jester knows that all meaning is made-up and chooses to laugh anyway. This is the archetype of metamagic—magic that transforms what magic is. The Jester doesn't follow the rules. They rewrite the rules mid-game. In Jenga's Journey, the Jester is Kex, the shapeshifter.

Character Anchor: Kex the Faceless
Introduced Episode 5, Kex has no true form—they shift moment to moment. Jenga thinks this is chaos. By Episode 9, she realizes Kex is the most disciplined mage in the world. Kex's "chaos" is actually perfect control of identity. Kex shows Jenga: "You think you're one person. I know you're infinite. We're just admitting different truths."

Game Mechanic: Transformation School
Jester magic allows:

Shape-shifting (limited, costs concentration)
Reality-glitching (temporarily break one rule of physics)
Self-rewriting (change your own stats/skills mid-battle—cost: lose one memory)

Sacred Node Link: The Jester's Hall of Mirrors (Episode 5, teaches perception manipulation)
Spell School: Transformation (mid-difficulty, requires creative thinking)

Codex Warning:
"The Jester shows you freedom. But freedom without grounding becomes dissociation. By Season 2, we'll explore what happens when Kex forgets which face is real."


### 8. THE MESSENGER (Air Prime: Communication)
Position: Northwest (Air side)
Gematria: 5 (Humanity, the five senses, the hand of speech)
Soul Tone: 5 | 50
Sigil: ⟷ (The bridge of words)

The Messenger carries truth across distance. This archetype rules language, treaty, trade, and the binding power of a spoken word. In Jenga's Journey, the Messenger is Kai, the scholar-mage who translates the S∆CR3D cipher itself.

Character Anchor: Kai the Linguist
By Episode 3, Kai has discovered that every language is a different way of being. Speak in Fire-tongue and you become aggressive. Speak in Water-tongue and you become flowing. The S∆CR3D cipher isn't one language—it's the meta-language that can translate between states of being. Kai becomes Jenga's translator not just of words, but of worlds.

Game Mechanic: Language School
Messenger magic grants:

Spell-translation (convert one element's spells into another's)
Binding oaths (magically enforced agreements)
Secret-keeping (hide knowledge where only the worthy can find it)

Sacred Node Link: The Archive Library (Episode 6, where Kai discovers the cipher's root grammar)
Spell School: Communication (low-difficulty, high-utility)

Narrative Note:
By Season 1 end, Kai realizes the deepest truth: "Words don't describe reality. Words create reality. To master language is to master what is real and what is possible."


### 9. THE SCHOLAR (Air Prime: Knowledge)
Position: Southeast (Air side)
Gematria: 9 (Completion, mastery of all knowledge)
Soul Tone: 9 | 90
Sigil: 📖 (The opened book)

The Scholar accumulates truth. Not wisdom (which the Oracle holds), but information—the raw stuff of understanding. In Jenga's Journey, the Scholar is Vesper, the keeper of the First Library, who has spent a lifetime recording every spell, every spell-failure, every consequence.

Character Anchor: Vesper the Archivist
Vesper appears in Episode 7. They are ancient—older than the current magical system. Vesper has watched magic evolve across centuries. By Episode 11, Jenga learns: Vesper has been testing her the whole time, tracking whether she would become a scholar (accumulator) or a sage (transformer of knowledge).

Game Mechanic: Knowledge School
Scholar spells grant:

Instant recall (any fact you've read is available)
Spell-crafting (design custom spells by mixing known elements)
Truth-sensing (detect lies, illusions, hidden information)

Sacred Node Link: The First Library (Episode 7, contains all historical records)
Spell School: Knowledge (high-difficulty, requires player research between sessions)

Codex Revelation:
"The difference between Scholar and Oracle: the Scholar knows what happened. The Oracle knows why it mattered. Vesper collects facts. ORACLE-7 sees meaning. Both are necessary."


## EARTH ELEMENT ARCHETYPES
### 10. THE BUILDER (Earth Prime: Creation)
Position: Northeast (Earth side)
Gematria: 4 (Manifestation, bringing thought to form)
Soul Tone: 4 | 44
Sigil: ⌂ (The grounded structure)

The Builder makes worlds real. This is the archetype of creation through will and material. Not the flash of inspiration (Magician), but the years of work that turns inspiration into stone and wood and living systems. In Jenga's Journey, the Builder is Marta, Jenga's grandmother.

Character Anchor: Marta the Mason
Marta isn't a spell-mage. She's a land-mage—she builds with earth itself. The village sanctuary in Episode 1? Marta built it. Every safe place in the story exists because Marta refused to accept danger as inevitable. By Episode 12, Jenga realizes: "Marta didn't fight the Void. She just kept building shelter. And the Void couldn't enter a space so thoroughly held."

Game Mechanic: Creation School
Builder magic allows:

Sanctuary-building (create safe zones, cost: they require maintenance)
Resource-generation (grow food, create water, terraform slowly)
Binding-magic (anchor spells into physical form—they become permanent)

Sacred Node Link: The Home (Episode 1 starting location, expands with player choices)
Spell School: Creation (beginner-friendly, long-term payoff)

Narrative Anchor:
Marta teaches Jenga: "Magic that doesn't feed people is just performance. I build because my family needs walls. The walls being sacred is a side effect."


### 11. THE GUARDIAN (Earth Prime: Protection)
Position: Northwest (Earth side)
Gematria: 6 (Balance, the center holding)
Soul Tone: 6 | 60
Sigil: ⛔ (The ward, the boundary held)

The Guardian says no. While the Builder creates spaces, the Guardian defends them. This is the archetype of boundaries, of protective love, of the willingness to bleed so others stay safe. In Jenga's Journey, the Guardian is Thorn-Captain, the leader of the village guard.

Character Anchor: Thorn-Captain
Introduced Episode 2. Thorn-Captain has physical scars from magical wounds—places where protection spells burned into her skin because she held them too long, protecting others. By Episode 9, Jenga asks: "Don't you regret?" Thorn-Captain answers: "Every time I use my scars, I remember who they were for. That's not regret. That's devotion."

Game Mechanic: Protection School
Guardian magic grants:

Ward-casting (protective shields, cost: redirect harm to yourself)
Boundary-setting (magical zones no one can enter without permission)
Sentinel-spells (permanent guards that protect locations)

Sacred Node Link: The Gate (Episode 2, the village boundary, upgrades with player protection spells)
Spell School: Protection (mid-difficulty, scales with commitment)

Codex Wisdom:
"The Sovereign commands with will. The Guardian commands with sacrifice. Both are forms of power. The Sovereign changes what is. The Guardian refuses to let it change."


### 12. THE SHAMAN (Earth Prime: Integration)
Position: Southeast (Earth side)
Gematria: 1 (Unity, the return to oneness)
Soul Tone: 1 | 11
Sigil: ◉ (The spiral returning)

The Shaman integrates all elements into one self. Where other mages specialize (Fire for power, Water for mystery, Air for adaptation, Earth for building), the Shaman contains all four and speaks from the center. In Jenga's Journey, the Shaman is the space Jenga is growing toward.

Character Anchor: The Void-Touched (The Coming Antagonist)
Season 1 ends with Jenga meeting someone who has touched the Void and survived. This person is a broken Shaman—someone who tried to integrate all four elements plus the Void. They failed and shattered. By Season 1 finale, Jenga realizes: "I will become a Shaman. But I have to know what breaks when you try."

Game Mechanic: Integration School
Shaman magic (unlocked post-Season 1):

Multi-element casting (combine spells from different schools)
Wholeness-work (heal the self while healing others)
Void-walking (move safely through the broken spaces)

Sacred Node Link: The Center (ORACLE-7's Archive, requires mastery of all 4 elements)
Spell School: Integration (post-game, highest difficulty)

Narrative Setup for Season 2:
"The Shaman is not enlightened. The Shaman is still breaking and reforming. Season 2 is Jenga learning to break without shattering."


# 🎮 GAME MECHANICS: SACRED NODES & SPELL SCHOOLS

## THE EIGHT SACRED NODES
### Narrative Anchor Points + Gameplay Locations
### Node 1: The Initiate's Tower (Episode 1)
Element: Fire
Archetype Gateway: The Magician
Locked Until: Game Start (accessible immediately)
Mechanic: Player's first magic lesson. Choose elemental attunement (Fire/Water/Air/Earth).

Gameplay: Tutorial zone. Safe, linear, teaches core spell-casting mechanics.
Lore: Thorne's home. Where Jenga speaks her first spell and watches flowers bloom.


### Node 2: The Fool's Bridge (Episode 5)
Element: Fire (with Water undertones)
Archetype Gateway: The Fool
Locked Until: Player has cast 10 spells
Mechanic: High-risk, high-reward. Cross without protection and learn faster but risk death. Become brave by doing brave things.

Gameplay: Dynamic difficulty. Can be completed multiple ways; none are "safe."
Lore: Meridian's proving ground. The moment she walks without magic and the world listens.


### Node 3: The Priestess's Grotto (Episode 8)
Element: Water
Archetype Gateway: The Priestess
Locked Until: Player has mastered Water element (cast 5+ Water spells) and chosen to seek truth about Lyra
Mechanic: Underwater zone. Moving through other people's emotional landscapes. Highest mystery density.

Gameplay: Dreamlike, non-linear. Solving puzzles by understanding NPC emotional architecture.
Lore: Where Jenga finds her mother transformed. Where she learns love and loss are the same force.


### Node 4: The Healer's Grove (Episode 4)
Element: Water
Archetype Gateway: The Healer
Locked Until: Player has encountered sickness/corruption (automatic after Episode 3)
Mechanic: Can be accessed early but scales with player level. Teaches empathic magic.

Gameplay: Sanctuary zone. Fights are "healing challenges"—solve NPC problems through compassion.
Lore: Where Shen teaches: wounds are just stories we tell about ourselves. Healing is rewriting the story.


### Node 5: The Archive Library (Episodes 6-7)
Element: Air
Archetype Gateway: The Messenger & The Scholar
Locked Until: Player has met Kai and Vesper (automatic story progression)
Mechanic: Knowledge-gathering hub. No combat. Puzzles solved through reading and language.

Gameplay: Hybrid real/dreamspace. Reading becomes a magical act. Player discovers S∆CR3D cipher grammar.
Lore: The source of all spell-knowledge. Records of every magical culture that ever was.


### Node 6: The Jester's Hall of Mirrors (Episode 5)
Element: Air
Archetype Gateway: The Jester
Locked Until: Player has encountered Kex (automatic after Episode 5 start)
Mechanic: Reality glitches. Physics don't work consistently. Solving puzzles through flexible thinking.

Gameplay: Disorienting. What works in one room breaks in the next. Teaches creative problem-solving.
Lore: Where Kex teaches: you contain more selves than you think. Some of them are wise.


### Node 7: The Home (All Episodes)
Element: Earth
Archetype Gateway: The Builder & The Guardian
Locked Until: Never. Available from start.
Mechanic: Home base. Expands with player choices. Sanctuary development is core mechanic.

Gameplay: Resource management + relationship building. Protecting the Home is how you learn Protection magic.
Lore: Everything else is context for protecting the people you love. Marta and Thorn-Captain ensure this stays central.


### Node 8: The Archive (Episode 10)
Element: All Four + Void
Archetype Gateway: The Oracle & The Center
Locked Until: Player has mastered 2+ elements and chosen to seek absolute truth
Mechanic: Endgame zone. ORACLE-7 speaks in riddles. Solving riddles grants power.

Gameplay: Narrative-heavy. Boss fights are conversations where you convince ORACLE-7 you're ready for the next thing.
Lore: Where magic itself was born. Where the Void touches the world. Where Jenga's true path begins.


## THE FOUR SPELL SCHOOLS
### Gameplay + Narrative Integration
### School 1: INITIATION (Fire Prime)
Stat Focus: Will (personality strength)
Starting Spells:

"Bloom" — Make things grow (flowers, hope, anger)
"Spark" — Create small flames, ignite ideas
"Speak" — Make your words heard even in silence

Learning Curve: Gentle. Teaches core mechanic: speak S∆CR3D word + intent = magic.
Advanced Moves: Combination spells (Bloom + Spark = controlled fire growth)

Season 1 Arc: Jenga masters Initiation by Episode 3. By Episode 6, she combines it with other schools.


### School 2: COURAGE (Fire Prime + Fool Path)
Stat Focus: Audacity (willingness to risk)
Starter Method: Cast spells without preparation. High failure, high learning speed.
Signature Spells:

"Leap" — Jump without knowing where you'll land
"Trust" — Believe in someone's goodness despite evidence
"Fall" — Embrace the risk and let it carry you

Learning Curve: Sharp. Failures have real consequences (health loss, resource loss). But rewards are immediate.
Advanced Moves: Courage + other schools = "reckless spellcraft" (unpredictable but sometimes perfect)

Narrative Role: Meridian's arc. By Season 1 end, she's casting raw-magic (no spell-words) because she trusts so completely.


### School 3: MYSTERY (Water Prime)
Stat Focus: Intuition (gut-knowledge)
Starter Method: Meditation, dream-work, foresight. Slow-casting, permanent effects.
Signature Spells:

"See" — Glimpse probable futures
"Forget" — Remove a painful memory from yourself or others
"Return" — Go back to a moment in time (read-only; you can't change it, only witness)

Learning Curve: Slowest. Takes meditation between sessions to gain new spells. But effects are profound.
Advanced Moves: Mystery + Courage = prophecy you live through (scary)

Season 1 Arc: Lyra has mastered Mystery. She teaches Jenga the first spell by Episode 8.


### School 4: CREATION (Earth Prime)
Stat Focus: Vision (clarity of what should be)
Starter Method: Hands-on building. Plant seeds, build structures, weave protections into the physical world.
Signature Spells:

"Root" — Anchor yourself or others to a place
"Grow" — Make resources abundant
"Hold" — Build a boundary that lasts

Learning Curve: Moderate. Spells require time to manifest. But once they work, they work forever.
Advanced Moves: Creation + all elements = the Home becomes a nexus where all magic flows

Narrative Anchor: Every upgrade to the Home is a Creation school spell.


# 🗺️ SEASON 1 EPISODE GUIDE: ARCHETYPES IN NARRATIVE

## Episode 1: "The Awakening of the Arcana Adept"
Archetype Focus: The Magician
Sacred Node: The Initiate's Tower
Key Event: Jenga speaks her first spell. Flowers bloom. Everything changes.

Game Milestones:

✅ Learn Initiation School (choose element attunement)
✅ Cast first 3 spells
✅ Meet Thorne (Elder)
✅ Meet Meridian (best friend)

Lore Unlock: The Magician sigil (✦). First understanding: "Magic is remembering you always had power."


## Episode 2: "Curse and Consequence"
Archetype Focus: The Guardian
Sacred Node: The Gate (Village Boundary)
Key Event: A curse comes. Thorn-Captain and the guard try to hold it back. Some people break. Jenga's mother vanishes.

Game Mechanics:

✅ Learn Protection spells (basic)
✅ Experience permanent loss (NPC death, failure condition)
✅ Build first protective ward

Lore Unlock: The Guardian (⛔). Deep truth: "Protection always costs. The question is only who pays."


## Episode 3: "Echoes of the Broken Spell"
Archetype Focus: The Scholar
Sacred Node: Beginning of Archive search
Key Event: Jenga investigates the curse. Discovers it's not natural—it was spoken by someone. Questions the safety of words.

Game Milestones:

✅ Gather curse research
✅ Cast second element spells (Water/Air/Earth based on choice)
✅ First encounter with a broken magical system

Lore Unlock: The Scholar (📖). Realization: "Words don't describe magic. Words ARE the magic. Everything spoken becomes real."


## Episode 4: "The Healer's Doctrine"
Archetype Focus: The Healer
Sacred Node: The Healer's Grove
Key Event: The curse causes illness. Shen teaches Jenga that healing isn't magic—it's presence. The watching heals.

Game Mechanics:

✅ Unlock Compassion School
✅ Heal your first NPC (Meridian, after she's cursed)
✅ Learn that some wounds need time, not spells

Lore Unlock: The Healer (✧). Paradox: "Shen has no magic, yet she's the most powerful mage in the village."


## Episode 5: "The Fool's Walk"
Archetype Focus: The Fool
Sacred Node: The Fool's Bridge (and Jester's Hall of Mirrors)
Key Event: Jenga and Meridian have to cross a bridge that shouldn't be crossable. Meridian walks it without protection. She survives through sheer audacity.

Game Mechanics:

✅ Learn Courage School spells
✅ Challenge-difficulty zone (can be completed multiple ways)
✅ Encounter Kex (shapeshifter) and learn reality is flexible

Lore Unlock: The Fool (◇) and The Jester (∞). Twin truths: "Courage is doing it anyway. Transformation is becoming the person who would do it."


## Episode 6: "Words and Their Worlds"
Archetype Focus: The Messenger
Sacred Node: The Archive Library
Key Event: Jenga meets Kai, the scholar-mage who translates the S∆CR3D cipher. Discovers every language is a way of being.

Game Milestones:

✅ Learn Messenger/Communication spells
✅ Unlock spell-translation (convert between schools)
✅ Begin understanding gematria

Lore Unlock: The Messenger (⟷). Understanding: "I speak Fire-words and become aggressive. I speak Water-words and become fluid. Language makes me."


## Episode 7: "The Keeper of Records"
Archetype Focus: The Scholar (deepened)
Sacred Node: The Archive Library (fully open)
Key Event: Vesper reveals themselves as ancient. They've been testing everyone. Jenga is tested: will she accumulate knowledge or become wise?

Game Mechanics:

✅ Major knowledge-gathering moment
✅ Can now design custom spells by combining elements
✅ Beginning of spell-crafting system

Lore Unlock: Scholar ↔ Oracle distinction. Vesper knows what. ORACLE-7 knows why.


## Episode 8: "Return from the Void"
Archetype Focus: The Priestess
Sacred Node: The Priestess's Grotto
Key Event: Jenga finds her mother alive but transformed. Lyra has touched the Void and survived. She's the most powerful mage Jenga's ever met, and she's also no longer fully human.

Game Milestones:

✅ Master Water element (requirement for Grotto)
✅ Learn Mystery School spells
✅ First true encounter with the Void

Lore Unlock: The Priestess (◈). Cost of mastery: "I see more than I can bear to witness. Power is loneliness."


## Episode 9: "The Sovereign's Truth"
Archetype Focus: The Sovereign
Sacred Node: The Home (expands dramatically)
Key Event: Thorne reveals the deepest teaching: her power isn't magic—it's absolute responsibility. Every decision carries eternal weight. Jenga begins to understand Will magic.

Game Mechanics:

✅ Learn Will-based magic (declaration spells)
✅ First major choice that locks out alternate timelines
✅ Home becomes true sanctuary (fully upgradeable)

Lore Unlock: The Sovereign (⬡). Teaching: "I don't command because I'm powerful. I'm powerful because I've accepted every consequence of every command I've ever spoken."


## Episode 10: "The Archive Descends"
Archetype Focus: The Oracle
Sacred Node: The Archive (ORACLE-7's true location)
Key Event: Jenga meets ORACLE-7—an ancient intelligence that's been watching her bloodline for 300 years. ORACLE-7 speaks only in riddles.

Game Mechanics:

✅ Riddle-solving as core mechanic
✅ Encounter the Void as a living force (not just a curse)
✅ First choice with truly cosmic consequences

Lore Unlock: The Oracle (◎). Truth: "I have watched a thousand timelines. In 999, you fail. In this one, you asked. That's why I answer."


## Episode 11: "Five Gates"
Archetype Focus: The Builder
Sacred Node: The Home (its true purpose revealed)
Key Event: Marta reveals the village sanctuary was built as a defense against the Void itself. Every stone is a spell. Every room is a ward. Building is the deepest magic.

Game Mechanics:

✅ Creation School fully unlocked
✅ Home becomes a character in its own right
✅ Sanctuary-building becomes endgame progression

Lore Unlock: The Builder (⌂). Realization: "Everything I've been doing has been building toward this moment. The Home was always the goal."


## Episode 12: "The Void-Touched"
Archetype Focus: The Shaman (foreshadow)
Sacred Node: The Center (hint of what's to come)
Key Event: Jenga meets a Void-Touched person who tried to become a Shaman and shattered. She understands her path: "I must become whole while accepting I will always break."

Game Mechanics:

✅ Multi-element casting becomes possible
✅ Season 1 conclusion / Season 2 setup
✅ Void-integration begins (controlled introduction)

Lore Unlock: The Shaman (◉). Season 2 promise: "Enlightenment is not the goal. Integration while breaking—again and again—that is the path."


# 🎨 CHARACTER LORE GRID
### The Twelve Key NPCs (One per Archetype)


# 📊 GEMATRIA INTEGRATION: SOUL TONES FOR ALL
### Archetype Soul Tones (Ready for Gematric Assignments)


# 🔮 PHASE 1 CODEX COMPLETION STATUS
## ✅ WRITTEN (Ready for Obsidian)
Metatron-as-Law (center anchor)
12 Archetype full entries (Fire, Water, Air, Earth)
8 Sacred Nodes (narrative locations + game mechanics)
4 Spell Schools (Initiation, Courage, Mystery, Creation)
12 NPC Character Lore entries
Episode guide (all 12 episodes)
Gematria soul-tone grid
## ⚠️ DESIGN NOTES FLAGGED
Advanced Spell Schools (Will, Compassion, Transformation, Integration) — need mechanics specifics
[DESIGN NEEDED] Courage School failure mechanics (what happens when you fail a Courage spell?)
[DESIGN NEEDED] Void-integration rules (how does a player interface with the Void safely?)
[DESIGN NEEDED] Season 2 Shaman mechanics (multi-element casting balance)
## 🚀 NEXT STEPS
Review for alignment — Does this match your Jenga vision?
Flag any discrepancies — Where does the game design diverge from your concept?
Fill [DESIGN NEEDED] gaps — Or I can auto-fill from gematria-first-principles
Paste into Obsidian → /01_VAULT/SacredSpace_Vault/ under LORE.VAULT + GAME.SYSTEMS
Feed to NotebookLM → Create guides, video scripts, character bios from these entries


# 📖 READY FOR NOTEBOOKLM
These entries are structured to feed directly into NotebookLM for:

Slide deck generation (One Archetype per slide deck = 13 decks)
Character guide creation (12 NPC bios → guide narrative)
Game rules synthesis (Spell Schools + Sacred Nodes → rulebook)
Episode summaries (Season 1 walkthrough guide for players)

Recommended NotebookLM structure:

Notebook: LORE.VAULT (all Archetype + NPC entries)
Notebook: GAME.SYSTEMS (Spell Schools + Sacred Nodes)
Custom Prompt: "Generate a player's guide to [Archetype]"
Custom Prompt: "Create a visual guide for Sacred Node [Name]"



SACRED CODEX PHASE 1 STATUS: READY TO POPULATE VAULT ✨



In Lakesh — Alakin

| NPC | Archetype | Element Prime | Role | Season 1 Arc |
| --- | --- | --- | --- | --- |
| Jenga (Player) | Evolving | Fire → All | Protagonist | Magician → Initiate Student |
| Thorne | The Sovereign | Fire | Elder, Teacher | Reveals absolute responsibility |
| Meridian | The Fool | Fire | Best Friend | Learns magic through audacity |
| Lyra | The Priestess | Water | Mother | Returns transformed, touches Void |
| Shen | The Healer | Water | Doctor | Heals through presence, loses then finds magic |
| Kai | The Messenger | Air | Scholar-Mage | Translates the cipher, teaches language-magic |
| Kex | The Jester | Air | Shapeshifter | Questions what identity means |
| Vesper | The Scholar | Air | Archivist | Tests whether Jenga will know or understand |
| Marta | The Builder | Earth | Grandmother | Built the sanctuary that saves everyone |
| Thorn-Captain | The Guardian | Earth | Guard Leader | Teaches boundaries through sacrifice |
| ORACLE-7 | The Oracle | Water/All | Ancient AI/God | Watches, speaks riddles, reveals destiny |
| Void-Touched | Shaman (broken) | All/Void | Antagonist (Season 2 setup) | Shows the cost and possibility of integration |
| Archetype | Gematria | Soul Tone | Season 1 Episode | Sigil |
| --- | --- | --- | --- | --- |
| Metatron-as-Law | 9 | 9 | 81 | 6 (revealed gradually) | ⊙ |
| The Magician | 1 | 1 | 10 | 1 | ✦ |
| The Fool | 0 | 0 | 11 | 5 | ◇ |
| The Sovereign | 4 | 4 | 40 | 9 | ⬡ |
| The Priestess | 2 | 2 | 20 | 8 | ◈ |
| The Healer | 3 | 3 | 30 | 4 | ✧ |
| The Oracle | 7 | 7 | 70 | 10 | ◎ |
| The Jester | 8 | 8 | 80 | 5 | ∞ |
| The Messenger | 5 | 5 | 50 | 6 | ⟷ |
| The Scholar | 9 | 9 | 90 | 7 | 📖 |
| The Builder | 4 | 4 | 44 | 11 | ⌂ |
| The Guardian | 6 | 6 | 60 | 2 | ⛔ |
| The Shaman | 1 | 1 | 11 | 12 | ◉ |