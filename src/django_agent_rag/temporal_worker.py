from __future__ import annotations

import asyncio
import os

from django.conf import settings

from django_agent_rag.settings import get_app_settings


async def run_worker() -> None:
    from temporalio.client import Client
    from temporalio.worker import Worker

    from django_agent_rag.temporal import DocumentWorkflow, process_document_activity

    client = await Client.connect(
        getattr(
            settings,
            "TEMPORAL_ADDRESS",
            os.getenv("TEMPORAL_ADDRESS", "localhost:7233"),
        )
    )
    config = get_app_settings()
    worker = Worker(
        client,
        task_queue=config.temporal_task_queue,
        workflows=[DocumentWorkflow],
        activities=[process_document_activity],
    )
    await worker.run()


def main() -> None:
    asyncio.run(run_worker())
