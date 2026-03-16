from __future__ import annotations

import hashlib

from django_agent_rag.backends.embeddings.base import EmbeddingBackend


class FakeEmbeddingBackend(EmbeddingBackend):
    def __init__(self, dimensions: int = 8) -> None:
        self._dimensions = dimensions

    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._vectorize(text) for text in texts]

    def dimensions(self) -> int:
        return self._dimensions

    def provider_name(self) -> str:
        return "fake-embeddings"

    def _vectorize(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return [round((digest[index] / 255.0), 6) for index in range(self._dimensions)]

