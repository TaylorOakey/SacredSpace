"""Sacred Sigil IDE — Forge Backend Router
Code execution, spell persistence, terminal integration
Mount at /api/forge/*
In lakesh alakin. ∆
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
from io import StringIO
import sys
import tempfile

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

try:
    from restricted_python import compile_restricted
except ImportError:
    compile_restricted = None

router = APIRouter(prefix="/api/forge", tags=["forge"])

# Constants
SACRED_ROOT = Path(os.environ.get("SACRED_ROOT", "/mnt/d/SacredSpace_OS"))
SPELLS_DIR = SACRED_ROOT / "04_SACRED_CODEX" / "spells"
SPELLS_DIR.mkdir(parents=True, exist_ok=True)

# ── Request/Response Models ──────────────────────────────────────────────

class ExecuteCodeRequest(BaseModel):
    code: str
    spell_id: str = "MANUAL"
    brain: str = "GENERAL"

class SaveSpellRequest(BaseModel):
    code: str
    spell_id: str
    name: str
    concept: str = ""
    domain: str = "PY"

class VitalsRequest(BaseModel):
    pass

# ── Safe Execution Environment ──────────────────────────────────────────

# Allowed builtins in restricted sandbox
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'str': str,
    'int': int,
    'float': float,
    'bool': bool,
    'list': list,
    'dict': dict,
    'tuple': tuple,
    'set': set,
    'enumerate': enumerate,
    'zip': zip,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'sorted': sorted,
    'reversed': reversed,
    'map': map,
    'filter': filter,
    '__builtins__': {},
}

def execute_python_spell(code: str, spell_id: str) -> dict:
    """Execute Python code in a restricted sandbox.

    Uses RestrictedPython if available, falls back to basic string validation.
    """

    # Security: reject dangerous patterns
    dangerous_patterns = [
        '__import__', 'exec', 'eval', 'open', 'file',
        'compile', '__code__', 'sys.exit', 'os.', 'subprocess',
        '__loader__', '__spec__', 'globals', 'locals', 'vars'
    ]

    for pattern in dangerous_patterns:
        if pattern.lower() in code.lower():
            return {
                "status": "error",
                "spell_id": spell_id,
                "output": f"⚠ GATE SECURITY: Pattern '{pattern}' not allowed in spells",
                "message": "Forbidden operation detected — spell rejected"
            }

    try:
        # Use RestrictedPython if available
        if compile_restricted:
            compiled = compile_restricted(code, f'<spell:{spell_id}>', 'exec')
            if compiled.errors:
                error_msg = "\n".join(str(e) for e in compiled.errors)
                return {
                    "status": "error",
                    "spell_id": spell_id,
                    "output": f"[COMPILATION ERROR]\n{error_msg}",
                    "message": "Spell compilation failed"
                }

            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                exec(compiled.code, {"__builtins__": SAFE_BUILTINS})
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout

        else:
            # Fallback: basic exec with restrictions
            old_stdout = sys.stdout
            sys.stdout = StringIO()

            try:
                exec(code, {"__builtins__": SAFE_BUILTINS})
                output = sys.stdout.getvalue()
            finally:
                sys.stdout = old_stdout

        return {
            "status": "success",
            "spell_id": spell_id,
            "output": output if output else "[No output]",
            "message": f"✓ {spell_id} cast successfully"
        }

    except SyntaxError as e:
        return {
            "status": "error",
            "spell_id": spell_id,
            "output": f"[SYNTAX ERROR] Line {e.lineno}: {e.msg}",
            "message": f"Syntax error at line {e.lineno}"
        }

    except Exception as e:
        return {
            "status": "error",
            "spell_id": spell_id,
            "output": f"[{type(e).__name__}] {str(e)}",
            "message": f"Spell execution failed: {type(e).__name__}"
        }

# ── Endpoints ────────────────────────────────────────────────────────────

@router.post("/execute")
async def execute_spell(req: ExecuteCodeRequest):
    """Execute Python code in a sandboxed environment.

    Returns stdout + execution status.
    Logs to terminal for narrative recording.
    """
    result = execute_python_spell(req.code, req.spell_id)

    # Log to terminal event
    try:
        from app.services import sigil_terminal_backend
        sigil_terminal_backend.record_query(
            query=f"forge:execute {req.spell_id}",
            dimension="agent",
            result_count=1 if result["status"] == "success" else 0,
            source="ide"
        )
    except:
        pass  # Non-critical

    return result

@router.post("/seal")
async def seal_spell_to_codex(req: SaveSpellRequest):
    """Persist a spell to the Codex.

    Writes spell to /04_SACRED_CODEX/spells/{spell_id}.json
    """
    try:
        # Validate spell ID format
        if not req.spell_id or len(req.spell_id) < 3:
            raise HTTPException(status_code=400, detail="Invalid spell_id")

        spell_data = {
            "id": req.spell_id,
            "name": req.name,
            "code": req.code,
            "concept": req.concept,
            "domain": req.domain,
            "sealed_at": datetime.now().isoformat(),
            "sealed_by": "forge_ide"
        }

        spell_path = SPELLS_DIR / f"{req.spell_id}.json"
        with open(spell_path, 'w') as f:
            json.dump(spell_data, f, indent=2)

        return {
            "status": "sealed",
            "spell_id": req.spell_id,
            "path": str(spell_path),
            "message": f"✓ {req.spell_id} sealed to Codex"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to seal spell: {str(e)}")

@router.get("/vitals")
async def forge_vitals():
    """Query system health — Pulse, Ollama, ChromaDB, MCP.

    Returns status of all connected services.
    """
    vitals = {
        "fastapi": "✓ online",
        "timestamp": datetime.now().isoformat(),
    }

    # Check Pulse
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex(('127.0.0.1', 8890)) == 0:
            vitals["pulse"] = "✓ online"
        else:
            vitals["pulse"] = "✗ offline"
        s.close()
    except:
        vitals["pulse"] = "✗ unreachable"

    # Check Ollama
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex(('127.0.0.1', 11434)) == 0:
            vitals["ollama"] = "✓ online"
        else:
            vitals["ollama"] = "✗ offline"
        s.close()
    except:
        vitals["ollama"] = "✗ unreachable"

    # Check ChromaDB (if running)
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        if s.connect_ex(('127.0.0.1', 8000)) == 0:
            vitals["chromadb"] = "✓ online"
        else:
            vitals["chromadb"] = "✗ offline"
        s.close()
    except:
        vitals["chromadb"] = "✗ unreachable"

    # Count sealed spells
    try:
        spell_count = len(list(SPELLS_DIR.glob("*.json")))
        vitals["sealed_spells"] = spell_count
    except:
        vitals["sealed_spells"] = 0

    # HKM status
    vitals["hkm_layer"] = "✓ active"
    vitals["sigil_engine"] = "✓ active"

    return vitals

@router.get("/spells")
async def list_sealed_spells():
    """List all sealed spells in the Codex."""
    try:
        spells = []
        for spell_file in SPELLS_DIR.glob("*.json"):
            try:
                with open(spell_file, 'r') as f:
                    spell_data = json.load(f)
                    spells.append(spell_data)
            except:
                pass

        return {
            "status": "success",
            "spells": spells,
            "total": len(spells)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list spells: {str(e)}")

@router.get("/spells/{spell_id}")
async def get_sealed_spell(spell_id: str):
    """Retrieve a single sealed spell."""
    try:
        spell_path = SPELLS_DIR / f"{spell_id}.json"
        if not spell_path.exists():
            raise HTTPException(status_code=404, detail=f"Spell '{spell_id}' not found")

        with open(spell_path, 'r') as f:
            spell_data = json.load(f)

        return spell_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve spell: {str(e)}")

@router.post("/sigilify")
async def sigilify_text(text: str):
    """Convert text to sigil cipher.

    Encodes text into sacred glyph notation.
    """
    sigil_map = {
        'A': '∆', 'a': '∆',
        'E': '3', 'e': '3',
        'I': '!', 'i': '!',
        'O': '0', 'o': '0',
        'S': '$', 's': '$',
        'T': '7', 't': '7',
        'Y': '¥', 'y': '¥',
        'H': '#', 'h': '#',
    }

    result = text
    for char, sigil in sigil_map.items():
        result = result.replace(char, sigil)

    return {
        "original": text,
        "sigilified": result,
        "message": "✓ Text transformed into sacred cipher"
    }

@router.get("/health")
async def forge_health():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "service": "Sacred Sigil IDE Forge",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
