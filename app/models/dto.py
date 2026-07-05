"""请求/响应数据模型"""

from pydantic import BaseModel


class EmbeddingAddRequest(BaseModel):
    """图片入库请求"""
    pictureId: int
    title: str
    tags: str
    category: str
    description: str | None = None


class EmbeddingUpdateRequest(BaseModel):
    """图片更新请求"""
    pictureId: int
    title: str
    tags: str
    category: str
    description: str | None = None


class RagSearchRequest(BaseModel):
    """AI 搜图请求"""
    query: str
    top_k: int = 5


class RagSearchResult(BaseModel):
    """单条推荐结果"""
    pictureId: int
    title: str
    category: str
    score: float
    reason: str


from typing import Any

class RagSearchResponse(BaseModel):
    """AI 搜图响应"""
    results: list[RagSearchResult]
    query: str
    recommendation: str


# ===== V2: Scout 策展助手 DTO =====

class ScoutSearchRequest(BaseModel):
    """策展搜图请求"""
    query: str
    top_k: int = 5
    space_id: int | None = None
    category: str | None = None
    color: str | None = None


class Recommendation(BaseModel):
    """单条策展推荐"""
    pictureId: int
    title: str
    category: str
    score: float
    task_type: str
    reason: str = ""


class ScoutSearchResponse(BaseModel):
    """策展搜图响应"""
    intent: dict[str, str]
    tasks: list[dict[str, str]]
    recommendations: list[Recommendation]
    answer: str
