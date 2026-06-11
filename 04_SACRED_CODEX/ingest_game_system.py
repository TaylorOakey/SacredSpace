"""
Ingest GAME_SYSTEM markdown files into ChromaDB collection: sacredspace_canon
Uses the IRIS venv's ChromaDB installation.
"""
import hashlib
import re
import sys
from pathlib import Path

import chromadb

VAULT_ROOT = Path("/mnt/d/SacredSpace_OS/01_OBSIDIAN_VAULTS/SacredSpace_Vault")
CHROMA_PATH = Path("/mnt/d/SacredSpace_OS/06_AGENT_LAYER/IRIS/chroma_db")
COLLECTION = "sacredspace_canon"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADER_RE = re.compile(r"\n(?=##+ )")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def chunk(body: str) -> list[str]:
    sections = HEADER_RE.split(body.strip())
    out = []
    for s in sections:
        s = s.strip()
        if len(s) >= 80:
            out.append(s)
    return out or [body.strip()]


def chunk_id(source: str, idx: int, text: str) -> str:
    raw = f"{source}::{idx}::{text}".encode()
    return hashlib.sha1(raw).hexdigest()


def main():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    col = client.get_or_create_collection(COLLECTION)

    files = sorted(VAULT_ROOT.rglob("*.md"))
    if not files:
        print("No .md files found.")
        sys.exit(1)

    total_chunks = 0
    for path in files:
        text = path.read_text(encoding="utf-8", errors="replace")
        meta, body = parse_frontmatter(text)

        title = meta.get("title", path.stem)
        pillar = meta.get("pillar", "unknown")
        status = meta.get("status", "raw")
        tags = meta.get("tags", "")

        chunks = chunk(body)
        ids, docs, metas = [], [], []

        for idx, c in enumerate(chunks):
            ids.append(chunk_id(str(path), idx, c))
            docs.append(c)
            metas.append({
                "source": path.name,
                "title": title,
                "pillar": pillar,
                "status": status,
                "tags": tags,
                "chunk_index": idx,
                "path": str(path),
            })

        col.upsert(ids=ids, documents=docs, metadatas=metas)
        total_chunks += len(chunks)
        print(f"  [{len(chunks):2d} chunks] {path.relative_to(VAULT_ROOT)}")

    print(f"\nDone. {len(files)} files → {total_chunks} chunks → collection '{COLLECTION}'")
    print(f"ChromaDB at: {CHROMA_PATH}")


if __name__ == "__main__":
    main()
