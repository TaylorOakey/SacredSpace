"""
╔══════════════════════════════════════════════════════════════╗
║  LORE-TO-PRODUCT ENGINE                                      ║
║  SacredSpace OS · 07_SOCIAL_MOTHERSHIP (lore) + 09_SACRED_MARKET ║
║  Owner Agent: ELIAS (extraction) + AURORA (inventory cross-  ║
║               reference) + GR∆M∆ (artifact naming)          ║
║  System Tag: LORE_PRODUCT_ENGINE                             ║
║  Status: Active                                              ║
╚══════════════════════════════════════════════════════════════╝

"The story already knows what the market needs.
 The engine only listens."

Scans Obsidian lore/creative notes for physical objects, relics,
and artifacts implied by the narrative. Cross-references them
against the M3RCH∆NT inventory. Surfaces gaps — things the story
mentions that the Sacred Market doesn't carry yet.

For each gap, generates a ready-to-paste Obsidian artifact note
with full frontmatter, so vault_watcher.py can sync it to
merchant.py immediately after review.

─── LORE NOTE DETECTION ──────────────────────────────────────
The engine scans notes tagged with:
    type: lore | story | worldbuilding | chapter | idea | scene

Or notes in these folders (configurable):
    Lore/ | Story/ | Chapters/ | Characters/ | Worldbuilding/

Notes tagged `type: artifact` are skipped (already in inventory).

─── LLM LAYER (Ollama — local, zero-cost) ───────────────────
Model: deepseek-r1:1.5b (confirmed operational)
Endpoint: http://192.168.240.1:11434  (WSL2 Ollama — NOT localhost)

Falls back to keyword extraction if Ollama is unreachable.

─── CROSS-REFERENCE ─────────────────────────────────────────
Fuzzy match (difflib) against merchant.py artifact names.
Threshold: 0.72 similarity = "already exists."

─── OUTPUT ──────────────────────────────────────────────────
Gap report: JSON + markdown
Auto-draft: Obsidian frontmatter for each gap, ready for review
            and paste into vault → vault_watcher picks it up.
"""

import os
import re
import json
import time
import logging
import requests
from pathlib import Path
from datetime import datetime, timezone
from difflib import SequenceMatcher
from typing import Optional

import yaml
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ─── CONFIG ────────────────────────────────────────────────────────────────────

VAULT_PATH = Path(
    os.environ.get(
        "SACREDSPACE_VAULT",
        r"D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault",
    )
)

# Ollama — WSL2 endpoint (192.168.240.1, NOT localhost — Tailscale DNS conflict)
OLLAMA_URL   = os.environ.get("OLLAMA_URL", "http://192.168.240.1:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-r1:1.5b")

# M3RCH∆NT API
MERCHANT_API = os.environ.get("MERCHANT_API", "http://localhost:8888")

# Fuzzy match threshold — 0.72 means "close enough to be the same artifact"
MATCH_THRESHOLD = 0.72

# Lore note type tags (case-insensitive)
LORE_TYPES = {"lore", "story", "worldbuilding", "chapter", "idea", "scene",
              "myth", "character", "quest", "ritual", "creative"}

# Folder names that signal lore content (scanned regardless of type tag)
LORE_FOLDERS = {"lore", "story", "chapters", "characters", "worldbuilding",
                "scenes", "myths", "quests", "rituals", "creative", "novel",
                "jenga", "sacredspace"}

# Skip these types — already handled
SKIP_TYPES = {"artifact"}

# Folders to always skip
SKIP_FOLDERS = {".obsidian", ".trash", "templates", "attachments"}

# SacredSpace artifact vocabulary for keyword fallback
ARTIFACT_KEYWORDS = [
    # Objects with material form
    "lantern", "staff", "blade", "mask", "relic", "crystal", "stone",
    "amulet", "talisman", "sigil", "glyph", "scroll", "tome", "codex",
    "drum", "bow", "arrow", "shield", "cloak", "robe", "hood", "ring",
    "pendant", "crown", "vessel", "jar", "flask", "pouch", "satchel",
    "map", "compass", "clock", "mirror", "lens", "key", "lock", "seed",
    "root", "flower", "feather", "wing", "tooth", "bone", "horn",
    # SacredSpace-specific
    "heartstone", "memory mote", "waystone", "moonfeather", "raindrop staff",
    "spiceblade", "mirroreblade", "techno-runic", "hyperglyph", "totem",
    "spirit guide", "sacred fire", "ancestral flame", "living artifact",
    # Product-adjacent
    "card deck", "tarot", "oracle", "journal", "notebook", "poster",
    "print", "sticker", "patch", "coin", "token", "badge",
]

