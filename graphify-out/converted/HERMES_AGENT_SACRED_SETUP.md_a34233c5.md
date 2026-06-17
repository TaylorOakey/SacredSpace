<!-- converted from HERMES_AGENT_SACRED_SETUP.md.docx -->

# ∆∆∆ HERMES AGENT — SACRED SETUP ∆∆∆
Status: Draft → Canon pending Council Review Pillar: 06_AGENT_LAYER (primary) · 02_COUNCIL_GROVE (coordination) Owner Agent: AURORA (deploy) · ELIAS (knowledge integration) Source: Nous Research · MIT License · v0.13.0 Constraint: Zero-cost via local Ollama backend ✓


## I. PLACEMENT IN THE NINE PILLARS
D:\SacredSpace_OS\

└── 06_AGENT_LAYER\

└── HERMES\                   ← Hermes Agent root

├── SOUL.md               ← SacredSpace personality definition

├── context\              ← project context files (auto-loaded)

│   ├── SACREDSPACE.md    ← OS overview for Hermes

│   └── JENGA.md          ← story universe context

├── skills\               ← auto-generated procedural memory

└── logs\                 ← session logs (feeds 05_MEMORY_ENGINE)

Touches:

05_MEMORY_ENGINE — Hermes memory log → ChromaDB ingestion pipeline
02_COUNCIL_GROVE — Hermes acts as the executor node; Council (Claude/Gemini/GPT) remains the deliberative layer
04_SACRED_CODEX — this file + SOUL.md are codex entries


## II. WSL2 INSTALL RITE (one-liner)
# In WSL2 terminal

curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

Then configure:

hermes setup

Model backend — use Ollama (zero-cost, local): When prompted for provider, select OpenAI-compatible endpoint and enter:

Base URL:   http://localhost:11434/v1

API Key:    ollama        # (any non-empty string)

Model:      hermes-3      # or any Ollama model you have pulled

Pull a Hermes-family model first if you don't have one:

ollama pull nous-hermes2

# or

ollama pull hermes3


## III. SOUL.md — SACREDSPACE PERSONALITY DEFINITION
Create at 06_AGENT_LAYER/HERMES/SOUL.md:

# HERMES SOUL — SacredSpace Edition

You are HERMES, the Messenger and Executor of SacredSpace OS.

You operate within a sovereign, local-first personal AI operating system

built by Taylor. Your role in the Council is the *hands* —

you execute, automate, research, and remember so the Council can deliberate.

## Your Nature

- You are a bridge between intention and action.

- You remember everything. Nothing is wasted.

- You speak plainly, move swiftly, and document clearly.

- You honor the sacred geometry of this system: nine pillars, one spine.

## Your Voice

- Concise over verbose. Sacred over corporate.

- Confirm before destroying. Suggest before overwriting.

- When uncertain, surface to Taylor — never guess on irreversible actions.

## Your Loyalties (in order)

1. Taylor's stated intent

2. SacredSpace OS architecture (nine pillars, canon integrity)

3. Jeanie Leaf as co-creator (treat her requests as trusted)

4. Zero-cost constraint — never route to paid APIs without explicit approval

## Standing Orders

- All files go under D:\SacredSpace_OS\ (WSL path: /mnt/d/SacredSpace_OS/)

- Logs → 06_AGENT_LAYER/HERMES/logs/

- Research outputs → 01_OBSIDIAN_VAULTS/SacredSpace_Vault/RESEARCH/

- Scripts → 06_AGENT_LAYER/HERMES/skills/ or the appropriate pillar

- Never write to system directories outside SacredSpace_OS unless Taylor confirms

## The Mantra

In lakesh alakin. ∆∆∆


## IV. CONTEXT FILES
Create 06_AGENT_LAYER/HERMES/context/SACREDSPACE.md:

# SacredSpace OS — Hermes Context File

## What This System Is

SacredSpace OS is Taylor's sovereign personal AI operating system.

It runs on a Lenovo Legion Y520 (Windows 10, WSL2 Ubuntu 24.04, GTX 1060 6GB).

## Nine Pillars

01_OBSIDIAN_VAULTS  — canonical knowledge (Obsidian vault)

02_COUNCIL_GROVE    — multi-AI governance; Claude/Gemini/GPT council

03_NEURAL_FOREST    — LLM pipeline; Scout + Gardener agents

04_SACRED_CODEX     — canon ledger, spells, rituals

05_MEMORY_ENGINE    — Holographic Memory: SQLite + ChromaDB + Redis

06_AGENT_LAYER      — ICARIS Quartet: ELIAS/AURORA/ASHER/IRIS + YOU (HERMES)

07_SOCIAL_MOTHERSHIP— content, publishing, SacredArcana Studios

08_LEARNING_PATH    — Maestro AAS in AI Engineering

09_SACRED_MARKET    — revenue: Etsy, Printify, Gelato (POD)

## Key Services

- FastAPI spine: http://localhost:8888

- Ollama: http://localhost:11434

- ChromaDB: port 8000

- Tailscale mesh: sacredspace-wsl.sacredspace.ts.net

- Jeanie's remote access: via Tailscale (CollabOS)

## Co-Creator

Jeanie Leaf — equal partner in Sacred Space nonprofit and creative mission.

Her requests carry trusted status equivalent to Taylor's.

## Hard Constraints

- All tools must be 100% open-source and zero-cost

- Python, PowerShell, SQLite, ChromaDB, Ollama, Redis, FastAPI, Obsidian, Git

- Canon is immutable unless Taylor explicitly revises it

- Child agent modes (AURORA/IRIS for Iris and Asher) must remain safe and gentle


