
import chromadb

from tracemate.providers.base import EmbeddingProvider


class VectorStore:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        persist_directory: str = "data/chroma",
        collection_name: str = "tracemate_knowledge",
    ):
        self.embedding_provider = embedding_provider

        self.client = chromadb.PersistentClient(
            path=persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def add_chunks(self, chunks: list[dict]) -> None:
        if not chunks:
            return

        documents = [chunk["text"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        ids = [
            f"{metadata['source']}:{metadata['chunk_index']}"
            for metadata in metadatas
        ]

        embeddings = self.embedding_provider.embed(documents)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        if not query.strip():
            return []

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        collection_count = self.collection.count()

        if collection_count == 0:
            return []

        query_embedding = self.embedding_provider.embed([query])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, collection_count),
        )

        matches = []

        if not results["documents"] or not results["documents"][0]:
            return matches

        for i, document in enumerate(results["documents"][0]):
            matches.append({
                "text": document,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
            })

        return matches