logging.basicConfig(
    level=logging.INFO,
    format="[LORE ENGINE] %(asctime)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("lore_engine")


# ─── OLLAMA CLIENT ─────────────────────────────────────────────────────────────

class OllamaClient:
    """Thin wrapper for local Ollama inference."""

    def __init__(self, base_url: str, model: str):
        self.url   = base_url.rstrip("/")
        self.model = model

    def is_reachable(self) -> bool:
        try:
            r = requests.get(f"{self.url}/api/tags", timeout=4)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def extract_artifacts(self, text: str) -> list[dict]:
        """
        Ask Ollama to extract artifact signals from lore text.
        Returns list of signal dicts, or empty list on failure.
        """
        prompt = f"""You are analyzing creative writing from the SacredSpace universe — a mythic world of sacred artifacts, elemental magic, and ancestral memory.

Read the text below and extract every PHYSICAL OBJECT mentioned or strongly implied that could realistically become a real-world product. Include: relics, tools, weapons, garments, jewelry, masks, staffs, crystals, books, maps, cards, lanterns, pouches, or any named sacred item.

RULES:
- Only include objects with a clear physical form
- Include both explicitly named objects AND strongly implied ones
- Skip abstract concepts, places, emotions, characters
- Assign the most fitting type and element from SacredSpace canon

Return ONLY a JSON array. No explanation. No markdown. No other text.

Format exactly:
[{{"name": "item name", "type": "PRINT|APPAREL|ACCESSORY|JOURNAL|CARD_DECK|RELIC|DIGITAL|BUNDLE", "element": "FIRE|WATER|EARTH|AIR|AETHER", "excerpt": "short quote from text showing this item", "confidence": 0.85}}]

If nothing qualifies, return: []

TEXT TO ANALYZE:
---
{text[:3000]}
---

JSON array:"""

        try:
            r = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model":  self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 512},
                },
                timeout=60,
            )
            if r.status_code != 200:
                return []

            raw = r.json().get("response", "").strip()

            # Strip any <think> blocks deepseek-r1 emits
            raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()

            # Find the JSON array
            start = raw.find("[")
            end   = raw.rfind("]") + 1
            if start == -1 or end == 0:
                return []

            signals = json.loads(raw[start:end])
            return [s for s in signals if isinstance(s, dict) and "name" in s]

        except (requests.RequestException, json.JSONDecodeError, KeyError):
            return []


# ─── KEYWORD FALLBACK EXTRACTOR ────────────────────────────────────────────────

def keyword_extract(text: str, source_note: str) -> list[dict]:
    """
    Fallback when Ollama is not reachable.
    Scans text for SacredSpace artifact vocabulary.
    Lower confidence, higher false-positive rate — always review.
    """
    found = []
    text_lower = text.lower()
    for kw in ARTIFACT_KEYWORDS:
        if kw in text_lower:
            # Find the surrounding sentence as excerpt
            idx = text_lower.find(kw)
            start = max(0, text_lower.rfind(".", 0, idx) + 1)
            end   = text_lower.find(".", idx)
            end   = end if end != -1 else min(idx + 100, len(text))
            excerpt = text[start:end].strip()

            # Rough element guess from context
            element = "AETHER"
            ctx = text_lower[max(0, idx - 80): idx + 80]
            if any(w in ctx for w in ["fire","flame","burn","ember","heat","sun"]):
                element = "FIRE"
            elif any(w in ctx for w in ["water","river","ocean","rain","wave","flow"]):
                element = "WATER"
            elif any(w in ctx for w in ["earth","soil","root","stone","tree","forest"]):
                element = "EARTH"
            elif any(w in ctx for w in ["wind","air","sky","breath","feather","cloud"]):
                element = "AIR"

            # Rough type guess
            artifact_type = "RELIC"
            if any(w in kw for w in ["scroll","tome","codex","map","journal","notebook"]):
                artifact_type = "JOURNAL"
            elif any(w in kw for w in ["card","tarot","oracle"]):
                artifact_type = "CARD_DECK"
            elif any(w in kw for w in ["print","poster","glyph","sigil"]):
                artifact_type = "PRINT"
            elif any(w in kw for w in ["sticker","patch","badge","coin"]):
                artifact_type = "ACCESSORY"

            found.append({
                "name":       kw.title(),
                "type":       artifact_type,
                "element":    element,
                "excerpt":    excerpt[:200],
                "confidence": 0.55,
                "method":     "keyword_fallback",
            })

    return found


