import hashlib
from .config import VAULT_PATH, REQUIRED_FIELDS
from .parse_frontmatter import parse_note
from .chunker import get_chunks
from .embed import get_embedding
from .vector_store import ensure_collection, upsert_points

def run():
    ensure_collection()
    print(f"Scanning Vault: {VAULT_PATH}")

    all_points = []
    files_seen = 0
    files_indexed = 0

    for md_file in VAULT_PATH.rglob("*.md"):
        if ".obsidian" in md_file.parts:
            continue

        files_seen += 1

        try:
            content = md_file.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"Skipping unreadable file: {md_file} ({e})")
            continue

        meta, body = parse_note(content)

        if not all(k in meta for k in REQUIRED_FIELDS):
            print(f"Skipping (Missing Metadata): {md_file.name}")
            continue

        chunks = get_chunks(body)
        if not chunks:
            continue

        files_indexed += 1

        for i, chunk in enumerate(chunks):
            vector = get_embedding(chunk)
            if not vector:
                continue

            point_id = hashlib.md5(f"{md_file.as_posix()}::{i}".encode()).hexdigest()

            payload = {
                "file": md_file.name,
                "path": str(md_file),
                "chunk": i,
                "text": chunk,
                **{k: meta.get(k) for k in REQUIRED_FIELDS}
            }

            all_points.append({
                "id": point_id,
                "vector": vector,
                "payload": payload
            })

    print(f"Files scanned: {files_seen}")
    print(f"Files indexed: {files_indexed}")
    print(f"Fragments prepared: {len(all_points)}")

    if all_points:
        upsert_points(all_points)
        print(f"Done. Indexed {len(all_points)} fragments.")
    else:
        print("No valid notes found to index.")

if __name__ == "__main__":
    run()
