from django_agent_rag.backends.embeddings.fake import FakeEmbeddingBackend
from django_agent_rag.backends.llm.fake import FakeLLMBackend


def test_fake_embedding_backend_dimensions():
    backend = FakeEmbeddingBackend()
    vector = backend.embed_text("hello")
    assert len(vector) == backend.dimensions()


def test_fake_llm_backend_response():
    backend = FakeLLMBackend()
    response = backend.generate("hello", context=["world"])
    assert response.provider == backend.provider_name()
    assert "hello" in response.text

