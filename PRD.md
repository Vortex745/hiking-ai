# PRD: ai-hiking — 多模态 AI Agent 系统

> 基于 LangChain + Go + React 构建的 AI Agent 系统，复刻 Yu AI Agent 的核心能力。

---

## 1. 产品定位

一个能自主决策、使用工具、检索知识的 AI Agent 系统。核心交付两条闭环流程：

- **Agent 执行流**：ReAct 范式，Agent 自主思考、调工具、多步推理、SSE 流式输出
- **RAG 检索流**：文档加载 → 向量化 → 查询重写 → 检索增强 → 生成回答

### 1.1 非目标

- 不涉及用户认证与权限管理
- 不涉及生产级监控与告警
- 不做单元测试覆盖（Phase 6 有余力再补）
- 不构建生产级 Docker 镜像（仅本地开发 Docker Compose）

---

## 2. 技术栈

| 层 | 技术 | 决策理由 |
|----|------|----------|
| AI 框架 | LangChain Python | Agent/RAG/Memory 生态最成熟 |
| API 网关 | Go + Gin | 高性能、社区大、中间件全 |
| 前端 | React + TypeScript + Vite | |
| 向量数据库 | PostgreSQL + pgvector | 与 RDBMS 合一，零额外运维 |
| 缓存/记忆 | Redis | 生产级对话记忆存储 |
| LLM | OpenAI 兼容 API | 单套 `ChatOpenAI` 配置，切 `base_url` 即切换模型 |
| MCP | Python langchain-mcp-adapters | Agent 无缝集成 MCP 工具 |

### 2.1 架构部署

- Docker Compose 管理基础设施（PostgreSQL + pgvector + Redis）
- AI 服务（Python）、网关（Go）、前端（React）本地 IDE 运行，热重载开发
- 单仓库微服务：各服务独立目录、独立 Dockerfile、独立部署

---

## 3. 系统架构

### 3.1 模块划分

```
ai-hiking/
├── ai-service/               # Python FastAPI + LangChain
│   ├── agent/                #   Agent 核心
│   │   ├── agent.py          #     ReAct Agent 定义
│   │   ├── prompts.py        #     System / Next Step Prompt
│   │   └── advisors.py       #     日志 / 重读 Advisor
│   ├── rag/                  #   RAG 管线
│   │   ├── loader.py         #     文档加载 + 分割
│   │   ├── retriever.py      #     pgvector 检索
│   │   ├── rewriter.py       #     查询重写（多查询扩展）
│   │   └── augmenter.py      #     上下文增强
│   ├── tools/                #   工具集
│   │   ├── web_search.py     #     SerpAPI 搜索
│   │   ├── web_scraping.py   #     网页抓取
│   │   ├── file_operation.py #     文件操作
│   │   ├── resource_download.py
│   │   ├── terminal.py       #     Shell 命令（白名单）
│   │   ├── pdf_generation.py
│   │   └── terminate.py
│   ├── memory/               #   对话记忆
│   │   ├── base.py           #     接口抽象
│   │   ├── file_memory.py    #     文件存储实现
│   │   └── redis_memory.py   #     Redis 实现
│   ├── mcp/                  #   MCP Client
│   │   └── client.py         #     langchain-mcp-adapters
│   ├── api/                  #   FastAPI 路由
│   │   ├── chat.py           #     /chat/sync /chat/sse
│   │   ├── rag.py            #     /rag/query
│   │   └── models.py
│   ├── main.py               #   FastAPI 入口
│   ├── config.py             #   env 驱动配置
│   └── requirements.txt
├── gateway/                  # Go Gin API 网关
│   ├── handler/
│   │   ├── chat.go           #   SSE 代理
│   │   └── health.go
│   ├── middleware/
│   │   ├── cors.go
│   │   └── ratelimit.go
│   ├── config/config.go
│   ├── main.go
│   ├── go.mod
│   └── go.sum
├── frontend/                 # React (TypeScript)
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── LoveMaster.tsx
│   │   │   └── SuperAgent.tsx
│   │   ├── components/
│   │   │   ├── ChatRoom.tsx
│   │   │   ├── AiAvatar.tsx
│   │   │   └── ConnectionStatus.tsx
│   │   ├── api/
│   │   │   └── sse.ts
│   │   └── App.tsx
│   ├── package.json
│   └── vite.config.ts
├── mcp-server/
│   └── image_search/
│       ├── server.py
│       └── requirements.txt
├── docker-compose.yml        # PostgreSQL + pgvector + Redis
└── README.md
```

### 3.2 数据流

**Agent 流**

```
用户输入 → React → Go 网关 → Python /chat/sse
  → AgentExecutor 开始 ReAct 循环
  → 思考 → 调用工具 → 工具结果 → 继续推理
  → 循环直到终止或达到 20 步
  → StreamingResponse → Go io.Copy → React EventSource → 打字机渲染
```

**RAG 流**

```
用户问题 → React → Go 网关 → Python /rag/query
  → QueryRewriter（多查询扩展）
  → VectorStoreRetriever（pgvector 检索）
  → ContextualAugmentation（上下文增强）
  → LLM 生成回答 → SSE 流式返回
```

---

## 4. 功能规格

### 4.1 Agent 执行引擎

| 功能 | 说明 | 映射原项目 |
|------|------|-----------|
| ReAct Agent | `create_react_agent` + `AgentExecutor`，最大 20 步 | YuManus |
| System Prompt | 定义 Agent 行为准则 | YuManus System Prompt |
| Next Step Prompt | 引导 Agent 逐步推理 | Next Step Prompt |
| 日志 Advisor | 记录每一步推理过程，方便调试 | MyLoggerAdvisor |
| 重读 Advisor | 允许 Agent 重新阅读对话历史 | ReReadingAdvisor |
| SSE 流式输出 | 边生成边输出，前端打字机效果 | AiController `/chat/sse` |

