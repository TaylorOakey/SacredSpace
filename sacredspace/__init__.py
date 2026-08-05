"""
sacredspace — SacredSpace OS Cipher Core (GR∆M∆)

Functional core both GR∆M∆ canon tracks depend on. Exposes the unified
cipher comparison API across all five SacredSpace cipher systems.

Pillar: 04_SACRED_CODEX (functional core)
Canon: 2026-08-01
"""

from .ciphers import (
    CIPHER_SUBSTITUTIONS,
    GLYPH_MAP,
    SACRED_ALPHABET_MAP,
    WORD_OVERRIDES,
    CipherComparison,
    abazith_resonance,
    cipher,
    compare_ciphers,
    gematria,
    hebrew_value,
    reduce_to_digit,
    sigil_decode_partial,
    sigil_encode,
    sigil_encode_word,
)

__all__ = [
    "CIPHER_SUBSTITUTIONS",
    "GLYPH_MAP",
    "SACRED_ALPHABET_MAP",
    "WORD_OVERRIDES",
    "CipherComparison",
    "abazith_resonance",
    "cipher",
    "compare_ciphers",
    "gematria",
    "hebrew_value",
    "reduce_to_digit",
    "sigil_decode_partial",
    "sigil_encode",
    "sigil_encode_word",
]

__version__ = "1.0.0-GRAMA"
