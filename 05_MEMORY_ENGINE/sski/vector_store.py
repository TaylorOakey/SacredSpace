import requests
from .config import QDRANT_URL, COLLECTION_NAME, VECTOR_SIZE

def ensure_collection():
    """Create collection if missing."""
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}"
    response = requests.get(url, timeout=15)

    if response.status_code == 404:
        print(f"Initializing Qdrant collection: {COLLECTION_NAME}")
        payload = {
            "vectors": {
                "size": VECTOR_SIZE,
                "distance": "Cosine"
            }
        }
        create_response = requests.put(url, json=payload, timeout=15)
        create_response.raise_for_status()
        return

    response.raise_for_status()

def upsert_points(points):
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points"
    response = requests.put(url, json={"points": points}, timeout=60)
    response.raise_for_status()
    return response.json()

def search_memory(vector, limit=5, pillar=None):
    url = f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search"
    payload = {
        "vector": vector,
        "limit": limit,
        "with_payload": True
    }

    if pillar:
        payload["filter"] = {
            "must": [
                {"key": "pillar", "match": {"value": pillar}}
            ]
        }

    response = requests.post(url, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get("result", [])
