"""Generator for RAG pipeline using Ollama."""

from __future__ import annotations

from dataclasses import dataclass

from llama_index.llms.ollama import Ollama

from src.config.settings import settings
from src.rag.retriever import Retriever


@dataclass
class Answer:
    """Generated answer with sources."""

    text: str
    sources: list[dict]
    is_not_documented: bool = False


class Generator:
    """Generates responses using LLM with RAG context."""

    def __init__(self) -> None:
        self.llm = Ollama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            timeout=settings.llm_timeout,
        )
        self.retriever = Retriever()

    def generate(self, query: str) -> Answer:
        """Generate an answer to the query using RAG."""
        # Retrieve relevant docs
        sources = self.retriever.get_sources(query)

        if not sources:
            return Answer(
                text="Non documenté — Aucune information trouvée dans la documentation Angular pour cette requête.",
                sources=[],
                is_not_documented=True,
            )

        # Build context from sources
        context = self._build_context(sources)

        # Build prompt with context
        prompt = self._build_prompt(query, context)

        # Generate response
        response = self.llm.complete(prompt)

        return Answer(
            text=response.text,
            sources=sources,
            is_not_documented=False,
        )

    def _build_context(self, sources: list[dict]) -> str:
        """Build context string from sources."""
        context_parts = []
        for i, source in enumerate(sources, 1):
            context_parts.append(
                f"--- Document {i} ---\n"
                f"Source: {source.get('title', 'Unknown')}\n"
                f"URL: {source.get('url', '')}\n"
                f"Content:\n{source.get('content', '')}\n"
            )
        return "\n\n".join(context_parts)

    def _build_prompt(self, query: str, context: str) -> str:
        """Build the full prompt with context."""
        return f"""Tu es un expert Angular. Utilise UNIQUEMENT les documents fournis pour répondre à la question.

INSTRUCTIONS:
- Réponds en français
- Sois concis et orienté action
- Cite les sources quand tu utilises des informations des documents
- Si l'information n'est pas dans les documents, dis "Non documenté"

DOCUMENTS:
{context}

QUESTION: {query}

RÉPONSE:"""
