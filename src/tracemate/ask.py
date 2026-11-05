from pathlib import Path

from tracemate.config import get_settings
from tracemate.providers.factory import (
    get_embedding_provider,
    get_llm_provider,
)
from tracemate.rag.qa import TraceMateRAG
from tracemate.rag.vector_store import VectorStore


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    persist_directory = project_root / "data" / "chroma"

    settings = get_settings()

    llm_provider = get_llm_provider(settings)
    embedding_provider = get_embedding_provider(settings)

    vector_store = VectorStore(
        embedding_provider=embedding_provider,
        persist_directory=str(persist_directory),
    )

    if vector_store.collection.count() == 0:
        print("Knowledge base is empty. Run the ingestion script first.")
        return

    assistant = TraceMateRAG(
        llm_provider=llm_provider,
        vector_store=vector_store,
    )

    print("TraceMate — Java DSA Assistant")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        try:
            result = assistant.answer_question(question)

            print("\nTraceMate:\n")
            print(result["answer"])

            print("\nSources:")
            for source in result["sources"]:
                print(f"- {source}")

            print("\n" + "-" * 60 + "\n")

        except Exception as error:
            print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()