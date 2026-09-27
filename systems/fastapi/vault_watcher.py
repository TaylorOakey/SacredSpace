"""
╔══════════════════════════════════════════════════════════════╗
║  VAULT WATCHER — Obsidian → M3RCH∆NT Sync Bridge            ║
║  SacredSpace OS · SYSTEMS Pillar (02)                        ║
║  Owner Agent: AURORA (bridge/sync)                           ║
║  System Tag: VAULT_WATCHER_SYNC                              ║
║  Status: Active                                              ║
╚══════════════════════════════════════════════════════════════╝

Watches the Obsidian vault for .md files tagged with:
    type: artifact

When a matching file is created or updated, it reads the YAML
frontmatter and syncs the artifact to M3RCH∆NT via HTTP.

Two modes:
  --once   : scan the vault once and exit (good for cron)
  --watch  : run continuously, react to file changes (default)

Also mounts a FastAPI router at /vault-watcher for status + manual trigger.

─── OBSIDIAN FRONTMATTER SCHEMA ──────────────────────────────
Add this to the top of any .md note you want synced:

    ---
    type: artifact
    true_name: ∆∆∆ The Forest Lantern ∆∆∆
    common_name: Forest Lantern Print
    artifact_type: PRINT
    element: EARTH
    pillar: CREATION
    archetype: The Forest Guardian
    soul_statement: A lamp that remembers what the dark forgot.
    anti_soul: Decoration without warmth — light without memory.
    price_usd: 24.99
    platform: ETSY
    tags:
      - sacred art
      - forest lantern
      - earth element
    merchant_status: DRAFT
    ---

artifact_type options: PRINT | APPAREL | ACCESSORY | JOURNAL |
                        CARD_DECK | RELIC | DIGITAL | BUNDLE
element options:        FIRE | WATER | EARTH | AIR | AETHER
pillar options:         CORE | SYSTEMS | LEARNING | ECONOMY |
                        HABITAT | CREATION | COUNCIL | LINEAGE | ARCHIVE
platform options:       ETSY | PRINTIFY | GELATO | SACRED_MARKET | INTERNAL
merchant_status:        DRAFT | FORGED | LISTED | ACTIVE | ARCHIVED
──────────────────────────────────────────────────────────────
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

import yaml
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent

from fastapi import APIRouter
from pydantic import BaseModel

# ─── CONFIG ────────────────────────────────────────────────────────────────────

# Vault path — set for Windows or WSL2
# Windows native:  D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault
# WSL2:            /mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault
VAULT_PATH = Path(
    os.environ.get(
        "SACREDSPACE_VAULT",
        r"D:\SacredSpace_OS\01_OBSIDIAN_VAULTS\SacredSpace_Vault"
    )
)

# Where the sync ledger lives (tracks file → artifact_id mappings)
LEDGER_PATH = Path(
    os.environ.get(
        "SACREDSPACE_LEDGER",
        r"D:\SacredSpace_OS\05_MEMORY_ENGINE\vault_sync_ledger.json"
    )
)

# M3RCH∆NT API base URL
MERCHANT_API = os.environ.get("MERCHANT_API", "http://localhost:8888")

# Tag in frontmatter that triggers sync
SYNC_TAG = "artifact"

# Debounce seconds — prevents double-firing on rapid saves
DEBOUNCE_SECONDS = 2.0

# ─── LOGGING ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="[VAULT WATCHER] %(asctime)s — %(levelname)s — %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("vault_watcher")


# ─── SYNC LEDGER ───────────────────────────────────────────────────────────────

class SyncLedger:
    """
    Tracks which Obsidian files have been synced to M3RCH∆NT.
    Stored as JSON: { "relative/path/to/note.md": { "artifact_id": 7, "synced_at": "..." } }
    """

    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._data: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if self.path.exists():
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except (json.JSONDecodeError, IOError):
                log.warning("Ledger corrupt or missing — starting fresh.")
                self._data = {}

    def _save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def get(self, file_key: str) -> Optional[dict]:
        return self._data.get(file_key)

    def record(self, file_key: str, artifact_id: int):
        self._data[file_key] = {
            "artifact_id": artifact_id,
            "synced_at": datetime.now(timezone.utc).isoformat(),
            "file_key": file_key,
        }
        self._save()

    def remove(self, file_key: str):
        if file_key in self._data:
            del self._data[file_key]
            self._save()

    def all_entries(self) -> dict:
        return dict(self._data)

    def total(self) -> int:
        return len(self._data)


# ─── FRONTMATTER PARSER ────────────────────────────────────────────────────────

def parse_frontmatter(md_path: Path) -> Optional[dict]:
    """
    Read a .md file and extract its YAML frontmatter block (--- ... ---).
    Returns the parsed dict, or None if no valid frontmatter found.
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except (IOError, UnicodeDecodeError) as e:
        log.warning(f"Cannot read {md_path.name}: {e}")
        return None

    if not text.startswith("---"):
        return None

    # Find closing ---
    end = text.find("\n---", 3)
    if end == -1:
        return None

    raw_yaml = text[3:end].strip()
    try:
        data = yaml.safe_load(raw_yaml)
        return data if isinstance(data, dict) else None
    except yaml.YAMLError as e:
        log.warning(f"YAML parse error in {md_path.name}: {e}")
        return None


