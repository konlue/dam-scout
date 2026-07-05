"""Node1: Intent Analyzer — 分析用户需求的行业/用途/场景/风格"""

import json
import re
from app.llm import get_llm
from app.graph.state import ScoutState

PROMPT = """分析以下用户需求，提取行业、用途、场景、风格四个维度。

用户需求：{query}

请严格返回 JSON 格式，不要输出其他内容：
{{"industry": "行业", "purpose": "用途", "scene": "场景", "style": "风格"}}"""

DEFAULT = {"industry": "通用", "purpose": "展示", "scene": "通用", "style": "现代"}


def intent_node(state: ScoutState) -> dict:
    llm = get_llm()
    response = llm.invoke(PROMPT.format(query=state["query"])).content
    try:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return {"intent": json.loads(match.group())}
    except Exception:
        pass
    return {"intent": DEFAULT}
