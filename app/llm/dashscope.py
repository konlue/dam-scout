"""阿里百炼 DashScope 适配器（OpenAI 兼容接口）"""

from langchain_openai import ChatOpenAI
from app.config import settings
from app.llm.adapter import LLMAdapter


class DashScopeAdapter(LLMAdapter):
    def get_chat_model(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=settings.LLM_MODEL,
            api_key=settings.DASHSCOPE_API_KEY,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
