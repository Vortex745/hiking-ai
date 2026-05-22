# ai-hiking

ai-hiking 是一个面向徒步场景的本地 AI 助手应用。项目由 React 前端、Go API Gateway、Python FastAPI AI Service 组成，提供两类核心能力：

- RAG 模块：上传或同步徒步资料后进行知识库问答，支持向量检索、BM25、实体召回、查询改写、Rerank 和检索调试信息。
- Agent 模块：围绕徒步路线、天气适宜性、装备清单、风险提醒和报告导出进行行动式对话，使用 LangGraph ReAct、确定性徒步工作流、工具预算、SSE 流式输出和高风险工具确认。

## 架构概览

```text
Browser
  |
  | HTTP / SSE
  v
frontend/  React 18 + TypeScript + Vite + TailwindCSS
  |
  | /api/v1 proxy
  v
gateway/   Go 1.22 + Gin
  |
  | HTTP / SSE proxy
  v
ai-service/ Python 3.12 + FastAPI + LangChain + LangGraph
  |
  +-- Agent: intent intake, deterministic hiking workflows, ReAct fallback
  +-- RAG: upload, split, hybrid retrieval, rerank, answer streaming
  +-- Memory: chat history, session compression, vector knowledge memory
  +-- MCP: AMap stdio MCP and optional image-search MCP
  +-- Tools: web, file, download, terminal, PDF and hiking-domain adapters
  |
  +-- PostgreSQL + pgvector
  +-- Redis
```

默认端口：

| 服务 | 地址 | 说明 |
|---|---|---|
| Frontend | `http://localhost:5173` | Vite 开发服务器 |
| Gateway | `http://localhost:8080` | 前端访问的统一 API 入口 |
| AI Service | `http://localhost:8000` | FastAPI 服务与 OpenAPI 文档 |
| PostgreSQL | `localhost:5432` | `docker-compose.yml` 中的 pgvector |
| Redis | `localhost:5379` | 宿主机端口映射到容器 `6379` |

## 快速开始

### 1. 准备环境

需要本机安装：

- Python 3.12+
- Node.js 18+，推荐 20 LTS
- Go 1.22+
- Docker Desktop / Docker Compose
- 一个 OpenAI 兼容的大模型 API Key
- 可选：高德地图 API Key，用于天气、地理反查和 POI 路线候选
- 可选：Pexels API Key，用于内置图片搜索 MCP Server
- 可选：`lark-cli`，用于飞书文档同步

### 2. 启动 PostgreSQL 和 Redis

```bash
docker compose up -d
```

容器名称：

- `ai-hiking-postgres`
- `ai-hiking-redis`

### 3. 配置 AI Service 环境变量

在 `ai-service/.env` 中配置。该文件不应提交到仓库。

```env
# LLM
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=your-llm-api-key
OPENAI_MODEL=deepseek-v4-flash

# Embedding
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=your-embedding-api-key
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# Rerank, optional
RERANK_BASE_URL=https://api.example.com/v1
RERANK_API_KEY=your-rerank-api-key
RERANK_MODEL=Qwen/Qwen3-Reranker-8B
RERANK_ENABLED=true

# Storage
DATABASE_URL=postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking
REDIS_URL=redis://localhost:5379/0
MEMORY_STORE_PATH=./memory_store
MEMORY_ENABLED=true

# AMap MCP, optional but recommended for hiking workflows
AMAP_MAPS_API_KEY=your-amap-key
# AMAP_API_KEY is still accepted for compatibility.
# AMAP_MCP_COMMAND=npx
# AMAP_MCP_ARGS=-y @amap/amap-maps-mcp-server

# Web search, optional
BAIDU_SEARCH_API_KEY=your-baidu-search-key

# Image search MCP, optional
PEXELS_API_KEY=your-pexels-key
```

也可以在前端 `/llm-config` 页面填写大模型、Embedding 和 Rerank 配置。保存时前端会调用 `/api/v1/models/save-config`，由 AI Service 写入 `ai-service/.env`。

