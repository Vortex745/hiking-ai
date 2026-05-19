# LangChain 组件学习指南

> 数据来源：通过 Firecrawl CLI 抓取 [https://docs.langchain.com/](https://docs.langchain.com/) 官方文档整理而成  
> 覆盖范围：LangChain Python 开源框架核心组件

---

## 一、先搞清楚 LangChain 到底是什么

很多人一开始看到 LangChain、LangGraph、LangSmith 这一堆名字，容易搞混。其实可以把它们理解成一个产品家族：

| 产品 | 定位 | 适合什么场景 |
|------|------|-------------|
| **LangChain** | 开源框架，提供预置 Agent 架构 + 丰富集成 | 快速搭建 Agent，10 行代码就能跑起来 |
| **LangGraph** | 低层编排框架，控制每一步执行流程 | 需要精确控制 Agent 的每个节点和边 |
| **Deep Agents** | "开箱即用"的完整 Agent，内置上下文压缩、虚拟文件系统等 | 直接用，不想自己搭建 |
| **LangSmith** | 可观测性 + 评估 + 部署平台 | 追踪、调试、评估各种框架构建的 Agent |

简单说：**LangChain 是搭积木的零件库，LangGraph 是精确控制积木拼法的工具，LangSmith 是观察这堆积木运转情况的望远镜。**

---

## 二、组件全局地图

LangChain 的核心组件可以用下面这个流程来理解，每一层都建立在上一层之上：

```
┌─────────────────────────────────────────────────────┐
│  🎯 编排层：Agent + Memory（协调一切）              │
├─────────────────────────────────────────────────────┤
│  🤖 生成层：Chat Models + Tools（推理 + 行动）       │
├─────────────────────────────────────────────────────┤
│  🔍 检索层：Retrievers + Vector Stores（找信息）     │
├─────────────────────────────────────────────────────┤
│  🔢 向量层：Embedding Models（文本变数字）           │
├─────────────────────────────────────────────────────┤
│  📥 输入层：Document Loaders + Text Splitters        │
└─────────────────────────────────────────────────────┘
```

**数据流向**：原始数据 → 切分 → 向量化 → 存入向量库 → 用户提问 → 向量检索 → 喂给模型 → 生成回答

七大组件分类速查：

| 组件类别 | 核心作用 | 典型用途 |
|----------|----------|----------|
| **Models（模型）** | AI 推理和生成的大脑 | 文本生成、推理、语义理解 |
| **Messages（消息）** | 模型的基本输入输出单元 | 多轮对话、多模态内容 |
| **Tools（工具）** | 给 Agent 赋予外部能力 | 联网搜索、调数据库、执行代码 |
| **Agents（智能体）** | 模型 + 工具的协调者 | 非确定性工作流、自主决策 |
| **Memory（记忆）** | 保存对话上下文 | 有状态的多轮对话 |
| **Retrieval（检索）** | 注入外部知识 | RAG 问答、知识库搜索 |
| **Document Processing** | 原始数据摄取 | PDF 解析、网页抓取 |

---

## 三、Models — 推理引擎

### 是什么

模型是 Agent 的"大脑"，负责理解输入、决策、生成回复。除了文本，现代模型还支持：

- **工具调用**：调用外部工具并利用结果
- **结构化输出**：按指定格式输出
- **多模态**：处理图片、音频、视频
- **推理模式**：多步骤链式思考

### 怎么初始化

最简单的方式是用 `init_chat_model`，LangChain 会自动识别 provider：

```python
from langchain.chat_models import init_chat_model

# 用模型 ID 字符串（自动推断 provider）
model = init_chat_model("gpt-5.4")           # OpenAI
model = init_chat_model("claude-sonnet-4-6")  # Anthropic
model = init_chat_model("google_genai:gemini-2.5-flash-lite")  # Google

# 或用类直接实例化，方便配置更多参数
from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-5.4", temperature=0.1, max_tokens=1000, timeout=30)
```

### 三种调用方式

```python
# 1. invoke：等待完整回复（最常用）
response = model.invoke("为什么鹦鹉能说话？")

# 2. stream：流式输出，边生成边显示
for chunk in model.stream("解释一下量子计算"):
    print(chunk.text, end="", flush=True)

# 3. batch：批量处理，并行提速
responses = model.batch([
    "为什么天空是蓝的？",
    "飞机怎么飞起来的？",
    "量子计算是什么？"
])
```

### 工具调用（Tool Calling）

模型本身不执行工具，它只是"决定调用哪个工具、传什么参数"。实际执行由外部代码或 Agent 框架处理：

```python
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """获取某地的天气信息"""
    return f"{location}：晴天，25°C"

# 把工具绑定到模型
model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("北京今天天气怎么样？")

# 模型会返回工具调用请求（而不是直接调用）
for tool_call in response.tool_calls:
    print(tool_call['name'])   # get_weather
    print(tool_call['args'])   # {'location': '北京'}
```

### 结构化输出

让模型按指定 schema 返回数据，告别手动解析：

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str = Field(description="电影标题")
    year: int = Field(description="上映年份")
    rating: float = Field(description="评分，满分10分")

model_with_structure = model.with_structured_output(Movie)
result = model_with_structure.invoke("介绍一下《盗梦空间》这部电影")
# Movie(title='盗梦空间', year=2010, rating=8.8)
```

### 关键参数速查

| 参数 | 含义 | 推荐值 |
|------|------|--------|
| `temperature` | 输出随机性，越高越有创意 | 生产场景 0.1，创意场景 0.7 |
| `max_tokens` | 最大输出长度 | 按需设置 |
| `timeout` | 超时时间（秒） | 30~120 |
| `max_retries` | 网络失败重试次数 | 默认 6，不稳定网络可设 10~15 |

---

## 四、Messages — 对话的基本单元

### 消息是什么

消息是模型交互的基础数据结构，包含三个核心属性：

- **Role（角色）**：说话的是谁（system/user/assistant/tool）
- **Content（内容）**：说了什么（文本、图片、音频……）
- **Metadata（元数据）**：token 用量、消息 ID 等

### 四种消息类型

**SystemMessage**：给模型立规矩，定角色

```python
from langchain.messages import SystemMessage
system = SystemMessage("你是一位专业的 Python 开发工程师，回答要简洁、有代码示例。")
```

**HumanMessage**：用户说的话

```python
from langchain.messages import HumanMessage
human = HumanMessage("怎么用 Python 创建一个 REST API？")

# 也支持多模态：图片、PDF、音频
human_with_image = HumanMessage(content=[
    {"type": "text", "text": "这张图片里有什么？"},
    {"type": "image", "url": "https://example.com/photo.jpg"}
])
```

**AIMessage**：模型的回复

```python
from langchain.messages import AIMessage
response = model.invoke(messages)  # 返回 AIMessage
print(response.content)            # 文本内容
print(response.tool_calls)         # 工具调用（如果有）
print(response.usage_metadata)     # token 用量
```

**ToolMessage**：工具执行结果，回传给模型

```python
from langchain.messages import ToolMessage
tool_result = ToolMessage(
    content="北京天气：晴天，25°C",
    tool_call_id="call_abc123"  # 必须对应 AIMessage 里的工具调用 ID
)
```

### 多轮对话怎么写

LangChain 的交互是**无状态**的，每次调用都需要传入完整对话历史：

```python
messages = [
    SystemMessage("你是一个翻译助手，把英文翻译成中文"),
    HumanMessage("Translate: I love programming."),
    AIMessage("我热爱编程。"),
    HumanMessage("Translate: The sky is blue.")   # 继续对话
]
response = model.invoke(messages)
```

---

## 五、Tools — 给 Agent 安上手脚

### 工具是什么

工具是 Agent 能调用的函数。Agent 本质上是"推理 + 行动"的循环，而工具就是"行动"部分——联网、查数据库、执行代码、调 API，都靠工具来实现。

### 创建工具

最简单的方式是用 `@tool` 装饰器：

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """在客户数据库中搜索匹配记录。
    
    Args:
        query: 搜索关键词
        limit: 最多返回多少条结果
    """
    return f"找到 {limit} 条关于 '{query}' 的记录"
```

几个要注意的地方：
- **类型注解是必须的**，它定义了工具的输入 schema，模型靠这个理解怎么调用
- **docstring 要清晰**，模型根据它决定什么时候用这个工具
- **工具名用 snake_case**，避免含空格和特殊字符（部分 provider 会报错）

### 工具访问运行时信息

工具可以通过 `ToolRuntime` 访问对话状态、用户上下文、持久化存储：

```python
from langchain.tools import tool, ToolRuntime

# 访问对话历史（短期记忆）
@tool
def get_message_count(runtime: ToolRuntime) -> str:
    """获取当前对话中的消息数量。"""
    messages = runtime.state["messages"]
    return f"当前共有 {len(messages)} 条消息"

# 访问用户上下文（不可变配置）
from dataclasses import dataclass

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """获取当前用户的账户信息。"""
    user_id = runtime.context.user_id
    return f"用户 {user_id} 的账户信息"

# 访问持久化存储（长期记忆，跨会话存续）
@tool
def save_preference(key: str, value: str, runtime: ToolRuntime) -> str:
    """保存用户偏好设置。"""
    runtime.store.put(("preferences",), key, {"value": value})
    return f"已保存：{key} = {value}"
```

> `runtime` 参数对模型**不可见**，不会出现在工具 schema 里，只供工具内部使用。

### 三种返回值

| 返回类型 | 适用场景 | 效果 |
|----------|----------|------|
| `str` | 纯文本结果 | 转为 ToolMessage，模型直接读取 |
| `dict/object` | 结构化数据 | 序列化后供模型解析 |
| `Command` | 需要更新 Agent 状态 | 修改状态字段，并可附带 ToolMessage |

---

## 六、Agents — 自主决策的核心

### Agent 是什么

Agent 是 LangChain 里最核心的概念。它把**模型的推理能力**和**工具的执行能力**结合起来，让 AI 能够：

- 根据任务**自主决定**调用哪些工具
- 处理工具结果，进行**多步推理**
- 直到满足终止条件才停止

### 快速创建一个 Agent

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """获取某城市的天气"""
    return f"{city}：晴天，25°C"

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    system_prompt="你是一个有帮助的助手"
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "北京今天天气怎么样？"}]
})
print(result["messages"][-1].content)
```

### ReAct 循环：Agent 的运转方式

Agent 遵循 **ReAct（推理 + 行动）**模式：

```
用户提问
   ↓
