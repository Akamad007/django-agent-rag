from __future__ import annotations

import time

from django_agent_rag.models import AgentRun, RetrievalRun
from django_agent_rag.services.ingestion import (
    get_embedding_backend,
    get_llm_backend,
    get_task_backend,
)
from django_agent_rag.services.retrieval import retrieve_context


def ask(
    query: str,
    system_prompt: str | None = None,
    top_k: int = 5,
    filters: dict | None = None,
    llm_backend=None,
):
    llm = llm_backend or get_llm_backend()
    task_backend = get_task_backend()
    embedding_backend = get_embedding_backend()
    start = time.perf_counter()
    retrieved = retrieve_context(query=query, top_k=top_k, filters=filters)
    context = [item.text for item in retrieved]
    response = llm.generate(prompt=query, system_prompt=system_prompt, context=context)
    latency_ms = int((time.perf_counter() - start) * 1000)
    retrieval_run = RetrievalRun.objects.create(
        query=query,
        selected_document_ids=list({item.document_id for item in retrieved}),
        selected_chunk_ids=[item.chunk_id for item in retrieved],
        embedding_provider=embedding_backend.provider_name(),
        llm_provider=llm.provider_name(),
        execution_backend=task_backend.backend_name(),
        latency_ms=latency_ms,
        prompt_tokens=response.prompt_tokens,
        completion_tokens=response.completion_tokens,
        metadata={"top_k": top_k, "filters": filters or {}},
    )
    AgentRun.objects.create(
        retrieval_run=retrieval_run,
        query=query,
        response_text=response.text,
        llm_provider=llm.provider_name(),
        status=AgentRun.Status.SUCCESS,
        metadata=response.raw,
    )
    return response