### 4. 启动 AI Service

```bash
cd ai-service
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

Windows PowerShell：

```powershell
cd ai-service
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

如果本机已有项目内的本地 Conda 环境，也可以直接使用：

```powershell
ai-service\.conda312\python.exe ai-service\main.py
```

### 5. 启动 Gateway

```bash
cd gateway
go run main.go
```

可用环境变量：

| 变量 | 默认值 | 说明 |
|---|---|---|
| `PORT` | `8080` | Gateway 监听端口 |
| `AI_SERVICE_URL` | `http://localhost:8000` | AI Service 地址 |
| `ALLOWED_ORIGINS` | `http://localhost:5173,http://127.0.0.1:5173` | CORS 白名单 |

### 6. 启动 Frontend

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:5173`。

## 页面

| 路由 | 页面 | 说明 |
|---|---|---|
| `/` | 首页 | 入口页，连接 RAG 和 Agent 两个模块 |
| `/love-master` | RAG 模块 | 知识问答、文件上传、检索过程和检索调试 |
| `/super-agent` | Agent 模块 | 徒步计划、天气适宜性、路线推荐、工具执行和确认 |
| `/llm-config` | LLM 配置 | 配置 LLM、Embedding、Rerank，保存到浏览器和 `.env` |

## API

Gateway 对外暴露 `/api/v1/*`，并代理到 AI Service。

| 方法 | 路径 | 说明 |
|---|---|---|
| `GET` | `/health` | Gateway 健康检查 |
| `GET` | `/api/v1/chat/health` | Agent 健康检查 |
| `POST` | `/api/v1/chat/sync` | 同步 Agent 对话 |
| `POST` | `/api/v1/chat/sse` | SSE Agent 对话 |
| `GET` | `/api/v1/chat/history/:chatId` | 对话历史 |
| `POST` | `/api/v1/chat/confirm` | 确认、拒绝或编辑高风险工具调用 |
| `GET` | `/api/v1/chat/pending/:chatId` | 查询待确认工具调用 |
| `GET` | `/api/v1/rag/health` | RAG 健康检查 |
| `POST` | `/api/v1/rag/upload` | 上传 RAG 文档 |
| `POST` | `/api/v1/rag/query` | SSE RAG 问答 |
| `GET` | `/api/v1/rag/documents` | 已上传文档列表 |
| `POST` | `/api/v1/rag/feishu/sync` | 同步单个飞书文档 |
| `POST` | `/api/v1/rag/feishu/default-sync` | 从默认飞书空间或文件夹同步 |
| `POST` | `/api/v1/models/fetch` | 从 OpenAI 兼容接口读取模型列表 |
| `POST` | `/api/v1/models/save-config` | 保存模型配置到 `ai-service/.env` |

AI Service 还直接暴露：

- `GET http://localhost:8000/health`
- `GET http://localhost:8000/api/v1/tools`
- `GET http://localhost:8000/api/v1/tools/health`
- `GET http://localhost:8000/docs`

## Agent 模块

Agent 入口位于 `ai-service/agent/agent.py`，请求理解位于 `ai-service/agent/intake.py`。

当前支持的意图：

- `general_chat`
- `knowledge_qa`
- `route_plan`
- `gear_check`
- `risk_assessment`
- `report_export`

执行路径：

1. `understand_request()` 先做确定性意图识别、槽位提取和当前位置归一化。
2. `HikingWorkflowRunner` 优先处理可确定完成的徒步工作流，例如天气适宜性和路线推荐。
3. 若工作流不能直接回答，则构建 Agent runtime policy，限制工具集合、工具预算和最大步骤数。
4. ReAct fallback 使用 LangGraph 和 OpenAI 兼容模型生成最终回答。
5. SSE 事件返回 `thought`、`tool_call`、`tool_result`、`approval_required`、`artifact`、`text`、`done`、`error` 等类型。

模型可见工具是 reference-style 的 8 个工具：

| 工具 | 说明 |
|---|---|
| `searchWeb` | 搜索公开网页信息 |
| `scrapeWebPage` | 读取指定 URL 内容 |
| `readFile` | 读取工作区文件 |
| `writeFile` | 写入工作区文件，高风险工具，执行前需要确认 |
| `downloadResource` | 下载资源 |
| `executeTerminalCommand` | 执行终端命令，关键风险工具 |
| `generatePDF` | 生成 PDF |
| `doTerminate` | Agent 内部终止控制 |

徒步领域能力不直接作为模型可见工具暴露，而是由内部适配器和确定性工作流使用：

- `geo_lookup`
- `weather_lookup`
- `route_research`
- `gear_checklist`
- `risk_assessment`
- `trip_report_export`
- `hiking_knowledge_search`

## RAG 模块

RAG 入口位于 `ai-service/api/rag.py`，核心组件位于 `ai-service/rag/`。

文档处理：

- 后端支持 `.txt`、`.md`、`.pdf`、`.docx`
- 上传文件保存到 `rag_docs/`
- 文本先归一化、降噪、切块，再写入检索存储
- 文档元数据会附带 source、title、doc_type、chunk 信息和实体抽取结果

检索路径：

1. QueryRewriter 对问题进行改写和多查询拓展。
2. VectorStoreRetriever 优先连接 PostgreSQL/pgvector，失败时降级到内存存储。
3. 对每个查询执行 semantic、BM25 keyword、entity 三路召回。
4. 使用 RRF 融合候选结果。
5. Reranker 可选开启，用于重排候选片段。
6. ContextAugmenter 将检索上下文注入最终回答。

过滤约定：

- 推荐使用 `filters.status`，例如 `{"filters": {"status": "feishu"}}`
- 旧字段 `status` 会归一化并返回诊断信息
- `user_id`、`agent_id`、`scope` 不是 RAG 查询支持的 top-level filter，会返回明确错误

前端会在折叠面板中展示隐私安全的检索调试信息，例如：

- 查询数和候选 chunk 数
- 存储后端：`pgvector` 或 `memory`
- source/signal/entity 命中计数
- 过滤器诊断

## Memory

记忆相关代码位于 `ai-service/memory/`。

当前实现包括：

- `FileChatMemory`：按 `chat_id` 保存对话历史。
- `SessionCompressor`：压缩短期会话上下文。
- `KnowledgeExtractor`：从对话中抽取长期知识项。
- `VectorStore`：使用 FAISS 或内存 fallback 保存长期知识向量。
- `MemoryCommitter`：只在回答完成后提交稳定偏好或行程相关记忆。

长期记忆写入采用保守去重策略：

- 同 scope/user/agent/type/subject/predicate/object 的精确重复会跳过。
- 近似重复只标记为 `merge_candidate`，不会删除或覆盖已有记忆。
- 写入报告包含 `dedupe_skip_count`、`outcome_status_counts` 等观测字段。

## MCP

### AMap MCP

当 `AMAP_MAPS_API_KEY` 或兼容变量 `AMAP_API_KEY` 存在时，AI Service 会配置官方高德 MCP：

```text
npx -y @amap/amap-maps-mcp-server
```

相关代码：

- `ai-service/mcp/client.py`
- `ai-service/mcp/amap.py`
- `ai-service/tools/hiking_domain.py`

Windows 下 `.cmd` / `.bat` 启动由 MCP client 包装处理。

### Image Search MCP

项目内置一个可选图片搜索 MCP Server：

```bash
cd mcp-server/image_search
pip install -r requirements.txt
set PEXELS_API_KEY=your-pexels-key
python server.py --transport stdio
```

SSE 模式：

```bash
python server.py --transport sse --port 8100
```

AI Service 检测到 `PEXELS_API_KEY` 后会使用默认的内置 server 路径启动该 MCP。通常只需要配置：

```env
PEXELS_API_KEY=your-pexels-key
```

## 目录结构

```text
ai-hiking/
├── ai-service/
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 环境变量配置
│   ├── api/                    # chat, rag, models, tools 路由
│   ├── agent/                  # LangGraph Agent、工作流、策略、性能指标
│   ├── rag/                    # 文档加载、检索、改写、重排、增强
│   ├── memory/                 # 对话历史、压缩、知识抽取、向量记忆
│   ├── mcp/                    # MCP stdio client 和 AMap 适配
│   └── tools/                  # Agent 工具与徒步领域工具
├── frontend/
│   ├── src/App.tsx             # 路由和主布局
│   ├── src/pages/              # Home, LoveMaster, SuperAgent, LlmConfig
│   ├── src/api/                # SSE、RAG、LLM 配置 API 客户端
│   └── src/components/         # 聊天、状态、记忆计量等组件
├── gateway/
│   ├── main.go                 # Gin 入口和路由注册
│   ├── config/                 # Gateway 环境变量
│   ├── handler/                # chat, rag, models, health 代理
│   └── middleware/             # CORS 和限流
├── mcp-server/image_search/    # Pexels 图片搜索 MCP Server
├── docker-compose.yml          # PostgreSQL/pgvector 与 Redis
├── MEMORY.md                   # 项目长期记忆
├── progress.md                 # Agent 会话进度
└── verify.json                 # Agent 验证记录
```

运行时生成目录通常会被 `.gitignore` 忽略：

- `ai-service/.env`
- `memory_store/`
- `rag_docs/`
- `workspace/`
- `repo-context.md`
- `frontend/dist/`
- `node_modules/`
- `.venv/`、`.conda*/`

## 常用命令

基础设施：

```bash
docker compose up -d
docker compose ps
docker compose down
```

AI Service：

```bash
cd ai-service
pip install -r requirements.txt
python main.py
python -m compileall -q agent api mcp memory rag tools main.py config.py
```

Gateway：

```bash
cd gateway
go run main.go
go test ./...
```

Frontend：

```bash
cd frontend
npm install
npm run dev
npm run build
npm test
```

当前 `frontend/package.json` 的测试脚本是 `node --test tests/*.test.mjs`。如果当前工作副本没有 `frontend/tests/*.test.mjs`，该命令不会有可运行的前端测试文件。

## 健康检查

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/chat/health
curl http://localhost:8000/api/v1/rag/health
curl http://localhost:8000/api/v1/tools/health
curl http://localhost:8080/health
```

前端本地检查：

```bash
curl http://localhost:5173/
curl http://localhost:5173/super-agent
curl http://localhost:5173/love-master
```

## 常见问题

### Agent 返回“主模型未配置 API Key”

处理方式：

- 在 `/llm-config` 页面保存 LLM 配置。
- 或在 `ai-service/.env` 中设置 `OPENAI_API_KEY`、`OPENAI_BASE_URL`、`OPENAI_MODEL`。

### RAG 没有检索结果

先检查：

- `EMBEDDING_API_KEY` 是否可用。
- PostgreSQL 是否启动。
- `DATABASE_URL` 是否指向 `localhost:5432`。
- 是否已经通过 `/love-master` 上传文档。

如果 pgvector 不可用，系统会降级到内存存储，但重启后内存中的 RAG 文档不会保留。

### Redis 连接失败

`docker-compose.yml` 将 Redis 容器端口 `6379` 映射到宿主机 `5379`。本地运行 AI Service 时建议设置：

```env
REDIS_URL=redis://localhost:5379/0
```

### AMap MCP 不可用

先确认：

- `AMAP_MAPS_API_KEY` 已设置。
- Node.js 和 `npx` 可用。
- `npx -y @amap/amap-maps-mcp-server` 能正常启动。
- `/api/v1/tools/health` 中的 MCP 配置状态符合预期。

### 飞书同步不可用

飞书同步依赖 `lark-cli`。如果 `lark-cli` 不在 PATH 中，`settings.feishu_enabled` 会返回 false，相关接口会提示未启用。

## 许可

当前仓库未包含独立的 `LICENSE` 文件。
