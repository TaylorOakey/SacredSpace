"""
╔══════════════════════════════════════════════════════════════╗
║  KETHRAS — The Learning Gate                                 ║
║  SacredSpace OS · LEARNING Pillar (03)                       ║
║  Owner Agent: IRIS (vault) + ELIAS (knowledge)               ║
║  System Tag: KETHRAS_LEARN_GATE                              ║
║  Status: Active                                              ║
╚══════════════════════════════════════════════════════════════╝

Tracks spell progression through the SACREDCODEX, rites completion,
and grove status across the Neural Forest / Maestro AAS pathway.

Every learning moment is a threshold crossed.
The gate keeps the record. The seeker keeps the key.
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, asdict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DB_PATH = Path("/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/kethras.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Spell progression states — in order of advancement
SPELL_STATES = ["PENDING", "ACTIVE", "PRACTICED", "CANONIZED", "SEALED"]

# Known SACREDCODEX spell IDs (expandable)
KNOWN_SPELLS = {
    # Canonized (Season 1)
    "PY-STR-001": {"name": "The String Weave",       "grove": "Grove_01_Strings",   "season": 1},
    "PY-STR-002": {"name": "The Format Ritual",       "grove": "Grove_01_Strings",   "season": 1},
    "PY-LST-003": {"name": "The List Construct",      "grove": "Grove_02_Lists",     "season": 1},
    "PY-LST-004": {"name": "The Loop Invocation",     "grove": "Grove_02_Lists",     "season": 1},
    "PY-DCT-005": {"name": "The Dict Cipher",         "grove": "Grove_03_Dicts",     "season": 1},
    "PY-DCT-006": {"name": "The Key-Value Seal",      "grove": "Grove_03_Dicts",     "season": 1},
    "PY-FNC-007": {"name": "The Function Forge",      "grove": "Grove_04_Functions", "season": 1},
    "PY-MOD-008": {"name": "The Module Gate",         "grove": "Grove_04_Functions", "season": 1},
    # Pending canonization (Season 2 — advanced)
    "PY-OOP-009": {"name": "The Class Construct",     "grove": "Grove_05_Objects",   "season": 2},
    "PY-OOP-010": {"name": "The Inheritance Chain",   "grove": "Grove_05_Objects",   "season": 2},
    "PY-OOP-011": {"name": "The Method Bind",         "grove": "Grove_05_Objects",   "season": 2},
    "PY-OOP-012": {"name": "The Dunder Rite",         "grove": "Grove_05_Objects",   "season": 2},
    "PY-ERR-013": {"name": "The Exception Ward",      "grove": "Grove_06_Errors",    "season": 2},
    "PY-ERR-014": {"name": "The Try-Catch Sigil",     "grove": "Grove_06_Errors",    "season": 2},
    "PY-IO-015":  {"name": "The File Portal",         "grove": "Grove_06_Errors",    "season": 2},
    "PY-THREAD-016": {"name": "The Thread Weave",     "grove": "Grove_06_Errors",    "season": 2},
}

KNOWN_RITES = [
    "RITE_OF_ARRIVAL",       # Session-start ritual completion
    "RITE_OF_NAMING",        # First canonical name assigned
    "RITE_OF_FIRST_SPELL",   # First spell practiced
    "RITE_OF_GROVE_CLEAR",   # First grove completed (all spells canonized)
    "RITE_OF_SEASON_SEAL",   # Full season canonized
    "RITE_OF_COUNCIL",       # First Council Grove session completed
    "RITE_OF_LINEAGE",       # First Sacred Message sent
]

KNOWN_GROVES = [
    "Grove_01_Strings",
    "Grove_02_Lists",
    "Grove_03_Dicts",
    "Grove_04_Functions",
    "Grove_05_Objects",
    "Grove_06_Errors",
]


# ─── DATABASE INIT ─────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_kethras_db():
    """Create KETHRAS tables and seed known spells/rites/groves if empty."""
    conn = _get_conn()
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS spells (
            spell_id    TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            grove       TEXT NOT NULL,
            season      INTEGER NOT NULL,
            state       TEXT NOT NULL DEFAULT 'PENDING',
            notes       TEXT,
            activated_at  TEXT,
            canonized_at  TEXT,
            updated_at    TEXT
        );

        CREATE TABLE IF NOT EXISTS rites (
            rite_id     INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            completed   INTEGER NOT NULL DEFAULT 0,
            completed_at TEXT,
            notes       TEXT
        );

        CREATE TABLE IF NOT EXISTS groves (
            grove_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL UNIQUE,
            total_spells  INTEGER NOT NULL DEFAULT 0,
            canonized_count INTEGER NOT NULL DEFAULT 0,
            cleared     INTEGER NOT NULL DEFAULT 0,
            cleared_at  TEXT
        );
    """)

    # Seed spells if table is empty
    existing = c.execute("SELECT COUNT(*) FROM spells").fetchone()[0]
    if existing == 0:
        now = datetime.now(timezone.utc).isoformat()
        for spell_id, meta in KNOWN_SPELLS.items():
            # Season 1 spells start as CANONIZED; Season 2 start as PENDING
            state = "CANONIZED" if meta["season"] == 1 else "PENDING"
            canonized_at = now if state == "CANONIZED" else None
            c.execute("""
                INSERT INTO spells (spell_id, name, grove, season, state, canonized_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (spell_id, meta["name"], meta["grove"], meta["season"],
                  state, canonized_at, now))

    # Seed rites if empty
    existing_rites = c.execute("SELECT COUNT(*) FROM rites").fetchone()[0]
    if existing_rites == 0:
        for rite in KNOWN_RITES:
            c.execute("INSERT INTO rites (name) VALUES (?)", (rite,))

    # Seed groves if empty
    existing_groves = c.execute("SELECT COUNT(*) FROM groves").fetchone()[0]
    if existing_groves == 0:
        for grove in KNOWN_GROVES:
            spells_in_grove = sum(
                1 for m in KNOWN_SPELLS.values() if m["grove"] == grove
            )
            c.execute("""
                INSERT INTO groves (name, total_spells) VALUES (?, ?)
            """, (grove, spells_in_grove))

    conn.commit()
    conn.close()
    _sync_grove_counts()
    print("[KETHRAS] Database initialized. The gate is open.")


def _sync_grove_counts():
    """Recalculate canonized_count and cleared status for all groves."""
    conn = _get_conn()
    c = conn.cursor()
    groves = c.execute("SELECT name FROM groves").fetchall()
    now = datetime.now(timezone.utc).isoformat()
    for g in groves:
        grove_name = g["name"]
        canon_count = c.execute(
            "SELECT COUNT(*) FROM spells WHERE grove=? AND state='CANONIZED'",
            (grove_name,)
        ).fetchone()[0]
        total = c.execute(
            "SELECT total_spells FROM groves WHERE name=?",
            (grove_name,)
        ).fetchone()[0]
        cleared = 1 if (total > 0 and canon_count >= total) else 0
        cleared_at = now if cleared else None
        c.execute("""
            UPDATE groves
            SET canonized_count=?, cleared=?, cleared_at=?
            WHERE name=?
        """, (canon_count, cleared, cleared_at, grove_name))
    conn.commit()
    conn.close()


# ─── CORE ENGINE ───────────────────────────────────────────────────────────────

class KethrasEngine:
    """The Learning Gate — reads, advances, and seals spell progression."""

    # ── Spells ─────────────────────────────────────────────────────────────────

    def get_all_spells(self, season: Optional[int] = None, state: Optional[str] = None):
        conn = _get_conn()
        c = conn.cursor()
        query = "SELECT * FROM spells WHERE 1=1"
        params = []
        if season:
            query += " AND season=?"
            params.append(season)
        if state:
            query += " AND state=?"
            params.append(state.upper())
        query += " ORDER BY spell_id"
        rows = c.execute(query, params).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_spell(self, spell_id: str):
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM spells WHERE spell_id=?", (spell_id.upper(),)
        ).fetchone()
        conn.close()
        if not row:
            return None
        return dict(row)

    def advance_spell(self, spell_id: str, notes: Optional[str] = None) -> dict:
        """Move a spell one step forward in the progression chain."""
        spell = self.get_spell(spell_id)
        if not spell:
            raise ValueError(f"Spell '{spell_id}' not found in SACREDCODEX.")

        current_idx = SPELL_STATES.index(spell["state"])
        if current_idx >= len(SPELL_STATES) - 1:
            return {"status": "already_sealed", "spell": spell}

        next_state = SPELL_STATES[current_idx + 1]
        now = datetime.now(timezone.utc).isoformat()

        conn = _get_conn()
        c = conn.cursor()
        update_fields = "state=?, updated_at=?"
        params = [next_state, now]

        if next_state == "ACTIVE":
            update_fields += ", activated_at=?"
            params.append(now)
        elif next_state == "CANONIZED":
            update_fields += ", canonized_at=?"
            params.append(now)

        if notes:
            update_fields += ", notes=?"
            params.append(notes)

        params.append(spell_id.upper())
        c.execute(f"UPDATE spells SET {update_fields} WHERE spell_id=?", params)
        conn.commit()
        conn.close()
        _sync_grove_counts()

        updated = self.get_spell(spell_id)
        return {
            "status": "advanced",
            "from_state": spell["state"],
            "to_state": next_state,
            "spell": updated
        }

    def pending_canonization(self):
        """Return all spells in ACTIVE or PRACTICED state — ready to advance."""
        return self.get_all_spells(state=None)  # filter below
    
    def get_pending(self):
        return self.get_all_spells(state="PENDING")

    def get_active(self):
        return self.get_all_spells(state="ACTIVE")

    # ── Rites ──────────────────────────────────────────────────────────────────

    def get_all_rites(self):
        conn = _get_conn()
        rows = conn.execute("SELECT * FROM rites ORDER BY rite_id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def complete_rite(self, rite_name: str, notes: Optional[str] = None) -> dict:
        conn = _get_conn()
        c = conn.cursor()
        row = c.execute(
            "SELECT * FROM rites WHERE name=?", (rite_name.upper(),)
        ).fetchone()
        if not row:
            conn.close()
            raise ValueError(f"Rite '{rite_name}' not recognized.")
        if row["completed"]:
            conn.close()
            return {"status": "already_complete", "rite": dict(row)}

        now = datetime.now(timezone.utc).isoformat()
        c.execute("""
            UPDATE rites SET completed=1, completed_at=?, notes=? WHERE name=?
        """, (now, notes, rite_name.upper()))
        conn.commit()
        updated = dict(c.execute(
            "SELECT * FROM rites WHERE name=?", (rite_name.upper(),)
        ).fetchone())
        conn.close()
        return {"status": "rite_completed", "rite": updated}

    # ── Groves ─────────────────────────────────────────────────────────────────

    def get_all_groves(self):
        conn = _get_conn()
        rows = conn.execute("SELECT * FROM groves ORDER BY grove_id").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_grove(self, grove_name: str):
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM groves WHERE name=?", (grove_name,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    # ── Status Summary ─────────────────────────────────────────────────────────

    def get_status(self) -> dict:
        """Full KETHRAS status — the gate reading."""
        spells = self.get_all_spells()
        rites = self.get_all_rites()
        groves = self.get_all_groves()

        by_state = {}
        for s in SPELL_STATES:
            by_state[s] = sum(1 for sp in spells if sp["state"] == s)

        return {
            "system": "KETHRAS_LEARN_GATE",
            "pillar": "LEARNING (03)",
            "total_spells": len(spells),
            "spells_by_state": by_state,
            "rites_completed": sum(1 for r in rites if r["completed"]),
            "rites_total": len(rites),
            "groves_cleared": sum(1 for g in groves if g["cleared"]),
            "groves_total": len(groves),
            "season_1_complete": all(
                sp["state"] == "CANONIZED" or sp["state"] == "SEALED"
                for sp in spells if sp["season"] == 1
            ),
            "next_threshold": next(
                (sp["spell_id"] for sp in spells if sp["state"] == "PENDING"), None
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ─── PYDANTIC MODELS ───────────────────────────────────────────────────────────

class AdvanceSpellRequest(BaseModel):
    notes: Optional[str] = None

class CompleteRiteRequest(BaseModel):
    notes: Optional[str] = None


# ─── FASTAPI ROUTER ────────────────────────────────────────────────────────────

router = APIRouter(prefix="/kethras", tags=["KETHRAS — Learning Gate"])
engine = KethrasEngine()


@router.get("/status")
def kethras_status():
    """Full gate status — spell counts, rites, grove progress."""
    return engine.get_status()


@router.get("/spells")
def list_spells(season: Optional[int] = None, state: Optional[str] = None):
    """List all spells. Filter by season (1 or 2) or state (PENDING, ACTIVE, etc)."""
    return engine.get_all_spells(season=season, state=state)


@router.get("/spells/pending")
def list_pending():
    """All spells awaiting activation — the unsealed gates."""
    return engine.get_pending()


@router.get("/spells/active")
def list_active():
    """All spells currently in practice."""
    return engine.get_active()


@router.get("/spells/{spell_id}")
def get_spell(spell_id: str):
    spell = engine.get_spell(spell_id)
    if not spell:
        raise HTTPException(status_code=404, detail=f"Spell '{spell_id}' not found.")
    return spell


@router.post("/spells/{spell_id}/advance")
def advance_spell(spell_id: str, body: AdvanceSpellRequest = AdvanceSpellRequest()):
    """Advance a spell one step: PENDING → ACTIVE → PRACTICED → CANONIZED → SEALED."""
    try:
        return engine.advance_spell(spell_id, body.notes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/rites")
def list_rites():
    """All rites and their completion status."""
    return engine.get_all_rites()


@router.post("/rites/{rite_name}/complete")
def complete_rite(rite_name: str, body: CompleteRiteRequest = CompleteRiteRequest()):
    """Mark a rite as completed."""
    try:
        return engine.complete_rite(rite_name, body.notes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/groves")
def list_groves():
    """All Neural Forest groves and their canonization progress."""
    return engine.get_all_groves()


@router.get("/groves/{grove_name}")
def get_grove(grove_name: str):
    grove = engine.get_grove(grove_name)
    if not grove:
        raise HTTPException(status_code=404, detail=f"Grove '{grove_name}' not found.")
    spells = engine.get_all_spells()
    grove_spells = [s for s in spells if s["grove"] == grove_name]
    return {"grove": grove, "spells": grove_spells}


# ─── STANDALONE ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI(title="KETHRAS — Learning Gate", version="1.0.0")
    init_kethras_db()
    app.include_router(router)

    print("[KETHRAS] The gate is open. Listening on port 8888.")
    uvicorn.run(app, host="0.0.0.0", port=8888)
