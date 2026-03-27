"""Indexer for building the vector store."""

from __future__ import annotations

from llama_index.core import VectorStoreIndex

from src.rag.loader import DocumentLoader
from src.rag.splitter import TextSplitter
from src.rag.embedder import get_storage_context, get_chroma_client, Embedder


def index_documents() -> None:
    """Index all documents into the vector store."""
    from src.config.settings import settings

    # Ensure directories exist
    settings.chroma_dir.mkdir(parents=True, exist_ok=True)
    settings.docs_output_dir.mkdir(parents=True, exist_ok=True)

    # Clear existing collection
    chroma_client = get_chroma_client()
    try:
        chroma_client.delete_collection(settings.chroma_collection_name)
    except Exception:
        pass

    # Load documents
    loader = DocumentLoader()
    try:
        texts = loader.load_as_texts()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Run 'python -m src scrape' first to download Angular documentation.")
        raise SystemExit(1) from e

    # Split into chunks
    splitter = TextSplitter()
    nodes = splitter.split(texts)

    # Create index with storage context
    embedder = Embedder()
    storage_context = get_storage_context()
    index = VectorStoreIndex(
        nodes=nodes,
        storage_context=storage_context,
        embed_model=embedder.get_model(),
    )

    print(f"Indexed {len(nodes)} chunks from {len(texts)} documents")


if __name__ == "__main__":
    index_documents()