### 4.2 工具集

| 工具 | 功能 | 风险控制 |
|------|------|----------|
| WebSearchTool | 调用 SerpAPI 返回搜索结果摘要 | 无 |
| WebScrapingTool | Jsoup 解析 HTML 提取页面内容 | 限制请求频率 |
| FileOperationTool | 读写文件、创建目录、列出文件 | 限定工作目录 |
| ResourceDownloadTool | 下载网络资源到本地 | 限文件大小、类型 |
| TerminalOperationTool | 执行 shell 命令 | 白名单制，仅允许预定义命令 |
| PDFGenerationTool | 将文本转换为 PDF | 无 |
| TerminateTool | Agent 主动结束执行 | 无 |

### 4.3 RAG 管线

| 功能 | 说明 |
|------|------|
| 文档加载 | 支持 TXT/MD/PDF，RecursiveCharacterTextSplitter 分割 |
| 向量存储 | OpenAI Embeddings → pgvector |
| 查询重写 | MultiQueryRetriever 多查询扩展 |
| 上下文增强 | 检索结果注入 + 原始问题拼接 |
| 状态过滤 | 按 status 字段过滤（单身/恋爱/已婚），映射 LoveApp 场景 |

### 4.4 对话记忆

| 功能 | 说明 |
|------|------|
| 窗口管理 | ConversationBufferWindowMemory，默认 20 条 |
| 文件持久化 | 按 chatId 写入 JSON 文件，重启不丢 |
| Redis 持久化 | RedisChatMessageHistory，上线只需改配置 |
| 隔离 | 每个 chatId 独立存储 |

### 4.5 MCP 集成

| 功能 | 说明 |
|------|------|
| MCP Client | langchain-mcp-adapters 接入，Agent 自动发现工具 |
| MCP Server | fastmcp 实现，Stdio/SSE 双模式 |
| Image Search | Pexels API 图片搜索工具（首个 MCP 工具） |

### 4.6 前端页面

| 页面 | 路由 | 功能 |
|------|------|------|
| Home | `/` | 项目介绍入口 |
| LoveMaster | `/love-master` | RAG 问答，调用 RAG 管线 |
| SuperAgent | `/super-agent` | 通用 Agent，调用 Agent Executor |

ChatRoom 组件核心特性：

- SSE EventSource 连接
- 打字机逐字渲染效果
- 连接状态指示：connecting / connected / error
- AI 头像根据场景切换（LoveMaster / SuperAgent）

---

## 5. 实施计划

### Phase 1：基础设施 + 骨架（0.5 天）

- docker-compose.yml：PG（pgvector）+ Redis
- Python FastAPI 空入口 + /health
- Gin 网关 /health + /api/* 反向代理
- React Vite + Router + ChatRoom 骨架

**验收标准**：浏览器访问前端首页，三端 /health 200。

### Phase 2：Agent 执行流（2 天）

- 7 个工具实现（Terminal 带白名单）
- ReAct Agent + Prompts + Advisors
- /chat/sse 端点 + Gin SSE 代理
- ChatRoom 完整流式渲染

**验收标准**：输入"搜索 AI 新闻并保存到文件"，Agent 调用 WebSearch → FileOperation，前端流式显示。

### Phase 3：RAG 管线（1.5 天）

- 文档加载 + 分割 + 向量化 + pgvector
- 查询重写 + 上下文增强
- /rag/query + SSE 输出
- LoveMaster 页面

**验收标准**：提问，回答基于已入库文档内容生成。

### Phase 4：对话记忆（0.5 天）

- 文件存储实现 + 窗口管理
- Redis 存储实现（配置切换）
- Agent 传入 memory 参数

**验收标准**：先问"我叫小明"，再问"我叫什么" → 回答"小明"。

### Phase 5：MCP 集成（1 天）

- image_search MCP Server（Pexels API）
- MCP Client 接入 Agent

**验收标准**："找日落的图片" → Agent 调用 search_image，返回图片 URL。

### Phase 6：打磨（0.5 天）

- 连接状态指示
- 错误处理 + 超时回退
- AI 头像切换
- /health 集成检查
- README

---

## 6. 关键假设与风险

### 6.1 风险矩阵

| 风险 | 影响 | 概率 | 备用方案 |
|------|------|------|----------|
| Go SSE 代理引入明显延迟 | 流式体验差 | 低 | 前端直连 Python，Go 只处理非 AI 接口 |
| langchain-mcp-adapters 不兼容 | MCP 集成受阻 | 中 | Python 侧自建 MCP Client，JSON-RPC 协议 |
| OpenAI 兼容 API 行为差异 | 切模型时出错 | 低 | config.py 持 model_provider 字段，切换 LC 的 ChatXxx 类 |
| pgvector 性能不够 | RAG 检索慢 | 低 | 加 IVFFlat 索引，或换独立的向量数据库 |

### 6.2 假设

1. Go `io.Copy` + `http.Flusher` 能在长连接流式场景下保持低延迟
2. LangChain Python 的 AgentExecutor SSE 输出可以被 Go 正确逐块转发
3. OpenAI Embeddings API 在 RAG 管线中延迟可接受（< 500ms）

---

## 7. 验收总清单

- [ ] Phase 1：基础设施启动，三端 /health 全部 200
- [ ] Phase 2：Agent 成功调用至少 2 个工具完成任务
- [ ] Phase 3：RAG 基于文档内容正确回答问题
- [ ] Phase 4：对话记忆跨轮次正确保留上下文
- [ ] Phase 5：MCP 工具被 Agent 发现并调用
- [ ] Phase 6：前端错误状态有反馈，README 可用
