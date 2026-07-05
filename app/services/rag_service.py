"""RAG 检索服务，LangChain 编排 Embedding → Chroma → LLM"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.services.llm_service import get_llm
from app.services.embedding_service import embedding_service
from app.vectorstore.chroma_manager import chroma_manager
from app.models.dto import RagSearchResponse, RagSearchResult
from app.config import settings


PROMPT_TEMPLATE = PromptTemplate.from_template(
    """你是一个专业的视觉素材推荐助手。根据用户的搜索需求和检索到的图片信息，为用户推荐最合适的图片。

用户需求：{query}

检索到的图片信息：
{context}

请针对每张图片给出简短的推荐理由（一句话），按相关性从高到低排列。"""
)


class RagService:
    def __init__(self):
        self.llm = get_llm()
        self.output_parser = StrOutputParser()

    def search(self, query: str, top_k: int | None = None) -> RagSearchResponse:
        k = top_k or settings.RAG_TOP_K

        # 1. 向量化查询
        query_embedding = embedding_service.embed_text(query)

        # 2. Chroma 相似度检索
        results = chroma_manager.search(query_embedding, k)

        # 3. 构造上下文
        context = "\n".join(
            f"- 图片ID: {r['pictureId']}, 标题: {r['title']}, "
            f"分类: {r['category']}, 标签: {r['tags']}"
            for r in results
        )

        # 4. LLM 生成推荐理由
        prompt = PROMPT_TEMPLATE.format(query=query, context=context)
        recommendation = self.output_parser.invoke(self.llm.invoke(prompt))

        # 5. 组装响应
        items = [
            RagSearchResult(
                pictureId=r["pictureId"],
                title=r["title"],
                category=r["category"],
                score=r["score"],
                reason="",
            )
            for r in results
        ]

        return RagSearchResponse(
            results=items,
            query=query,
            recommendation=recommendation,
        )


rag_service = RagService()
