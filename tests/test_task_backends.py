from unittest.mock import MagicMock, patch

import pytest

from django_agent_rag.backends.tasks.celery_backend import CeleryTaskBackend
from django_agent_rag.backends.tasks.sync import SyncTaskBackend
from django_agent_rag.backends.tasks.temporal_backend import TemporalTaskBackend
from django_agent_rag.exceptions import OptionalDependencyMissing


def test_sync_backend_name():
    assert SyncTaskBackend().backend_name() == "sync"


def test_celery_backend_smoke():
    with patch("django_agent_rag.backends.tasks.celery_backend.optional_module_available", return_value=True):
        backend = CeleryTaskBackend()
        with patch("django_agent_rag.celery_tasks.process_document_reindex") as task:
            task.delay = MagicMock()
            backend.enqueue_reindex(1)
            task.delay.assert_called_once_with(1)


def test_temporal_backend_requires_optional_dependency():
    with patch("django_agent_rag.backends.tasks.temporal_backend.optional_module_available", return_value=False):
        with pytest.raises(OptionalDependencyMissing):
            TemporalTaskBackend()

