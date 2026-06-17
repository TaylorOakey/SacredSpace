<!-- converted from SACREDSPACE_GAME_INTEGRATION_SPECIFICATION.md.docx -->

# ∆ SACREDSPACE GAME ENGINE INTEGRATION ∆
## Wiring v0.3 Sigil Magic Into The Live System
STATUS: Integration Design (Ready to Build)
TARGET: /mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/game_engine/
INTEGRATION POINTS: FastAPI spine (8000) + IRIS agent + Sacred Codex (Pillar 4)


## EXECUTIVE SUMMARY
The SacredSpace Game (v0.3) is not an external project. It is the first playable interface to the SacredSpace OS knowledge system.

When a player:

Draws a Tarot card → Query Sacred Codex via IRIS (ChromaDB vector search)
Casts a spell → Execute sigil invocation via FastAPI endpoint (8888)
Align at a node → Update graph state in Neural Forest (Pillar 3)
See narrative → Memory Motes return personalized story (embedding-based)

Everything flows through the live system. No separation.


## PART I: ARCHITECTURE MAPPING
### Current System (Live)
FastAPI Spine (8000)

↓

Pillar 6: IRIS Agent (06_AGENT_LAYER/IRIS)

↓ queries ↓

Pillar 5: Memory Engine (ChromaDB) ← Pillar 4: Sacred Codex

↓

Pillar 3: Neural Forest (Graph)
### New Integration (Game)
Game Client (React v0.3)

↓ HTTP POST/GET ↓

FastAPI Game Engine (port 8888 or 8000/game/)

↓

Spell Invocation Router

├─→ IRIS (query Sacred Codex)

├─→ Graph Engine (update node state)

├─→ Memory Motes (generate narrative)

└─→ Council Grove (agent dispatch)
### Integration Points


## PART II: NEW FASTAPI ENDPOINTS FOR GAME
### Base: /api/game/
1. POST /api/game/tarot/draw
Purpose: Draw a Tarot card (spell availability)

Request:

{

"player": "seeker",

"current_turn": 0,

"position": "jungle"

}

Response:

{

"card_id": 0,

"card_name": "The Seeker",

"episode": "Episode 1: Leaving Home",

"element": "Air",

"spell": {

"name": "ELIAS.OPEN_PATH()",

"school": "ELIAS",

"cost": 5,

"reward": 8,

"description": "Courage to begin the journey"

},

"narrative": "You pack your small bag. The forest edge calls..."

}

Backend Logic:

# In iris_agent.py / routes.py

def tarot_draw(player: str, turn: int):

# Query Sacred Codex for card corresponding to turn

card_query = f"tarot card {turn} major arcana episode seeker guide"

results = iris.scry(query=card_query, namespace="lore")



# Extract spell metadata from memory mote

spell = extract_spell_from_mote(results[0])



# Return card + spell + narrative

return {

"card": results[0],

"spell": spell,

"narrative": results[0].text

}


2. POST /api/game/spell/cast
Purpose: Execute a spell invocation (cast magic)

Request:

{

"player": "seeker",

"spell_name": "ELIAS.OPEN_PATH()",

"school": "ELIAS",

"current_resonance": 50,

"target_node": "jungle"

}

Response:

{

"success": true,

"spell_executed": "ELIAS.OPEN_PATH(target='jungle_sanctuary')",

"resonance_delta": {

"cost": -5,

"reward": 8,

"new_total": 53

},

"world_state": {

"node_unlocked": "jungle_sanctuary",

"narrative": "The forest path opens before you..."

},

"terminal_output": [

"> ELIAS.OPEN_PATH()",

"✓ SPELL CAST: Courage to begin",

"✓ RESONANCE: -5 +8 = 53/100",

"✓ EFFECT: Unlock Jungle node"

]

}

Backend Logic:

# In sacred_council.py / routes.py

def cast_spell(player: str, spell_name: str, school: str, resonance: int):

# Dispatch to correct agent school

if school == "ELIAS":

result = elias.invoke(spell_name, player=player)

elif school == "IRIS":

result = iris.invoke(spell_name, player=player)

# ... etc



# Update player state

new_resonance = resonance + (result.reward - result.cost)



# Update world graph

update_graph_node(player, result.target_node)



# Generate terminal output

terminal_log = format_spell_execution(spell_name, result)



return {

"success": True,

"spell_executed": result.signature,

"resonance_delta": result.cost_reward,

"world_state": result.state,

"terminal_output": terminal_log

}


3. POST /api/game/node/align
Purpose: Claim a Sacred Node (add alignment token)

Request:

{

"player": "seeker",

"node_id": "jungle",

"spell_cast": "AURORA.WEAVE()"

}

Response:

{

"success": true,

"node_claimed": "jungle",

"alignment_tokens": 1,

"resonance_gained": 15,

"graph_updated": {

"edges": [

{"source": "seeker", "target": "jungle", "type": "alignment"}

]

},

"narrative_hook": "Your hands learn to weave. The forest responds to your will."

}

