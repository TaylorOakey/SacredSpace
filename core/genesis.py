from pathlib import Path
import sys
SACRED_ROOT = Path(__file__).resolve().parent.parent
PILLARS = ["core", "systems", "learning", "economy", "habitat", "creation", "council", "lineage", "archive"]

def check():
    print(f"\n∆∆∆ SACREDSPACE OS — GENESIS v1.2.0")
    for p in PILLARS:
        status = "✓ ACTIVE" if (SACRED_ROOT / p).is_dir() else "✗ MISSING"
        print(f"  {status:<10} | {p.upper()}")
    return True

if __name__ == "__main__":
    check()
