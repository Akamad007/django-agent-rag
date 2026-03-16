from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from django.conf import settings
from django.utils.module_loading import import_string

from django_agent_rag.exceptions import ConfigurationError


DEFAULTS: dict[str, Any] = {
    "VECTOR_STORE_CLASS": "django_agent_rag.retrievers.pgvector.PGVectorRetriever",
    "EMBEDDING_BACKEND": "django_agent_rag.backends.embeddings.fake.FakeEmbeddingBackend",
    "LLM_BACKEND": "django_agent_rag.backends.llm.fake.FakeLLMBackend",
    "TASK_BACKEND": "django_agent_rag.backends.tasks.sync.SyncTaskBackend",
    "CHUNKER_CLASS": "django_agent_rag.chunkers.simple.SimpleChunker",
    "DEFAULT_CHUNK_SIZE": 500,
    "DEFAULT_CHUNK_OVERLAP": 50,
    "DEFAULT_TOP_K": 5,
    "AUTO_CREATE_EXTENSION": True,
    "DEFAULT_DISTANCE_STRATEGY": "cosine",
    "ENABLE_ADMIN": True,
    "ENABLE_MANAGEMENT_COMMANDS": True,
    "TEMPORAL_TASK_QUEUE": "django-agent-rag",
    "TEMPORAL_WORKFLOW": "django_agent_rag.temporal.workflows.DocumentWorkflow",
}


@dataclass(frozen=True, slots=True)
class AppSettings:
    vector_store_class: str
    embedding_backend: str
    llm_backend: str
    task_backend: str
    chunker_class: str
    default_chunk_size: int
    default_chunk_overlap: int
    default_top_k: int
    auto_create_extension: bool
    default_distance_strategy: str
    enable_admin: bool
    enable_management_commands: bool
    temporal_task_queue: str
    temporal_workflow: str


def get_raw_settings() -> dict[str, Any]:
    raw = getattr(settings, "DJANGO_AGENT_RAG", {})
    if not isinstance(raw, dict):
        raise ConfigurationError("DJANGO_AGENT_RAG must be a dict.")
    merged = DEFAULTS.copy()
    merged.update(raw)
    return merged


def get_app_settings() -> AppSettings:
    data = get_raw_settings()
    return AppSettings(
        vector_store_class=data["VECTOR_STORE_CLASS"],
        embedding_backend=data["EMBEDDING_BACKEND"],
        llm_backend=data["LLM_BACKEND"],
        task_backend=data["TASK_BACKEND"],
        chunker_class=data["CHUNKER_CLASS"],
        default_chunk_size=int(data["DEFAULT_CHUNK_SIZE"]),
        default_chunk_overlap=int(data["DEFAULT_CHUNK_OVERLAP"]),
        default_top_k=int(data["DEFAULT_TOP_K"]),
        auto_create_extension=bool(data["AUTO_CREATE_EXTENSION"]),
        default_distance_strategy=str(data["DEFAULT_DISTANCE_STRATEGY"]),
        enable_admin=bool(data["ENABLE_ADMIN"]),
        enable_management_commands=bool(data["ENABLE_MANAGEMENT_COMMANDS"]),
        temporal_task_queue=str(data["TEMPORAL_TASK_QUEUE"]),
        temporal_workflow=str(data["TEMPORAL_WORKFLOW"]),
    )


def import_from_setting(setting_name: str) -> Any:
    raw = get_raw_settings()[setting_name]
    try:
        return import_string(raw)
    except Exception as exc:
        raise ConfigurationError(f"Could not import {setting_name} from '{raw}'.") from exc


def optional_module_available(module_name: str) -> bool:
    try:
        import_module(module_name)
    except Exception:
        return False
    return True

