"""LLM 适配层，根据 MODEL_PROVIDER 返回对应 LLM 实例"""

from app.config import settings
from app.llm.dashscope import DashScopeAdapter
from app.llm.ollama import OllamaAdapter

_adapters = {
    "dashscope": DashScopeAdapter,
    "ollama": OllamaAdapter,
}


def get_llm():
    """统一入口：返回 LangChain BaseChatModel 实例"""
    adapter_cls = _adapters.get(settings.MODEL_PROVIDER)
    if not adapter_cls:
        raise ValueError(f"未知 MODEL_PROVIDER: {settings.MODEL_PROVIDER}")
    return adapter_cls().get_chat_model()