# ─── VAULT SCANNER ─────────────────────────────────────────────────────────────

def is_lore_note(md_path: Path, frontmatter: Optional[dict]) -> bool:
    """
    Determine if a note is eligible for lore scanning.
    Scans ALL .md files unless explicitly tagged type: artifact.
    Compatible with SacredSpace vault structure (01_OBSIDIAN_VAULTS, 07_SOCIAL_MOTHERSHIP, etc.)
    """
    if frontmatter:
        note_type = str(frontmatter.get("type", "")).lower()
        if note_type in SKIP_TYPES:
            return False  # Already an artifact — skip
    return True


def read_note_body(md_path: Path) -> str:
    """Return note body text (below the frontmatter block)."""
    try:
        text = md_path.read_text(encoding="utf-8")
    except (IOError, UnicodeDecodeError):
        return ""

    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].strip()
    return text.strip()


def read_frontmatter(md_path: Path) -> Optional[dict]:
    try:
        text = md_path.read_text(encoding="utf-8")
    except (IOError, UnicodeDecodeError):
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[3:end].strip())
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


def scan_lore_notes(vault: Path) -> list[dict]:
    """Walk the vault and collect all lore-eligible notes."""
    results = []
    if not vault.exists():
        log.warning(f"Vault not found: {vault}")
        return results

    for md_path in vault.rglob("*.md"):
        # Skip hidden and system folders
        if any(p.lower() in SKIP_FOLDERS for p in md_path.parts):
            continue
        if any(part.startswith(".") for part in md_path.parts):
            continue

        fm = read_frontmatter(md_path)
        if is_lore_note(md_path, fm):
            body = read_note_body(md_path)
            if len(body.strip()) > 80:  # Skip near-empty notes
                results.append({
                    "path":       md_path,
                    "key":        str(md_path.relative_to(vault)),
                    "frontmatter": fm or {},
                    "body":       body,
                    "title":      md_path.stem,
                })
    return results


# ─── INVENTORY READER ──────────────────────────────────────────────────────────

def fetch_inventory() -> list[dict]:
    """Pull current artifact list from M3RCH∆NT API."""
    try:
        r = requests.get(f"{MERCHANT_API}/merchant/artifacts", timeout=8)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass

    # Fallback: try direct import if running in same process
    try:
        from merchant import MerchantEngine
        return MerchantEngine().list_artifacts()
    except ImportError:
        pass

    log.warning("Cannot reach M3RCH∆NT API or import merchant module. Inventory empty.")
    return []


# ─── CROSS-REFERENCE ───────────────────────────────────────────────────────────

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_in_inventory(signal_name: str, inventory: list[dict]) -> Optional[dict]:
    """
    Fuzzy-match a signal name against the inventory.
    Returns the best-matching artifact if above threshold, else None.
    """
    best_score = 0.0
    best_match = None
    for artifact in inventory:
        score = max(
            similarity(signal_name, artifact.get("common_name", "")),
            similarity(signal_name, artifact.get("true_name",  "")),
        )
        if score > best_score:
            best_score = score
            best_match = artifact

    if best_score >= MATCH_THRESHOLD:
        return {**best_match, "_match_score": round(best_score, 3)}
    return None


# ─── DRAFT GENERATOR ───────────────────────────────────────────────────────────

def generate_draft_note(signal: dict, source_note: str) -> str:
    """
    Produce an Obsidian-ready artifact note with frontmatter.
    After review, drop this into the vault → vault_watcher syncs it.
    """
    name    = signal.get("name", "Unknown Artifact")
    el      = signal.get("element", "AETHER")
    atype   = signal.get("type", "RELIC")
    excerpt = signal.get("excerpt", "")

    true_name = f"∆∆∆ {name} ∆∆∆"
    soul      = f"Born of lore — the {name.lower()} that the story remembers."

    frontmatter = {
        "type":          "artifact",
        "true_name":     true_name,
        "common_name":   name,
        "artifact_type": atype,
        "element":       el,
        "pillar":        "07_SOCIAL_MOTHERSHIP",
        "soul_statement": soul,
        "anti_soul":     f"A {name.lower()} without memory — form without meaning.",
        "price_usd":     None,
        "platform":      "ETSY",
        "merchant_status": "DRAFT",
        "tags":          ["sacred art", name.lower(), el.lower()],
        "lore_source":   source_note,
        "lore_excerpt":  excerpt[:200],
        "auto_drafted":  datetime.now(timezone.utc).isoformat()[:10],
    }

    yaml_block = yaml.dump(
        frontmatter, allow_unicode=True,
        default_flow_style=False, sort_keys=False
    )

    return f"""---
{yaml_block.rstrip()}
---

# {name}

> *Lore source: {source_note}*
> *Excerpt: "{excerpt[:200]}"*

<!-- Add description, backstory, and product details below. -->
<!-- When ready: set merchant_status to FORGED and vault_watcher will sync. -->

## Lore Origin
{excerpt[:400]}

## Product Vision
<!-- Describe the physical artifact — size, materials, print specs, etc. -->

## Sacred Alignment
- Element: {el}
- Pillar: 07_SOCIAL_MOTHERSHIP
- Soul: {soul}
"""


