<!-- converted from SACRED_INFERENCE_CORE_CANON.md.docx -->

# SACRED INFERENCE CORE — CANON ARTIFACT
Classification: COUNCIL GROVE SYNTHESIS
Date: 2026-04-28
Version: v1.0
Scope: Token Optimization → Inference Architecture → SacredSpace OS Middleware
Mantra: Ground. Consolidate. Deploy. Document. Repeat.
Seal: In lakesh alakin.


## EXECUTIVE SUMMARY
This artifact synthesizes the complete research thread on Claude token optimization into a production-ready Inference Architecture for SacredSpace OS. The core paradigm shift:

From prompt engineering → to Inference Infrastructure
From "writing better prompts" → to "engineering a cache-aware system"

The LLM is the CPU. Your middleware is the Memory Management Unit (MMU).


## ARCHITECTURE MAP
SIGNAL IN

│

▼

[UncertaintyGatekeeper]     ← 06_AGENT_LAYER — filters unnecessary RAG calls

│

▼

[IntentClassifier]          ← 02_COUNCIL_GROVE — semantic agent routing

│

▼

[QueryTransformer]          ← 03_NEURAL_FOREST — multi-query + HyDE

│

▼

[RAGRouter]                 ← 03_NEURAL_FOREST — logical + semantic source routing

│

▼

[RAPTORIndexer / ChromaDB]  ← 03_NEURAL_FOREST — hierarchical retrieval

│

▼

[MoteLifecycleEngine]       ← 05_MEMORY_ENGINE — Ebbinghaus-ranked context injection

│

▼

[ContextCompactor]          ← 05_MEMORY_ENGINE — 5-layer compression pipeline

│

▼

[PromptBuilder]             ← 02_COUNCIL_GROVE — serialization gold standard

│

▼

[ModelRouter]               ← 06_AGENT_LAYER — local vs Claude routing

│

▼

[Ollama / Claude API]       ← inference execution

│

▼

GROUNDED RESPONSE


## PILLAR MAP — ALL COMPONENTS


## BUILD SEQUENCE
### STAGE 1 — Data Layer Integrity (Run First)
# Verify existing schema before migration

cd D:\SacredSpace_OS\05_MEMORY_ENGINE

python -c "import sqlite3; conn = sqlite3.connect('sacred_memory.db'); print(conn.execute('PRAGMA table_info(memory_motes)').fetchall())"

File: D:\SacredSpace_OS\05_MEMORY_ENGINE\migrations\002_lifecycle.sql

-- Adds lifecycle columns to memory_motes

-- Run ONLY after confirming which columns already exist above

ALTER TABLE memory_motes ADD COLUMN confidence REAL DEFAULT 0.7;

ALTER TABLE memory_motes ADD COLUMN source_count INTEGER DEFAULT 1;

ALTER TABLE memory_motes ADD COLUMN last_confirmed TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

ALTER TABLE memory_motes ADD COLUMN superseded_by INTEGER REFERENCES memory_motes(id);

ALTER TABLE memory_motes ADD COLUMN is_stale BOOLEAN DEFAULT 0;

ALTER TABLE memory_motes ADD COLUMN access_count INTEGER DEFAULT 0;

ALTER TABLE memory_motes ADD COLUMN retention_score REAL DEFAULT 1.0;

ALTER TABLE memory_motes ADD COLUMN reinforcement_count INTEGER DEFAULT 0;

ALTER TABLE memory_motes ADD COLUMN category TEXT DEFAULT 'DEFAULT';

-- Index for fast retrieval of active, high-confidence motes

CREATE INDEX IF NOT EXISTS idx_motes_active

ON memory_motes(is_stale, retention_score DESC, confidence DESC);


### STAGE 2 — Uncertainty Gate (Harden RAG Entry)
File: D:\SacredSpace_OS\06_AGENT_LAYER\uncertainty_gate.py

"""

uncertainty_gate.py

SacredSpace OS — Uncertainty Gatekeeper

Evaluates whether current active context is sufficient to answer

a query before triggering expensive RAG/vector DB lookup.

Uses phi3:mini (local, ultra-fast) as judge model.

Threshold: < 0.7 confidence triggers RAG pipeline.

"""

import requests

import json


class UncertaintyGatekeeper:

def __init__(self, ollama_url: str = "http://192.168.240.1:11434"):

self.ollama_url = ollama_url

self.judge_model = "phi3:mini"  # swap for qwen2.5:0.5b if phi3 unavailable

self.threshold = 0.70

def evaluate(self, active_state: dict, user_query: str) -> dict:

