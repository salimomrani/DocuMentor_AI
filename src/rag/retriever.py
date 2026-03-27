"""Retriever for RAG pipeline."""

from __future__ import annotations

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

from src.config.settings import settings
from src.rag.embedder import get_vector_store, Embedder


class Retriever:
    """Retrieves relevant documents from vector store."""

    def __init__(self) -> None:
        try:
            self.vector_store = get_vector_store()
        except Exception:
            self.vector_store = None
        self._index: VectorStoreIndex | None = None

    @property
    def index(self) -> VectorStoreIndex | None:
        """Get or create the index."""
        if self._index is None:
            if self.vector_store is None:
                return None
            try:
                embedder = Embedder()
                self._index = VectorStoreIndex.from_vector_store(
                    self.vector_store,
                    embed_model=embedder.get_model(),
                )
            except Exception:
                return None
        return self._index

    def retrieve(self, query: str, top_k: int = settings.top_k) -> list:
        """Retrieve relevant chunks for a query."""
        if self.index is None:
            return []
        retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=top_k,
        )
        results = retriever.retrieve(query)
        return results

    def get_sources(self, query: str, top_k: int = settings.top_k) -> list[dict]:
        """Retrieve sources with metadata."""
        results = self.retrieve(query, top_k)
        sources = []
        for node in results:
            sources.append(
                {
                    "url": node.node.metadata.get("url", ""),
                    "title": node.node.metadata.get("title", ""),
                    "content": node.node.text[:200] + "..." if len(node.node.text) > 200 else node.node.text,
                }
            )
        return sources
