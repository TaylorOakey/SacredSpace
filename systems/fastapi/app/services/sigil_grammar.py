"""Sacred Sigil Stack — Grammar Parser (Tier 2)
Parses sigil strings into structured components.

Grammar: <dimension>:<operation>[<affixes>][#<limit>]
  Where:
    <dimension> = glyph[+glyph...]              (one or more, '+' = amplify)
    <operation> = sigil[+sigil...]               (one or more)
    <affixes>  = [!]*[+]*[~]*[>]*[*]*            (any order, zero or more)
    <limit>    = #<int>                           (optional)

In lakesh alakin. ∆
"""
import re
import json
from dataclasses import dataclass, field, asdict
from typing import Optional
from pathlib import Path


# ── Grammar Tables ─────────────────────────────────────────────────────────

DIMENSION_GLYPHS: dict[str, str] = {
    "∞": "vault",
    "◊": "grove",
    "∆": "forest",
    "⊙": "codex",
    "≈": "memory",
    "♦": "agent",
    "⊗": "social",
    "⊜": "market",
    "Λ": "path",
    "♰": "lore",
}

DIMENSION_NAMES: dict[str, str] = {v: k for k, v in DIMENSION_GLYPHS.items()}

ROOT_SIGIL_GLYPHS: dict[str, str] = {
    "╻": "gateway",   # primary — used in spell macro compositions
    "○•": "mote",     # U+25CB + U+2022 — circle with orbiting dot
    "✧": "quest",     # U+2727 — four-point star
    "⚒": "forge",     # U+2692 — hammer & pick
    "Ϟ": "maestro",   # U+03DE — archaic koppa (lightning note)
    "✦": "lantern",   # U+2726 — diamond with inset dot
    # Alternate glyphs
    "╺": "gateway",   # alternate partial gateway
}

# Canonical display glyph per root sigil
ROOT_SIGIL_CANON: dict[str, str] = {
    "gateway": "╻",
    "mote": "○•",
    "quest": "✧",
    "forge": "⚒",
    "maestro": "Ϟ",
    "lantern": "✦",
}

AFFIX_MAP: dict[str, str] = {
    "!": "broadcast",
    "+": "amplify",
    "~": "loop",
    ">": "transform",
    "*": "persist",
}

AFFIX_GLYPHS: dict[str, str] = {v: k for k, v in AFFIX_MAP.items()}

SHAPE_CLASS: dict[str, str] = {
    "gateway": "hybrid",
    "mote": "curved",
    "quest": "angular",
    "forge": "angular",
    "maestro": "curved",
    "lantern": "hybrid",
}


# ── Macros (built-in + custom) ─────────────────────────────────────────────

# In-memory macro registry: populated with built-ins, extended from DB at startup
_MACRO_REGISTRY: dict[str, dict] = {}
_CUSTOM_MACROS_LOADED: bool = False


def _init_macros() -> None:
    """Seed built-in macros into the registry."""
    _MACRO_REGISTRY.clear()
    _MACRO_REGISTRY.update(_BUILTIN_MACROS)


_BUILTIN_MACROS: dict[str, dict] = {
    "aurora_weave": {
        "name": "AURORA.WEAVE",
        "composition": "∆+⊙:✦+╻",
        "description": "Weave awareness across Forest + Codex with Lantern insight",
        "agent": "AURORA",
        "cost_resonance": 10,
        "reward_insight": 15,
        "reward_xp": 25,
    },
    "elias_open_path": {
        "name": "ELIAS.OPEN_PATH",
        "composition": "✧+╻",
        "description": "Open a Quest at the Gateway — find the path",
        "agent": "ELIAS",
        "cost_resonance": 5,
        "reward_insight": 8,
        "reward_xp": 12,
    },
    "iris_thread": {
        "name": "IRIS.THREAD",
        "composition": "⊗:⚒+╻",
        "description": "From SOCIAL, Forge a connection at the Gateway",
        "agent": "IRIS",
        "cost_resonance": 12,
        "reward_insight": 25,
        "reward_xp": 40,
    },
    "asher_shadow": {
        "name": "ASHER.SHADOW",
        "composition": "✦:⚒",
        "description": "Apply Lantern to Forge — illuminate what is hidden",
        "agent": "ASHER",
        "cost_resonance": 8,
        "reward_insight": 20,
        "reward_xp": 30,
    },
    "scribe_record": {
        "name": "SCRIBE.RECORD",
        "composition": "○•:⚒",
        "description": "Turn a Mote into a crafted record",
        "agent": "SCRIBE",
        "cost_resonance": 3,
        "reward_insight": 5,
        "reward_xp": 8,
    },
    "lore_unveil": {
        "name": "LORE.UNVEIL",
        "composition": "♰:✦",
        "description": "Reveal storyline connections with Lantern illumination",
        "agent": "LORE",
        "cost_resonance": 6,
        "reward_insight": 18,
        "reward_xp": 22,
    },
}


