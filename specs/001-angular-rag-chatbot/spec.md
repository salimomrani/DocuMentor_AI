# Feature Specification: DocuMentor AI - RAG Angular Expert

**Feature Branch**: `001-angular-rag-chatbot`  
**Created**: 2026-03-27  
**Status**: Draft  
**Input**: User description: "DocuMentor AI est un LLM spécialisé conçu pour servir d'expert technique local sur la stack Angular. Il doit fonctionner à 100% hors-ligne via Ollama avec une interface Streamlit."

## User Scenarios & Testing

### User Story 1 - Ask Angular Questions (Priority: P1)

A developer asks a question about Angular 17+ in natural language and receives an accurate, cited answer based on official documentation.

**Why this priority**: This is the core value proposition - users need to get reliable Angular answers offline.

**Independent Test**: Can be tested by asking a question like "how to create a signal in Angular 17" and verifying the answer cites angular.dev documentation.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** user types a question about Angular, **Then** the system retrieves relevant docs and generates a response
2. **Given** no relevant docs are found, **When** user asks a question, **Then** the system says "Non documenté" rather than hallucinating

---

### User Story 2 - Chat History (Priority: P2)

Users can view their previous conversations with the AI expert.

**Why this priority**: Developers often reference previous answers; chat history improves usability.

**Independent Test**: Can be tested by asking a question, then refreshing the page, and verifying the conversation appears in history.

**Acceptance Scenarios**:

1. **Given** user asked questions, **When** they return to the app, **Then** previous conversations are visible
2. **Given** user clears chat, **When** they click clear, **Then** the conversation is reset

---

### User Story 3 - Source Citations (Priority: P2)

The AI response includes links to the source documentation.

**Why this priority**: Users need to verify and explore the original docs for deeper understanding.

**Independent Test**: Can be tested by asking a question and verifying clickable links appear in the response.

**Acceptance Scenarios**:

1. **Given** a response is generated, **When** it uses documentation, **Then** source URLs are displayed
2. **Given** no docs are retrieved, **When** generating response, **Then** no fake citations are shown

---

### Edge Cases

- What happens when Ollama is not running?
- What happens when the vector database is empty (not yet indexed)?
- How does the system handle very long questions?
- What happens when no relevant docs are found for a query?

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept natural language questions about Angular 17+
- **FR-002**: System MUST retrieve relevant documentation chunks based on semantic similarity
- **FR-003**: System MUST generate responses using the LLM with retrieved context
- **FR-004**: System MUST display source citations with each response
- **FR-005**: System MUST indicate when information is "Non documenté" (not in source docs)
- **FR-006**: Users MUST be able to view and continue previous conversations
- **FR-007**: Users MUST be able to clear the current conversation
- **FR-008**: System MUST work 100% offline (no external API calls at runtime)
- **FR-009**: System MUST provide a simple web interface for user interaction

### Key Entities

- **Question**: User input text about Angular
- **RetrievedContext**: Relevant documentation chunks from the vector store
- **Response**: Generated answer with citations
- **Conversation**: Session containing question-response pairs

## Success Criteria

### Measurable Outcomes

- **SC-001**: Users receive answers to Angular questions within 10 seconds of submitting
- **SC-002**: At least 90% of responses include at least one valid source citation
- **SC-003**: System functions completely offline after initial setup
- **SC-004**: 100% of "Non documenté" responses contain no hallucinated information

## Assumptions

- Users have Ollama installed with Llama-3-8B model available
- Users will run a one-time indexing step to load Angular docs into the vector store
- The system will use the official Angular documentation at angular.dev as the sole source
- CPU inference is acceptable (GPU not required)
