from __future__ import annotations

import os

import pytest


def pytest_collection_modifyitems(config, items):
    if os.getenv("SKIP_DB_TESTS") == "1":
        skip_marker = pytest.mark.skip(reason="Database-backed tests skipped.")
        for item in items:
            if "db" in item.keywords:
                item.add_marker(skip_marker)


@pytest.fixture
def rag_settings(settings):
    settings.DJANGO_AGENT_RAG = settings.DJANGO_AGENT_RAG.copy()
    return settings.DJANGO_AGENT_RAG
