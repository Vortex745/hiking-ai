# 🏔️ ai-hiking

**多模态 AI Agent 系统** — 以户外徒步为场景，基于 LangChain + Go + React 构建的智能助手，集成 ReAct Agent、RAG 知识检索、三层记忆架构、MCP 工具发现和多种领域工具。

---

## 🧱 系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            Frontend                                      │
│                    React 18 + TypeScript + Vite                           │
│               TailwindCSS · React Router · SSE Stream                     │
│                     :5173  (Vite dev server)                              │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │  HTTP / SSE
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         API Gateway                                       │
│                       Go + Gin Framework                                  │
│              SSE Proxy · CORS · Rate Limiting · Health                    │
│                     :8080  (gateway)                                      │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │  HTTP Proxy
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         AI Service                                        │
│                    Python FastAPI + LangChain                              │
│                                                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌──────────┐       │
│  │  Agent   │ │   RAG    │ │  Memory  │ │   MCP   │ │  Tools   │       │
│  │ ReAct +  │ │ Rewriter │ │ Session  │ │ Client  │ │ WebSearch│       │
│  │ LangGraph│ │ Retriever│ │Knowledge │ │ FastMCP │ │ Terminal │       │
│  │ Intent   │ │ Reranker │ │ Vector   │ │         │ │ PDF Gen  │       │
│  │ Slots    │ │ Augment  │ │ Redis    │ │         │ │ Hiking   │       │
│  └──────────┘ └──────────┘ └──────────┘ └─────────┘ └──────────┘       │
│                     :8000  (uvicorn)                                      │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
          ┌──────────────┐      ┌──────────────┐
          │  PostgreSQL   │      │    Redis      │
          │  + pgvector   │      │   缓存 / 记忆  │
          │  :5432        │      │   :5379       │
          └──────────────┘      └──────────────┘
                    ▲
                    │    MCP Protocol (stdio / SSE)
          ┌─────────┴─────────┐
          │   MCP Server       │
          │ Image Search       │
          │ (Pexels API)       │
          └───────────────────┘
```

### 数据流

```
Agent 对话:
  User → React → Go Gateway → FastAPI /chat/sse
       → AgentExecutor ReAct Loop (LangGraph)
       → 工具调用 (WebSearch / Terminal / Hiking tools)
       → SSE 流式返回

RAG 问答:
  User → React → Go Gateway → FastAPI /rag/query
       → QueryRewriter → VectorStoreRetriever (pgvector)
       → Reranker → ContextualAugmenter → LLM
       → SSE 流式返回
```

---

## 🛠 技术栈

| 层 | 技术 | 版本 |
|---|---|---|
| **AI 服务** | Python · FastAPI · LangChain · LangGraph | Python 3.12+ |
| **API 网关** | Go · Gin | Go 1.22 |
| **前端** | React 18 · TypeScript · Vite · TailwindCSS · React Router | Node 18+ |
| **向量数据库** | PostgreSQL + pgvector | pg16 |
| **缓存 / 会话** | Redis | 7 Alpine |
| **LLM** | OpenAI 兼容 API (单套配置切 `base_url` 即可切换模型) | — |
| **Embedding** | OpenAI 兼容接口 (支持 ModelScope / Qwen3-Embedding) | — |
| **MCP** | Python `langchain-mcp-adapters` + `fastmcp` | — |
| **容器化** | Docker Compose | 3.8 |

---

## 🚀 快速开始

### 前置条件

- **Python 3.12+** (推荐使用 conda 或 venv)
- **Go 1.22+**
- **Node.js 18+** (推荐 20 LTS)
- **Docker & Docker Compose**
- **OpenAI 兼容 API Key** (支持任意兼容服务，如 DeepSeek、ModelScope、OpenAI 等)

### 1. 克隆仓库

```bash
git clone <repo-url> ai-hiking
cd ai-hiking
```

### 2. 环境变量配置

在 `ai-service/` 下创建 `.env` 文件：

```bash
# === LLM (OpenAI 兼容) ===
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4o

# === Embedding (OpenAI 兼容) ===
EMBEDDING_BASE_URL=https://api.openai.com/v1
EMBEDDING_API_KEY=sk-your-key-here
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536

# === Rerank (可选) ===
RERANK_BASE_URL=https://api-inference.modelscope.cn/v1
RERANK_API_KEY=your-modelscope-key
RERANK_MODEL=Qwen/Qwen3-Reranker-8B
RERANK_ENABLED=true

# === Database ===
DATABASE_URL=postgresql://ai_hiking:ai_hiking@localhost:5432/ai_hiking
REDIS_URL=redis://localhost:5379/0

# === 高德地图 (天气/地理查询) ===
AMAP_API_KEY=your-amap-key
```

### 3. 启动基础设施 (PostgreSQL + Redis)

```bash
docker compose up -d
```

### 4. 启动 AI 服务

```bash
cd ai-service

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
# .venv\Scripts\activate    # Windows