def is_artifact_note(frontmatter: Optional[dict]) -> bool:
    """Check if the frontmatter marks this file as a syncable artifact."""
    if not frontmatter:
        return False
    return str(frontmatter.get("type", "")).lower() == SYNC_TAG


def frontmatter_to_payload(fm: dict, file_key: str) -> dict:
    """
    Map Obsidian frontmatter fields to M3RCH∆NT CreateArtifactRequest fields.
    Tolerant — missing fields get defaults rather than errors.
    """
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",")]

    return {
        "true_name":      str(fm.get("true_name", fm.get("name", file_key))),
        "common_name":    str(fm.get("common_name", fm.get("name", file_key))),
        "artifact_type":  str(fm.get("artifact_type", "PRINT")).upper(),
        "element":        str(fm.get("element", "AETHER")).upper() if fm.get("element") else None,
        "pillar":         str(fm.get("pillar", "CREATION")).upper() if fm.get("pillar") else None,
        "archetype":      fm.get("archetype"),
        "description":    fm.get("description"),
        "soul_statement": fm.get("soul_statement"),
        "anti_soul":      fm.get("anti_soul"),
        "price_usd":      float(fm["price_usd"]) if fm.get("price_usd") else None,
        "platform":       str(fm.get("platform", "ETSY")).upper() if fm.get("platform") else None,
        "tags":           [str(t) for t in tags] if tags else [],
    }


# ─── MERCHANT HTTP CLIENT ──────────────────────────────────────────────────────

class MerchantClient:
    """Thin HTTP wrapper around the M3RCH∆NT FastAPI endpoints."""

    def __init__(self, base_url: str):
        self.base = base_url.rstrip("/")

    def ping(self) -> bool:
        try:
            r = requests.get(f"{self.base}/merchant/status", timeout=5)
            return r.status_code == 200
        except requests.RequestException:
            return False

    def create_artifact(self, payload: dict) -> Optional[dict]:
        try:
            r = requests.post(
                f"{self.base}/merchant/artifacts",
                json=payload,
                timeout=10,
            )
            if r.status_code == 200:
                return r.json()
            log.error(f"CREATE failed ({r.status_code}): {r.text[:200]}")
            return None
        except requests.RequestException as e:
            log.error(f"CREATE request error: {e}")
            return None

    def get_artifact(self, artifact_id: int) -> Optional[dict]:
        try:
            r = requests.get(
                f"{self.base}/merchant/artifacts/{artifact_id}",
                timeout=5,
            )
            return r.json() if r.status_code == 200 else None
        except requests.RequestException:
            return None

    def advance_artifact(self, artifact_id: int, target_state: str) -> Optional[dict]:
        """
        Advance an artifact until it reaches target_state.
        M3RCH∆NT only advances one step at a time.
        """
        state_order = ["DRAFT", "FORGED", "LISTED", "ACTIVE", "ARCHIVED", "SEALED"]
        artifact = self.get_artifact(artifact_id)
        if not artifact:
            return None

        current = artifact["state"]
        if current == target_state:
            return artifact

        target_idx = state_order.index(target_state) if target_state in state_order else 0
        current_idx = state_order.index(current) if current in state_order else 0

        if target_idx <= current_idx:
            return artifact  # already at or past target

        # Step forward once (one step per sync to avoid runaway advancement)
        try:
            r = requests.post(
                f"{self.base}/merchant/artifacts/{artifact_id}/advance",
                json={"notes": f"Vault watcher sync — target state: {target_state}"},
                timeout=10,
            )
            return r.json() if r.status_code == 200 else artifact
        except requests.RequestException as e:
            log.error(f"ADVANCE error: {e}")
            return artifact


# ─── CORE SYNC ENGINE ──────────────────────────────────────────────────────────

