# ai-hiking

ai-hiking 是一个本地优先的智能徒步助手。项目把 React 前端、Go API Gateway 和 Python FastAPI AI Service 组合在一起，面向徒步知识问答、路线规划、天气适宜性判断、装备建议和风险提醒等场景。

当前 main 分支包含两个主要体验：

- **RAG 模块**：上传或同步徒步资料后进行知识库问答，支持向量检索、BM25 召回、实体信号、查询改写、可选 rerank 和检索调试信息。
- **Agent 模块**：围绕徒步任务进行行动式对话，结合确定性徒步工作流、LangGraph ReAct fallback、工具风险分级、SSE 流式输出和会话记忆。

## 架构

```text
Browser
  |
  | HTTP / SSE
  v
frontend/   React 18 + TypeScript + Vite + TailwindCSS
  |
  | /api/v1/*
  v
gateway/    Go 1.22 + Gin
  |
  | HTTP / SSE proxy
  v
ai-service/ Python 3.12 + FastAPI + LangChain + LangGraph
  |
  +-- Agent: intent intake, hiking workflows, tool policy, memory commit
  +-- RAG: document loading, query rewriting, hybrid retrieval, rerank
  +-- Memory: chat history, session compression, extracted knowledge
  +-- Tools: web, file, terminal, PDF, route, weather, risk, gear
  |
  +-- PostgreSQL + pgvector
  +-- Redis
```

默认端口：

| Service | URL | Notes |
|---|---|---|
| Frontend | `http://localhost:5173` | Vite dev server |
| Gateway | `http://localhost:8080` | Frontend API entry |
| AI Service | `http://localhost:8000` | FastAPI app and `/docs` |
| PostgreSQL | `localhost:5432` | `pgvector/pgvector:pg16` |
| Redis | `localhost:5379` | Host port mapped to container `6379` |

## Tech Stack

- Frontend: React 18, TypeScript, Vite 5, TailwindCSS, React Router, lucide-react
- Gateway: Go 1.22, Gin, CORS middleware, rate limiting
- AI Service: Python 3.12, FastAPI, LangChain 0.3, LangGraph 0.2, OpenAI-compatible clients
- Retrieval: PostgreSQL + pgvector, in-memory fallback, BM25, RRF, optional rerank
- Runtime dependencies: Docker Compose, Redis, optional `lark-cli`, optional AMap API

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
```

This starts:

- `ai-hiking-postgres`
- `ai-hiking-redis`

### 2. Configure AI Service

Create `ai-service/.env`. The file is intentionally ignored by Git.

```env
# LLM
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-llm-api-key
OPENAI_MODEL=deepseek-v4-flash

# Embeddings
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=your-embedding-api-key
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Optional rerank
RERANK_BASE_URL=https://api.openai.com/v1
RERANK_API_KEY=your-rerank-api-key
RERANK_MODEL=Qwen/Qwen3-Reranker-8B
RERANK_ENABLED=true

# Storage
DATABASE_URL=postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking
REDIS_URL=redis://localhost:5379/0
MEMORY_STORE_PATH=./memory_store
MEMORY_ENABLED=true

# Optional hiking data providers
AMAP_API_KEY=your-amap-key

# Optional Feishu sync defaults
FEISHU_DEFAULT_SPACE_ID=
FEISHU_DEFAULT_FOLDER_TOKEN=
```

Notes:

- `config.py` defaults Redis to `localhost:6379`; when using this repository's `docker-compose.yml`, set `REDIS_URL=redis://localhost:5379/0`.
- `/llm-config` stores model settings in browser localStorage and sends them with chat/RAG requests. It does not persist secrets to the repository.

### 3. Run AI Service

PowerShell:

```powershell
cd ai-service
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Bash:

```bash
cd ai-service
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### 4. Run Gateway

```bash
cd gateway
go run main.go
```

Gateway environment variables:

