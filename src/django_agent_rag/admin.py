from __future__ import annotations

from django.contrib import admin

from django_agent_rag.models import AgentRun, Chunk, Conversation, Document, RetrievalRun
from django_agent_rag.services import delete_document, get_task_backend


@admin.action(description="Enqueue reindex for selected documents")
def enqueue_reindex(_modeladmin, _request, queryset):
    backend = get_task_backend()
    for document in queryset:
        backend.enqueue_reindex(document.id)


@admin.action(description="Enqueue re-embed for selected documents")
def enqueue_reembed(_modeladmin, _request, queryset):
    backend = get_task_backend()
    for document in queryset:
        backend.enqueue_embedding(document.id)


@admin.action(description="Delete chunks for selected documents")
def delete_chunks(_modeladmin, _request, queryset):
    for document in queryset:
        document.chunks.all().delete()


@admin.action(description="Soft delete selected documents")
def soft_delete_documents(_modeladmin, _request, queryset):
    for document in queryset:
        delete_document(document.id, hard_delete=False)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "external_id", "source_type", "status", "chunk_count", "updated_at")
    search_fields = ("title", "external_id", "status")
    list_filter = ("source_type", "status", "created_at", "updated_at")
    actions = [enqueue_reindex, enqueue_reembed, delete_chunks, soft_delete_documents]

    @admin.display(ordering="id")
    def chunk_count(self, obj: Document) -> int:
        return obj.chunks.count()


@admin.register(Chunk)
class ChunkAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "chunk_index", "embedding_status", "embedding_provider", "updated_at")
    search_fields = ("document__title", "document__external_id", "text")
    list_filter = ("embedding_status", "embedding_provider", "updated_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "session_id", "actor_id", "updated_at")
    search_fields = ("session_id", "actor_id")


@admin.register(RetrievalRun)
class RetrievalRunAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "llm_provider", "execution_backend", "latency_ms", "created_at")
    search_fields = ("query", "llm_provider", "execution_backend")
    list_filter = ("llm_provider", "execution_backend", "created_at")


@admin.register(AgentRun)
class AgentRunAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "llm_provider", "status", "created_at")
    search_fields = ("query", "llm_provider", "status")
    list_filter = ("status", "llm_provider", "created_at")

