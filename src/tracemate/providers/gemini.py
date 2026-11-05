from google import genai
from google.genai import types

from tracemate.config import Settings
from tracemate.providers.base import EmbeddingProvider, LLMProvider


class GeminiLLMProvider(LLMProvider):
    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your local .env file."
            )
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(self, prompt: str, system_instruction: str | None = None) -> str:
        config = None
        if system_instruction:
            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=config,
        )
        if not response.text:
            raise RuntimeError("Gemini returned an empty text response.")
        return response.text


class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your local .env file."
            )
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_embedding_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        response = self.client.models.embed_content(
            model=self.model,
            contents=texts,
        )
        if not response.embeddings:
            raise RuntimeError("Gemini returned no embeddings.")
        return [item.values for item in response.embeddings]