| Variable | Default | Description |
|---|---|---|
| `PORT` | `8080` | Gateway listen port |
| `AI_SERVICE_URL` | `http://localhost:8000` | Upstream AI Service URL |
| `ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | CORS allow list |

### 5. Run Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## Pages

| Route | Page | Purpose |
|---|---|---|
| `/` | Home | Entry page |
| `/love-master` | RAG module | Knowledge-base Q&A and document upload |
| `/super-agent` | Agent module | Hiking assistant chat and streamed tool execution |
| `/llm-config` | LLM config | Browser-side model, embedding and rerank settings |

## API Surface

The frontend calls the Gateway under `/api/v1/*`.

| Method | Gateway path | Description |
|---|---|---|
| `GET` | `/health` | Gateway health check |
| `GET` | `/api/v1/chat/health` | Agent health check |
| `POST` | `/api/v1/chat/sync` | Synchronous Agent chat |
| `POST` | `/api/v1/chat/sse` | Streaming Agent chat |
| `GET` | `/api/v1/chat/history/:chatId` | Chat history |
| `POST` | `/api/v1/models/fetch` | Fetch models from an OpenAI-compatible provider |
| `GET` | `/api/v1/rag/health` | RAG health check |
| `POST` | `/api/v1/rag/upload` | Upload a RAG document |
| `POST` | `/api/v1/rag/query` | Streaming RAG answer |
| `GET` | `/api/v1/rag/documents` | List uploaded documents |
| `POST` | `/api/v1/rag/feishu/sync` | Sync a single Feishu document |
| `POST` | `/api/v1/rag/feishu/default-sync` | Sync configured Feishu sources |

AI Service also exposes direct endpoints:

| Method | AI Service path | Description |
|---|---|---|
| `GET` | `/health` | Service health check |
| `GET` | `/docs` | FastAPI OpenAPI UI |
| `GET` | `/api/v1/tools` | Tool registry metadata |
| `GET` | `/api/v1/tools/health` | Tool configuration and external key status |
| `POST` | `/api/v1/chat/confirm` | Resolve a high-risk tool confirmation |
| `GET` | `/api/v1/chat/pending/{chat_id}` | List pending tool confirmations |

## Agent Module

Core files:

- `ai-service/agent/intake.py`: deterministic intent detection, slot extraction and current-location normalization
- `ai-service/agent/agent.py`: LangGraph ReAct wrapper, tool selection, SSE events and memory commit
- `ai-service/tools/hiking_domain.py`: weather, geo, route, gear, risk and report adapters
- `ai-service/api/chat.py`: sync and SSE chat endpoints

Supported high-level intents:

- `general_chat`
- `knowledge_qa`
- `route_plan`
- `gear_check`
- `risk_assessment`
- `report_export`

Execution flow:

1. The request is normalized with `understand_request()`.
2. Current-location weather and route flows are prefetched deterministically when possible.
3. The Agent exposes only a small intent-specific tool set for the current turn.
4. LangGraph ReAct handles fallback reasoning with `MAX_STEPS = 6`.
5. SSE emits `thought`, `tool_call`, `tool_result`, `approval_required`, `artifact`, `text`, `done` and `error` events.
6. Conversation memory is committed only after a final assistant response is produced.

Visible base tools:

- `web_search`
- `web_scraping`
- `file_operation`
- `resource_download`
- `terminal`
- `generate_pdf`
- `terminate`

Hidden hiking-domain tools:

- `weather_lookup`
- `geo_lookup`
- `route_research`
- `hiking_knowledge_search`
- `gear_checklist`
- `risk_assessment`
- `trip_report_export`

## RAG Module

Core files:

- `ai-service/api/rag.py`: upload, query, document list and Feishu sync endpoints
- `ai-service/rag/loader.py`: file loading and chunking
- `ai-service/rag/retriever.py`: pgvector/in-memory retrieval, BM25 and hybrid search
- `ai-service/rag/rewriter.py`: query rewriting and multi-query expansion
- `ai-service/rag/reranker.py`: optional rerank stage
- `ai-service/rag/augmenter.py`: context construction for final answers

Supported upload formats:

- `.txt`
- `.md`
- `.pdf`
- `.docx`

Retrieval flow:

1. Normalize and rewrite the user query.
2. Retrieve candidates through vector search and BM25 lexical search.
3. Fuse ranked lists with reciprocal rank fusion.
4. Optionally rerank top candidates.
5. Stream final answer events back to the frontend.

If pgvector is unavailable, the retriever falls back to memory mode. Memory mode is useful for local development but uploaded documents are not durable across process restarts.

## Memory

Memory code lives in `ai-service/memory/`.

Current pieces:

- `FileChatMemory`: per-chat message history
- `SessionCompressor`: short-term session compression
- `KnowledgeExtractor`: extracts durable user/task facts
- `VectorStore`: FAISS or in-memory vector storage
- `MemoryCommitter`: commits stable memory after completed answers

The memory layer is conservative: exact duplicates are skipped, approximate duplicates are marked as merge candidates, and existing memory is not silently overwritten.

## Project Layout

```text
ai-hiking/
├── ai-service/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   ├── agent/
│   ├── rag/
│   ├── memory/
│   ├── mcp/
│   ├── tools/
│   └── tests/
├── frontend/
│   ├── src/
│   ├── tests/
│   ├── package.json
│   └── vite.config.ts
├── gateway/
│   ├── main.go
│   ├── config/
│   ├── handler/
│   └── middleware/
├── mcp-server/image_search/
├── docker-compose.yml
└── README.md
```

Runtime and generated files are ignored, including:

- `ai-service/.env`
- `.venv/`, `.conda*/`, `__pycache__/`
- `node_modules/`, `frontend/dist/`
- `memory_store/`, `memory_data/`, `rag_docs/`, `workspace/`
- generated Markdown documents other than `README.md`

## Common Commands

Infrastructure:

```bash
docker compose up -d
docker compose ps
docker compose down
```

AI Service:

```bash
cd ai-service
pip install -r requirements.txt
python main.py
python -m compileall -q agent api memory mcp rag tools main.py config.py
python -m pytest tests -q
```

Gateway:

```bash
cd gateway
go run main.go
go test ./...
```

Frontend:

```bash
cd frontend
npm install
npm run dev
npm run build
npm test
```

## Health Checks

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/rag/health
curl http://localhost:8000/api/v1/tools/health
curl http://localhost:8080/health
curl http://localhost:5173/
```

