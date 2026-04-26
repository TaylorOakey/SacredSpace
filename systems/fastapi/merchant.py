"""
╔══════════════════════════════════════════════════════════════╗
║  M3RCH∆NT of S∆CR3D ∆RT1F∆CT$                               ║
║  SacredSpace OS · ECONOMY Pillar (04) + CREATION (06)        ║
║  Owner Agent: AURORA (inventory) + GR∆M∆ (gematria layer)   ║
║  System Tag: MERCHANT_ARTIFACT_MARKET                        ║
║  Status: Active                                              ║
╚══════════════════════════════════════════════════════════════╝

Sacred artifacts are not products. They are transmissions.
Each one carries an element, an archetype, a gematria pulse.
This system tracks them from forging to offering —
from the CREATION pillar out to the Sacred Market.

Platform targets: Etsy · Printify · Gelato · Sacred Space Market
"""

import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DB_PATH = Path("D:/SacredSpace_OS/05_MEMORY_ENGINE/merchant.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

PLATFORMS = ["ETSY", "PRINTIFY", "GELATO", "SACRED_MARKET", "INTERNAL"]
ELEMENTS  = ["FIRE", "WATER", "EARTH", "AIR", "AETHER"]
PILLARS   = [
    "CORE", "SYSTEMS", "LEARNING", "ECONOMY",
    "HABITAT", "CREATION", "COUNCIL", "LINEAGE", "ARCHIVE"
]
ARTIFACT_TYPES = [
    "PRINT",         # Wall art, poster, digital print
    "APPAREL",       # T-shirt, hoodie, hat
    "ACCESSORY",     # Sticker, pin, patch
    "JOURNAL",       # Sacred journal, notebook
    "CARD_DECK",     # Tarot or oracle deck
    "RELIC",         # Physical sacred object (handmade)
    "DIGITAL",       # Digital download, PDF, guide
    "BUNDLE",        # Multi-item sacred bundle
]
ARTIFACT_STATES = ["DRAFT", "FORGED", "LISTED", "ACTIVE", "ARCHIVED", "SEALED"]

# ─── GR∆M∆ GEMATRIA ENGINE (Mispar Hecrechi — English approximation) ──────────

# English letters mapped to Hebrew positional values
ORDINAL_VALUES = {
    'A': 1,  'B': 2,  'C': 3,  'D': 4,  'E': 5,
    'F': 6,  'G': 7,  'H': 8,  'I': 9,  'J': 10,
    'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15,
    'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20,
    'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
}

SOUL_TONES = {
    1:  {"title": "The Pioneer",        "shadow": "Isolation — the initiator who forgets to invite others."},
    2:  {"title": "The Bridge",         "shadow": "Codependence — peacemaking that erases the self."},
    3:  {"title": "The Creator",        "shadow": "Scattered expression — all spark, no vessel."},
    4:  {"title": "The Builder",        "shadow": "Rigidity — structure that refuses to breathe."},
    5:  {"title": "The Explorer",       "shadow": "Escapism — freedom that avoids the necessary."},
    6:  {"title": "The Nurturer",       "shadow": "Self-neglect — tending others at cost of self."},
    7:  {"title": "The Seeker",         "shadow": "Withdrawal — the mystic who never returns."},
    8:  {"title": "The Integrator",     "shadow": "Control — mistaking order for wisdom."},
    9:  {"title": "The Cycle Elder",    "shadow": "Martyrdom — wisdom weaponized as sacrifice."},
    11: {"title": "The Illuminator",    "shadow": "Nervous imbalance — channeling without grounding."},
    22: {"title": "The Master Builder", "shadow": "Overwhelm — vision too vast for the vessel."},
}


def calculate_gematria(word: str) -> dict:
    """
    Compute English Ordinal gematria for a word or phrase.
    Returns full breakdown, sum, soul tone, and interpretation.
    GR∆M∆ discipline: show the work.
    """
    clean = word.upper().replace(" ", "").replace("-", "").replace("'", "")
    breakdown = []
    total = 0

    for char in clean:
        val = ORDINAL_VALUES.get(char, 0)
        breakdown.append({"letter": char, "value": val})
        total += val

    # Reduce to soul tone (1–9, preserve 11 and 22)
    reduced = total
    while reduced > 9 and reduced not in (11, 22):
        reduced = sum(int(d) for d in str(reduced))

    soul = SOUL_TONES.get(reduced, SOUL_TONES[9])

    return {
        "word": word,
        "method": "English Ordinal (GR∆M∆ approximation)",
        "breakdown": breakdown,
        "total": total,
        "soul_tone": reduced,
        "soul_title": soul["title"],
        "soul_shadow": soul["shadow"],
        "note": "For Hebrew Mispar Hecrechi, transliterate word to Hebrew first."
    }


def generate_sigil(name: str, element: str, soul_tone: int) -> str:
    """
    Compose a Core Identity Sigil string for an artifact.
    Format: [element_glyph][name_root][soul_tone][seal]
    """
    element_glyphs = {
        "FIRE":   "🔥",
        "WATER":  "〜",
        "EARTH":  "◈",
        "AIR":    "≋",
        "AETHER": "✦",
    }
    glyph = element_glyphs.get(element.upper(), "∆")
    root = name.upper().replace(" ", "")[:4]  # first 4 chars
    return f"{glyph}{root}{soul_tone}∆"


# ─── DATABASE INIT ─────────────────────────────────────────────────────────────

def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_merchant_db():
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS artifacts (
            artifact_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            true_name     TEXT NOT NULL,
            common_name   TEXT NOT NULL,
            artifact_type TEXT NOT NULL,
            element       TEXT,
            pillar        TEXT,
            archetype     TEXT,
            soul_tone     INTEGER,
            sigil         TEXT,
            gematria_total INTEGER,
            description   TEXT,
            soul_statement TEXT,
            anti_soul     TEXT,
            price_usd     REAL,
            platform      TEXT,
            state         TEXT NOT NULL DEFAULT 'DRAFT',
            sku           TEXT,
            tags          TEXT,        -- JSON array
            created_at    TEXT,
            updated_at    TEXT,
            listed_at     TEXT,
            sealed_at     TEXT
        );

        CREATE TABLE IF NOT EXISTS listings (
            listing_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            artifact_id   INTEGER NOT NULL,
            platform      TEXT NOT NULL,
            listing_title TEXT,
            listing_body  TEXT,
            tags          TEXT,        -- JSON array of SEO tags
            status        TEXT NOT NULL DEFAULT 'DRAFT',
            created_at    TEXT,
            FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id)
        );
    """)
    conn.commit()
    conn.close()
    print("[M3RCH∆NT] The market is open. Sacred artifacts ready to forge.")


# ─── CORE ENGINE ───────────────────────────────────────────────────────────────

class MerchantEngine:
    """The M3RCH∆NT — forges, tracks, and lists sacred artifacts."""

    def create_artifact(
        self,
        true_name: str,
        common_name: str,
        artifact_type: str,
        element: Optional[str] = None,
        pillar: Optional[str] = None,
        archetype: Optional[str] = None,
        description: Optional[str] = None,
        soul_statement: Optional[str] = None,
        anti_soul: Optional[str] = None,
        price_usd: Optional[float] = None,
        platform: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> dict:
        """Forge a new sacred artifact into the registry."""
        if artifact_type.upper() not in ARTIFACT_TYPES:
            raise ValueError(f"Unknown artifact type: {artifact_type}. Valid: {ARTIFACT_TYPES}")

        # GR∆M∆ layer — auto-calculate gematria on true name
        gem = calculate_gematria(true_name)
        soul_tone = gem["soul_tone"]
        sigil = generate_sigil(true_name, element or "AETHER", soul_tone)

        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO artifacts
            (true_name, common_name, artifact_type, element, pillar, archetype,
             soul_tone, sigil, gematria_total, description, soul_statement, anti_soul,
             price_usd, platform, state, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DRAFT', ?, ?, ?)
        """, (
            true_name, common_name, artifact_type.upper(),
            element.upper() if element else None,
            pillar.upper() if pillar else None,
            archetype,
            soul_tone, sigil, gem["total"],
            description, soul_statement, anti_soul,
            price_usd,
            platform.upper() if platform else None,
            json.dumps(tags or []),
            now, now
        ))
        artifact_id = c.lastrowid
        conn.commit()
        conn.close()
        return self.get_artifact(artifact_id)

    def get_artifact(self, artifact_id: int) -> dict:
        conn = _get_conn()
        row = conn.execute(
            "SELECT * FROM artifacts WHERE artifact_id=?", (artifact_id,)
        ).fetchone()
        conn.close()
        if not row:
            return None
        artifact = dict(row)
        artifact["tags"] = json.loads(artifact["tags"] or "[]")
        return artifact

    def list_artifacts(
        self,
        state: Optional[str] = None,
        element: Optional[str] = None,
        pillar: Optional[str] = None,
        platform: Optional[str] = None,
    ) -> List[dict]:
        conn = _get_conn()
        query = "SELECT * FROM artifacts WHERE 1=1"
        params = []
        if state:
            query += " AND state=?"
            params.append(state.upper())
        if element:
            query += " AND element=?"
            params.append(element.upper())
        if pillar:
            query += " AND pillar=?"
            params.append(pillar.upper())
        if platform:
            query += " AND platform=?"
            params.append(platform.upper())
        query += " ORDER BY artifact_id DESC"
        rows = conn.execute(query, params).fetchall()
        conn.close()
        result = []
        for row in rows:
            a = dict(row)
            a["tags"] = json.loads(a["tags"] or "[]")
            result.append(a)
        return result

    def advance_artifact(self, artifact_id: int, notes: Optional[str] = None) -> dict:
        """Move artifact one step forward: DRAFT → FORGED → LISTED → ACTIVE → ARCHIVED."""
        artifact = self.get_artifact(artifact_id)
        if not artifact:
            raise ValueError(f"Artifact ID {artifact_id} not found.")
        current_idx = ARTIFACT_STATES.index(artifact["state"])
        if current_idx >= len(ARTIFACT_STATES) - 1:
            return {"status": "already_sealed", "artifact": artifact}

        next_state = ARTIFACT_STATES[current_idx + 1]
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        extra = ""
        params = [next_state, now]
        if next_state == "LISTED":
            extra = ", listed_at=?"
            params.append(now)
        elif next_state == "SEALED":
            extra = ", sealed_at=?"
            params.append(now)
        params.append(artifact_id)
        conn.execute(
            f"UPDATE artifacts SET state=?, updated_at=?{extra} WHERE artifact_id=?",
            params
        )
        conn.commit()
        conn.close()
        return {
            "status": "advanced",
            "from_state": artifact["state"],
            "to_state": next_state,
            "artifact": self.get_artifact(artifact_id)
        }

    def generate_listing(self, artifact_id: int, platform: Optional[str] = None) -> dict:
        """
        Generate a platform-ready listing for an artifact.
        Produces title, body copy, and SEO tags ready to paste into Etsy/Printify/etc.
        """
        artifact = self.get_artifact(artifact_id)
        if not artifact:
            raise ValueError(f"Artifact ID {artifact_id} not found.")

        plat = (platform or artifact.get("platform") or "ETSY").upper()

        # Build the listing
        title = f"{artifact['common_name']} | {artifact['artifact_type'].title()} | Sacred Space"

        soul_line = artifact.get("soul_statement") or \
            f"A {artifact['element'] or 'sacred'}-aligned artifact from the SacredSpace universe."

        body = f"""{title}

✦ {soul_line}

────────────────────────────────
ABOUT THIS ARTIFACT
────────────────────────────────
True Name: {artifact['true_name']}
Element: {artifact['element'] or 'Aether'}
Pillar: {artifact['pillar'] or 'CREATION'}
Archetype: {artifact['archetype'] or 'The Seeker'}
Soul Tone: {artifact['soul_tone']} — {SOUL_TONES.get(artifact['soul_tone'] or 9, SOUL_TONES[9])['title']}
Sigil: {artifact['sigil']}

────────────────────────────────
DESCRIPTION
────────────────────────────────
{artifact.get('description') or 'A living artifact from the SacredSpace universe.'}

────────────────────────────────
SACREDSPACE UNIVERSE
────────────────────────────────
Every piece from SacredSpace carries an intention. This artifact is part
of the CREATION pillar — where art, narrative, and sacred geometry become
offerings rather than products.

"Ground. Consolidate. Deploy. Document. Repeat."
∆∆∆O∆K3YTREE∆∆∆ · In lakesh alakin.
"""

        seo_tags = (artifact.get("tags") or []) + [
            "sacred art", "spiritual print", "sacred geometry",
            "mystical art", artifact.get("element", "aether").lower(),
            "sacredspace", "gematria art", "ancestral wisdom",
        ]

        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO listings (artifact_id, platform, listing_title, listing_body, tags, status, created_at)
            VALUES (?, ?, ?, ?, ?, 'DRAFT', ?)
        """, (artifact_id, plat, title, body, json.dumps(seo_tags[:13]), now))
        listing_id = c.lastrowid
        conn.commit()

        listing = dict(c.execute(
            "SELECT * FROM listings WHERE listing_id=?", (listing_id,)
        ).fetchone())
        listing["tags"] = json.loads(listing["tags"] or "[]")
        conn.close()
        return {"listing": listing, "artifact": artifact}

    def get_market_summary(self) -> dict:
        """Full market status — the merchant's ledger."""
        conn = _get_conn()
        total = conn.execute("SELECT COUNT(*) FROM artifacts").fetchone()[0]
        by_state = {}
        for s in ARTIFACT_STATES:
            by_state[s] = conn.execute(
                "SELECT COUNT(*) FROM artifacts WHERE state=?", (s,)
            ).fetchone()[0]
        by_element = {}
        for e in ELEMENTS:
            count = conn.execute(
                "SELECT COUNT(*) FROM artifacts WHERE element=?", (e,)
            ).fetchone()[0]
            if count:
                by_element[e] = count
        total_listings = conn.execute("SELECT COUNT(*) FROM listings").fetchone()[0]
        conn.close()
        return {
            "system": "MERCHANT_ARTIFACT_MARKET",
            "pillar": "ECONOMY (04) + CREATION (06)",
            "total_artifacts": total,
            "by_state": by_state,
            "by_element": by_element,
            "total_listings_generated": total_listings,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# ─── PYDANTIC MODELS ───────────────────────────────────────────────────────────

class CreateArtifactRequest(BaseModel):
    true_name: str
    common_name: str
    artifact_type: str
    element: Optional[str] = None
    pillar: Optional[str] = None
    archetype: Optional[str] = None
    description: Optional[str] = None
    soul_statement: Optional[str] = None
    anti_soul: Optional[str] = None
    price_usd: Optional[float] = None
    platform: Optional[str] = None
    tags: Optional[List[str]] = None

class AdvanceArtifactRequest(BaseModel):
    notes: Optional[str] = None

class GenerateListingRequest(BaseModel):
    platform: Optional[str] = None


# ─── FASTAPI ROUTER ────────────────────────────────────────────────────────────

router = APIRouter(prefix="/merchant", tags=["M3RCH∆NT — Sacred Artifacts"])
engine = MerchantEngine()


@router.get("/status")
def market_status():
    """The merchant's ledger — full market summary."""
    return engine.get_market_summary()


@router.get("/artifacts")
def list_artifacts(
    state: Optional[str] = None,
    element: Optional[str] = None,
    pillar: Optional[str] = None,
    platform: Optional[str] = None,
):
    """List all artifacts. Filter by state, element, pillar, or platform."""
    return engine.list_artifacts(state=state, element=element, pillar=pillar, platform=platform)


@router.post("/artifacts")
def forge_artifact(body: CreateArtifactRequest):
    """
    Forge a new sacred artifact into the registry.
    GR∆M∆ gematria is calculated automatically from true_name.
    """
    try:
        return engine.create_artifact(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/artifacts/{artifact_id}")
def get_artifact(artifact_id: int):
    artifact = engine.get_artifact(artifact_id)
    if not artifact:
        raise HTTPException(status_code=404, detail=f"Artifact {artifact_id} not found.")
    return artifact


@router.post("/artifacts/{artifact_id}/advance")
def advance_artifact(artifact_id: int, body: AdvanceArtifactRequest = AdvanceArtifactRequest()):
    """Advance artifact state: DRAFT → FORGED → LISTED → ACTIVE → ARCHIVED → SEALED."""
    try:
        return engine.advance_artifact(artifact_id, body.notes)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/artifacts/{artifact_id}/listing")
def generate_listing(artifact_id: int, body: GenerateListingRequest = GenerateListingRequest()):
    """Generate a platform-ready listing (title, body, SEO tags) for an artifact."""
    try:
        return engine.generate_listing(artifact_id, body.platform)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/gematria/{word}")
def gematria_decode(word: str):
    """
    Run GR∆M∆'s gematria engine on any word or phrase.
    Returns full breakdown, soul tone, and interpretation.
    """
    return calculate_gematria(word)


@router.get("/sigil")
def build_sigil(name: str, element: str = "AETHER"):
    """Generate a Core Identity Sigil string for any name + element."""
    gem = calculate_gematria(name)
    sigil = generate_sigil(name, element, gem["soul_tone"])
    return {
        "name": name,
        "element": element,
        "soul_tone": gem["soul_tone"],
        "sigil": sigil,
        "gematria": gem,
    }


# ─── STANDALONE ENTRYPOINT ─────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI(title="M3RCH∆NT of S∆CR3D ∆RT1F∆CT$", version="1.0.0")
    init_merchant_db()
    app.include_router(router)

    print("[M3RCH∆NT] The market is open. Forging at port 8888.")
    uvicorn.run(app, host="0.0.0.0", port=8888)
