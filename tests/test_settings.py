import pytest
from django.test import override_settings

from django_agent_rag.exceptions import ConfigurationError
from django_agent_rag.settings import get_app_settings, import_from_setting


def test_default_settings_load():
    settings = get_app_settings()
    assert settings.default_top_k == 5


@override_settings(DJANGO_AGENT_RAG={"EMBEDDING_BACKEND": "does.not.exist"})
def test_invalid_import_raises_configuration_error():
    with pytest.raises(ConfigurationError):
        import_from_setting("EMBEDDING_BACKEND")

