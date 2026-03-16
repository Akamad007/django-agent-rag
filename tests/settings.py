from __future__ import annotations

import os

SECRET_KEY = "tests"
DEBUG = True
USE_TZ = True
ROOT_URLCONF = "tests.urls"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "pgvector.django",
    "django_agent_rag",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB", "django_agent_rag"),
        "USER": os.getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

DJANGO_AGENT_RAG = {
    "EMBEDDING_BACKEND": "django_agent_rag.backends.embeddings.fake.FakeEmbeddingBackend",
    "LLM_BACKEND": "django_agent_rag.backends.llm.fake.FakeLLMBackend",
    "TASK_BACKEND": "django_agent_rag.backends.tasks.sync.SyncTaskBackend",
    "CHUNKER_CLASS": "django_agent_rag.chunkers.simple.SimpleChunker",
}

