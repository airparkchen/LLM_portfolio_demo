from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "LLM RAG Resume System"
    DEBUG: bool = True

    # Ollama settings
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_MODEL: str = "llama3.2"

    # Available models configuration
    # Format: "model_name:display_name:description"
    AVAILABLE_MODELS: List[str] = [
        "llama3.2:Llama 3.2:Meta's latest lightweight model",
        "mistral:Mistral 7B:Efficient and powerful 7B model",
    ]

    # RAG settings
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50
    TOP_K_RESULTS: int = 3

    # Paths
    RESUME_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "resume")
    VECTORSTORE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "vectorstore")

    # Embedding model (using Ollama)
    EMBEDDING_MODEL: str = "nomic-embed-text"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