# ─── CORE ENGINE ───────────────────────────────────────────────────────────────

class LoreProductEngine:

    def __init__(
        self,
        vault:       Path = VAULT_PATH,
        ollama_url:  str  = OLLAMA_URL,
        ollama_model:str  = OLLAMA_MODEL,
        merchant_api:str  = MERCHANT_API,
    ):
        self.vault        = vault
        self.ollama       = OllamaClient(ollama_url, ollama_model)
        self.merchant_api = merchant_api
        self._ollama_live: Optional[bool] = None

    def _check_ollama(self) -> bool:
        if self._ollama_live is None:
            self._ollama_live = self.ollama.is_reachable()
            if self._ollama_live:
                log.info(f"Ollama reachable at {OLLAMA_URL} — using LLM extraction.")
            else:
                log.warning(f"Ollama not reachable — falling back to keyword extraction.")
        return self._ollama_live

    def extract_signals(self, note: dict) -> list[dict]:
        """Extract artifact signals from a single lore note."""
        body   = note["body"]
        source = note["key"]

        if self._check_ollama():
            signals = self.ollama.extract_artifacts(body)
            for s in signals:
                s["source_note"]  = source
                s["method"]       = s.get("method", "ollama")
        else:
            signals = keyword_extract(body, source)
            for s in signals:
                s["source_note"] = source

        return signals

    def run_gap_analysis(self) -> dict:
        """
        Full pipeline:
        1. Scan vault for lore notes
        2. Extract artifact signals from each
        3. Cross-reference against M3RCH∆NT inventory
        4. Return gap report with auto-drafted notes
        """
        log.info("Starting Lore-to-Product gap analysis...")
        started = datetime.now(timezone.utc).isoformat()

        lore_notes = scan_lore_notes(self.vault)
        log.info(f"Found {len(lore_notes)} lore notes to scan.")

        inventory = fetch_inventory()
        log.info(f"Loaded {len(inventory)} existing artifacts from M3RCH∆NT.")

        all_signals = []
        for note in lore_notes:
            sigs = self.extract_signals(note)
            log.info(f"  {note['title'][:40]:<40} → {len(sigs)} signal(s)")
            all_signals.extend(sigs)

        # Deduplicate signals by name (case-insensitive)
        seen_names = {}
        unique_signals = []
        for sig in all_signals:
            key = sig["name"].lower().strip()
            if key not in seen_names:
                seen_names[key] = True
                unique_signals.append(sig)

        log.info(f"Total unique signals: {len(unique_signals)}")

        # Cross-reference
        gaps       = []
        confirmed  = []

        for sig in unique_signals:
            match = find_in_inventory(sig["name"], inventory)
            if match:
                confirmed.append({
                    "signal":       sig["name"],
                    "source_note":  sig.get("source_note", "?"),
                    "artifact_id":  match.get("artifact_id"),
                    "match_name":   match.get("common_name"),
                    "match_score":  match.get("_match_score"),
                    "state":        match.get("state"),
                })
            else:
                draft = generate_draft_note(sig, sig.get("source_note", "unknown"))
                gaps.append({
                    "signal":      sig["name"],
                    "source_note": sig.get("source_note", "?"),
                    "excerpt":     sig.get("excerpt", "")[:200],
                    "type":        sig.get("type", "RELIC"),
                    "element":     sig.get("element", "AETHER"),
                    "confidence":  sig.get("confidence", 0.5),
                    "method":      sig.get("method", "keyword_fallback"),
                    "draft_note":  draft,
                    "draft_filename": f"DRAFT_{sig['name'].replace(' ', '_')}.md",
                })

        # Sort gaps by confidence descending
        gaps.sort(key=lambda g: g["confidence"], reverse=True)

        report = {
            "system":           "LORE_PRODUCT_ENGINE",
            "pillar":           "07_SOCIAL_MOTHERSHIP + 09_SACRED_MARKET",
            "vault":            str(self.vault),
            "lore_notes_scanned": len(lore_notes),
            "total_signals":    len(unique_signals),
            "gaps_found":       len(gaps),
            "already_in_inventory": len(confirmed),
            "extraction_method": "ollama" if self._check_ollama() else "keyword_fallback",
            "gaps":             gaps,
            "confirmed":        confirmed,
            "started_at":       started,
            "completed_at":     datetime.now(timezone.utc).isoformat(),
        }

        log.info(
            f"Gap analysis complete: {len(gaps)} gaps, "
            f"{len(confirmed)} already in inventory."
        )
        return report

    def draft_to_vault(self, gap: dict, output_dir: Optional[Path] = None) -> Path:
        """
        Write a gap's draft_note to the vault as a .md file.
        Default target: Vault/LORE_DRAFTS/ folder.
        """
        target_dir = output_dir or (self.vault / "LORE_DRAFTS")
        target_dir.mkdir(parents=True, exist_ok=True)
        filename = gap.get("draft_filename", f"DRAFT_{gap['signal']}.md")
        filepath = target_dir / filename
        filepath.write_text(gap["draft_note"], encoding="utf-8")
        log.info(f"Draft written: {filepath}")
        return filepath


