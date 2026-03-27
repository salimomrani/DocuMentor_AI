# Implementation Plan: DocuMentor AI - RAG Angular Expert

**Branch**: `001-angular-rag-chatbot` | **Date**: 2026-03-27 | **Spec**: [spec.md](./spec.md)

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

A local RAG-based Angular expert chatbot that works 100% offline using Ollama for LLM inference and embeddings, with a Streamlit web interface. The system scrapes angular.dev documentation, embeds it into a vector store, and uses retrieval-augmented generation to answer user questions with citations.

## Technical Context

**Language/Version**: Python 3.11+  
**Primary Dependencies**: Ollama, LangChain/LlamaIndex, Streamlit, BeautifulSoup4, ChromaDB  
**Storage**: ChromaDB (vector store), JSON files (chat history)  
**Testing**: pytest  
**Target Platform**: Local machine (Linux/macOS/Windows)  
**Performance Goals**: <10s response time for queries  
**Constraints**: 100% offline operation  
**Scale/Scope**: Single-user local application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Constitution Rule | Status | Notes |
|------------------|--------|-------|
| Exactitude Technique | ✅ PASS | RAG provides source citations |
| Concision Opérationnelle | ✅ PASS | Focus on actionable answers |
| Honnêteté des Limites | ✅ PASS | System says "Non documenté" when no docs found |
| No deprecated practices | ✅ PASS | Using current libraries (LangChain, LlamaIndex) |
| No API keys in code | ✅ PASS | All local, no external APIs |

## Project Structure

### Documentation (this feature)

```text
specs/001-angular-rag-chatbot/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── scraper/             # Documentation scraping
│   └── angular_scraper.py
├── rag/                 # RAG pipeline
│   ├── loader.py        # Document loading
│   ├── splitter.py     # Text chunking
│   ├── embedder.py     # Embedding generation
│   ├── retriever.py    # Vector search
│   └── generator.py    # LLM response generation
├── ui/                  # Streamlit interface
│   └── app.py
├── storage/             # Data persistence
│   └── history.py
└── config/
    └── settings.py

data/
├── chroma/              # Vector database
└── history/             # Chat history

tests/
├── test_scraper.py
├── test_rag.py
└── test_ui.py
```

**Structure Decision**: Single Python project with modular structure for scraper, RAG pipeline, and UI components. Uses local ChromaDB for vector storage, JSON for chat history.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations - all Constitution rules satisfied.

## Phase 0: Research

### Key Research Areas

1. **RAG with Ollama**: Using LangChain or LlamaIndex with Ollama for both embeddings and LLM
2. **Angular documentation structure**: Understanding angular.dev layout for scraping
3. **Streamlit chat patterns**: Maintaining conversation history in session state

### Research Findings

**Decision**: Use LlamaIndex over LangChain for RAG
- **Rationale**: LlamaIndex has better built-in RAG primitives and integrates easier with ChromaDB
- **Alternatives considered**: LangChain, raw Ollama API

**Decision**: Use BeautifulSoup4 for scraping
- **Rationale**: Simple, well-documented, handles HTML well
- **Alternatives considered**: Playwright (overkill), requests (no parsing)

**Decision**: Use ChromaDB for vector storage
- **Rationale**: Pure Python, works offline, good LlamaIndex integration
- **Alternatives considered**: FAISS (less intuitive API), qdrant (requires server)

## Phase 1: Design

### Data Model

- **Document**: id, content, source_url, title
- **Chunk**: id, document_id, content, embedding
- **Conversation**: id, messages[], created_at
- **Message**: role (user/assistant), content, sources[]

### Interface Contracts

- **Streamlit App**: Single-page chat interface
- **CLI**: Commands for indexing docs, running app, managing history

### Quickstart

1. Install Ollama and pull llama3 model
2. Install dependencies: `pip install -r requirements.txt`
3. Run indexing: `python -m src.scraper.angular_scraper`
4. Start app: `streamlit run src/ui/app.py`
