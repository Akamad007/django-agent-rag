from __future__ import annotations

from abc import ABC, abstractmethod

from django_agent_rag.types import RetrievedChunk


class Retriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[RetrievedChunk]:
        raise NotImplementedError