[推理] 我需要查天气，用 get_weather 工具
   ↓
[行动] 调用 get_weather("北京")
   ↓
[观察] 工具返回："北京：晴天，25°C"
   ↓
[推理] 我已经有答案了，可以回复用户
   ↓
最终回复
```

这个循环会持续，直到模型觉得它已经能回答用户的问题了。

### Agent 的核心组件

**1. 模型（推理大脑）**

支持静态模型和动态模型切换：

```python
# 静态模型：始终用同一个
agent = create_agent("openai:gpt-5.4", tools=tools)

# 动态模型：根据情况切换（如根据对话长度选便宜/贵的模型）
from langchain.agents.middleware import wrap_model_call, ModelRequest

@wrap_model_call
def dynamic_model(request: ModelRequest, handler):
    if len(request.state["messages"]) > 10:
        return handler(request.override(model=advanced_model))
    return handler(request.override(model=basic_model))

agent = create_agent(model=basic_model, tools=tools, middleware=[dynamic_model])
```

**2. 系统提示（行为规范）**

```python
agent = create_agent(
    model,
    tools,
    system_prompt="你是一个专注于 Python 的技术助手，回答要包含代码示例，避免废话。"
)
```

**3. 结构化输出**

让 Agent 按指定格式返回结果：

```python
from pydantic import BaseModel
from langchain.agents.structured_output import ToolStrategy