## Troubleshooting

### Agent reports missing API key

Set `OPENAI_API_KEY` in `ai-service/.env`, or configure LLM settings in `/llm-config` before sending requests from the frontend.

### RAG has no retrieval results

Check:

- `EMBEDDING_API_KEY` is configured.
- PostgreSQL is running on `localhost:5432`.
- `DATABASE_URL` points to the Docker database.
- Documents have been uploaded through `/love-master`.

### Redis connection fails

When using the repository Docker setup, set:

```env
REDIS_URL=redis://localhost:5379/0
```

### Weather or location tools return placeholder data

Set:

```env
AMAP_API_KEY=your-amap-key
```

### Feishu sync is disabled

Feishu sync depends on `lark-cli` being available in `PATH`. Optional defaults can be configured with `FEISHU_DEFAULT_SPACE_ID` and `FEISHU_DEFAULT_FOLDER_TOKEN`.

## Deployment

### GitHub Actions + GHCR + Docker Compose

The repository includes a GitHub Actions deployment pipeline in `.github/workflows/deploy.yml`.

On every push to `main`, or on manual `workflow_dispatch`, the workflow:

1. Validates the frontend, gateway, AI service syntax and production Compose file.
2. Builds three Docker images with Buildx.
3. Pushes the images to GitHub Container Registry:
   - `ghcr.io/vortex745/hiking-ai-ai-service`
   - `ghcr.io/vortex745/hiking-ai-gateway`
   - `ghcr.io/vortex745/hiking-ai-frontend`
4. Uploads `docker-compose.prod.yml` to the server over SSH.
5. Pulls the commit-tagged images and restarts services with Docker Compose.

Required GitHub repository secrets:

| Secret | Description |
|---|---|
| `DEPLOY_HOST` | Server hostname or IP |
| `DEPLOY_USER` | SSH user on the server |
| `DEPLOY_SSH_KEY` | Private SSH key with access to the server |
| `DEPLOY_PORT` | SSH port, usually `22` |
| `DEPLOY_PATH` | Server directory for the production compose file and `.env` |

Server requirements:

- Docker Engine and Docker Compose plugin installed.
- The `DEPLOY_USER` can run Docker commands.
- A production `.env` exists in `DEPLOY_PATH`; keep secrets on the server, not in Git.
- If GHCR packages are private, the workflow logs in during deployment with the repository `GITHUB_TOKEN`.

Production deploy files:

- `docker-compose.prod.yml` pulls GHCR images instead of building locally.
- Only the frontend port is published by default through `FRONTEND_PORT`.
- Gateway, AI Service, PostgreSQL and Redis stay on the private Docker network.
- Runtime data is stored in Docker volumes: `pgdata`, `redis-data`, `ai-memory`, `ai-rag-docs`, and `ai-workspace`.

Manual server smoke check after deployment:

```bash
cd /path/to/deploy
docker compose -f docker-compose.prod.yml ps
curl http://localhost:${FRONTEND_PORT:-3000}/
```

### CloudBase

项目已部署到腾讯云 CloudBase：

| 服务 | 类型 | URL |
|------|------|-----|
| **前端** | 静态托管 | `https://ai-hiking-d4gf29b4zcebc048d-1364947792.tcloudbaseapp.com/` |
| **网关 (Gateway)** | CloudRun | `https://gateway-262534-6-1364947792.sh.run.tcloudbase.com` |
| **AI 服务** | CloudRun | `https://ai-service-262534-6-1364947792.sh.run.tcloudbase.com` |

### 环境信息

- **EnvId**: `ai-hiking-d4gf29b4zcebc048d`
- **地域**: 上海 (ap-shanghai)
- **套餐**: 体验版

### Frontend 静态托管

前端使用 `@cloudbase/js-sdk` 的 `uploadFiles` 工具部署。API 调用通过网关公网 URL 直接跨域请求：

```typescript
const API_BASE = 'https://gateway-262534-6-1364947792.sh.run.tcloudbase.com/api/v1'
```

### Gateway CloudRun

- 语言: Go 1.22 + Gin
- 访问类型: PUBLIC
- 端口: 8080
- 资源: 0.25 CPU / 0.5GB MEM
- 环境变量:
  - `AI_SERVICE_URL`: `https://ai-service-262534-6-1364947792.sh.run.tcloudbase.com`
  - `ALLOWED_ORIGINS`: 包含静态托管域和 CloudRun 域

### AI Service CloudRun

- 语言: Python 3.12 + FastAPI
- 访问类型: PUBLIC
- 端口: 8000
- 资源: 1 CPU / 2GB MEM
- 状态: 运行中（内存模式，无 PostgreSQL/Redis）
- 功能端点: `/health`、`/api/v1/chat/*`、`/api/v1/rag/*`、`/api/v1/models/*`

### CloudBase 资源

- 静态托管: 用于前端部署
- CloudRun x3: frontend, gateway, ai-service
- NoSQL 数据库: 已启用

## License

No standalone `LICENSE` file is currently included.
