from __future__ import annotations

from abc import ABC, abstractmethod

from django_agent_rag.types import ChunkPayload


class Chunker(ABC):
    @abstractmethod
    def chunk(self, text: str, **kwargs) -> list[ChunkPayload]:
        raise NotImplementedError

