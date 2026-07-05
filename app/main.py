"""FastAPI 入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import embedding, rag, scout

app = FastAPI(
    title="AI 素材助手",
    description="DAM-Scout AI 素材策展助手",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(embedding.router)
app.include_router(rag.router)
app.include_router(scout.router)


@app.get("/")
async def root():
    return {"message": "DAM-Scout 服务运行中", "version": "0.1.0"}