class Report(BaseModel):
    summary: str
    key_points: list[str]
    confidence: float

agent = create_agent(
    model="gpt-5.4",
    tools=[search_tool],
    response_format=ToolStrategy(Report)
)
result = agent.invoke({"messages": [...]})
result["structured_response"]  # Report 对象
```

**4. 流式输出**

```python
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "搜索最新 AI 新闻并总结"}]},
    stream_mode="values"
):
    latest = chunk["messages"][-1]
    if latest.content:
        print(latest.content)
    elif latest.tool_calls:
        print(f"[调用工具: {[tc['name'] for tc in latest.tool_calls]}]")
```

### Middleware：Agent 的拦截器

Middleware 让你在不改变核心逻辑的情况下，给 Agent 加各种能力：

```python
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage

# 工具错误处理
@wrap_tool_call
def handle_errors(request, handler):
    try:
        return handler(request)
    except Exception as e:
        return ToolMessage(
            content=f"工具出错了，请检查输入后重试。（{str(e)}）",
            tool_call_id=request.tool_call["id"]
        )

agent = create_agent(model, tools, middleware=[handle_errors])
```

Middleware 能做的事：
- 在模型调用前修剪消息（防止超出上下文窗口）
- 动态切换模型
- 动态过滤工具（根据用户权限）
- 添加 guardrails（内容过滤）
- 自定义日志和监控

---

## 七、Retrieval — 让模型知道它不知道的事

### 为什么需要 RAG

大模型有两个硬伤：
1. **上下文有限**：不能把所有文档都塞进去
2. **知识固化**：训练数据有截止日期，不知道最新的事

RAG（检索增强生成）的思路很简单：**在生成前先检索相关内容，把检索结果一起喂给模型**。

### RAG 的完整流程

```
外部数据源（PDF、网页、数据库）
    ↓ Document Loaders（加载）
    ↓ Text Splitters（切块）
    ↓ Embedding Models（向量化）
    ↓ Vector Stores（存储）
          ↕
