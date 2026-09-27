#!/usr/bin/env python3
"""neural_forest_v2.py — Neural Forest :: ChromaDB + nomic-embed-text
Pillar: 03_NEURAL_FOREST | Owner: ELIAS | Status: Active
"""
import os
import json
import requests
from typing import Optional

# chromadb's pydantic-settings init stat()s '.env' — fails if CWD is an unmounted WSL path
os.chdir(os.path.expanduser("~"))

try:
    import chromadb
    _CHROMA = True
except ImportError:
    _CHROMA = False

OLLAMA_URL = "http://192.168.240.1:11434"
EMBED_MODEL = "nomic-embed-text"
CHROMA_PATH = "/home/useroak3ytree/sacredspace/03_NEURAL_FOREST/.chromadb"


def embed(text: str) -> list[float]:
    resp = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


class NeuralForest:
    def __init__(self, collection: str = "sacred_lore"):
        if not _CHROMA:
            raise RuntimeError("chromadb not installed: pip install chromadb")
        self.client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.col = self.client.get_or_create_collection(
            name=collection,
            metadata={"hnsw:space": "cosine"},
        )

    def store(self, doc_id: str, text: str, metadata: Optional[dict] = None) -> None:
        vec = embed(text)
        self.col.upsert(
            ids=[doc_id],
            embeddings=[vec],
            documents=[text],
            metadatas=[metadata or {}],
        )

    def search(self, query: str, n: int = 5) -> list[dict]:
        vec = embed(query)
        results = self.col.query(query_embeddings=[vec], n_results=n)
        hits = []
        for i, doc in enumerate(results["documents"][0]):
            hits.append({
                "id":       results["ids"][0][i],
                "text":     doc,
                "distance": results["distances"][0][i],
                "meta":     results["metadatas"][0][i],
            })
        return hits

    def count(self) -> int:
        return self.col.count()


# ∆ CLI
if __name__ == "__main__":
    import sys
    forest = NeuralForest()

    if len(sys.argv) < 2:
        print(f"Neural Forest v2 | {forest.count()} documents indexed")
        print("Usage: neural_forest_v2.py search <query>")
        print("       neural_forest_v2.py store <id> <text>")
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == "search" and len(sys.argv) >= 3:
        query = " ".join(sys.argv[2:])
        hits = forest.search(query)
        print(json.dumps(hits, indent=2))
    elif cmd == "store" and len(sys.argv) >= 4:
        forest.store(sys.argv[2], " ".join(sys.argv[3:]))
        print(f"∆ Stored: {sys.argv[2]}")
    else:
        print("Unknown command")
        sys.exit(1)
