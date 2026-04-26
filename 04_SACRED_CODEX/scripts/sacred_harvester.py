"""
sacred_harvester.py
═══════════════════════════════════════════════════════════
SacredSpace OS — Neural Forest Daemon
Pillar:      03_NEURAL_FOREST
Owner Agent: IRIS (vault) + AURORA (code)
Status:      Canon Draft
Purpose:     Watches 00_INBOX for new .md clips, sends content
             to local Ollama for tag/pillar suggestions, writes
             metadata back into YAML frontmatter without touching
             the note body. Logs all operations to Neural Forest.

Stack:       watchdog, python-frontmatter, httpx, pathlib
             — 100% open-source, zero-cost, local-first

WSL2 path:   /mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault/
Windows path: D:\\SacredSpace_OS\\01_OBSIDIAN_VAULTS\\SacredSpace_Vault\\

Install deps:
    pip install watchdog python-frontmatter httpx --break-system-packages

Run:
    python3 sacred_harvester.py

    Or as background daemon:
    nohup python3 sacred_harvester.py > harvester.log 2>&1 &
═══════════════════════════════════════════════════════════
"""

import time
import json
import logging
import httpx
import frontmatter
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ─── CONFIGURATION ────────────────────────────────────────────────────────────

VAULT_ROOT = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
INBOX_PATH = VAULT_ROOT / "00_INBOX"
HOLDING_PATH = INBOX_PATH / "HOLDING"
LOG_PATH = Path("/mnt/d/SacredSpace_OS/03_NEURAL_FOREST/logs/harvester.log")

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral"  # Change to your preferred local model (llama3, phi3, etc.)

# Pillar routing map — matches TRIAGE_REFERENCE.md
PILLAR_MAP = {
    "ai": "01_OBSIDIAN_VAULTS/KNOWLEDGE_VAULT",
    "research": "01_OBSIDIAN_VAULTS/KNOWLEDGE_VAULT",
    "python": "08_LEARNING_PATH/references",
    "fastapi": "08_LEARNING_PATH/references",
    "code": "08_LEARNING_PATH/references",
    "brand": "07_SOCIAL_MOTHERSHIP/brand",
    "design": "07_SOCIAL_MOTHERSHIP/brand",
    "typography": "07_SOCIAL_MOTHERSHIP/brand",
    "tarot": "04_SACRED_CODEX/lore",
    "arcana": "04_SACRED_CODEX/lore",
    "hermetic": "04_SACRED_CODEX/lore",
    "jenga": "04_SACRED_CODEX/story",
    "story": "04_SACRED_CODEX/story",
    "narrative": "04_SACRED_CODEX/story",
    "market": "09_SACRED_MARKET/research",
    "etsy": "09_SACRED_MARKET/research",
    "revenue": "09_SACRED_MARKET/research",
    "ollama": "03_NEURAL_FOREST/references",
    "chromadb": "03_NEURAL_FOREST/references",
    "wsl": "03_NEURAL_FOREST/references",
    "infra": "03_NEURAL_FOREST/references",
    "family": "FAMILY_LEGACY",
    "parenting": "FAMILY_LEGACY",
    "iris": "FAMILY_LEGACY",
    "asher": "FAMILY_LEGACY",
}

# ─── LOGGING SETUP ────────────────────────────────────────────────────────────

LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [HARVESTER] %(levelname)s — %(message)s",
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler(),  # also print to terminal
    ],
)
log = logging.getLogger("sacred_harvester")

# ─── OLLAMA INTERFACE ─────────────────────────────────────────────────────────

TRIAGE_PROMPT = """You are IRIS, the vault agent of SacredSpace OS. 
Analyze the following web clip and return ONLY a valid JSON object with no preamble, 
no markdown, no explanation. The JSON must have exactly these keys:

{{
  "suggested_tags": ["tag1", "tag2", "tag3"],
  "suggested_pillar": "pillar/path",
  "summary": "one sentence describing the core content",
  "confidence": "high|medium|low"
}}

Available pillars:
- 01_OBSIDIAN_VAULTS/KNOWLEDGE_VAULT (AI, ML, research, tools)
- 03_NEURAL_FOREST/references (Ollama, ChromaDB, WSL2, infra)
- 04_SACRED_CODEX/lore (sacred geometry, Tarot, Hermetics, arcana)
- 04_SACRED_CODEX/story (Jenga's Journey, narrative, character)
- 07_SOCIAL_MOTHERSHIP/brand (branding, design, typography, aesthetics)
- 08_LEARNING_PATH/references (Python, FastAPI, code, engineering)
- 09_SACRED_MARKET/research (business, revenue, Etsy, POD)
- FAMILY_LEGACY (family, parenting, Iris, Asher, Sacred Messages)
- 00_INBOX/HOLDING (ambiguous, unclear, needs more context)

Web clip content:
---
{content}
---

Return only the JSON object."""


