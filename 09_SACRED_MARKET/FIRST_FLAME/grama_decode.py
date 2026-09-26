"""
GR∆M∆ Name Decode — deliverable generator (First Flame product #1)

Turns an order into a print-ready HTML page (open in a browser → Print → Save as
PDF). Lenses 2, 4 and 5 are computed by the MERCHANT engine, so a Mini Decode is
fully automatic; Full and Deep add the lenses only Taylor can write.

  Lens 1  Root Meaning       — written by hand (--meaning)           Full, Deep
  Lens 2  Gematria Pulse     — computed (English ordinal + soul tone) all tiers
  Lens 3  Elemental Image    — chosen by hand (--element + --image)  Full, Deep
  Lens 4  Archetypal Thread  — computed (soul tone title + shadow)   all tiers
  Lens 5  Core Identity Sigil— computed (sigil + S∆CR3DS!G∆L cipher) all tiers
  Deep adds an extended narrative (--narrative-file).

Usage:
  python3 grama_decode.py "Ada Lovelace" --tier mini
  python3 grama_decode.py "Ada Lovelace" --tier full --element AIR \\
      --meaning "Ada: noble..." --image "A lantern held over deep water"
  python3 grama_decode.py "Ada Lovelace" --tier deep --element AIR \\
      --meaning "..." --image "..." --narrative-file ada.md --out ada.html
"""

import argparse
import html
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "systems" / "fastapi"))
from merchant import calculate_gematria, generate_sigil, ELEMENTS  # noqa: E402

TIERS = {"mini": "Mini Decode", "full": "Full Decode", "deep": "Deep Skry"}
CIPHER = str.maketrans({"A": "∆", "E": "3", "I": "!", "O": "0", "S": "$", "T": "7"})
DISCLAIMER = (
    "This decode is a creative and reflective reading built from the letters of "
    "your name. It is offered for inspiration and self-reflection only; it does "
    "not predict events or promise any outcome."
)


def sigilify(text: str) -> str:
    """S∆CR3DS!G∆L cipher: A→∆ E→3 I→! O→0 S→$ T→7 (uppercase first)."""
    return text.upper().translate(CIPHER)


def build(name, tier, element, meaning, image, narrative):
    gem = calculate_gematria(name)
    if gem["total"] == 0:
        raise SystemExit("Name has no A–Z letters to decode.")
    sigil = generate_sigil(name, element, gem["soul_tone"])
    e = html.escape

    letters = "".join(
        f'<td><b>{e(b["letter"])}</b><br>{b["value"]}</td>' for b in gem["breakdown"]
    )
    lenses = []
    if tier != "mini":
        lenses.append(("I · Root Meaning", f"<p>{e(meaning)}</p>"))
    lenses.append((
        "II · Gematria Pulse",
        f'<table class="g"><tr>{letters}</tr></table>'
        f'<p>Sum <b>{gem["total"]}</b> → Soul Tone <b>{gem["soul_tone"]}</b></p>',
    ))
    if tier != "mini":
        lenses.append(("III · Elemental Image", f"<p><b>{e(element.title())}</b> — {e(image)}</p>"))
    lenses.append((
        "IV · Archetypal Thread",
        f'<p><b>{e(gem["soul_title"])}</b></p><p class="shadow">Shadow to watch: {e(gem["soul_shadow"])}</p>',
    ))
    lenses.append((
        "V · Core Identity Sigil",
        f'<p class="sigil">{e(sigil)}</p><p class="cipher">{e(sigilify(name))}</p>',
    ))
    if tier == "deep":
        paras = "".join(f"<p>{e(p)}</p>" for p in narrative.split("\n\n") if p.strip())
        lenses.append(("Deep Skry · The Extended Reading", paras))

    sections = "".join(f"<section><h2>{t}</h2>{body}</section>" for t, body in lenses)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GR∆M∆ {e(TIERS[tier])} — {e(name)}</title>
<style>
:root{{--void:#060a07;--gold:#c8972a;--gold-pale:#e8c87a;--text:#a8a890;--text-hi:#e0d8c0;
--moss:#7aaa5a;--vine:#b86a8a;--border:rgba(200,151,42,0.32)}}
body{{background:var(--void);color:var(--text);font:16px/1.6 Georgia,serif;max-width:720px;margin:0 auto;padding:40px 24px}}
h1{{color:var(--gold-pale);font-weight:normal;letter-spacing:.08em;margin:0}}
.sub{{color:var(--gold);margin:4px 0 32px}}
section{{border-top:1px solid var(--border);padding:18px 0}}
h2{{color:var(--gold);font-size:15px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 8px}}
b{{color:var(--text-hi)}}
table.g{{border-collapse:collapse;margin:8px 0}} table.g td{{border:1px solid var(--border);padding:4px 7px;text-align:center;font-size:13px}}
.shadow{{color:var(--vine)}} .sigil{{font-size:34px;color:var(--gold-pale);margin:6px 0}}
.cipher{{color:var(--moss);letter-spacing:.2em}}
footer{{border-top:1px solid var(--border);margin-top:24px;padding-top:12px;font-size:12px}}
@media print{{body{{background:#fff;color:#222}} h1,.sigil,b{{color:#000}} h2{{color:#7a5a10}}}}
</style></head><body>
<h1>GR∆M∆ {e(TIERS[tier])}</h1>
<p class="sub">for {e(name)} · {date.today().isoformat()}</p>
{sections}
<footer>{e(DISCLAIMER)}<br>S∆CR3D.ARC∆N∆.STUDIØS · In lakesh alakin.</footer>
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("name")
    ap.add_argument("--tier", choices=TIERS, default="mini")
    ap.add_argument("--element", default="AETHER", type=str.upper, choices=ELEMENTS)
    ap.add_argument("--meaning", default="", help="Lens I, required for full/deep")
    ap.add_argument("--image", default="", help="Lens III description, required for full/deep")
    ap.add_argument("--narrative-file", type=Path, help="Deep Skry extended reading (blank line = new paragraph)")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()

    if a.tier != "mini" and not (a.meaning and a.image):
        ap.error("--meaning and --image are required for full and deep tiers")
    if a.tier == "deep" and not a.narrative_file:
        ap.error("--narrative-file is required for the deep tier")
    narrative = a.narrative_file.read_text(encoding="utf-8") if a.narrative_file else ""

    out = a.out or Path(f"decode_{a.tier}_{''.join(ch for ch in a.name if ch.isalnum())}.html")
    out.write_text(build(a.name, a.tier, a.element, a.meaning, a.image, narrative), encoding="utf-8")
    print(f"∆ {TIERS[a.tier]} written → {out}")


if __name__ == "__main__":
    main()
