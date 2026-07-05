"""Chroma 向量数据库管理，封装增删改查"""

import chromadb
from app.config import settings


class ChromaManager:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name=settings.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def add(self, doc_id: str, text: str, embedding: list[float], metadata: dict):
        """新增向量"""
        self.collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def delete(self, doc_id: str):
        """删除向量"""
        self.collection.delete(ids=[doc_id])

    def update(self, doc_id: str, text: str, embedding: list[float], metadata: dict):
        """更新向量"""
        self.collection.update(
            ids=[doc_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def search(self, query_embedding: list[float], top_k: int = 5) -> list[dict]:
        """相似度检索，返回 top_k 结果"""
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
        formatted = []
        for i in range(len(results["ids"][0])):
            formatted.append({
                "pictureId": str(results["metadatas"][0][i].get("pictureId")),
                "title": results["metadatas"][0][i].get("title"),
                "category": results["metadatas"][0][i].get("category"),
                "tags": results["metadatas"][0][i].get("tags"),
                "score": round(1 - results["distances"][0][i], 4),
                "text": results["documents"][0][i],
            })
        return formatted

    def count(self) -> int:
        """当前集合中的向量数量"""
        return self.collection.count()


chroma_manager = ChromaManager()
