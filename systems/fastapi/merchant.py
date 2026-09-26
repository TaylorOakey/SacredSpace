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
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# ─── CONFIG ────────────────────────────────────────────────────────────────────

DB_PATH = Path("/mnt/d/SacredSpace_OS/05_MEMORY_ENGINE/merchant.db")
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

# ─── GR∆M∆ GEMATRIA ENGINE (English Ordinal, A=1 … Z=26) ─────────────────────

# Plain English ordinal values. Hebrew Mispar Hechrachi needs transliteration first.
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


def _check_enum(value: str, allowed: List[str], field: str) -> str:
    v = value.upper()
    if v not in allowed:
        raise ValueError(f"Unknown {field}: {value}. Valid: {allowed}")
    return v


def _check_date(value: str, field: str) -> str:
    try:
        return date.fromisoformat(value).isoformat()
    except (TypeError, ValueError):
        raise ValueError(f"{field} must be YYYY-MM-DD, got {value!r}")


VAAS_STATUSES = ["PROSPECT", "ONBOARDING", "ACTIVE", "PAUSED", "CHURNED"]

# Every ledger/grant row is tagged with the entity it belongs to, so business,
# nonprofit and household money never share a bucket. SOLE_PROP is the starting
# entity; LLC and NONPROFIT exist for when (if) those are formed.
ENTITIES = ["SOLE_PROP", "LLC", "NONPROFIT", "PERSONAL", "FISCAL_SPONSOR"]
COMMERCIAL_ENTITIES = ("SOLE_PROP", "LLC")
SALE_CHANNELS = [
    "ETSY", "SHOPIFY", "KOFI", "REDBUBBLE", "TEEPUBLIC",
    "PRINTIFY", "GELATO", "PRINTFUL", "KICKSTARTER",
    "VAAS", "WHOLESALE", "DIRECT", "OTHER",
]
SALE_KINDS = ["PRODUCT", "SERVICE", "DONATION", "REFUND"]
GRANT_STATUSES = [
    "RESEARCH", "ELIGIBLE", "DRAFTING", "SUBMITTED",
    "AWARDED", "DECLINED", "WITHDRAWN", "CLOSED",
]
FIRST_FLAME_TARGET_USD = 1111.0   # cumulative PRODUCT net, after platform fees + COGS
# Money out that isn't tied to a single sale (per-sale fees/COGS live on the sale row).
EXPENSE_CATEGORIES = [
    "PLATFORM",      # Etsy listing renewals, Ko-fi Gold, Shopify plan
    "SOFTWARE",      # Canva, domains, hosting
    "SAMPLES",       # test prints / proof copies
    "SUPPLIES",      # plant stock, packaging, art materials
    "MARKETING",     # ads, printed cards
    "LEGAL_FILING",  # LLC, annual report, trademark
    "EQUIPMENT",
    "OTHER",
]


