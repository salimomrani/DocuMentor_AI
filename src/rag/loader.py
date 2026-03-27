"""Document loader for RAG pipeline."""

from __future__ import annotations

import json
from pathlib import Path

from src.config.settings import settings


class DocumentLoader:
    """Loads scraped documents from JSON."""

    def __init__(self, docs_path: Path | None = None) -> None:
        self.docs_path = docs_path or (settings.docs_output_dir / "angular_docs.json")

    def load(self) -> list[dict[str, str]]:
        """Load documents from JSON file."""
        if not self.docs_path.exists():
            raise FileNotFoundError(f"Documents not found: {self.docs_path}")

        with open(self.docs_path, encoding="utf-8") as f:
            return json.load(f)

    def load_as_texts(self) -> list[tuple[str, dict]]:
        """Load documents as (text, metadata) tuples."""
        docs = self.load()
        result = []
        for doc in docs:
            text = f"{doc['title']}\n\n{doc['content']}"
            metadata = {"url": doc["url"], "title": doc["title"]}
            result.append((text, metadata))
        return result
