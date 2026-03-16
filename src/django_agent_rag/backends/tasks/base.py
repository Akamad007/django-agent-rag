from __future__ import annotations

from abc import ABC, abstractmethod


class TaskBackend(ABC):
    @abstractmethod
    def enqueue_document_ingestion(self, document_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def enqueue_embedding(self, document_id: int | None = None, chunk_ids: list[int] | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def enqueue_reindex(self, document_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def backend_name(self) -> str:
        raise NotImplementedError

