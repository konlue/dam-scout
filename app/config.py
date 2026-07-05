"""配置管理，从 .env 文件读取环境变量"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ===== LLM 配置 =====
    MODEL_PROVIDER: str = "dashscope"  # dashscope / ollama
    USE_OLLAMA: bool = False
    DASHSCOPE_API_KEY: str = ""
    LLM_MODEL: str = "qwen-turbo"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_LLM_MODEL: str = "qwen3:4b"

    # ===== Embedding 配置 =====
    EMBEDDING_MODEL: str = "text-embedding-v3"

    # ===== Chroma 配置 =====
    CHROMA_PERSIST_DIR: str = "./chroma_data"
    CHROMA_COLLECTION_NAME: str = "picture_embeddings"

    # ===== RAG 配置 =====
    RAG_TOP_K: int = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
