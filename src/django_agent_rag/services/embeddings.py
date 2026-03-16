from __future__ import annotations

from django.db import transaction

from django_agent_rag.models import Chunk, Document
from django_agent_rag.services.ingestion import get_embedding_backend


@transaction.atomic
def embed_document(document_id: int, chunk_ids: list[int] | None = None) -> list[Chunk]:
    backend = get_embedding_backend()
    queryset = Chunk.objects.filter(document_id=document_id)
    if chunk_ids:
        queryset = queryset.filter(id__in=chunk_ids)
    chunks = list(queryset.order_by("chunk_index"))
    vectors = backend.embed_texts([chunk.text for chunk in chunks])
    for chunk, vector in zip(chunks, vectors, strict=False):
        chunk.vector = vector
        chunk.embedding_status = Chunk.EmbeddingStatus.READY
        chunk.embedding_provider = backend.provider_name()
    Chunk.objects.bulk_update(chunks, ["vector", "embedding_status", "embedding_provider", "updated_at"])
    Document.objects.filter(id=document_id).update(status=Document.Status.READY)
    return chunks

