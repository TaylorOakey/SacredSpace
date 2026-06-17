"""
Gardener Agent — decay, prune, resurrect, dead-link detection, and SPI scoring.
All operations are additive: nodes are never hard-deleted.
"""
from __future__ import annotations

import asyncio
import json
import logging
import math
from typing import Dict, List, Tuple

import httpx
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..config import settings

log = logging.getLogger(__name__)


# ── Sacred Progress Index ─────────────────────────────────────────────────────
async def compute_spi(db: AsyncSession) -> Dict:
    """
    SPI formula (0–100) inspired by network science metrics:
      - Node count score    (15 pts): log-scaled, saturates at ~1000 nodes
      - Edge density score  (25 pts): edges / (nodes * max_edges_per_node)
      - Energy distribution (25 pts): % nodes NOT archived (healthy nodes)
      - Avg resurrection    (20 pts): mean resurrection_score across active nodes
      - Recency score       (15 pts): % of nodes updated in last 30 days
    """
    counts = (await db.execute(text("""
        SELECT
          COUNT(*) AS total_nodes,
          COUNT(*) FILTER (WHERE NOT (tags ? 'archived')) AS active_nodes,
          COUNT(*) FILTER (WHERE updated_at > NOW() - INTERVAL '30 days') AS recent_nodes,
          COALESCE(AVG(resurrection_score) FILTER (WHERE NOT (tags ? 'archived')), 0) AS avg_rs
        FROM forest_nodes
    """))).mappings().first()

    edge_count = (await db.execute(text("SELECT COUNT(*) FROM forest_edges"))).scalar_one()

    total = max(1, int(counts["total_nodes"]))
    active = int(counts["active_nodes"])
    recent = int(counts["recent_nodes"])
    avg_rs = float(counts["avg_rs"] or 0)
    edges = int(edge_count)

    # Score components
    node_score = min(15, 15 * math.log10(total + 1) / math.log10(1001))
    max_possible_edges = total * settings.link_max_edges_per_node
    density_score = min(25, 25 * (edges / max(1, max_possible_edges)))
    health_score = min(25, 25 * (active / total))
    rs_score = min(20, 20 * avg_rs)
    recency_score = min(15, 15 * (recent / total))

    spi = node_score + density_score + health_score + rs_score + recency_score

    return {
        "spi": round(spi, 1),
        "components": {
            "node_score": round(node_score, 2),
            "density_score": round(density_score, 2),
            "health_score": round(health_score, 2),
            "resurrection_score": round(rs_score, 2),
            "recency_score": round(recency_score, 2),
        },
        "stats": {
            "total_nodes": total,
            "active_nodes": active,
            "recent_nodes": recent,
            "total_edges": edges,
            "avg_resurrection_score": round(avg_rs, 4),
        },
    }


