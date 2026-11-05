from pathlib import Path

from tracemate.rag.loader import load_markdown_documents
from tracemate.rag.chunker import chunk_documents


def main():
    knowledge_base_path = Path("knowledge_base")

    documents = load_markdown_documents(knowledge_base_path)
    print(f"Documents loaded: {len(documents)}")

    chunks = chunk_documents(documents)

    print(f"Total chunks created: {len(chunks)}")

    for chunk in chunks:
        print("\n" + "=" * 50)
        print("Source:", chunk["metadata"]["source"])
        print("Chunk:", chunk["metadata"]["chunk_index"])
        print("Characters:", len(chunk["text"]))
        print(chunk["text"][:200])


if __name__ == "__main__":
    main()