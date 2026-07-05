"""Ollama 本地模型适配器"""

from langchain_ollama import ChatOllama
from app.config import settings
from app.llm.adapter import LLMAdapter


class OllamaAdapter(LLMAdapter):
    def get_chat_model(self) -> ChatOllama:
        return ChatOllama(
            model=settings.OLLAMA_LLM_MODEL,
            base_url=settings.OLLAMA_BASE_URL,
        )
