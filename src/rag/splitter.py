"""Text splitter for RAG pipeline."""

from __future__ import annotations

from llama_index.core.node_parser import SentenceSplitter

from src.config.settings import settings


class TextSplitter:
    """Splits documents into chunks for embedding."""

    def __init__(
        self,
        chunk_size: int = settings.chunk_size,
        chunk_overlap: int = settings.chunk_overlap,
    ) -> None:
        self.splitter = SentenceSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def split(self, texts: list[tuple[str, dict]]) -> list:
        """Split texts into chunks with metadata."""
        documents = []
        for text, metadata in texts:
            from llama_index.core import Document

            doc = Document(text=text, metadata=metadata)
            documents.append(doc)

        nodes = self.splitter.get_nodes_from_documents(documents)
        return nodes
