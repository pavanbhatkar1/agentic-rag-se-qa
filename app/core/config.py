from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic RAG"
    app_env: str = "development"

    host: str = "0.0.0.0"
    port: int = 8000
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333

    qdrant_collection: str = "software_docs"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "mistral"
    ollama_model: str = "mistral:7b"
    tavily_api_key: str = "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"


    embedding_model: str = "BAAI/bge-small-en-v1.5"
    rerank_model: str = "BAAI/bge-reranker-base"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()