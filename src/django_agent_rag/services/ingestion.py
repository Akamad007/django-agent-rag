from __future__ import annotations

import hashlib

from django.db import transaction
from django.utils import timezone

from django_agent_rag.models import Chunk, Document
from django_agent_rag.settings import get_app_settings, import_from_setting


def get_embedding_backend():
    return import_from_setting("EMBEDDING_BACKEND")()


def get_llm_backend():
    return import_from_setting("LLM_BACKEND")()


def get_chunker():
    return import_from_setting("CHUNKER_CLASS")()


def get_task_backend():
    return import_from_setting("TASK_BACKEND")()


def get_retriever():
    cfg = get_app_settings()
    retriever_cls = import_from_setting("VECTOR_STORE_CLASS")
    return retriever_cls(get_embedding_backend(), distance_strategy=cfg.default_distance_strategy)


def _checksum(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@transaction.atomic
def ingest_text(
    *,
    text: str,
    title: str,
    external_id: str = "",
    metadata: dict | None = None,
    source_type: str = Document.SourceType.TEXT,
) -> Document:
    document, _created = Document.objects.update_or_create(
        external_id=external_id or f"inline-{_checksum(title + text)[:12]}",
        defaults={
            "title": title,
            "source_type": source_type,
            "raw_text": text,
            "metadata": metadata or {},
            "status": Document.Status.PROCESSING,
            "checksum": _checksum(text),
        },
    )
    get_task_backend().enqueue_document_ingestion(document.id)
    document.refresh_from_db()
    return document


def ingest_document(
    *,
    title: str,
    source_type: str,
    raw_text: str = "",
    source_pointer: str = "",
    external_id: str = "",
    metadata: dict | None = None,
) -> Document:
    document, _created = Document.objects.update_or_create(
        external_id=external_id or f"doc-{_checksum(title + source_pointer + raw_text)[:12]}",
        defaults={
            "title": title,
            "source_type": source_type,
            "raw_text": raw_text,
            "source_pointer": source_pointer,
            "metadata": metadata or {},
            "status": Document.Status.PROCESSING,
            "checksum": _checksum(raw_text or source_pointer),
        },
    )
    get_task_backend().enqueue_document_ingestion(document.id)
    document.refresh_from_db()
    return document


def index_text(**kwargs) -> Document:
    return ingest_text(**kwargs)


def index_document(**kwargs) -> Document:
    return ingest_document(**kwargs)


@transaction.atomic
def reindex_document(document_id: int) -> Document:
    from django_agent_rag.services.chunking import chunk_document
    from django_agent_rag.services.embeddings import embed_document

    document = Document.objects.get(id=document_id)
    document.status = Document.Status.PROCESSING
    document.updated_at = timezone.now()
    document.save(update_fields=["status", "updated_at"])
    chunk_document(document_id)
    embed_document(document_id)
    document.refresh_from_db()
    return document


@transaction.atomic
def delete_document(document_id: int, hard_delete: bool = False) -> None:
    document = Document.objects.get(id=document_id)
    if hard_delete:
        document.delete()
        return
    Chunk.objects.filter(document=document).delete()
    document.status = Document.Status.DELETED
    document.save(update_fields=["status", "updated_at"])