用户提问 → 向量化查询 → Retrievers（检索相关块）
                                ↓
                         Context + 问题 → LLM → 回答
```

每个组件都是**可替换的模块**，换个向量库或分词器不影响其他部分。

### 三种 RAG 架构

**1. 两步式 RAG（2-Step RAG）**

先检索，再生成。流程固定，延迟可预测，适合 FAQ 机器人、文档问答：

```
用户问题 → 检索相关文档 → 喂给 LLM → 返回答案
```

**2. Agentic RAG**

Agent 自己决定何时检索、检索什么。更灵活，适合研究助手、需要多次搜索的场景：

```python
import requests
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def fetch_url(url: str) -> str:
    """从 URL 获取文本内容"""
    response = requests.get(url, timeout=10.0)
    return response.text

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[fetch_url],   # 检索是一个工具！
    system_prompt="当你不确定答案时，用 fetch_url 工具查询相关文档。"
)
```

**3. 混合 RAG（Hybrid RAG）**

在两步式基础上加入验证和重试逻辑：

```
用户问题 → 查询增强 → 检索 → 质量验证
                            ↑ (不够好就重新检索)
                       生成回答 → 质量检查 → 返回最佳答案
```

适合需要高质量保证的场景，如医疗、法律问答。

### 比较三种架构

| 架构 | 延迟 | 灵活性 | 适用场景 |
|------|------|--------|----------|
| 两步式 RAG | ⚡ 快 | 低 | FAQ、简单文档问答 |
| Agentic RAG | ⏳ 不固定 | 高 | 研究助手、多步推理 |
| 混合 RAG | ⏳ 中等 | 中等 | 高质量要求的专业场景 |

---

## 八、Memory — 让 Agent 记住上下文

### 短期记忆 vs 长期记忆

| 类型 | 存储位置 | 生命周期 | 典型用途 |
|------|----------|----------|----------|
| **短期记忆（State）** | Agent 运行时状态 | 当前对话结束即消失 | 消息历史、对话进度 |
| **长期记忆（Store）** | 持久化数据库 | 跨会话持久存在 | 用户偏好、知识积累 |
| **上下文（Context）** | 调用时传入 | 单次调用内有效 | 用户 ID、权限信息 |

### 短期记忆：消息历史

Agent 默认把所有消息保存在 State 里，这就是短期记忆。你可以扩展 State 存更多信息：

```python
from langchain.agents import AgentState, create_agent
from typing import TypedDict

