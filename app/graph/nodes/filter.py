"""Node4: Filter — 按 Metadata 过滤候选素材"""

from app.graph.state import ScoutState


def filter_node(state: ScoutState) -> dict:
    docs = state.get("documents", [])
    filtered = []

    for doc in docs:
        if state.get("category") and doc.get("category") != state["category"]:
            continue
        if state.get("space_id") is not None and doc.get("spaceId") != state["space_id"]:
            continue
        if state.get("color") and doc.get("color") != state["color"]:
            continue
        filtered.append(doc)

    # 按 pictureId 去重，保留得分最高的
    seen = {}
    for doc in filtered:
        pid = doc.get("pictureId")
        if pid is None:
            continue
        if pid not in seen or doc.get("score", 0) > seen[pid].get("score", 0):
            seen[pid] = doc

    return {"filtered_documents": list(seen.values())}
