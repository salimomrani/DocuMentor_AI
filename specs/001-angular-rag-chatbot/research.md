# Research: DocuMentor AI - RAG Angular Expert

## Research Questions

### RQ1: How to implement RAG with Ollama locally?

**Finding**: Use LlamaIndex or LangChain with Ollama. LlamaIndex provides better RAG primitives.

**Decision**: Use LlamaIndex with Ollama
- Ollama hosts both the embedding model (nomic-embed-text) and LLM (llama3)
- LlamaIndex has built-in ChromaDB integration
- Works 100% offline after models are pulled

### RQ2: How to scrape angular.dev effectively?

**Finding**: angular.dev is a static site with good structure. Use BeautifulSoup4.

**Decision**: Use requests + BeautifulSoup4
- Scrape main content areas from angular.dev docs
- Extract title, content, and source URL for citations
- Save as markdown or plain text for embedding

### RQ3: How to maintain chat history in Streamlit?

**Finding**: Use Streamlit session_state to store conversation history.

**Decision**: Use st.session_state
- Store messages as list of dicts: [{"role": "user", "content": "..."}]
- Persist to JSON for cross-session history
- Clear button to reset conversation

## Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| LangChain | More complex than needed for simple RAG |
| FAISS | Less intuitive API than ChromaDB |
| Playwright for scraping | Overkill for static content |
| Gradio UI | Streamlit is more chat-focused |

## Conclusion

All research questions resolved. Technology stack confirmed:
- **RAG**: LlamaIndex + ChromaDB + Ollama
- **Scraping**: requests + BeautifulSoup4
- **UI**: Streamlit
- **Storage**: ChromaDB (vectors) + JSON (history)
