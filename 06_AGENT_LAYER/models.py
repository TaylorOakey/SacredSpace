from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class SacredPart(BaseModel):
    """Atomic unit of communication (Gemini-like)."""
    text: Optional[str] = None
    inline_data: Optional[Dict[str, str]] = None  # mime_type, data or REF
    function_call: Optional[Dict[str, Any]] = None
    function_response: Optional[Dict[str, Any]] = None
    thought_signature: Optional[str] = Field(default=None, description="Encrypted state required for continuity.")
    model_config = ConfigDict(extra="ignore")

class SacredTurn(BaseModel):
    role: str  # user | model | tool | system
    parts: List[SacredPart]

class SacredConfig(BaseModel):
    thinking_level: str = "medium"  # low | medium | high
    temperature: float = 0.7
    media_resolution: Optional[str] = "media_resolution_medium"
    tools: Optional[List[Dict[str, Any]]] = None

class SacredSessionState(BaseModel):
    session_id: str
    user_id: str
    model_id: str
    history: List[SacredTurn] = Field(default_factory=list)
    config: SacredConfig = Field(default_factory=SacredConfig)
    canon_version: str = "v1.0"
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class NodeIn(BaseModel):
    id: str
    title: str
    node_type: str
    source_url: Optional[str] = None
    body: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    license: Optional[str] = None

class NodeOut(NodeIn):
    resurrection_score: float = 0.0
    decay_rate: float = 0.0001
    embedding_hash: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TaskIn(BaseModel):
    task_type: str
    payload: Dict[str, Any]
    priority: int = 100
    run_after: Optional[datetime] = None
    max_attempts: int = 5

class TaskOut(BaseModel):
    id: int
    task_type: str
    payload: Dict[str, Any]
    status: str
    priority: int
    attempts: int
    max_attempts: int
    locked_by: Optional[str]
    locked_at: Optional[datetime]
    run_after: datetime
    last_error: Optional[str]
    created_at: datetime
    updated_at: datetime
