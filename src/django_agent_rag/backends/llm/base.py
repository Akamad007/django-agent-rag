from __future__ import annotations

from abc import ABC, abstractmethod

from django_agent_rag.types import LLMResponse


class LLMBackend(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        context: list[str] | None = None,
        **kwargs,
    ) -> LLMResponse:
        raise NotImplementedError

    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

