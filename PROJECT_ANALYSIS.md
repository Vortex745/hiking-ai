# Yu AI Agent 项目架构与流程剖析

## 一、项目概览

这是一个基于 Spring AI + Spring Boot 3.4 构建的多模态 AI Agent 系统。核心目标不是"调用 API"，而是打造能自主决策、使用工具、检索知识的智能体。

技术栈很明确：Spring AI Alibaba（对接通义千问）、Ollama（本地模型）、PostgreSQL + pgvector（向量数据库）、MCP 协议（模型上下文协议）。前端用 Vue 3 + Vite，整体走的是微服务思路——主应用、图片搜索 MCP 服务器各自独立部署。

---

## 二、系统架构分层

### 2.1 后端核心模块划分

```
yu-ai-agent (Spring Boot)
├── agent/          # Agent 核心逻辑层
├── tools/          # 工具集（Agent 可调用的能力）
├── rag/            # 检索增强生成（RAG）
├── chatmemory/     # 对话记忆管理
├── controller/     # HTTP 接口层
├── config/         # 配置类
└── demo/           # 示例代码（各种 AI 调用方式演示）
```

### 2.2 前端模块

```
yu-ai-agent-frontend (Vue 3)
├── views/          # 页面视图（Home、LoveMaster、SuperAgent）
├── components/     # 组件（ChatRoom、AiAvatarFallback 等）
└── api/            # API 调用封装
```

### 2.3 独立 MCP 服务器

```
yu-image-search-mcp-server
└── tools/ImageSearchTool.java  # 图片搜索工具（通过 MCP 协议暴露）
```

---

## 三、核心流程拆解

### 3.1 Agent 执行流程（YuManus）

这是整个系统的"大脑"。`YuManus` 继承自 `ToolCallAgent`，遵循 ReAct（Reasoning + Acting）范式：

```
用户输入 → YuManus 接收
    ↓
思考下一步该做什么（Next Step Prompt）
    ↓
决定：调用工具 / 直接回答 / 终止
    ↓
如果调用工具：
    - 从 ToolRegistration 获取可用工具列表
    - 执行工具（WebSearch、FileOperation、Terminal...）
    - 将工具结果反馈给 LLM
    ↓
LLM 基于工具输出继续推理
    ↓
循环直到达到最大步数（20步）或调用 TerminateTool
    ↓
返回最终结果（SSE 流式输出）
```

关键点：
- **System Prompt** 定义了 Agent 的行为准则
- **Next Step Prompt** 引导 Agent 逐步思考
- **MyLoggerAdvisor** 记录每一步的推理过程（方便调试）
- **ReReadingAdvisor** 让 Agent 能重新阅读之前的对话历史

### 3.2 RAG 检索流程（恋爱问答场景）

`LoveApp` 是专门针对恋爱咨询场景的应用，用了两种 RAG 策略：

#### 方案 A：云端知识库（阿里云 DashScope）

```
用户问题 → LoveAppRagCloudAdvisorConfig
    ↓
DashScopeDocumentRetriever 从云端索引检索
    ↓
检索到的文档片段注入到 prompt
    ↓
LLM 基于检索内容生成回答
```

#### 方案 B：本地向量库（PostgreSQL + pgvector）

```
文档加载（LoveAppDocumentLoader）
    ↓
文本分割（MyTokenTextSplitter）
    ↓
向量化并存储到 pgvector
    ↓
查询时：
    - QueryRewriter 重写问题（多查询扩展）
    - VectorStoreDocumentRetriever 检索相似文档
    - 按 status 字段过滤（单身/恋爱/已婚）
    ↓
LoveAppContextualQueryAugmenterFactory 增强查询
    ↓
LLM 生成回答
```

这里的巧妙之处在于：**同一套 RAG 框架，通过不同的 DocumentRetriever 实现，既能用云端服务，也能用本地数据库**。

### 3.3 对话记忆管理

`FileBasedChatMemory` 把聊天记录持久化到文件系统：

