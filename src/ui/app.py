"""Streamlit UI for DocuMentor AI."""

from __future__ import annotations

import uuid
from datetime import datetime

import streamlit as st

from src.config.settings import settings
from src.rag.generator import Generator, Answer
from src.storage.history import HistoryManager, Conversation, Message


def init_session_state() -> None:
    """Initialize Streamlit session state."""
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "generator" not in st.session_state:
        try:
            st.session_state.generator = Generator()
        except Exception as e:
            st.session_state.generator = None
            st.session_state.generator_error = str(e)
    if "history_manager" not in st.session_state:
        st.session_state.history_manager = HistoryManager()


def load_conversation(conversation_id: str) -> None:
    """Load a conversation from history."""
    history_manager = st.session_state.history_manager
    conversation = history_manager.load_conversation(conversation_id)
    if conversation:
        st.session_state.conversation_id = conversation.id
        st.session_state.messages = [
            {"role": msg.role, "content": msg.content, "sources": msg.sources} for msg in conversation.messages
        ]


def save_conversation() -> None:
    """Save current conversation to history."""
    history_manager = st.session_state.history_manager
    conversation = Conversation(
        id=st.session_state.conversation_id,
        created_at=datetime.now(),
        messages=[
            Message(
                role=msg["role"],
                content=msg["content"],
                sources=msg.get("sources", []),
            )
            for msg in st.session_state.messages
        ],
    )
    history_manager.save_conversation(conversation)


def clear_conversation() -> None:
    """Clear current conversation."""
    st.session_state.conversation_id = str(uuid.uuid4())
    st.session_state.messages = []


def display_sources(sources: list[dict]) -> None:
    """Display source citations."""
    if not sources:
        return

    with st.expander("Sources"):
        for i, source in enumerate(sources, 1):
            st.markdown(f"**{i}. {source.get('title', 'Unknown')}**")
            if source.get("url"):
                st.markdown(f"🔗 [{source['url']}]({source['url']})")
            with st.container():
                st.caption(source.get("content", "")[:200] + "...")


def handle_user_input(user_input: str) -> None:
    """Process user input and generate response."""
    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    # Generate response
    generator = st.session_state.generator
    if generator is None:
        error_msg = st.session_state.get("generator_error", "Generator not initialized")
        st.error(f"Erreur: {error_msg}")
        st.info("Assurez-vous qu'Ollama est en cours d'exécution et que les modèles sont installés.")
        return

    try:
        # Get conversation history (all messages except the new one we're about to add)
        history = [msg for msg in st.session_state.messages if msg.get("role") in ("user", "assistant")]
        answer = generator.generate(user_input, conversation_history=history)

        # Add assistant message
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer.text,
                "sources": answer.sources,
            }
        )

        # Save to history
        save_conversation()

        # Rerun to display new messages
        st.rerun()

    except Exception as e:
        st.error(f"Erreur lors de la génération: {str(e)}")
        st.info("Vérifiez qu'Ollama est en cours d'exécution.")


def main() -> None:
    """Main Streamlit app."""
    st.set_page_config(
        page_title=settings.app_title,
        page_icon="🤖",
        layout="wide",
    )

    init_session_state()

    # Sidebar
    with st.sidebar:
        st.title("🤖 DocuMentor AI")

        st.markdown("---")

        # Check Ollama status
        if st.session_state.generator is None:
            st.error("⚠️ Ollama non connecté")
            st.caption("Vérifiez qu'Ollama est en cours d'exécution")
        else:
            st.success("✅ Ollama connecté")

        st.markdown("---")

        # New conversation
        if st.button("Nouvelle conversation", use_container_width=True):
            clear_conversation()
            st.rerun()

        st.markdown("---")

        # History
        st.subheader("Historique")
        history_manager = st.session_state.history_manager
        conversations = history_manager.list_conversations()[:5]

        if conversations:
            for conv in conversations:
                if st.button(
                    f"📝 {conv.created_at.strftime('%d/%m %H:%M')}",
                    key=f"conv_{conv.id}",
                    use_container_width=True,
                ):
                    load_conversation(conv.id)
                    st.rerun()
        else:
            st.caption("Aucun historique")

    # Main content
    st.title("🤖 Expert Angular")

    st.markdown("Posez-moi vos questions sur Angular 17+ — Réponses basées sur la documentation officielle.")

    # Display chat
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("sources") and msg["role"] == "assistant":
                display_sources(msg["sources"])

    # User input
    if prompt := st.chat_input("Votre question sur Angular..."):
        handle_user_input(prompt)


if __name__ == "__main__":
    main()
