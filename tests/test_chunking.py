from pathlib import Path

from tracemate.rag.loader import load_markdown_documents
from tracemate.rag.chunker import chunk_documents


def test_knowledge_base_loading():
    documents = load_markdown_documents(Path("knowledge_base"))

    assert len(documents) == 3


def test_chunk_generation():
    documents = load_markdown_documents(Path("knowledge_base"))
    chunks = chunk_documents(documents)

    assert len(chunks) > 0

    for chunk in chunks:
        assert chunk["text"].strip()
        assert "source" in chunk["metadata"]
        assert "chunk_index" in chunk["metadata"]