from __future__ import annotations

from django_agent_rag.chunkers.base import Chunker
from django_agent_rag.types import ChunkPayload


class SimpleChunker(Chunker):
    def chunk(self, text: str, **kwargs) -> list[ChunkPayload]:
        chunk_size = int(kwargs.get("chunk_size", 500))
        overlap = int(kwargs.get("chunk_overlap", 50))
        if overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size.")
        payloads: list[ChunkPayload] = []
        start = 0
        index = 0
        while start < len(text):
            end = min(len(text), start + chunk_size)
            chunk_text = text[start:end]
            payloads.append(
                ChunkPayload(
                    text=chunk_text,
                    chunk_index=index,
                    char_length=len(chunk_text),
                    token_length=len(chunk_text.split()),
                    metadata={"start": start, "end": end},
                )
            )
            if end == len(text):
                break
            start = end - overlap
            index += 1
        if not payloads and text == "":
            payloads.append(
                ChunkPayload(
                    text="",
                    chunk_index=0,
                    char_length=0,
                    token_length=0,
                    metadata={"start": 0, "end": 0},
                )
            )
        return payloads