class Gardener:

    # ── Decay ─────────────────────────────────────────────────────────────────
    async def apply_decay(self, db: AsyncSession) -> int:
        """Exponential decay based on time since last access."""
        lam = math.log(2) / max(1, settings.decay_half_life_days)
        q = text("""
            UPDATE forest_nodes
            SET resurrection_score = GREATEST(
                  0,
                  resurrection_score - (:lam * COALESCE(
                    EXTRACT(EPOCH FROM (NOW() - COALESCE(last_accessed_at, created_at))) / 86400,
                    1
                  ))
                ),
                updated_at = NOW()
        """)
        await db.execute(q, {"lam": lam})
        await db.commit()
        count = (await db.execute(text("SELECT COUNT(*) FROM forest_nodes"))).scalar_one()
        log.info("Decay applied to %d nodes (λ=%.6f)", count, lam)
        return int(count)

    # ── Prune (archive, never delete) ─────────────────────────────────────────
    async def prune(self, db: AsyncSession) -> int:
        q = text("""
            UPDATE forest_nodes
            SET tags = tags || '"archived"'::jsonb,
                updated_at = NOW()
            WHERE resurrection_score < :thresh
              AND NOT (tags ? 'archived')
              AND NOT (tags ? 'sealed')
        """)
        res = await db.execute(q, {"thresh": settings.prune_threshold})
        await db.commit()
        count = res.rowcount or 0
        log.info("Pruned (archived) %d nodes below threshold %.2f", count, settings.prune_threshold)
        return count

    # ── Resurrect ─────────────────────────────────────────────────────────────
    async def resurrect_candidates(self, db: AsyncSession) -> int:
        """
        Boost resurrection_score for high-degree archived nodes.
        State transition: archived → active (remove 'archived' tag) when score >= threshold.
        """
        q = text("""
            WITH degree AS (
              SELECT n.id,
                     COALESCE(s.cnt, 0) + COALESCE(d.cnt, 0) AS deg
              FROM forest_nodes n
              LEFT JOIN (SELECT src_id, COUNT(*) cnt FROM forest_edges GROUP BY src_id) s ON s.src_id = n.id
              LEFT JOIN (SELECT dst_id, COUNT(*) cnt FROM forest_edges GROUP BY dst_id) d ON d.dst_id = n.id
            ),
            boosted AS (
              SELECT n.id,
                     LEAST(1.0, n.resurrection_score + (0.025 * deg.deg)) AS new_score
              FROM forest_nodes n
              JOIN degree deg ON n.id = deg.id
              WHERE (n.tags ? 'archived') AND NOT (n.tags ? 'sealed')
            )
            UPDATE forest_nodes fn
            SET resurrection_score = b.new_score,
                tags = CASE
                  WHEN b.new_score >= :thresh
                  THEN (
                    SELECT jsonb_agg(val)
                    FROM jsonb_array_elements_text(fn.tags) AS val
                    WHERE val <> 'archived'
                  )
                  ELSE fn.tags
                END,
                updated_at = NOW()
            FROM boosted b
            WHERE fn.id = b.id
        """)
        res = await db.execute(q, {"thresh": settings.resurrect_threshold})
        await db.commit()
        count = res.rowcount or 0
        log.info("Resurrection pass: %d nodes evaluated", count)
        return count

    # ── Dead-link detection ────────────────────────────────────────────────────
    async def check_dead_links(self, db: AsyncSession) -> Dict:
        """
        Async-concurrent URL health check on forest nodes.
        Tags broken links as 'dead_link'; marks dormant if already archived.
        """
        if not settings.deadlink_check_enabled:
            return {"checked": 0, "dead": 0}

        res = await db.execute(text("""
            SELECT id, source_url FROM forest_nodes
            WHERE source_url IS NOT NULL
              AND NOT (tags ? 'dead_link')
            ORDER BY last_accessed_at ASC NULLS FIRST
            LIMIT :batch
        """), {"batch": settings.deadlink_batch_size})
        rows = res.fetchall()

        timeout = settings.deadlink_timeout_secs
        dead_ids: List[str] = []

        async def check_url(node_id: str, url: str):
            try:
                async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as c:
                    r = await c.head(url)
                    if r.status_code >= 400:
                        dead_ids.append(node_id)
            except Exception:
                dead_ids.append(node_id)

        semaphore = asyncio.Semaphore(20)  # max 20 concurrent checks

        async def bounded_check(nid, url):
            async with semaphore:
                await check_url(nid, url)

        await asyncio.gather(*[bounded_check(r[0], r[1]) for r in rows])

        if dead_ids:
            dead_list = json.dumps(dead_ids)
            await db.execute(text("""
                UPDATE forest_nodes
                SET tags = tags || '"dead_link"'::jsonb,
                    updated_at = NOW()
                WHERE id = ANY(:ids::text[])
            """), {"ids": dead_ids})
            await db.commit()

        log.info("Dead-link check: %d checked, %d dead", len(rows), len(dead_ids))
        return {"checked": len(rows), "dead": len(dead_ids)}