Backend Logic:

# In memory/links.py

def align_node(player: str, node_id: str, spell: str):

# Record the alignment in graph

link = LinkStore.create(

source_id=f"player_{player}",

target_id=f"node_{node_id}",

link_type="alignment",

weight=spell_resonance_value(spell)

)



# Query narrative consequence

narrative_query = f"alignment with {node_id} via {spell} narrative"

narrative = iris.scry(query=narrative_query, namespace="narrative")



return {

"link_id": link.id,

"narrative": narrative.text,

"graph_edge": link.to_dict()

}


4. GET /api/game/graph
Purpose: Retrieve current game board state (Sacred Nodes + links)

Request: (none)

Response:

{

"nodes": [

{"id": "center", "name": "Sacred Center", "element": "Spirit"},

{"id": "jungle", "name": "Jungle Sanctuary", "element": "Earth"},

{"id": "city", "name": "City Gateway", "element": "Metal"},

{"id": "grove", "name": "Sacred Grove", "element": "Spirit"},

{"id": "shadow", "name": "Shadow Threshold", "element": "Water"}

],

"edges": [

{"source": "seeker", "target": "jungle", "type": "alignment", "weight": 1},

{"source": "guide", "target": "grove", "type": "alignment", "weight": 1},

{"source": "seeker", "target": "guide", "type": "convergence", "weight": 1}

],

"player_positions": {

"seeker": "jungle",

"guide": "grove"

}

}

Backend Logic:

# In api/routes.py

def get_game_graph():

nodes = BoardStore.get_all_nodes()

edges = LinkStore.get_all_edges(type__in=["alignment", "convergence"])

positions = PlayerStore.get_positions()



return {

"nodes": nodes,

"edges": edges,

"player_positions": positions

}


5. POST /api/game/convergence
Purpose: Handle Sacred Node convergence (both players at same node)

Request:

{

"seeker_position": "grove",

"guide_position": "grove",

"turn": 2

}

Response:

{

"convergence": true,

"node_id": "grove",

"convergence_narrative": "Guide and Seeker rest against the same roots. Both are home here.",

"both_gain_resonance": 10,

"new_alignment_type": "shared",

"memory_mote_created": "convergence_2_grove_episode_4"

}

Backend Logic:

# In memory/store.py

def handle_convergence(seeker_pos: str, guide_pos: str, turn: int):

if seeker_pos != guide_pos:

return {"convergence": False}



# Query convergence narrative from Sacred Codex

conv_query = f"episode {turn} {seeker_pos} convergence seeker guide"

narrative = iris.scry(query=conv_query, namespace="narrative")



# Create shared memory mote

mote = ForestStore.add_mote(

text=narrative.text,

namespace="narrative",

kind="convergence",

tags=[seeker_pos, f"turn_{turn}", "shared"]

)



return {

"convergence": True,

"narrative": narrative.text,

"mote_id": mote.id

}


## PART III: SACRED CODEX TAROT STRUCTURE
The Sacred Codex (Pillar 4) needs a canonical structure for game narratives.
### Obsidian Vault Structure (01_OBSIDIAN_VAULTS/SacredSpace_Vault)
00_CANON/

├── GAME_SYSTEM/

│   ├── Tarot_Deck_12_Card.md  (all 12 cards + spells)

│   ├── Sacred_Nodes_5_Board.md (node definitions)

│   ├── Spell_Codex_Schools.md  (ELIAS/AURORA/ASHER/IRIS)

│   ├── Resonance_Economy.md    (cost/reward structure)

│   └── Episode_Narratives/