# 安装依赖
pip install -r requirements.txt

# 启动 (端口 8000)
python main.py
```

### 5. 启动 API 网关

```bash
cd gateway
go run main.go
# 默认端口 8080，可通过环境变量 GATEWAY_PORT 修改
```

### 6. 启动前端

```bash
cd frontend
npm install
npm run dev
# Vite dev server 运行在 :5173，自动代理 /api 到 :8080
```

### 7. (可选) 启动 MCP Server

```bash
cd mcp-server/image_search
pip install -r requirements.txt
export PEXELS_API_KEY=your-pexels-key
python server.py --transport stdio
# 或 SSE 模式: python server.py --transport sse --port 8100
```

### 访问

- **前端页面**: http://localhost:5173
- **Gateway Health**: http://localhost:8080/health
- **AI Service Health**: http://localhost:8000/health
- **API 文档**: http://localhost:8000/docs

---

## 📂 项目结构

```
ai-hiking/
├── ai-service/                    # Python AI 服务
│   ├── main.py                    # FastAPI 入口
│   ├── config.py                  # 配置管理 (Settings)
│   ├── requirements.txt           # Python 依赖
│   ├── .env                       # 环境变量 (不入库)
│   ├── agent/                     # ReAct Agent
│   │   ├── agent.py               # AIAgent 核心 (LangGraph ReAct)
│   │   ├── advisors.py            # Logger / ReReading Advisor
│   │   ├── intake.py              # 请求理解 (意图识别、槽位提取)
│   │   ├── prompts.py             # System Prompt / Next Step Prompt
│   │   └── task_exit.py           # 任务退出控制器
│   ├── rag/                       # RAG 检索增强
│   │   ├── loader.py              # 文档加载 (PDF / Markdown / Feishu)
│   │   ├── retriever.py           # 向量检索 (pgvector)
│   │   ├── rewriter.py            # Query 改写
│   │   ├── reranker.py            # 重排序
│   │   ├── augmenter.py           # 上下文增强
│   │   ├── feishu.py              # 飞书文档同步
│   │   └── text_processing.py     # 文本清洗
│   ├── memory/                    # 三层记忆架构
│   │   ├── base.py                # 记忆抽象基类
│   │   ├── file_memory.py         # 文件存储
│   │   ├── redis_memory.py        # Redis 存储
│   │   ├── vector_store.py        # FAISS 向量记忆
│   │   ├── memory_manager.py      # 记忆管理器
│   │   ├── compressor.py          # 记忆压缩
│   │   ├── committer.py           # 记忆提交策略
│   │   └── knowledge.py           # 知识抽取
│   ├── mcp/                       # MCP 客户端
│   │   └── client.py              # MCP 工具发现与加载
│   ├── tools/                     # Agent 工具集
│   │   ├── tool_registry.py       # 工具注册中心 (风险等级、限流)
│   │   ├── web_search.py          # Web 搜索
│   │   ├── web_scraping.py        # 网页抓取
│   │   ├── file_operation.py      # 文件操作
│   │   ├── terminal.py            # 终端命令 (白名单)
│   │   ├── pdf_generation.py      # PDF 生成 (ReportLab)
│   │   ├── resource_download.py   # 资源下载
│   │   ├── terminate.py           # 任务终止
│   │   ├── hiking_knowledge.py    # 徒步知识 RAG 检索
│   │   ├── hiking_domain.py       # 徒步领域工具 (天气/路线/装备/风险评估/报告导出)
│   │   └── risk_classifier.py     # 工具风险分级
│   ├── api/                       # API 路由
│   │   ├── chat.py                # /chat/sse, /chat/sync, /chat/history
│   │   ├── rag.py                 # /rag/query, /rag/upload, /rag/documents
│   │   ├── tools.py               # /tools 工具列表
│   │   ├── models_router.py       # /models/fetch 模型列表
│   │   └── models.py              # 数据模型 (RuntimeLlmConfig 等)
│   └── tests/                     # 测试
│
├── gateway/                       # Go API 网关
│   ├── main.go                    # 入口 (路由注册)
│   ├── go.mod / go.sum            # Go 模块依赖
│   ├── config/
│   │   └── config.go              # 配置加载
│   ├── handler/
│   │   ├── chat.go                # Chat SSE/Sync/History 代理
│   │   ├── health.go              # 健康检查
│   │   ├── rag.go                 # RAG 上传/查询/文档 代理
│   │   └── models.go              # 模型列表代理
│   └── middleware/
│       ├── cors.go                # CORS 中间件
│       └── ratelimit.go           # 限流中间件
│
├── frontend/                      # React 前端
│   ├── index.html                 # HTML 入口
│   ├── package.json               # 依赖与脚本
│   ├── vite.config.ts             # Vite 配置 (含 API 代理)
│   ├── tailwind.config.cjs        # Tailwind 配置
│   ├── tsconfig.json              # TypeScript 配置
│   ├── src/
│   │   ├── main.tsx               # React 入口
│   │   ├── App.tsx                # 路由 + 侧边栏布局
│   │   ├── pages/
│   │   │   ├── Home.tsx           # 首页 (项目介绍)
│   │   │   ├── LoveMaster.tsx     # RAG 知识问答页
│   │   │   ├── SuperAgent.tsx     # 通用 Agent 对话页
│   │   │   └── LlmConfig.tsx      # LLM 配置页
│   │   ├── components/
│   │   │   ├── ChatRoom.tsx       # 聊天室 (SSE 流式打字)
│   │   │   ├── ConnectionStatus.tsx
│   │   │   ├── ConversationMemoryMeter.tsx  # 记忆占用计量表
│   │   │   └── AiAvatar.tsx       # AI 头像
│   │   └── api/
│   │       ├── config.ts          # API 配置
│   │       ├── sse.ts             # SSE 客户端
│   │       ├── ragStream.ts       # RAG 流式请求
│   │       ├── llmConfig.ts       # LLM 配置 API
│   │       └── conversationMemory.ts  # 记忆 API
│   └── tests/                     # 前端测试
│
├── mcp-server/                    # MCP Server
│   └── image_search/
│       ├── server.py              # 图片搜索 MCP Server (Pexels API)
│       └── requirements.txt       # Python 依赖
│
├── memory_data/                   # 持久化记忆数据
├── rag_docs/                      # RAG 文档库 (Markdown / PDF)
├── docker-compose.yml             # PostgreSQL + Redis 编排
└── README.md                      # 本文件
```

---

## ✨ 功能亮点

### 🤖 ReAct Agent

- 基于 **LangGraph** 的 ReAct 循环，最多 6 步推理
- **意图识别** + **槽位提取**：自动理解用户请求类型（知识问答、路线规划、装备检查、风险评估、报告导出）
- **工具按需加载**：根据意图只暴露相关工具，减少模型幻觉
- **预取优化**：天气/路线请求自动预取 geo_lookup + weather_lookup / route_research，跳过完整 ReAct 循环直接回答
- **工具确认机制**：高危工具 (terminal、file_operation 等) 需用户审批后才能执行
- **风险分级**：每个工具标记 LOW / MEDIUM / HIGH / CRITICAL 风险等级
- **流式 SSE**：实时返回思考过程、工具调用、工具结果和最终回答

### 📚 RAG 检索增强

- **文档加载**：支持 PDF、Markdown、飞书文档等多源摄入
- **向量化**：通过 OpenAI 兼容 Embedding API 向量化后存入 pgvector
- **Query 改写**：自动将口语化查询改写为检索优化形式
- **重排序**：支持 Reranker (如 Qwen3-Reranker) 提升检索精度
- **上下文增强**：检索结果注入 LLM 上下文，带来源引用

### 🧠 三层记忆架构

- **会话记忆**：短期对话窗口管理，支持 File / Redis 两种后端
- **知识记忆**：FAISS 向量存储，长期知识抽取与检索
- **记忆压缩**：自动摘要压缩，控制上下文窗口
- **记忆计量表**：前端可视化当前记忆使用情况

### 🔌 MCP 工具扩展

- **MCP Client**：通过 `langchain-mcp-adapters` 动态发现和加载外部 MCP 工具
- **MCP Server**：内置图片搜索 MCP Server，基于 Pexels API，支持 stdio / SSE 双模式

### 🏕️ 徒步领域工具

| 工具 | 说明 |
|---|---|
| `weather_lookup` | 天气查询 (高德 API) |
| `geo_lookup` | 地理定位反查 (高德 API) |
| `route_research` | 路线搜索与研究 |
| `hiking_knowledge_search` | 徒步知识 RAG 检索 |
| `gear_checklist` | 装备清单生成 |
| `risk_assessment` | 风险等级评估 |
| `trip_report_export` | 出行报告导出 (Markdown / PDF) |

### 🛡 通用工具

| 工具 | 说明 |
|---|---|
| `web_search` | 网页搜索 |
| `web_scraping` | 网页内容抓取 |
| `file_operation` | 文件读写操作 |
| `terminal` | 终端命令执行 (白名单安全策略) |
| `generate_pdf` | PDF 文档生成 |
| `resource_download` | 资源下载 |

---

## 📱 页面路由

| 路由 | 页面 | 说明 |
|---|---|---|
| `/` | 首页 (Home) | 项目介绍、功能概览 |
| `/love-master` | RAG 模块 (LoveMaster) | 基于知识库的徒步问答，支持文件上传和飞书同步 |
| `/super-agent` | Agent 模块 (SuperAgent) | 通用 ReAct Agent 对话，实时 SSE 打字效果 |
| `/llm-config` | LLM 配置 | 运行时切换模型、Base URL、API Key |

---

## 📄 License

MIT
