from __future__ import annotations

import asyncio

from django.conf import settings

from django_agent_rag.backends.tasks.base import TaskBackend
from django_agent_rag.exceptions import OptionalDependencyMissing
from django_agent_rag.settings import get_app_settings, optional_module_available


class TemporalTaskBackend(TaskBackend):
    def __init__(self) -> None:
        if not optional_module_available("temporalio.client"):
            raise OptionalDependencyMissing("Temporal support requires installing django-agent-rag[temporal].")

    def enqueue_document_ingestion(self, document_id: int) -> None:
        self._start_workflow("document_ingestion", document_id=document_id)

    def enqueue_embedding(self, document_id: int | None = None, chunk_ids: list[int] | None = None) -> None:
        self._start_workflow("document_embedding", document_id=document_id, chunk_ids=chunk_ids or [])

    def enqueue_reindex(self, document_id: int) -> None:
        self._start_workflow("document_reindex", document_id=document_id)

    def backend_name(self) -> str:
        return "temporal"

    def _start_workflow(self, operation: str, **payload) -> None:
        asyncio.run(self._run_workflow(operation=operation, payload=payload))

    async def _run_workflow(self, operation: str, payload: dict) -> None:
        from temporalio.client import Client

        cfg = get_app_settings()
        client = await Client.connect(getattr(settings, "TEMPORAL_ADDRESS", "localhost:7233"))
        workflow_name = cfg.temporal_workflow
        workflow_id = f"django-agent-rag-{operation}-{payload.get('document_id', 'unknown')}"
        await client.start_workflow(
            workflow_name,
            {"operation": operation, **payload},
            id=workflow_id,
            task_queue=cfg.temporal_task_queue,
        )

