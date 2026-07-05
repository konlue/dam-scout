"""LLM 适配器抽象基类"""

from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel


class LLMAdapter(ABC):
    @abstractmethod
    def get_chat_model(self) -> BaseChatModel:
        ...
