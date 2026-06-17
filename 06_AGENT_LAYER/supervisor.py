"""
Supervisor Kernel — Canonical session management, injection filtering,
self-healing turn repair, and audit logging.
This is the governance layer: AI reasoning is a managed infrastructure resource.
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings

log = logging.getLogger(__name__)

# ── Injection patterns (expanded) ─────────────────────────────────────────────
_INJECTION_RE = re.compile(
    r"ignore\s+(all\s+)?previous\s+instructions"
    r"|you\s+are\s+now\s+(a|an)\b"
    r"|\bsystem\s+prompt\b"
    r"|\bdeveloper\s+message\b"
    r"|disregard\s+(all\s+)?(prior|previous)"
    r"|forget\s+(everything|all)"
    r"|act\s+as\s+if\s+you\s+are"
    r"|pretend\s+you\s+are",
    re.IGNORECASE,
)


def _canon_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def scan_injection(text_in: str) -> tuple[str, bool]:
    """Return (cleaned_text, injection_detected)."""
    detected = bool(_INJECTION_RE.search(text_in))
    cleaned = _INJECTION_RE.sub("[FILTERED]", text_in)
    return cleaned, detected


class SupervisorKernel:
    """
    Mediates all AI session state. Enforces Canon Lock invariants.
    All session mutations flow through here.
    """

    # ── Session lifecycle ─────────────────────────────────────────────────────
    async def create_session(
        self,
        db: AsyncSession,
        session_id: str,
        user_id: str,
        model_id: str,
        thinking_level: str = "medium",
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        q = text("""
            INSERT INTO sacred_sessions
              (session_id, user_id, model_id, thinking_level, temperature,
               canon_version, updated_at)
            VALUES
              (:session_id, :user_id, :model_id, :thinking_level, :temperature,
               :canon_version, NOW())
            ON CONFLICT (session_id) DO UPDATE SET updated_at = NOW()
            RETURNING *
        """)
        res = await db.execute(q, dict(
            session_id=session_id,
            user_id=user_id,
            model_id=model_id,
            thinking_level=thinking_level,
            temperature=temperature,
            canon_version=settings.canon_version,
        ))
        await db.commit()
        return dict(res.mappings().first())

    async def get_session(self, db: AsyncSession, session_id: str) -> Optional[Dict]:
        res = await db.execute(
            text("SELECT * FROM sacred_sessions WHERE session_id = :sid"),
            {"sid": session_id},
        )
        row = res.mappings().first()
        return dict(row) if row else None

    # ── Turn management ───────────────────────────────────────────────────────
    async def append_turn(
        self,
        db: AsyncSession,
        session_id: str,
        role: str,
        parts: List[Dict[str, Any]],
    ) -> int:
        """
        Append a new turn. Scans all text parts for injection attacks.
        Returns the turn index.
        """
        injection_found = False
        clean_parts = []
        for part in parts:
            if "text" in part and part["text"]:
                cleaned, detected = scan_injection(part["text"])
                if detected:
                    injection_found = True
                    log.warning(
                        "Injection attempt detected in session %s (role=%s)",
                        session_id, role
                    )
                clean_parts.append({**part, "text": cleaned})
            else:
                clean_parts.append(part)

        # Get next turn index
        res = await db.execute(
            text("SELECT COALESCE(MAX(turn_index), -1) + 1 FROM sacred_turns WHERE session_id = :sid"),
            {"sid": session_id},
        )
        turn_index = int(res.scalar_one())

        q = text("""
            INSERT INTO sacred_turns
              (session_id, turn_index, role, parts, contains_signature, is_healed)
            VALUES
              (:session_id, :turn_index, :role, :parts::jsonb, :has_sig, FALSE)
            RETURNING id
        """)
        has_sig = any(p.get("thought_signature") for p in clean_parts)
        await db.execute(q, dict(
            session_id=session_id,
            turn_index=turn_index,
            role=role,
            parts=json.dumps(clean_parts),
            has_sig=has_sig,
        ))

        # Update session timestamp
        await db.execute(
            text("UPDATE sacred_sessions SET updated_at = NOW() WHERE session_id = :sid"),
            {"sid": session_id},
        )
        await db.commit()
        return turn_index

    async def get_history(
        self, db: AsyncSession, session_id: str, limit: int = 50
    ) -> List[Dict[str, Any]]:
        res = await db.execute(
            text("""
                SELECT turn_index, role, parts, is_healed, created_at
                FROM sacred_turns
                WHERE session_id = :sid
                ORDER BY turn_index ASC
                LIMIT :lim
            """),
            {"sid": session_id, "lim": limit},
        )
        return [dict(r) for r in res.mappings().all()]

    # ── Self-healing ──────────────────────────────────────────────────────────
    async def heal_turn(
        self,
        db: AsyncSession,
        session_id: str,
        turn_index: int,
        reason: str,
        corrected_parts: List[Dict[str, Any]],
    ) -> bool:
        """
        Replace a turn's parts with corrected content and mark is_healed=True.
        Writes an audit entry to sacred_repair_log.
        """
        q = text("""
            UPDATE sacred_turns
            SET parts = :parts::jsonb,
                is_healed = TRUE
            WHERE session_id = :sid AND turn_index = :tidx
        """)
        res = await db.execute(q, dict(
            parts=json.dumps(corrected_parts),
            sid=session_id,
            tidx=turn_index,
        ))
        if res.rowcount == 0:
            return False

        await db.execute(text("""
            INSERT INTO sacred_repair_log
              (session_id, repaired_turn_index, reason)
            VALUES (:sid, :tidx, :reason)
        """), {"sid": session_id, "tidx": turn_index, "reason": reason})

        await db.commit()
        log.info("Healed turn %d in session %s: %s", turn_index, session_id, reason)
        return True

    # ── Canon verification ─────────────────────────────────────────────────────
    async def audit_session(self, db: AsyncSession, session_id: str) -> Dict[str, Any]:
        """Audit a session for injection evidence and unhealed anomalies."""
        turns = await self.get_history(db, session_id, limit=1000)
        anomalies = []
        for t in turns:
            parts = t.get("parts") or []
            if isinstance(parts, str):
                parts = json.loads(parts)
            for part in parts:
                text_val = part.get("text", "") or ""
                _, injected = scan_injection(text_val)
                if injected and not t.get("is_healed"):
                    anomalies.append({
                        "turn_index": t["turn_index"],
                        "role": t["role"],
                        "issue": "injection_detected",
                    })

        return {
            "session_id": session_id,
            "total_turns": len(turns),
            "anomalies": anomalies,
            "canon_version": settings.canon_version,
            "audited_at": datetime.now(timezone.utc).isoformat(),
        }
