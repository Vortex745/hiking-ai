# 🥾 AI Hiking

![Deploy](https://img.shields.io/github/actions/workflow/status/Vortex745/hiking-ai/deploy.yml?branch=main&label=deploy&logo=githubactions&style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white&style=for-the-badge)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white&style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white&style=for-the-badge)
![Go](https://img.shields.io/badge/Go-1.22-00ADD8?logo=go&logoColor=white&style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white&style=for-the-badge)
![Docker Hub](https://img.shields.io/docker/pulls/zijinn123/ai-hiking?label=Docker%20Hub&logo=docker&style=for-the-badge)

AI Hiking 是一个面向户外徒步场景的智能助手项目。它把 **React 前端**、**Go API Gateway** 和 **Python FastAPI AI Service** 组合在一起，提供 RAG 知识库问答、Agent 行动式对话、路线规划、天气适宜性判断、装备检查、风险提醒和模型配置能力。

## ✨ 亮点

- 🧭 **徒步 Agent**：识别路线规划、装备检查、风险评估、知识问答等意图，并按场景暴露小而准的工具集。
- 📚 **RAG 知识库**：支持文档上传、Feishu 同步、向量检索、BM25、RRF 融合、查询改写和可选 rerank。
- 🌦️ **位置与天气工作流**：前端可传递浏览器定位，后端可用地理/天气工具辅助判断是否适合徒步。
- ⚡ **SSE 流式体验**：Agent 和 RAG 都通过流式事件返回思考、工具调用、检索过程和最终回答。
- 🧠 **会话记忆**：支持聊天历史、会话压缩、知识抽取和回答完成后的记忆提交。
- 🛡️ **工具风险分级**：高风险工具具备确认模型，避免直接执行敏感操作。
- 🎛️ **浏览器侧模型配置**：`/llm-config` 可配置 LLM、Embedding、Rerank 模型参数。

## 🧱 架构

```text
Browser
  │ HTTP / SSE
  ▼
frontend/   React 18 + TypeScript + Vite + TailwindCSS
  │ /api/v1/*
  ▼
gateway/    Go 1.22 + Gin + CORS + proxy
  │ HTTP / SSE proxy
  ▼
ai-service/ Python 3.12 + FastAPI
  ├─ Agent: intent intake, hiking workflows, LangGraph fallback, memory commit
  ├─ RAG: loader, query rewrite, vector/BM25 retrieval, rerank, answer augment
  ├─ Memory: chat history, compression, knowledge extraction, vector store
  └─ Tools: search, file, terminal, PDF, geo, weather, route, gear, risk

PostgreSQL + pgvector
Redis
```

## 🧩 模块一览

| 模块 | 路径 | 说明 |
|---|---|---|
| 🖥️ Frontend | `frontend/` | React 页面、assistant-ui 聊天界面、SSE 客户端、模型配置 |
| 🚪 Gateway | `gateway/` | 统一 `/api/v1/*` 入口，代理 AI Service，处理 CORS 和限流 |
| 🤖 AI Service | `ai-service/` | Agent、RAG、Memory、工具注册、FastAPI 路由 |
| 🧰 MCP Server | `mcp-server/` | 扩展工具服务，目前包含图片搜索相关能力 |
| 🚢 Deploy | `.github/workflows/deploy.yml` | GitHub Actions 构建、推送 Docker Hub、SSH 部署 |

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/Vortex745/hiking-ai.git
cd hiking-ai
```

### 2. 准备环境变量

复制示例配置并填入自己的模型和可选服务密钥：

```bash
cp .env.example .env
```

关键变量：

| 变量 | 用途 |
|---|---|
| `OPENAI_BASE_URL` / `OPENAI_API_KEY` / `OPENAI_MODEL` | 主对话模型 |
| `EMBEDDING_BASE_URL` / `EMBEDDING_API_KEY` / `EMBEDDING_MODEL` | 向量模型 |
| `RERANK_BASE_URL` / `RERANK_API_KEY` / `RERANK_MODEL` | 可选 rerank 模型 |
| `AMAP_API_KEY` | 可选，高德地图地理与天气能力 |
| `FEISHU_DEFAULT_SPACE_ID` / `FEISHU_DEFAULT_FOLDER_TOKEN` | 可选，Feishu 默认同步源 |

### 3. Docker Compose 一键启动

```bash
docker compose up -d
```

默认服务：

| 服务 | 地址 | 说明 |
|---|---|---|
| 🌐 Frontend | `http://localhost:3000` | Docker 中的 Nginx 静态站点 |
| 🚪 Gateway | `http://localhost:8080` | API 网关 |
| 🤖 AI Service | `http://localhost:8000` | FastAPI 服务 |
| 🐘 PostgreSQL | `localhost:5432` | `pgvector/pgvector:pg16` |
| 🧱 Redis | `localhost:6379` | `redis:7-alpine` |

### 4. 本地开发模式

基础设施：

```bash
docker compose up -d postgres redis
```

AI Service：

```bash
cd ai-service
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Gateway：

```bash
cd gateway
go run main.go
```

Frontend：

```bash
cd frontend
npm install
npm run dev
```

开发模式下访问 `http://localhost:5173`。

## 🗺️ 页面

| 路由 | 页面 | 用途 |
|---|---|---|
| `/` | 首页 | 产品入口和模块跳转 |
| `/love-master` | RAG 模块 | 文档上传、知识库问答、检索过程展示 |
| `/super-agent` | Agent 模块 | 徒步助手对话、工具过程、路线/装备/风险任务 |
| `/llm-config` | 模型配置 | 浏览器侧 LLM、Embedding、Rerank 参数配置 |

## 🔌 API

前端统一访问 Gateway 的 `/api/v1/*`。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/health` | Gateway 健康检查 |
| `GET` | `/api/v1/chat/health` | Agent 健康检查 |
| `POST` | `/api/v1/chat/sync` | 同步 Agent 对话 |
| `POST` | `/api/v1/chat/sse` | SSE Agent 对话 |
| `GET` | `/api/v1/chat/history/:chatId` | 聊天历史 |
| `POST` | `/api/v1/chat/confirm` | 工具确认 |
| `GET` | `/api/v1/chat/pending/:chatId` | 待确认工具 |
| `POST` | `/api/v1/models/fetch` | 拉取模型列表 |
| `GET` | `/api/v1/rag/health` | RAG 健康检查 |
| `POST` | `/api/v1/rag/upload` | 上传知识库文档 |
| `POST` | `/api/v1/rag/query` | SSE RAG 问答 |
| `GET` | `/api/v1/rag/documents` | 文档列表 |
| `POST` | `/api/v1/rag/feishu/sync` | 同步单个 Feishu 文档 |
| `POST` | `/api/v1/rag/feishu/default-sync` | 同步默认 Feishu 源 |
| `GET` | `/api/v1/tools` | 工具注册表 |
| `GET` | `/api/v1/tools/health` | 工具配置健康检查 |

## 🤖 Agent 工作流

核心文件：

- `ai-service/agent/intake.py`：意图识别、槽位抽取、当前位置处理。
- `ai-service/agent/agent.py`：工具选择、LangGraph ReAct fallback、SSE 事件、记忆提交。
- `ai-service/tools/hiking_domain.py`：徒步领域工具，包括地理、天气、路线、装备、风险和报告。
- `ai-service/api/chat.py`：Agent HTTP 与 SSE 接口。

主要意图：

- `general_chat`
- `knowledge_qa`
- `route_plan`
- `gear_check`
- `risk_assessment`
- `report_export`

SSE 事件类型：

```text
thought
tool_call
tool_result
approval_required
artifact
text
done
error
```

## 📚 RAG 工作流

核心文件：

- `ai-service/api/rag.py`：上传、查询、文档列表、Feishu 同步。
- `ai-service/rag/loader.py`：文档加载与切分。
- `ai-service/rag/retriever.py`：pgvector / memory 检索、BM25、混合召回。
- `ai-service/rag/rewriter.py`：查询改写和多查询扩展。
- `ai-service/rag/reranker.py`：可选 rerank。
- `ai-service/rag/augmenter.py`：上下文拼接和答案生成。

支持上传格式：

```text
.txt
.md
.pdf
.docx
```

检索链路：

```text
问题归一化 → 查询改写 → 向量召回 + BM25 → RRF 融合 → 可选 rerank → 流式答案
```

## 🧪 测试与验证

Frontend：

```bash
cd frontend
npm test
npm run build
```

Gateway：

```bash
cd gateway
go test ./...
```

AI Service：

```bash
cd ai-service
python -m compileall -q .
python -m pytest tests -q
```

常用健康检查：

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/rag/health
curl http://localhost:8000/api/v1/tools/health
curl http://localhost:8080/health
curl http://localhost:3000/
```

## 🚢 部署

### GitHub Actions + Docker Hub + Docker Compose

`main` 分支推送会触发 `.github/workflows/deploy.yml`：

1. 校验前端、Gateway、AI Service 语法和生产 Compose 文件。
2. 构建 `ai-service`、`gateway`、`frontend` 三个镜像。
3. 推送到 Docker Hub 仓库 `zijinn123/ai-hiking`。
4. 发布 Redis 与 pgvector 的 runtime 镜像副本。
5. 通过 SSH 上传 `docker-compose.prod.yml` 和生产 `.env`。
6. 在服务器上拉取 `sha-*` 镜像并重启服务。

需要的 GitHub Secrets：

| Secret | 说明 |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub 用户名 |
| `DOCKERHUB_TOKEN` | Docker Hub Token |
| `DEPLOY_HOST` | 服务器地址 |
| `DEPLOY_USER` | SSH 用户 |
| `DEPLOY_SSH_KEY` | SSH 私钥 |
| `DEPLOY_PORT` | SSH 端口 |
| `DEPLOY_PATH` | 服务器部署目录 |
| `OPENAI_API_KEY` | 生产 LLM Key |
| `EMBEDDING_API_KEY` | 生产 Embedding Key |
| `RERANK_API_KEY` | 生产 Rerank Key |

生产 Compose：

```bash
DOCKERHUB_IMAGE=zijinn123/ai-hiking IMAGE_TAG=latest docker compose -f docker-compose.prod.yml up -d
```

### CloudBase

前端生产环境默认 API 地址配置在 `frontend/src/api/config.ts`：

```text
https://gateway-262534-6-1364947792.sh.run.tcloudbase.com/api/v1
```

当前 CloudBase 资源：

| 服务 | 类型 | URL |
|---|---|---|
| 🌐 Frontend | 静态托管 | `https://ai-hiking-d4gf29b4zcebc048d-1364947792.tcloudbaseapp.com/` |
| 🚪 Gateway | CloudRun | `https://gateway-262534-6-1364947792.sh.run.tcloudbase.com` |
| 🤖 AI Service | CloudRun | `https://ai-service-262534-6-1364947792.sh.run.tcloudbase.com` |

## 🧯 排障

### Agent 提示缺少 API Key

检查 `.env` 中的 `OPENAI_API_KEY`，或在 `/llm-config` 中配置可用模型参数。

### RAG 没有检索结果

检查：

- `EMBEDDING_API_KEY` 是否可用。
- PostgreSQL 是否运行。
- 是否已经在 `/love-master` 上传文档。
- `DATABASE_URL` 是否指向正确数据库。

### 天气或位置工具不可用

配置：

```env
AMAP_API_KEY=your-amap-key
```

### Feishu 同步不可用

确认 `lark-cli` 已安装并可在 `PATH` 中访问；必要时设置 `FEISHU_DEFAULT_SPACE_ID` 和 `FEISHU_DEFAULT_FOLDER_TOKEN`。

## 📁 目录结构

```text
ai-hiking/
├── ai-service/              # FastAPI AI Service
│   ├── agent/               # Agent intake, policy, execution
│   ├── api/                 # FastAPI routers
│   ├── memory/              # Chat and long-term memory
│   ├── rag/                 # Retrieval-augmented generation
│   ├── tools/               # Base and hiking-domain tools
│   └── tests/
├── frontend/                # React + Vite frontend
│   ├── src/
│   └── tests/
├── gateway/                 # Go API Gateway
│   ├── handler/
│   └── middleware/
├── mcp-server/              # Optional MCP extensions
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

## 📄 License

当前仓库没有单独的 `LICENSE` 文件。
