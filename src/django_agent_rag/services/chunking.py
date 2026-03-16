from __future__ import annotations

from django.db import transaction

from django_agent_rag.models import Chunk, Document
from django_agent_rag.services.ingestion import get_chunker
from django_agent_rag.settings import get_app_settings


@transaction.atomic
def chunk_document(document_id: int) -> list[Chunk]:
    config = get_app_settings()
    document = Document.objects.get(id=document_id)
    chunker = get_chunker()
    payloads = chunker.chunk(
        document.raw_text,
        chunk_size=config.default_chunk_size,
        chunk_overlap=config.default_chunk_overlap,
    )
    document.chunks.all().delete()
    chunks = [
        Chunk(
            document=document,
            chunk_index=payload.chunk_index,
            text=payload.text,
            char_length=payload.char_length,
            token_length=payload.token_length,
            metadata=payload.metadata,
        )
        for payload in payloads
    ]
    created = Chunk.objects.bulk_create(chunks)
    return created
