# Quickstart: DocuMentor AI

## Prerequisites

1. **Ollama installed**: https://ollama.ai
2. **Python 3.11+**

## Setup

```bash
# 1. Clone and install dependencies
pip install -r requirements.txt

# 2. Pull required Ollama models
ollama pull llama3
ollama pull nomic-embed-text

# 3. Start Ollama
ollama serve

# 4. Index Angular documentation (one-time)
python -m src.scraper.angular_scraper

# 5. Run the app
streamlit run src/ui/app.py
```

## Usage

1. Open http://localhost:8501
2. Ask Angular questions in the chat
3. View citations in the response

## Commands

| Command | Description |
|---------|-------------|
| `python -m src.scraper.angular_scraper` | Scrape and index docs |
| `streamlit run src/ui/app.py` | Start web interface |
| `rm -rf data/chroma/*` | Reset vector database |

## Troubleshooting

- **Ollama not running**: Run `ollama serve` first
- **No embeddings found**: Re-run scraper
- **Slow responses**: Use smaller model or CPU-friendly settings
