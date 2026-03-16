from django_agent_rag.chunkers.simple import SimpleChunker


def test_simple_chunker_splits_with_overlap():
    chunker = SimpleChunker()
    chunks = chunker.chunk("abcdefghij", chunk_size=4, chunk_overlap=1)
    assert [chunk.text for chunk in chunks] == ["abcd", "defg", "ghij"]