```
每次对话 → 根据 chatId 读取对应的历史消息
    ↓
MessageWindowChatMemory 维护最近 N 条消息（默认 20 条）
    ↓
新消息追加到窗口
    ↓
超出窗口的旧消息自动丢弃
    ↓
保存到文件（JSON 格式）
```

这样做的好处是：**重启服务后对话历史不丢失**，而且每个用户的对话隔离（通过 chatId）。

---

## 四、工具集详解

`ToolRegistration` 注册了 7 个核心工具，Agent 可以自主调用：

| 工具 | 功能 | 实现细节 |
|------|------|----------|
| **WebSearchTool** | 网络搜索 | 调用 SerpAPI（百度引擎），返回搜索结果摘要 |
| **WebScrapingTool** | 网页抓取 | Jsoup 解析 HTML，提取页面内容 |
| **FileOperationTool** | 文件操作 | 读写文件、创建目录、列出文件 |
| **ResourceDownloadTool** | 资源下载 | 下载网络资源到本地 |
| **TerminalOperationTool** | 终端命令 | 执行 shell 命令（有风险，需谨慎） |
| **PDFGenerationTool** | PDF 生成 | 将文本转换为 PDF 文档 |
| **TerminateTool** | 终止执行 | Agent 主动结束任务 |

这些工具通过 `@ToolParam` 注解声明参数，Spring AI 自动生成 JSON Schema，LLM 就能理解如何调用。

---

## 五、MCP 协议集成

MCP（Model Context Protocol）是让 AI 模型访问外部数据的标准协议。项目里有两个 MCP 相关组件：

### 5.1 MCP Client（主应用）

在 `application.yml` 中配置：

```yaml
spring:
  ai:
    mcp:
      client:
        enabled: true
        stdio:
          servers:
            yu-image-search:
              command: java
              args: -jar yu-image-search-mcp-server.jar
```

主应用作为 MCP Client，可以连接到多个 MCP Server，动态获取工具。

### 5.2 MCP Server（图片搜索）

`yu-image-search-mcp-server` 是一个独立的 Spring Boot 应用，暴露 `ImageSearchTool`：

```
Pexels API → ImageSearchTool.searchImage()
    ↓
返回图片 URL 列表
    ↓
通过 SSE 或 Stdio 协议传输给 Client
```

支持两种通信模式：
- **Stdio**：进程间通信（适合本地部署）
- **SSE**：HTTP Server-Sent Events（适合远程部署）

---

## 六、前端交互流程

### 6.1 聊天室组件（ChatRoom.vue）

```vue
用户输入 → 发送到后端 API
    ↓
建立 SSE 连接（EventSource）
    ↓
实时接收流式响应
    ↓
逐字显示 AI 回复（打字机效果）
    ↓
保存聊天记录到本地存储
```

关键特性：
- **流式输出**：不用等完整回答，边生成边显示
- **连接状态指示**：connecting / connected / error
- **AI 头像切换**：根据 AI 类型显示不同头像

### 6.2 三个主要页面

| 页面 | 路由 | 功能 |
|------|------|------|
| **Home** | `/` | 首页介绍 |
| **LoveMaster** | `/love-master` | 恋爱问答（调用 LoveApp） |
| **SuperAgent** | `/super-agent` | 通用 Agent（调用 YuManus） |

---

## 七、数据流转全景图

```
┌─────────────┐
│   用户输入   │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  AiController    │ ← HTTP 接口层
│  - /chat/sync    │
│  - /chat/sse     │
└──────┬───────────┘
       │
       ├──────────────┐
       ▼              ▼
┌────────────┐ ┌─────────────┐
│  LoveApp   │ │  YuManus    │
│ (恋爱问答)  │ │ (通用Agent)  │
└──────┬─────┘ └──────┬──────┘
       │               │
       ▼               ▼
┌────────────┐ ┌──────────────┐
│ RAG Advisor│ │ ToolCallback  │
│ - 云端检索  │ │ - WebSearch  │
│ - 本地检索  │ │ - FileOp     │
└──────┬─────┘ │ - Terminal   │
       │       └──────┬───────┘
       ▼              │
┌────────────┐        │
│VectorStore │        │
│(pgvector)  │        │
└────────────┘        │
                      ▼
               ┌──────────────┐
               │  LLM (Qwen)  │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │ SSE 流式返回  │
               └──────┬───────┘
                      │
                      ▼
               ┌──────────────┐
               │  前端展示     │
               └──────────────┘
```

