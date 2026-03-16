# django-agent-rag

Installable RAG infrastructure for Django projects.

`django-agent-rag` is a reusable Django app that adds document ingestion, chunking, embeddings, pgvector-backed retrieval, context assembly, pluggable LLM backends, pluggable embedding backends, and optional async execution backends.

It is:

- Django-first
- provider-agnostic
- PostgreSQL + pgvector focused
- sync by default
- optionally integrated with Celery and Temporal

It is not:

- a full UI product
- a full authentication package
- tied to a single model vendor
- a giant agent framework

## Features

- Install with `pip install django-agent-rag`
- Add to `INSTALLED_APPS`
- Manage source documents, chunks, conversations, retrieval runs, and agent runs
- Use pgvector as the v1 vector store
- Swap LLM and embedding providers through import-string based settings
- Run ingestion synchronously or through Celery or Temporal adapters
- Use management commands and Django admin for operations
- Develop locally with built-in fake providers

## Installation

```bash
pip install django-agent-rag
```

From this repository during development:

```bash
pip install -e .
```

If you use `pyenv`, this repository includes `.python-version` set to `django-agent-rag`, so entering the project directory can select that environment automatically when `pyenv` is configured in your shell.

Optional extras:

```bash
pip install "django-agent-rag[celery]"
pip install "django-agent-rag[temporal]"
pip install "django-agent-rag[dev]"
```

Developer setup from source:

```bash
pip install -r requirements-dev.txt
```

Add the app:

```python
INSTALLED_APPS = [
    # ...
    "pgvector.django",
    "django_agent_rag",
]
```

Configure `DJANGO_AGENT_RAG`:

```python
DJANGO_AGENT_RAG = {
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
}
```

Run migrations:

```bash
python manage.py migrate
```

## PostgreSQL and pgvector

v1 supports PostgreSQL only. The package ships a migration that creates the `vector` extension with `CREATE EXTENSION IF NOT EXISTS vector;`.

Local development stack:

```bash
docker compose up -d postgres redis
```

## Basic usage

```python
from django_agent_rag import ask, index_text, retrieve

document = index_text(
    text="Django apps can be packaged and reused.",
    title="Reusable apps",
    external_id="doc-1",
    metadata={"topic": "django"},
)

results = retrieve("How does Django support reuse?", top_k=3)
response = ask("How does Django support reuse?", top_k=3)
```

## Sync usage

Sync is the default backend. Service functions call chunking and embedding inline:

```python
from django_agent_rag.services import ingest_text

document = ingest_text(text="hello world", title="Greeting")
```

## Celery usage

Install the extra:

```bash
pip install "django-agent-rag[celery]"
```

Switch the task backend:

```python
DJANGO_AGENT_RAG = {
    # ...
    "TASK_BACKEND": "django_agent_rag.backends.tasks.celery_backend.CeleryTaskBackend",
}
```

Then wire Celery in your project and import `django_agent_rag.celery_tasks`.

## Temporal usage

Install the extra:

```bash
pip install "django-agent-rag[temporal]"
```

Switch the task backend:

```python
DJANGO_AGENT_RAG = {
    # ...
    "TASK_BACKEND": "django_agent_rag.backends.tasks.temporal_backend.TemporalTaskBackend",
}
```

Temporal remains optional. It requires a Temporal service, workers, and task queue configuration. The package isolates Temporal imports so base installs still work.

## Custom embedding backend

```python
from django_agent_rag.backends.embeddings.base import EmbeddingBackend


class MyEmbeddingBackend(EmbeddingBackend):
    def embed_text(self, text: str) -> list[float]:
        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [[0.0, 1.0, 0.0] for _ in texts]

    def dimensions(self) -> int:
        return 3

    def provider_name(self) -> str:
        return "my-embeddings"
```

## Custom LLM backend

```python
from django_agent_rag.backends.llm.base import LLMBackend
from django_agent_rag.types import LLMResponse


class MyLLMBackend(LLMBackend):
    def generate(self, prompt: str, system_prompt: str | None = None, context: list[str] | None = None, **kwargs) -> LLMResponse:
        return LLMResponse(
            text=f"Prompt: {prompt}",
            provider=self.provider_name(),
            raw={"context": context or []},
        )

    def provider_name(self) -> str:
        return "my-llm"
```

## Running tests

```bash
make test
```

The test suite expects PostgreSQL for vector integration tests. Temporal tests skip gracefully when the dependency or service is unavailable.

## Linting and packaging

```bash
make lint
make format
make check-dist
```

`make check-dist` builds the sdist and wheel, then runs `twine check` to validate the package metadata before publishing.

## Local development

```bash
make install-dev
docker compose up -d
make migrate
make test
```

See [`examples/demo_project`](examples/demo_project) for a minimal Django project wired to the package.

## Publishing to PyPI

1. Update the version in `pyproject.toml`.
2. Run `make check-dist`.
3. Upload `dist/*` with Twine, or use the included GitHub Actions publishing workflow with PyPI trusted publishing.