class MyState(AgentState):
    user_preferences: dict   # 扩展：保存用户偏好
    task_count: int          # 扩展：记录任务次数

agent = create_agent(model, tools, state_schema=MyState)

result = agent.invoke({
    "messages": [{"role": "user", "content": "帮我搜索 Python 教程"}],
    "user_preferences": {"language": "zh", "level": "beginner"},
    "task_count": 0
})
```

### 长期记忆：跨会话持久化

用 `BaseStore` 实现跨会话记忆，生产环境推荐用 `PostgresStore`：

```python
from langgraph.store.memory import InMemoryStore
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent

@tool
def remember_user_info(user_id: str, info: dict, runtime: ToolRuntime) -> str:
    """保存用户信息到长期记忆"""
    runtime.store.put(("users",), user_id, info)
    return "已记住用户信息"

@tool
def recall_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """从长期记忆中读取用户信息"""
    item = runtime.store.get(("users",), user_id)
    return str(item.value) if item else "没有找到该用户信息"

store = InMemoryStore()  # 生产环境换成 PostgresStore
agent = create_agent(model, tools=[remember_user_info, recall_user_info], store=store)

# 第一次对话：保存信息
agent.invoke({"messages": [{"role": "user", "content": "记住我：用户ID abc123，叫小明，25岁"}]})

# 第二次对话（新会话）：依然能想起来
agent.invoke({"messages": [{"role": "user", "content": "我叫什么名字？"}]})
```

### 处理长对话：避免超出上下文窗口

当对话很长时，需要主动管理消息，防止超出模型的上下文窗口。LangChain 提供了内置的中间件：

```python
# 消息裁剪：只保留最近 N 条消息
# 消息摘要：把早期对话压缩成摘要
# 这些通过 Middleware 实现，详见 middleware/built-in 文档
```

---

## 九、Multi-Agent — 让 Agent 们协作

### 为什么需要多 Agent

单个 Agent 有局限：上下文窗口有限、单一模型不擅长所有任务、并行处理效率低。多 Agent 架构把任务分发给专业的子 Agent：

```
复杂任务
    ↓
督导 Agent（Supervisor）
    ├── 研究 Agent（负责联网搜索）
    ├── 写作 Agent（负责生成内容）
    └── 审核 Agent（负责质量把关）
    ↓
汇总结果
```

### 三种多 Agent 模式

**1. Handoff（移交）**：一个 Agent 把任务移交给另一个

```python
# Agent A 决定把任务交给 Agent B
# 典型场景：客服路由，根据问题类型转交技术/账单/投诉专员
```

**2. Router（路由）**：根据规则把请求路由到不同 Agent

```python
# 像调度台：收到请求后判断该派哪个专员处理
# 典型场景：多知识库问答，根据问题领域选择对应知识库
```

**3. Subagents（子 Agent）**：主 Agent 动态创建并指挥子 Agent

```python
# 像团队 Leader：把任务拆解，分发给下属并收集结果
# 典型场景：深度研究，主 Agent 派多个子 Agent 分头调研不同方向
```

---

## 十、组件交互总结：一个完整的 RAG Agent

把前面所有组件整合起来，一个完整的 RAG Agent 是这样工作的：

```python
import requests
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.chat_models import init_chat_model
from langgraph.store.memory import InMemoryStore