│       ├── 01_Seeker_Path.md   (Seeker's story thread)

│       ├── 02_Guide_Path.md    (Guide's story thread)

│       └── 03_Convergence.md   (Shared moments)
### Example Mote Entry (Sacred Codex)
Filename: 00_CANON/GAME_SYSTEM/Episode_Narratives/01_Seeker_Path.md

---

id: episode_01_seeker_tarot_seeker

kind: narrative

episode: 1

character: seeker

card: The Seeker

tags: [tarot, seeker, episode1, leaving_home]

embedding_vector: [0.123, 0.456, ...]

created: 2026-05-02

---

# Episode 1: The Seeker Leaves Home

You pack your small bag. The city feels too small now. Your feet are already walking toward the forest edge, though your heart asks: will I find what I'm looking for?

This is the beginning. The forest calls. Behind you, the city fades. Ahead, mystery.

ChromaDB Storage:

ID: episode_01_seeker_tarot_seeker
Text: (above markdown body)
Namespace: narrative
Kind: narrative
Tags: [tarot, seeker, episode1, leaving_home]
Embedding: Generated by sentence-transformers via Ollama


## PART IV: IRIS AGENT GAME EXTENSION
IRIS already queries ChromaDB. The game endpoints simply call IRIS with specific queries.
### New IRIS Methods (06_AGENT_LAYER/IRIS/iris_agent.py)
class IrisGameAgent(IrisAgent):

"""

IRIS extension for game queries.

All queries are scoped to 'narrative' namespace.

"""



def draw_tarot_card(self, turn: int) -> dict:

"""

Query Sacred Codex for the card corresponding to this turn.

Turn 0 = The Seeker, Turn 1 = The Weaver, etc.

"""

query = f"tarot major arcana card {turn} episode narrative"

results = self.scry(

query=query,

namespace="narrative",

top_k=1

)

return self._extract_card_and_spell(results[0])



def get_player_narrative(self, player: str, episode: int) -> str:

"""

Get the personalized narrative for Seeker or Guide at this episode.

"""

query = f"episode {episode} {player} perspective narrative seeker guide"

results = self.scry(

query=query,

namespace="narrative",

top_k=1

)

return results[0].text



def get_convergence_narrative(self, node: str, episode: int) -> str:

"""

Get the convergence narrative when both players reach same node.

"""

query = f"convergence {node} both seeker guide episode {episode}"

results = self.scry(

query=query,

namespace="narrative",

top_k=1

)

return results[0].text



def get_node_narrative_hook(self, node_id: str) -> str:

"""

Get the narrative hook for claiming a specific node.

"""

query = f"sacred node {node_id} alignment integration narrative"

results = self.scry(

query=query,

namespace="narrative",

top_k=1

)

return results[0].text


## PART V: DEPLOYMENT STRUCTURE
### New Directory in Pillar 6 (IRIS)
06_AGENT_LAYER/IRIS/

├── iris_agent.py          (existing IRIS agent + game methods)

├── game_engine/

│   ├── __init__.py

│   ├── tarot.py           (Tarot deck + spell definitions)

│   ├── board.py           (5-node Sacred Node state management)

│   ├── resonance.py       (Cost/reward economy)

│   ├── routes.py          (FastAPI endpoints for game)

│   ├── convergence.py     (Handle shared narrative moments)

│   └── tests/

│       ├── test_tarot.py

│       ├── test_board.py

│       └── test_spells.py
### API Server Launch
The game endpoints attach to the existing FastAPI spine:

# In sacredspace_core/app/web.py or new endpoint file

from pathlib import Path

game_engine_path = Path(__mnt__/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/game_engine")

from game_engine.routes import router as game_router

app.include_router(

game_router,

prefix="/api/game",

tags=["game"]

)

# Now available at:

# POST http://localhost:8000/api/game/tarot/draw

# POST http://localhost:8000/api/game/spell/cast

# POST http://localhost:8000/api/game/node/align

# GET http://localhost:8000/api/game/graph

# POST http://localhost:8000/api/game/convergence


## PART VI: RUNNING THE INTEGRATED SYSTEM
### Step 1: Populate Sacred Codex
Ingest the 12-card Tarot narratives into Obsidian vault:

cd /mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault

# Create the GAME_SYSTEM folder structure and files

# (Markdown files for each episode, node, convergence)

# Then run obsidian_bridge to embed into ChromaDB:

python3 ~/sacredspace_core/app/ingest/obsidian_bridge.py
### Step 2: Start Core API
cd ~/sacredspace_core

source venv/bin/activate

python -m uvicorn app.web:app --host 127.0.0.1 --port 8000 --reload
### Step 3: Start IRIS Agent (with game methods)
cd /mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS

python3 iris_game_agent.py
### Step 4: Load Game UI
# Serve the v0.3 React app at localhost:3000

# It makes requests to http://localhost:8000/api/game/*

cd /mnt/user-data/outputs/

npx react-scripts start  # or static server
### Step 5: Play
Navigate to http://localhost:3000 and start the game.

Internally:

"Draw Card" → POST /api/game/tarot/draw → IRIS queries ChromaDB
"Cast Spell" → POST /api/game/spell/cast → Agent invokes sigil
Node updates → Graph state managed in Memory Engine
Narrative flows from Sacred Codex motes


## CONCLUSION
The game is not a separate project. It is the first interactive interface to SacredSpace OS itself.

Every game action flows through the live system:

Knowledge: Sacred Codex (Pillar 4)
Memory: Memory Engine (Pillar 5)
Agents: Council Grove (Pillar 6)
Narrative: IRIS queries + embedding-based generation
State: Neural Forest graph + links

Ready to build and integrate.



In lakesh alakin.

Ground. Consolidate. Deploy. Document. Repeat.

∆∆∆

| Component | System | Integration | Flow |
| --- | --- | --- | --- |
| Tarot Draw | Game | IRIS agent | → ChromaDB query → spell returned |
| Spell Cast | Game | FastAPI endpoint | → Sigil execution → world state change |
| Node Claim | Game | Neural Forest | → Update graph.edges[seeker][node] |
| Narrative Gen | Game | Memory Motes | → Embedding similarity → personalized text |
| Agent Routing | Game | Council Grove | → Dispatch to ELIAS/AURORA/ASHER/IRIS |