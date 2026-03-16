from __future__ import annotations

try:
    from celery import shared_task
except Exception:  # pragma: no cover
    def shared_task(*_args, **_kwargs):
        def decorator(func):
            return func

        return decorator


@shared_task
def process_document_ingestion(document_id: int) -> None:
    from django_agent_rag.services import chunk_document, embed_document

    chunk_document(document_id)
    embed_document(document_id)


@shared_task
def process_document_embedding(document_id: int | None = None, chunk_ids: list[int] | None = None) -> None:
    from django_agent_rag.services import embed_document

    if document_id is None:
        raise ValueError("document_id is required.")
    embed_document(document_id, chunk_ids=chunk_ids)


@shared_task
def process_document_reindex(document_id: int) -> None:
    from django_agent_rag.services import reindex_document

    reindex_document(document_id)

