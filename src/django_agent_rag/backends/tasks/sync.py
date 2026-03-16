from __future__ import annotations

from django_agent_rag.backends.tasks.base import TaskBackend


class SyncTaskBackend(TaskBackend):
    def enqueue_document_ingestion(self, document_id: int) -> None:
        from django_agent_rag.services import chunk_document, embed_document

        chunk_document(document_id)
        embed_document(document_id)

    def enqueue_embedding(self, document_id: int | None = None, chunk_ids: list[int] | None = None) -> None:
        from django_agent_rag.services import embed_document

        if document_id is None:
            raise ValueError("SyncTaskBackend requires a document_id for enqueue_embedding.")
        embed_document(document_id=document_id, chunk_ids=chunk_ids)

    def enqueue_reindex(self, document_id: int) -> None:
        from django_agent_rag.services import reindex_document

        reindex_document(document_id)

    def backend_name(self) -> str:
        return "sync"

