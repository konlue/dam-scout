"""向量管理路由：图片入库 / 更新 / 删除"""

from fastapi import APIRouter, HTTPException
from app.models.dto import EmbeddingAddRequest, EmbeddingUpdateRequest
from app.services.embedding_service import embedding_service
from app.vectorstore.chroma_manager import chroma_manager

router = APIRouter(prefix="/embedding", tags=["embedding"])


def _build_text(title: str, tags: str, category: str, description: str | None = None) -> str:
    parts = [title, tags, category]
    if description:
        parts.append(description)
    return " ".join(parts)


@router.post("/add")
async def add_embedding(req: EmbeddingAddRequest):
    try:
        text = _build_text(req.title, req.tags, req.category, req.description)
        embedding = embedding_service.embed_text(text)
        metadata = {
            "pictureId": req.pictureId,
            "title": req.title,
            "tags": req.tags,
            "category": req.category,
        }
        chroma_manager.add(str(req.pictureId), text, embedding, metadata)
        return {"code": 0, "message": "success", "data": {"pictureId": req.pictureId}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{picture_id}")
async def delete_embedding(picture_id: int):
    try:
        chroma_manager.delete(str(picture_id))
        return {"code": 0, "message": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/update")
async def update_embedding(req: EmbeddingUpdateRequest):
    try:
        text = _build_text(req.title, req.tags, req.category, req.description)
        embedding = embedding_service.embed_text(text)
        metadata = {
            "pictureId": req.pictureId,
            "title": req.title,
            "tags": req.tags,
            "category": req.category,
        }
        chroma_manager.update(str(req.pictureId), text, embedding, metadata)
        return {"code": 0, "message": "success", "data": {"pictureId": req.pictureId}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
