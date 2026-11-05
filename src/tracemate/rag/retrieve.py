from pathlib import Path

from tracemate.config import get_settings
from tracemate.providers.factory import get_embedding_provider
from tracemate.rag.vector_store import VectorStore


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    persist_directory = project_root / "data" / "chroma"

    settings = get_settings()
    embedding_provider = get_embedding_provider(settings)

    vector_store = VectorStore(
        embedding_provider=embedding_provider,
        persist_directory=str(persist_directory),
    )

    question = input("Ask a Java DSA question: ")

    results = vector_store.search(question, top_k=3)

    if not results:
        print("No relevant documents found.")
        return

    print("\nRetrieved knowledge:\n")

    for index, result in enumerate(results, start=1):
        print(f"--- Result {index} ---")
        print(f"Source: {result['metadata']['source']}")
        print(f"Distance: {result['distance']:.4f}")
        print(result["text"])
        print()


if __name__ == "__main__":
    main()