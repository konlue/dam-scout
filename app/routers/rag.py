"""AI 搜图路由"""

from fastapi import APIRouter, HTTPException
from app.models.dto import RagSearchRequest, RagSearchResponse
from app.services.rag_service import rag_service

router = APIRouter(prefix="/rag", tags=["rag"])


@router.post("/search", response_model=RagSearchResponse)
async def rag_search(req: RagSearchRequest):
    try:
        return rag_service.search(req.query, req.top_k)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
