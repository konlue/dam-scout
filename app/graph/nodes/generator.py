"""Node5: Generator — Qwen 生成结构化策展方案"""

from app.llm import get_llm
from app.graph.state import ScoutState

PROMPT = """你是专业的视觉素材策展助手。根据用户需求和检索到的图片，生成策展方案。

用户需求：{query}

需求分析：
- 行业：{industry}
- 用途：{purpose}
- 场景：{scene}
- 风格：{style}

检索到的图片素材：
{context}

请生成策展方案，包含：
1. 推荐的素材组合（按任务类型分组）
2. 每个素材的推荐理由（一句话）
3. 整体搭配建议"""


def generator_node(state: ScoutState) -> dict:
    llm = get_llm()
    docs = state.get("filtered_documents", [])

    context = "\n".join(
        f"- [{d.get('task_type', '素材')}] 图片ID: {d['pictureId']}, "
        f"标题: {d['title']}, 分类: {d['category']}, 相似度: {d['score']}"
        for d in docs
    ) or "（无匹配素材）"

    prompt = PROMPT.format(
        query=state["query"],
        context=context,
        **state["intent"],
    )

    answer = llm.invoke(prompt).content
    return {"answer": answer}
