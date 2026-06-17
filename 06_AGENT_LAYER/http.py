from __future__ import annotations
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter

@retry(stop=stop_after_attempt(5), wait=wait_exponential_jitter(initial=1, max=30))
async def fetch_text(url: str, headers: dict | None = None, timeout: float = 30.0) -> str:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        r = await client.get(url, headers=headers)
        r.raise_for_status()
        return r.text
