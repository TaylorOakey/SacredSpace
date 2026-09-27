import sys
from .embed import get_embedding
from .vector_store import search_memory

def ask(question: str, pillar=None):
    print(f"Query: {question}")

    vector = get_embedding(question)
    if not vector:
        print("No embedding returned.")
        return

    results = search_memory(vector, pillar=pillar)
    if not results:
        print("No relevant memories found.")
        return

    for idx, hit in enumerate(results, start=1):
        payload = hit.get("payload", {})
        score = hit.get("score", 0.0)
        print(f"\n[{idx}] Score: {score:.3f}")
        print(f"Pillar: {payload.get('pillar')}")
        print(f"File: {payload.get('file')}")
        print(f"Project: {payload.get('project')}")
        print(f"Text: {str(payload.get('text', ''))[:300]}...")
