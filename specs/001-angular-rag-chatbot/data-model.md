# Data Model: DocuMentor AI - RAG Angular Expert

## Entities

### Document
Represents a scraped documentation page from angular.dev.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| url | string | Source URL |
| title | string | Page title |
| content | string | Full page content |
| scraped_at | datetime | When page was scraped |

### Chunk
A chunk of a document for embedding.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| document_id | UUID | Parent document |
| content | string | Chunk text |
| embedding | float[] | Vector embedding |
| index | int | Position in document |

### Conversation
A chat session.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Unique identifier |
| created_at | datetime | Session start |
| messages | Message[] | Chat messages |

### Message
A single message in a conversation.

| Field | Type | Description |
|-------|------|-------------|
| role | enum | "user" or "assistant" |
| content | string | Message text |
| sources | Source[] | Retrieved sources (optional) |

### Source
A citation to documentation.

| Field | Type | Description |
|-------|------|-------------|
| url | string | Documentation URL |
| title | string | Page title |
| chunk_content | string | Retrieved text |

## Validation Rules

- Document.content: non-empty, max 1MB
- Chunk.content: non-empty, 100-1000 chars
- Message.content: non-empty, max 10000 chars
- Conversation.messages: max 100 messages

## State Transitions

```
[New Conversation] --> [Active] --> [Ended]
                                      |
                                      v
                                [Archived]
```

## Storage

- **Documents & Chunks**: ChromaDB collection
- **Conversations**: JSON file per session (data/history/)
- **Settings**: config/settings.py or .env
