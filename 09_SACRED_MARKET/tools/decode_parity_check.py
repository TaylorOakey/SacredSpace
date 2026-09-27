"""
Parity check: C2 web page JS engine  vs  merchant.py / grama_decode.py.

Runs the code between ENGINE-START and ENGINE-END in decode_web/index.html
under node and compares every result with the Python engine.
Usage (repo root):  python3 09_SACRED_MARKET/tools/decode_parity_check.py
Needs `node` on PATH (or NODE=/path/to/node).
"""
import json, os, re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
if hasattr(sys.stdout, "reconfigure"):  # Windows consoles default to cp1252 and choke on ∆
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path[:0] = [str(REPO / "systems/fastapi"), str(REPO / "09_SACRED_MARKET/FIRST_FLAME")]
from merchant import calculate_gematria, generate_sigil  # noqa: E402
from grama_decode import sigilify  # noqa: E402

html = (REPO / "09_SACRED_MARKET/FIRST_FLAME/decode_web/index.html").read_text(encoding="utf-8")
engine = re.search(r"// ENGINE-START.*?\n(.*?)// ENGINE-END", html, re.S).group(1)

names = ["Ada Lovelace", "Taylor Oakey", "Mary-Jane O'Neil", "José Núñez", "Straße",
         "  Sp  aced  ", "Ωmega 🌿 root", "abc123", "A", "zzzzzzzzzzzz"]
names += ["".join(chr(65 + (i * 7 + j) % 26) for j in range(i % 15 + 1)) for i in range(300)]

js = engine + "\nconst N=" + json.dumps(names) + ";console.log(JSON.stringify(N.map(n=>{" \
     "const g=gematria(n);return [g.breakdown.map(b=>[b.letter,b.value]),g.total,g.soul_tone," \
     "g.title,g.shadow,sigil(n,g.soul_tone),sigilify(n)]})))"
out = json.loads(subprocess.run([os.environ.get("NODE", "node"), "-e", js],
                                capture_output=True, text=True, check=True).stdout)

bad = 0
for n, j in zip(names, out):
    g = calculate_gematria(n)
    p = [[[b["letter"], b["value"]] for b in g["breakdown"]], g["total"], g["soul_tone"],
         g["soul_title"], g["soul_shadow"], generate_sigil(n, "AETHER", g["soul_tone"]), sigilify(n)]
    if p != j:
        bad += 1
        print("MISMATCH", repr(n), "\n  py:", p, "\n  js:", j)
print(f"∆ {len(names)} names · {bad} mismatches · soul tones covered {sorted({o[2] for o in out})}")
sys.exit(1 if bad else 0)
