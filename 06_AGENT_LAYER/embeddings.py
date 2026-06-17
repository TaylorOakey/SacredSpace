from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Iterable, List
import numpy as np
from sentence_transformers import SentenceTransformer
from ..config import settings

@dataclass
class EmbeddingResult:
    vector: List[float]
    embedding_hash: str

class EmbeddingsProvider:
    def embed_text(self, text: str) -> EmbeddingResult: ...

class LocalSentenceTransformersEmbeddings(EmbeddingsProvider):
    def __init__(self) -> None:
        self.model = SentenceTransformer(settings.sentence_transformers_model)

    def embed_text(self, text: str) -> EmbeddingResult:
        vec = self.model.encode([text], normalize_embeddings=True)[0]
        raw = vec.tobytes()
        h = hashlib.blake2b(raw, digest_size=16).hexdigest()
        return EmbeddingResult(vector=[float(x) for x in vec.tolist()], embedding_hash=h)

def build_embeddings_provider() -> EmbeddingsProvider:
    # Currently only local sentence-transformers wired by default.
    return LocalSentenceTransformersEmbeddings()
