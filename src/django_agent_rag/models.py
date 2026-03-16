from __future__ import annotations

from django.db import models
from pgvector.django import VectorField

from django_agent_rag.managers import DocumentManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Document(TimeStampedModel):
    class SourceType(models.TextChoices):
        TEXT = "text", "Text"
        FILE = "file", "File reference"
        URL = "url", "URL reference"
        MANUAL = "manual", "Manual content"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        READY = "ready", "Ready"
        ERROR = "error", "Error"
        DELETED = "deleted", "Deleted"

    external_id = models.CharField(max_length=255, blank=True, db_index=True)
    title = models.CharField(max_length=255)
    source_type = models.CharField(
        max_length=20,
        choices=SourceType.choices,
        default=SourceType.TEXT,
    )
    raw_text = models.TextField(blank=True)
    source_pointer = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    checksum = models.CharField(max_length=128, blank=True, db_index=True)

    objects = DocumentManager()

    class Meta:
        indexes = [
            models.Index(fields=["source_type", "status"]),
            models.Index(fields=["title"]),
        ]

    def __str__(self) -> str:
        return self.title


class Chunk(TimeStampedModel):
    class EmbeddingStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        READY = "ready", "Ready"
        ERROR = "error", "Error"

    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.PositiveIntegerField()
    text = models.TextField()
    char_length = models.PositiveIntegerField(default=0)
    token_length = models.PositiveIntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    embedding_status = models.CharField(
        max_length=20,
        choices=EmbeddingStatus.choices,
        default=EmbeddingStatus.PENDING,
        db_index=True,
    )
    embedding_provider = models.CharField(max_length=255, blank=True)
    vector = VectorField(null=True, blank=True)

    class Meta:
        ordering = ["document_id", "chunk_index"]
        unique_together = [("document", "chunk_index")]
        indexes = [
            models.Index(fields=["document", "embedding_status"]),
        ]

    def __str__(self) -> str:
        return f"{self.document_id}:{self.chunk_index}"


class Conversation(TimeStampedModel):
    session_id = models.CharField(max_length=255, unique=True)
    actor_id = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.session_id


class RetrievalRun(TimeStampedModel):
    conversation = models.ForeignKey(
        Conversation,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="retrieval_runs",
    )
    query = models.TextField()
    selected_document_ids = models.JSONField(default=list, blank=True)
    selected_chunk_ids = models.JSONField(default=list, blank=True)
    embedding_provider = models.CharField(max_length=255, blank=True)
    llm_provider = models.CharField(max_length=255, blank=True)
    execution_backend = models.CharField(max_length=255, blank=True)
    latency_ms = models.PositiveIntegerField(null=True, blank=True)
    prompt_tokens = models.PositiveIntegerField(null=True, blank=True)
    completion_tokens = models.PositiveIntegerField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"RetrievalRun({self.id})"


class AgentRun(TimeStampedModel):
    class Status(models.TextChoices):
        SUCCESS = "success", "Success"
        ERROR = "error", "Error"

    retrieval_run = models.ForeignKey(
        RetrievalRun,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="agent_runs",
    )
    query = models.TextField()
    response_text = models.TextField(blank=True)
    llm_provider = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUCCESS)
    error_message = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return f"AgentRun({self.id})"
