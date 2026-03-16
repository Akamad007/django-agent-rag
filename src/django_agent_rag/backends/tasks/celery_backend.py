from __future__ import annotations

from django_agent_rag.backends.tasks.base import TaskBackend
from django_agent_rag.exceptions import OptionalDependencyMissing
from django_agent_rag.settings import optional_module_available


class CeleryTaskBackend(TaskBackend):
    def __init__(self) -> None:
        if not optional_module_available("celery"):
            raise OptionalDependencyMissing(
                "Celery support requires installing django-agent-rag[celery]."
            )

    def enqueue_document_ingestion(self, document_id: int) -> None:
        from django_agent_rag.celery_tasks import process_document_ingestion

        process_document_ingestion.delay(document_id)

    def enqueue_embedding(
        self,
        document_id: int | None = None,
        chunk_ids: list[int] | None = None,
    ) -> None:
        from django_agent_rag.celery_tasks import process_document_embedding

        process_document_embedding.delay(document_id=document_id, chunk_ids=chunk_ids)

    def enqueue_reindex(self, document_id: int) -> None:
        from django_agent_rag.celery_tasks import process_document_reindex

        process_document_reindex.delay(document_id)

    def backend_name(self) -> str:
        return "celery"