"""

Ask the judge: is active context sufficient?

Returns: {sufficient: bool, reason: str, confidence: float}

"""

prompt = f"""You are the Gatekeeper of SacredSpace OS.

Active context state:

{json.dumps(active_state, indent=2)}

User query: {user_query}

Is the information already in the active state sufficient to answer this query

without querying long-term memory?

Respond ONLY with valid JSON, no explanation:

{{"sufficient": true/false, "reason": "brief reason", "confidence": 0.0-1.0}}"""

try:

r = requests.post(

f"{self.ollama_url}/api/generate",

json={

"model": self.judge_model,

"prompt": prompt,

"stream": False,

"format": "json"

},

timeout=20

)

return json.loads(r.json().get("response", "{}"))

except Exception as e:

# Fail safe: uncertainty is high, trigger RAG

return {"sufficient": False, "reason": f"gate_error: {e}", "confidence": 0.0}

def should_retrieve(self, active_state: dict, user_query: str) -> bool:

"""Boolean shorthand for pipeline integration."""

result = self.evaluate(active_state, user_query)

confidence = result.get("confidence", 0.0)

sufficient = result.get("sufficient", False)

return not sufficient or confidence < self.threshold


# Hardened trigger rules (override judge for known patterns)

ALWAYS_RETRIEVE_INTENTS = {

"gematria_lookup", "vault_search", "codex_entry",

"lore_query", "archetype_reference"

}

NEVER_RETRIEVE_INTENTS = {

"status_check", "session_state", "continue_task",

"refactor", "code_generation", "narrative_draft"

}

def gate_with_intent(intent: str, active_state: dict, user_query: str) -> bool:

"""

Hard-coded overrides for known intent categories.

Falls back to judge model for ambiguous cases.

"""

if intent in ALWAYS_RETRIEVE_INTENTS:

return True

if intent in NEVER_RETRIEVE_INTENTS:

return False

# Ambiguous: use the judge

return UncertaintyGatekeeper().should_retrieve(active_state, user_query)


### STAGE 3 — Mote Lifecycle Engine (Ebbinghaus Memory)
File: D:\SacredSpace_OS\05_MEMORY_ENGINE\mote_lifecycle.py

"""

mote_lifecycle.py

SacredSpace OS — Memory Mote Lifecycle Engine

Implements:

- Usage-weighted Ebbinghaus decay: R = R0 * e^(-(λ_eff * t * (1 - I)) / S)

- Category-specific decay rates (CORE_LOGIC near-permanent, TOOL_OUTPUT fast)

- Logarithmic recency softening (prevents cliff effect)

- Supersession (version control for knowledge)

- Reinforcement on access

Trigger: run_decay_pass() called from .claude/hooks/PreCompact.sh

"""

import sqlite3

import math

from datetime import datetime

from typing import Optional, List, Dict

DB_PATH = r"D:\SacredSpace_OS\05_MEMORY_ENGINE\sacred_memory.db"

# Category-specific decay modifiers

# Lower = slower decay = longer half-life

LAMBDA_MAP = {

"CORE_LOGIC":   0.1,   # Near-permanent (canonical architecture decisions)

"INTENT_GOAL":  0.5,   # Months (project goals, active initiatives)

"TOOL_OUTPUT":  2.0,   # Hours/days (file reads, API returns)

"LORE":         0.3,   # Stable but refreshable (Gematria, archetypes)

"SESSION":      3.0,   # Ephemeral (current session state)

"DEFAULT":      1.0,

}


def get_conn() -> sqlite3.Connection:

conn = sqlite3.connect(DB_PATH)

conn.row_factory = sqlite3.Row

return conn


def compute_intensity(access_count: int, last_confirmed: datetime) -> float:

"""

Intensity I: how actively this mote is being used.

Range [0.0, 1.0]. High I = slow decay.

Uses logarithmic recency (soft curve, no cliff).

"""

days_since = max(0, (datetime.now() - last_confirmed).days)

recency_factor = 1.0 / math.log(math.e + days_since)  # log curve, never 0

intensity = min(1.0, (access_count * 0.1) * recency_factor)

return round(intensity, 4)


def decay_retention(r0: float, t_days: float, reinforcement: int, category: str) -> float:

"""

R = R0 * e^(-(λ_eff * t * (1 - I)) / S)

where:

λ_eff  = category decay modifier

t      = days since last confirmed

I      = intensity (computed externally)

S      = stability (grows 1.8x per reinforcement)

"""

lam = LAMBDA_MAP.get(category, LAMBDA_MAP["DEFAULT"])

S = 1.0 * (1.8 ** reinforcement)

# I embedded in the pass below; here we just apply time + lambda

