import pytest

from django_agent_rag.models import Chunk, Document


@pytest.mark.django_db
def test_document_and_chunk_models():
    document = Document.objects.create(title="Test", raw_text="hello", checksum="abc")
    chunk = Chunk.objects.create(document=document, chunk_index=0, text="hello", char_length=5)
    assert str(document) == "Test"
    assert str(chunk) == f"{document.id}:0"

