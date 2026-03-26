from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    anthropic_api_key: str
    claude_model: str = "claude-3-5-haiku-20241022"
    embedding_model: str = "all-MiniLM-L6-v2"
    chroma_path: str = "./chroma_db"
    chunk_size: int = 500
    chunk_overlap: int = 50
    retrieval_k: int = 4

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
