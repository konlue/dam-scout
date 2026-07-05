# DAM-Scout — **智能素材策展助手**

基于 RAG + LangGraph 的智能素材策展助手。用户输入自然语言需求，系统自动分析意图、规划检索任务、从向量数据库中召回匹配素材，由 LLM 生成专业策展方案。

## 架构

```
用户需求（自然语言）
       │
       ▼
  Intent Analyzer    ← 行业 / 用途 / 场景 / 风格
       │
       ▼
  Planner            ← 生成多个检索任务
       │
       ▼
  Retriever          ← DashScope Embedding → ChromaDB
       │
       ▼
  Filter             ← 去重 / 相关性过滤
       │
       ▼
  Generator          ← Qwen 生成策展方案 + 推荐理由
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 框架 | FastAPI + Uvicorn |
| LLM | 阿里百炼 Qwen（qwen-turbo）/ Ollama（可切换） |
| Embedding | 阿里百炼 DashScope text-embedding-v3（1024 维，云端） |
| 向量数据库 | ChromaDB（本地持久化） |
| 工作流 | LangGraph StateGraph |
| LLM 适配 | LangChain ChatOpenAI |

## 项目结构

```
dam-scout/
├── app/
│   ├── main.py                  # FastAPI 入口
│   ├── config.py                # 环境变量配置
│   ├── llm/                     # LLM 适配层
│   ├── graph/                   # LangGraph 工作流
│   │   ├── state.py             # 状态定义
│   │   ├── workflow.py          # 5 节点 DAG
│   │   └── nodes/               # intent / planner / retriever / filter / generator
│   ├── models/dto.py            # Pydantic 数据模型
│   ├── routers/                 # API 路由
│   │   ├── embedding.py         # 向量 CRUD
│   │   ├── rag.py               # 基础 RAG 搜图
│   │   └── scout.py             # 策展助手（主接口）
│   ├── services/                # 业务服务
│   │   ├── embedding_service.py # DashScope Embedding API
│   │   ├── llm_service.py       # LLM 兼容层
│   │   └── rag_service.py       # 基础 RAG
│   └── vectorstore/
│       └── chroma_manager.py    # ChromaDB 封装
├── springboot/                  # Spring Boot 集成文件（可直接复制到主项目）
├── sync_embeddings.py           # 批量同步脚本（MySQL → ChromaDB）
├── .env.example                 # 环境变量模板
└── requirements.txt
```

## 快速开始

### 1. 克隆 & 创建虚拟环境

```bash
git clone https://github.com/konlue/dam-scout.git
cd dam-scout
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入 DashScope API Key：

```env
MODEL_PROVIDER=dashscope
DASHSCOPE_API_KEY=sk-your-actual-key-here
```

> API Key 获取：[阿里百炼控制台](https://bailian.console.aliyun.com/)

### 4. 启动服务

```bash
uvicorn app.main:app --reload --port 8000
```

访问 http://localhost:8000/docs 查看 Swagger 文档。

### 5. 向量数据同步

首次使用需要将图片数据同步到 ChromaDB 向量数据库：

```bash
# 编辑 sync_embeddings.py 中的数据库连接信息后执行
python sync_embeddings.py
```

后续图片的增删改会通过 Spring Boot 自动同步向量。

## API 接口

### POST /scout/search — 策展搜索（主接口）

**请求：**

```json
{
  "query": "给电商大促准备一组科技感的横幅和背景图",
  "top_k": 5
}
```

**响应：**

```json
{
  "intent": {
    "industry": "电商",
    "purpose": "大促活动",
    "scene": "线上推广",
    "style": "科技感"
  },
  "tasks": [
    { "task_type": "banner", "description": "..." }
  ],
  "recommendations": [
    {
      "pictureId": 1001,
      "title": "蓝色科技横幅",
      "category": "banner",
      "score": 0.92,
      "task_type": "banner",
      "reason": "深蓝渐变背景搭配几何线条，符合科技感调性"
    }
  ],
  "answer": "根据您的需求分析，为您策划了一组科技感素材..."
}
```

### 向量管理

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/embedding/add` | 图片入库，生成向量 |
| DELETE | `/embedding/{pictureId}` | 删除图片向量 |
| PUT | `/embedding/update` | 更新图片向量 |

### POST /rag/search — 基础 RAG 搜图

```json
{ "query": "科技感背景", "top_k": 5 }
```

## 配置说明

| 环境变量 | 默认值 | 说明 |
|----------|--------|------|
| `MODEL_PROVIDER` | `dashscope` | `dashscope` 或 `ollama` |
| `DASHSCOPE_API_KEY` | — | 阿里百炼 API Key |
| `LLM_MODEL` | `qwen-turbo` | 百炼 LLM 模型名称 |
| `EMBEDDING_MODEL` | `text-embedding-v3` | 百炼 Embedding 模型名称 |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 地址 |
| `OLLAMA_LLM_MODEL` | `qwen3:4b` | Ollama 模型 |
| `CHROMA_PERSIST_DIR` | `./chroma_data` | ChromaDB 存储目录 |
| `CHROMA_COLLECTION_NAME` | `picture_embeddings` | 集合名称 |
| `RAG_TOP_K` | `5` | 检索返回数量 |

### 本地离线模式

```env
MODEL_PROVIDER=ollama
```

需提前安装 [Ollama](https://ollama.com) 并拉取模型：`ollama pull qwen3:4b`

## Spring Boot 集成

| 文件 | 说明 |
|------|------|
| `AIController.java` | AI 接口控制器 |
| `AIManager.java` | 调用本服务的客户端封装 |
| `AIEmbeddingRequest.java` | 向量入库请求 DTO |
| `AISearchRequest.java` | 搜索请求 DTO |
| `AISearchResponse.java` | 搜索响应 DTO |

前端调用 `POST /api/ai/search`，由 Spring Boot 转发到本服务（默认 `http://localhost:8000`）。

## 效果展示

**AI 搜图主页**

![AI 搜索主页](screenshots/ai-search-home.jpeg)

**策展结果**

![策展结果](screenshots/ai-search-result.jpeg)

## 许可证

本项目仅供交流学习使用。
