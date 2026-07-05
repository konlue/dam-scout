"""LLM 服务 — 兼容层，委托给 app.llm 适配器"""

from app.llm import get_llm  # noqa: F401（保留旧导入路径兼容）
