from __future__ import annotations
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..config import settings

class Linker:
    async def link_recent(self, db: AsyncSession, node_id: str) -> int:
        # Find similar nodes via pgvector cosine distance; insert edges.
        # vector_cosine_ops: smaller is more similar; cosine distance = 1 - cosine_similarity
        threshold = settings.link_similarity_threshold
        max_edges = settings.link_max_edges_per_node

        # Convert similarity threshold to distance threshold
        max_dist = 1.0 - float(threshold)

        q = text("""
            SELECT id, 1 - (embedding <=> (SELECT embedding FROM forest_nodes WHERE id=:node_id)) AS similarity
            FROM forest_nodes
            WHERE id <> :node_id AND embedding IS NOT NULL
            ORDER BY (embedding <=> (SELECT embedding FROM forest_nodes WHERE id=:node_id)) ASC
            LIMIT :limit
        """)
        res = await db.execute(q, dict(node_id=node_id, limit=max_edges))
        rows = res.fetchall()

        inserted = 0
        for other_id, sim in rows:
            if sim is None:
                continue
            if float(sim) < threshold:
                continue

            ins = text("""
                INSERT INTO forest_edges (src_id, dst_id, weight, edge_type)
                VALUES (:src, :dst, :w, 'semantic')
                ON CONFLICT (src_id, dst_id, edge_type) DO UPDATE SET weight=EXCLUDED.weight
            """)
            await db.execute(ins, dict(src=node_id, dst=other_id, w=float(sim)))
            inserted += 1

        await db.commit()
        return inserted
