"""Chat history storage."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from src.config.settings import settings


@dataclass
class Message:
    """A chat message."""

    role: str  # "user" or "assistant"
    content: str
    sources: list[dict] = field(default_factory=list)


@dataclass
class Conversation:
    """A chat conversation."""

    id: str
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


class HistoryManager:
    """Manages chat history persistence."""

    def __init__(self) -> None:
        self.history_dir = settings.history_dir
        self.history_dir.mkdir(parents=True, exist_ok=True)

    def save_conversation(self, conversation: Conversation) -> None:
        """Save a conversation to JSON."""
        file_path = self.history_dir / f"{conversation.id}.json"
        data = {
            "id": conversation.id,
            "created_at": conversation.created_at.isoformat(),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "sources": msg.sources,
                }
                for msg in conversation.messages
            ],
        }
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_conversation(self, conversation_id: str) -> Conversation | None:
        """Load a conversation from JSON."""
        file_path = self.history_dir / f"{conversation_id}.json"
        if not file_path.exists():
            return None

        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        messages = [
            Message(
                role=msg["role"],
                content=msg["content"],
                sources=msg.get("sources", []),
            )
            for msg in data.get("messages", [])
        ]

        return Conversation(
            id=data["id"],
            messages=messages,
            created_at=datetime.fromisoformat(data["created_at"]),
        )

    def list_conversations(self) -> list[Conversation]:
        """List all saved conversations."""
        conversations = []
        for file_path in self.history_dir.glob("*.json"):
            conv = self.load_conversation(file_path.stem)
            if conv:
                conversations.append(conv)
        return sorted(conversations, key=lambda c: c.created_at, reverse=True)

    def delete_conversation(self, conversation_id: str) -> None:
        """Delete a conversation."""
        file_path = self.history_dir / f"{conversation_id}.json"
        if file_path.exists():
            file_path.unlink()