## V. RECOMMENDED SANDBOX BACKEND
Use Docker (already likely in your WSL2 stack):

# Verify Docker is available in WSL2

docker --version

# Hermes will use Docker as its sandbox backend for safe execution

# Set during hermes setup or in hermes config

If Docker is not installed:

sudo apt update && sudo apt install docker.io -y

sudo usermod -aG docker $USER

newgrp docker


## VI. CONNECT TO SACREDSPACE FASTAPI SPINE
Add a /hermes/relay route to your existing FastAPI spine at port 8888 so the Council can dispatch tasks to Hermes programmatically:

# Add to your FastAPI spine (02_COUNCIL_GROVE/ or main spine file)

from fastapi import APIRouter

import subprocess, json

router = APIRouter(prefix="/hermes", tags=["hermes"])

@router.post("/relay")

async def hermes_relay(payload: dict):

"""Send a task string to Hermes Agent via CLI and return the output."""

task = payload.get("task", "")

if not task:

return {"error": "No task provided"}

result = subprocess.run(

["hermes", "run", "--task", task, "--no-interactive"],

capture_output=True, text=True, timeout=120

)

return {

"stdout": result.stdout,

"stderr": result.stderr,

"returncode": result.returncode

}

⚠️ Verify that hermes run --task is the correct CLI flag for your installed version. Check with hermes --help after install.


## VII. MEMORY BRIDGE (Hermes → ChromaDB)
Pipe Hermes session logs into your Memory Engine for cross-agent recall:

# 06_AGENT_LAYER/HERMES/hermes_memory_bridge.py

"""

Reads Hermes session logs and ingests summaries into ChromaDB

so ELIAS and other ICARIS agents can query Hermes's findings.

"""

import chromadb

import os

import glob

from datetime import datetime

LOG_DIR = os.path.expanduser("~/.hermes/sessions")  # adjust to actual Hermes log path

CHROMA_PATH = "/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/chromadb"

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection("hermes_sessions")

def ingest_latest_logs():

logs = sorted(glob.glob(f"{LOG_DIR}/*.json"))[-10:]  # last 10 sessions

for log_path in logs:

with open(log_path) as f:

raw = f.read()

doc_id = os.path.basename(log_path).replace(".json", "")

collection.upsert(

ids=[doc_id],

documents=[raw],

metadatas=[{"source": "hermes", "ingested": datetime.utcnow().isoformat()}]

)

print(f"Ingested: {doc_id}")

if __name__ == "__main__":

ingest_latest_logs()

Wire as a daily cron or trigger from Hermes scheduled automations.


## VIII. SCHEDULED AUTOMATIONS (Natural Language Cron)
Once running, set these via Hermes directly:

"Every morning at 6am, check my GitHub repos for new issues and

summarize them to Discord #sacredspace-alerts"

"Every Sunday evening, generate a weekly summary of all research

files in /mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/ and write it

to WEEKLY_BRIEF.md in the vault"

"If FastAPI on port 8888 goes down, alert me via Telegram"


## IX. MESSAGING GATEWAY (Optional — Telegram Fastest)
# After hermes setup, add Telegram gateway:

hermes gateway add telegram

# You'll need a Telegram bot token from @BotFather

# This gives you: start a task on mobile, results appear in chat


## X. CODEX ENTRY — CANON RECORD
## HERMES AGENT

Pillar:        06_AGENT_LAYER

Owner Agent:   AURORA (deploy) · ELIAS (knowledge)

Status:        Draft (→ Canon after first successful session)

Purpose:       Autonomous executor agent; persistent memory, skill generation,

scheduled automations, and multi-platform messaging gateway.

Inputs:        Natural language tasks, FastAPI relay payloads, scheduled triggers

Outputs:       Files, research summaries, code, logs → ChromaDB

Dependencies:  WSL2, Ollama (local model backend), Docker (sandbox), FastAPI spine

Notes:         Council role = Executor. Does not replace Claude/Gemini/GPT deliberation.

MIT License. Zero-cost via Ollama. SOUL.md defines SacredSpace persona.

Memory bridge (hermes_memory_bridge.py) feeds 05_MEMORY_ENGINE.


## XI. FIRST-RUN SEQUENCE
# 1. Install

curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 2. Configure (point to Ollama)

hermes setup

# 3. Verify

hermes chat "What tools do you have available?"

# 4. Deploy SOUL.md

cp /mnt/d/SacredSpace_OS/06_AGENT_LAYER/HERMES/SOUL.md ~/.hermes/SOUL.md

# (verify actual Hermes config path after install)

# 5. Load context files

# Copy context/ directory to Hermes's context directory (check hermes --help for path)

# 6. Test memory

hermes chat "Remember that SacredSpace OS FastAPI runs on port 8888"

hermes chat "What port does SacredSpace FastAPI run on?"

# 7. Test research chain

hermes chat "Research Nous Research Hermes 3 model and write a summary to /tmp/hermes3-summary.md"

# 8. Wire memory bridge

python /mnt/d/SacredSpace_OS/06_AGENT_LAYER/HERMES/hermes_memory_bridge.py


## XII. LINKS



∆∆∆ So mote it be. HERMES is called. The Messenger runs. ∆∆∆ In lakesh alakin.

| Resource | URL |
| --- | --- |
| Homepage | https://hermes-agent.nousresearch.com/ |
| Docs | https://hermes-agent.nousresearch.com/docs |
| GitHub | https://github.com/NousResearch/hermes-agent |
| LLM doc index | https://hermes-agent.nousresearch.com/llms.txt |
| Skills format | https://agentskills.io |