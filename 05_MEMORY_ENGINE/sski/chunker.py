def get_chunks(text: str, chunk_size: int = 800, overlap: int = 150):
    """Fixed-size word chunking with overlap."""
    words = text.split()
    if not words:
        return []

    chunks = []
    step = max(1, chunk_size - overlap)

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)

    return chunks