def query_ollama(content: str) -> dict:
    """Send clip content to local Ollama for tag/pillar analysis."""
    prompt = TRIAGE_PROMPT.format(content=content[:3000])  # cap at 3k chars

    try:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2},  # low temp for consistent structure
            },
            timeout=60.0,
        )
        response.raise_for_status()
        raw = response.json().get("response", "").strip()

        # Strip markdown fences if model wraps in ```json
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        return json.loads(raw)

    except httpx.TimeoutException:
        log.warning("Ollama timeout — marking clip for manual review")
        return _fallback_metadata()
    except json.JSONDecodeError as e:
        log.warning(f"Ollama returned malformed JSON: {e}")
        return _fallback_metadata()
    except Exception as e:
        log.error(f"Ollama query failed: {e}")
        return _fallback_metadata()


def _fallback_metadata() -> dict:
    """Return safe defaults when Ollama is unavailable or fails."""
    return {
        "suggested_tags": ["#unclear", "#needs-review"],
        "suggested_pillar": "00_INBOX/HOLDING",
        "summary": "Auto-triage failed — manual review required.",
        "confidence": "low",
    }

# ─── FRONTMATTER PROCESSOR ────────────────────────────────────────────────────

def process_clip(filepath: Path) -> None:
    """Read a clipped .md file, query Ollama, update YAML frontmatter."""
    log.info(f"Processing: {filepath.name}")

    try:
        post = frontmatter.load(filepath)
    except Exception as e:
        log.error(f"Failed to parse frontmatter in {filepath.name}: {e}")
        return

    # Skip if already reviewed or canon
    current_status = post.metadata.get("status", "raw")
    if current_status in ("reviewed", "canon", "archived"):
        log.info(f"Skipping {filepath.name} — status is already '{current_status}'")
        return

    # Build content string for Ollama
    title = post.metadata.get("title", "")
    body = post.content or ""
    content = f"Title: {title}\n\n{body}"

    # Query local Ollama
    log.info(f"Querying {OLLAMA_MODEL} for metadata suggestions...")
    suggestions = query_ollama(content)

    # Update frontmatter — never touch the body
    post.metadata["suggested_tags"] = suggestions.get("suggested_tags", [])
    post.metadata["suggested_pillar"] = suggestions.get("suggested_pillar", "00_INBOX/HOLDING")
    post.metadata["iris_summary"] = suggestions.get("summary", "")
    post.metadata["iris_confidence"] = suggestions.get("confidence", "low")
    post.metadata["harvested_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    post.metadata["status"] = "reviewed"  # promote from raw → reviewed

    # Write back to file
    try:
        updated = frontmatter.dumps(post)
        filepath.write_text(updated, encoding="utf-8")
        log.info(
            f"✓ Updated: {filepath.name} → pillar: {suggestions.get('suggested_pillar')} "
            f"| confidence: {suggestions.get('confidence')}"
        )
    except Exception as e:
        log.error(f"Failed to write updated frontmatter to {filepath.name}: {e}")

# ─── WATCHDOG EVENT HANDLER ───────────────────────────────────────────────────

class InboxWatcher(FileSystemEventHandler):
    """Watches 00_INBOX for new .md files and triggers processing."""

    def on_created(self, event):
        if event.is_directory:
            return

        path = Path(event.src_path)

        # Only process markdown files
        if path.suffix != ".md":
            return

        # Skip HOLDING subfolder (those are already flagged ambiguous)
        if "HOLDING" in str(path):
            return

        # Brief pause to ensure file is fully written before reading
        time.sleep(1.5)

        log.info(f"New clip detected: {path.name}")
        process_clip(path)

    def on_modified(self, event):
        # Ignore modification events — we only want fresh clips
        pass

# ─── STARTUP BANNER ──────────────────────────────────────────────────────────

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║          S∆CR3D H∆RV3ST3R — Neural Forest Daemon        ║
║          IRIS Vault Ingestion Layer v1.0                 ║
╠══════════════════════════════════════════════════════════╣
║  Watching:  00_INBOX                                     ║
║  Model:     {model:<48}║
║  Log:       03_NEURAL_FOREST/logs/harvester.log          ║
║                                                          ║
║  Clip → Detect → Ollama → Tag → status: reviewed         ║
║  The Forest watches. In lakesh alakin.                   ║
╚══════════════════════════════════════════════════════════╝
""".format(model=OLLAMA_MODEL)
    print(banner)

# ─── MAIN DAEMON LOOP ─────────────────────────────────────────────────────────

def main():
    print_banner()

    # Ensure inbox exists
    INBOX_PATH.mkdir(parents=True, exist_ok=True)
    HOLDING_PATH.mkdir(parents=True, exist_ok=True)

    log.info(f"Daemon started. Watching: {INBOX_PATH}")
    log.info(f"Ollama endpoint: {OLLAMA_URL} | Model: {OLLAMA_MODEL}")

    # Process any existing unreviewed clips on startup
    existing = list(INBOX_PATH.glob("*.md"))
    if existing:
        log.info(f"Found {len(existing)} existing clip(s) in inbox — processing on startup...")
        for clip in existing:
            if "DAILY_TRIAGE" not in clip.name:
                process_clip(clip)

    # Start file watcher
    event_handler = InboxWatcher()
    observer = Observer()
    observer.schedule(event_handler, str(INBOX_PATH), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        log.info("Daemon interrupted by user. Shutting down cleanly.")
        observer.stop()

    observer.join()
    log.info("Sacred Harvester offline. The Forest rests.")


if __name__ == "__main__":
    main()
