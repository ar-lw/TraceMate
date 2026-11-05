from tracemate.config import get_settings
from tracemate.providers.factory import (
    get_embedding_provider,
    get_llm_provider,
)


def main() -> None:
    settings = get_settings()
    print(f"LLM provider: {settings.llm_provider}")
    print(f"Embedding provider: {settings.embedding_provider}")

    llm = get_llm_provider(settings)
    answer = llm.generate(
        "Explain what a linked list is in two concise sentences.",
        system_instruction=(
            "You are TraceMate, a precise Java DSA tutor. "
            "Use simple language and avoid giving unnecessary detail."
        ),
    )
    print("\nGemini response:\n")
    print(answer)

    embeddings = get_embedding_provider(settings).embed(
        ["A linked list stores elements in nodes connected by references."]
    )
    print(f"\nEmbedding dimensions: {len(embeddings[0])}")


if __name__ == "__main__":
    main()
