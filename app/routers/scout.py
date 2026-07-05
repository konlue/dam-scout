"""V2 策展路由：DAM-Scout"""

from fastapi import APIRouter, HTTPException
from app.models.dto import ScoutSearchRequest, ScoutSearchResponse, Recommendation
from app.graph.workflow import build_workflow

router = APIRouter(prefix="/scout", tags=["scout"])
workflow = build_workflow()


@router.post("/search", response_model=ScoutSearchResponse)
async def scout_search(req: ScoutSearchRequest):
    try:
        state = {
            "query": req.query,
            "top_k": req.top_k,
            "space_id": req.space_id,
            "category": req.category,
            "color": req.color,
        }
        result = workflow.invoke(state)

        recommendations = [
            Recommendation(
                pictureId=d["pictureId"],
                title=d["title"],
                category=d["category"],
                score=d["score"],
                task_type=d.get("task_type", "素材"),
            )
            for d in result.get("filtered_documents", [])
        ]

        return ScoutSearchResponse(
            intent=result.get("intent", {}),
            tasks=result.get("tasks", []),
            recommendations=recommendations,
            answer=result.get("answer", ""),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