class VaultSyncEngine:
    """
    Orchestrates the sync between the Obsidian vault and M3RCH∆NT.
    Used by both the watcher daemon and the one-shot scan.
    """

    def __init__(self, vault: Path, ledger: SyncLedger, client: MerchantClient):
        self.vault = vault
        self.ledger = ledger
        self.client = client
        self._last_processed: Dict[str, float] = {}  # debounce tracker

    def file_key(self, md_path: Path) -> str:
        """Relative path from vault root — stable identifier for ledger."""
        try:
            return str(md_path.relative_to(self.vault))
        except ValueError:
            return str(md_path)

    def _debounced(self, md_path: Path) -> bool:
        """True if file was processed too recently (debounce guard)."""
        key = str(md_path)
        now = time.time()
        last = self._last_processed.get(key, 0)
        if now - last < DEBOUNCE_SECONDS:
            return True
        self._last_processed[key] = now
        return False

    def sync_file(self, md_path: Path) -> dict:
        """
        Sync a single .md file to M3RCH∆NT.
        Returns a result dict with status and details.
        """
        if self._debounced(md_path):
            return {"status": "debounced", "file": md_path.name}

        fm = parse_frontmatter(md_path)
        if not is_artifact_note(fm):
            return {"status": "skipped", "file": md_path.name, "reason": "not tagged type: artifact"}

        key = self.file_key(md_path)
        payload = frontmatter_to_payload(fm, key)
        existing = self.ledger.get(key)

        if existing:
            # Already synced — check if we need to advance state
            artifact_id = existing["artifact_id"]
            target_state = str(fm.get("merchant_status", "DRAFT")).upper()
            result = self.client.advance_artifact(artifact_id, target_state)
            if result:
                log.info(f"↺ UPDATED  {md_path.name} → artifact #{artifact_id} (state: {result.get('state', '?')})")
                return {"status": "updated", "artifact_id": artifact_id, "file": md_path.name}
            return {"status": "update_failed", "file": md_path.name}
        else:
            # New artifact — create it
            if not self.client.ping():
                log.error("M3RCH∆NT API is not reachable. Is the server running on port 8888?")
                return {"status": "api_unreachable", "file": md_path.name}

            result = self.client.create_artifact(payload)
            if result:
                artifact_id = result["artifact_id"]
                self.ledger.record(key, artifact_id)
                # Advance to requested state if not DRAFT
                target_state = str(fm.get("merchant_status", "DRAFT")).upper()
                if target_state != "DRAFT":
                    self.client.advance_artifact(artifact_id, target_state)
                log.info(f"✦ FORGED   {md_path.name} → artifact #{artifact_id} ({result.get('common_name')})")
                return {"status": "created", "artifact_id": artifact_id, "file": md_path.name}
            return {"status": "create_failed", "file": md_path.name}

    def scan_vault(self) -> dict:
        """
        One-shot scan — walk the entire vault and sync all artifact notes.
        Returns a summary of what happened.
        """
        if not self.vault.exists():
            log.error(f"Vault not found: {self.vault}")
            return {"error": f"Vault path not found: {self.vault}"}

        log.info(f"Scanning vault: {self.vault}")
        results = {"created": [], "updated": [], "skipped": [], "failed": []}
        total_md = 0

        for md_path in self.vault.rglob("*.md"):
            # Skip hidden/system files
            if any(part.startswith(".") for part in md_path.parts):
                continue
            total_md += 1
            result = self.sync_file(md_path)
            status = result.get("status", "unknown")
            if status in ("created",):
                results["created"].append(result)
            elif status in ("updated",):
                results["updated"].append(result)
            elif status in ("skipped", "debounced"):
                results["skipped"].append(result["file"])
            else:
                results["failed"].append(result)

        summary = {
            "vault": str(self.vault),
            "total_md_files": total_md,
            "created": len(results["created"]),
            "updated": len(results["updated"]),
            "skipped": len(results["skipped"]),
            "failed": len(results["failed"]),
            "ledger_total": self.ledger.total(),
            "details": {k: v for k, v in results.items() if k != "skipped"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        log.info(
            f"Scan complete: {summary['created']} forged, "
            f"{summary['updated']} updated, "
            f"{summary['failed']} failed, "
            f"{summary['skipped']} skipped."
        )
        return summary


# ─── WATCHDOG EVENT HANDLER ────────────────────────────────────────────────────

class VaultEventHandler(FileSystemEventHandler):
    """Watchdog handler — fires on file create or modify events."""

    def __init__(self, engine: VaultSyncEngine):
        super().__init__()
        self.engine = engine

    def _handle(self, event):
        path = Path(event.src_path)
        if path.suffix.lower() != ".md":
            return
        if any(part.startswith(".") for part in path.parts):
            return
        log.info(f"Change detected: {path.name}")
        self.engine.sync_file(path)

    def on_created(self, event):
        if not event.is_directory:
            self._handle(event)

    def on_modified(self, event):
        if not event.is_directory:
            self._handle(event)


# ─── FASTAPI ROUTER ────────────────────────────────────────────────────────────

router = APIRouter(prefix="/vault-watcher", tags=["VAULT WATCHER — Obsidian Sync"])

# Module-level engine instance (initialized on startup)
_engine: Optional[VaultSyncEngine] = None


def init_vault_watcher(
    vault_path: Path = VAULT_PATH,
    ledger_path: Path = LEDGER_PATH,
    api_url: str = MERCHANT_API,
) -> VaultSyncEngine:
    global _engine
    ledger = SyncLedger(ledger_path)
    client = MerchantClient(api_url)
    _engine = VaultSyncEngine(vault_path, ledger, client)
    log.info(f"Vault Watcher initialized. Vault: {vault_path}")
    return _engine


@router.get("/status")
def watcher_status():
    """Vault watcher status — ledger size, vault path, API reachability."""
    engine = _engine
    if not engine:
        return {"error": "Vault watcher not initialized."}
    return {
        "system": "VAULT_WATCHER_SYNC",
        "vault": str(engine.vault),
        "vault_exists": engine.vault.exists(),
        "ledger_path": str(engine.ledger.path),
        "ledger_entries": engine.ledger.total(),
        "merchant_api": MERCHANT_API,
        "merchant_reachable": engine.client.ping(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@router.post("/scan")
def trigger_scan():
    """Manually trigger a full vault scan and sync."""
    if not _engine:
        from fastapi import HTTPException
        raise HTTPException(status_code=503, detail="Vault watcher not initialized.")
    return _engine.scan_vault()


@router.get("/ledger")
def view_ledger():
    """View the full sync ledger — all file → artifact_id mappings."""
    if not _engine:
        return {"error": "Not initialized."}
    return {"ledger": _engine.ledger.all_entries(), "total": _engine.ledger.total()}


def trigger_harvest() -> dict:
    """Run a full vault scan in the background. Called by POST /harvest."""
    if not _engine:
        return {"error": "Vault watcher not initialized."}
    return _engine.scan_vault()


# ─── DAEMON MODE ───────────────────────────────────────────────────────────────

def run_watcher_daemon(engine: VaultSyncEngine):
    """
    Run the vault watcher as a continuous daemon.
    Performs initial scan on startup, then watches for file changes.
    Press Ctrl+C to stop.
    """
    if not engine.vault.exists():
        log.error(f"Vault path not found: {engine.vault}")
        log.error("Set SACREDSPACE_VAULT env var or edit VAULT_PATH in this file.")
        sys.exit(1)

    if not engine.client.ping():
        log.warning("M3RCH∆NT API not reachable at startup. Will retry on each sync.")
        log.warning(f"Expected: {MERCHANT_API}/merchant/status")

    # Initial full scan
    log.info("Running initial vault scan...")
    engine.scan_vault()

    # Start watchdog observer
    handler = VaultEventHandler(engine)
    observer = Observer()
    observer.schedule(handler, str(engine.vault), recursive=True)
    observer.start()
    log.info(f"Watching vault for changes: {engine.vault}")
    log.info("Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        log.info("Vault watcher stopped.")
    observer.join()


# ─── STANDALONE ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="SacredSpace Vault Watcher — Obsidian → M3RCH∆NT sync bridge"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Scan the vault once and exit (good for cron/Task Scheduler).",
    )
    parser.add_argument(
        "--vault",
        type=str,
        default=str(VAULT_PATH),
        help=f"Path to the Obsidian vault. Default: {VAULT_PATH}",
    )
    parser.add_argument(
        "--ledger",
        type=str,
        default=str(LEDGER_PATH),
        help=f"Path to the sync ledger JSON. Default: {LEDGER_PATH}",
    )
    parser.add_argument(
        "--api",
        type=str,
        default=MERCHANT_API,
        help=f"M3RCH∆NT API base URL. Default: {MERCHANT_API}",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print ledger status and exit.",
    )
    args = parser.parse_args()

    engine = init_vault_watcher(
        vault_path=Path(args.vault),
        ledger_path=Path(args.ledger),
        api_url=args.api,
    )

    if args.status:
        ledger_entries = engine.ledger.all_entries()
        print(f"\nVault:   {engine.vault}")
        print(f"Exists:  {engine.vault.exists()}")
        print(f"API:     {args.api} ({'reachable' if engine.client.ping() else 'NOT reachable'})")
        print(f"Ledger:  {engine.ledger.total()} entries")
        if ledger_entries:
            print("\nSynced artifacts:")
            for key, val in ledger_entries.items():
                print(f"  #{val['artifact_id']:>4}  {key}  (synced {val['synced_at'][:10]})")
        sys.exit(0)

    if args.once:
        summary = engine.scan_vault()
        print(json.dumps(summary, indent=2))
        sys.exit(0)

    # Default: daemon mode
    run_watcher_daemon(engine)
