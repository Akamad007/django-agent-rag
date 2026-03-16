from __future__ import annotations

from django_agent_rag.backends.llm.base import LLMBackend
from django_agent_rag.types import LLMResponse


class FakeLLMBackend(LLMBackend):
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        context: list[str] | None = None,
        **kwargs,
    ) -> LLMResponse:
        joined_context = "\n".join(context or [])
        text = f"system={system_prompt or ''}\nquestion={prompt}\ncontext={joined_context}".strip()
        return LLMResponse(
            text=text,
            provider=self.provider_name(),
            raw={"kwargs": kwargs, "context_count": len(context or [])},
            prompt_tokens=len(prompt.split()),
            completion_tokens=len(text.split()),
        )

    def provider_name(self) -> str:
        return "fake-llm"

