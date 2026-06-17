from __future__ import annotations
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from typing import Any, Dict, Optional

class TaskQueue:
    """Durable DB-backed queue. Concurrency-safe via SKIP LOCKED."""

    @staticmethod
    async def enqueue(db: AsyncSession, task_type: str, payload: Dict[str, Any], priority: int = 100,
                      run_after: Optional[datetime] = None, max_attempts: int = 5) -> int:
        run_after = run_after or datetime.now(timezone.utc)
        q = text("""
            INSERT INTO task_queue (task_type, payload, priority, run_after, max_attempts)
            VALUES (:task_type, :payload::jsonb, :priority, :run_after, :max_attempts)
            RETURNING id
        """)
        res = await db.execute(q, dict(task_type=task_type, payload=payload, priority=priority, run_after=run_after, max_attempts=max_attempts))
        task_id = int(res.scalar_one())
        await db.commit()
        return task_id

    @staticmethod
    async def claim_next(db: AsyncSession, worker_id: str):
        q = text("""
            WITH cte AS (
              SELECT id
              FROM task_queue
              WHERE status = 'queued'
                AND run_after <= NOW()
              ORDER BY priority ASC, id ASC
              FOR UPDATE SKIP LOCKED
              LIMIT 1
            )
            UPDATE task_queue t
            SET status='running', locked_by=:worker_id, locked_at=NOW(), updated_at=NOW()
            FROM cte
            WHERE t.id = cte.id
            RETURNING t.*
        """)
        res = await db.execute(q, dict(worker_id=worker_id))
        row = res.mappings().first()
        if not row:
            return None
        await db.commit()
        return dict(row)

    @staticmethod
    async def mark_done(db: AsyncSession, task_id: int):
        q = text("""
            UPDATE task_queue
            SET status='done', updated_at=NOW()
            WHERE id=:id
        """)
        await db.execute(q, dict(id=task_id))
        await db.commit()

    @staticmethod
    async def mark_failed(db: AsyncSession, task_id: int, err: str):
        q = text("""
            UPDATE task_queue
            SET status=CASE WHEN attempts + 1 >= max_attempts THEN 'failed' ELSE 'queued' END,
                attempts=attempts+1,
                last_error=:err,
                locked_by=NULL,
                locked_at=NULL,
                run_after=CASE WHEN attempts + 1 >= max_attempts THEN run_after ELSE NOW() + INTERVAL '60 seconds' * POWER(2, LEAST(attempts, 6)) END,
                updated_at=NOW()
            WHERE id=:id
        """)
        await db.execute(q, dict(id=task_id, err=err[:2000]))
        await db.commit()
