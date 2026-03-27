from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


type OllamaBaseUrl = str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Ollama
    ollama_base_url: OllamaBaseUrl = "http://localhost:11434"
    ollama_model: str = "llama3"
    ollama_embed_model: str = "nomic-embed-text"

    # Paths
    data_dir: Path = Path("data")
    chroma_dir: Path = Path("data/chroma")
    history_dir: Path = Path("data/history")

    # Scraping
    docs_base_url: str = "https://angular.dev"
    docs_output_dir: Path = Path("data/docs")

    # RAG
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k: int = 5
    chroma_collection_name: str = "angular_docs"
    llm_timeout: int = 60

    # App
    app_title: str = "DocuMentor AI"
    app_description: str = "Votre expert Angular local"


settings = Settings()
