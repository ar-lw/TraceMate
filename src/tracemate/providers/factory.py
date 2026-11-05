from tracemate.config import Settings
from tracemate.providers.base import EmbeddingProvider, LLMProvider
from tracemate.providers.gemini import GeminiEmbeddingProvider, GeminiLLMProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_provider == "gemini":
        return GeminiLLMProvider(settings)
    if settings.llm_provider == "ollama":
        raise NotImplementedError("Ollama LLM provider is scheduled for Day 3.")
    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")


def get_embedding_provider(settings: Settings) -> EmbeddingProvider:
    if settings.embedding_provider == "gemini":
        return GeminiEmbeddingProvider(settings)
    if settings.embedding_provider == "ollama":
        raise NotImplementedError(
            "Ollama embedding provider is scheduled for Day 3."
        )
    raise ValueError(
        f"Unsupported embedding provider: {settings.embedding_provider}"
    )
