from __future__ import annotations

from django_agent_rag.settings import get_app_settings
from django_agent_rag.services.ingestion import get_retriever


def retrieve_context(query: str, top_k: int = 5, filters: dict | None = None):
    if top_k <= 0:
        top_k = get_app_settings().default_top_k
    return get_retriever().retrieve(query=query, top_k=top_k, filters=filters)


def retrieve(query: str, top_k: int = 5, filters: dict | None = None):
    return retrieve_context(query=query, top_k=top_k, filters=filters)

