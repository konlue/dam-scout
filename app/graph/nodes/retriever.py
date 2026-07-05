"""Node3: Retriever — 按任务逐个检索 Chroma，收集候选素材"""

from app.services.embedding_service import embedding_service
from app.vectorstore.chroma_manager import chroma_manager
from app.graph.state import ScoutState


def retriever_node(state: ScoutState) -> dict:
    all_docs: list[dict] = []
    k = state.get("top_k", 5)

    for task in state.get("tasks", []):
        embedding = embedding_service.embed_text(task["description"])
        results = chroma_manager.search(embedding, k)
        for r in results:
            r["task_type"] = task["task_type"]
        all_docs.extend(results)

    return {"documents": all_docs}
