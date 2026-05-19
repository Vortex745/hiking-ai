# AI Hiking Agent PRD

> 版本：v0.1  
> 日期：2026-05-18  
> 状态：规划稿  
> 范围：`ai-service/agent`、`ai-service/tools`、`ai-service/mcp`、`ai-service/memory`、`api/chat`、前端 SuperAgent 流式展示

## 1. 背景

AI Hiking 当前的 Agent 已经从早期关键词分支改成统一的 LangGraph ReAct 链路。核心代码在 `ai-service/agent/agent.py`：

- 使用 `langgraph.prebuilt.create_react_agent` 创建 ReAct Agent。
- 固定注册 7 个工具：`web_search`、`web_scraping`、`file_operation`、`resource_download`、`terminal`、`generate_pdf`、`terminate`。
- `aexecute_stream()` 通过 `astream(stream_mode="updates")` 输出 `thought`、`tool_call`、`tool_result`、`text`、`done` 事件。
- `MemoryManager` 会在每次执行前处理历史，注入会话摘要和长期记忆。
- 前端 `SuperAgent.tsx` 已能显示思考、工具调用和工具结果，但这些事件现在是粗粒度文本。

这套实现能跑通 Demo，但还不够像一个可控的户外 Agent。问题主要不在“有没有工具”，而在工具是否分层、可选、可审计、能恢复、能被用户批准。

## 2. 调研依据

本 PRD 按项目要求先重新生成并阅读 `repo-context.md` 与 `MEMORY.md`，再阅读当前 Agent、工具、MCP、记忆和前端流式代码。

外部文档使用 Firecrawl CLI 读取 LangChain 最新文档，命令验证结果：

- `npx firecrawl-cli@latest --status`：已通过 `FIRECRAWL_API_KEY` 认证，CLI 版本 `1.18.0`。
- `npx firecrawl-cli@latest map https://docs.langchain.com/oss/python/langchain --limit 80`
- `npx firecrawl-cli@latest map https://docs.langchain.com/oss/python/langgraph --limit 80`
- 针对关键页面执行 `scrape -f markdown --only-main-content`。

主要参考页面：