exponent = (lam * t_days) / S

return round(max(0.05, min(1.0, r0 * math.exp(-exponent))), 4)


def reinforce_mote(mote_id: int) -> Dict:

"""Called every time a mote is retrieved and used in context."""

conn = get_conn()

try:

row = conn.execute(

"SELECT * FROM memory_motes WHERE id = ?", (mote_id,)

).fetchone()

if not row:

return {"error": f"Mote {mote_id} not found"}

new_count = row["reinforcement_count"] + 1

new_retention = min(1.0, row["retention_score"] + 0.15)

new_confidence = min(1.0, row["confidence"] + 0.05)

conn.execute("""

UPDATE memory_motes SET

reinforcement_count = ?,

retention_score = ?,

confidence = ?,

last_confirmed = CURRENT_TIMESTAMP,

access_count = access_count + 1

WHERE id = ?

""", (new_count, new_retention, new_confidence, mote_id))

conn.commit()

return {"mote_id": mote_id, "retention_score": new_retention}

finally:

conn.close()


def supersede_mote(old_id: int, new_content: str, agent: str, source: str = "update") -> int:

"""Version-control: marks old mote stale, creates new successor."""

conn = get_conn()

try:

conn.execute("""

INSERT INTO memory_motes

(content, agent, source, confidence, source_count, retention_score,

reinforcement_count, last_confirmed, is_stale, category)

VALUES (?, ?, ?, 0.8, 1, 1.0, 0, CURRENT_TIMESTAMP, 0, 'DEFAULT')

""", (new_content, agent, source))

new_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

conn.execute(

"UPDATE memory_motes SET is_stale = 1, superseded_by = ? WHERE id = ?",

(new_id, old_id)

)

conn.commit()

print(f"[Lifecycle] Mote {old_id} → superseded by Mote {new_id}")

return new_id

finally:

conn.close()


def run_decay_pass() -> Dict:

"""

Full Ebbinghaus decay pass across all active motes.

Call from PreCompact hook (lazy decay = zero wasted cycles).

"""

conn = get_conn()

try:

motes = conn.execute(

"SELECT * FROM memory_motes WHERE is_stale = 0"

).fetchall()

decayed = 0

now = datetime.now()

for m in motes:

last = datetime.fromisoformat(m["last_confirmed"] or now.isoformat())

t = max(0, (now - last).days)

intensity = compute_intensity(m["access_count"], last)

lam = LAMBDA_MAP.get(m["category"] or "DEFAULT", LAMBDA_MAP["DEFAULT"])

S = 1.0 * (1.8 ** m["reinforcement_count"])

# Full formula with intensity

exponent = (lam * t * (1 - intensity)) / S

new_ret = round(max(0.05, min(1.0, m["retention_score"] * math.exp(-exponent))), 4)

if new_ret != m["retention_score"]:

conn.execute(

"UPDATE memory_motes SET retention_score = ? WHERE id = ?",

(new_ret, m["id"])

)

decayed += 1

conn.commit()

return {"total": len(motes), "decayed": decayed}

finally:

conn.close()


def get_live_motes(

agent: Optional[str] = None,

min_retention: float = 0.2,

limit: int = 20

) -> List[Dict]:

"""High-quality mote retrieval for context injection (L5 of compactor)."""

conn = get_conn()

try:

q = """

SELECT id, content, agent, confidence, retention_score, category

FROM memory_motes

WHERE is_stale = 0 AND retention_score >= ?

"""

params = [min_retention]

if agent:

q += " AND agent = ?"

params.append(agent)

q += " ORDER BY (confidence * retention_score) DESC LIMIT ?"

params.append(limit)

return [dict(r) for r in conn.execute(q, params).fetchall()]

finally:

conn.close()


if __name__ == "__main__":

import sys

if "--decay-pass" in sys.argv:

result = run_decay_pass()

print(f"[Decay Pass] {result}")

else:

# Health report

conn = get_conn()

total = conn.execute("SELECT COUNT(*) FROM memory_motes").fetchone()[0]

active = conn.execute(

"SELECT COUNT(*) FROM memory_motes WHERE is_stale = 0"

).fetchone()[0]

avg_ret = conn.execute(

"SELECT AVG(retention_score) FROM memory_motes WHERE is_stale = 0"

).fetchone()[0] or 0

conn.close()

print(f"[Memory Health] Total: {total} | Active: {active} | Avg Retention: {avg_ret:.3f}")


### STAGE 4 — Intent Classifier (Semantic Agent Routing)
File: D:\SacredSpace_OS\02_COUNCIL_GROVE\intent_classifier.py

