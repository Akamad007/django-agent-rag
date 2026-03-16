from django.apps import AppConfig


class DjangoAgentRagConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_agent_rag"
    verbose_name = "Django Agent RAG"

    def ready(self) -> None:
        from . import checks  # noqa: F401

