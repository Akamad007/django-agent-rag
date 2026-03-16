from django_agent_rag.backends.embeddings.base import EmbeddingBackend
from django_agent_rag.backends.embeddings.fake import FakeEmbeddingBackend

__all__ = ["EmbeddingBackend", "FakeEmbeddingBackend"]