- [LangChain Agents](https://docs.langchain.com/oss/python/langchain/agents)
- [LangChain Tools](https://docs.langchain.com/oss/python/langchain/tools)
- [LangChain Middleware](https://docs.langchain.com/oss/python/langchain/middleware/overview)
- [LangChain Built-in Middleware](https://docs.langchain.com/oss/python/langchain/middleware/built-in)
- [LangChain Short-term memory](https://docs.langchain.com/oss/python/langchain/short-term-memory)
- [LangChain Long-term memory](https://docs.langchain.com/oss/python/langchain/long-term-memory)
- [LangChain MCP](https://docs.langchain.com/oss/python/langchain/mcp)
- [LangChain Streaming](https://docs.langchain.com/oss/python/langchain/streaming)
- [LangChain Human-in-the-loop](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
- [LangChain Structured output](https://docs.langchain.com/oss/python/langchain/structured-output)
- [LangChain Guardrails](https://docs.langchain.com/oss/python/langchain/guardrails)
- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)
- [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [LangGraph Durable execution](https://docs.langchain.com/oss/python/langgraph/durable-execution)
- [LangGraph Streaming](https://docs.langchain.com/oss/python/langgraph/streaming)

重要约束：项目当前依赖是 `langchain==0.3.0`、`langgraph==0.2.0`，而最新文档主要面向 LangChain/LangGraph 1.x 的 `create_agent`、middleware、checkpointer、store、v2 streaming 等能力。落地时不能直接照搬最新示例，必须先做兼容性评估。短期可以把这些模式回填到现有 `create_react_agent` 封装里，中期再规划 1.x 迁移。

## 3. 目标

1. 让 Agent 工具集从“固定 7 个工具”升级为“按场景、权限、风险动态选择的工具系统”。
2. 让 ReAct 链路从“模型直接循环调用工具”升级为“请求准入、上下文装配、工具选择、执行预算、审批、流式观察、记忆提交”的完整链路。
3. 保留现有 Python/FastAPI + Go Gateway + React SSE 架构，不为了文档调研改技术栈。
4. 优先服务 AI Hiking 的真实场景：徒步计划、路线资料检索、装备清单、安全提醒、知识库问答、文件/PDF 产出。

非目标：

- 不在本阶段实现多 Agent 编排平台。
- 不把 RAG 模块整体塞进 Agent 内部；Agent 只通过受控工具调用 RAG 能力。
- 不开放任意终端命令或任意文件系统访问。
- 不把所有 LangChain 最新 middleware 一次性接入生产链路。

## 4. 当前问题

### 4.1 工具集问题

当前工具是静态列表，模型每次都看到全部工具。工具少时还能工作，但随着 MCP、RAG、地图、天气、文件搜索加入，工具说明会占用上下文，也会提高误调用概率。

当前 `terminal` 工具有白名单，但仍是模型可直接触发的操作。`file_operation` 限定在 `./workspace`，这是对的，但缺少操作前审批和可审计的 artifact 元数据。`resource_download` 定义了允许扩展名，但没有实际拒绝不在白名单内的扩展名，这是后续修复项。

`MCPClient` 已有雏形，但没有接入 `AVAILABLE_TOOLS`，也没有处理 MCP tool 的结构化内容、多模态内容、鉴权、状态注入和错误拦截。

### 4.2 ReAct 链路问题

当前链路能输出中粒度事件，但状态并不持久。用户刷新、服务重启、工具执行到一半失败时，无法从某个 checkpoint 恢复。ReAct 的每一步也没有统一的 run_id、step_id、tool_call_id、artifact_id。

记忆现在在 Agent 外部注入：`FileChatMemory` 保存聊天记录，`MemoryManager` 生成摘要和长期知识，再拼到系统 prompt。这能工作，但没有变成 LangGraph 的 thread state 或 store，也就不能天然支持时间旅行、断点续跑、HITL 审批和工具状态更新。

### 4.3 用户体验问题

前端把 `thought/tool_call/tool_result` 直接拼到聊天气泡。用户能看到过程，但过程和最终回答混在一起。后续应该把执行过程折叠显示，把最终回答保持干净，同时提供“查看工具证据”和“批准/拒绝操作”的交互。

## 5. 核心用户场景

### 场景 A：徒步计划生成

用户输入目的地、天数、体能、季节、装备水平。Agent 需要澄清缺失条件，检索路线资料和天气风险，生成行程、装备清单、风险提醒，必要时导出 PDF。

### 场景 B：知识库辅助问答

用户询问户外知识或已上传文档内容。Agent 应优先调用 RAG 检索工具，不凭空回答。检索结果不足时说明缺口，并建议上传资料或放宽问题范围。

### 场景 C：资料整理与文件产出

用户要求把搜索结果、路线规划、装备清单保存为 Markdown 或 PDF。Agent 可以写入 workspace，但写文件前要展示路径、摘要和影响范围。覆盖已有文件时需要审批。

### 场景 D：调试与执行任务

用户让 Agent 检查本地文件、运行低风险命令、汇总结果。Agent 可以使用文件搜索、文件读取和受限终端。任何删除、移动、下载可执行文件、访问敏感路径的操作都必须被拒绝或走审批。

## 6. 工具集规划

工具要按“能力域 + 风险等级 + 是否可自动调用”来注册，而不是简单放进一个数组。

### 6.1 工具注册元数据

每个工具都应有统一描述：

```python
class AgentToolSpec(TypedDict):
    name: str
    domain: str
    risk_level: Literal["safe", "review", "dangerous"]
    auto_allowed: bool
    requires_approval: bool
    max_calls_per_run: int
    timeout_seconds: float
    result_policy: Literal["raw", "compact", "artifact"]
    description_for_model: str
```

### 6.2 第一批工具集

| 工具域 | 工具 | 当前状态 | 风险 | PRD 建议 |
| --- | --- | --- | --- | --- |
| 网络检索 | `web_search` | 已有，DuckDuckGo Instant Answer | safe | 保留名称，但替换为可靠搜索适配器；返回标题、摘要、URL、时间 |
| 网页读取 | `web_scraping` / `read_url` | 已有，BeautifulSoup | safe | 增加 Firecrawl/普通抓取双实现；强制返回来源 URL 和提取时间 |
| RAG 检索 | `rag_search` | 未作为 Agent 工具暴露 | safe | 把本地 RAG 查询封装成只读工具，返回 chunks、score、source |
| 飞书知识 | `feishu_sync`、`feishu_search` | RAG API 已有同步能力 | review | 同步是写操作需审批；搜索是只读可自动 |
| 文件读取 | `file_read`、`file_list` | `file_operation` 混合实现 | safe | 拆分读/列目录，保留 workspace 沙箱 |
| 文件写入 | `file_write`、`file_edit` | `file_operation.write` | review | 写入、覆盖、编辑必须有路径校验和审批策略 |
| 文件搜索 | `glob_search`、`grep_search` | 未接入 | safe | 参考 LangChain File Search middleware，用 ripgrep 做代码/资料定位 |
| 资源下载 | `resource_download` | 已有 | review | 实际校验扩展名、MIME、大小；下载前说明来源和保存路径 |
| PDF 生成 | `generate_pdf` | 已有 | review | 生成前先产出 Markdown/结构化正文；返回 artifact 元数据 |
| 终端执行 | `terminal` / `shell` | 已有白名单 | dangerous | 保留白名单；默认只读命令可自动，写/网络/进程类命令拒绝或审批 |
| 图片搜索 | `image_search` | MCP server 已有 | safe | 通过 MCP adapter 正式接入，适合路线/地点图片辅助 |
| 计划管理 | `write_todos` | 未接入 | safe | 复杂任务自动维护 plan，前端可折叠展示 |
| 用户确认 | `ask_user` / `interrupt` | 未接入 | review | 缺少关键约束或敏感操作前暂停 |
| 终止控制 | `terminate` | 已有 | safe | 继续保留，但终止要带 reason 和 final status |

### 6.3 徒步领域工具建议

这些工具不一定第一阶段全做，但应进入工具注册表：

- `weather_lookup`：按目的地和日期查天气、温度、降水、风力。安全相关信息必须标注来源和时间。
- `route_lookup`：查路线、海拔、里程、预计耗时、交通信息。第一版可以先走网页搜索 + RAG，后续接地图 API。
- `gear_checklist`：根据季节、天数、路线强度生成装备清单。可以先做规则工具，减少模型自由发挥。
- `risk_assessment`：把天气、海拔、路线强度、用户经验转成风险等级和应对建议。
- `itinerary_export`：将行程结构化后输出 Markdown/PDF。

## 7. 目标 ReAct 链路

目标链路如下：

```text
用户请求
  -> 请求准入与意图识别
  -> 构建 AgentContext
  -> 读取 thread state 与长期 store
  -> 动态系统 prompt 与工具选择
  -> ReAct 循环
      -> 模型思考
      -> 工具调用预算检查
      -> 审批/拒绝/编辑
      -> 工具执行、重试、结果压缩
      -> 状态更新与流式事件
  -> 结构化最终输出
  -> 记忆提交与审计记录
  -> SSE 完成
```

### 7.1 请求准入

进入模型前先做确定性检查：

- 空输入、超长输入、明显恶意指令直接拒绝或要求缩短。
- 检测 API key、手机号、邮箱等敏感内容，至少在日志和工具结果里脱敏。
- 识别任务类型：问答、路线规划、资料检索、文件产出、终端执行、知识库操作。
- 计算本轮默认预算：模型调用上限、工具调用上限、网络工具上限、最大运行时长。

### 7.2 AgentContext

每次调用都要有明确上下文：

```python
class AgentContext(TypedDict):
    chat_id: str
    thread_id: str
    user_id: str | None
    permissions: list[str]
    module: Literal["super_agent"]
    risk_mode: Literal["normal", "review_required"]
    model_settings: dict
```

`chat_id` 继续兼容当前前端，`thread_id` 用于 LangGraph checkpointer。后续如果登录体系上线，`user_id` 用于长期记忆命名空间。

### 7.3 AgentState

当前 state 不能只有 `messages`。建议扩展：

```python
class HikingAgentState(AgentState):
    task_type: str
    current_plan: list[dict]
    tool_budget: dict
    artifacts: list[dict]
    memory_context: dict
    approvals: list[dict]
    last_error: str | None
```

这样工具可以通过 `ToolRuntime` 读取当前计划、写入 artifact、更新用户偏好，而不是把所有状态塞进自然语言 prompt。

### 7.4 动态 prompt

系统 prompt 不应该只是一段静态中文。应按任务动态补充：

- 徒步规划：补路线、天气、装备、安全核验规则。
- 文件产出：补 workspace 限制、覆盖文件审批规则。
- 终端执行：补只读优先、命令最小化、禁止危险操作规则。
- RAG 问答：补“证据不足就说明不足，不编造”。

这对应 LangChain 文档里的 dynamic system prompt / context engineering 思路：把对本轮有用的 state、store、runtime context 注入模型，而不是长期堆在 prompt 里。

### 7.5 动态工具选择

第一阶段先实现确定性工具过滤：

- 默认只给模型：`web_search`、`read_url`、`rag_search`、`terminate`。
- 用户明确要求文件操作时，再暴露文件工具。
- 用户明确要求执行命令时，再暴露终端工具。
- 需要导出文档时，再暴露 `generate_pdf`。
- MCP 工具按 server、权限和任务类型动态加入。

第二阶段再引入 LLM tool selector：当工具超过 10 个时，用小模型先筛出 3 到 5 个相关工具，并始终保留 `terminate` 与必要的只读工具。

### 7.6 工具执行策略

每次工具调用都要经过统一包装层：

- 参数校验：路径、URL、文件大小、命令白名单。
- 调用预算：单工具、本轮、当前 thread 都要有限制。
- 重试：网络型工具支持指数退避；文件/终端写操作不自动重试。
- 结果压缩：长网页、长命令输出、长 RAG chunks 进入 artifact，只把摘要给模型。
- 审计：记录 tool_call_id、tool_name、args_digest、status、duration、result_size。

### 7.7 审批与中断

以下操作默认需要用户审批：

- 写文件、覆盖文件、生成 PDF。
- 下载外部资源。
- 执行终端命令。
- 同步飞书文档到本地知识库。
- 任何未来会影响外部系统的 MCP 工具。

审批动作支持四类：

- `approve`：按原参数执行。
- `edit`：用户修改参数后执行。
- `reject`：拒绝本次工具调用，并把原因返回给模型继续思考。
- `respond`：跳过工具，把用户补充信息作为工具结果。

这部分应基于 LangGraph interrupt / LangChain Human-in-the-loop 的模式设计。没有 checkpointer 前，不要上线真正的暂停恢复；可以先做“前端确认弹窗 + 同请求内继续”的轻量版。

### 7.8 流式事件

当前 SSE 类型可以保留，但需要补齐结构化字段：

```ts
type AgentSSE =
  | { type: "thought"; content: string; metadata: { step: number; phase: string } }
  | { type: "tool_call"; content: string; metadata: ToolCallMeta }
  | { type: "tool_result"; content: string; metadata: ToolResultMeta }
  | { type: "approval_required"; content: string; metadata: ApprovalMeta }
  | { type: "artifact"; content: string; metadata: ArtifactMeta }
  | { type: "text"; content: string; metadata?: Record<string, unknown> }
  | { type: "done"; content: ""; metadata: { status: "success" | "cancelled" | "error" } }
  | { type: "error"; content: string; metadata?: Record<string, unknown> }
```

前端展示策略：

- 最终回答只显示 `text`。
- `thought/tool_call/tool_result/artifact` 放进“执行过程”折叠面板。
- `approval_required` 触发可操作 UI，不直接塞进聊天气泡。

LangGraph 最新 streaming 文档支持同时使用 `updates`、`messages`、`custom`、`checkpoints`、`tasks` 等模式。当前项目短期继续用 `updates`，但事件结构要按未来 v2 streaming 预留。

### 7.9 结构化最终输出

最终输出建议先在服务端内部结构化，再渲染成中文文本：

```python
class AgentFinalResponse(BaseModel):
    answer: str
    summary: str
    actions_taken: list[str]
    tools_used: list[str]
    artifacts: list[dict]
    needs_follow_up: bool
    follow_up_questions: list[str]
```

这可以减少前端解析自然语言的成本。最新 LangChain 提供 `ProviderStrategy` / `ToolStrategy` 结构化输出；当前依赖未必支持同样 API，第一版可以用 Pydantic + 二次校验实现。

### 7.10 记忆提交

记忆写入不要在每一步都做。建议：

1. 执行前读取 L0/L1/L2，用于上下文。
2. 执行中只把关键 artifact 和状态写入 thread state。
3. 执行结束后再做一次记忆提取：
   - 用户稳定偏好，例如“喜欢两天一夜轻装路线”。
   - 项目信息，例如“正在整理北京周边徒步资料”。
   - 可复用经验，例如“雨季路线规划必须提醒备用撤退点”。
4. 低置信度记忆不自动入库，先放 pending。

中期把当前 `MemoryManager` 对齐到 LangGraph store：thread 级短期记忆用 checkpointer，跨 thread 长期记忆用 store，向量检索用 semantic search。

## 8. LangChain/LangGraph 可用组件映射

| 文档组件 | 对当前项目的价值 | 建议 |
| --- | --- | --- |
| `create_agent` | 新版生产级 agent 封装，基于 LangGraph | 中期迁移目标；短期继续封装 `create_react_agent` |
| `ToolRuntime` | 工具读取 state/context/store，写 stream | 新工具按这个模式设计，当前版本需验证兼容 |
| `Command` | 工具更新 state 或结束/跳转 | 用于记忆写入、artifact 注册、成功后终止 |
| `SummarizationMiddleware` | 接近当前 L1 摘要需求 | 短期保留自研，升级后替换或对齐 |
| `HumanInTheLoopMiddleware` | 敏感工具审批 | 依赖 checkpointer；作为 Phase 4 |
| `ModelCallLimitMiddleware` | 防止 runaway agent | 先用自研计数器，升级后接 middleware |
| `ToolCallLimitMiddleware` | 限制搜索/终端/API 过度调用 | Phase 1 必做，可先自研 |
| `ModelFallbackMiddleware` | 模型故障兜底 | 当前已有多模型配置页，可接入 fallback |
| `ToolRetryMiddleware` / `ModelRetryMiddleware` | 网络和模型暂态失败重试 | Phase 2 必做 |
| `LLMToolSelectorMiddleware` | 工具多后减少上下文和误调用 | 工具超过 10 个后启用 |
| `TodoListMiddleware` | 复杂任务计划管理 | 可先用 `write_todos` 自研工具 |
| `ContextEditingMiddleware` | 清理旧工具输出，降低 token 成本 | Phase 2 做长结果 artifact 化 |
| `FilesystemFileSearchMiddleware` | glob/grep 工具 | 适合本项目 workspace 与代码搜索 |
| `ShellToolMiddleware` | 持久 shell session | 暂不直接接入；当前白名单终端更安全 |
| `PIIMiddleware` | API key、邮箱、手机号脱敏 | 日志和工具结果保护需要 |
| `MultiServerMCPClient` | 多 MCP server 工具加载 | 替换当前手写 MCP client 的长期方向 |
| MCP interceptors | 给 MCP 工具注入权限、用户、store | 接入图片搜索、外部服务时必须有 |
| Checkpointer | thread state、HITL、恢复、调试 | Phase 3 核心 |
| Store/PostgresStore | 跨会话长期记忆 | 替换或承接当前 `memory_store` |
| Streaming v2 | `updates/messages/custom/checkpoints/tasks` | 事件协议现在就按 v2 思路预留 |

## 9. 技术方案

### Phase 0：依赖与兼容性验证

目标：确认最新 LangChain 组件能否用于当前项目，避免直接升级炸裂。

任务：

- 建一个小型兼容实验，不改主链路。
- 对比当前 `langchain==0.3.0`、`langgraph==0.2.0` 与最新文档 API。
- 产出两条路径：
  - 路径 A：保守路线，继续当前版本，自研 middleware wrapper。
  - 路径 B：升级路线，迁移到 `langchain.agents.create_agent` 和新版 LangGraph。

验收：

- 有最小 ReAct 调用测试。
- 有流式事件测试。
- 有工具调用、工具失败、终止测试。

### Phase 1：工具注册表与风险治理

目标：让工具可描述、可过滤、可限流、可审计。

任务：

- 新增 `agent/tool_registry.py`。
- 把当前 `AVAILABLE_TOOLS` 改成由 registry 生成。
- 拆分 `file_operation` 为读、列、写、建目录，或至少在 registry 中区分 operation 风险。
- 修复 `resource_download` 的扩展名/MIME 校验。
- 为所有工具返回统一 envelope：

```python
class ToolResult(BaseModel):
    ok: bool
    summary: str
    data: dict | list | None = None
    artifact_id: str | None = None
    error: str | None = None
```

验收：

- 搜索类请求只暴露搜索/网页/RAG/终止工具。
- 文件产出请求才暴露写文件/PDF。
- 终端工具默认不出现在普通问答里。
- 单轮工具调用超限会返回可理解错误，而不是继续循环。

### Phase 2：ReAct 执行链路升级

目标：把“能跑”变成“过程可控”。

任务：

- 引入 `AgentRun`、`AgentStep`、`ToolCallRecord` 内部对象。
- 每个 SSE 事件都带 `run_id`、`step`、`tool_call_id`。
- 增加模型调用和工具调用预算。
- 网络工具增加重试；写操作不自动重试。
- 长工具结果自动 artifact 化，只把摘要留给模型。
- 流式输出拆成执行过程和最终回答两类。

验收：

- 单元测试覆盖：工具失败后模型能继续；工具超限后优雅结束；长网页结果不会塞满 prompt。
- 前端可以折叠查看执行过程。

### Phase 3：Memory 与 Persistence 收敛

目标：让短期对话、长期记忆、执行状态进入同一套 thread/store 设计。

任务：

- 以 `chat_id` 映射 `thread_id`。
- 引入开发环境 `InMemorySaver`，生产设计使用 Postgres checkpointer。
- 保留当前 `FileChatMemory` 作为兼容层，逐步迁移。
- 长期记忆继续用现有 `MemoryManager`，但新增 namespace：`(user_id, "memories")`、`(project_id, "lessons")`。
- 记忆写入增加置信度和去重。

验收：

- 同一个 chat_id 多轮对话能从 thread state 恢复。
- 服务重启后的恢复路径有测试或明确限制。
- 用户偏好能跨 session 被检索，但不会污染所有用户。

### Phase 4：审批与 Guardrails

目标：敏感动作必须过用户确认。

任务：

- 定义 `approval_required` SSE 事件。
- 前端增加 approve/edit/reject/respond 四类交互。
- 写文件、终端、下载、飞书同步默认审批。
- 增加 PII 脱敏：输入、日志、工具结果至少覆盖 API key、邮箱、手机号、URL token。
- 未接入持久 checkpointer 前，只支持同连接内审批；接入后支持暂停和恢复。

验收：

- “写入 workspace/test.md”会先弹审批。
- “运行 rm -rf”会被拒绝，不进入审批。
- 用户 reject 后，模型能解释并给替代方案。

### Phase 5：MCP 正式接入

目标：把 MCP 从实验 client 变成工具来源。

任务：

- 优先接入现有 `mcp-server/image_search`。
- 引入或适配 `langchain-mcp-adapters` 的 `MultiServerMCPClient`。
- MCP 工具进入 registry，带 server、transport、risk_level。
- MCP tool result 支持 structured content 和 multimodal content。
- 增加 MCP interceptor：鉴权、限流、日志、状态注入。

验收：

- “找一张雪山徒步图片”能触发 image_search MCP 工具。
- MCP 工具失败不会拖垮主 Agent。
- MCP 返回图片 URL 时，前端能以 artifact 展示。

### Phase 6：评估、观察与发布

目标：知道链路是否真的变好。

任务：

- 建 Agent 回归用例集：
  - 路线规划
  - 装备检查
  - 天气风险
  - RAG 问答
  - 文件导出
  - 终端拒绝
  - MCP 图片搜索
- 记录关键指标：
  - 首 token 时间
  - 总耗时
  - 模型调用次数
  - 工具调用次数
  - 工具失败率
  - 审批触发率
  - 用户取消率
- 后续可接 LangSmith tracing，但第一版先用本地结构化日志。

验收：

- 每次 Agent 改动有 focused tests。
- SSE 协议变更有前端测试。
- 一条完整任务能从请求到工具证据、artifact、最终回答、记忆写入闭环。

## 10. 验收标准

### 功能验收

- 用户问“帮我规划两天一夜徒步行程”，Agent 会先补关键约束或检索路线/天气，再给行程。
- 用户问知识库问题时，Agent 优先调用 `rag_search`，没有证据时不编造。
- 用户要求保存文件时，Agent 展示路径和摘要，用户批准后才写入。
- 用户要求执行危险命令时，Agent 拒绝并说明安全原因。
- 用户要求生成 PDF 时，Agent 生成 artifact，并在最终回答中给出文件名。
- MCP 图片搜索工具能被动态加载和调用。

### 工程验收

- Agent 工具注册表有测试。
- ReAct 流式事件有测试。
- 工具限流、重试、失败转换有测试。
- 审批流有 API 和前端测试。
- `MEMORY.md` 记录每次实现决策。

### 安全验收

- 文件路径不能逃出 workspace。
- 终端命令不能执行删除、提权、下载、改权限、杀进程。
- API key 等敏感内容不会进入前端事件和普通日志。
- 外部写操作默认需要审批。

## 11. 风险与对策

| 风险 | 影响 | 对策 |
| --- | --- | --- |
| 最新 LangChain 文档与当前依赖不兼容 | 直接升级会破坏现有链路 | Phase 0 先做兼容实验；短期自研 wrapper |
| 工具增多后模型误调用 | 体验下降、风险上升 | 动态工具选择 + 工具限流 + 风险等级 |
| HITL 需要持久化支持 | 审批后无法恢复 | 先做同请求审批，再接 checkpointer |
| 记忆误写入 | 用户偏好被污染 | 置信度、去重、pending 区、可视化删除 |
| 终端工具风险 | 文件损坏或泄露 | 白名单、沙箱、审批、日志脱敏 |
| 长工具结果塞满上下文 | 模型变慢、回答变差 | artifact 化 + Context Editing 思路 |

## 12. 推荐的下一步

第一步不要急着升级 LangChain。先做 Phase 1 和 Phase 2 的低风险部分：

1. 新建工具注册表，给现有 7 个工具补齐风险等级、预算和结果策略。
2. 修复 `resource_download` 扩展名校验。
3. 给 `aexecute_stream()` 的事件补 `run_id`、`step`、`tool_call_id`。
4. 前端把执行过程折叠展示，最终回答保持干净。
5. 加 focused tests，确保搜索、文件、PDF、终端请求都走统一 ReAct 链路。

这一步做完，Agent 的底座会更稳。之后再上 checkpointer、HITL、MCP 动态工具和长期 store，风险会小很多。

