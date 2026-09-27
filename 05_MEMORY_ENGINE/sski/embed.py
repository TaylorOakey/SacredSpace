import requests
from .config import OLLAMA_URL, EMBED_MODEL

def get_embedding(text: str):
    """Call Ollama embeddings endpoint."""
    if not text or not text.strip():
        return None

    payload = {
        "model": EMBED_MODEL,
        "prompt": text
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()
        return response.json().get("embedding")
    except Exception as e:
        print(f"Error calling Ollama embeddings: {e}")
        return None