---

## 八、关键技术决策分析

### 8.1 为什么用 Spring AI 而不是 LangChain？

LangChain4j 也有引入（`langchain4j-community-dashscope`），但主力是 Spring AI。原因可能是：
- **生态整合**：Spring Boot 原生支持，配置简单
- **类型安全**：Java 强类型，比 Python 更易维护
- **企业级特性**：事务管理、监控、日志开箱即用

### 8.2 为什么同时支持云端和本地 RAG？

- **云端（DashScope）**：无需维护向量数据库，适合快速原型
- **本地（pgvector）**：数据可控，成本低，适合生产环境

这种设计让系统能在不同场景下灵活切换。

### 8.3 为什么用 MCP 协议？

传统做法是把所有工具硬编码在主应用里。MCP 的优势：
- **解耦**：工具可以独立开发、部署
- **可扩展**：新增工具只需启动新的 MCP Server
- **标准化**：符合行业趋势（Anthropic、OpenAI 都在推）

### 8.4 为什么用文件存储对话记忆？

没用 Redis 或数据库，而是直接用文件系统：
- **简单**：无需额外依赖
- **持久化**：重启不丢数据
- **隔离**：每个 chatId 一个文件，天然隔离

缺点是并发性能差，但对于 Demo 级别够用了。

---

## 九、潜在问题与改进方向

### 9.1 当前局限

1. **安全性**：`TerminalOperationTool` 能执行任意命令，风险极高
2. **并发**：文件-based ChatMemory 不适合高并发场景
3. **容错**：工具调用失败时缺少重试机制
4. **监控**：没有指标采集（请求量、延迟、错误率）

### 9.2 可优化点

1. **工具沙箱**：限制 TerminalOperationTool 的命令白名单
2. **Redis ChatMemory**：替换文件存储，提升并发性能
3. **熔断降级**：LLM 超时或失败时的兜底策略
4. **A/B 测试**：对比不同 RAG 策略的效果
5. **缓存层**：常见问题直接返回缓存答案，减少 LLM 调用

---

## 十、部署架构

### 10.1 Docker 部署

主应用 Dockerfile：

```dockerfile
FROM maven:3.9-amazoncorretto-21
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package -DskipTests
EXPOSE 8123
CMD ["java", "-jar", "/app/target/yu-ai-agent-0.0.1-SNAPSHOT.jar", "--spring.profiles.active=prod"]
```

前端 Dockerfile 类似，用 Nginx 托管静态文件。

### 10.2 推荐拓扑

```
                    ┌─────────────┐
                    │   Nginx     │ ← 反向代理 + 静态资源
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
     ┌────────────┐ ┌──────────┐ ┌──────────┐
     │ Frontend   │ │ Backend  │ │ MCP      │
     │ (Vue)      │ │ (Spring) │ │ Server   │
     └────────────┘ └────┬─────┘ └──────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
     ┌────────────┐ ┌────────┐ ┌────────┐
     │ PostgreSQL │ │ Redis  │ │ OSS    │
     │ (pgvector) │ │(可选)  │ │(可选)  │
     └────────────┘ └────────┘ └────────┘
```

---

## 十一、总结

这个项目的核心价值不在于"调用了多少个 API"，而在于**展示了如何构建一个完整的 AI Agent 系统**：

1. **Agent 层**：ReAct 范式 + 工具调用 + 多步推理
2. **RAG 层**：云端/本地双方案 + 查询重写 + 上下文增强
3. **记忆层**：对话历史管理 + 持久化存储
4. **工具层**：7 种工具 + MCP 协议扩展
5. **交互层**：SSE 流式输出 + Vue 前端

它不是一个"玩具项目"，而是一个**可演进的生产级架构雏形**。如果要落地到真实业务，需要补上安全、监控、测试这三块短板。
