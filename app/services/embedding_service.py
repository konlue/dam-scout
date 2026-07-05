"""Embedding 服务，通过 DashScope API 进行文本向量化"""

import requests
from app.config import settings


class EmbeddingService:
    API_URL = "https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding"

    def _call_api(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {settings.DASHSCOPE_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.EMBEDDING_MODEL,
            "input": {"texts": texts},
        }
        resp = requests.post(self.API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return [item["embedding"] for item in data["output"]["embeddings"]]

    def embed_text(self, text: str) -> list[float]:
        """单条文本向量化"""
        return self._call_api([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """批量文本向量化"""
        return self._call_api(texts)


embedding_service = EmbeddingService()