# ─── PYDANTIC MODELS ───────────────────────────────────────────────────────────

class WriteDraftsRequest(BaseModel):
    gap_indices: Optional[list[int]] = None  # None = write all gaps


# ─── FASTAPI ROUTER ────────────────────────────────────────────────────────────

router  = APIRouter(prefix="/lore-engine", tags=["LORE-TO-PRODUCT ENGINE"])
_engine: Optional[LoreProductEngine] = None
_last_report: Optional[dict] = None


def init_lore_engine(
    vault_path:   Path = VAULT_PATH,
    ollama_url:   str  = OLLAMA_URL,
    ollama_model: str  = OLLAMA_MODEL,
    merchant_api: str  = MERCHANT_API,
) -> LoreProductEngine:
    global _engine
    _engine = LoreProductEngine(vault_path, ollama_url, ollama_model, merchant_api)
    log.info("Lore-to-Product Engine initialized.")
    return _engine


@router.get("/status")
def lore_engine_status():
    """Engine status — vault path, Ollama reachability, last report summary."""
    if not _engine:
        return {"error": "Lore engine not initialized."}
    ollama_live = _engine.ollama.is_reachable()
    last = {}
    if _last_report:
        last = {
            "lore_notes_scanned":    _last_report["lore_notes_scanned"],
            "total_signals":         _last_report["total_signals"],
            "gaps_found":            _last_report["gaps_found"],
            "already_in_inventory":  _last_report["already_in_inventory"],
            "completed_at":          _last_report["completed_at"],
        }
    return {
        "system":           "LORE_PRODUCT_ENGINE",
        "vault":            str(_engine.vault),
        "vault_exists":     _engine.vault.exists(),
        "ollama_url":       OLLAMA_URL,
        "ollama_model":     OLLAMA_MODEL,
        "ollama_reachable": ollama_live,
        "extraction_mode":  "ollama" if ollama_live else "keyword_fallback",
        "merchant_api":     MERCHANT_API,
        "last_report":      last,
        "timestamp":        datetime.now(timezone.utc).isoformat(),
    }


@router.post("/scan")
def run_scan():
    """
    Run the full gap analysis pipeline.
    Scans lore notes → extracts signals → cross-references inventory → returns gap report.
    Stores the report for /gaps and /drafts endpoints.
    """
    global _last_report
    if not _engine:
        raise HTTPException(status_code=503, detail="Lore engine not initialized.")
    _last_report = _engine.run_gap_analysis()
    # Strip draft_note content from top-level response (can be large)
    summary = {**_last_report}
    summary["gaps"] = [
        {k: v for k, v in g.items() if k != "draft_note"}
        for g in _last_report["gaps"]
    ]
    return summary


@router.get("/gaps")
def get_gaps():
    """Return the gaps from the last scan (without draft note bodies)."""
    if not _last_report:
        raise HTTPException(status_code=404, detail="No scan run yet. POST /lore-engine/scan first.")
    return {
        "gaps_found": _last_report["gaps_found"],
        "gaps": [
            {k: v for k, v in g.items() if k != "draft_note"}
            for g in _last_report["gaps"]
        ],
    }


