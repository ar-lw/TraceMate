
import math

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

        self.collection_name = collection_name

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def reset_collection(self) -> None:
        self.client.delete_collection(name=self.collection_name)

        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    @staticmethod
    def _validate_embeddings(
        embeddings: list[list[float]],
        expected_count: int,
    ) -> None:
        if len(embeddings) != expected_count:
            raise ValueError(
                f"Expected {expected_count} embeddings, "
                f"but received {len(embeddings)}."
            )

        if not embeddings:
            return

        dimensions = len(embeddings[0])

        if dimensions == 0:
            raise ValueError("Embeddings cannot be empty.")

        for index, embedding in enumerate(embeddings):
            if len(embedding) != dimensions:
                raise ValueError(
                    f"Embedding {index} has {len(embedding)} dimensions; "
                    f"expected {dimensions}."
                )

            try:
                valid = all(
                    math.isfinite(float(value))
                    for value in embedding
                )
            except (TypeError, ValueError, OverflowError):
                valid = False

            if not valid:
                raise ValueError(
                    f"Embedding {index} contains invalid numeric values."
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

        self._validate_embeddings(
            embeddings,
            expected_count=len(documents),
        )

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

        query_embeddings = self.embedding_provider.embed([query])

        self._validate_embeddings(
            query_embeddings,
            expected_count=1,
        )

        results = self.collection.query(
            query_embeddings=query_embeddings,
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
