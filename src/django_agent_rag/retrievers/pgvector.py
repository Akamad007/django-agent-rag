from __future__ import annotations

from django.db.models import QuerySet
from pgvector.django import CosineDistance, L2Distance, MaxInnerProduct

from django_agent_rag.models import Chunk
from django_agent_rag.types import RetrievedChunk

DISTANCE_MAP = {
    "cosine": CosineDistance,
    "l2": L2Distance,
    "max_inner_product": MaxInnerProduct,
}


class PGVectorRetriever:
    def __init__(self, embedding_backend, distance_strategy: str = "cosine") -> None:
        self.embedding_backend = embedding_backend
        self.distance_strategy = distance_strategy

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict | None = None,
    ) -> list[RetrievedChunk]:
        vector = self.embedding_backend.embed_text(query)
        queryset: QuerySet[Chunk] = Chunk.objects.select_related("document").filter(
            embedding_status=Chunk.EmbeddingStatus.READY
        )
        if filters:
            if "document_id" in filters:
                queryset = queryset.filter(document_id=filters["document_id"])
            if "document_ids" in filters:
                queryset = queryset.filter(document_id__in=filters["document_ids"])
            if "source_type" in filters:
                queryset = queryset.filter(document__source_type=filters["source_type"])
        distance_cls = DISTANCE_MAP.get(self.distance_strategy, CosineDistance)
        queryset = queryset.annotate(
            distance=distance_cls("vector", vector)
        ).order_by("distance")[:top_k]
        return [
            RetrievedChunk(
                chunk_id=chunk.id,
                document_id=chunk.document_id,
                document_title=chunk.document.title,
                text=chunk.text,
                score=(
                    float(getattr(chunk, "distance", 0.0))
                    if getattr(chunk, "distance", None) is not None
                    else None
                ),
                metadata=chunk.metadata,
            )
            for chunk in queryset
        ]