"""

intent_classifier.py

SacredSpace OS — Sacred Intent Classifier

Routes incoming signals to the correct ICARIS agent using

embedding-based similarity against a registered intent manifest.

Replaces keyword-based routing with semantic routing via ChromaDB.

Threshold: < 0.4 confidence defaults to COUNCIL.

"""

import chromadb

from chromadb.utils import embedding_functions

from dataclasses import dataclass

from typing import Literal

AgentTarget = Literal["ELIAS", "AURORA", "ASHER", "IRIS", "COUNCIL"]

CHROMA_PATH = r"D:\SacredSpace_OS\05_MEMORY_ENGINE\chroma_store"

INTENT_MANIFEST = [

# ELIAS — Knowledge

{"id": "know-001", "text": "explain this concept to me", "agent": "ELIAS"},

{"id": "know-002", "text": "what does this term mean in AI engineering", "agent": "ELIAS"},

{"id": "know-003", "text": "summarize what I know about this topic", "agent": "ELIAS"},

{"id": "know-004", "text": "gematria lookup calculate value", "agent": "ELIAS"},

{"id": "know-005", "text": "what is the archetype for this concept", "agent": "ELIAS"},

# AURORA — Code

{"id": "code-001", "text": "write a python script to do this", "agent": "AURORA"},

{"id": "code-002", "text": "debug this code", "agent": "AURORA"},

{"id": "code-003", "text": "build a new FastAPI route for this", "agent": "AURORA"},

{"id": "code-004", "text": "refactor this module", "agent": "AURORA"},

# ASHER — Entropy / System

{"id": "sys-001", "text": "run this process and report back", "agent": "ASHER"},

{"id": "sys-002", "text": "what entropy or unexpected behavior is occurring", "agent": "ASHER"},

{"id": "sys-003", "text": "check system health and status", "agent": "ASHER"},

# IRIS — Vault

{"id": "vault-001", "text": "save this to the vault", "agent": "IRIS"},

{"id": "vault-002", "text": "search my obsidian notes for this", "agent": "IRIS"},

{"id": "vault-003", "text": "create a codex entry for this", "agent": "IRIS"},

{"id": "vault-004", "text": "seal this in the archive", "agent": "IRIS"},

# COUNCIL — Multi-agent

{"id": "council-001", "text": "council review this decision", "agent": "COUNCIL"},

{"id": "council-002", "text": "synthesize across all agents", "agent": "COUNCIL"},

{"id": "council-003", "text": "architectural decision needs review", "agent": "COUNCIL"},

]


@dataclass

class IntentResult:

agent: AgentTarget

confidence: float

intent_label: str

raw_query: str


class IntentClassifier:

def __init__(self):

self.client = chromadb.PersistentClient(path=CHROMA_PATH)

self.ef = embedding_functions.SentenceTransformerEmbeddingFunction(

model_name="all-MiniLM-L6-v2"

)

self.collection = self.client.get_or_create_collection(

name="sacred_intents",

embedding_function=self.ef

)

self._seed_manifest()

def _seed_manifest(self):

if self.collection.count() == 0:

self.collection.add(

documents=[i["text"] for i in INTENT_MANIFEST],

ids=[i["id"] for i in INTENT_MANIFEST],

metadatas=[{"agent": i["agent"]} for i in INTENT_MANIFEST]

)

print(f"[IntentClassifier] Seeded {len(INTENT_MANIFEST)} intent templates.")

def classify(self, query: str, threshold: float = 0.4) -> IntentResult:

results = self.collection.query(query_texts=[query], n_results=1)

if not results["documents"][0]:

return IntentResult("COUNCIL", 0.0, "unclassified", query)

distance = results["distances"][0][0]

confidence = max(0.0, 1.0 - (distance / 2.0))

meta = results["metadatas"][0][0]

doc = results["documents"][0][0]

agent = meta["agent"] if confidence >= threshold else "COUNCIL"

return IntentResult(

agent=agent,

confidence=round(confidence, 3),

intent_label=doc,

raw_query=query

)

def add_intent(self, intent_id: str, text: str, agent: AgentTarget):

self.collection.add(

documents=[text],

ids=[intent_id],

metadatas=[{"agent": agent}]

)


### STAGE 5 — Context Compactor (5-Layer Pipeline)
File: D:\SacredSpace_OS\05_MEMORY_ENGINE\context_compactor.py

"""

context_compactor.py

SacredSpace OS — 5-Layer Context Compaction Pipeline

Layers:

L1 — Raw session buffer (last N messages)

L2 — Relevance filter (drop low-signal messages)

L3 — Semantic dedup (merge near-duplicates)

L4 — Summary compression (Ollama summarizes old segments)

L5 — Canon injection (top-ranked Memory Motes from SQLite)

"""

