import pytest

from django_agent_rag.models import Chunk, Document
from django_agent_rag.services import ingest_text


@pytest.mark.django_db
def test_ingest_text_creates_document_and_chunks():
    document = ingest_text(text="hello world " * 100, title="Greeting", external_id="greeting")
    assert Document.objects.get(id=document.id).status == Document.Status.READY
    assert Chunk.objects.filter(document=document).exists()

