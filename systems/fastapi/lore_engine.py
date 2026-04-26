import os
from pathlib import Path
from typing import Optional
from fastapi import APIRouter
import yaml
from datetime import datetime, timezone

router = APIRouter(prefix="/lore-engine", tags=["Lore-to-Product"])

VAULT_PATH = Path(os.getenv("SACREDSPACE_VAULT", "/mnt/d/01_VAULT/SacredSpace_Vault"))

ARTIFACT_KEYWORDS = [
    "lantern","staff","blade","mask","relic","crystal","stone","amulet",
    "talisman","sigil","glyph","scroll","tome","codex","drum","bow",
    "shield","cloak","robe","ring","pendant","crown","vessel","jar",
    "pouch","satchel","map","compass","mirror","key","seed","root",
    "feather","totem","card deck","tarot","oracle","journal","poster","sticker",
    "heartstone","waystone","moonfeather","raindrop staff","spiceblade",
]

def init_lore_engine():
    print(f"[LORE ENGINE] Initialized. Vault: {VAULT_PATH}")

def read_frontmatter(path: Path) -> Optional[dict]:
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) > 2:
                return yaml.safe_load(parts[1])
    except Exception:
        pass
    return None

@router.get("/status")
async def get_status():
    return {
        "system": "LORE_PRODUCT_ENGINE",
        "vault": str(VAULT_PATH),
        "vault_exists": VAULT_PATH.exists(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@router.post("/scan")
async def scan_lore():
    if not VAULT_PATH.exists():
        return {"error": "Vault not found", "vault": str(VAULT_PATH)}

    all_files = list(VAULT_PATH.rglob("*.md"))
    lore_notes = []
    gaps = []

    for md_path in all_files:
        if any(p.startswith(".") for p in md_path.parts):
            continue
        fm = read_frontmatter(md_path)
        if fm and str(fm.get("type", "")).lower() == "artifact":
            continue
        try:
            body = md_path.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            continue
        lore_notes.append(str(md_path.name))
        for kw in ARTIFACT_KEYWORDS:
            if kw in body:
                gaps.append({
                    "signal": kw.title(),
                    "source": md_path.name,
                    "type": "RELIC",
                })

    # Deduplicate by signal name
    seen = set()
    unique_gaps = []
    for g in gaps:
        if g["signal"] not in seen:
            seen.add(g["signal"])
            unique_gaps.append(g)

    return {
        "system": "LORE_PRODUCT_ENGINE",
        "vault": str(VAULT_PATH),
        "lore_notes_scanned": len(lore_notes),
        "gaps_found": len(unique_gaps),
        "gaps": unique_gaps,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

@router.get("/gaps")
async def get_gaps():
    return {"message": "Run POST /lore-engine/scan first"}