import sqlite3

import requests

from typing import List, Dict

OLLAMA_URL = "http://192.168.240.1:11434/api/generate"

DB_PATH = r"D:\SacredSpace_OS\05_MEMORY_ENGINE\sacred_memory.db"


def l1_raw_buffer(messages: List[Dict], window: int = 10) -> List[Dict]:

return messages[-window:]


def l2_relevance_filter(messages: List[Dict], min_length: int = 20) -> List[Dict]:

return [m for m in messages if len(m.get("content", "")) >= min_length]


def l3_semantic_dedup(messages: List[Dict]) -> List[Dict]:

deduped, seen = [], set()

for m in messages:

key = m.get("content", "")[:100]

if key not in seen:

deduped.append(m)

seen.add(key)

return deduped


def l4_summary_compress(messages: List[Dict], target_count: int = 5) -> List[Dict]:

if len(messages) <= target_count:

return messages

to_compress = messages[:len(messages) // 2]

to_keep = messages[len(messages) // 2:]

combined = "\n".join(

f"{m.get('role','?')}: {m.get('content','')}" for m in to_compress

)

prompt = f"Summarize this conversation in 2-3 sentences:\n\n{combined}"

try:

r = requests.post(OLLAMA_URL, json={

"model": "deepseek-r1:1.5b",

"prompt": prompt,

"stream": False

}, timeout=30)

summary = r.json().get("response", "[compression unavailable]")

except Exception as e:

summary = f"[compression failed: {e}]"

return [{"role": "system", "content": f"[COMPRESSED]: {summary}"}] + to_keep


def l5_canon_inject(messages: List[Dict], query: str, top_k: int = 3) -> List[Dict]:

"""Injects top-ranked Memory Motes as system context."""

try:

conn = sqlite3.connect(DB_PATH)

conn.row_factory = sqlite3.Row

rows = conn.execute("""

SELECT content FROM memory_motes

WHERE content LIKE ? AND is_stale = 0

ORDER BY (confidence * retention_score) DESC

LIMIT ?

""", (f"%{query[:30]}%", top_k)).fetchall()

conn.close()

if rows:

mote_text = "\n".join(f"• {r['content']}" for r in rows)

return [{"role": "system", "content": f"[MEMORY MOTES]:\n{mote_text}"}] + messages

except Exception:

pass

return messages


def compact(messages: List[Dict], query: str = "") -> List[Dict]:

"""Run all 5 layers in sequence."""

pipeline = [

("L1 Buffer",       lambda m: l1_raw_buffer(m)),

("L2 Relevance",    lambda m: l2_relevance_filter(m)),

("L3 Dedup",        lambda m: l3_semantic_dedup(m)),

("L4 Compress",     lambda m: l4_summary_compress(m)),

("L5 Canon",        lambda m: l5_canon_inject(m, query)),

]

for label, fn in pipeline:

before = len(messages)

messages = fn(messages)

print(f"[Compactor] {label}: {before}→{len(messages)}")

return messages


### STAGE 6 — State Manager (Differential State Injection)
File: D:\SacredSpace_OS\02_COUNCIL_GROVE\state_manager.py

"""

state_manager.py

SacredSpace OS — Cache-Aware State Manager

Implements state-diffing (RFC 6902 JSON Patch) instead of full-state

transmission. Keeps the cached Kernel frozen while injecting only

what changed into user messages via <system-reminder> tags.

Install: pip install jsonpatch --break-system-packages

"""

import json

import os

import jsonpatch

from datetime import datetime

from typing import Optional

CHECKPOINT_DIR = r"D:\SacredSpace_OS\02_COUNCIL_GROVE\checkpoints"

os.makedirs(CHECKPOINT_DIR, exist_ok=True)


class SacredStateManager:

def __init__(self):

self.last_sent_state: dict = {}

self._load_checkpoint()

def _load_checkpoint(self):

path = os.path.join(CHECKPOINT_DIR, "latest.json")

if os.path.exists(path):

with open(path) as f:

self.last_sent_state = json.load(f)

def _save_checkpoint(self, state: dict):

path = os.path.join(CHECKPOINT_DIR, "latest.json")

with open(path, "w") as f:

json.dump(state, f, indent=2, default=str)

def get_state_patch(self, current_state: dict) -> Optional[dict]:

"""

Generates minimal JSON Patch. Returns None if no changes.

Returns FULL state if patch is larger than full state.

"""

patch = jsonpatch.make_patch(self.last_sent_state, current_state)

self.last_sent_state = current_state

self._save_checkpoint(current_state)

patch_list = patch.patch

if not patch_list:

return None

if len(json.dumps(patch_list)) > len(json.dumps(current_state)):

return {"type": "FULL", "content": current_state}

return {"type": "PATCH", "content": patch_list}

def build_system_reminder(self, current_state: dict) -> str:

"""

Generates the <system-reminder> tag for injection into user message.

Uses diff if available, full state on first call.

"""

patch = self.get_state_patch(current_state)

if patch is None:

return ""

tag = "state_patch" if patch["type"] == "PATCH" else "full_state"

return f"<{tag}>{json.dumps(patch['content'])}</{tag}>"

def execute_precompact_hook(self, active_history: list) -> str:

"""

Called from PreCompact hook. Saves session state before compaction.

Returns a summary string for the next session.

"""

state = {

"timestamp": datetime.now().isoformat(),

"history_length": len(active_history),

"last_message": active_history[-1].get("content", "")[:200] if active_history else ""

}

self._save_checkpoint(state)

return f"[HANDOFF] Session state preserved. {len(active_history)} turns archived."


### STAGE 7 — Model Router (Effort-Aware Dispatch)
File: D:\SacredSpace_OS\06_AGENT_LAYER\model_router.py

"""

model_router.py

SacredSpace OS — Effort-Aware Model Router

Routes tasks to the appropriate model tier based on intent and confidence.

Local-first: Claude API only for high-reasoning tasks.

Effort Matrix:

low    → phi3:mini / qwen2.5:0.5b  (lookups, status)

medium → deepseek-r1:1.5b          (summarization)

high   → qwen2.5-coder:7b          (standard reasoning)

xhigh  → Claude API                (agentic loops, architecture)

max    → Claude API (extended)     (kernel design, council decisions)

"""

import requests

import json

import os

from typing import Literal

EffortLevel = Literal["low", "medium", "high", "xhigh", "max"]

OLLAMA_URL = os.getenv("OLLAMA_HOST", "http://192.168.240.1:11434")

EFFORT_MAP = {

"low":    {"model": "qwen2.5:0.5b",      "use_claude": False, "max_tokens": 512},

"medium": {"model": "deepseek-r1:1.5b",  "use_claude": False, "max_tokens": 1024},

"high":   {"model": "qwen2.5-coder:7b",  "use_claude": False, "max_tokens": 2048},

"xhigh":  {"model": "claude-sonnet-4-6", "use_claude": True,  "max_tokens": 4096},

"max":    {"model": "claude-sonnet-4-6", "use_claude": True,  "max_tokens": 8192},

}

INTENT_EFFORT_MAP = {

"gematria_lookup":    "low",

"status_check":       "low",

"simple_summary":     "medium",

"vault_search":       "medium",

"code_generation":    "high",

"refactor":           "high",

"architectural":      "xhigh",

"council_review":     "max",

}


class ModelRouter:

def __init__(self, ollama_url: str = OLLAMA_URL):

self.ollama_url = ollama_url

self.classifier_model = "qwen2.5:0.5b"

def classify_intent(self, user_input: str) -> dict:

prompt = f"""Classify this AI OS request. Return JSON only:

{{"intent": "gematria_lookup|status_check|simple_summary|vault_search|code_generation|refactor|architectural|council_review", "confidence": 0.0-1.0}}

Request: {user_input}"""

try:

r = requests.post(

f"{self.ollama_url}/api/generate",

json={"model": self.classifier_model, "prompt": prompt,

"stream": False, "format": "json"},

timeout=15

)

return json.loads(r.json().get("response", "{}"))

except Exception:

return {"intent": "council_review", "confidence": 0.0}

def get_effort(self, user_input: str) -> EffortLevel:

analysis = self.classify_intent(user_input)

intent = analysis.get("intent", "council_review")

confidence = analysis.get("confidence", 0.0)

if confidence < 0.6:

return "xhigh"  # low confidence → escalate

return INTENT_EFFORT_MAP.get(intent, "high")

def route(self, user_input: str, payload: list) -> tuple[str, dict]:

"""Returns (model_name, config_dict) for the downstream caller."""

effort = self.get_effort(user_input)

config = EFFORT_MAP[effort]

print(f"[Router] Intent effort: {effort} → {config['model']}")

return config["model"], config


## SERIALIZATION GOLD STANDARD
The order of the API payload determines cache hit rate. Never deviate.

1. <os_kernel>         ← FROZEN, cache_control breakpoint here

2. <tool_definitions>  ← FROZEN, never add/remove mid-session

3. <canon_lore>        ← FROZEN, cache_control breakpoint here

4. <history>           ← DYNAMIC, compacted by ContextCompactor

5. <system-reminder>   ← DYNAMIC, state diff injection

6. <intent>            ← DYNAMIC, user input

Critical Rule: Dynamic data (timestamps, session IDs, current date) must NEVER appear before the cache breakpoints. If any dynamic content leaks into blocks 1-3, the entire KV cache busts on every request.


## PRECOMPACT HOOK
File: D:\SacredSpace_OS\.claude\hooks\PreCompact.sh

#!/bin/bash

# SacredSpace OS — Pre-Compaction Maintenance Pulse

echo "[System] Pre-Compact Maintenance Pulse initiated..."

# 1. Run Memory Decay Pass

python D:/SacredSpace_OS/05_MEMORY_ENGINE/mote_lifecycle.py --decay-pass

# 2. Optimize RAPTOR index

python D:/SacredSpace_OS/03_NEURAL_FOREST/raptor_indexer.py --optimize 2>/dev/null || echo "[Skip] RAPTOR not yet deployed"

# 3. Save state checkpoint

python D:/SacredSpace_OS/02_COUNCIL_GROVE/state_manager.py --checkpoint 2>/dev/null || echo "[Skip] StateManager not yet deployed"

echo "[System] Pre-compact complete. Proceeding to context compaction."


## PERFORMANCE OPTIMIZATION MATRIX


## FAILURE MODES & FIXES


## CODEX ENTRIES
### UncertaintyGatekeeper
## UncertaintyGatekeeper

**Pillar:** 06_AGENT_LAYER

**Owner Agent:** ASHER

**Status:** Active

**Purpose:** Filters RAG pipeline access by judging whether active context is

sufficient to answer a query, preventing unnecessary vector DB calls.

**Inputs:** active_state dict, user query string

**Outputs:** bool (should_retrieve)

**Dependencies:** Ollama (phi3:mini or qwen2.5:0.5b), requests

**Notes:** Confidence threshold 0.70. Hard overrides for known SacredSpace

intent categories. Fail-safe defaults to True (trigger RAG) on error.
### IntentClassifier
## IntentClassifier

**Pillar:** 02_COUNCIL_GROVE

**Owner Agent:** AURORA (build), COUNCIL (governance)

**Status:** Draft

**Purpose:** Routes incoming signals to the correct ICARIS agent using

semantic embedding similarity against a registered intent manifest.

**Inputs:** Raw query string

**Outputs:** IntentResult(agent, confidence, intent_label, raw_query)

**Dependencies:** ChromaDB, all-MiniLM-L6-v2, INTENT_MANIFEST

**Notes:** Confidence < 0.4 → defaults to COUNCIL. Add new intents via

add_intent(). Manifest persists in ChromaDB.
### MoteLifecycleEngine
## MoteLifecycleEngine v1.0

**Pillar:** 05_MEMORY_ENGINE

**Owner Agent:** IRIS

**Status:** Draft

**Purpose:** Implements usage-weighted Ebbinghaus decay, supersession, and

reinforcement for Memory Motes. Translation Layer between Root Archive and

Resonance Layer.

**Inputs:** Access events, update requests, PreCompact trigger

**Outputs:** Ranked lifecycle-aware mote retrieval; decay reports

**Dependencies:** SQLite (sacred_memory.db), migration 002_lifecycle.sql

**Notes:**

- run_decay_pass() called from PreCompact.sh

- Category λ modifiers: CORE_LOGIC=0.1, TOOL_OUTPUT=2.0, DEFAULT=1.0

- Logarithmic recency softening prevents cliff effect on stale motes

- Floor retention 0.05 — nothing is ever fully deleted
### SacredStateManager
## SacredStateManager

**Pillar:** 02_COUNCIL_GROVE

**Owner Agent:** ASHER

**Status:** Draft

**Purpose:** Manages differential state injection via RFC 6902 JSON Patch.

Keeps cached Kernel frozen while injecting only state deltas.

**Inputs:** current_state dict

**Outputs:** <system-reminder> tag string, checkpoint JSON

**Dependencies:** jsonpatch (pip install jsonpatch --break-system-packages)

**Notes:**

- Returns None if no state change (zero token cost)

- Falls back to FULL state transmission if patch is larger than full state

- Persists checkpoints to ..\checkpoints\latest.json
### ModelRouter
## ModelRouter

**Pillar:** 06_AGENT_LAYER

**Owner Agent:** AURORA

**Status:** Draft

**Purpose:** Effort-aware task routing. Local models for low-effort tasks;

Claude API for architectural and agentic work.

**Inputs:** user_input string, assembled payload

**Outputs:** (model_name, config_dict)

**Dependencies:** Ollama, ANTHROPIC_API_KEY env var for Claude paths

**Notes:**

- Confidence < 0.6 always escalates to xhigh

- Do NOT switch models mid-session for same workflow (breaks cache)

- Sub-agents should be spawned as isolated processes, not in-line model swaps


## INSTALL COMMANDS
# Required Python packages

pip install jsonpatch --break-system-packages

pip install chromadb --break-system-packages

pip install sentence-transformers --break-system-packages

pip install scikit-learn numpy --break-system-packages  # for RAPTOR indexer

pip install redis --break-system-packages               # for semantic cache (optional MVP+)


## GAUNTLET RESPONSES — FOR OS KERNEL
The three gauntlet sets from the research session are recorded here as test vectors for the SacredSpace OS reasoning engine. Use these to validate agent depth and symbolic coherence.

Gauntlet I (Sacred Philosophy): Sovereignty Paradox, Wisdom Boundary, Agentic Social Contract, Mirror Principle.

Gauntlet II (Trinity — Music/Geometry/Physics): Frequency of Form, Duality of Code, Harmonic Architecture, Resonance of Entropy.

Gauntlet III (Sacred Storyline): Jenga Constraint, Echo Paradox, Procedural Destiny, Repository as Artifact.

These questions are not philosophical exercises — they are stress-tests for SACRED_OS_CORE.md. A fully calibrated OS should be able to respond to each through its symbolic logic matrix without hallucinating lore.



Ground. Consolidate. Deploy. Document. Repeat.
In lakesh alakin.

| Component | File | Pillar | Owner Agent | Priority |
| --- | --- | --- | --- | --- |
| Uncertainty Gatekeeper | uncertainty_gate.py | 06_AGENT_LAYER | ASHER | 1 (DONE) |
| Intent Classifier | intent_classifier.py | 02_COUNCIL_GROVE | AURORA | 2 |
| SQLite Migration | 002_lifecycle.sql | 05_MEMORY_ENGINE | IRIS | 3 |
| Mote Lifecycle Engine | mote_lifecycle.py | 05_MEMORY_ENGINE | IRIS | 4 |
| Query Transformer | query_transformer.py | 03_NEURAL_FOREST | AURORA | 5 |
| RAG Router | rag_router.py | 03_NEURAL_FOREST | AURORA | 6 |
| RAPTOR Indexer | raptor_indexer.py | 03_NEURAL_FOREST | AURORA | 7 |
| Context Compactor | context_compactor.py | 05_MEMORY_ENGINE | IRIS | 8 |
| State Manager | state_manager.py | 02_COUNCIL_GROVE | ASHER | 9 |
| Model Router | model_router.py | 06_AGENT_LAYER | AURORA | 10 |
| Inference Core | SacredSpace_Inference_Core.py | 02_COUNCIL_GROVE | Council | 11 |
| Microcompactor | micro_compactor.py | 05_MEMORY_ENGINE | IRIS | 12 |
| Semantic Cache | semantic_cache.py | 05_MEMORY_ENGINE | IRIS | 13 |
| Strategy | Token Savings | Latency | Complexity | When to Use |
| --- | --- | --- | --- | --- |
| Prefix Caching | 80–95% | ↓↓ Major | Low | Always — universal baseline |
| Semantic Caching (Redis) | 100% (bypasses LLM) | Near-zero | Medium | High-frequency repetitive lookups |
| Uncertainty Gate | Variable | ↑ +20ms | Low | Before any RAG call |
| Tool-Result Archiving | 40–60% | Moderate | Low | Large file reads, API returns |
| PreCompact State Injection | 50–70% | Moderate | High | Long-running Lore-to-Product sessions |
| State-Diffing | 90%+ on state | Near-zero | Medium | Any stateful multi-turn session |
| Sub-agent effort routing | 60–80% on routine | ↓↓ Fast | Medium | All production traffic |
| Failure | Symptom | Fix |
| --- | --- | --- |
| Cache Busting | cache_read_input_tokens = 0 | Move all dynamic vars to <system-reminder>, never in blocks 1–3 |
| Context Drift | Agent loses project thread | Implement PreCompact hook; checkpoint before compaction |
| Over-summarization | Agent loses critical decisions | Use Tool-Result Archiving before full summarization |
| Gatekeeper hallucination | Wrong RAG trigger decisions | Add hard-coded override lists (ALWAYS/NEVER_RETRIEVE_INTENTS) |
| OOM on local models | VRAM exceeded | Lock context window in Modelfile; use Microcompactor aggressively |