def init_merchant_db():
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS vaas_clients (
            client_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name             TEXT NOT NULL,
            email            TEXT,
            vault_name       TEXT NOT NULL,
            setup_fee        REAL DEFAULT 5000.0,
            monthly_retainer REAL DEFAULT 500.0,
            status           TEXT NOT NULL DEFAULT 'PROSPECT',
            months_active    INTEGER DEFAULT 0,
            notes            TEXT,
            deployed_at      TEXT,
            last_invoice     TEXT,
            created_at       TEXT DEFAULT (datetime('now'))
        );

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

        -- Append-only money ledger. Corrections are REFUND rows, not edits.
        CREATE TABLE IF NOT EXISTS sales (
            sale_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date      TEXT NOT NULL,          -- YYYY-MM-DD
            entity         TEXT NOT NULL,          -- ENTITIES
            channel        TEXT NOT NULL,          -- SALE_CHANNELS
            kind           TEXT NOT NULL DEFAULT 'PRODUCT',
            artifact_id    INTEGER,
            client_id      INTEGER,
            description    TEXT,
            quantity       INTEGER NOT NULL DEFAULT 1,
            gross_usd      REAL NOT NULL,          -- what the customer paid (negative for REFUND)
            fees_usd       REAL NOT NULL DEFAULT 0, -- platform + payment processing + ads
            cogs_usd       REAL NOT NULL DEFAULT 0, -- fulfillment / print / shipping cost
            net_usd        REAL NOT NULL,          -- gross - fees - cogs
            external_ref   TEXT,                   -- platform order id
            notes          TEXT,
            created_at     TEXT NOT NULL,
            FOREIGN KEY (artifact_id) REFERENCES artifacts(artifact_id),
            FOREIGN KEY (client_id)   REFERENCES vaas_clients(client_id)
        );
        CREATE UNIQUE INDEX IF NOT EXISTS idx_sales_channel_ref
            ON sales(channel, external_ref) WHERE external_ref IS NOT NULL;
        CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);

        CREATE TABLE IF NOT EXISTS grants (
            grant_id         INTEGER PRIMARY KEY AUTOINCREMENT,
            funder           TEXT NOT NULL,
            program          TEXT,
            applicant_entity TEXT NOT NULL,        -- ENTITIES
            status           TEXT NOT NULL DEFAULT 'RESEARCH',
            amount_requested REAL,
            amount_awarded   REAL,
            deadline         TEXT,                 -- YYYY-MM-DD
            url              TEXT,
            eligibility      TEXT,
            notes            TEXT,
            submitted_at     TEXT,
            decided_at       TEXT,
            created_at       TEXT NOT NULL,
            updated_at       TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_grants_deadline ON grants(deadline);

        CREATE TABLE IF NOT EXISTS expenses (
            expense_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date  TEXT NOT NULL,           -- YYYY-MM-DD
            entity        TEXT NOT NULL,           -- ENTITIES
            category      TEXT NOT NULL,           -- EXPENSE_CATEGORIES
            vendor        TEXT,
            description   TEXT,
            amount_usd    REAL NOT NULL,           -- always positive
            notes         TEXT,
            created_at    TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_expenses_date ON expenses(expense_date);
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

    def get_vaas_clients(self, status: Optional[str] = None) -> dict:
        """VaaS client registry + revenue summary."""
        conn = _get_conn()
        q = "SELECT * FROM vaas_clients"
        params = []
        if status:
            q += " WHERE status=?"
            params.append(status.upper())
        q += " ORDER BY client_id DESC"
        rows = conn.execute(q, params).fetchall()

        clients = [dict(r) for r in rows]
        active = [c for c in clients if c["status"] == "ACTIVE"]
        mrr = sum(c["monthly_retainer"] for c in active)
        setup_total = sum(c["setup_fee"] for c in clients if c["status"] != "PROSPECT")
        arr = mrr * 12

        conn.close()
        return {
            "service":          "Vault-as-a-Service (VaaS)",
            "model":            "$5,000 setup · $500/mo retainer",
            "pillar":           "09_SACRED_MARKET",
            "clients":          clients,
            "summary": {
                "total":        len(clients),
                "active":       len(active),
                "prospects":    sum(1 for c in clients if c["status"] == "PROSPECT"),
                "mrr_usd":      round(mrr, 2),
                "arr_usd":      round(arr, 2),
                "setup_revenue": round(setup_total, 2),
                "ltv_estimate": round(setup_total + arr, 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def add_vaas_client(
        self,
        name: str,
        vault_name: str,
        email: Optional[str] = None,
        setup_fee: float = 5000.0,
        monthly_retainer: float = 500.0,
        notes: Optional[str] = None,
    ) -> dict:
        """Register a new VaaS client."""
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO vaas_clients
            (name, email, vault_name, setup_fee, monthly_retainer, status, notes, created_at)
            VALUES (?,?,?,?,?,'PROSPECT',?,?)
        """, (name, email, vault_name, setup_fee, monthly_retainer, notes, now))
        client_id = c.lastrowid
        conn.commit()
        row = dict(conn.execute("SELECT * FROM vaas_clients WHERE client_id=?", (client_id,)).fetchone())
        conn.close()
        return row

    # ─── SALES LEDGER ──────────────────────────────────────────────────────────

    def record_sale(
        self,
        sale_date: str,
        entity: str,
        channel: str,
        gross_usd: float,
        kind: str = "PRODUCT",
        fees_usd: float = 0.0,
        cogs_usd: float = 0.0,
        quantity: int = 1,
        artifact_id: Optional[int] = None,
        client_id: Optional[int] = None,
        description: Optional[str] = None,
        external_ref: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """Append one sale to the ledger. Net is computed, never entered."""
        sale_date = _check_date(sale_date, "sale_date")
        entity = _check_enum(entity, ENTITIES, "entity")
        channel = _check_enum(channel, SALE_CHANNELS, "channel")
        kind = _check_enum(kind, SALE_KINDS, "kind")
        if kind == "REFUND":
            if gross_usd > 0:
                raise ValueError("REFUND rows carry a negative (or zero) gross_usd.")
        elif gross_usd < 0:
            raise ValueError("gross_usd must be >= 0; record reversals as kind=REFUND.")
        if fees_usd < 0 or cogs_usd < 0:
            raise ValueError("fees_usd and cogs_usd are costs and must be >= 0.")
        if quantity < 1:
            raise ValueError("quantity must be >= 1.")

        net = round(gross_usd - fees_usd - cogs_usd, 2)
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        try:
            if artifact_id is not None and not conn.execute(
                "SELECT 1 FROM artifacts WHERE artifact_id=?", (artifact_id,)
            ).fetchone():
                raise ValueError(f"Artifact ID {artifact_id} not found.")
            if client_id is not None and not conn.execute(
                "SELECT 1 FROM vaas_clients WHERE client_id=?", (client_id,)
            ).fetchone():
                raise ValueError(f"VaaS client ID {client_id} not found.")
            c = conn.cursor()
            try:
                c.execute("""
                    INSERT INTO sales
                    (sale_date, entity, channel, kind, artifact_id, client_id, description,
                     quantity, gross_usd, fees_usd, cogs_usd, net_usd, external_ref, notes, created_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    sale_date, entity, channel, kind, artifact_id, client_id, description,
                    quantity, round(gross_usd, 2), round(fees_usd, 2), round(cogs_usd, 2),
                    net, external_ref, notes, now,
                ))
            except sqlite3.IntegrityError:
                # Release the write lock now; close() alone defers it while the
                # failed statement is still referenced by the traceback.
                conn.rollback()
                c.close()
                raise ValueError(f"{channel} order {external_ref} is already in the ledger.") from None
            conn.commit()
            return dict(conn.execute(
                "SELECT * FROM sales WHERE sale_id=?", (c.lastrowid,)
            ).fetchone())
        finally:
            conn.close()

    def get_ledger(
        self,
        entity: Optional[str] = None,
        channel: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
    ) -> dict:
        """Sales rows + totals by entity, channel and month, plus First Flame progress."""
        q = "SELECT * FROM sales WHERE 1=1"
        params = []
        if entity:
            q += " AND entity=?"
            params.append(_check_enum(entity, ENTITIES, "entity"))
        if channel:
            q += " AND channel=?"
            params.append(_check_enum(channel, SALE_CHANNELS, "channel"))
        if since:
            q += " AND sale_date>=?"
            params.append(_check_date(since, "since"))
        if until:
            q += " AND sale_date<=?"
            params.append(_check_date(until, "until"))
        q += " ORDER BY sale_date DESC, sale_id DESC"
        conn = _get_conn()
        rows = [dict(r) for r in conn.execute(q, params).fetchall()]
        # First Flame is all-time, independent of the filters above.
        flame_net = conn.execute(
            "SELECT COALESCE(SUM(net_usd), 0) FROM sales "
            "WHERE entity IN (?, ?) AND kind IN ('PRODUCT', 'REFUND')",
            COMMERCIAL_ENTITIES,
        ).fetchone()[0]
        # Expenses share the entity/date filters; channel doesn't apply to them.
        eq = "SELECT * FROM expenses WHERE 1=1"
        eparams = []
        if entity:
            eq += " AND entity=?"
            eparams.append(_check_enum(entity, ENTITIES, "entity"))
        if since:
            eq += " AND expense_date>=?"
            eparams.append(_check_date(since, "since"))
        if until:
            eq += " AND expense_date<=?"
            eparams.append(_check_date(until, "until"))
        expenses = [dict(r) for r in conn.execute(eq, eparams).fetchall()]
        conn.close()

        def _bucket(key: str) -> dict:
            out = {}
            for r in rows:
                b = out.setdefault(r[key], {"count": 0, "gross_usd": 0.0, "net_usd": 0.0})
                b["count"] += 1
                b["gross_usd"] = round(b["gross_usd"] + r["gross_usd"], 2)
                b["net_usd"] = round(b["net_usd"] + r["net_usd"], 2)
            return out

        for r in rows:
            r["month"] = r["sale_date"][:7]
        by_month = _bucket("month")
        for r in rows:
            del r["month"]

        return {
            "system": "MERCHANT_LEDGER",
            "pillar": "09_SACRED_MARKET",
            "sales": rows,
            "totals": {
                "count":     len(rows),
                "gross_usd": round(sum(r["gross_usd"] for r in rows), 2),
                "fees_usd":  round(sum(r["fees_usd"] for r in rows), 2),
                "cogs_usd":  round(sum(r["cogs_usd"] for r in rows), 2),
                "net_usd":   round(sum(r["net_usd"] for r in rows), 2),
            },
            "by_entity":  _bucket("entity"),
            "by_channel": _bucket("channel"),
            "by_month":   dict(sorted(by_month.items())),
            "expenses": {
                "count":       len(expenses),
                "total_usd":   round(sum(e["amount_usd"] for e in expenses), 2),
                "by_category": {
                    c: round(sum(e["amount_usd"] for e in expenses if e["category"] == c), 2)
                    for c in sorted({e["category"] for e in expenses})
                },
            },
            # Channel-filtered views exclude expenses, so a cash position there would mislead.
            "cash_position_usd": None if channel else round(
                sum(r["net_usd"] for r in rows) - sum(e["amount_usd"] for e in expenses), 2
            ),
            "first_flame": {
                "definition": "Cumulative SOLE_PROP + LLC product net (PRODUCT + REFUND rows), after per-sale fees and COGS",
                "target_usd": FIRST_FLAME_TARGET_USD,
                "net_usd":    round(flame_net, 2),
                "progress":   round(min(flame_net / FIRST_FLAME_TARGET_USD, 1.0), 4),
                "ignited":    flame_net >= FIRST_FLAME_TARGET_USD,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ─── EXPENSES ──────────────────────────────────────────────────────────────

    def record_expense(
        self,
        expense_date: str,
        entity: str,
        category: str,
        amount_usd: float,
        vendor: Optional[str] = None,
        description: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """Append one expense (money out not tied to a single sale)."""
        expense_date = _check_date(expense_date, "expense_date")
        entity = _check_enum(entity, ENTITIES, "entity")
        category = _check_enum(category, EXPENSE_CATEGORIES, "category")
        if amount_usd <= 0:
            raise ValueError("amount_usd must be > 0.")
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO expenses
            (expense_date, entity, category, vendor, description, amount_usd, notes, created_at)
            VALUES (?,?,?,?,?,?,?,?)
        """, (expense_date, entity, category, vendor, description, round(amount_usd, 2), notes, now))
        conn.commit()
        row = dict(conn.execute("SELECT * FROM expenses WHERE expense_id=?", (c.lastrowid,)).fetchone())
        conn.close()
        return row

    def list_expenses(self, entity: Optional[str] = None, category: Optional[str] = None) -> List[dict]:
        q = "SELECT * FROM expenses WHERE 1=1"
        params = []
        if entity:
            q += " AND entity=?"
            params.append(_check_enum(entity, ENTITIES, "entity"))
        if category:
            q += " AND category=?"
            params.append(_check_enum(category, EXPENSE_CATEGORIES, "category"))
        q += " ORDER BY expense_date DESC, expense_id DESC"
        conn = _get_conn()
        rows = [dict(r) for r in conn.execute(q, params).fetchall()]
        conn.close()
        return rows

    # ─── GRANT PIPELINE ────────────────────────────────────────────────────────

    def add_grant(
        self,
        funder: str,
        applicant_entity: str,
        program: Optional[str] = None,
        amount_requested: Optional[float] = None,
        deadline: Optional[str] = None,
        url: Optional[str] = None,
        eligibility: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """Add a grant opportunity to the pipeline at RESEARCH."""
        applicant_entity = _check_enum(applicant_entity, ENTITIES, "applicant_entity")
        if deadline:
            deadline = _check_date(deadline, "deadline")
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        c = conn.cursor()
        c.execute("""
            INSERT INTO grants
            (funder, program, applicant_entity, status, amount_requested, deadline,
             url, eligibility, notes, created_at, updated_at)
            VALUES (?,?,?,'RESEARCH',?,?,?,?,?,?,?)
        """, (funder, program, applicant_entity, amount_requested, deadline,
              url, eligibility, notes, now, now))
        conn.commit()
        row = dict(conn.execute("SELECT * FROM grants WHERE grant_id=?", (c.lastrowid,)).fetchone())
        conn.close()
        return row

    def update_grant_status(
        self,
        grant_id: int,
        status: str,
        amount_awarded: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """Move a grant to any pipeline status; stamps submitted_at / decided_at."""
        status = _check_enum(status, GRANT_STATUSES, "status")
        if amount_awarded is not None and status != "AWARDED":
            raise ValueError("amount_awarded can only be set with status=AWARDED.")
        now = datetime.now(timezone.utc).isoformat()
        conn = _get_conn()
        row = conn.execute("SELECT * FROM grants WHERE grant_id=?", (grant_id,)).fetchone()
        if not row:
            conn.close()
            raise LookupError(f"Grant ID {grant_id} not found.")
        sets = ["status=?", "updated_at=?"]
        params: list = [status, now]
        if status == "SUBMITTED" and not row["submitted_at"]:
            sets.append("submitted_at=?")
            params.append(now)
        if status in ("AWARDED", "DECLINED") and not row["decided_at"]:
            sets.append("decided_at=?")
            params.append(now)
        if amount_awarded is not None:
            sets.append("amount_awarded=?")
            params.append(amount_awarded)
        if notes:
            sets.append("notes=?")
            params.append(f"{row['notes']}\n{notes}" if row["notes"] else notes)
        params.append(grant_id)
        conn.execute(f"UPDATE grants SET {', '.join(sets)} WHERE grant_id=?", params)
        conn.commit()
        updated = dict(conn.execute("SELECT * FROM grants WHERE grant_id=?", (grant_id,)).fetchone())
        conn.close()
        return {"status": "updated", "from_status": row["status"], "grant": updated}

    def get_grants(
        self,
        status: Optional[str] = None,
        entity: Optional[str] = None,
        due_within_days: int = 30,
    ) -> dict:
        """Grant pipeline with counts by status and open deadlines coming up."""
        q = "SELECT * FROM grants WHERE 1=1"
        params = []
        if status:
            q += " AND status=?"
            params.append(_check_enum(status, GRANT_STATUSES, "status"))
        if entity:
            q += " AND applicant_entity=?"
            params.append(_check_enum(entity, ENTITIES, "entity"))
        q += " ORDER BY deadline IS NULL, deadline, grant_id"
        conn = _get_conn()
        grants = [dict(r) for r in conn.execute(q, params).fetchall()]
        conn.close()

        today = datetime.now(timezone.utc).date()
        horizon = (today + timedelta(days=due_within_days)).isoformat()
        open_states = ("RESEARCH", "ELIGIBLE", "DRAFTING")
        upcoming = [
            g for g in grants
            if g["status"] in open_states and g["deadline"]
            and today.isoformat() <= g["deadline"] <= horizon
        ]
        return {
            "system": "MERCHANT_GRANT_PIPELINE",
            "pillar": "09_SACRED_MARKET",
            "grants": grants,
            "summary": {
                "total":          len(grants),
                "by_status":      {s: sum(1 for g in grants if g["status"] == s) for s in GRANT_STATUSES},
                "requested_open_usd": round(sum(
                    g["amount_requested"] or 0 for g in grants
                    if g["status"] in open_states + ("SUBMITTED",)), 2),
                "awarded_usd":    round(sum(g["amount_awarded"] or 0 for g in grants), 2),
                "due_within_days": due_within_days,
                "upcoming_deadlines": upcoming,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

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

class AddVaasClientRequest(BaseModel):
    name: str
    vault_name: str
    email: Optional[str] = None
    setup_fee: float = 5000.0
    monthly_retainer: float = 500.0
    notes: Optional[str] = None

class RecordSaleRequest(BaseModel):
    sale_date: str
    entity: str
    channel: str
    gross_usd: float
    kind: str = "PRODUCT"
    fees_usd: float = 0.0
    cogs_usd: float = 0.0
    quantity: int = 1
    artifact_id: Optional[int] = None
    client_id: Optional[int] = None
    description: Optional[str] = None
    external_ref: Optional[str] = None
    notes: Optional[str] = None

class RecordExpenseRequest(BaseModel):
    expense_date: str
    entity: str
    category: str
    amount_usd: float
    vendor: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class AddGrantRequest(BaseModel):
    funder: str
    applicant_entity: str
    program: Optional[str] = None
    amount_requested: Optional[float] = None
    deadline: Optional[str] = None
    url: Optional[str] = None
    eligibility: Optional[str] = None
    notes: Optional[str] = None

class UpdateGrantStatusRequest(BaseModel):
    status: str
    amount_awarded: Optional[float] = None
    notes: Optional[str] = None


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


@router.get("/vaas")
def vaas_clients(status: Optional[str] = None):
    """
    VaaS — Vault-as-a-Service client registry.
    $5,000 setup + $500/mo retainer model.
    Filter by status: PROSPECT | ONBOARDING | ACTIVE | PAUSED | CHURNED
    """
    return engine.get_vaas_clients(status=status)


@router.post("/vaas")
def add_vaas_client(body: AddVaasClientRequest):
    """Register a new VaaS client prospect."""
    return engine.add_vaas_client(**body.model_dump())


@router.get("/ledger")
def sales_ledger(
    entity: Optional[str] = None,
    channel: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
):
    """
    Sales ledger with totals by entity, channel and month, plus First Flame progress.
    Filter by entity (SOLE_PROP | LLC | NONPROFIT | PERSONAL | FISCAL_SPONSOR), channel, and
    since/until dates (YYYY-MM-DD).
    """
    try:
        return engine.get_ledger(entity=entity, channel=channel, since=since, until=until)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/ledger")
def record_sale(body: RecordSaleRequest):
    """
    Append a sale. net_usd = gross_usd - fees_usd - cogs_usd.
    Append-only: record reversals as kind=REFUND with a negative gross_usd.
    external_ref (platform order id) is unique per channel to block double entry.
    """
    try:
        return engine.record_sale(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/expenses")
def list_expenses(entity: Optional[str] = None, category: Optional[str] = None):
    """List expenses. Filter by entity or category."""
    try:
        return engine.list_expenses(entity=entity, category=category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/expenses")
def record_expense(body: RecordExpenseRequest):
    """
    Record money out that isn't tied to one sale (per-sale fees and COGS go on
    the sale row). Categories: PLATFORM | SOFTWARE | SAMPLES | SUPPLIES |
    MARKETING | LEGAL_FILING | EQUIPMENT | OTHER
    """
    try:
        return engine.record_expense(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/grants")
def grant_pipeline(
    status: Optional[str] = None,
    entity: Optional[str] = None,
    due_within_days: int = 30,
):
    """
    Grant pipeline: every opportunity, counts by status, and open deadlines
    due within `due_within_days`.
    """
    try:
        return engine.get_grants(status=status, entity=entity, due_within_days=due_within_days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/grants")
def add_grant(body: AddGrantRequest):
    """Add a grant opportunity (starts at RESEARCH)."""
    try:
        return engine.add_grant(**body.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/grants/{grant_id}/status")
def update_grant_status(grant_id: int, body: UpdateGrantStatusRequest):
    """
    Move a grant: RESEARCH → ELIGIBLE → DRAFTING → SUBMITTED →
    AWARDED | DECLINED | WITHDRAWN | CLOSED.
    """
    try:
        return engine.update_grant_status(grant_id, **body.model_dump())
    except LookupError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


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
