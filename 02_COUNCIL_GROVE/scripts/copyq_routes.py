"""
copyq_routes.py
FastAPI routes for CopyQ integration — mount with prefix="/copyq"
Pillar: 02_COUNCIL_GROVE
Owner: AURORA
"""

from fastapi import APIRouter
from pydantic import BaseModel
from copyq_bridge import (
    clipboard_read, clipboard_write, push_to_tab,
    route_by_pillar, sacredtag_stamp, flush_tab_to_file,
    search_tabs, list_tabs,
)

copyq_router = APIRouter(tags=["copyq"])


class ClipPayload(BaseModel):
    text: str
    tab: str = "INBOX"


class RoutePayload(BaseModel):
    text: str
    pillar: str
    topic: str = ""
    keywords: str = ""


@copyq_router.get("/clipboard")
def get_clipboard():
    return {"text": clipboard_read()}


@copyq_router.post("/push")
def push_clip(payload: ClipPayload):
    push_to_tab(payload.tab, payload.text)
    return {"status": "ok", "tab": payload.tab}


@copyq_router.post("/route")
def route_clip(payload: RoutePayload):
    tab = route_by_pillar(payload.pillar, payload.text)
    return {"status": "ok", "routed_to": tab}


@copyq_router.post("/stamp")
def stamp_clip(payload: RoutePayload):
    stamped = sacredtag_stamp(payload.text, payload.pillar, payload.topic, payload.keywords)
    return {"status": "ok", "stamped": stamped}


@copyq_router.get("/tabs")
def get_tabs():
    return {"tabs": list_tabs()}


@copyq_router.get("/search")
def search(q: str):
    results = search_tabs(q)
    return {"query": q, "results": results}


@copyq_router.post("/flush/{tab}")
def flush(tab: str = "FORGE"):
    path = flush_tab_to_file(tab)
    return {"status": "ok", "file": str(path)}
