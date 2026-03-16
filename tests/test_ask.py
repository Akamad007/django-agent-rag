import pytest

from django_agent_rag.models import AgentRun, RetrievalRun
from django_agent_rag.services import ask, ingest_text


@pytest.mark.django_db
def test_ask_logs_runs():
    ingest_text(text="Django has reusable apps.", title="Django", external_id="django")
    response = ask("What does Django have?")
    assert "Django" in response.text
    assert RetrievalRun.objects.exists()
    assert AgentRun.objects.exists()