@router.get("/gaps/{index}/draft")
def get_draft(index: int):
    """Get the full draft Obsidian note for a specific gap (by index)."""
    if not _last_report:
        raise HTTPException(status_code=404, detail="No scan run yet.")
    gaps = _last_report["gaps"]
    if index < 0 or index >= len(gaps):
        raise HTTPException(status_code=404, detail=f"Gap index {index} out of range (0–{len(gaps)-1}).")
    g = gaps[index]
    return {
        "index":         index,
        "signal":        g["signal"],
        "draft_filename": g["draft_filename"],
        "draft_note":    g["draft_note"],
    }


@router.post("/gaps/write-drafts")
def write_drafts_to_vault(body: WriteDraftsRequest = WriteDraftsRequest()):
    """
    Write gap draft notes to VAULT/LORE_DRAFTS/ folder.
    vault_watcher will pick them up after you review and approve them.
    gap_indices=null writes all gaps. gap_indices=[0,2,4] writes selected.
    """
    if not _last_report:
        raise HTTPException(status_code=404, detail="No scan run yet.")
    if not _engine:
        raise HTTPException(status_code=503, detail="Engine not initialized.")

    gaps    = _last_report["gaps"]
    indices = body.gap_indices if body.gap_indices is not None else list(range(len(gaps)))
    written = []

    for i in indices:
        if 0 <= i < len(gaps):
            path = _engine.draft_to_vault(gaps[i])
            written.append({"index": i, "signal": gaps[i]["signal"], "path": str(path)})

    return {
        "written":    len(written),
        "target_dir": str(_engine.vault / "LORE_DRAFTS"),
        "files":      written,
    }


@router.get("/confirmed")
def get_confirmed():
    """Signals already in the merchant inventory (confirmed matches)."""
    if not _last_report:
        raise HTTPException(status_code=404, detail="No scan run yet.")
    return {
        "count":     _last_report["already_in_inventory"],
        "confirmed": _last_report["confirmed"],
    }


# ─── STANDALONE ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(
        description="SacredSpace Lore-to-Product Engine"
    )
    parser.add_argument("--vault",  default=str(VAULT_PATH))
    parser.add_argument("--ollama", default=OLLAMA_URL)
    parser.add_argument("--model",  default=OLLAMA_MODEL)
    parser.add_argument("--api",    default=MERCHANT_API)
    parser.add_argument(
        "--write-drafts",
        action="store_true",
        help="Write gap draft notes to VAULT/LORE_DRAFTS/ after scan."
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Save full gap report as JSON to this path."
    )
    args = parser.parse_args()

    engine = LoreProductEngine(
        vault        = Path(args.vault),
        ollama_url   = args.ollama,
        ollama_model = args.model,
        merchant_api = args.api,
    )

    report = engine.run_gap_analysis()

    print(f"\n{'═'*60}")
    print(f"  LORE-TO-PRODUCT GAP REPORT")
    print(f"{'═'*60}")
    print(f"  Lore notes scanned : {report['lore_notes_scanned']}")
    print(f"  Unique signals     : {report['total_signals']}")
    print(f"  Already in market  : {report['already_in_inventory']}")
    print(f"  GAPS FOUND         : {report['gaps_found']}")
    print(f"  Extraction method  : {report['extraction_method']}")
    print(f"{'═'*60}\n")

    for i, gap in enumerate(report["gaps"]):
        print(f"  [{i}] {gap['signal']:<30} "
              f"| {gap['type']:<12} | {gap['element']:<6} "
              f"| conf: {gap['confidence']:.2f} "
              f"| {gap['source_note']}")
    print()

    if report["gaps"] and args.write_drafts:
        print(f"Writing {len(report['gaps'])} draft notes to VAULT/LORE_DRAFTS/...")
        for gap in report["gaps"]:
            engine.draft_to_vault(gap)
        print("Done. Review drafts in Obsidian, then vault_watcher will sync them.")

    if args.output:
        out = Path(args.output)
        # Remove draft_note from JSON output to keep it lean
        lean = {
            **report,
            "gaps": [{k: v for k, v in g.items() if k != "draft_note"}
                     for g in report["gaps"]],
        }
        out.write_text(json.dumps(lean, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Report saved to {out}")

    sys.exit(0 if report["gaps_found"] >= 0 else 1)
