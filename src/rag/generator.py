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

    def generate(self, query: str, conversation_history: list[dict] | None = None) -> Answer:
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

        # Build conversation history
        history = self._build_history(conversation_history or [])

        # Build prompt with context
        prompt = self._build_prompt(query, context, history)

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

    def _build_history(self, conversation_history: list[dict]) -> str:
        """Build conversation history string."""
        if not conversation_history:
            return ""
        parts = []
        for msg in conversation_history:
            role = "Utilisateur" if msg.get("role") == "user" else "Assistant"
            parts.append(f"{role}: {msg.get('content', '')}")
        return "\n".join(parts)

    def _build_prompt(self, query: str, context: str, history: str = "") -> str:
        """Build the full prompt with context."""
        history_section = (
            f"""CONVERSATION PRÉCÉDENTE:
{history}

"""
            if history
            else ""
        )
        return f"""Tu es un expert Angular. Utilise UNIQUEMENT les documents fournis pour répondre à la question.

INSTRUCTIONS:
- Réponds en français
- Sois concis et orienté action
- Cite les sources quand tu utilises des informations des documents
- Si l'information n'est pas dans les documents, dis "Non documenté"

{history_section}DOCUMENTS:
{context}

QUESTION: {query}

RÉPONSE:"""
