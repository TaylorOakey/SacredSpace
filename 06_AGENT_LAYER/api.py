"""
FastAPI — REST surface for Forest operations, task management, and governance.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .db import SessionLocal, db_ping
from .models import NodeOut, TaskIn, TaskOut
from .queue import TaskQueue
from .services.gardener import compute_spi
from .services.supervisor import SupervisorKernel

app = FastAPI(
    title="S∆CR3D Neural Forest Kernel",
    description="Self-regulating cognitive ingestion and memory architecture.",
    version="1.0.0",
)
supervisor = SupervisorKernel()


async def get_db():
    async with SessionLocal() as s:
        yield s


# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health():
    ok = await db_ping()
    return {"ok": ok, "version": "1.0.0", "canon": settings.canon_version}


# ── Task queue ────────────────────────────────────────────────────────────────
@app.post("/tasks", response_model=dict)
async def create_task(t: TaskIn, db: AsyncSession = Depends(get_db)):
    task_id = await TaskQueue.enqueue(
        db, t.task_type, t.payload,
        priority=t.priority, run_after=t.run_after, max_attempts=t.max_attempts
    )
    return {"id": task_id}


@app.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("SELECT * FROM task_queue WHERE id=:id"), {"id": task_id})
    row = res.mappings().first()
    if not row:
        raise HTTPException(404, "Task not found")
    return dict(row)


@app.get("/tasks", response_model=List[dict])
async def list_tasks(status: Optional[str] = None, limit: int = 50, db: AsyncSession = Depends(get_db)):
    if status:
        res = await db.execute(
            text("SELECT id, task_type, status, priority, attempts, created_at FROM task_queue WHERE status=:s ORDER BY id DESC LIMIT :l"),
            {"s": status, "l": limit},
        )
    else:
        res = await db.execute(
            text("SELECT id, task_type, status, priority, attempts, created_at FROM task_queue ORDER BY id DESC LIMIT :l"),
            {"l": limit},
        )
    return [dict(r) for r in res.mappings().all()]


# ── Nodes ─────────────────────────────────────────────────────────────────────
@app.get("/nodes", response_model=List[NodeOut])
async def list_nodes(
    limit: int = 50,
    tag: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    if tag:
        res = await db.execute(
            text("""
                SELECT id, title, node_type, source_url, body, tags, license,
                       resurrection_score, decay_rate, embedding_hash, created_at, updated_at
                FROM forest_nodes
                WHERE tags ? :tag
                ORDER BY updated_at DESC LIMIT :limit
            """),
            {"tag": tag, "limit": limit},
        )
    else:
        res = await db.execute(
            text("""
                SELECT id, title, node_type, source_url, body, tags, license,
                       resurrection_score, decay_rate, embedding_hash, created_at, updated_at
                FROM forest_nodes
                ORDER BY updated_at DESC LIMIT :limit
            """),
            {"limit": limit},
        )
    return [dict(r) for r in res.mappings().all()]


@app.get("/nodes/{node_id}", response_model=NodeOut)
async def get_node(node_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        text("SELECT * FROM forest_nodes WHERE id=:id"), {"id": node_id}
    )
    row = res.mappings().first()
    if not row:
        raise HTTPException(404, "Node not found")
    # Touch last_accessed_at
    await db.execute(
        text("UPDATE forest_nodes SET last_accessed_at=NOW() WHERE id=:id"),
        {"id": node_id},
    )
    await db.commit()
    return dict(row)


@app.get("/nodes/{node_id}/neighbors", response_model=List[dict])
async def get_neighbors(node_id: str, limit: int = 12, db: AsyncSession = Depends(get_db)):
    res = await db.execute(text("""
        SELECT n.id, n.title, n.node_type, e.weight, e.edge_type
        FROM forest_edges e
        JOIN forest_nodes n ON (
            CASE WHEN e.src_id = :nid THEN e.dst_id ELSE e.src_id END = n.id
        )
        WHERE e.src_id = :nid OR e.dst_id = :nid
        ORDER BY e.weight DESC LIMIT :lim
    """), {"nid": node_id, "lim": limit})
    return [dict(r) for r in res.mappings().all()]


@app.post("/nodes/{node_id}/resurrect", response_model=dict)
async def resurrect_node(node_id: str, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        text("SELECT id, resurrection_score, tags FROM forest_nodes WHERE id=:id"),
        {"id": node_id},
    )
    row = res.mappings().first()
    if not row:
        raise HTTPException(404, "Node not found")
    new_score = min(1.0, float(row["resurrection_score"]) + 0.25)
    await db.execute(text("""
        UPDATE forest_nodes
        SET resurrection_score = :score,
            tags = (
                SELECT jsonb_agg(val)
                FROM jsonb_array_elements_text(tags) AS val
                WHERE val <> 'archived'
            ),
            updated_at = NOW()
        WHERE id = :id
    """), {"score": new_score, "id": node_id})
    await db.commit()
    return {"id": node_id, "new_resurrection_score": new_score}


# ── Forest stats ──────────────────────────────────────────────────────────────
@app.get("/forest/spi", response_model=dict)
async def forest_spi(db: AsyncSession = Depends(get_db)):
    return await compute_spi(db)


@app.get("/forest/stats", response_model=dict)
async def forest_stats(db: AsyncSession = Depends(get_db)):
    spi_data = await compute_spi(db)

    tag_res = await db.execute(text("""
        SELECT tag_val, COUNT(*) as cnt
        FROM forest_nodes, jsonb_array_elements_text(tags) AS tag_val
        GROUP BY tag_val ORDER BY cnt DESC LIMIT 20
    """))
    top_tags = [{"tag": r[0], "count": r[1]} for r in tag_res.fetchall()]

    type_res = await db.execute(text("""
        SELECT node_type, COUNT(*) cnt FROM forest_nodes GROUP BY node_type ORDER BY cnt DESC
    """))
    by_type = {r[0]: r[1] for r in type_res.fetchall()}

    orphan_res = await db.execute(text("""
        SELECT COUNT(*) FROM forest_nodes n
        WHERE NOT EXISTS (
            SELECT 1 FROM forest_edges e WHERE e.src_id=n.id OR e.dst_id=n.id
        )
    """))
    orphans = int(orphan_res.scalar_one())

    return {
        **spi_data,
        "top_tags": top_tags,
        "nodes_by_type": by_type,
        "orphan_count": orphans,
    }


# ── Harvest (full pipeline trigger) ──────────────────────────────────────────
@app.post("/ops/harvest", response_model=dict)
async def enqueue_harvest(db: AsyncSession = Depends(get_db)):
    ids = {}
    ids["scout"] = await TaskQueue.enqueue(db, "scout.run", {}, priority=10)
    ids["decay"] = await TaskQueue.enqueue(db, "gardener.decay", {}, priority=200)
    ids["prune"] = await TaskQueue.enqueue(db, "gardener.prune", {}, priority=210)
    ids["resurrect"] = await TaskQueue.enqueue(db, "gardener.resurrect", {}, priority=220)
    ids["deadlinks"] = await TaskQueue.enqueue(db, "gardener.deadlinks", {}, priority=230)
    ids["pulse"] = await TaskQueue.enqueue(db, "pulse.send", {}, priority=250)
    return {"ok": True, "task_ids": ids}


@app.post("/ops/pulse", response_model=dict)
async def trigger_pulse(db: AsyncSession = Depends(get_db)):
    task_id = await TaskQueue.enqueue(db, "pulse.send", {}, priority=5)
    return {"ok": True, "task_id": task_id}


# ── Governance / Sessions ─────────────────────────────────────────────────────
@app.post("/sessions", response_model=dict)
async def create_session(body: dict, db: AsyncSession = Depends(get_db)):
    session_id = body.get("session_id") or str(uuid.uuid4())
    user_id = body.get("user_id", "anonymous")
    model_id = body.get("model_id", "unknown")
    result = await supervisor.create_session(
        db, session_id, user_id, model_id,
        thinking_level=body.get("thinking_level", "medium"),
        temperature=float(body.get("temperature", 0.7)),
    )
    return result


@app.get("/sessions/{session_id}", response_model=dict)
async def get_session(session_id: str, db: AsyncSession = Depends(get_db)):
    sess = await supervisor.get_session(db, session_id)
    if not sess:
        raise HTTPException(404, "Session not found")
    return sess


@app.get("/sessions/{session_id}/history", response_model=List[dict])
async def get_history(session_id: str, limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await supervisor.get_history(db, session_id, limit=limit)


@app.post("/sessions/{session_id}/turns", response_model=dict)
async def append_turn(session_id: str, body: dict, db: AsyncSession = Depends(get_db)):
    turn_index = await supervisor.append_turn(
        db, session_id,
        role=body.get("role", "user"),
        parts=body.get("parts", []),
    )
    return {"turn_index": turn_index}


@app.get("/sessions/{session_id}/audit", response_model=dict)
async def audit_session(session_id: str, db: AsyncSession = Depends(get_db)):
    return await supervisor.audit_session(db, session_id)
