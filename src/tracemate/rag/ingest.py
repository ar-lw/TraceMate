from pathlib import Path

from tracemate.config import get_settings
from tracemate.providers.factory import get_embedding_provider
from tracemate.rag.chunker import chunk_documents
from tracemate.rag.loader import load_markdown_documents
from tracemate.rag.vector_store import VectorStore


def main() -> None:
    project_root = Path(__file__).resolve().parents[3]
    knowledge_base_dir = project_root / "knowledge_base"
    persist_directory = project_root / "data" / "chroma"

    settings = get_settings()
    embedding_provider = get_embedding_provider(settings)

    documents = load_markdown_documents(knowledge_base_dir)
    chunks = chunk_documents(documents)

    print(f"Documents loaded: {len(documents)}")
    print(f"Chunks generated: {len(chunks)}")

    vector_store = VectorStore(
        embedding_provider=embedding_provider,
        persist_directory=str(persist_directory),
    )

    vector_store.reset_collection()
    vector_store.add_chunks(chunks)

    print(f"Chunks stored: {vector_store.collection.count()}")
    print("Knowledge base ingestion completed.")


if __name__ == "__main__":
    main()