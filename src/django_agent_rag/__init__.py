from __future__ import annotations

from typing import Any

default_app_config = "django_agent_rag.apps.DjangoAgentRagConfig"


def index_text(*args: Any, **kwargs: Any):
    from django_agent_rag.services import index_text as service

    return service(*args, **kwargs)


def index_document(*args: Any, **kwargs: Any):
    from django_agent_rag.services import index_document as service

    return service(*args, **kwargs)


def retrieve(*args: Any, **kwargs: Any):
    from django_agent_rag.services import retrieve as service

    return service(*args, **kwargs)


def ask(*args: Any, **kwargs: Any):
    from django_agent_rag.services import ask as service

    return service(*args, **kwargs)


def delete_document(*args: Any, **kwargs: Any):
    from django_agent_rag.services import delete_document as service

    return service(*args, **kwargs)


__all__ = ["ask", "delete_document", "index_document", "index_text", "retrieve"]
