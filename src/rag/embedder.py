"""Embedder for RAG pipeline using Ollama."""

from __future__ import annotations

from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

from src.config.settings import settings


class Embedder:
    """Generates embeddings using Ollama."""

    def __init__(self) -> None:
        self.embed_model = OllamaEmbedding(
            model_name=settings.ollama_embed_model,
            base_url=settings.ollama_base_url,
        )

    def get_model(self) -> OllamaEmbedding:
        """Get the embedding model."""
        return self.embed_model


def get_chroma_client():
    """Get ChromaDB client."""
    import chromadb

    return chromadb.PersistentClient(path=str(settings.chroma_dir))


def get_vector_store() -> ChromaVectorStore:
    """Get ChromaDB vector store."""
    return ChromaVectorStore.from_params(
        persist_dir=str(settings.chroma_dir),
        collection_name=settings.chroma_collection_name,
    )


def get_storage_context():
    """Get storage context with vector store."""
    vector_store = get_vector_store()
    return StorageContext.from_defaults(vector_store=vector_store)
