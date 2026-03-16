from __future__ import annotations

from datetime import timedelta

try:
    from temporalio import activity, workflow
except Exception:  # pragma: no cover
    activity = None
    workflow = None


if workflow is not None:
    @activity.defn
    async def process_document_activity(payload: dict) -> None:
        from django_agent_rag.services import chunk_document, embed_document, reindex_document

        operation = payload["operation"]
        document_id = payload["document_id"]
        if operation == "document_ingestion":
            chunk_document(document_id)
            embed_document(document_id)
        elif operation == "document_embedding":
            embed_document(document_id=document_id, chunk_ids=payload.get("chunk_ids"))
        elif operation == "document_reindex":
            reindex_document(document_id)


    @workflow.defn(name="django_agent_rag.temporal.workflows.DocumentWorkflow")
    class DocumentWorkflow:
        @workflow.run
        async def run(self, payload: dict) -> None:
            await workflow.execute_activity(
                process_document_activity,
                payload,
                start_to_close_timeout=timedelta(seconds=300),
            )
