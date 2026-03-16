import pytest

from django_agent_rag.services import ingest_text, retrieve


@pytest.mark.django_db
def test_retrieve_returns_ranked_chunks():
    ingest_text(
        text="Django reusable apps are packaged Python code.",
        title="Docs",
        external_id="doc-1",
    )
    results = retrieve("reusable apps", top_k=1)
    assert len(results) == 1
    assert results[0].document_title == "Docs"
