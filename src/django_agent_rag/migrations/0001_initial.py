from django.db import migrations, models
import django.db.models.deletion
import pgvector.django


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS vector;", reverse_sql=""),
        migrations.CreateModel(
            name="Conversation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("session_id", models.CharField(max_length=255, unique=True)),
                ("actor_id", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
            ],
        ),
        migrations.CreateModel(
            name="Document",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("external_id", models.CharField(blank=True, db_index=True, max_length=255)),
                ("title", models.CharField(max_length=255)),
                ("source_type", models.CharField(choices=[("text", "Text"), ("file", "File reference"), ("url", "URL reference"), ("manual", "Manual content")], default="text", max_length=20)),
                ("raw_text", models.TextField(blank=True)),
                ("source_pointer", models.CharField(blank=True, max_length=500)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("processing", "Processing"), ("ready", "Ready"), ("error", "Error"), ("deleted", "Deleted")], db_index=True, default="pending", max_length=20)),
                ("checksum", models.CharField(blank=True, db_index=True, max_length=128)),
            ],
            options={"indexes": [models.Index(fields=["source_type", "status"], name="django_agen_source__1061ee_idx"), models.Index(fields=["title"], name="django_agen_title_20dd3a_idx")]},
        ),
        migrations.CreateModel(
            name="RetrievalRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("query", models.TextField()),
                ("selected_document_ids", models.JSONField(blank=True, default=list)),
                ("selected_chunk_ids", models.JSONField(blank=True, default=list)),
                ("embedding_provider", models.CharField(blank=True, max_length=255)),
                ("llm_provider", models.CharField(blank=True, max_length=255)),
                ("execution_backend", models.CharField(blank=True, max_length=255)),
                ("latency_ms", models.PositiveIntegerField(blank=True, null=True)),
                ("prompt_tokens", models.PositiveIntegerField(blank=True, null=True)),
                ("completion_tokens", models.PositiveIntegerField(blank=True, null=True)),
                ("error_message", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("conversation", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="retrieval_runs", to="django_agent_rag.conversation")),
            ],
        ),
        migrations.CreateModel(
            name="Chunk",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("chunk_index", models.PositiveIntegerField()),
                ("text", models.TextField()),
                ("char_length", models.PositiveIntegerField(default=0)),
                ("token_length", models.PositiveIntegerField(blank=True, null=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("embedding_status", models.CharField(choices=[("pending", "Pending"), ("ready", "Ready"), ("error", "Error")], db_index=True, default="pending", max_length=20)),
                ("embedding_provider", models.CharField(blank=True, max_length=255)),
                ("vector", pgvector.django.VectorField(blank=True, null=True)),
                ("document", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="chunks", to="django_agent_rag.document")),
            ],
            options={"ordering": ["document_id", "chunk_index"], "unique_together": {("document", "chunk_index")}, "indexes": [models.Index(fields=["document", "embedding_status"], name="django_agen_documen_b12098_idx")]},
        ),
        migrations.CreateModel(
            name="AgentRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("query", models.TextField()),
                ("response_text", models.TextField(blank=True)),
                ("llm_provider", models.CharField(blank=True, max_length=255)),
                ("status", models.CharField(choices=[("success", "Success"), ("error", "Error")], default="success", max_length=20)),
                ("error_message", models.TextField(blank=True)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("retrieval_run", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="agent_runs", to="django_agent_rag.retrievalrun")),
            ],
        ),
    ]