# ── Data Model ──────────────────────────────────────────────────────────────

@dataclass
class ParsedSigil:
    """Structured representation of a parsed sigil string."""
    dimensions: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    affixes: dict[str, bool] = field(default_factory=dict)
    limit: Optional[int] = None
    params: dict[str, str] = field(default_factory=dict)
    original: str = ""
    is_macro: bool = False
    macro_name: str = ""
    macro_composition: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Serialise to plain dict for JSON responses."""
        return {
            "dimensions": self.dimensions,
            "operations": self.operations,
            "affixes": {a: True for a in self.affixes},
            "limit": self.limit,
            "params": self.params,
            "original": self.original,
            "is_macro": self.is_macro,
            "macro_name": self.macro_name,
            "macro_composition": self.macro_composition,
            "errors": self.errors,
            "valid": len(self.errors) == 0,
            "display": format_sigil(self),
        }

    @property
    def human_readable(self) -> str:
        """Natural-language description of the sigil."""
        parts = []
        if self.dimensions:
            dim_names = ", ".join(d.capitalize() for d in self.dimensions)
            parts.append(f"in {dim_names}")
        if self.operations:
            op_names = ", ".join(o.capitalize() for o in self.operations)
            parts.append(f"perform {op_names}")
        if self.affixes:
            ax = list(self.affixes.keys())
            parts.append(f"with {'+'.join(ax)}")
        if self.limit is not None:
            parts.append(f"limit {self.limit}")
        return " → ".join(parts) if parts else "empty sigil"


# ── Tokenizer ──────────────────────────────────────────────────────────────

# Order matters: multi-char glyphs before single-char
_GLYPH_PATTERN = "|".join(
    re.escape(g) for g in
    sorted(ROOT_SIGIL_GLYPHS.keys(), key=len, reverse=True)
    + sorted(DIMENSION_GLYPHS.keys(), key=len, reverse=True)
)

_SIGIL_RE = re.compile(
    r"(?P<glyph>" + _GLYPH_PATTERN + r")"
    r"|(?P<affix>[!+~>*])"
    r"|(?P<limit>#\d+)"
    r"|(?P<colon>:)"
    r"|(?P<space>\s+)"
    r"|(?P<other>[^\s#!+~>*:]+)"
)


def tokenize(sigil_string: str) -> list[dict]:
    """Split a sigil string into meaningful tokens."""
    tokens = []
    for m in _SIGIL_RE.finditer(sigil_string.strip()):
        kind = m.lastgroup
        val = m.group()
        if kind == "space":
            continue
        tokens.append({"kind": kind, "value": val})
    return tokens


# ── Parser ─────────────────────────────────────────────────────────────────

def parse(sigil_string: str) -> ParsedSigil:
    """Parse a raw sigil string into a structured ParsedSigil.

    Full pipeline: tokenize → macro-check → parse → validate.
    """
    original = sigil_string.strip()
    if not original:
        return ParsedSigil(errors=["Empty sigil string"], original=original)

    # Phase 1: check if it's a macro name (e.g. "AURORA.WEAVE" or "aurora_weave")
    macro_check = _try_expand_macro(original)
    if macro_check:
        ps = macro_check
        ps.original = original
        return _validate(ps)

    # Phase 2: tokenize and parse
    tokens = tokenize(original)
    if not tokens:
        return ParsedSigil(errors=["No parseable tokens"], original=original)

    ps = ParsedSigil(original=original)
    _parse_tokens(tokens, ps)
    return _validate(ps)


def _try_expand_macro(sigil_string: str) -> Optional[ParsedSigil]:
    """If the string is a macro name or invocation, expand it."""
    clean = sigil_string.strip().rstrip(")").rstrip("(").strip()
    # Match both "AURORA.WEAVE" and "AURORA.WEAVE()" and "aurora_weave"
    for key, macro in _MACRO_REGISTRY.items():
        if clean.upper() == macro["name"] or clean == key:
            ps = ParsedSigil(
                is_macro=True,
                macro_name=macro["name"],
                macro_composition=macro["composition"],
            )
            # Recursively parse the composition
            composed = parse(macro["composition"])
            ps.dimensions = composed.dimensions
            ps.operations = composed.operations
            ps.affixes = composed.affixes
            ps.limit = composed.limit
            return ps
    return None


def _parse_tokens(tokens: list[dict], ps: ParsedSigil) -> None:
    """Populate a ParsedSigil from a token list."""
    state = "dimension"        # dimension | operation | affix | done
    prev_token_kind = None
    i = 0
    while i < len(tokens):
        t = tokens[i]
        tk = t["kind"]
        tv = t["value"]

        if tk == "colon":
            state = "operation"
            prev_token_kind = "colon"
            i += 1
            continue

        if tk == "glyph":
            val = tv
            # Check if it's a dimension glyph or root sigil glyph
            if val in DIMENSION_GLYPHS and state == "dimension":
                ps.dimensions.append(DIMENSION_GLYPHS[val])
                prev_token_kind = "dim_glyph"
            elif val in ROOT_SIGIL_GLYPHS:
                state = "operation"
                ps.operations.append(ROOT_SIGIL_GLYPHS[val])
                prev_token_kind = "op_glyph"
            else:
                if val in DIMENSION_GLYPHS:
                    ps.dimensions.append(DIMENSION_GLYPHS[val])
                    prev_token_kind = "dim_glyph"
                else:
                    ps.errors.append(f"Unknown glyph: {val}")
                    prev_token_kind = "glyph"
            i += 1
            continue

        if tk == "affix":
            if tv == "+":
                # `+` between glyphs = separator, not amplify affix
                # Check next token: if it's a glyph, this + is a separator
                next_is_glyph = (
                    i + 1 < len(tokens) and tokens[i + 1]["kind"] == "glyph"
                )
                if next_is_glyph and prev_token_kind in ("dim_glyph", "op_glyph"):
                    # `+` acts as a separator between composed glyphs.
                    # Between dimensions it also implies amplify.
                    if prev_token_kind == "dim_glyph":
                        ps.affixes["amplify"] = True
                    # Between operations it's pure composition — no affix.
                    i += 1
                    continue

            # Trailing `+` or other affix tokens
            state = "affix"
            ps.affixes[AFFIX_MAP[tv]] = True
            prev_token_kind = "affix"
            i += 1
            continue

        if tk == "limit":
            try:
                ps.limit = int(tv[1:])
            except ValueError:
                ps.errors.append(f"Invalid limit: {tv}")
            prev_token_kind = "limit"
            i += 1
            continue

        if tk == "other":
            param_key = tv
            # Check if followed by = or value
            if i + 1 < len(tokens) and tokens[i + 1]["value"] == "=":
                # param=value pattern
                if i + 2 < len(tokens):
                    ps.params[param_key] = tokens[i + 2]["value"]
                    i += 3
                    continue
            ps.params[param_key] = True
            prev_token_kind = "other"
            i += 1
            continue

        i += 1

    # Post-process: if no dimensions but operations exist,
    # the sigil is dimensionless (broadcast implicit)
    if not ps.dimensions and not ps.operations and not ps.affixes:
        ps.errors.append("Sigil has no dimensions or operations")


def _validate(ps: ParsedSigil) -> ParsedSigil:
    """Validate a parsed sigil against grammar rules."""
    # Rule 1 — Shape carries purpose (informational, not blocking)
    for op in ps.operations:
        if op not in SHAPE_CLASS:
            ps.errors.append(f"Unknown operation '{op}' has no shape class")

    # Rule 2 — Stacked sigils must compose meaningfully
    # (all operations are valid — no invalid combinations)
    if len(ps.operations) > 3:
        ps.errors.append(
            f"Too many operations ({len(ps.operations)}); max 3"
        )

    # Rule 3 — Activation requires at least one operation or affix
    if not ps.operations and not ps.is_macro and "broadcast" not in ps.affixes:
        # A dimension with no operation is just navigation — valid but weak
        if ps.dimensions and not ps.affixes:
            pass  # pure dimension query is valid

    return ps


# ── Formatting ──────────────────────────────────────────────────────────────

def format_sigil(parsed: ParsedSigil) -> str:
    """Reconstruct a canonical sigil string from a ParsedSigil."""
    parts = []

    # Dimensions
    dim_glyphs = [DIMENSION_NAMES.get(d, d) for d in parsed.dimensions]
    if dim_glyphs:
        parts.append("+".join(dim_glyphs))

    # Operations
    op_glyphs = [ROOT_SIGIL_CANON.get(o, o) for o in parsed.operations]
    if op_glyphs:
        parts.append(":")
        parts.append("+".join(op_glyphs))

    # Affixes
    for affix_name in ["broadcast", "amplify", "loop", "transform", "persist"]:
        if parsed.affixes.get(affix_name):
            parts.append(AFFIX_GLYPHS.get(affix_name, affix_name))

    # Limit
    if parsed.limit is not None:
        parts.append(f"#{parsed.limit}")

    return "".join(parts)


def describe_sigil(parsed: ParsedSigil) -> str:
    """Generate a human-readable description of what the sigil does."""
    lines = []
    if parsed.is_macro:
        lines.append(f"✦ Macro: {parsed.macro_name}()")
        lines.append(f"   Composition: {parsed.macro_composition}")
        lines.append(f"   {_MACRO_REGISTRY.get(parsed.macro_name.lower().replace('.', '_'), {}).get('description', '')}")

    if parsed.dimensions:
        glyphs = " ".join(DIMENSION_NAMES.get(d, d) for d in parsed.dimensions)
        lines.append(f"📍 Dimensions: {', '.join(d.capitalize() for d in parsed.dimensions)} ({glyphs})")

    if parsed.operations:
        ops_fmt = []
        for op in parsed.operations:
            glyph = ROOT_SIGIL_CANON.get(op, "?")
            shape = SHAPE_CLASS.get(op, "?")
            name = op.capitalize()
            ops_fmt.append(f"{glyph} {name} ({shape})")
        lines.append(f"⚡ Operations: {' + '.join(ops_fmt)}")

    if parsed.affixes:
        affix_names = ", ".join(parsed.affixes.keys())
        lines.append(f"🔧 Affixes: {affix_names}")

    if parsed.limit is not None:
        lines.append(f"🎯 Limit: {parsed.limit} results")

    if parsed.params:
        lines.append(f"📎 Params: {parsed.params}")

    if parsed.errors:
        lines.append(f"⚠️ Errors: {'; '.join(parsed.errors)}")
        lines.append("❌ Invalid sigil")
    else:
        lines.append("✅ Valid sigil")

    return "\n".join(lines)


# ── Library Reference ──────────────────────────────────────────────────────

def get_library() -> dict:
    """Return the full grammar reference (dimensions + root sigils + macros)."""
    dimensions = []
    for glyph, name in DIMENSION_GLYPHS.items():
        dimensions.append({
            "glyph": glyph,
            "name": name.capitalize(),
            "id": name,
        })

    root_sigils = []
    for glyph, name in ROOT_SIGIL_GLYPHS.items():
        if glyph == "╺":
            continue  # skip alternate
        root_sigils.append({
            "glyph": glyph,
            "name": name.capitalize(),
            "id": name,
            "shape_class": SHAPE_CLASS.get(name, "unknown"),
            "canonical": ROOT_SIGIL_CANON.get(name),
        })
    # Deduplicate by id
    seen = set()
    unique_sigils = []
    for s in root_sigils:
        if s["id"] not in seen:
            seen.add(s["id"])
            unique_sigils.append(s)

    macros_list = []
    for key, m in _MACRO_REGISTRY.items():
        macros_list.append({
            "id": key,
            "name": m["name"],
            "composition": m["composition"],
            "description": m["description"],
            "agent": m["agent"],
            "cost_resonance": m["cost_resonance"],
            "reward_insight": m["reward_insight"],
            "reward_xp": m["reward_xp"],
        })

    return {
        "dimensions": dimensions,
        "root_sigils": unique_sigils,
        "macros": macros_list,
        "affixes": [{"glyph": k, "name": v} for k, v in AFFIX_MAP.items()],
        "version": "1.0.0",
        "canon": "In lakesh alakin. ∆",
    }


# ── Affinity Engine ────────────────────────────────────────────────────────

AFFINITIES: dict[str, dict[str, str]] = {
    "gateway": {
        "full": ["path"],
        "resonant": ["vault", "agent"],
    },
    "mote": {
        "full": ["memory"],
        "resonant": ["codex", "forest"],
    },
    "quest": {
        "full": ["path"],
        "resonant": ["market", "social"],
    },
    "forge": {
        "full": ["codex"],
        "resonant": ["agent", "market"],
    },
    "maestro": {
        "full": ["social"],
        "resonant": ["forest", "memory"],
    },
    "lantern": {
        "full": ["forest"],
        "resonant": ["codex", "vault"],
    },
}


def get_affinity(operation: str, dimension: str) -> str:
    """Return the affinity level for an operation in a dimension.

    Returns one of: 'full', 'resonant', 'neutral'
    """
    aff = AFFINITIES.get(operation)
    if not aff:
        return "neutral"
    if dimension in aff.get("full", []):
        return "full"
    if dimension in aff.get("resonant", []):
        return "resonant"
    return "neutral"


def calculate_cost(parsed: ParsedSigil) -> dict:
    """Calculate resonance cost for a parsed sigil.

    Base: 1
    Per dimension: 2
    Affix broadcast: +5 per extra dimension
    Affix amplify: +3
    Affix loop: +2 per cycle
    Affix persist: +2
    """
    base = 1
    dim_cost = len(parsed.dimensions) * 2
    affix_cost = 0
    if parsed.affixes.get("broadcast"):
        # Broadcast adds 5 per extra dimension beyond the first
        extra = max(0, len(parsed.dimensions) - 1) if parsed.dimensions else 8
        affix_cost += 5 * max(1, extra)
    if parsed.affixes.get("amplify"):
        affix_cost += 3
    if parsed.affixes.get("loop"):
        affix_cost += 2
    if parsed.affixes.get("persist"):
        affix_cost += 2

    total = base + dim_cost + affix_cost
    return {
        "base": base,
        "per_dimension": dim_cost,
        "affixes": affix_cost,
        "total": total,
    }


# ── Lint / Validate Entry Point ────────────────────────────────────────────

def lint(sigil_string: str) -> dict:
    """Lint a sigil string and return diagnostics."""
    result = {"original": sigil_string.strip(), "valid": True, "warnings": [], "errors": []}

    ps = parse(sigil_string)
    if ps.errors:
        result["valid"] = False
        result["errors"] = ps.errors

    # Additional lint checks
    if ps.dimensions and ps.operations:
        for dim in ps.dimensions:
            for op in ps.operations:
                affinity = get_affinity(op, dim)
                if affinity == "neutral":
                    result["warnings"].append(
                        f"'{op.capitalize()}' in '{dim.capitalize()}' is neutral affinity "
                        f"(no bonus)"
                    )

    result["parsed"] = ps.to_dict()
    return result


# ── Custom Macros (DB-backed) ─────────────────────────────────────────────

def get_all_macros() -> dict[str, dict]:
    """Return the complete macro registry (built-in + custom)."""
    if not _MACRO_REGISTRY:
        _init_macros()
    return _MACRO_REGISTRY


def load_custom_macros(conn) -> int:
    """Load custom macros from the database into the registry.
    
    Args:
        conn: SQLite connection with a sigil_macros table.
    
    Returns:
        Number of custom macros loaded.
    """
    global _CUSTOM_MACROS_LOADED
    _init_macros()
    try:
        rows = conn.execute(
            "SELECT id, name, composition, description, agent FROM sigil_macros WHERE active = 1"
        ).fetchall()
    except Exception:
        return 0  # table may not exist yet
    
    count = 0
    for row in rows:
        _id = f"custom_{row['id']}"
        _MACRO_REGISTRY[_id] = {
            "name": row["name"],
            "composition": row["composition"],
            "description": row.get("description", ""),
            "agent": row.get("agent", "CUSTOM"),
            "custom_id": row["id"],
            "cost_resonance": _auto_cost_from_composition(row["composition"]),
            "reward_insight": 3,
            "reward_xp": 5,
        }
        count += 1
    
    _CUSTOM_MACROS_LOADED = count > 0
    return count


def add_custom_macro(conn, name: str, composition: str, description: str = "", agent: str = "CUSTOM") -> dict:
    """Add a custom macro to the database and registry.
    
    Returns the macro record dict.
    """
    import sqlite3
    cursor = conn.execute(
        "INSERT INTO sigil_macros (name, composition, description, agent) VALUES (?, ?, ?, ?)",
        (name, composition, description, agent),
    )
    conn.commit()
    macro_id = cursor.lastrowid
    
    _id = f"custom_{macro_id}"
    _MACRO_REGISTRY[_id] = {
        "name": name,
        "composition": composition,
        "description": description,
        "agent": agent,
        "custom_id": macro_id,
        "cost_resonance": _auto_cost_from_composition(composition),
        "reward_insight": 3,
        "reward_xp": 5,
    }
    return _MACRO_REGISTRY[_id]


def delete_custom_macro(conn, macro_id: int) -> bool:
    """Soft-delete a custom macro from DB and remove from registry."""
    conn.execute("UPDATE sigil_macros SET active = 0 WHERE id = ?", (macro_id,))
    conn.commit()
    _id = f"custom_{macro_id}"
    if _id in _MACRO_REGISTRY:
        del _MACRO_REGISTRY[_id]
        return True
    return False


def _auto_cost_from_composition(composition: str) -> int:
    """Estimate resonance cost from a sigil composition string."""
    parsed = parse(composition)
    cost = calculate_cost(parsed)
    return cost.get("total", 5)


# ── Init ──────────────────────────────────────────────────────────────────

_init_macros()
