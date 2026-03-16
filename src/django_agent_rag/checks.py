from django.core.checks import Error, register

from django_agent_rag.settings import get_raw_settings, import_from_setting


@register()
def django_agent_rag_settings_check(_app_configs, **_kwargs):
    errors = []
    for setting_name in (
        "VECTOR_STORE_CLASS",
        "EMBEDDING_BACKEND",
        "LLM_BACKEND",
        "TASK_BACKEND",
        "CHUNKER_CLASS",
    ):
        try:
            import_from_setting(setting_name)
        except Exception as exc:
            errors.append(Error(str(exc), id=f"django_agent_rag.E{setting_name}"))
    data = get_raw_settings()
    if data["DEFAULT_CHUNK_OVERLAP"] >= data["DEFAULT_CHUNK_SIZE"]:
        errors.append(
            Error(
                "DEFAULT_CHUNK_OVERLAP must be smaller than DEFAULT_CHUNK_SIZE.",
                id="django_agent_rag.E001",
            )
        )
    return errors
