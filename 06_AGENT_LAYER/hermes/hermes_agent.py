"""
hermes_agent.py — Hermes Agent v0.13.0
MCP-compatible orchestration layer for SacredSpace OS — Pillar 06 (AGENT_LAYER)
Active Persona: GR∆M∆ (AGENT-GRAMA-001) | Cipher Sage of the Sacred Codex

Stack: smolagents ToolCallingAgent + LiteLLM (Ollama → Gemini cascade)
Status: Canon | v0.13.0
"""

import sys
import os

# Allow import from sacredspace_core whether running standalone or as module
sys.path.insert(0, os.path.expanduser("~/sacredspace_core"))

from smolagents import ToolCallingAgent

from .grama_persona import (
    GRAMA_SYSTEM_PROMPT,
    GRAMA_SEAL_TEMPLATE,
    GRAMA_VERSION,
    gematria,
)
from .sacredspace_mcp import ALL_TOOLS


def _get_model():
    try:
        from app.llm_cascade import get_model
        return get_model()
    except Exception:
        # Standalone fallback — try Ollama directly
        from smolagents import LiteLLMModel
        import os
        ollama_host = os.getenv("OLLAMA_HOST", "http://192.168.240.1:11434")
        return LiteLLMModel(
            model_id="ollama_chat/llama3.2",
            api_base=ollama_host,
            api_key="ollama",
        )


class HermesAgent:
    """
    Hermes v0.13.0 — orchestration agent with GR∆M∆ persona.
    Wraps a smolagents ToolCallingAgent loaded with the 7 MCP tools.
    """

    VERSION = GRAMA_VERSION

    def __init__(self):
        model = _get_model()
        self._agent = ToolCallingAgent(
            tools=ALL_TOOLS,
            model=model,
            max_steps=6,
            verbosity_level=1,
            system_prompt=GRAMA_SYSTEM_PROMPT,
        )

    def run(self, query: str) -> str:
        """Run a natural-language query through Hermes / GR∆M∆."""
        response = self._agent.run(query)

        # Append gematria seal on the primary topic word
        topic = query.split()[0] if query.split() else "HERMES"
        g_val = gematria(topic)
        seal = GRAMA_SEAL_TEMPLATE.format(
            gematria_note=f"{topic.upper()} = {g_val}"
        )
        return f"{response}{seal}"

    def health(self) -> dict:
        return {
            "status": "ok",
            "version": self.VERSION,
            "agent": "GR∆M∆",
            "id": "AGENT-GRAMA-001",
            "pillar": "04_SACRED_CODEX",
            "tools": [t.name for t in ALL_TOOLS],
        }


# Module-level singleton — lazy-initialized on first request
_hermes: HermesAgent | None = None


def get_hermes() -> HermesAgent:
    global _hermes
    if _hermes is None:
        _hermes = HermesAgent()
    return _hermes
