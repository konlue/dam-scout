"""Node2: Planner — 根据意图规划多个检索任务"""

import json
import re
from app.llm import get_llm
from app.graph.state import ScoutState

PROMPT = """基于以下需求分析，规划需要搜索的图片素材类型。

- 行业：{industry}
- 用途：{purpose}
- 场景：{scene}
- 风格：{style}

请返回 JSON 数组，每个元素包含 task_type（banner / background / effect / character / icon）
和 description（用于语义检索的关键词描述）：
[{{"task_type": "banner", "description": "搜索关键词"}}]"""


def planner_node(state: ScoutState) -> dict:
    llm = get_llm()
    response = llm.invoke(PROMPT.format(**state["intent"])).content
    try:
        match = re.search(r"\[.*\]", response, re.DOTALL)
        if match:
            return {"tasks": json.loads(match.group())}
    except Exception:
        pass
    return {"tasks": [{"task_type": "banner", "description": state["query"]}]}
