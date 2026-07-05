"""ScoutState — LangGraph 工作流状态定义"""

from typing import TypedDict


class IntentResult(TypedDict):
    industry: str   # 行业
    purpose: str    # 用途
    scene: str      # 场景
    style: str      # 风格


class TaskItem(TypedDict):
    task_type: str       # banner / background / effect / character ...
    description: str     # 任务描述


class ScoutState(TypedDict, total=False):
    # 输入
    query: str
    top_k: int
    space_id: int | None
    category: str | None
    color: str | None

    # 中间状态
    intent: IntentResult
    tasks: list[TaskItem]
    documents: list[dict]           # Retriever 原始结果
    filtered_documents: list[dict]  # Filter 过滤后

    # 输出
    answer: str
