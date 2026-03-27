# Tasks: DocuMentor AI - RAG Angular Expert

**Feature**: DocuMentor AI - RAG Angular Expert  
**Branch**: 001-angular-rag-chatbot  
**Created**: 2026-03-27

## Summary

- **Total Tasks**: 18 (updated for clarity)
- **User Story 1**: 7 tasks (P1 - Ask Angular Questions)
- **User Story 2**: 4 tasks (P2 - Chat History)
- **User Story 3**: 3 tasks (P2 - Source Citations)
- **Setup**: 4 tasks (Project initialization)

## Dependencies

```
Phase 1 (Setup)
    │
    ├── T001: Create project structure
    ├── T002: Create requirements.txt
    ├── T003: Create config/settings.py
    └── T004: Create .env.example

Phase 2 (Foundational)
    │
    ├── T005: Implement scraper/angular_scraper.py
    ├── T006: Implement rag/loader.py
    ├── T007: Implement rag/splitter.py
    ├── T008: Implement rag/embedder.py
    ├── T009: Implement rag/retriever.py
    └── T010: Implement rag/generator.py

Phase 3 (User Story 1 - Ask Angular Questions)
    │
    ├── T011: Implement storage/history.py
    ├── T012: Implement UI app.py
    └── T013: Test full RAG pipeline end-to-end

Phase 4 (User Story 2 - Chat History)
    │
    └── T014: Add chat history persistence

Phase 5 (User Story 3 - Source Citations)
    │
    └── T015: Display citations in UI

Phase 6 (Polish)
    │
    ├── T016: Add error handling
    ├── T017: Create quickstart documentation
    └── T018: Final integration test
```

## Implementation Strategy

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (T011-T013)  
**Delivery**: Incremental - each phase delivers working software

---

## Phase 1: Setup

- [x] T001 Create project structure per implementation plan (src/, data/, tests/)
- [x] T002 Create requirements.txt with all dependencies
- [x] T003 Create config/settings.py with configuration
- [x] T004 Create .env.example template

---

## Phase 2: Foundational (RAG Pipeline)

- [x] T005 [P] Implement scraper/angular_scraper.py - Scrape angular.dev docs
- [x] T006 [P] Implement rag/loader.py - Load documents into pipeline
- [x] T007 [P] Implement rag/splitter.py - Chunk documents
- [x] T008 [P] Implement rag/embedder.py - Generate embeddings with Ollama
- [x] T009 [P] Implement rag/retriever.py - Vector search with ChromaDB
- [x] T010 [P] Implement rag/generator.py - LLM response generation with source citation extraction

---

## Phase 3: User Story 1 - Ask Angular Questions (P1)

**Goal**: Users can ask Angular questions and receive accurate answers with citations.

**Independent Test**: Run `streamlit run src/ui/app.py`, ask "how to create a signal", verify response.

- [x] T011 [P] Implement storage/history.py - Chat history storage
- [x] T012 [P] [US1] Implement UI app.py - Streamlit chat interface
- [ ] T013 [US1] Test full RAG pipeline end-to-end

---

## Phase 4: User Story 2 - Chat History (P2)

**Goal**: Users can view previous conversations.

**Independent Test**: Ask question, refresh page, verify conversation appears.

- [x] T014 [US2] Add chat history persistence - Load/save conversations from JSON

---

## Phase 5: User Story 3 - Source Citations (P2)

**Goal**: AI responses include links to source documentation.

**Independent Test**: Ask question, verify clickable links in response.

- [x] T015 [US3] Display citations in UI - Show source URLs with responses

---

## Phase 6: Polish & Cross-Cutting

- [ ] T016 [P] Add error handling - Handle edge cases: Ollama not running, empty vector DB, no docs found, long queries
- [ ] T017 [P] Create quickstart.md - Setup and usage instructions
- [ ] T018 Final integration test - Verify all features work together

---

## Parallel Opportunities

| Tasks | Reason |
|-------|--------|
| T005-T010 | All RAG pipeline components are independent - can implement in parallel |
| T011-T012 | Storage and UI are loosely coupled via session state |
| T016-T017 | Error handling and docs are independent |

## Notes

- Tests are NOT included - implement first, test manually
- Focus on MVP: Core RAG pipeline + basic chat UI first
- Add polish after core functionality works