# 工具：从 URL 检索文档（RAG 的检索部分）
@tool
def fetch_document(url: str) -> str:
    """从指定 URL 获取文档内容"""
    resp = requests.get(url, timeout=10)
    return resp.text[:3000]  # 限制长度

# 工具：读取用户偏好（长期记忆）
@tool
def get_user_preference(key: str, runtime: ToolRuntime) -> str:
    """读取用户存储的偏好信息"""
    item = runtime.store.get(("prefs",), key)
    return str(item.value) if item else "未设置"

# 初始化模型
model = init_chat_model("claude-sonnet-4-6", temperature=0.1)

# 持久化存储
store = InMemoryStore()

# 创建 Agent
agent = create_agent(
    model=model,
    tools=[fetch_document, get_user_preference],
    store=store,
    system_prompt="""
    你是一个智能研究助手。
    - 遇到需要最新信息的问题，用 fetch_document 工具查阅文档
    - 回答前先了解用户偏好（语言、详细程度）
    - 用清晰、简洁的方式组织答案
    """
)

# 调用
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "帮我了解一下 LangGraph 最新的功能"
    }]
})

print(result["messages"][-1].content)
```

---

## 十一、学习路径建议

根据官方文档和组件复杂度，推荐按以下顺序学习：

```
第一阶段：基础（1-2天）
  ✅ Messages 消息类型和格式
  ✅ Models 模型初始化和调用
  ✅ Tools 创建简单工具

第二阶段：核心（2-3天）
  ✅ Agents 创建和调用 Agent
  ✅ Streaming 流式输出
  ✅ Structured Output 结构化输出

第三阶段：进阶（3-5天）
  ✅ Memory 短期/长期记忆管理
  ✅ Retrieval RAG 架构
  ✅ Middleware Agent 中间件

第四阶段：生产（按需）
  ✅ Multi-Agent 多智能体协作
  ✅ LangGraph 精细编排
  ✅ LangSmith 可观测性
```

---

## 十二、常见集成一览

LangChain 支持大量第三方集成，以下是最常用的：

### Chat Models（对话模型）

| Provider | 代表模型 | 安装 |
|----------|----------|------|
| OpenAI | GPT-5.4, o1 | `pip install langchain[openai]` |
| Anthropic | Claude Sonnet/Haiku | `pip install langchain[anthropic]` |
| Google | Gemini 2.5 | `pip install langchain[google-genai]` |
| AWS Bedrock | Claude/Titan | `pip install langchain[aws]` |
| HuggingFace | Phi-3, Llama | `pip install langchain[huggingface]` |
| Ollama | 本地模型 | `pip install langchain-ollama` |

### Vector Stores（向量数据库）

| 产品 | 特点 |
|------|------|
| Chroma | 轻量，适合本地开发 |
| Pinecone | 托管云服务，生产可用 |
| FAISS | Facebook 出品，高性能 |
| Weaviate | 开源，支持混合搜索 |

### Document Loaders（文档加载器）

支持：PDF、Word、Excel、网页、Notion、Google Drive、Slack、GitHub 等几十种数据源。

---

## 参考资料

- LangChain 官方文档：https://docs.langchain.com/oss/python/langchain/overview.md
- 组件架构图：https://docs.langchain.com/oss/python/langchain/component-architecture.md
- 模型文档：https://docs.langchain.com/oss/python/langchain/models.md
- 消息文档：https://docs.langchain.com/oss/python/langchain/messages.md
- 工具文档：https://docs.langchain.com/oss/python/langchain/tools.md
- Agent 文档：https://docs.langchain.com/oss/python/langchain/agents.md
- 检索文档：https://docs.langchain.com/oss/python/langchain/retrieval.md
- LangGraph 概览：https://docs.langchain.com/oss/python/langgraph/overview.md

---

*本文档由 Firecrawl CLI 抓取 https://docs.langchain.com/ 官方内容，经整理和翻译生成，旨在帮助快速上手 LangChain 核心组件。*
