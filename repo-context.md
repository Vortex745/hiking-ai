This file is a merged representation of the entire codebase, combined into a single document by Repomix.
The content has been processed where comments have been removed, empty lines have been removed, content has been compressed (code blocks are separated by ⋮---- delimiter).

# File Summary

## Purpose
This file contains a packed representation of the entire repository's contents.
It is designed to be easily consumable by AI systems for analysis, code review,
or other automated processes.

## File Format
The content is organized as follows:
1. This summary section
2. Repository information
3. Directory structure
4. Repository files (if enabled)
5. Multiple file entries, each consisting of:
  a. A header with the file path (## File: path/to/file)
  b. The full contents of the file in a code block

## Usage Guidelines
- This file should be treated as read-only. Any changes should be made to the
  original repository files, not this packed version.
- When processing this file, use the file path to distinguish
  between different files in the repository.
- Be aware that this file may contain sensitive information. Handle it with
  the same level of security as you would the original repository.

## Notes
- Some files may have been excluded based on .gitignore rules and Repomix's configuration
- Binary files are not included in this packed representation. Please refer to the Repository Structure section for a complete list of file paths, including binary files
- Files matching patterns in .gitignore are excluded
- Files matching default ignore patterns are excluded
- Code comments have been removed from supported file types
- Empty lines have been removed from all files
- Content has been compressed - code blocks are separated by ⋮---- delimiter
- Long base64 data strings (e.g., data:image/png;base64,...) have been truncated to reduce token count
- Files are sorted by Git change count (files with more changes are at the bottom)

# Directory Structure
```
.firecrawl/docs.langchain.com-oss-python-langchain-agents.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-component-architecture.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-messages.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-models.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-overview.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-retrieval.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-short-term-memory.md.md
.firecrawl/docs.langchain.com-oss-python-langchain-tools.md.md
.gitignore
.omc/state/agent-replay-b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27.jsonl
.omc/state/agent-replay-dacf2d60-50e5-4603-9c6e-db62701af3ee.jsonl
.omc/state/hud-stdin-cache.json
.omc/state/last-tool-error.json
.omc/state/mission-state.json
.omc/state/sessions/02f4062a-21d8-44df-95cf-5ef3f0ec57bb/hud-state.json
.omc/state/sessions/02f4062a-21d8-44df-95cf-5ef3f0ec57bb/session-started.json
.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/session-started.json
.omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/hud-state.json
.omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/session-started.json
.omc/state/subagent-tracking.json
.omx/logs/omx-2026-05-16.jsonl
.omx/logs/omx-2026-05-17.jsonl
.omx/logs/omx-2026-05-18.jsonl
.omx/logs/omx-2026-05-19.jsonl
.omx/logs/tmux-hook-2026-05-16.jsonl
.omx/logs/tmux-hook-2026-05-17.jsonl
.omx/logs/tmux-hook-2026-05-18.jsonl
.omx/logs/tmux-hook-2026-05-19.jsonl
.omx/logs/turns-2026-05-16.jsonl
.omx/logs/turns-2026-05-17.jsonl
.omx/logs/turns-2026-05-18.jsonl
.omx/logs/turns-2026-05-19.jsonl
.omx/metrics.json
.omx/state/hud-state.json
.omx/state/notify-hook-state.json
.omx/state/session.json
.omx/state/sessions/019e30a2-25ee-7121-a02a-2e915835f249/prompt-routing-state.json
.omx/state/sessions/019e3104-76e4-7ac3-901b-8f37bd81ff00/prompt-routing-state.json
.omx/state/sessions/019e3637-0c5d-7492-8205-61c8653c23b8/prompt-routing-state.json
.omx/state/sessions/019e3637-5de3-7e10-99f9-54ce396e991f/skill-active-state.json
.omx/state/sessions/019e3701-953a-72d0-ac5f-91d4a33c67d6/hud-state.json
.omx/state/sessions/019e3701-953a-72d0-ac5f-91d4a33c67d6/notify-hook-state.json
.omx/state/sessions/019e395f-c99b-7563-9f9a-d5ef33cc59e5/skill-active-state.json
.omx/state/sessions/019e39e8-5f3d-71c1-a914-74ff757bd5ad/prompt-routing-state.json
.omx/state/sessions/019e3a16-5a64-7103-8b3c-e70142c689e6/skill-active-state.json
.omx/state/sessions/019e3c1e-8308-7720-8ca8-64d1acc7c24c/prompt-routing-state.json
.omx/state/sessions/019e3c3d-3186-78c3-adce-9a8ea1e12314/prompt-routing-state.json
.omx/state/sessions/019e3e06-b481-7b82-a53f-364e6e0c13c5/prompt-routing-state.json
.omx/state/sessions/019e3e09-6b8d-7983-a25f-31ce8f890ede/prompt-routing-state.json
.omx/state/sessions/019e3f21-cb5f-70a3-8638-e836d7e5e93e/prompt-routing-state.json
.omx/state/sessions/019e3f2b-015c-7d43-b8d2-2c30e360c39b/prompt-routing-state.json
.omx/state/skill-active-state.json
.omx/state/subagent-tracking.json
.omx/state/team-leader-nudge.json
.omx/state/tmux-hook-state.json
.repomixignore
.sisyphus/run-continuation/ses_1c4a6b54fffe1Eb5cRxJ3yYoki.json
.sisyphus/run-continuation/ses_1ce5e2737ffebAggBXgtATGn3a.json
.sisyphus/run-continuation/ses_1d2d113a8ffednNHMAhaQFHZsq.json
户外徒步知识文档.md
agent-layout-fixed.png
agent-memory-meter-check.png
agent-memory-meter-mobile-check.png
Agent-PRD.md
Agent三层记忆架构-实现文档.md
AI-Hiking-Agent改造计划书.md
ai-service/__init__.py
ai-service/.omc/project-memory.json
ai-service/.omc/state/agent-replay-b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27.jsonl
ai-service/.omc/state/hud-stdin-cache.json
ai-service/.omc/state/last-tool-error.json
ai-service/.omc/state/sessions/a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a/hud-state.json
ai-service/.omc/state/sessions/a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a/session-started.json
ai-service/.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
ai-service/.omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/hud-state.json
ai-service/户外徒步知识文档.md
ai-service/agent/__init__.py
ai-service/agent/advisors.py
ai-service/agent/agent.py
ai-service/agent/intake.py
ai-service/agent/prompts.py
ai-service/agent/task_exit.py
ai-service/api/__init__.py
ai-service/api/chat.py
ai-service/api/confirmation_store.py
ai-service/api/models_router.py
ai-service/api/models.py
ai-service/api/rag.py
ai-service/api/tools.py
ai-service/config.py
ai-service/main.py
ai-service/mcp/__init__.py
ai-service/mcp/client.py
ai-service/memory_data/chat-1778939095217.json
ai-service/memory_data/chat-1f98ad51-d9d9-4da6-acf7-ba9d020e970d.json
ai-service/memory_data/chat-361239fe-5541-4c84-9caf-2af16fcd06d8.json
ai-service/memory_data/chat-3da6ba32-288d-400e-b5ba-9b3cb01babb1.json
ai-service/memory_data/chat-6ffb0cff-c060-4357-9864-a7dad4d4f1d1.json
ai-service/memory_data/chat-a8e377aa-cbb5-493a-9452-5c9ad55a17a9.json
ai-service/memory_data/chat-dc3c1c3c-9197-4adb-bd24-ae3a3e4ef56a.json
ai-service/memory_data/chat-f5ff9a77-3929-4353-8e80-742e1c6946af.json
ai-service/memory_data/live-gateway-location-weather-check-dummy-2.json
ai-service/memory_data/live-gateway-location-weather-check-dummy-3.json
ai-service/memory_data/live-gateway-location-weather-check-dummy.json
ai-service/memory_data/live-location-weather-check-dummy-new.json
ai-service/memory_data/live-location-weather-check-dummy.json
ai-service/memory_data/live-location-weather-check.json
ai-service/memory_data/manual-missing-key-test.json
ai-service/memory_data/missing-key-sse.json
ai-service/memory_data/runtime-config-live-check.json
ai-service/memory_data/runtime-config-missing.json
ai-service/memory_data/runtime-config-present.json
ai-service/memory_data/runtime-llm-sse.json
ai-service/memory_data/test-1.json
ai-service/memory_data/test-2.json
ai-service/memory_data/test-chat-disabled.json
ai-service/memory_data/test-chat-error.json
ai-service/memory_data/test-chat-sse-123.json
ai-service/memory_data/test-chat-sync-123.json
ai-service/memory_data/verify-chat.json
ai-service/memory_store/knowledge.pkl
ai-service/memory/__init__.py
ai-service/memory/base.py
ai-service/memory/committer.py
ai-service/memory/compressor.py
ai-service/memory/file_memory.py
ai-service/memory/knowledge.py
ai-service/memory/memory_manager.py
ai-service/memory/redis_memory.py
ai-service/memory/vector_store.py
ai-service/rag_docs/户外徒步知识文档.md
ai-service/rag/__init__.py
ai-service/rag/augmenter.py
ai-service/rag/feishu.py
ai-service/rag/loader.py
ai-service/rag/reranker.py
ai-service/rag/retriever.py
ai-service/rag/rewriter.py
ai-service/rag/text_processing.py
ai-service/requirements.txt
ai-service/tests/__init__.py
ai-service/tests/conftest.py
ai-service/tests/test_advisors.py
ai-service/tests/test_agent_execution_flow.py
ai-service/tests/test_agent_intake.py
ai-service/tests/test_agent.py
ai-service/tests/test_chat_confirmation_fields.py
ai-service/tests/test_chat_health.py
ai-service/tests/test_chat_memory_integration.py
ai-service/tests/test_confirmation.py
ai-service/tests/test_embedding_config.py
ai-service/tests/test_feishu.py
ai-service/tests/test_file_memory.py
ai-service/tests/test_hiking_domain_tools.py
ai-service/tests/test_hiking_knowledge_tool.py
ai-service/tests/test_hiking_tool_selection.py
ai-service/tests/test_mcp_client.py
ai-service/tests/test_memory_committer.py
ai-service/tests/test_memory.py
ai-service/tests/test_models_router.py
ai-service/tests/test_rag_augmenter.py
ai-service/tests/test_rag_direct_answer.py
ai-service/tests/test_rag_loader_pipeline.py
ai-service/tests/test_rag_rerank.py
ai-service/tests/test_rag_retrieve_and_output.py
ai-service/tests/test_rag_retriever.py
ai-service/tests/test_rag_rewriter.py
ai-service/tests/test_reranker.py
ai-service/tests/test_retriever.py
ai-service/tests/test_tools_api.py
ai-service/tools/__init__.py
ai-service/tools/file_operation.py
ai-service/tools/hiking_domain.py
ai-service/tools/hiking_knowledge.py
ai-service/tools/pdf_generation.py
ai-service/tools/resource_download.py
ai-service/tools/risk_classifier.py
ai-service/tools/terminal.py
ai-service/tools/terminate.py
ai-service/tools/tool_registry.py
ai-service/tools/web_scraping.py
ai-service/tools/web_search.py
ai-service/workspace/Python知识点总复习.pdf
docker-compose.yml
frontend/index.html
frontend/llm-config-check.png
frontend/package.json
frontend/postcss.config.cjs
frontend/public/favicon.svg
frontend/src/api/config.ts
frontend/src/api/conversationMemory.ts
frontend/src/api/llmConfig.ts
frontend/src/api/ragStream.ts
frontend/src/api/sse.ts
frontend/src/App.css
frontend/src/App.tsx
frontend/src/components/AiAvatar.tsx
frontend/src/components/ChatRoom.tsx
frontend/src/components/ConnectionStatus.tsx
frontend/src/components/ConversationMemoryMeter.tsx
frontend/src/index.css
frontend/src/main.tsx
frontend/src/pages/Home.tsx
frontend/src/pages/LlmConfig.tsx
frontend/src/pages/LoveMaster.tsx
frontend/src/pages/SuperAgent.tsx
frontend/src/vite-env.d.ts
frontend/super-agent-check.png
frontend/tailwind.config.cjs
frontend/tests/appLayout.test.mjs
frontend/tests/conversationMemory.test.mjs
frontend/tests/llmConfig.test.mjs
frontend/tests/ragStream.test.mjs
frontend/tests/superAgent.test.mjs
frontend/tests/thinkingAnimation.test.mjs
frontend/tsconfig.json
frontend/tsconfig.node.json
frontend/vite.config.ts
gateway/.omc/state/hud-stdin-cache.json
gateway/.omc/state/last-tool-error.json
gateway/.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
gateway/config/config_test.go
gateway/config/config.go
gateway/go.mod
gateway/handler/chat_test.go
gateway/handler/chat.go
gateway/handler/health_test.go
gateway/handler/health.go
gateway/handler/models_test.go
gateway/handler/models.go
gateway/handler/rag_extended_test.go
gateway/handler/rag_test.go
gateway/handler/rag.go
gateway/main.go
gateway/middleware/cors_test.go
gateway/middleware/cors.go
gateway/middleware/ratelimit_test.go
gateway/middleware/ratelimit.go
homepage-icons.png
homepage.png
LangChain组件学习指南.md
love-master.png
mcp-server/image_search/requirements.txt
mcp-server/image_search/server.py
memory_data/missing-key-sse.json
memory_data/runtime-llm-sse.json
memory_data/test-chat-disabled.json
memory_data/test-chat-error.json
memory_data/test-chat-sse-123.json
memory_data/test-chat-sync-123.json
PRD.md
PROJECT_ANALYSIS.md
rag-memory-meter-check.png
rag-memory-meter-mobile-check.png
rag-output-details-check.png
rag-sidebar-collapsed.png
rag-sidebar-open.png
super-agent.png
```

# Files

## File: .firecrawl/docs.langchain.com-oss-python-langchain-agents.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Agents

Agents combine language models with \[tools\](/oss/python/langchain/tools) to create systems that can reason about tasks, decide which tools to use, and iteratively work towards solutions.

\[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent) provides a production-ready agent implementation.

\[An LLM Agent runs tools in a loop to achieve a goal\](https://simonwillison.net/2025/Sep/18/agents/).
An agent runs until a stop condition is met - i.e., when the model emits a final output or an iteration limit is reached.

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
%%{
 init: {
 "fontFamily": "monospace",
 "flowchart": {
 "curve": "curve"
 }
 }
}%%
graph TD
 %% Outside the agent
 QUERY(\[input\])
 LLM{model}
 TOOL(tools)
 ANSWER(\[output\])

 %% Main flows (no inline labels)
 QUERY --> LLM
 LLM --"action"--> TOOL
 TOOL --"observation"--> LLM
 LLM --"finish"--> ANSWER

 classDef blueHighlight fill:#E5F4FF,stroke:#006DDD,color:#030710;
 classDef greenHighlight fill:#F6FFDB,stroke:#6E8900,color:#2E3900;
 class QUERY blueHighlight;
 class ANSWER blueHighlight;
 class LLM greenHighlight;
 class TOOL greenHighlight;
\`\`\`

 \[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent) builds a \*\*graph\*\*-based agent runtime using \[LangGraph\](/oss/python/langgraph/overview). A graph consists of nodes (steps) and edges (connections) that define how your agent processes information. The agent moves through this graph, executing nodes like the model node (which calls the model), the tools node (which executes tools), or middleware.

 Learn more about the \[Graph API\](/oss/python/langgraph/graph-api).

 Trace each step of this loop, debug tool calls, and evaluate agent outputs with \[LangSmith\](https://smith.langchain.com?utm\_source=docs\\&utm\_medium=cta\\&utm\_campaign=langsmith-signup\\&utm\_content=oss-langchain-agents). Follow the \[tracing quickstart\](/langsmith/trace-with-langchain) to get set up.

\## Core components

\### Model

The \[model\](/oss/python/langchain/models) is the reasoning engine of your agent. It can be specified in multiple ways, supporting both static and dynamic model selection.

\#### Static model

Static models are configured once when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach.

To initialize a static model from a model identifier string:

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import create\_agent

agent = create\_agent("openai:gpt-5.4", tools=tools)
\`\`\`

 Model identifier strings support automatic inference (e.g., \`"gpt-5.4"\` will be inferred as \`"openai:gpt-5.4"\`). Refer to the \[reference\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model) to see a full list of model identifier string mappings.

For more control over the model configuration, initialize a model instance directly using the provider package. In this example, we use \[\`ChatOpenAI\`\](https://reference.langchain.com/python/langchain-openai/chat\_models/base/ChatOpenAI). See \[Chat models\](/oss/python/integrations/chat) for other available chat model classes.

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import create\_agent
from langchain\_openai import ChatOpenAI

model = ChatOpenAI(
 model="gpt-5.4",
 temperature=0.1,
 max\_tokens=1000,
 timeout=30
 # ... (other params)
)
agent = create\_agent(model, tools=tools)
\`\`\`

Model instances give you complete control over configuration. Use them when you need to set specific \[parameters\](/oss/python/langchain/models#parameters) like \`temperature\`, \`max\_tokens\`, \`timeouts\`, \`base\_url\`, and other provider-specific settings. Refer to the \[reference\](/oss/python/integrations/providers/all\_providers) to see available params and methods on your model.

\#### Dynamic model

Dynamic models are selected at runtime based on the current state and context. This enables sophisticated routing logic and cost optimization.

To use a dynamic model, create middleware using the \[\`@wrap\_model\_call\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/wrap\_model\_call) decorator that modifies the model in the request:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain\_openai import ChatOpenAI
from langchain.agents import create\_agent
from langchain.agents.middleware import wrap\_model\_call, ModelRequest, ModelResponse

basic\_model = ChatOpenAI(model="gpt-5.4-mini")
advanced\_model = ChatOpenAI(model="gpt-5.4")

@wrap\_model\_call
def dynamic\_model\_selection(request: ModelRequest, handler) -> ModelResponse:
 """Choose model based on conversation complexity."""
 message\_count = len(request.state\["messages"\])

 if message\_count > 10:
 # Use an advanced model for longer conversations
 model = advanced\_model
 else:
 model = basic\_model

 return handler(request.override(model=model))

agent = create\_agent(
 model=basic\_model, # Default model
 tools=tools,
 middleware=\[dynamic\_model\_selection\]
)
\`\`\`

 Pre-bound models (models with \[\`bind\_tools\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/bind\_tools) already called) are not supported when using structured output. If you need dynamic model selection with structured output, ensure the models passed to the middleware are not pre-bound.

 For model configuration details, see \[Models\](/oss/python/langchain/models). For dynamic model selection patterns, see \[Dynamic model in middleware\](/oss/python/langchain/middleware#dynamic-model).

\### Tools

Tools give agents the ability to take actions. Agents go beyond simple model-only tool binding by facilitating:

\\* Multiple tool calls in sequence (triggered by a single prompt)
\\* Parallel tool calls when appropriate
\\* Dynamic tool selection based on previous results
\\* Tool retry logic and error handling
\\* State persistence across tool calls

For more information, see \[Tools\](/oss/python/langchain/tools).

\#### Static tools

Static tools are defined when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach.

To define an agent with static tools, pass a list of the tools to the agent.

 Tools can be specified as plain Python functions or coroutines.

 The \[tool decorator\](/oss/python/langchain/tools#create-tools) can be used to customize tool names, descriptions, argument schemas, and other properties.

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool
from langchain.agents import create\_agent

@tool
def search(query: str) -> str:
 """Search for information."""
 return f"Results for: {query}"

@tool
def get\_weather(location: str) -> str:
 """Get weather information for a location."""
 return f"Weather in {location}: Sunny, 72°F"

agent = create\_agent(model, tools=\[search, get\_weather\])
\`\`\`

If an empty tool list is provided, the agent will consist of a single LLM node without tool-calling capabilities.

\#### Dynamic tools

With dynamic tools, the set of tools available to the agent is modified at runtime rather than defined all upfront. Not every tool is appropriate for every situation. Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities. Dynamic tool selection enables adapting the available toolset based on authentication state, user permissions, feature flags, or conversation stage.

There are two approaches depending on whether tools are known ahead of time:

 When all possible tools are known at agent creation time, you can pre-register them and dynamically filter which ones are exposed to the model based on state, permissions, or context.


 Enable advanced tools only after certain conversation milestones:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_model\_call, ModelRequest, ModelResponse
 from typing import Callable

 @wrap\_model\_call
 def state\_based\_tools(
 request: ModelRequest,
 handler: Callable\[\[ModelRequest\], ModelResponse\]
 ) -\> ModelResponse:
 """Filter tools based on conversation State."""
 # Read from State: check if user has authenticated
 state = request.state
 is\_authenticated = state.get("authenticated", False)
 message\_count = len(state\["messages"\])

 # Only enable sensitive tools after authentication
 if not is\_authenticated:
 tools = \[t for t in request.tools if t.name.startswith("public\_")\]
 request = request.override(tools=tools)
 elif message\_count < 5:
 # Limit tools early in conversation
 tools = \[t for t in request.tools if t.name != "advanced\_search"\]
 request = request.override(tools=tools)

 return handler(request)

 agent = create\_agent(
 model="gpt-5.4",
 tools=\[public\_search, private\_search, advanced\_search\],
 middleware=\[state\_based\_tools\]
 )
 \`\`\`

 Filter tools based on user preferences or feature flags in Store:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from dataclasses import dataclass
 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_model\_call, ModelRequest, ModelResponse
 from typing import Callable
 from langgraph.store.memory import InMemoryStore

 @dataclass
 class Context:
 user\_id: str

 @wrap\_model\_call
 def store\_based\_tools(
 request: ModelRequest,
 handler: Callable\[\[ModelRequest\], ModelResponse\]
 ) -\> ModelResponse:
 """Filter tools based on Store preferences."""
 user\_id = request.runtime.context.user\_id

 # Read from Store: get user's enabled features
 store = request.runtime.store
 feature\_flags = store.get(("features",), user\_id)

 if feature\_flags:
 enabled\_features = feature\_flags.value.get("enabled\_tools", \[\])
 # Only include tools that are enabled for this user
 tools = \[t for t in request.tools if t.name in enabled\_features\]
 request = request.override(tools=tools)

 return handler(request)

 agent = create\_agent(
 model="gpt-5.4",
 tools=\[search\_tool, analysis\_tool, export\_tool\],
 middleware=\[store\_based\_tools\],
 context\_schema=Context,
 store=InMemoryStore()
 )
 \`\`\`

 Filter tools based on user permissions from Runtime Context:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from dataclasses import dataclass
 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_model\_call, ModelRequest, ModelResponse
 from typing import Callable

 @dataclass
 class Context:
 user\_role: str

 @wrap\_model\_call
 def context\_based\_tools(
 request: ModelRequest,
 handler: Callable\[\[ModelRequest\], ModelResponse\]
 ) -\> ModelResponse:
 """Filter tools based on Runtime Context permissions."""
 # Read from Runtime Context: get user role
 if request.runtime is None or request.runtime.context is None:
 # If no context provided, default to viewer (most restrictive)
 user\_role = "viewer"
 else:
 user\_role = request.runtime.context.user\_role

 if user\_role == "admin":
 # Admins get all tools
 pass
 elif user\_role == "editor":
 # Editors can't delete
 tools = \[t for t in request.tools if t.name != "delete\_data"\]
 request = request.override(tools=tools)
 else:
 # Viewers get read-only tools
 tools = \[t for t in request.tools if t.name.startswith("read\_")\]
 request = request.override(tools=tools)

 return handler(request)

 agent = create\_agent(
 model="gpt-5.4",
 tools=\[read\_data, write\_data, delete\_data\],
 middleware=\[context\_based\_tools\],
 context\_schema=Context
 )
 \`\`\`


 This approach is best when:

 \\* All possible tools are known at compile/startup time
 \\* You want to filter based on permissions, feature flags, or conversation state
 \\* Tools are static but their availability is dynamic

 See \[Dynamically selecting tools\](/oss/python/langchain/middleware/custom#dynamically-selecting-tools) for more examples.

 When tools are discovered or created at runtime (e.g., loaded from an MCP server, generated based on user data, or fetched from a remote registry), you need to both register the tools and handle their execution dynamically.

 This requires two middleware hooks:

 1\. \`wrap\_model\_call\` - Add the dynamic tools to the request
 2\. \`wrap\_tool\_call\` - Handle execution of the dynamically added tools

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.tools import tool
 from langchain.agents import create\_agent
 from langchain.agents.middleware import AgentMiddleware, ModelRequest, ToolCallRequest

 # A tool that will be added dynamically at runtime
 @tool
 def calculate\_tip(bill\_amount: float, tip\_percentage: float = 20.0) -> str:
 """Calculate the tip amount for a bill."""
 tip = bill\_amount \* (tip\_percentage / 100)
 return f"Tip: ${tip:.2f}, Total: ${bill\_amount + tip:.2f}"

 class DynamicToolMiddleware(AgentMiddleware):
 """Middleware that registers and handles dynamic tools."""

 def wrap\_model\_call(self, request: ModelRequest, handler):
 # Add dynamic tool to the request
 # This could be loaded from an MCP server, database, etc.
 updated = request.override(tools=\[\*request.tools, calculate\_tip\])
 return handler(updated)

 def wrap\_tool\_call(self, request: ToolCallRequest, handler):
 # Handle execution of the dynamic tool
 if request.tool\_call\["name"\] == "calculate\_tip":
 return handler(request.override(tool=calculate\_tip))
 return handler(request)

 agent = create\_agent(
 model="gpt-4o",
 tools=\[get\_weather\], # Only static tools registered here
 middleware=\[DynamicToolMiddleware()\],
 )

 # The agent can now use both get\_weather AND calculate\_tip
 result = agent.invoke({
 "messages": \[{"role": "user", "content": "Calculate a 20% tip on $85"}\]
 })
 \`\`\`

 This approach is best when:

 \\* Tools are discovered at runtime (e.g., from an MCP server)
 \\* Tools are generated dynamically based on user data or configuration
 \\* You're integrating with external tool registries


 The \`wrap\_tool\_call\` hook is required for runtime-registered tools because the agent needs to know how to execute tools that weren't in the original tool list. Without it, the agent won't know how to invoke the dynamically added tool.

 To learn more about tools, see \[Tools\](/oss/python/langchain/tools).

\#### Tool error handling

To customize how tool errors are handled, use the \[\`@wrap\_tool\_call\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/wrap\_tool\_call) decorator to create middleware:

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import create\_agent
from langchain.agents.middleware import wrap\_tool\_call
from langchain.messages import ToolMessage

@wrap\_tool\_call
def handle\_tool\_errors(request, handler):
 """Handle tool execution errors with custom messages."""
 try:
 return handler(request)
 except Exception as e:
 # Return a custom error message to the model
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({str(e)})",
 tool\_call\_id=request.tool\_call\["id"\]
 )

agent = create\_agent(
 model="gpt-5.4",
 tools=\[search, get\_weather\],
 middleware=\[handle\_tool\_errors\]
)
\`\`\`

The agent will return a \[\`ToolMessage\`\](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) with the custom error message when a tool fails:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
\[\
 ...\
 ToolMessage(\
 content="Tool error: Please check your input and try again. (division by zero)",\
 tool\_call\_id="..."\
 ),\
 ...\
\]
\`\`\`

\#### Tool use in the ReAct loop

Agents follow the ReAct ("Reasoning + Acting") pattern, alternating between brief reasoning steps with targeted tool calls and feeding the resulting observations into subsequent decisions until they can deliver a final answer.

 \*\*Prompt:\*\* Identify the current most popular wireless headphones and verify availability.

 \`\`\`
 ================================ Human Message =================================

 Find the most popular wireless headphones right now and check if they're in stock
 \`\`\`

 \\* \*\*Reasoning\*\*: "Popularity is time-sensitive, I need to use the provided search tool."
 \\* \*\*Acting\*\*: Call \`search\_products("wireless headphones")\`

 \`\`\`
 ================================== Ai Message ==================================
 Tool Calls:
 search\_products (call\_abc123)
 Call ID: call\_abc123
 Args:
 query: wireless headphones
 \`\`\`

 \`\`\`
 ================================= Tool Message =================================

 Found 5 products matching "wireless headphones". Top 5 results: WH-1000XM5, ...
 \`\`\`

 \\* \*\*Reasoning\*\*: "I need to confirm availability for the top-ranked item before answering."
 \\* \*\*Acting\*\*: Call \`check\_inventory("WH-1000XM5")\`

 \`\`\`
 ================================== Ai Message ==================================
 Tool Calls:
 check\_inventory (call\_def456)
 Call ID: call\_def456
 Args:
 product\_id: WH-1000XM5
 \`\`\`

 \`\`\`
 ================================= Tool Message =================================

 Product WH-1000XM5: 10 units in stock
 \`\`\`

 \\* \*\*Reasoning\*\*: "I have the most popular model and its stock status. I can now answer the user's question."
 \\* \*\*Acting\*\*: Produce final answer

 \`\`\`
 ================================== Ai Message ==================================

 I found wireless headphones (model WH-1000XM5) with 10 units in stock...
 \`\`\`

\### System prompt

You can shape how your agent approaches tasks by providing a prompt. The \[\`system\_prompt\`\](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create\_agent\\(system\_prompt\\)) parameter can be provided as a string:

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create\_agent(
 model,
 tools,
 system\_prompt="You are a helpful assistant. Be concise and accurate."
)
\`\`\`

When no \[\`system\_prompt\`\](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create\_agent\\(system\_prompt\\)) is provided, the agent will infer its task from the messages directly.

The \[\`system\_prompt\`\](https://reference.langchain.com/python/langchain/agents/#langchain.agents.create\_agent\\(system\_prompt\\)) parameter accepts either a \`str\` or a \[\`SystemMessage\`\](https://reference.langchain.com/python/langchain-core/messages/system/SystemMessage). Using a \`SystemMessage\` gives you more control over the prompt structure, which is useful for provider-specific features like \[Anthropic's prompt caching\](/oss/python/integrations/chat/anthropic#prompt-caching):

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import create\_agent
from langchain.messages import SystemMessage, HumanMessage

literary\_agent = create\_agent(
 model="google\_genai:gemini-3.1-pro-preview",
 system\_prompt=SystemMessage(
 content=\[\
 {\
 "type": "text",\
 "text": "You are an AI assistant tasked with analyzing literary works.",\
 },\
 {\
 "type": "text",\
 "text": "",\
 "cache\_control": {"type": "ephemeral"}\
 }\
 \]
 )
)

result = literary\_agent.invoke(
 {"messages": \[HumanMessage("Analyze the major themes in 'Pride and Prejudice'.")\]}
)
\`\`\`

The \`cache\_control\` field with \`{"type": "ephemeral"}\` tells Anthropic to cache that content block, reducing latency and costs for repeated requests that use the same system prompt.

\#### Dynamic system prompt

For more advanced use cases where you need to modify the system prompt based on runtime context or agent state, you can use \[middleware\](/oss/python/langchain/middleware).

The \[\`@dynamic\_prompt\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/dynamic\_prompt) decorator creates middleware that generates system prompts based on the model request:

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from typing import TypedDict

from langchain.agents import create\_agent
from langchain.agents.middleware import dynamic\_prompt, ModelRequest

class Context(TypedDict):
 user\_role: str

@dynamic\_prompt
def user\_role\_prompt(request: ModelRequest) -> str:
 """Generate system prompt based on user role."""
 user\_role = request.runtime.context.get("user\_role", "user")
 base\_prompt = "You are a helpful assistant."

 if user\_role == "expert":
 return f"{base\_prompt} Provide detailed technical responses."
 elif user\_role == "beginner":
 return f"{base\_prompt} Explain concepts simply and avoid jargon."

 return base\_prompt

agent = create\_agent(
 model="gpt-5.4",
 tools=\[web\_search\],
 middleware=\[user\_role\_prompt\],
 context\_schema=Context
)

\# The system prompt will be set dynamically based on context
result = agent.invoke(
 {"messages": \[{"role": "user", "content": "Explain machine learning"}\]},
 context={"user\_role": "expert"}
)
\`\`\`

 For more details on message types and formatting, see \[Messages\](/oss/python/langchain/messages). For comprehensive middleware documentation, see \[Middleware\](/oss/python/langchain/middleware).

\### Name

Set an optional \[\`name\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent) for the agent. This is used as the node identifier when adding the agent as a subgraph in \[multi-agent systems\](/oss/python/langchain/multi-agent):

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
agent = create\_agent(
 model,
 tools,
 name="research\_assistant"
)
\`\`\`

 Prefer \`snake\_case\` for agent names (e.g., \`research\_assistant\` instead of \`Research Assistant\`). Some model providers reject names containing spaces or special characters with errors. Using alphanumeric characters, underscores, and hyphens only ensures compatibility across all providers. The same applies to \[tool names\](/oss/python/langchain/tools).

\## Invocation

You can invoke an agent by passing an update to its \[\`State\`\](/oss/python/langgraph/graph-api#state). All agents include a \[sequence of messages\](/oss/python/langgraph/use-graph-api#messagesstate) in their state; to invoke the agent, pass a new message:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
)
\`\`\`

For streaming steps and / or tokens from the agent, refer to the \[streaming\](/oss/python/langchain/streaming) guide.

Otherwise, the agent follows the LangGraph \[Graph API\](/oss/python/langgraph/use-graph-api) and supports all associated methods, such as \`stream\` and \`invoke\`.

\## Advanced concepts

\### Structured output

In some situations, you may want the agent to return an output in a specific format. LangChain provides strategies for structured output via the \[\`response\_format\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent) parameter.

\#### ToolStrategy

\`ToolStrategy\` uses artificial tool calling to generate structured output. This works with any model that supports tool calling. \`ToolStrategy\` should be used when provider-native structured output (via \[\`ProviderStrategy\`\](#providerstrategy)) is not available or reliable.

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from pydantic import BaseModel
from langchain.agents import create\_agent
from langchain.agents.structured\_output import ToolStrategy

class ContactInfo(BaseModel):
 name: str
 email: str
 phone: str

agent = create\_agent(
 model="gpt-5.4-mini",
 tools=\[search\_tool\],
 response\_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
 "messages": \[{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}\]
})

result\["structured\_response"\]
\# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
\`\`\`

\#### ProviderStrategy

\`ProviderStrategy\` uses the model provider's native structured output generation. This is more reliable but only works with providers that support native structured output:

\`\`\`python wrap theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents.structured\_output import ProviderStrategy

agent = create\_agent(
 model="gpt-5.4",
 response\_format=ProviderStrategy(ContactInfo)
)
\`\`\`

 As of \`langchain 1.0\`, simply passing a schema (e.g., \`response\_format=ContactInfo\`) will default to \`ProviderStrategy\` if the model supports native structured output. It will fall back to \`ToolStrategy\` otherwise.

 To learn about structured output, see \[Structured output\](/oss/python/langchain/structured-output).

\### Memory

Agents maintain conversation history automatically through the message state. You can also configure the agent to use a custom state schema to remember additional information during the conversation.

Information stored in the state can be thought of as the \[short-term memory\](/oss/python/langchain/short-term-memory) of the agent:

Custom state schemas must extend \[\`AgentState\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/AgentState) as a \`TypedDict\`.

There are two ways to define custom state:

1\. Via \[middleware\](/oss/python/langchain/middleware) (preferred)
2\. Via \[\`state\_schema\`\](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state\_schema) on \[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent)

\#### Defining state via middleware

Use middleware to define custom state when your custom state needs to be accessed by specific middleware hooks and tools attached to said middleware.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from typing import Any

class CustomState(AgentState):
 user\_preferences: dict

class CustomMiddleware(AgentMiddleware):
 state\_schema = CustomState
 tools = \[tool1, tool2\]

 def before\_model(self, state: CustomState, runtime) -> dict\[str, Any\] \| None:
 ...

agent = create\_agent(
 model,
 tools=tools,
 middleware=\[CustomMiddleware()\]
)

\# The agent can now track additional state beyond messages
result = agent.invoke({
 "messages": \[{"role": "user", "content": "I prefer technical explanations"}\],
 "user\_preferences": {"style": "technical", "verbosity": "detailed"},
})
\`\`\`

\#### Defining state via \`state\_schema\`

Use the \[\`state\_schema\`\](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state\_schema) parameter as a shortcut to define custom state that is only used in tools.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import AgentState

class CustomState(AgentState):
 user\_preferences: dict

agent = create\_agent(
 model,
 tools=\[tool1, tool2\],
 state\_schema=CustomState
)
\# The agent can now track additional state beyond messages
result = agent.invoke({
 "messages": \[{"role": "user", "content": "I prefer technical explanations"}\],
 "user\_preferences": {"style": "technical", "verbosity": "detailed"},
})
\`\`\`

 As of \`langchain 1.0\`, custom state schemas \*\*must\*\* be \`TypedDict\` types. Pydantic models and dataclasses are no longer supported. See the \[v1 migration guide\](/oss/python/migrate/langchain-v1#state-type-restrictions) for more details.

 Defining custom state via middleware is preferred over defining it via \[\`state\_schema\`\](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state\_schema) on \[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent) because it allows you to keep state extensions conceptually scoped to the relevant middleware and tools.

 \[\`state\_schema\`\](https://reference.langchain.com/python/langchain/middleware/#langchain.agents.middleware.AgentMiddleware.state\_schema) is still supported for backwards compatibility on \[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent).

 To learn more about memory, see \[Memory\](/oss/python/concepts/memory). For information on implementing long-term memory that persists across sessions, see \[Long-term memory\](/oss/python/langchain/long-term-memory).

\### Streaming

We've seen how the agent can be called with \`invoke\` to get a final response. If the agent executes multiple steps, this may take a while. To show intermediate progress, we can stream back messages as they occur.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import AIMessage, HumanMessage

for chunk in agent.stream({
 "messages": \[{"role": "user", "content": "Search for AI news and summarize the findings"}\]
}, stream\_mode="values"):
 # Each chunk contains the full state at that point
 latest\_message = chunk\["messages"\]\[-1\]
 if latest\_message.content:
 if isinstance(latest\_message, HumanMessage):
 print(f"User: {latest\_message.content}")
 elif isinstance(latest\_message, AIMessage):
 print(f"Agent: {latest\_message.content}")
 elif latest\_message.tool\_calls:
 print(f"Calling tools: {\[tc\['name'\] for tc in latest\_message.tool\_calls\]}")
\`\`\`

 For more details on streaming, see \[Streaming\](/oss/python/langchain/streaming).

\### Middleware

\[Middleware\](/oss/python/langchain/middleware) provides powerful extensibility for customizing agent behavior at different stages of execution. You can use middleware to:

\\* Process state before the model is called (e.g., message trimming, context injection)
\\* Modify or validate the model's response (e.g., guardrails, content filtering)
\\* Handle tool execution errors with custom logic
\\* Implement dynamic model selection based on state or context
\\* Add custom logging, monitoring, or analytics

Middleware integrates seamlessly into the agent's execution, allowing you to intercept and modify data flow at key points without changing the core agent logic.

 For comprehensive middleware documentation including decorators like \[\`@before\_model\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/before\_model), \[\`@after\_model\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/after\_model), and \[\`@wrap\_tool\_call\`\](https://reference.langchain.com/python/langchain/agents/middleware/types/wrap\_tool\_call), see \[Middleware\](/oss/python/langchain/middleware).

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/agents.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-component-architecture.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Component architecture

LangChain's power comes from how its components work together to create sophisticated AI applications. This page provides diagrams showcasing the relationships between different components.

\## Core component ecosystem

The diagram below shows how LangChain's major components connect to form complete AI applications:

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph TD
 %% Input processing
 subgraph "📥 Input processing"
 A\[Text input\] --> B\[Document loaders\]
 B --> C\[Text splitters\]
 C --> D\[Documents\]
 end

 %% Embedding & storage
 subgraph "🔢 Embedding & storage"
 D --> E\[Embedding models\]
 E --> F\[Vectors\]
 F --> G\[(Vector stores)\]
 end

 %% Retrieval
 subgraph "🔍 Retrieval"
 H\[User Query\] --> I\[Embedding models\]
 I --> J\[Query vector\]
 J --> K\[Retrievers\]
 K --> G
 G --> L\[Relevant context\]
 end

 %% Generation
 subgraph "🤖 Generation"
 M\[Chat models\] --> N\[Tools\]
 N --> O\[Tool results\]
 O --> M
 L --> M
 M --> P\[AI response\]
 end

 %% Orchestration
 subgraph "🎯 Orchestration"
 Q\[Agents\] --> M
 Q --> N
 Q --> K
 Q --> R\[Memory\]
 end

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class A,H trigger
 class B,C,E,I,K,M,N,Q process
 class D,F,J,L,O,P,R neutral
 class G output
\`\`\`

\### How components connect

Each component layer builds on the previous ones:

1\. \*\*Input processing\*\* – Transform raw data into structured documents
2\. \*\*Embedding & storage\*\* – Convert text into searchable vector representations
3\. \*\*Retrieval\*\* – Find relevant information based on user queries
4\. \*\*Generation\*\* – Use AI models to create responses, optionally with tools
5\. \*\*Orchestration\*\* – Coordinate everything through agents and memory systems

\## Component categories

LangChain organizes components into these main categories:

\| Category \| Purpose \| Key Components \| Use Cases \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \*\*\[Models\](/oss/python/langchain/models)\*\* \| AI reasoning and generation \| Chat models, LLMs, Embedding models \| Text generation, reasoning, semantic understanding \|
\| \*\*\[Tools\](/oss/python/langchain/tools)\*\* \| External capabilities \| APIs, databases, etc. \| Web search, data access, computations \|
\| \*\*\[Agents\](/oss/python/langchain/agents)\*\* \| Orchestration and reasoning \| ReAct agents, tool calling agents \| Nondeterministic workflows, decision making \|
\| \*\*\[Memory\](/oss/python/langchain/short-term-memory)\*\* \| Context preservation \| Message history, custom state \| Conversations, stateful interactions \|
\| \*\*\[Retrievers\](/oss/python/integrations/retrievers)\*\* \| Information access \| Vector retrievers, web retrievers \| RAG, knowledge base search \|
\| \*\*\[Document processing\](/oss/python/integrations/document\_loaders)\*\* \| Data ingestion \| Loaders, splitters, transformers \| PDF processing, web scraping \|
\| \*\*\[Vector Stores\](/oss/python/integrations/vectorstores)\*\* \| Semantic search \| Chroma, Pinecone, FAISS \| Similarity search, embeddings storage \|

\## Common patterns

\### RAG (Retrieval-Augmented generation)

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[User question\] --> B\[Retriever\]
 B --> C\[Relevant docs\]
 C --> D\[Chat model\]
 A --> D
 D --> E\[Informed response\]

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class A trigger
 class B,D process
 class C,E neutral
\`\`\`

\### Agent with tools

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[User request\] --> B\[Agent\]
 B --> C{Need tool?}
 C -->\|Yes\| D\[Call tool\]
 D --> E\[Tool result\]
 E --> B
 C -->\|No\| F\[Final answer\]

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class A trigger
 class B,D process
 class C decision
 class E,F neutral
\`\`\`

\### Multi-agent system

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[Complex Task\] --> B\[Supervisor agent\]
 B --> C\[Specialist agent 1\]
 B --> D\[Specialist agent 2\]
 C --> E\[Results\]
 D --> E
 E --> B
 B --> F\[Coordinated response\]

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class A trigger
 class B,C,D process
 class E,F neutral
\`\`\`

\## Learn more

\\* \[Creating agents\](/oss/python/langchain/agents)
\\* \[Working with tools\](/oss/python/langchain/tools)
\\* \[Browse integrations\](/oss/python/integrations/providers/overview)

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/component-architecture.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-messages.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Messages

Messages are the fundamental unit of context for models in LangChain. They represent the input and output of models, carrying both the content and metadata needed to represent the state of a conversation when interacting with an LLM.

Messages are objects that contain:

\\*  \[\*\*Role\*\*\](#message-types) - Identifies the message type (e.g. \`system\`, \`user\`)
\\*  \[\*\*Content\*\*\](#message-content) - Represents the actual content of the message (like text, images, audio, documents, etc.)
\\*  \[\*\*Metadata\*\*\](#message-metadata) - Optional fields such as response information, message IDs, and token usage

LangChain provides a standard message type that works across all model providers, ensuring consistent behavior regardless of the model being called.

\## Basic usage

The simplest way to use messages is to create message objects and pass them to a model when \[invoking\](/oss/python/langchain/models#invocation).

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init\_chat\_model("gpt-5-nano")

system\_msg = SystemMessage("You are a helpful assistant.")
human\_msg = HumanMessage("Hello, how are you?")

\# Use with chat models
messages = \[system\_msg, human\_msg\]
response = model.invoke(messages) # Returns AIMessage
\`\`\`

\### Text prompts

Text prompts are strings - ideal for straightforward generation tasks where you don't need to retain conversation history.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke("Write a haiku about spring")
\`\`\`

\*\*Use text prompts when:\*\*

\\* You have a single, standalone request
\\* You don't need conversation history
\\* You want minimal code complexity

\### Message prompts

Alternatively, you can pass in a list of messages to the model by providing a list of message objects.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import SystemMessage, HumanMessage, AIMessage

messages = \[\
 SystemMessage("You are a poetry expert"),\
 HumanMessage("Write a haiku about spring"),\
 AIMessage("Cherry blossoms bloom...")\
\]
response = model.invoke(messages)
\`\`\`

\*\*Use message prompts when:\*\*

\\* Managing multi-turn conversations
\\* Working with multimodal content (images, audio, files)
\\* Including system instructions

\### Dictionary format

You can also specify messages directly in OpenAI chat completions format.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
messages = \[\
 {"role": "system", "content": "You are a poetry expert"},\
 {"role": "user", "content": "Write a haiku about spring"},\
 {"role": "assistant", "content": "Cherry blossoms bloom..."}\
\]
response = model.invoke(messages)
\`\`\`

\## Message types

\\*  \[System message\](#system-message) - Tells the model how to behave and provide context for interactions
\\*  \[Human message\](#human-message) - Represents user input and interactions with the model
\\*  \[AI message\](#ai-message) - Responses generated by the model, including text content, tool calls, and metadata
\\*  \[Tool message\](#tool-message) - Represents the outputs of \[tool calls\](/oss/python/langchain/models#tool-calling)

\### System message

A \[\`SystemMessage\`\](https://reference.langchain.com/python/langchain-core/messages/system/SystemMessage) represent an initial set of instructions that primes the model's behavior. You can use a system message to set the tone, define the model's role, and establish guidelines for responses.

\`\`\`python Basic instructions theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
system\_msg = SystemMessage("You are a helpful coding assistant.")

messages = \[\
 system\_msg,\
 HumanMessage("How do I create a REST API?")\
\]
response = model.invoke(messages)
\`\`\`

\`\`\`python Detailed persona theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import SystemMessage, HumanMessage

system\_msg = SystemMessage("""
You are a senior Python developer with expertise in web frameworks.
Always provide code examples and explain your reasoning.
Be concise but thorough in your explanations.
""")

messages = \[\
 system\_msg,\
 HumanMessage("How do I create a REST API?")\
\]
response = model.invoke(messages)
\`\`\`

\\*\\*\\*

\### Human message

A \[\`HumanMessage\`\](https://reference.langchain.com/python/langchain-core/messages/human/HumanMessage) represents user input and interactions. They can contain text, images, audio, files, and any other amount of multimodal \[content\](#message-content).

\#### Text content

 \`\`\`python Message object theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 response = model.invoke(\[\
 HumanMessage("What is machine learning?")\
 \])
 \`\`\`

 \`\`\`python String shortcut theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # Using a string is a shortcut for a single HumanMessage
 response = model.invoke("What is machine learning?")
 \`\`\`

\#### Message metadata

\`\`\`python Add metadata theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
human\_msg = HumanMessage(
 content="Hello!",
 name="alice", # Optional: identify different users
 id="msg\_123", # Optional: unique identifier for tracing
)
\`\`\`

 The \`name\` field behavior varies by provider—some use it for user identification, others ignore it. To check, refer to the model provider's \[reference\](https://reference.langchain.com/python/integrations/).

\\*\\*\\*

\### AI message

An \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) represents the output of a model invocation. They can include multimodal data, tool calls, and provider-specific metadata that you can later access.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke("Explain AI")
print(type(response)) #
\`\`\`

\[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) objects are returned by the model when calling it, which contains all of the associated metadata in the response.

Providers weigh/contextualize types of messages differently, which means it is sometimes helpful to manually create a new \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) object and insert it into the message history as if it came from the model.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import AIMessage, SystemMessage, HumanMessage

\# Create an AI message manually (e.g., for conversation history)
ai\_msg = AIMessage("I'd be happy to help you with that question!")

\# Add to conversation history
messages = \[\
 SystemMessage("You are a helpful assistant"),\
 HumanMessage("Can you help me?"),\
 ai\_msg, # Insert as if it came from the model\
 HumanMessage("Great! What's 2+2?")\
\]

response = model.invoke(messages)
\`\`\`

 The text content of the message.

 The raw content of the message.

 The standardized \[content blocks\](#message-content) of the message.

 The tool calls made by the model.

 Empty if no tools are called.

 A unique identifier for the message (either automatically generated by LangChain or returned in the provider response)

 The usage metadata of the message, which can contain token counts when available.

 The response metadata of the message.


\#### Tool calls

When models make \[tool calls\](/oss/python/langchain/models#tool-calling), they're included in the \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage):

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model

model = init\_chat\_model("gpt-5-nano")

def get\_weather(location: str) -> str:
 """Get the weather at a location."""
 ...

model\_with\_tools = model.bind\_tools(\[get\_weather\])
response = model\_with\_tools.invoke("What's the weather in Paris?")

for tool\_call in response.tool\_calls:
 print(f"Tool: {tool\_call\['name'\]}")
 print(f"Args: {tool\_call\['args'\]}")
 print(f"ID: {tool\_call\['id'\]}")
\`\`\`

Other structured data, such as reasoning or citations, can also appear in message \[content\](/oss/python/langchain/messages#message-content).

\#### Token usage

An \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) can hold token counts and other usage metadata in its \[\`usage\_metadata\`\](https://reference.langchain.com/python/langchain-core/messages/ai/UsageMetadata) field:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model

model = init\_chat\_model("gpt-5-nano")

response = model.invoke("Hello!")
response.usage\_metadata
\`\`\`

\`\`\`
{'input\_tokens': 8,
 'output\_tokens': 304,
 'total\_tokens': 312,
 'input\_token\_details': {'audio': 0, 'cache\_read': 0},
 'output\_token\_details': {'audio': 0, 'reasoning': 256}}
\`\`\`

See \[\`UsageMetadata\`\](https://reference.langchain.com/python/langchain-core/messages/ai/UsageMetadata) for details.

\#### Streaming and chunks

During streaming, you'll receive \[\`AIMessageChunk\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessageChunk) objects that can be combined into a full message object:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
chunks = \[\]
full\_message = None
for chunk in model.stream("Hi"):
 chunks.append(chunk)
 print(chunk.text)
 full\_message = chunk if full\_message is None else full\_message + chunk
\`\`\`

 Learn more:

 \\* \[Streaming tokens from chat models\](/oss/python/langchain/models#stream)
 \\* \[Streaming tokens and/or steps from agents\](/oss/python/langchain/streaming)

\\*\\*\\*

\### Tool message

For models that support \[tool calling\](/oss/python/langchain/models#tool-calling), AI messages can contain tool calls. Tool messages are used to pass the results of a single tool execution back to the model.

\[Tools\](/oss/python/langchain/tools) can generate \[\`ToolMessage\`\](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) objects directly. Below, we show a simple example. Read more in the \[tools guide\](/oss/python/langchain/tools).

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import AIMessage
from langchain.messages import ToolMessage

\# After a model makes a tool call
\# (Here, we demonstrate manually creating the messages for brevity)
ai\_message = AIMessage(
 content=\[\],
 tool\_calls=\[{\
 "name": "get\_weather",\
 "args": {"location": "San Francisco"},\
 "id": "call\_123"\
 }\]
)

\# Execute tool and create result message
weather\_result = "Sunny, 72°F"
tool\_message = ToolMessage(
 content=weather\_result,
 tool\_call\_id="call\_123" # Must match the call ID
)

\# Continue conversation
messages = \[\
 HumanMessage("What's the weather in San Francisco?"),\
 ai\_message, # Model's tool call\
 tool\_message, # Tool execution result\
\]
response = model.invoke(messages) # Model processes the result
\`\`\`

 The stringified output of the tool call.

 The ID of the tool call that this message is responding to. Must match the ID of the tool call in the \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage).

 The name of the tool that was called.

 Additional data not sent to the model but can be accessed programmatically.

 The \`artifact\` field stores supplementary data that won't be sent to the model but can be accessed programmatically. This is useful for storing raw results, debugging information, or data for downstream processing without cluttering the model's context.


 For example, a \[retrieval\](/oss/python/langchain/retrieval) tool could retrieve a passage from a document for reference by a model. Where message \`content\` contains text that the model will reference, an \`artifact\` can contain document identifiers or other metadata that an application can use (e.g., to render a page). See example below:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.messages import ToolMessage

 # Sent to model
 message\_content = "It was the best of times, it was the worst of times."

 # Artifact available downstream
 artifact = {"document\_id": "doc\_123", "page": 0}

 tool\_message = ToolMessage(
 content=message\_content,
 tool\_call\_id="call\_123",
 name="search\_books",
 artifact=artifact,
 )
 \`\`\`

 See the \[RAG tutorial\](/oss/python/langchain/rag) for an end-to-end example of building retrieval \[agents\](/oss/python/langchain/agents) with LangChain.


\\*\\*\\*

\## Message content

You can think of a message's content as the payload of data that gets sent to the model. Messages have a \`content\` attribute that is loosely-typed, supporting strings and lists of untyped objects (e.g., dictionaries). This allows support for provider-native structures directly in LangChain chat models, such as \[multimodal\](#multimodal) content and other data.

Separately, LangChain provides dedicated content types for text, reasoning, citations, multi-modal data, server-side tool calls, and other message content. See \[content blocks\](#standard-content-blocks) below.

LangChain chat models accept message content in the \`content\` attribute.

This may contain either:

1\. A string
2\. A list of content blocks in a provider-native format
3\. A list of \[LangChain's standard content blocks\](#standard-content-blocks)

See below for an example using \[multimodal\](#multimodal) inputs:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import HumanMessage

\# String content
human\_message = HumanMessage("Hello, how are you?")

\# Provider-native format (e.g., OpenAI)
human\_message = HumanMessage(content=\[\
 {"type": "text", "text": "Hello, how are you?"},\
 {"type": "image\_url", "image\_url": {"url": "https://example.com/image.jpg"}}\
\])

\# List of standard content blocks
human\_message = HumanMessage(content\_blocks=\[\
 {"type": "text", "text": "Hello, how are you?"},\
 {"type": "image", "url": "https://example.com/image.jpg"},\
\])
\`\`\`

 Specifying \`content\_blocks\` when initializing a message will still populate message
 \`content\`, but provides a type-safe interface for doing so.

\### Standard content blocks

LangChain provides a standard representation for message content that works across providers.

Message objects implement a \`content\_blocks\` property that will lazily parse the \`content\` attribute into a standard, type-safe representation. For example, messages generated from \[\`ChatAnthropic\`\](/oss/python/integrations/chat/anthropic) or \[\`ChatOpenAI\`\](/oss/python/integrations/chat/openai) will include \`thinking\` or \`reasoning\` blocks in the format of the respective provider, but can be lazily parsed into a consistent \[\`ReasoningContentBlock\`\](#content-block-reference) representation:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.messages import AIMessage

 message = AIMessage(
 content=\[\
 {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."},\
 {"type": "text", "text": "..."},\
 \],
 response\_metadata={"model\_provider": "anthropic"}
 )
 message.content\_blocks
 \`\`\`

 \`\`\`
 \[{'type': 'reasoning',\
 'reasoning': '...',\
 'extras': {'signature': 'WaUjzkyp...'}},\
 {'type': 'text', 'text': '...'}\]
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.messages import AIMessage

 message = AIMessage(
 content=\[\
 {\
 "type": "reasoning",\
 "id": "rs\_abc123",\
 "summary": \[\
 {"type": "summary\_text", "text": "summary 1"},\
 {"type": "summary\_text", "text": "summary 2"},\
 \],\
 },\
 {"type": "text", "text": "...", "id": "msg\_abc123"},\
 \],
 response\_metadata={"model\_provider": "openai"}
 )
 message.content\_blocks
 \`\`\`

 \`\`\`
 \[{'type': 'reasoning', 'id': 'rs\_abc123', 'reasoning': 'summary 1'},\
 {'type': 'reasoning', 'id': 'rs\_abc123', 'reasoning': 'summary 2'},\
 {'type': 'text', 'text': '...', 'id': 'msg\_abc123'}\]
 \`\`\`


See the \[integrations guides\](/oss/python/integrations/providers/overview) to get started with the
inference provider of your choice.

 \*\*Serializing standard content\*\*

 If an application outside of LangChain needs access to the standard content block
 representation, you can opt-in to storing content blocks in message content.

 To do this, you can set the \`LC\_OUTPUT\_VERSION\` environment variable to \`v1\`. Or,
 initialize any chat model with \`output\_version="v1"\`:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.chat\_models import init\_chat\_model

 model = init\_chat\_model("gpt-5-nano", output\_version="v1")
 \`\`\`

\### Multimodal

\*\*Multimodality\*\* refers to the ability to work with data that comes in different
forms, such as text, audio, images, and video. LangChain includes standard types
for these data that can be used across providers.

\[Chat models\](/oss/python/langchain/models) can accept multimodal data as input and generate
it as output. Below we show short examples of input messages featuring multimodal data.

 Extra keys can be included top-level in the content block or nested in \`"extras": {"key": value}\`.

 \[OpenAI\](/oss/python/integrations/chat/openai) and \[AWS Bedrock Converse\](/oss/python/integrations/chat/bedrock),
 for example, require a filename for PDFs. See the \[provider page\](/oss/python/integrations/providers/overview)
 for your chosen model for specifics.

 \`\`\`python Image input theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # From URL
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this image."},\
 {"type": "image", "url": "https://example.com/path/to/image.jpg"},\
 \]
 }

 # From base64 data
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this image."},\
 {\
 "type": "image",\
 "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",\
 "mime\_type": "image/jpeg",\
 },\
 \]
 }

 # From provider-managed File ID
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this image."},\
 {"type": "image", "file\_id": "file-abc123"},\
 \]
 }
 \`\`\`

 \`\`\`python PDF document input theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # From URL
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this document."},\
 {"type": "file", "url": "https://example.com/path/to/document.pdf"},\
 \]
 }

 # From base64 data
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this document."},\
 {\
 "type": "file",\
 "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",\
 "mime\_type": "application/pdf",\
 },\
 \]
 }

 # From provider-managed File ID
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this document."},\
 {"type": "file", "file\_id": "file-abc123"},\
 \]
 }
 \`\`\`

 \`\`\`python Audio input theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # From base64 data
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this audio."},\
 {\
 "type": "audio",\
 "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",\
 "mime\_type": "audio/wav",\
 },\
 \]
 }

 # From provider-managed File ID
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this audio."},\
 {"type": "audio", "file\_id": "file-abc123"},\
 \]
 }
 \`\`\`

 \`\`\`python Video input theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # From base64 data
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this video."},\
 {\
 "type": "video",\
 "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",\
 "mime\_type": "video/mp4",\
 },\
 \]
 }

 # From provider-managed File ID
 message = {
 "role": "user",
 "content": \[\
 {"type": "text", "text": "Describe the content of this video."},\
 {"type": "video", "file\_id": "file-abc123"},\
 \]
 }
 \`\`\`

 Not all models support all file types. Check the model provider's \[reference\](https://reference.langchain.com/python/integrations/) for supported formats and size limits.

\### Content block reference

Content blocks are represented (either when creating a message or accessing the \`content\_blocks\` property) as a list of typed dictionaries. Each item in the list must adhere to one of the following block types:

 \*\*Purpose:\*\* Standard text output


 Always \`"text"\`

 The text content

 List of annotations for the text

 Additional provider-specific data


 \*\*Example:\*\*

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 {
 "type": "text",
 "text": "Hello world",
 "annotations": \[\]
 }
 \`\`\`

 \*\*Purpose:\*\* Model reasoning steps


 Always \`"reasoning"\`

 The reasoning content

 Additional provider-specific data


 \*\*Example:\*\*

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 {
 "type": "reasoning",
 "reasoning": "The user is asking about...",
 "extras": {"signature": "abc123"},
 }
 \`\`\`

 \*\*Purpose:\*\* Image data


 Always \`"image"\`

 URL pointing to the image location.

 Base64-encoded image data.

 Unique identifier for this content block (either generated by the provider or by LangChain).

 Image \[MIME type\](https://www.iana.org/assignments/media-types/media-types.xhtml#image) (e.g., \`image/jpeg\`, \`image/png\`). Required for base64 data.

 \*\*Purpose:\*\* Audio data


 Always \`"audio"\`

 URL pointing to the audio location.

 Base64-encoded audio data.

 Unique identifier for this content block (either generated by the provider or by LangChain).

 Audio \[MIME type\](https://www.iana.org/assignments/media-types/media-types.xhtml#audio) (e.g., \`audio/mpeg\`, \`audio/wav\`). Required for base64 data.

 \*\*Purpose:\*\* Video data


 Always \`"video"\`

 URL pointing to the video location.

 Base64-encoded video data.

 Unique identifier for this content block (either generated by the provider or by LangChain).

 Video \[MIME type\](https://www.iana.org/assignments/media-types/media-types.xhtml#video) (e.g., \`video/mp4\`, \`video/webm\`). Required for base64 data.

 \*\*Purpose:\*\* Generic files (PDF, etc)


 Always \`"file"\`

 URL pointing to the file location.

 Base64-encoded file data.

 Unique identifier for this content block (either generated by the provider or by LangChain).

 File \[MIME type\](https://www.iana.org/assignments/media-types/media-types.xhtml) (e.g., \`application/pdf\`). Required for base64 data.

 \*\*Purpose:\*\* Document text (\`.txt\`, \`.md\`)


 Always \`"text-plain"\`

 The text content

 \[MIME type\](https://www.iana.org/assignments/media-types/media-types.xhtml) of the text (e.g., \`text/plain\`, \`text/markdown\`)

 \*\*Purpose:\*\* Function calls


 Always \`"tool\_call"\`

 Name of the tool to call

 Arguments to pass to the tool

 Unique identifier for this tool call


 \*\*Example:\*\*

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 {
 "type": "tool\_call",
 "name": "search",
 "args": {"query": "weather"},
 "id": "call\_123"
 }
 \`\`\`

 \*\*Purpose:\*\* Streaming tool call fragments


 Always \`"tool\_call\_chunk"\`

 Name of the tool being called

 Partial tool arguments (may be incomplete JSON)

 Tool call identifier

 Position of this chunk in the stream

 \*\*Purpose:\*\* Malformed calls, intended to catch JSON parsing errors.


 Always \`"invalid\_tool\_call"\`

 Name of the tool that failed to be called

 Arguments to pass to the tool

 Description of what went wrong

 \*\*Purpose:\*\* Tool call that is executed server-side.


 Always \`"server\_tool\_call"\`

 An identifier associated with the tool call.

 The name of the tool to be called.

 Partial tool arguments (may be incomplete JSON)

 \*\*Purpose:\*\* Streaming server-side tool call fragments


 Always \`"server\_tool\_call\_chunk"\`

 An identifier associated with the tool call.

 Name of the tool being called

 Partial tool arguments (may be incomplete JSON)

 Position of this chunk in the stream

 \*\*Purpose:\*\* Search results


 Always \`"server\_tool\_result"\`

 Identifier of the corresponding server tool call.

 Identifier associated with the server tool result.

 Execution status of the server-side tool. \`"success"\` or \`"error"\`.

 Output of the executed tool.

 \*\*Purpose:\*\* Provider-specific escape hatch


 Always \`"non\_standard"\`

 Provider-specific data structure


 \*\*Usage:\*\* For experimental or provider-unique features


 Additional provider-specific content types may be found within the \[reference documentation\](/oss/python/integrations/providers/overview) of each model provider.

 View the canonical type definitions in the \[API reference\](https://reference.langchain.com/python/langchain/messages).

 Content blocks were introduced as a new property on messages in LangChain v1 to standardize content formats across providers while maintaining backward compatibility with existing code.

 Content blocks are not a replacement for the \[\`content\`\](https://reference.langchain.com/python/langchain-core/messages/base/BaseMessage) property, but rather a new property that can be used to access the content of a message in a standardized format.

\## Use with chat models

\[Chat models\](/oss/python/langchain/models) accept a sequence of message objects as input and return an \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) as output. Interactions are often stateless, so that a simple conversational loop involves invoking a model with a growing list of messages.

Refer to the below guides to learn more:

\\* Built-in features for \[persisting and managing conversation histories\](/oss/python/langchain/short-term-memory)
\\* Strategies for managing context windows, including \[trimming and summarizing messages\](/oss/python/langchain/short-term-memory#common-patterns)

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/messages.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-models.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Models

\[LLMs\](https://en.wikipedia.org/wiki/Large\_language\_model) are powerful AI tools that can interpret and generate text like humans. They're versatile enough to write content, translate languages, summarize, and answer questions without needing specialized training for each task.

In addition to text generation, many models support:

\\*  \[Tool calling\](#tool-calling) - calling external tools (like databases queries or API calls) and use results in their responses.
\\*  \[Structured output\](#structured-output) - where the model's response is constrained to follow a defined format.
\\*  \[Multimodality\](#multimodal) - process and return data other than text, such as images, audio, and video.
\\*  \[Reasoning\](#reasoning) - models perform multi-step reasoning to arrive at a conclusion.

Models are the reasoning engine of \[agents\](/oss/python/langchain/agents). They drive the agent's decision-making process, determining which tools to call, how to interpret results, and when to provide a final answer.

The quality and capabilities of the model you choose directly impact your agent's baseline reliability and performance. Different models excel at different tasks - some are better at following complex instructions, others at structured reasoning, and some support larger context windows for handling more information.

LangChain's standard model interfaces give you access to many different provider integrations, which makes it easy to experiment with and switch between models to find the best fit for your use case.

 For provider-specific integration information and capabilities, see the provider's \[chat model page\](/oss/python/integrations/chat).

\## Basic usage

Models can be utilized in two ways:

1\. \*\*With agents\*\* - Models can be dynamically specified when creating an \[agent\](/oss/python/langchain/agents#model).
2\. \*\*Standalone\*\* - Models can be called directly (outside of the agent loop) for tasks like text generation, classification, or extraction without the need for an agent framework.

The same model interface works in both contexts, which gives you the flexibility to start simple and scale up to more complex agent-based workflows as needed.

\### Initialize a model

The easiest way to get started with a standalone model in LangChain is to use \[\`init\_chat\_model\`\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model) to initialize one from a chat model provider of your choice (examples below):

 👉 Read the \[OpenAI chat model integration docs\](/oss/python/integrations/chat/openai/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[openai\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["OPENAI\_API\_KEY"\] = "sk-..."

 model = init\_chat\_model("gpt-5.4")
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_openai import ChatOpenAI

 os.environ\["OPENAI\_API\_KEY"\] = "sk-..."

 model = ChatOpenAI(model="gpt-5.4")
 \`\`\`

 👉 Read the \[Anthropic chat model integration docs\](/oss/python/integrations/chat/anthropic/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[anthropic\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["ANTHROPIC\_API\_KEY"\] = "sk-..."

 model = init\_chat\_model("claude-sonnet-4-6")
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_anthropic import ChatAnthropic

 os.environ\["ANTHROPIC\_API\_KEY"\] = "sk-..."

 model = ChatAnthropic(model="claude-sonnet-4-6")
 \`\`\`

 👉 Read the \[Azure chat model integration docs\](/oss/python/integrations/chat/azure\_chat\_openai/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[openai\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["AZURE\_OPENAI\_API\_KEY"\] = "..."
 os.environ\["AZURE\_OPENAI\_ENDPOINT"\] = "..."
 os.environ\["OPENAI\_API\_VERSION"\] = "2025-03-01-preview"

 model = init\_chat\_model(
 "azure\_openai:gpt-5.4",
 azure\_deployment=os.environ\["AZURE\_OPENAI\_DEPLOYMENT\_NAME"\],
 )
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_openai import AzureChatOpenAI

 os.environ\["AZURE\_OPENAI\_API\_KEY"\] = "..."
 os.environ\["AZURE\_OPENAI\_ENDPOINT"\] = "..."
 os.environ\["OPENAI\_API\_VERSION"\] = "2025-03-01-preview"

 model = AzureChatOpenAI(
 model="gpt-5.4",
 azure\_deployment=os.environ\["AZURE\_OPENAI\_DEPLOYMENT\_NAME"\]
 )
 \`\`\`

 👉 Read the \[Google GenAI chat model integration docs\](/oss/python/integrations/chat/google\_generative\_ai/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[google-genai\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["GOOGLE\_API\_KEY"\] = "..."

 model = init\_chat\_model("google\_genai:gemini-2.5-flash-lite")
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_google\_genai import ChatGoogleGenerativeAI

 os.environ\["GOOGLE\_API\_KEY"\] = "..."

 model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
 \`\`\`

 👉 Read the \[AWS Bedrock chat model integration docs\](/oss/python/integrations/chat/bedrock/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[aws\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.chat\_models import init\_chat\_model

 # Follow the steps here to configure your credentials:
 # https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html

 model = init\_chat\_model(
 "anthropic.claude-3-5-sonnet-20240620-v1:0",
 model\_provider="bedrock\_converse",
 )
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain\_aws import ChatBedrock

 model = ChatBedrock(model="anthropic.claude-3-5-sonnet-20240620-v1:0")
 \`\`\`

 👉 Read the \[HuggingFace chat model integration docs\](/oss/python/integrations/chat/huggingface/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain\[huggingface\]"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["HUGGINGFACEHUB\_API\_TOKEN"\] = "hf\_..."

 model = init\_chat\_model(
 "microsoft/Phi-3-mini-4k-instruct",
 model\_provider="huggingface",
 temperature=0.7,
 max\_tokens=1024,
 )
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_huggingface import ChatHuggingFace, HuggingFaceEndpoint

 os.environ\["HUGGINGFACEHUB\_API\_TOKEN"\] = "hf\_..."

 llm = HuggingFaceEndpoint(
 repo\_id="microsoft/Phi-3-mini-4k-instruct",
 temperature=0.7,
 max\_length=1024,
 )
 model = ChatHuggingFace(llm=llm)
 \`\`\`

 👉 Read the \[OpenRouter chat model integration docs\](/oss/python/integrations/chat/openrouter/)

 \`\`\`shell theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install -U "langchain-openrouter"
 \`\`\`


 \`\`\`python init\_chat\_model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain.chat\_models import init\_chat\_model

 os.environ\["OPENROUTER\_API\_KEY"\] = "sk-..."

 model = init\_chat\_model(
 "auto",
 model\_provider="openrouter",
 )
 \`\`\`

 \`\`\`python Model Class theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import os
 from langchain\_openrouter import ChatOpenRouter

 os.environ\["OPENROUTER\_API\_KEY"\] = "sk-..."

 model = ChatOpenRouter(model="auto")
 \`\`\`


\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke("Why do parrots talk?")
\`\`\`

See \[\`init\_chat\_model\`\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model) for more detail, including information on how to pass model \[parameters\](#parameters).

\### Supported providers and models

LangChain supports all major model providers through dedicated integration packages. Each provider package implements the same standard interface, so you can swap providers without rewriting application logic. New model names work immediately — no LangChain update required — because provider packages pass model names directly to the provider's API.

Browse the \[full list of supported providers\](/oss/python/integrations/providers/overview), or see \[Providers and models\](/oss/python/concepts/providers-and-models) for a conceptual overview of how providers, packages, and model names work together in LangChain.

\### Key methods

 The model takes messages as input and outputs messages after generating a complete response.

 Invoke the model, but stream the output as it is generated in real-time.

 Send multiple requests to a model in a batch for more efficient processing.

 In addition to chat models, LangChain provides support for other adjacent technologies, such as embedding models and vector stores. See the \[integrations page\](/oss/python/integrations/providers/overview) for details.

\## Parameters

A chat model takes parameters that can be used to configure its behavior. The full set of supported parameters varies by model and provider, but standard ones include:

 The name or identifier of the specific model you want to use with a provider. You can also specify both the model and its provider in a single argument using the '{model\_provider}:{model}' format, for example, 'openai:o1'.

 The key required for authenticating with the model's provider. This is usually issued when you sign up for access to the model. Often accessed by setting an environment variable.

 Controls the randomness of the model's output. A higher number makes responses more creative; lower ones make them more deterministic.

 Limits the total number of tokens in the response, effectively controlling how long the output can be.

 The maximum time (in seconds) to wait for a response from the model before canceling the request.

 The maximum number of attempts the system will make to resend a request if it fails due to issues like network timeouts or rate limits. Retries use exponential backoff with jitter. Network errors, rate limits (429), and server errors (5xx) are retried automatically. Client errors such as 401 (unauthorized) or 404 are not retried. For long-running \[agent\](/oss/python/deepagents/overview) tasks on unreliable networks, consider increasing this to 10–15.

Using \[\`init\_chat\_model\`\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model), pass these parameters as inline \`\*\*kwargs\`:

\`\`\`python Initialize using model parameters theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
model = init\_chat\_model(
 "claude-sonnet-4-6",
 # Kwargs passed to the model:
 temperature=0.7,
 timeout=30,
 max\_tokens=1000,
 max\_retries=6, # Default; increase for unreliable networks
)
\`\`\`

\### Connection resilience

LangChain chat models automatically retry failed API requests with exponential backoff. By default, models retry up to \*\*6 times\*\* for network errors, rate limits (429), and server errors (5xx). Client errors like 401 (unauthorized) or 404 are not retried.

You can adjust \`max\_retries\` and \`timeout\` when creating a model, then pass that instance to \`create\_agent\`, \`create\_deep\_agent\`, or call it standalone:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model

model = init\_chat\_model(
 "google\_genai:gemini-3.1-pro-preview",
 max\_retries=10, # Increase for unreliable networks (default: 6)
 timeout=120, # Seconds; increase for slow connections
)
\`\`\`

 For long-running agent graphs on unreliable networks, consider higher \`max\_retries\` (for example 10–15) and a \[checkpointer\](/oss/python/langgraph/persistence) so that progress is preserved across failures.

 Each chat model integration may have additional params used to control provider-specific functionality.

 For example, \[\`ChatOpenAI\`\](https://reference.langchain.com/python/langchain-openai/chat\_models/base/ChatOpenAI) has \`use\_responses\_api\` to dictate whether to use the OpenAI Responses or Completions API.

 To find all the parameters supported by a given chat model, head to the \[chat model integrations\](/oss/python/integrations/chat) page.

\\*\\*\\*

\## Invocation

A chat model must be invoked to generate an output. There are three primary invocation methods, each suited to different use cases.

\### Invoke

The most straightforward way to call a model is to use \[\`invoke()\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/invoke) with a single message or a list of messages.

\`\`\`python Single message theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke("Why do parrots have colorful feathers?")
print(response)
\`\`\`

A list of messages can be provided to a chat model to represent conversation history. Each message has a role that models use to indicate who sent the message in the conversation.

See the \[messages\](/oss/python/langchain/messages) guide for more detail on roles, types, and content.

\`\`\`python Dictionary format theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
conversation = \[\
 {"role": "system", "content": "You are a helpful assistant that translates English to French."},\
 {"role": "user", "content": "Translate: I love programming."},\
 {"role": "assistant", "content": "J'adore la programmation."},\
 {"role": "user", "content": "Translate: I love building applications."}\
\]

response = model.invoke(conversation)
print(response) # AIMessage("J'adore créer des applications.")
\`\`\`

\`\`\`python Message objects theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = \[\
 SystemMessage("You are a helpful assistant that translates English to French."),\
 HumanMessage("Translate: I love programming."),\
 AIMessage("J'adore la programmation."),\
 HumanMessage("Translate: I love building applications.")\
\]

response = model.invoke(conversation)
print(response) # AIMessage("J'adore créer des applications.")
\`\`\`

 If the return type of your invocation is a string, ensure that you are using a chat model as opposed to a LLM. Legacy, text-completion LLMs return strings directly. LangChain chat models are prefixed with "Chat", e.g., \[\`ChatOpenAI\`\](https://reference.langchain.com/python/langchain-openai/chat\_models/base/ChatOpenAI)(/oss/integrations/chat/openai).

\### Stream

Most models can stream their output content while it is being generated. By displaying output progressively, streaming significantly improves user experience, particularly for longer responses.

Calling \[\`stream()\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/stream) returns an iterator that yields output chunks as they are produced. You can use a loop to process each chunk in real-time:

 \`\`\`python Basic text streaming theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 for chunk in model.stream("Why do parrots have colorful feathers?"):
 print(chunk.text, end="\|", flush=True)
 \`\`\`

 \`\`\`python Stream tool calls, reasoning, and other content theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 for chunk in model.stream("What color is the sky?"):
 for block in chunk.content\_blocks:
 if block\["type"\] == "reasoning" and (reasoning := block.get("reasoning")):
 print(f"Reasoning: {reasoning}")
 elif block\["type"\] == "tool\_call\_chunk":
 print(f"Tool call chunk: {block}")
 elif block\["type"\] == "text":
 print(block\["text"\])
 else:
 ...
 \`\`\`

As opposed to \[\`invoke()\`\](#invoke), which returns a single \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) after the model has finished generating its full response, \`stream()\` returns multiple \[\`AIMessageChunk\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessageChunk) objects, each containing a portion of the output text. Importantly, each chunk in a stream is designed to be gathered into a full message via summation:

\`\`\`python Construct an AIMessage theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
full = None # None \| AIMessageChunk
for chunk in model.stream("What color is the sky?"):
 full = chunk if full is None else full + chunk
 print(full.text)

\# The
\# The sky
\# The sky is
\# The sky is typically
\# The sky is typically blue
\# ...

print(full.content\_blocks)
\# \[{"type": "text", "text": "The sky is typically blue..."}\]
\`\`\`

The resulting message can be treated the same as a message that was generated with \[\`invoke()\`\](#invoke)—for example, it can be aggregated into a message history and passed back to the model as conversational context.

 Streaming only works if all steps in the program know how to process a stream of chunks. For instance, an application that isn't streaming-capable would be one that needs to store the entire output in memory before it can be processed.

 LangChain chat models can also stream semantic events using \`astream\_events()\`.

 This simplifies filtering based on event types and other metadata, and will aggregate the full message in the background. See below for an example.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 async for event in model.astream\_events("Hello"):

 if event\["event"\] == "on\_chat\_model\_start":
 print(f"Input: {event\['data'\]\['input'\]}")

 elif event\["event"\] == "on\_chat\_model\_stream":
 print(f"Token: {event\['data'\]\['chunk'\].text}")

 elif event\["event"\] == "on\_chat\_model\_end":
 print(f"Full message: {event\['data'\]\['output'\].text}")

 else:
 pass
 \`\`\`

 \`\`\`txt theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 Input: Hello
 Token: Hi
 Token: there
 Token: !
 Token: How
 Token: can
 Token: I
 ...
 Full message: Hi there! How can I help today?
 \`\`\`


 See the \[\`astream\_events()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.astream\_events) reference for event types and other details.

 LangChain simplifies streaming from chat models by automatically enabling streaming mode in certain cases, even when you're not explicitly calling the streaming methods. This is particularly useful when you use the non-streaming invoke method but still want to stream the entire application, including intermediate results from the chat model.

 In \[LangGraph agents\](/oss/python/langchain/agents), for example, you can call \`model.invoke()\` within nodes, but LangChain will automatically delegate to streaming if running in a streaming mode.

 #### How it works

 When you \`invoke()\` a chat model, LangChain will automatically switch to an internal streaming mode if it detects that you are trying to stream the overall application. The result of the invocation will be the same as far as the code that was using invoke is concerned; however, while the chat model is being streamed, LangChain will take care of invoking \[\`on\_llm\_new\_token\`\](https://reference.langchain.com/python/langchain-core/callbacks/base/AsyncCallbackHandler/on\_llm\_new\_token) events in LangChain's callback system.

 Callback events allow LangGraph \`stream()\` and \`astream\_events()\` to surface the chat model's output in real-time.


\### Batch

Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel:

\`\`\`python Batch theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
responses = model.batch(\[\
 "Why do parrots have colorful feathers?",\
 "How do airplanes fly?",\
 "What is quantum computing?"\
\])
for response in responses:
 print(response)
\`\`\`

 This section describes a chat model method \[\`batch()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch), which parallelizes model calls client-side.

 It is \*\*distinct\*\* from batch APIs supported by inference providers, such as \[OpenAI\](https://platform.openai.com/docs/guides/batch) or \[Anthropic\](https://platform.claude.com/docs/en/build-with-claude/batch-processing#message-batches-api).

By default, \[\`batch()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch) will only return the final output for the entire batch. If you want to receive the output for each individual input as it finishes generating, you can stream results with \[\`batch\_as\_completed()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch\_as\_completed):

\`\`\`python Yield batch responses upon completion theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
for response in model.batch\_as\_completed(\[\
 "Why do parrots have colorful feathers?",\
 "How do airplanes fly?",\
 "What is quantum computing?"\
\]):
 print(response)
\`\`\`

 When using \[\`batch\_as\_completed()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch\_as\_completed), results may arrive out of order. Each includes the input index for matching to reconstruct the original order as needed.

 When processing a large number of inputs using \[\`batch()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch) or \[\`batch\_as\_completed()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch\_as\_completed), you may want to control the maximum number of parallel calls. This can be done by setting the \[\`max\_concurrency\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) attribute in the \[\`RunnableConfig\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) dictionary.

 \`\`\`python Batch with max concurrency theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model.batch(
 list\_of\_inputs,
 config={
 'max\_concurrency': 5, # Limit to 5 parallel calls
 }
 )
 \`\`\`

 See the \[\`RunnableConfig\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) reference for a full list of supported attributes.

For more details on batching, see the \[reference\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch).

\\*\\*\\*

\## Tool calling

Models can request to call tools that perform tasks such as fetching data from a database, searching the web, or running code. Tools are pairings of:

1\. A schema, including the name of the tool, a description, and/or argument definitions (often a JSON schema)
2\. A function or coroutine to execute.

 You may hear the term "function calling". We use this interchangeably with "tool calling".

Here's the basic tool calling flow between a user and a model:

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
sequenceDiagram
 participant U as User
 participant M as Model
 participant T as Tools

 U->>M: "What's the weather in SF and NYC?"
 M->>M: Analyze request & decide tools needed

 par Parallel Tool Calls
 M->>T: get\_weather("San Francisco")
 M->>T: get\_weather("New York")
 end

 par Tool Execution
 T-->>M: SF weather data
 T-->>M: NYC weather data
 end

 M->>M: Process results & generate response
 M->>U: "SF: 72°F sunny, NYC: 68°F cloudy"
\`\`\`

To make tools that you have defined available for use by a model, you must bind them using \[\`bind\_tools\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/bind\_tools). In subsequent invocations, the model can choose to call any of the bound tools as needed.

Some model providers offer built-in tools that can be enabled via model or invocation parameters (e.g. \[\`ChatOpenAI\`\](/oss/python/integrations/chat/openai), \[\`ChatAnthropic\`\](/oss/python/integrations/chat/anthropic)). Check the respective \[provider reference\](/oss/python/integrations/providers/overview) for details.

 See the \[tools guide\](/oss/python/langchain/tools) for details and other options for creating tools.

\`\`\`python Binding user tools theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool

@tool
def get\_weather(location: str) -> str:
 """Get the weather at a location."""
 return f"It's sunny in {location}."

model\_with\_tools = model.bind\_tools(\[get\_weather\]) # \[!code highlight\]

response = model\_with\_tools.invoke("What's the weather like in Boston?")
for tool\_call in response.tool\_calls:
 # View tool calls made by the model
 print(f"Tool: {tool\_call\['name'\]}")
 print(f"Args: {tool\_call\['args'\]}")
\`\`\`

When binding user-defined tools, the model's response includes a \*\*request\*\* to execute a tool. When using a model separately from an \[agent\](/oss/python/langchain/agents), it is up to you to execute the requested tool and return the result back to the model for use in subsequent reasoning. When using an \[agent\](/oss/python/langchain/agents), the agent loop will handle the tool execution loop for you.

Below, we show some common ways you can use tool calling.

 When a model returns tool calls, you need to execute the tools and pass the results back to the model. This creates a conversation loop where the model can use tool results to generate its final response. LangChain includes \[agent\](/oss/python/langchain/agents) abstractions that handle this orchestration for you.

 Here's a simple example of how to do this:

 \`\`\`python Tool execution loop theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # Bind (potentially multiple) tools to the model
 model\_with\_tools = model.bind\_tools(\[get\_weather\])

 # Step 1: Model generates tool calls
 messages = \[{"role": "user", "content": "What's the weather in Boston?"}\]
 ai\_msg = model\_with\_tools.invoke(messages)
 messages.append(ai\_msg)

 # Step 2: Execute tools and collect results
 for tool\_call in ai\_msg.tool\_calls:
 # Execute the tool with the generated arguments
 tool\_result = get\_weather.invoke(tool\_call)
 messages.append(tool\_result)

 # Step 3: Pass results back to model for final response
 final\_response = model\_with\_tools.invoke(messages)
 print(final\_response.text)
 # "The current weather in Boston is 72°F and sunny."
 \`\`\`

 Each \[\`ToolMessage\`\](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage) returned by the tool includes a \`tool\_call\_id\` that matches the original tool call, helping the model correlate results with requests.

 By default, the model has the freedom to choose which bound tool to use based on the user's input. However, you might want to force choosing a tool, ensuring the model uses either a particular tool or \*\*any\*\* tool from a given list:


 \`\`\`python Force use of any tool theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model\_with\_tools = model.bind\_tools(\[tool\_1\], tool\_choice="any")
 \`\`\`

 \`\`\`python Force use of specific tools theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model\_with\_tools = model.bind\_tools(\[tool\_1\], tool\_choice="tool\_1")
 \`\`\`

 Many models support calling multiple tools in parallel when appropriate. This allows the model to gather information from different sources simultaneously.

 \`\`\`python Parallel tool calls theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model\_with\_tools = model.bind\_tools(\[get\_weather\])

 response = model\_with\_tools.invoke(
 "What's the weather in Boston and Tokyo?"
 )

 # The model may generate multiple tool calls
 print(response.tool\_calls)
 # \[\
 # {'name': 'get\_weather', 'args': {'location': 'Boston'}, 'id': 'call\_1'},\
 # {'name': 'get\_weather', 'args': {'location': 'Tokyo'}, 'id': 'call\_2'},\
 # \]

 # Execute all tools (can be done in parallel with async)
 results = \[\]
 for tool\_call in response.tool\_calls:
 if tool\_call\['name'\] == 'get\_weather':
 result = get\_weather.invoke(tool\_call)
 ...
 results.append(result)
 \`\`\`

 The model intelligently determines when parallel execution is appropriate based on the independence of the requested operations.


 Most models supporting tool calling enable parallel tool calls by default. Some (including \[OpenAI\](/oss/python/integrations/chat/openai) and \[Anthropic\](/oss/python/integrations/chat/anthropic)) allow you to disable this feature. To do this, set \`parallel\_tool\_calls=False\`:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model.bind\_tools(\[get\_weather\], parallel\_tool\_calls=False)
 \`\`\`

 When streaming responses, tool calls are progressively built through \[\`ToolCallChunk\`\](https://reference.langchain.com/python/langchain-core/messages/tool/ToolCallChunk). This allows you to see tool calls as they're being generated rather than waiting for the complete response.

 \`\`\`python Streaming tool calls theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 for chunk in model\_with\_tools.stream(
 "What's the weather in Boston and Tokyo?"
 ):
 # Tool call chunks arrive progressively
 for tool\_chunk in chunk.tool\_call\_chunks:
 if name := tool\_chunk.get("name"):
 print(f"Tool: {name}")
 if id\_ := tool\_chunk.get("id"):
 print(f"ID: {id\_}")
 if args := tool\_chunk.get("args"):
 print(f"Args: {args}")

 # Output:
 # Tool: get\_weather
 # ID: call\_SvMlU1TVIZugrFLckFE2ceRE
 # Args: {"lo
 # Args: catio
 # Args: n": "B
 # Args: osto
 # Args: n"}
 # Tool: get\_weather
 # ID: call\_QMZdy6qInx13oWKE7KhuhOLR
 # Args: {"lo
 # Args: catio
 # Args: n": "T
 # Args: okyo
 # Args: "}
 \`\`\`

 You can accumulate chunks to build complete tool calls:

 \`\`\`python Accumulate tool calls theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 gathered = None
 for chunk in model\_with\_tools.stream("What's the weather in Boston?"):
 gathered = chunk if gathered is None else gathered + chunk
 print(gathered.tool\_calls)
 \`\`\`


\\*\\*\\*

\## Structured output

Models can be requested to provide their response in a format matching a given schema. This is useful for ensuring the output can be easily parsed and used in subsequent processing. LangChain supports multiple schema types and methods for enforcing structured output.

 To learn about structured output, see \[Structured output\](/oss/python/langchain/structured-output).

 \[Pydantic models\](https://docs.pydantic.dev/latest/concepts/models/#basic-model-usage) provide the richest feature set with field validation, descriptions, and nested structures.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from pydantic import BaseModel, Field

 class Movie(BaseModel):
 """A movie with details."""
 title: str = Field(description="The title of the movie")
 year: int = Field(description="The year the movie was released")
 director: str = Field(description="The director of the movie")
 rating: float = Field(description="The movie's rating out of 10")

 model\_with\_structure = model.with\_structured\_output(Movie)
 response = model\_with\_structure.invoke("Provide details about the movie Inception")
 print(response) # Movie(title="Inception", year=2010, director="Christopher Nolan", rating=8.8)
 \`\`\`

 Python's \`TypedDict\` provides a simpler alternative to Pydantic models, ideal when you don't need runtime validation.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from typing\_extensions import TypedDict, Annotated

 class MovieDict(TypedDict):
 """A movie with details."""
 title: Annotated\[str, ..., "The title of the movie"\]
 year: Annotated\[int, ..., "The year the movie was released"\]
 director: Annotated\[str, ..., "The director of the movie"\]
 rating: Annotated\[float, ..., "The movie's rating out of 10"\]

 model\_with\_structure = model.with\_structured\_output(MovieDict)
 response = model\_with\_structure.invoke("Provide details about the movie Inception")
 print(response) # {'title': 'Inception', 'year': 2010, 'director': 'Christopher Nolan', 'rating': 8.8}
 \`\`\`

 Provide a \[JSON Schema\](https://json-schema.org/understanding-json-schema/about) for maximum control and interoperability.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import json

 json\_schema = {
 "title": "Movie",
 "description": "A movie with details",
 "type": "object",
 "properties": {
 "title": {
 "type": "string",
 "description": "The title of the movie"
 },
 "year": {
 "type": "integer",
 "description": "The year the movie was released"
 },
 "director": {
 "type": "string",
 "description": "The director of the movie"
 },
 "rating": {
 "type": "number",
 "description": "The movie's rating out of 10"
 }
 },
 "required": \["title", "year", "director", "rating"\]
 }

 model\_with\_structure = model.with\_structured\_output(
 json\_schema,
 method="json\_schema",
 )
 response = model\_with\_structure.invoke("Provide details about the movie Inception")
 print(response) # {'title': 'Inception', 'year': 2010, ...}
 \`\`\`

 \*\*Key considerations for structured output\*\*

 \\* \*\*Method parameter\*\*: Some providers support different methods for structured output:
 \\* \`'json\_schema'\`: Uses dedicated structured output features offered by the provider.
 \\* \`'function\_calling'\`: Derives structured output by forcing a \[tool call\](#tool-calling) that follows the given schema.
 \\* \`'json\_mode'\`: A precursor to \`'json\_schema'\` offered by some providers. Generates valid JSON, but the schema must be described in the prompt.
 \\* \*\*Include raw\*\*: Set \`include\_raw=True\` to get both the parsed output and the raw AI message.
 \\* \*\*Validation\*\*: Pydantic models provide automatic validation. \`TypedDict\` and JSON Schema require manual validation.

 See your \[provider's integration page\](/oss/python/integrations/providers/overview) for supported methods and configuration options.

 It can be useful to return the raw \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) object alongside the parsed representation to access response metadata such as \[token counts\](#token-usage). To do this, set \[\`include\_raw=True\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/with\_structured\_output) when calling \[\`with\_structured\_output\`\](https://reference.langchain.com/python/langchain-core/language\_models/chat\_models/BaseChatModel/with\_structured\_output):

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from pydantic import BaseModel, Field

 class Movie(BaseModel):
 """A movie with details."""
 title: str = Field(description="The title of the movie")
 year: int = Field(description="The year the movie was released")
 director: str = Field(description="The director of the movie")
 rating: float = Field(description="The movie's rating out of 10")

 model\_with\_structure = model.with\_structured\_output(Movie, include\_raw=True) # \[!code highlight\]
 response = model\_with\_structure.invoke("Provide details about the movie Inception")
 response
 # {
 # "raw": AIMessage(...),
 # "parsed": Movie(title=..., year=..., ...),
 # "parsing\_error": None,
 # }
 \`\`\`

 Schemas can be nested:


 \`\`\`python Pydantic BaseModel theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from pydantic import BaseModel, Field

 class Actor(BaseModel):
 name: str
 role: str

 class MovieDetails(BaseModel):
 title: str
 year: int
 cast: list\[Actor\]
 genres: list\[str\]
 budget: float \| None = Field(None, description="Budget in millions USD")

 model\_with\_structure = model.with\_structured\_output(MovieDetails)
 \`\`\`

 \`\`\`python TypedDict theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from typing\_extensions import Annotated, TypedDict

 class Actor(TypedDict):
 name: str
 role: str

 class MovieDetails(TypedDict):
 title: str
 year: int
 cast: list\[Actor\]
 genres: list\[str\]
 budget: Annotated\[float \| None, ..., "Budget in millions USD"\]

 model\_with\_structure = model.with\_structured\_output(MovieDetails)
 \`\`\`


\\*\\*\\*

\## Advanced topics

\### Model profiles

 Model profiles require \`langchain>=1.1\`.

LangChain chat models can expose a dictionary of supported features and capabilities through a \`profile\` attribute:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
model.profile
\# {
\# "max\_input\_tokens": 400000,
\# "image\_inputs": True,
\# "reasoning\_output": True,
\# "tool\_calling": True,
\# ...
\# }
\`\`\`

Refer to the full set of fields in the \[API reference\](https://reference.langchain.com/python/langchain-core/language\_models/model\_profile/ModelProfile).

Much of the model profile data is powered by the \[models.dev\](https://github.com/sst/models.dev) project, an open source initiative that provides model capability data. These data are augmented with additional fields for purposes of use with LangChain. These augmentations are kept aligned with the upstream project as it evolves.

Model profile data allow applications to work around model capabilities dynamically. For example:

1\. \[Summarization middleware\](/oss/python/langchain/middleware/built-in#summarization) can trigger summarization based on a model's context window size.
2\. \[Structured output\](/oss/python/langchain/structured-output) strategies in \`create\_agent\` can be inferred automatically (e.g., by checking support for native structured output features).
3\. Model inputs can be gated based on supported \[modalities\](#multimodal) and maximum input tokens.
4\. \[Deep Agents Code\](/oss/python/deepagents/code) filters the \[interactive model switcher\](/oss/python/deepagents/code/providers#which-models-appear-in-the-switcher) to models whose profiles report \`tool\_calling\` support and text I/O, and displays context window sizes and capability flags in the selector detail view.

 Model profile data can be changed if it is missing, stale, or incorrect.

 \*\*Option 1 (quick fix)\*\*

 You can instantiate a chat model with any valid profile:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 custom\_profile = {
 "max\_input\_tokens": 100\_000,
 "tool\_calling": True,
 "structured\_output": True,
 # ...
 }
 model = init\_chat\_model("...", profile=custom\_profile)
 \`\`\`

 The \`profile\` is also a regular \`dict\` and can be updated in place. If the model instance is shared, consider using \`model\_copy\` to avoid mutating shared state.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 new\_profile = model.profile \| {"key": "value"}
 model.model\_copy(update={"profile": new\_profile})
 \`\`\`

 \*\*Option 2 (fix data upstream)\*\*

 The primary source for the data is the \[models.dev\](https://models.dev/) project. This data is merged with additional fields and overrides in LangChain \[integration packages\](/oss/python/integrations/providers/overview) and are shipped with those packages.

 Model profile data can be updated through the following process:

 1\. (If needed) update the source data at \[models.dev\](https://models.dev/) through a pull request to its \[repository on GitHub\](https://github.com/sst/models.dev).
 2\. (If needed) update additional fields and overrides in \`langchain\_/data/profile\_augmentations.toml\` through a pull request to the LangChain \[integration package\](/oss/python/integrations/providers/overview)\\\`.
 3\. Use the \[\`langchain-model-profiles\`\](https://pypi.org/project/langchain-model-profiles/) CLI tool to pull the latest data from \[models.dev\](https://models.dev/), merge in the augmentations and update the profile data:

 \`\`\`bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 pip install langchain-model-profiles
 \`\`\`

 \`\`\`bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 langchain-profiles refresh --provider  --data-dir
 \`\`\`

 This command:

 \\* Downloads the latest data for \`\` from models.dev
 \\* Merges augmentations from \`profile\_augmentations.toml\` in \`\`
 \\* Writes merged profiles to \`profiles.py\` in \`\`

 For example: from \[\`libs/partners/anthropic\`\](https://github.com/langchain-ai/langchain/tree/master/libs/partners/anthropic) in the \[LangChain monorepo\](https://github.com/langchain-ai/langchain):

 \`\`\`bash theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 uv run --with langchain-model-profiles --provider anthropic --data-dir langchain\_anthropic/data
 \`\`\`

 Model profiles are a beta feature. The format of a profile is subject to change.

\### Multimodal

Certain models can process and return non-textual data such as images, audio, and video. You can pass non-textual data to a model by providing \[content blocks\](/oss/python/langchain/messages#message-content).

 All LangChain chat models with underlying multimodal capabilities support:

 1\. Data in the cross-provider standard format (see \[our messages guide\](/oss/python/langchain/messages))
 2\. OpenAI \[chat completions\](https://platform.openai.com/docs/api-reference/chat) format
 3\. Any format that is native to that specific provider (e.g., Anthropic models accept Anthropic native format)

See the \[multimodal section\](/oss/python/langchain/messages#multimodal) of the messages guide for details.

Some models can return multimodal data as part of their response. If invoked to do so, the resulting \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) will have content blocks with multimodal types.

\`\`\`python Multimodal output theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke("Create a picture of a cat")
print(response.content\_blocks)
\# \[\
\# {"type": "text", "text": "Here's a picture of a cat"},\
\# {"type": "image", "base64": "...", "mime\_type": "image/jpeg"},\
\# \]
\`\`\`

See the \[integrations page\](/oss/python/integrations/providers/overview) for details on specific providers.

\### Reasoning

Many models are capable of performing multi-step reasoning to arrive at a conclusion. This involves breaking down complex problems into smaller, more manageable steps.

\*\*If supported by the underlying model,\*\* you can surface this reasoning process to better understand how the model arrived at its final answer.

 \`\`\`python Stream reasoning output theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 for chunk in model.stream("Why do parrots have colorful feathers?"):
 reasoning\_steps = \[r for r in chunk.content\_blocks if r\["type"\] == "reasoning"\]
 print(reasoning\_steps if reasoning\_steps else chunk.text)
 \`\`\`

 \`\`\`python Complete reasoning output theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 response = model.invoke("Why do parrots have colorful feathers?")
 reasoning\_steps = \[b for b in response.content\_blocks if b\["type"\] == "reasoning"\]
 print(" ".join(step\["reasoning"\] for step in reasoning\_steps))
 \`\`\`

Depending on the model, you can sometimes specify the level of effort it should put into reasoning. Similarly, you can request that the model turn off reasoning entirely. This may take the form of categorical "tiers" of reasoning (e.g., \`'low'\` or \`'high'\`) or integer token budgets.

For details, see the \[integrations page\](/oss/python/integrations/providers/overview) or \[reference\](https://reference.langchain.com/python/integrations/) for your respective chat model.

\### Local models

LangChain supports running models locally on your own hardware. This is useful for scenarios where either data privacy is critical, you want to invoke a custom model, or when you want to avoid the costs incurred when using a cloud-based model.

\[Ollama\](/oss/python/integrations/chat/ollama) is one of the easiest ways to run chat and embedding models locally.

\### Prompt caching

Many providers offer prompt caching features to reduce latency and cost on repeat processing of the same tokens. These features can be \*\*implicit\*\* or \*\*explicit\*\*:

\\* \*\*Implicit prompt caching:\*\* providers will automatically pass on cost savings if a request hits a cache. Examples: \[OpenAI\](/oss/python/integrations/chat/openai) and \[Gemini\](/oss/python/integrations/chat/google\_generative\_ai).
\\* \*\*Explicit caching:\*\* providers allow you to manually indicate cache points for greater control or to guarantee cost savings. Examples:
 \\* \[\`ChatOpenAI\`\](https://reference.langchain.com/python/langchain-openai/chat\_models/base/ChatOpenAI) (via \`prompt\_cache\_key\`)
 \\* Anthropic's \[\`AnthropicPromptCachingMiddleware\`\](/oss/python/integrations/chat/anthropic#prompt-caching)
 \\* \[Gemini\](https://reference.langchain.com/python/integrations/langchain\_google\_genai/).
 \\* \[AWS Bedrock\](/oss/python/integrations/chat/bedrock)

 Prompt caching is often only engaged above a minimum input token threshold. See \[provider pages\](/oss/python/integrations/chat) for details.

Cache usage will be reflected in the \[usage metadata\](/oss/python/langchain/messages#token-usage) of the model response.

\### Server-side tool use

Some providers support server-side \[tool-calling\](#tool-calling) loops: models can interact with web search, code interpreters, and other tools and analyze the results in a single conversational turn.

If a model invokes a tool server-side, the content of the response message will include content representing the invocation and result of the tool. Accessing the \[content blocks\](/oss/python/langchain/messages#standard-content-blocks) of the response will return the server-side tool calls and results in a provider-agnostic format:

\`\`\`python Invoke with server-side tool use theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model

model = init\_chat\_model("gpt-5.4-mini")

tool = {"type": "web\_search"}
model\_with\_tools = model.bind\_tools(\[tool\])

response = model\_with\_tools.invoke("What was a positive news story from today?")
print(response.content\_blocks)
\`\`\`

\`\`\`python Result expandable theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
\[\
 {\
 "type": "server\_tool\_call",\
 "name": "web\_search",\
 "args": {\
 "query": "positive news stories today",\
 "type": "search"\
 },\
 "id": "ws\_abc123"\
 },\
 {\
 "type": "server\_tool\_result",\
 "tool\_call\_id": "ws\_abc123",\
 "status": "success"\
 },\
 {\
 "type": "text",\
 "text": "Here are some positive news stories from today...",\
 "annotations": \[\
 {\
 "end\_index": 410,\
 "start\_index": 337,\
 "title": "article title",\
 "type": "citation",\
 "url": "..."\
 }\
 \]\
 }\
\]
\`\`\`

This represents a single conversational turn; there are no associated \[ToolMessage\](/oss/python/langchain/messages#tool-message) objects that need to be passed in as in client-side \[tool-calling\](#tool-calling).

See the \[integration page\](/oss/python/integrations/chat) for your given provider for available tools and usage details.

\### Rate limiting

Many chat model providers impose a limit on the number of invocations that can be made in a given time period. If you hit a rate limit, you will typically receive a rate limit error response from the provider, and will need to wait before making more requests.

To help manage rate limits, chat model integrations accept a \`rate\_limiter\` parameter that can be provided during initialization to control the rate at which requests are made.

 LangChain in comes with (an optional) built-in \[\`InMemoryRateLimiter\`\](https://reference.langchain.com/python/langchain-core/rate\_limiters/InMemoryRateLimiter). This limiter is thread safe and can be shared by multiple threads in the same process.

 \`\`\`python Define a rate limiter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain\_core.rate\_limiters import InMemoryRateLimiter

 rate\_limiter = InMemoryRateLimiter(
 requests\_per\_second=0.1, # 1 request every 10s
 check\_every\_n\_seconds=0.1, # Check every 100ms whether allowed to make a request
 max\_bucket\_size=10, # Controls the maximum burst size.
 )

 model = init\_chat\_model(
 model="gpt-5.4",
 model\_provider="openai",
 rate\_limiter=rate\_limiter # \[!code highlight\]
 )
 \`\`\`


 The provided rate limiter can only limit the number of requests per unit time. It will not help if you need to also limit based on the size of the requests.


\### Base URL and proxy settings

You can configure a custom base URL for providers that implement the OpenAI Chat Completions API.

 \`model\_provider="openai"\` (or direct \`ChatOpenAI\` usage) targets the official OpenAI API specification. Provider-specific fields from routers and proxies may not be extracted or preserved.

 For OpenRouter and LiteLLM, prefer the dedicated integrations:

 \\* \[OpenRouter via \`ChatOpenRouter\`\](/oss/python/integrations/chat/openrouter) (\`langchain-openrouter\`)
 \\* \[LiteLLM via \`ChatLiteLLM\` / \`ChatLiteLLMRouter\`\](/oss/python/integrations/chat) (\`langchain-litellm\`)

 Many model providers offer OpenAI-compatible APIs (e.g., \[Together AI\](https://www.together.ai/), \[vLLM\](https://github.com/vllm-project/vllm)). You can use \[\`init\_chat\_model\`\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model) with these providers by specifying the appropriate \`base\_url\` parameter:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model = init\_chat\_model(
 model="MODEL\_NAME",
 model\_provider="openai",
 base\_url="BASE\_URL",
 api\_key="YOUR\_API\_KEY",
 )
 \`\`\`


 When using direct chat model class instantiation, the parameter name may vary by provider. Check the respective \[reference\](/oss/python/integrations/providers/overview) for details.

 For deployments requiring HTTP proxies, some model integrations support proxy configuration:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain\_openai import ChatOpenAI

 model = ChatOpenAI(
 model="gpt-5.4",
 openai\_proxy="http://proxy.example.com:8080"
 )
 \`\`\`


 Proxy support varies by integration. Check the specific model provider's \[reference\](/oss/python/integrations/providers/overview) for proxy configuration options.


\### Log probabilities

Certain models can be configured to return token-level log probabilities representing the likelihood of a given token by setting the \`logprobs\` parameter when initializing the model:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
model = init\_chat\_model(
 model="gpt-5.4",
 model\_provider="openai"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
print(response.response\_metadata\["logprobs"\])
\`\`\`

\### Token usage

A number of model providers return token usage information as part of the invocation response. When available, this information will be included on the \[\`AIMessage\`\](https://reference.langchain.com/python/langchain-core/messages/ai/AIMessage) objects produced by the corresponding model. For more details, see the \[messages\](/oss/python/langchain/messages) guide.

 Some provider APIs, notably OpenAI and Azure OpenAI chat completions, require users opt-in to receiving token usage data in streaming contexts. See the \[streaming usage metadata\](/oss/python/integrations/chat/openai#streaming-usage-metadata) section of the integration guide for details.

You can track aggregate token counts across models in an application using either a callback or context manager, as shown below:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.chat\_models import init\_chat\_model
 from langchain\_core.callbacks import UsageMetadataCallbackHandler

 model\_1 = init\_chat\_model(model="gpt-5.4-mini")
 model\_2 = init\_chat\_model(model="claude-haiku-4-5-20251001")

 callback = UsageMetadataCallbackHandler()
 result\_1 = model\_1.invoke("Hello", config={"callbacks": \[callback\]})
 result\_2 = model\_2.invoke("Hello", config={"callbacks": \[callback\]})
 print(callback.usage\_metadata)
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 {
 'gpt-5.4-mini': {
 'input\_tokens': 8,
 'output\_tokens': 10,
 'total\_tokens': 18,
 'input\_token\_details': {'audio': 0, 'cache\_read': 0},
 'output\_token\_details': {'audio': 0, 'reasoning': 0}
 },
 'claude-haiku-4-5-20251001': {
 'input\_tokens': 8,
 'output\_tokens': 21,
 'total\_tokens': 29,
 'input\_token\_details': {'cache\_read': 0, 'cache\_creation': 0}
 }
 }
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from langchain.chat\_models import init\_chat\_model
 from langchain\_core.callbacks import get\_usage\_metadata\_callback

 model\_1 = init\_chat\_model(model="gpt-5.4-mini")
 model\_2 = init\_chat\_model(model="claude-haiku-4-5-20251001")

 with get\_usage\_metadata\_callback() as cb:
 model\_1.invoke("Hello")
 model\_2.invoke("Hello")
 print(cb.usage\_metadata)
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 {
 'gpt-5.4-mini': {
 'input\_tokens': 8,
 'output\_tokens': 10,
 'total\_tokens': 18,
 'input\_token\_details': {'audio': 0, 'cache\_read': 0},
 'output\_token\_details': {'audio': 0, 'reasoning': 0}
 },
 'claude-haiku-4-5-20251001': {
 'input\_tokens': 8,
 'output\_tokens': 21,
 'total\_tokens': 29,
 'input\_token\_details': {'cache\_read': 0, 'cache\_creation': 0}
 }
 }
 \`\`\`


\### Invocation config

When invoking a model, you can pass additional configuration through the \`config\` parameter using a \[\`RunnableConfig\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) dictionary. This provides run-time control over execution behavior, callbacks, and metadata tracking.

Common configuration options include:

\`\`\`python Invocation with config theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
response = model.invoke(
 "Tell me a joke",
 config={
 "run\_name": "joke\_generation", # Custom name for this run
 "tags": \["humor", "demo"\], # Tags for categorization
 "metadata": {"user\_id": "123"}, # Custom metadata
 "callbacks": \[my\_callback\_handler\], # Callback handlers
 }
)
\`\`\`

These configuration values are particularly useful when:

\\* Debugging with \[LangSmith\](/langsmith/home) tracing
\\* Implementing custom logging or monitoring
\\* Controlling resource usage in production
\\* Tracking invocations across complex pipelines

 Identifies this specific invocation in logs and traces. Not inherited by sub-calls.

 Labels inherited by all sub-calls for filtering and organization in debugging tools.

 Custom key-value pairs for tracking additional context, inherited by all sub-calls.

 Controls the maximum number of parallel calls when using \[\`batch()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch) or \[\`batch\_as\_completed()\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.batch\_as\_completed).

 Handlers for monitoring and responding to events during execution.

 Maximum recursion depth for chains to prevent infinite loops in complex pipelines.

 See full \[\`RunnableConfig\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) reference for all supported attributes.

\### Configurable models

You can also create a runtime-configurable model by specifying \[\`configurable\_fields\`\](https://reference.langchain.com/python/langchain\_core/language\_models/#langchain\_core.language\_models.chat\_models.BaseChatModel.configurable\_fields). If you don't specify a model value, then \`'model'\` and \`'model\_provider'\` will be configurable by default.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.chat\_models import init\_chat\_model

configurable\_model = init\_chat\_model(temperature=0)

configurable\_model.invoke(
 "what's your name",
 config={"configurable": {"model": "gpt-5-nano"}}, # Run with GPT-5-Nano
)
configurable\_model.invoke(
 "what's your name",
 config={"configurable": {"model": "claude-sonnet-4-6"}}, # Run with Claude
)
\`\`\`

 We can create a configurable model with default model values, specify which parameters are configurable, and add prefixes to configurable params:

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 first\_model = init\_chat\_model(
 model="gpt-5.4-mini",
 temperature=0,
 configurable\_fields=("model", "model\_provider", "temperature", "max\_tokens"),
 config\_prefix="first", # Useful when you have a chain with multiple models
 )

 first\_model.invoke("what's your name")
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 first\_model.invoke(
 "what's your name",
 config={
 "configurable": {
 "first\_model": "claude-sonnet-4-6",
 "first\_temperature": 0.5,
 "first\_max\_tokens": 100,
 }
 },
 )
 \`\`\`

 See the \[\`init\_chat\_model\`\](https://reference.langchain.com/python/langchain/chat\_models/base/init\_chat\_model) reference for more details on \`configurable\_fields\` and \`config\_prefix\`.

 We can call declarative operations like \`bind\_tools\`, \`with\_structured\_output\`, \`with\_configurable\`, etc. on a configurable model and chain a configurable model in the same way that we would a regularly instantiated chat model object.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from pydantic import BaseModel, Field

 class GetWeather(BaseModel):
 """Get the current weather in a given location"""

 location: str = Field(description="The city and state, e.g. San Francisco, CA")

 class GetPopulation(BaseModel):
 """Get the current population in a given location"""

 location: str = Field(description="The city and state, e.g. San Francisco, CA")

 model = init\_chat\_model(temperature=0)
 model\_with\_tools = model.bind\_tools(\[GetWeather, GetPopulation\])

 model\_with\_tools.invoke(
 "what's bigger in 2024 LA or NYC", config={"configurable": {"model": "gpt-5.4-mini"}}
 ).tool\_calls
 \`\`\`

 \`\`\`
 \[\
 {\
 'name': 'GetPopulation',\
 'args': {'location': 'Los Angeles, CA'},\
 'id': 'call\_Ga9m8FAArIyEjItHmztPYA22',\
 'type': 'tool\_call'\
 },\
 {\
 'name': 'GetPopulation',\
 'args': {'location': 'New York, NY'},\
 'id': 'call\_jh2dEvBaAHRaw5JUDthOs7rt',\
 'type': 'tool\_call'\
 }\
 \]
 \`\`\`

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 model\_with\_tools.invoke(
 "what's bigger in 2024 LA or NYC",
 config={"configurable": {"model": "claude-sonnet-4-6"}},
 ).tool\_calls
 \`\`\`

 \`\`\`
 \[\
 {\
 'name': 'GetPopulation',\
 'args': {'location': 'Los Angeles, CA'},\
 'id': 'toolu\_01JMufPf4F4t2zLj7miFeqXp',\
 'type': 'tool\_call'\
 },\
 {\
 'name': 'GetPopulation',\
 'args': {'location': 'New York City, NY'},\
 'id': 'toolu\_01RQBHcE8kEEbYTuuS8WqY1u',\
 'type': 'tool\_call'\
 }\
 \]
 \`\`\`

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/models.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-overview.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# LangChain overview

\> LangChain is an open source framework with a prebuilt agent architecture and integrations for any model or tool—so you can build agents that adapt as fast as the ecosystem evolves

Build completely custom agents and applications powered by LLMs in under 10 lines of code, with integrations for \[OpenAI, Anthropic, Google, and more\](/oss/python/integrations/providers/overview).
LangChain provides a prebuilt agent architecture and model integrations to help you get started quickly and seamlessly incorporate LLMs into your agents and applications.

 \*\*LangChain vs. LangGraph vs. Deep Agents\*\*

 Start with \[Deep Agents\](/oss/python/deepagents/overview/) for a "batteries-included" agent with features like automatic context compression, a virtual filesystem, and subagent-spawning. Deep Agents are built on LangChain \[agents\](/oss/python/langchain/agents/) which you can also use LangChain directly.

 Use \[LangGraph\](/oss/python/langgraph/overview), our low-level orchestration framework, for advanced needs combining deterministic and agentic workflows.

 Use \[LangSmith\](/langsmith/home) to trace, debug, and evaluate agents built with any of these frameworks. Follow the \[tracing quickstart\](/langsmith/trace-with-langchain) to get set up.

 The \[LangSmith Engine\](/langsmith/engine) detects issues in your LangChain agent traces and proposes fixes. You can open a pull request with the proposed fix directly from the Issues tab.

\##  Create an agent

 \`\`\`python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain "langchain\[openai\]"
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="openai:gpt-5.4",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Google Gemini theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain "langchain\[google-genai\]"
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="google\_genai:gemini-2.5-flash-lite",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Claude (Anthropic) theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain "langchain\[anthropic\]"
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="claude-sonnet-4-6",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain langchain-openrouter
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="openrouter:anthropic/claude-sonnet-4-6",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain langchain-fireworks
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain langchain-baseten
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="baseten:zai-org/GLM-5",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain langchain-ollama
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="ollama:devstral-2",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python Azure theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain "langchain\[openai\]"
 import os
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="azure\_openai:gpt-5.4",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 azure\_deployment=os.environ\["AZURE\_OPENAI\_DEPLOYMENT\_NAME"\],
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python AWS Bedrock theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain langchain-aws
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="anthropic.claude-3-5-sonnet-20240620-v1:0",
 model\_provider="bedrock\_converse",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

 \`\`\`python HuggingFace theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 # pip install -qU langchain "langchain\[huggingface\]"
 from langchain.agents import create\_agent

 def get\_weather(city: str) -> str:
 """Get weather for a given city."""
 return f"It's always sunny in {city}!"

 agent = create\_agent(
 model="microsoft/Phi-3-mini-4k-instruct",
 model\_provider="huggingface",
 tools=\[get\_weather\],
 system\_prompt="You are a helpful assistant",
 temperature=0.7,
 max\_tokens=1024,
 )

 result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's the weather in San Francisco?"}\]}
 )
 print(result\["messages"\]\[-1\].content\_blocks)
 \`\`\`

See the \[Installation instructions\](/oss/python/langchain/install) and \[Quickstart guide\](/oss/python/langchain/quickstart) to get started building your own agents and applications with LangChain.

 Use \[LangSmith\](/langsmith/home) to trace requests, debug agent behavior, and evaluate outputs. Set \`LANGSMITH\_TRACING=true\` and your API key to get started.

\##  Core benefits

 Different providers have unique APIs for interacting with models, including the format of responses. LangChain standardizes how you interact with models so that you can seamlessly swap providers and avoid lock-in.

 LangChain's agent abstraction is designed to be easy to get started with, letting you build a simple agent in under 10 lines of code. But it also provides enough flexibility to allow you to do all the context engineering your heart desires.

 LangChain's agents are built on top of LangGraph. This allows us to take advantage of LangGraph's durable execution, human-in-the-loop support, persistence, and more.

 Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.


\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/overview.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-retrieval.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Retrieval

Large Language Models (LLMs) are powerful, but they have two key limitations:

\\* \*\*Finite context\*\*—they can’t ingest entire corpora at once.
\\* \*\*Static knowledge\*\*—their training data is frozen at a point in time.

Retrieval addresses these problems by fetching relevant external knowledge at query time. This is the foundation of \*\*Retrieval-Augmented Generation (RAG)\*\*: enhancing an LLM’s answers with context-specific information.

\## Building a knowledge base

A \*\*knowledge base\*\* is a repository of documents or structured data used during retrieval.

If you need a custom knowledge base, you can use LangChain’s document loaders and vector stores to build one from your own data.

 If you already have a knowledge base (e.g., a SQL database, CRM, or internal documentation system), you do \*\*not\*\* need to rebuild it. You can:

 \\* Connect it as a \*\*tool\*\* for an agent in Agentic RAG.
 \\* Query it and supply the retrieved content as context to the LLM \[(2-Step RAG)\](#2-step-rag).

See the following tutorial to build a searchable knowledge base and minimal RAG workflow:

 Learn how to create a searchable knowledge base from your own data using LangChain’s document loaders, embeddings, and vector stores.
 In this tutorial, you’ll build a search engine over a PDF, enabling retrieval of passages relevant to a query. You’ll also implement a minimal RAG workflow on top of this engine to see how external knowledge can be integrated into LLM reasoning.

\### From retrieval to RAG

Retrieval allows LLMs to access relevant context at runtime. But most real-world applications go one step further: they \*\*integrate retrieval with generation\*\* to produce grounded, context-aware answers.

This is the core idea behind \*\*Retrieval-Augmented Generation (RAG)\*\*. The retrieval pipeline becomes a foundation for a broader system that combines search with generation.

\### Retrieval pipeline

A typical retrieval workflow looks like this:

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
flowchart LR
 S(\["Sources\
\
(Google Drive, Slack, Notion, etc.)"\]) --> L\[Document Loaders\]
 L --> A(\[Documents\])
 A --> B\[Split into chunks\]
 B --> C\[Turn into embeddings\]
 C --> D\[(Vector Store)\]
 Q(\[User Query\]) --> E\[Query embedding\]
 E --> D
 D --> F\[Retriever\]
 F --> G\[LLM uses retrieved info\]
 G --> H(\[Answer\])

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class S,Q trigger
 class L,B,C,E,F,G process
 class D output
 class A,H neutral
\`\`\`

Each component is modular: you can swap loaders, splitters, embeddings, or vector stores without rewriting the app’s logic.

\### Building blocks

 Ingest data from external sources (Google Drive, Slack, Notion, etc.), returning standardized \[\`Document\`\](https://reference.langchain.com/python/langchain-core/documents/base/Document) objects.

 Break large docs into smaller chunks that will be retrievable individually and fit within a model's context window.

 An embedding model turns text into a vector of numbers so that texts with similar meaning land close together in that vector space.

 Specialized databases for storing and searching embeddings.

 A retriever is an interface that returns documents given an unstructured query.


\## RAG architectures

RAG can be implemented in multiple ways, depending on your system's needs. We outline each type in the sections below.

\| Architecture \| Description \| Control \| Flexibility \| Latency \| Example Use Case \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \*\*2-Step RAG\*\* \| Retrieval always happens before generation. Simple and predictable \| ✅ High \| ❌ Low \| ⚡ Fast \| FAQs, documentation bots \|
\| \*\*Agentic RAG\*\* \| An LLM-powered agent decides \*when\* and \*how\* to retrieve during reasoning \| ❌ Low \| ✅ High \| ⏳ Variable \| Research assistants with access to multiple tools \|
\| \*\*Hybrid\*\* \| Combines characteristics of both approaches with validation steps \| ⚖️ Medium \| ⚖️ Medium \| ⏳ Variable \| Domain-specific Q\\&A with quality validation \|

 \*\*Latency\*\*: Latency is generally more \*\*predictable\*\* in \*\*2-Step RAG\*\*, as the maximum number of LLM calls is known and capped. This predictability assumes that LLM inference time is the dominant factor. However, real-world latency may also be affected by the performance of retrieval steps—such as API response times, network delays, or database queries—which can vary based on the tools and infrastructure in use.

\### 2-step RAG

In \*\*2-Step RAG\*\*, the retrieval step is always executed before the generation step. This architecture is straightforward and predictable, making it suitable for many applications where the retrieval of relevant documents is a clear prerequisite for generating an answer.

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[User Question\] --> B\["Retrieve Relevant Documents"\]
 B --> C\["Generate Answer"\]
 C --> D\[Return Answer to User\]

 %% Styling
 classDef startend fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:1.5px,color:#030710

 class A,D startend
 class B,C process
\`\`\`

 See how to build a Q\\&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
 This tutorial walks through two approaches:

 \\* A \*\*RAG agent\*\* that runs searches with a flexible tool—great for general-purpose use.
 \\* A \*\*2-step RAG\*\* chain that requires just one LLM call per query—fast and efficient for simpler tasks.

\### Agentic RAG

\*\*Agentic Retrieval-Augmented Generation (RAG)\*\* combines the strengths of Retrieval-Augmented Generation with agent-based reasoning. Instead of retrieving documents before answering, an agent (powered by an LLM) reasons step-by-step and decides \*\*when\*\* and \*\*how\*\* to retrieve information during the interaction.

 The only thing an agent needs to enable RAG behavior is access to one or more \*\*tools\*\* that can fetch external knowledge—such as documentation loaders, web APIs, or database queries.

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[User Input / Question\] --> B\["Agent (LLM)"\]
 B --> C{Need external info?}
 C -- Yes --> D\["Search using tool(s)"\]
 D --> H{Enough to answer?}
 H -- No --> B
 H -- Yes --> I\[Generate final answer\]
 C -- No --> I
 I --> J\[Return to user\]

 %% Dark-mode friendly styling
 classDef startend fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:1.5px,color:#030710

 class A,J startend
 class B,D,I process
 class C,H decision
\`\`\`

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
import requests
from langchain.tools import tool
from langchain.chat\_models import init\_chat\_model
from langchain.agents import create\_agent

@tool
def fetch\_url(url: str) -> str:
 """Fetch text content from a URL"""
 response = requests.get(url, timeout=10.0)
 response.raise\_for\_status()
 return response.text

system\_prompt = """\
Use fetch\_url when you need to fetch information from a web-page; quote relevant snippets.
"""

agent = create\_agent(
 model="claude-sonnet-4-6",
 tools=\[fetch\_url\], # A tool for retrieval \[!code highlight\]
 system\_prompt=system\_prompt,
)
\`\`\`

 This example implements an \*\*Agentic RAG system\*\* to assist users in querying LangGraph documentation. The agent begins by loading \[llms.txt\](https://llmstxt.org/), which lists available documentation URLs, and can then dynamically use a \`fetch\_documentation\` tool to retrieve and process the relevant content based on the user’s question.

 \`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 import requests
 from langchain.agents import create\_agent
 from langchain.messages import HumanMessage
 from langchain.tools import tool
 from markdownify import markdownify

 ALLOWED\_DOMAINS = \["https://langchain-ai.github.io/"\]
 LLMS\_TXT = 'https://langchain-ai.github.io/langgraph/llms.txt'

 @tool
 def fetch\_documentation(url: str) -> str: # \[!code highlight\]
 """Fetch and convert documentation from a URL"""
 if not any(url.startswith(domain) for domain in ALLOWED\_DOMAINS):
 return (
 "Error: URL not allowed. "
 f"Must start with one of: {', '.join(ALLOWED\_DOMAINS)}"
 )
 response = requests.get(url, timeout=10.0)
 response.raise\_for\_status()
 return markdownify(response.text)

 # We will fetch the content of llms.txt, so this can
 # be done ahead of time without requiring an LLM request.
 llms\_txt\_content = requests.get(LLMS\_TXT).text

 # System prompt for the agent
 system\_prompt = f"""
 You are an expert Python developer and technical assistant.
 Your primary role is to help users with questions about LangGraph and related tools.

 Instructions:

 1\. If a user asks a question you're unsure about—or one that likely involves API usage,
 behavior, or configuration—you MUST use the \`fetch\_documentation\` tool to consult the relevant docs.
 2\. When citing documentation, summarize clearly and include relevant context from the content.
 3\. Do not use any URLs outside of the allowed domain.
 4\. If a documentation fetch fails, tell the user and proceed with your best expert understanding.

 You can access official documentation from the following approved sources:

 {llms\_txt\_content}

 You MUST consult the documentation to get up to date documentation
 before answering a user's question about LangGraph.

 Your answers should be clear, concise, and technically accurate.
 """

 tools = \[fetch\_documentation\]

 model = init\_chat\_model("claude-sonnet-4-0", max\_tokens=32\_000)

 agent = create\_agent(
 model=model,
 tools=tools, # \[!code highlight\]
 system\_prompt=system\_prompt, # \[!code highlight\]
 name="Agentic RAG",
 )

 response = agent.invoke({
 'messages': \[\
 HumanMessage(content=(\
 "Write a short example of a langgraph agent using the "\
 "prebuilt create react agent. the agent should be able "\
 "to look up stock pricing information."\
 ))\
 \]
 })

 print(response\['messages'\]\[-1\].content)
 \`\`\`

 See how to build a Q\\&A chatbot that can answer questions grounded in your data using Retrieval-Augmented Generation.
 This tutorial walks through two approaches:

 \\* A \*\*RAG agent\*\* that runs searches with a flexible tool—great for general-purpose use.
 \\* A \*\*2-step RAG\*\* chain that requires just one LLM call per query—fast and efficient for simpler tasks.

\### Hybrid RAG

Hybrid RAG combines characteristics of both 2-Step and Agentic RAG. It introduces intermediate steps such as query preprocessing, retrieval validation, and post-generation checks. These systems offer more flexibility than fixed pipelines while maintaining some control over execution.

Typical components include:

\\* \*\*Query enhancement\*\*: Modify the input question to improve retrieval quality. This can involve rewriting unclear queries, generating multiple variations, or expanding queries with additional context.
\\* \*\*Retrieval validation\*\*: Evaluate whether retrieved documents are relevant and sufficient. If not, the system may refine the query and retrieve again.
\\* \*\*Answer validation\*\*: Check the generated answer for accuracy, completeness, and alignment with source content. If needed, the system can regenerate or revise the answer.

The architecture often supports multiple iterations between these steps:

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 A\[User Question\] --> B\[Query Enhancement\]
 B --> C\[Retrieve Documents\]
 C --> D{Sufficient Info?}
 D -- No --> E\[Refine Query\]
 E --> C
 D -- Yes --> F\[Generate Answer\]
 F --> G{Answer Quality OK?}
 G -- No --> H{Try Different Approach?}
 H -- Yes --> E
 H -- No --> I\[Return Best Answer\]
 G -- Yes --> I
 I --> J\[Return to User\]

 classDef startend fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef decision fill:#FDF3FF,stroke:#7E65AE,stroke-width:2px,color:#504B5F
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:1.5px,color:#030710

 class A,J startend
 class B,C,E,F,I process
 class D,G,H decision
\`\`\`

This architecture is suitable for:

\\* Applications with ambiguous or underspecified queries
\\* Systems that require validation or quality control steps
\\* Workflows involving multiple sources or iterative refinement

 An example of \*\*Hybrid RAG\*\* that combines agentic reasoning with retrieval and self-correction.

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/retrieval.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .firecrawl/docs.langchain.com-oss-python-langchain-tools.md.md
````markdown
\> ## Documentation Index
\> Fetch the complete documentation index at: https://docs.langchain.com/llms.txt
\> Use this file to discover all available pages before exploring further.

\# Tools

Tools extend what \[agents\](/oss/python/langchain/agents) can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world.

Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a \[chat model\](/oss/python/langchain/models). The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.

 For details on how models handle tool calls, see \[Tool calling\](/oss/python/langchain/models#tool-calling). Trace tool calls and debug errors with \[LangSmith\](https://smith.langchain.com?utm\_source=docs\\&utm\_medium=cta\\&utm\_campaign=langsmith-signup\\&utm\_content=oss-langchain-tools)—follow the \[tracing quickstart\](/langsmith/trace-with-langchain) to get set up.

\## Create tools

\### Basic tool definition

The simplest way to create a tool is with the \[\`@tool\`\](https://reference.langchain.com/python/langchain-core/tools/convert/tool) decorator. By default, the function's docstring becomes the tool's description that helps the model understand when to use it:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool

@tool
def search\_database(query: str, limit: int = 10) -> str:
 """Search the customer database for records matching the query.

 Args:
 query: Search terms to look for
 limit: Maximum number of results to return
 """
 return f"Found {limit} results for '{query}'"
\`\`\`

Type hints are \*\*required\*\* as they define the tool's input schema. The docstring should be informative and concise to help the model understand the tool's purpose.

 \*\*Server-side tool use:\*\* Some chat models feature built-in tools (web search, code interpreters) that are executed server-side. See \[Server-side tool use\](#server-side-tool-use) for details.

 Prefer \`snake\_case\` for tool names (e.g., \`web\_search\` instead of \`Web Search\`). Some model providers have issues with or reject names containing spaces or special characters with errors. Sticking to alphanumeric characters, underscores, and hyphens helps to improve compatibility across providers.

\### Customize tool properties

\#### Custom tool name

By default, the tool name comes from the function name. Override it when you need something more descriptive:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
@tool("web\_search") # Custom name
def search(query: str) -> str:
 """Search the web for information."""
 return f"Results for: {query}"

print(search.name) # web\_search
\`\`\`

\#### Custom tool description

Override the auto-generated tool description for clearer model guidance:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
 """Evaluate mathematical expressions."""
 return str(eval(expression))
\`\`\`

\### Advanced schema definition

Define complex inputs with Pydantic models or JSON schemas:

 \`\`\`python Pydantic model theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from pydantic import BaseModel, Field
 from typing import Literal

 class WeatherInput(BaseModel):
 """Input for weather queries."""
 location: str = Field(description="City name or coordinates")
 units: Literal\["celsius", "fahrenheit"\] = Field(
 default="celsius",
 description="Temperature unit preference"
 )
 include\_forecast: bool = Field(
 default=False,
 description="Include 5-day forecast"
 )

 @tool(args\_schema=WeatherInput)
 def get\_weather(location: str, units: str = "celsius", include\_forecast: bool = False) -> str:
 """Get current weather and optional forecast."""
 temp = 22 if units == "celsius" else 72
 result = f"Current weather in {location}: {temp} degrees {units\[0\].upper()}"
 if include\_forecast:
 result += "\\nNext 5 days: Sunny"
 return result
 \`\`\`

 \`\`\`python JSON Schema theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 weather\_schema = {
 "type": "object",
 "properties": {
 "location": {"type": "string"},
 "units": {"type": "string"},
 "include\_forecast": {"type": "boolean"}
 },
 "required": \["location", "units", "include\_forecast"\]
 }

 @tool(args\_schema=weather\_schema)
 def get\_weather(location: str, units: str = "celsius", include\_forecast: bool = False) -> str:
 """Get current weather and optional forecast."""
 temp = 22 if units == "celsius" else 72
 result = f"Current weather in {location}: {temp} degrees {units\[0\].upper()}"
 if include\_forecast:
 result += "\\nNext 5 days: Sunny"
 return result
 \`\`\`

\### Reserved argument names

The following parameter names are reserved and cannot be used as tool arguments. Using these names will cause runtime errors.

\| Parameter name \| Purpose \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \`config\` \| Reserved for passing \`RunnableConfig\` to tools internally \|
\| \`runtime\` \| Reserved for \`ToolRuntime\` parameter (accessing state, context, store) \|

To access runtime information, use the \[\`ToolRuntime\`\](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime) parameter instead of naming your own arguments \`config\` or \`runtime\`.

\## Access context

Tools are most powerful when they can access runtime information like conversation history, user data, and persistent memory. This section covers how to access and update this information from within your tools.

Tools can access runtime information through the \[\`ToolRuntime\`\](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime) parameter, which provides:

\| Component \| Description \| Use case \|
\| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \| \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \|
\| \*\*State\*\* \| Short-term memory - mutable data that exists for the current conversation (messages, counters, custom fields) \| Access conversation history, track tool call counts \|
\| \*\*Context\*\* \| Immutable configuration passed at invocation time (user IDs, session info) \| Personalize responses based on user identity \|
\| \*\*Store\*\* \| Long-term memory - persistent data that survives across conversations \| Save user preferences, maintain knowledge base \|
\| \*\*Stream Writer\*\* \| Emit real-time updates during tool execution \| Show progress for long-running operations \|
\| \*\*Execution Info\*\* \| Identity and retry information for the current execution (thread ID, run ID, attempt number) \| Access thread/run IDs, adjust behavior based on retry state \|
\| \*\*Server Info\*\* \| Server-specific metadata when running on LangGraph Server (assistant ID, graph ID, authenticated user) \| Access assistant ID, graph ID, or authenticated user info \|
\| \*\*Config\*\* \| \[\`RunnableConfig\`\](https://reference.langchain.com/python/langchain-core/runnables/config/RunnableConfig) for the execution \| Access callbacks, tags, and metadata \|
\| \*\*Tool Call ID\*\* \| Unique identifier for the current tool invocation \| Correlate tool calls for logs and model invocations \|

\`\`\`mermaid theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
graph LR
 %% Runtime Context
 subgraph "🔧 Tool Runtime Context"
 A\[Tool Call\] --> B\[ToolRuntime\]
 B --> C\[State Access\]
 B --> D\[Context Access\]
 B --> E\[Store Access\]
 B --> F\[Stream Writer\]
 end

 %% Available Resources
 subgraph "📊 Available Resources"
 C --> G\[Messages\]
 C --> H\[Custom State\]
 D --> I\[User ID\]
 D --> J\[Session Info\]
 E --> K\[Long-term Memory\]
 E --> L\[User Preferences\]
 end

 %% Tool Capabilities
 subgraph "⚡ Enhanced Tool Capabilities"
 M\[Context-Aware Tools\]
 N\[Stateful Tools\]
 O\[Memory-Enabled Tools\]
 P\[Streaming Tools\]
 end

 %% Connections
 G --> M
 H --> N
 I --> M
 J --> M
 K --> O
 L --> O
 F --> P

 classDef trigger fill:#F6FFDB,stroke:#6E8900,stroke-width:2px,color:#2E3900
 classDef process fill:#E5F4FF,stroke:#006DDD,stroke-width:2px,color:#030710
 classDef output fill:#EBD0F0,stroke:#885270,stroke-width:2px,color:#441E33
 classDef neutral fill:#F2FAFF,stroke:#40668D,stroke-width:2px,color:#2F4B68

 class A trigger
 class B,C,D,E,F process
 class G,H,I,J,K,L neutral
 class M,N,O,P output
\`\`\`

\### Short-term memory (State)

State represents short-term memory that exists for the duration of a conversation. It includes the message history and any custom fields you define in your \[graph state\](/oss/python/langgraph/graph-api#state).

 Add \`runtime: ToolRuntime\` to your tool signature to access state. This parameter is automatically injected and hidden from the LLM - it won't appear in the tool's schema.

\#### Access state

Tools can access the current conversation state using \`runtime.state\`:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get\_last\_user\_message(runtime: ToolRuntime) -> str:
 """Get the most recent message from the user."""
 messages = runtime.state\["messages"\]

 # Find the last human message
 for message in reversed(messages):
 if isinstance(message, HumanMessage):
 return message.content

 return "No user messages found"

\# Access custom state fields
@tool
def get\_user\_preference(
 pref\_name: str,
 runtime: ToolRuntime
) -\> str:
 """Get a user preference value."""
 preferences = runtime.state.get("user\_preferences", {})
 return preferences.get(pref\_name, "Not set")
\`\`\`

 The \`runtime\` parameter is hidden from the model. For the example above, the model only sees \`pref\_name\` in the tool schema.

\#### Update state

Use \[\`Command\`\](https://reference.langchain.com/python/langgraph/types/Command) to update the agent's state. This is useful for tools that need to update custom state fields.
Include a \`ToolMessage\` in the update so the model can see the result of the tool call:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

class CustomState(AgentState):
 user\_name: str

@tool
def set\_user\_name(new\_name: str, runtime: ToolRuntime\[None, CustomState\]) -> Command:
 """Set the user's name in the conversation state."""
 return Command(
 update={
 "user\_name": new\_name,
 "messages": \[\
 ToolMessage(\
 content=f"User name set to {new\_name}.",\
 tool\_call\_id=runtime.tool\_call\_id,\
 )\
 \],
 }
 )
\`\`\`

 When tools update state variables, consider defining a \[reducer\](/oss/python/langgraph/graph-api#reducers) for those fields. Since LLMs can call multiple tools in parallel, a reducer determines how to resolve conflicts when the same state field is updated by concurrent tool calls.

\### Context

Context provides immutable configuration data that is passed at invocation time. Use it for user IDs, session details, or application-specific settings that shouldn't change during a conversation.

Access context through \`runtime.context\`:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from dataclasses import dataclass
from langchain\_openai import ChatOpenAI
from langchain.agents import create\_agent
from langchain.tools import tool, ToolRuntime

USER\_DATABASE = {
 "user123": {
 "name": "Alice Johnson",
 "account\_type": "Premium",
 "balance": 5000,
 "email": "alice@example.com"
 },
 "user456": {
 "name": "Bob Smith",
 "account\_type": "Standard",
 "balance": 1200,
 "email": "bob@example.com"
 }
}

@dataclass
class UserContext:
 user\_id: str

@tool
def get\_account\_info(runtime: ToolRuntime\[UserContext\]) -> str:
 """Get the current user's account information."""
 user\_id = runtime.context.user\_id

 if user\_id in USER\_DATABASE:
 user = USER\_DATABASE\[user\_id\]
 return f"Account holder: {user\['name'\]}\\nType: {user\['account\_type'\]}\\nBalance: ${user\['balance'\]}"
 return "User not found"

model = ChatOpenAI(model="gpt-5.4")
agent = create\_agent(
 model,
 tools=\[get\_account\_info\],
 context\_schema=UserContext,
 system\_prompt="You are a financial assistant."
)

result = agent.invoke(
 {"messages": \[{"role": "user", "content": "What's my current balance?"}\]},
 context=UserContext(user\_id="user123")
)
\`\`\`

\### Long-term memory (Store)

The \[\`BaseStore\`\](https://reference.langchain.com/python/langchain-core/stores/BaseStore) provides persistent storage that survives across conversations. Unlike state (short-term memory), data saved to the store remains available in future sessions.

Access the store through \`runtime.store\`. The store uses a namespace/key pattern to organize data:

 For production deployments, use a persistent store implementation like \[\`PostgresStore\`\](https://reference.langchain.com/python/langgraph/store/#langgraph.store.postgres.PostgresStore) instead of \`InMemoryStore\`. See the \[memory documentation\](/oss/python/langgraph/add-memory) for setup details.

\`\`\`python expandable theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create\_agent
from langchain.tools import tool, ToolRuntime
from langchain\_openai import ChatOpenAI

\# Access memory
@tool
def get\_user\_info(user\_id: str, runtime: ToolRuntime) -> str:
 """Look up user info."""
 store = runtime.store
 user\_info = store.get(("users",), user\_id)
 return str(user\_info.value) if user\_info else "Unknown user"

\# Update memory
@tool
def save\_user\_info(user\_id: str, user\_info: dict\[str, Any\], runtime: ToolRuntime) -> str:
 """Save user info."""
 store = runtime.store
 store.put(("users",), user\_id, user\_info)
 return "Successfully saved user info."

model = ChatOpenAI(model="gpt-5.4")

store = InMemoryStore()
agent = create\_agent(
 model,
 tools=\[get\_user\_info, save\_user\_info\],
 store=store
)

\# First session: save user info
agent.invoke({
 "messages": \[{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}\]
})

\# Second session: get user info
agent.invoke({
 "messages": \[{"role": "user", "content": "Get user info for user with id 'abc123'"}\]
})
\# Here is the user info for user with ID "abc123":
\# - Name: Foo
\# - Age: 25
\# - Email: foo@langchain.dev
\`\`\`

\### Stream writer

Stream real-time updates from tools during execution. This is useful for providing progress feedback to users during long-running operations.

Use \`runtime.stream\_writer\` to emit custom updates:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool, ToolRuntime

@tool
def get\_weather(city: str, runtime: ToolRuntime) -> str:
 """Get weather for a given city."""
 writer = runtime.stream\_writer

 # Stream custom updates as the tool executes
 writer(f"Looking up data for city: {city}")
 writer(f"Acquired data for city: {city}")

 return f"It's always sunny in {city}!"
\`\`\`

 If you use \`runtime.stream\_writer\` inside your tool, the tool must be invoked within a LangGraph execution context. See \[Streaming\](/oss/python/langchain/streaming) for more details.

\### Execution info

Access thread ID, run ID, and retry state from within a tool via \`runtime.execution\_info\`:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool, ToolRuntime

@tool
def log\_execution\_context(runtime: ToolRuntime) -> str:
 """Log execution identity information."""
 info = runtime.execution\_info
 print(f"Thread: {info.thread\_id}, Run: {info.run\_id}") # \[!code highlight\]
 print(f"Attempt: {info.node\_attempt}")
 return "done"
\`\`\`

 Requires \`deepagents>=0.5.0\` (or \`langgraph>=1.1.5\`).

\### Server info

When your tool runs on LangGraph Server, access the assistant ID, graph ID, and authenticated user via \`runtime.server\_info\`:

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool, ToolRuntime

@tool
def get\_assistant\_scoped\_data(runtime: ToolRuntime) -> str:
 """Fetch data scoped to the current assistant."""
 server = runtime.server\_info
 if server is not None:
 print(f"Assistant: {server.assistant\_id}, Graph: {server.graph\_id}") # \[!code highlight\]
 if server.user is not None:
 print(f"User: {server.user.identity}") # \[!code highlight\]
 return "done"
\`\`\`

\`server\_info\` is \`None\` when the tool is not running on LangGraph Server (e.g., during local development or testing).

 Requires \`deepagents>=0.5.0\` (or \`langgraph>=1.1.5\`).

\## Tool execution

In LangChain, tools are used by agents (for example via \[\`create\_agent\`\](https://reference.langchain.com/python/langchain/agents/factory/create\_agent)) and tool error handling is configured through \[middleware\](/oss/python/langchain/middleware).

For LangGraph workflows, tool execution is handled by \[\`ToolNode\`\](https://reference.langchain.com/python/langgraph/agents/#langgraph.prebuilt.tool\_node.ToolNode). See \[ToolNode\](/oss/python/langgraph/workflows-agents#toolnode).

\### Tool return values

You can choose different return values for your tools:

\\* Return a \`string\` for human-readable results.
\\* Return an \`object\` for structured results the model should parse.
\\* Return a \`Command\` with optional message when you need to write to state.

\#### Return a string

Return a string when the tool should provide plain text for the model to read and use in its next response.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool

@tool
def get\_weather(city: str) -> str:
 """Get weather for a city."""
 return f"It is currently sunny in {city}."
\`\`\`

Behavior:

\\* The return value is converted to a \`ToolMessage\`.
\\* The model sees that text and decides what to do next.
\\* No agent state fields are changed unless the model or another tool does so later.

Use this when the result is naturally human-readable text.

\#### Return an object

Return an object (for example, a \`dict\`) when your tool produces structured data that the model should inspect.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool

@tool
def get\_weather\_data(city: str) -> dict:
 """Get structured weather data for a city."""
 return {
 "city": city,
 "temperature\_c": 22,
 "conditions": "sunny",
 }
\`\`\`

Behavior:

\\* The object is serialized and sent back as tool output.
\\* The model can read specific fields and reason over them.
\\* Like string returns, this does not directly update graph state.

Use this when downstream reasoning benefits from explicit fields instead of free-form text.

\#### Return a Command

Return a \[\`Command\`\](https://reference.langchain.com/python/langgraph/types/Command) when the tool needs to update graph state (for example, setting user preferences or app state).
You can return a \`Command\` with or without including a \`ToolMessage\`.
If the model needs to see that the tool succeeded (for example, to confirm a preference change), include a \`ToolMessage\` in the update, using \`runtime.tool\_call\_id\` for the \`tool\_call\_id\` parameter.

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool
def set\_language(language: str, runtime: ToolRuntime) -> Command:
 """Set the preferred response language."""
 return Command(
 update={
 "preferred\_language": language,
 "messages": \[\
 ToolMessage(\
 content=f"Language set to {language}.",\
 tool\_call\_id=runtime.tool\_call\_id,\
 )\
 \],
 }
 )
\`\`\`

Behavior:

\\* The command updates state using \`update\`.
\\* Updated state is available to subsequent steps in the same run.
\\* Use reducers for fields that may be updated by parallel tool calls.

Use this when the tool is not just returning data, but also mutating agent state.

\### Error handling

Handle tool errors using LangChain agent \[middleware\](/oss/python/langchain/middleware) to retry failed tool calls or return custom error messages:

 \`\`\`python Google theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="google\_genai:gemini-3.1-pro-preview",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python OpenAI theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="openai:gpt-5.4",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python Anthropic theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="anthropic:claude-sonnet-4-6",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python OpenRouter theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="openrouter:anthropic/claude-sonnet-4-6",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python Fireworks theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="fireworks:accounts/fireworks/models/qwen3p5-397b-a17b",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python Baseten theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="baseten:zai-org/GLM-5",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

 \`\`\`python Ollama theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
 from collections.abc import Callable

 from langchain.agents import create\_agent
 from langchain.agents.middleware import wrap\_tool\_call
 from langchain.messages import ToolMessage
 from langchain.tools.tool\_node import ToolCallRequest

 @wrap\_tool\_call
 def handle\_tool\_errors(
 request: ToolCallRequest,
 handler: Callable\[\[ToolCallRequest\], ToolMessage\],
 ) -\> ToolMessage:
 """Convert tool exceptions into ToolMessages the model can handle."""
 try:
 return handler(request)
 except Exception as e:
 return ToolMessage(
 content=f"Tool error: Please check your input and try again. ({e})",
 tool\_call\_id=request.tool\_call\["id"\],
 )

 agent = create\_agent(
 model="ollama:devstral-2",
 tools=\[\],
 middleware=\[handle\_tool\_errors\],
 )
 \`\`\`

\### State injection

Tools can access the current graph state through \[\`ToolRuntime\`\](https://reference.langchain.com/python/langchain/tools/#langchain.tools.ToolRuntime):

\`\`\`python theme={"theme":{"light":"catppuccin-latte","dark":"catppuccin-mocha"}}
from langchain.tools import tool, ToolRuntime

@tool
def get\_message\_count(runtime: ToolRuntime) -> str:
 """Get the number of messages in the conversation."""
 messages = runtime.state\["messages"\]
 return f"There are {len(messages)} messages."
\`\`\`

For more details on accessing state, context, and long-term memory from tools, see \[Access context\](#access-context).

\## Prebuilt tools

LangChain provides a large collection of prebuilt tools and toolkits for common tasks like web search, code interpretation, database access, and more. These ready-to-use tools can be directly integrated into your agents without writing custom code.

See the \[tools and toolkits\](/oss/python/integrations/tools) integration page for a complete list of available tools organized by category.

\## Server-side tool use

Some chat models feature built-in tools that are executed server-side by the model provider. These include capabilities like web search and code interpreters that don't require you to define or host the tool logic.

Refer to the individual \[chat model integration pages\](/oss/python/integrations/providers) and the \[tool calling documentation\](/oss/python/langchain/models#server-side-tool-use) for details on enabling and using these built-in tools.

\\*\\*\\*

\[Connect these docs\](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.

\[Edit this page on GitHub\](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/tools.mdx) or \[file an issue\](https://github.com/langchain-ai/docs/issues/new/choose).
````

## File: .gitignore
````
ai-service/.env
````

## File: .omc/state/agent-replay-b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27.jsonl
````
{"t":0,"agent":"a6b658f","agent_type":"explore","event":"agent_start","parent_mode":"none"}
{"t":0,"agent":"a6b658f","agent_type":"explore","event":"agent_stop","success":true,"duration_ms":380524}
{"t":0,"agent":"aa85513","agent_type":"planner","event":"agent_start","parent_mode":"none"}
{"t":0,"agent":"aa85513","agent_type":"planner","event":"agent_stop","success":true,"duration_ms":210006}
````

## File: .omc/state/agent-replay-dacf2d60-50e5-4603-9c6e-db62701af3ee.jsonl
````
{"t":0,"agent":"system","event":"keyword_detected","keyword":"tdd"}
{"t":0,"agent":"system","event":"skill_invoked","skill_name":"pua:pua"}
{"t":0,"agent":"system","event":"skill_invoked","skill_name":"think"}
{"t":0,"agent":"system","event":"skill_invoked","skill_name":"tdd"}
````

## File: .omc/state/hud-stdin-cache.json
````json
{"session_id":"dacf2d60-50e5-4603-9c6e-db62701af3ee","transcript_path":"C:\\Users\\14253\\.claude\\projects\\C--Users-14253-Desktop-ai-hiking\\dacf2d60-50e5-4603-9c6e-db62701af3ee.jsonl","cwd":"C:\\Users\\14253\\Desktop\\ai-hiking","effort":{"level":"max"},"session_name":"Fix linked Feishu knowledge base sync","model":{"id":"deepseek-v4-pro[1m]","display_name":"deepseek-v4-pro[1m]"},"workspace":{"current_dir":"C:\\Users\\14253\\Desktop\\ai-hiking","project_dir":"C:\\Users\\14253\\Desktop\\ai-hiking","added_dirs":[]},"version":"2.1.143","output_style":{"name":"default"},"cost":{"total_cost_usd":2.1742560000000006,"total_duration_ms":863756,"total_api_duration_ms":509831,"total_lines_added":0,"total_lines_removed":0},"context_window":{"total_input_tokens":109723,"total_output_tokens":532,"context_window_size":1000000,"current_usage":{"input_tokens":1435,"output_tokens":532,"cache_creation_input_tokens":0,"cache_read_input_tokens":108288},"used_percentage":11,"remaining_percentage":89},"exceeds_200k_tokens":false,"fast_mode":false,"thinking":{"enabled":true}}
````

## File: .omc/state/last-tool-error.json
````json
{
  "tool_name": "Bash",
  "tool_input_preview": "{\"command\":\"lark-cli docs +fetch-v2 --doc \\\"SREndflzEonZnIxyGBEcLtEmnuQ\\\" --format json 2>&1\",\"timeout\":30000,\"description\":\"Test lark-cli new vs old doc fetch API\"}",
  "error": "Exit code 1\nUsage:\n  lark-cli docs [command]\n\nAvailable Commands:\n  +create            Create a Lark document\n  +fetch             Fetch Lark document content\n  +media-download    Download document media or whiteboard thumbnail (auto-detects extension)\n  +media-insert      Insert a local image or file into a Lark document (4-step orchestration + auto-rollback); appends to end by default, or inserts relative to a text selection with --selection-with-ellipsis\n  +media-preview     Preview document ...",
  "timestamp": "2026-05-17T12:34:09.799Z",
  "retry_count": 1
}
````

## File: .omc/state/mission-state.json
````json
{
  "updatedAt": "2026-05-16T09:11:23.605Z",
  "missions": [
    {
      "id": "session:b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27:none",
      "source": "session",
      "name": "none",
      "objective": "Session mission",
      "createdAt": "2026-05-16T08:57:03.229Z",
      "updatedAt": "2026-05-16T09:11:23.605Z",
      "status": "done",
      "workerCount": 2,
      "taskCounts": {
        "total": 2,
        "pending": 0,
        "blocked": 0,
        "inProgress": 0,
        "completed": 2,
        "failed": 0
      },
      "agents": [
        {
          "name": "explore:a6b658f",
          "role": "explore",
          "ownership": "a6b658f66665d78c1",
          "status": "done",
          "currentStep": null,
          "latestUpdate": "completed",
          "completedSummary": null,
          "updatedAt": "2026-05-16T09:03:23.753Z"
        },
        {
          "name": "planner:aa85513",
          "role": "planner",
          "ownership": "aa85513c5b47798da",
          "status": "done",
          "currentStep": null,
          "latestUpdate": "completed",
          "completedSummary": null,
          "updatedAt": "2026-05-16T09:11:23.605Z"
        }
      ],
      "timeline": [
        {
          "id": "session-start:a6b658f66665d78c1:2026-05-16T08:57:03.229Z",
          "at": "2026-05-16T08:57:03.229Z",
          "kind": "update",
          "agent": "explore:a6b658f",
          "detail": "started explore:a6b658f",
          "sourceKey": "session-start:a6b658f66665d78c1"
        },
        {
          "id": "session-stop:a6b658f66665d78c1:2026-05-16T09:03:23.753Z",
          "at": "2026-05-16T09:03:23.753Z",
          "kind": "completion",
          "agent": "explore:a6b658f",
          "detail": "completed",
          "sourceKey": "session-stop:a6b658f66665d78c1"
        },
        {
          "id": "session-start:aa85513c5b47798da:2026-05-16T09:07:53.599Z",
          "at": "2026-05-16T09:07:53.599Z",
          "kind": "update",
          "agent": "planner:aa85513",
          "detail": "started planner:aa85513",
          "sourceKey": "session-start:aa85513c5b47798da"
        },
        {
          "id": "session-stop:aa85513c5b47798da:2026-05-16T09:11:23.605Z",
          "at": "2026-05-16T09:11:23.605Z",
          "kind": "completion",
          "agent": "planner:aa85513",
          "detail": "completed",
          "sourceKey": "session-stop:aa85513c5b47798da"
        }
      ]
    }
  ]
}
````

## File: .omc/state/sessions/02f4062a-21d8-44df-95cf-5ef3f0ec57bb/hud-state.json
````json
{
  "timestamp": "2026-05-15T19:06:00.573Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-15T19:05:11.728Z",
  "sessionId": "02f4062a-21d8-44df-95cf-5ef3f0ec57bb"
}
````

## File: .omc/state/sessions/02f4062a-21d8-44df-95cf-5ef3f0ec57bb/session-started.json
````json
{
  "session_id": "02f4062a-21d8-44df-95cf-5ef3f0ec57bb",
  "started_at": "2026-05-15T19:05:11.496Z",
  "cwd": "C:\\Users\\14253\\Desktop\\ai-hiking",
  "pid": 42484
}
````

## File: .omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
````json
{
  "timestamp": "2026-05-16T08:51:16.208Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-16T08:49:32.702Z",
  "sessionId": "b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27"
}
````

## File: .omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/session-started.json
````json
{
  "session_id": "b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27",
  "started_at": "2026-05-16T08:49:31.967Z",
  "cwd": "C:\\Users\\14253\\Desktop\\ai-hiking",
  "pid": 33828
}
````

## File: .omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/hud-state.json
````json
{
  "timestamp": "2026-05-17T12:27:03.588Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-17T12:26:08.205Z",
  "sessionId": "dacf2d60-50e5-4603-9c6e-db62701af3ee"
}
````

## File: .omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/session-started.json
````json
{
  "session_id": "dacf2d60-50e5-4603-9c6e-db62701af3ee",
  "started_at": "2026-05-17T12:26:07.486Z",
  "cwd": "C:\\Users\\14253\\Desktop\\ai-hiking",
  "pid": 21832
}
````

## File: .omc/state/subagent-tracking.json
````json
{
  "agents": [
    {
      "agent_id": "a6b658f66665d78c1",
      "agent_type": "oh-my-claudecode:explore",
      "started_at": "2026-05-16T08:57:03.229Z",
      "parent_mode": "none",
      "status": "completed",
      "completed_at": "2026-05-16T09:03:23.753Z",
      "duration_ms": 380524
    },
    {
      "agent_id": "aa85513c5b47798da",
      "agent_type": "oh-my-claudecode:planner",
      "started_at": "2026-05-16T09:07:53.599Z",
      "parent_mode": "none",
      "status": "completed",
      "completed_at": "2026-05-16T09:11:23.605Z",
      "duration_ms": 210006
    }
  ],
  "total_spawned": 2,
  "total_completed": 2,
  "total_failed": 0,
  "last_updated": "2026-05-16T09:11:23.717Z"
}
````

## File: .omx/logs/omx-2026-05-16.jsonl
````
{"event":"session_start","session_id":"019e30a2-25ee-7121-a02a-2e915835f249","native_session_id":"019e30a2-25ee-7121-a02a-2e915835f249","pid":21684,"timestamp":"2026-05-16T11:53:22.283Z","_ts":"2026-05-16T11:53:22.286Z"}
{"event":"session_start","session_id":"019e30a2-0d92-7722-895b-3bc4c436195e","native_session_id":"019e30a2-0d92-7722-895b-3bc4c436195e","pid":25872,"timestamp":"2026-05-16T11:53:24.157Z","_ts":"2026-05-16T11:53:24.160Z"}
{"event":"session_start","session_id":"019e3104-76e4-7ac3-901b-8f37bd81ff00","native_session_id":"019e3104-76e4-7ac3-901b-8f37bd81ff00","pid":32304,"timestamp":"2026-05-16T13:40:52.295Z","_ts":"2026-05-16T13:40:52.298Z"}
{"event":"session_start","session_id":"019e3104-de0e-7620-8ea6-3c5b5209452d","native_session_id":"019e3104-de0e-7620-8ea6-3c5b5209452d","pid":33052,"timestamp":"2026-05-16T13:41:23.862Z","_ts":"2026-05-16T13:41:23.865Z"}
{"event":"session_start","session_id":"019e310e-7f8f-7600-982d-f9d8b8041eb0","native_session_id":"019e310e-7f8f-7600-982d-f9d8b8041eb0","pid":37328,"timestamp":"2026-05-16T13:51:55.968Z","_ts":"2026-05-16T13:51:55.971Z"}
{"event":"session_start","session_id":"019e3120-a1aa-7c92-93bd-6868d5eec123","native_session_id":"019e3120-a1aa-7c92-93bd-6868d5eec123","pid":21632,"timestamp":"2026-05-16T14:11:41.785Z","_ts":"2026-05-16T14:11:41.787Z"}
{"event":"session_start","session_id":"019e31e2-19f9-7102-a633-8f2c4c8edf28","native_session_id":"019e31e2-19f9-7102-a633-8f2c4c8edf28","pid":39200,"timestamp":"2026-05-16T17:44:29.393Z","_ts":"2026-05-16T17:44:29.396Z"}
{"event":"session_start","session_id":"019e31e2-19f9-7102-a633-8f2c4c8edf28","native_session_id":"019e31e2-19f9-7102-a633-8f2c4c8edf28","pid":26588,"timestamp":"2026-05-16T17:59:16.555Z","_ts":"2026-05-16T17:59:16.557Z"}
{"event":"session_start","session_id":"019e31f8-d6eb-7bf0-b3d4-c91f77376e2b","native_session_id":"019e31f8-d6eb-7bf0-b3d4-c91f77376e2b","pid":8764,"timestamp":"2026-05-16T18:12:09.275Z","_ts":"2026-05-16T18:12:09.278Z"}
````

## File: .omx/logs/omx-2026-05-17.jsonl
````
{"event":"session_start","session_id":"019e34bc-d302-79a3-a273-5fe32ee51183","native_session_id":"019e34bc-d302-79a3-a273-5fe32ee51183","pid":8292,"timestamp":"2026-05-17T07:04:03.938Z","_ts":"2026-05-17T07:04:03.941Z"}
{"event":"session_start","session_id":"019e34d5-3b9e-7e41-ba7a-e6c4b149d513","native_session_id":"019e34d5-3b9e-7e41-ba7a-e6c4b149d513","pid":28708,"timestamp":"2026-05-17T07:27:58.884Z","_ts":"2026-05-17T07:27:58.886Z"}
{"event":"session_start","session_id":"019e352f-f6ae-75d1-a576-7bf5eeb0d2cd","native_session_id":"019e352f-f6ae-75d1-a576-7bf5eeb0d2cd","pid":8604,"timestamp":"2026-05-17T09:08:26.315Z","_ts":"2026-05-17T09:08:26.317Z"}
{"event":"session_start","session_id":"019e3554-94f7-7a13-8b8d-3858ee673d08","native_session_id":"019e3554-94f7-7a13-8b8d-3858ee673d08","pid":31440,"timestamp":"2026-05-17T09:47:18.158Z","_ts":"2026-05-17T09:47:18.160Z"}
{"event":"session_start","session_id":"019e3637-0c5d-7492-8205-61c8653c23b8","native_session_id":"019e3637-0c5d-7492-8205-61c8653c23b8","pid":36048,"timestamp":"2026-05-17T13:54:09.070Z","_ts":"2026-05-17T13:54:09.072Z"}
{"event":"session_start","session_id":"019e3637-5de3-7e10-99f9-54ce396e991f","native_session_id":"019e3637-5de3-7e10-99f9-54ce396e991f","pid":35624,"timestamp":"2026-05-17T13:54:54.911Z","_ts":"2026-05-17T13:54:54.914Z"}
{"event":"session_start","session_id":"019e3701-953a-72d0-ac5f-91d4a33c67d6","native_session_id":"019e3701-953a-72d0-ac5f-91d4a33c67d6","pid":22504,"timestamp":"2026-05-17T17:35:26.522Z","_ts":"2026-05-17T17:35:26.524Z"}
````

## File: .omx/logs/omx-2026-05-18.jsonl
````
{"event":"session_start","session_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","native_session_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","pid":28940,"timestamp":"2026-05-18T04:40:09.301Z","_ts":"2026-05-18T04:40:09.303Z"}
{"event":"session_start","session_id":"019e39e8-5f3d-71c1-a914-74ff757bd5ad","native_session_id":"019e39e8-5f3d-71c1-a914-74ff757bd5ad","pid":18828,"timestamp":"2026-05-18T07:06:36.693Z","_ts":"2026-05-18T07:06:36.695Z"}
{"event":"session_start","session_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","native_session_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","pid":17080,"timestamp":"2026-05-18T07:07:44.987Z","_ts":"2026-05-18T07:07:44.990Z"}
{"event":"session_start","session_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","native_session_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","pid":20120,"timestamp":"2026-05-18T07:51:23.156Z","_ts":"2026-05-18T07:51:23.158Z"}
{"event":"session_start","session_id":"019e3a16-5a64-7103-8b3c-e70142c689e6","native_session_id":"019e3a16-5a64-7103-8b3c-e70142c689e6","pid":26364,"timestamp":"2026-05-18T07:58:00.571Z","_ts":"2026-05-18T07:58:00.575Z"}
{"event":"session_start","session_id":"019e3b30-5598-7233-bc1e-9a7647706db6","native_session_id":"019e3b30-5598-7233-bc1e-9a7647706db6","pid":21172,"timestamp":"2026-05-18T13:09:07.227Z","_ts":"2026-05-18T13:09:07.230Z"}
{"event":"session_start","session_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","native_session_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","pid":32060,"timestamp":"2026-05-18T17:25:55.934Z","_ts":"2026-05-18T17:25:55.937Z"}
{"event":"session_start","session_id":"019e3c3d-3186-78c3-adce-9a8ea1e12314","native_session_id":"019e3c3d-3186-78c3-adce-9a8ea1e12314","pid":10512,"timestamp":"2026-05-18T17:58:29.915Z","_ts":"2026-05-18T17:58:29.917Z"}
{"event":"session_start","session_id":"019e3c3d-5687-72b3-b471-53527e4aef0c","native_session_id":"019e3c3d-5687-72b3-b471-53527e4aef0c","pid":25120,"timestamp":"2026-05-18T17:58:45.340Z","_ts":"2026-05-18T17:58:45.342Z"}
{"event":"session_start","session_id":"019e3c3e-8dc3-7c62-b0c9-b7c1b6758ba5","native_session_id":"019e3c3e-8dc3-7c62-b0c9-b7c1b6758ba5","pid":27992,"timestamp":"2026-05-18T18:01:20.367Z","_ts":"2026-05-18T18:01:20.371Z"}
{"event":"session_start","session_id":"019e3c4b-1f35-7cc1-afbd-26235c7bd804","native_session_id":"019e3c4b-1f35-7cc1-afbd-26235c7bd804","pid":18584,"timestamp":"2026-05-18T18:14:32.162Z","_ts":"2026-05-18T18:14:32.165Z"}
{"event":"session_start","session_id":"019e3c90-f750-7f43-9ac8-1c72cc262de4","native_session_id":"019e3c90-f750-7f43-9ac8-1c72cc262de4","pid":20968,"timestamp":"2026-05-18T19:30:04.526Z","_ts":"2026-05-18T19:30:04.528Z"}
````

## File: .omx/logs/omx-2026-05-19.jsonl
````
{"event":"session_start","session_id":"019e3e06-b481-7b82-a53f-364e6e0c13c5","native_session_id":"019e3e06-b481-7b82-a53f-364e6e0c13c5","pid":22200,"timestamp":"2026-05-19T02:18:15.656Z","_ts":"2026-05-19T02:18:15.659Z"}
{"event":"session_start","session_id":"019e3e09-6b8d-7983-a25f-31ce8f890ede","native_session_id":"019e3e09-6b8d-7983-a25f-31ce8f890ede","pid":1992,"timestamp":"2026-05-19T02:21:11.274Z","_ts":"2026-05-19T02:21:11.277Z"}
{"event":"session_start","session_id":"019e3e09-c6f7-7e31-aa55-02ed67d29ad7","native_session_id":"019e3e09-c6f7-7e31-aa55-02ed67d29ad7","pid":24976,"timestamp":"2026-05-19T02:21:35.854Z","_ts":"2026-05-19T02:21:35.857Z"}
{"event":"session_start","session_id":"019e3ef1-2e98-7df3-9b7b-b34d2b86d447","native_session_id":"019e3ef1-2e98-7df3-9b7b-b34d2b86d447","pid":16088,"timestamp":"2026-05-19T06:34:34.040Z","_ts":"2026-05-19T06:34:34.043Z"}
{"event":"session_start","session_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","native_session_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","pid":27080,"timestamp":"2026-05-19T06:56:23.253Z","_ts":"2026-05-19T06:56:23.256Z"}
{"event":"session_start","session_id":"019e3f21-cb5f-70a3-8638-e836d7e5e93e","native_session_id":"019e3f21-cb5f-70a3-8638-e836d7e5e93e","pid":7020,"timestamp":"2026-05-19T07:27:26.472Z","_ts":"2026-05-19T07:27:26.474Z"}
{"event":"session_start","session_id":"019e3f2b-015c-7d43-b8d2-2c30e360c39b","native_session_id":"019e3f2b-015c-7d43-b8d2-2c30e360c39b","pid":22188,"timestamp":"2026-05-19T07:37:32.305Z","_ts":"2026-05-19T07:37:32.310Z"}
{"event":"session_start","session_id":"019e3f5c-1d36-7170-b332-9af526c5e71c","native_session_id":"019e3f5c-1d36-7170-b332-9af526c5e71c","pid":29584,"timestamp":"2026-05-19T08:32:51.066Z","_ts":"2026-05-19T08:32:51.070Z"}
{"event":"session_start","session_id":"019e3f7b-2396-79c1-8add-3221515c85bf","native_session_id":"019e3f7b-2396-79c1-8add-3221515c85bf","pid":33096,"timestamp":"2026-05-19T09:05:04.702Z","_ts":"2026-05-19T09:05:04.707Z"}
{"event":"session_start","session_id":"019e3f8f-a73f-7a41-8ec3-d045522df5d9","native_session_id":"019e3f8f-a73f-7a41-8ec3-d045522df5d9","pid":38628,"timestamp":"2026-05-19T09:30:56.926Z","_ts":"2026-05-19T09:30:56.929Z"}
{"event":"session_start","session_id":"019e3f96-85cf-7c93-a593-d8b1c9014896","native_session_id":"019e3f96-85cf-7c93-a593-d8b1c9014896","pid":25064,"timestamp":"2026-05-19T09:35:05.539Z","_ts":"2026-05-19T09:35:05.541Z"}
{"event":"session_start","session_id":"019e3fa8-e51c-76a3-a071-888dd38a852e","native_session_id":"019e3fa8-e51c-76a3-a071-888dd38a852e","pid":32568,"timestamp":"2026-05-19T09:55:52.741Z","_ts":"2026-05-19T09:55:52.744Z"}
{"event":"session_start","session_id":"019e3fc3-6efd-74b2-9051-78b4b234968d","native_session_id":"019e3fc3-6efd-74b2-9051-78b4b234968d","pid":37104,"timestamp":"2026-05-19T10:24:09.911Z","_ts":"2026-05-19T10:24:09.913Z"}
{"event":"session_start","session_id":"019e4019-c724-74c1-8b97-ee896d9bea78","native_session_id":"019e4019-c724-74c1-8b97-ee896d9bea78","pid":26832,"timestamp":"2026-05-19T12:02:37.424Z","_ts":"2026-05-19T12:02:37.426Z"}
````

## File: .omx/logs/tmux-hook-2026-05-16.jsonl
````
{"timestamp":"2026-05-16T11:53:24.068Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T13:41:30.328Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T13:44:12.301Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T13:44:33.922Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T13:52:06.313Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T13:55:29.754Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T14:10:15.233Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T14:11:44.684Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T14:16:13.135Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T14:26:55.724Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T17:44:38.193Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T18:06:21.765Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T18:12:25.893Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T18:27:35.725Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T19:27:48.205Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T19:40:27.300Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T19:49:27.981Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-16T19:56:16.862Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
````

## File: .omx/logs/tmux-hook-2026-05-17.jsonl
````
{"timestamp":"2026-05-17T07:04:22.161Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T07:13:07.395Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T07:24:47.944Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T07:28:05.114Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T07:37:54.778Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T07:47:40.630Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T09:08:39.933Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T09:21:28.048Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T09:47:27.865Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T10:07:51.956Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T13:55:01.738Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T13:57:23.749Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T14:09:06.708Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T14:25:29.700Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T14:35:14.685Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T17:13:37.939Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T17:31:25.662Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T17:35:26.419Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T17:39:09.395Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-17T18:36:28.662Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
````

## File: .omx/logs/tmux-hook-2026-05-18.jsonl
````
{"timestamp":"2026-05-18T04:40:20.983Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T04:54:21.316Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T05:10:18.700Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T05:36:31.478Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T06:19:11.250Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:07:56.865Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:08:26.420Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:13:17.076Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:26:54.508Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:42:43.710Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:45:52.061Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:46:06.438Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:47:46.843Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T07:58:13.683Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T08:12:37.846Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T13:25:36.539Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:26:08.025Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:30:24.466Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:32:06.512Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:33:58.907Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:36:26.830Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:38:36.636Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:42:42.217Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:44:54.768Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:50:13.073Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:57:00.107Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:58:47.853Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:58:54.792Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T17:59:39.716Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T18:00:19.013Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-18T18:01:32.050Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
````

## File: .omx/logs/tmux-hook-2026-05-19.jsonl
````
{"timestamp":"2026-05-19T02:21:48.543Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T02:24:17.183Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T06:34:29.055Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T06:56:39.398Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:01:30.266Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:11:51.893Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:30:06.158Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:33:14.626Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:34:28.963Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:40:20.152Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T07:41:10.793Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T08:03:19.009Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T08:26:16.840Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T08:33:13.529Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T08:51:00.612Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:05:15.972Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:35:05.449Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:43:39.131Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:53:08.934Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:56:06.709Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T09:58:17.354Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T10:17:45.743Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T10:24:09.810Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T10:35:39.373Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T10:38:29.459Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
{"timestamp":"2026-05-19T11:58:26.907Z","type":"auto_nudge_skipped","reason":"unmanaged_session"}
````

## File: .omx/logs/turns-2026-05-16.jsonl
````
{"timestamp":"2026-05-16T11:53:23.832Z","type":"agent-turn-complete","thread_id":"019e30a2-1201-71a1-8b9e-fb65442fff71","turn_id":"019e30a2-1447-7953-a482-bda446db0dc4","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"启动项目\"}"}
{"timestamp":"2026-05-16T13:41:30.061Z","type":"agent-turn-complete","thread_id":"019e3104-e44a-7903-8fab-049956f143bd","turn_id":"019e3104-e5c2-73a1-8e52-4a46773293c9","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"启动项目\"}"}
{"timestamp":"2026-05-16T13:44:11.982Z","type":"agent-turn-complete","thread_id":"019e3104-76e4-7ac3-901b-8f37bd81ff00","turn_id":"019e3104-7793-7e72-a2f6-ab700bab9544","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"title\":\"Fix the LoveMaster RAG stream crash before you start testing\",\"description\":\"You opened a `启动项目` thread today, and the current RAG endpoint will crash on first use: `ai-servi"}
{"timestamp":"2026-05-16T13:44:33.692Z","type":"agent-turn-complete","thread_id":"019e3104-de0e-7620-8ea6-3c5b5209452d","turn_id":"019e3104-deed-7d72-96c0-94ca302175fc","input_preview":"启动项目\n","input_message_count":1,"output_preview":"项目已启动，三端都通了：\n\n- 前端：<http://localhost:5173>，HTTP 200\n- Gateway：<http://localhost:8080/health>，返回 `{\"status\":\"ok\",\"service\":\"gateway\",\"ai_service\":\"ok\"}`\n- AI Service：<http://localhost:8000/health>，返回 `"}
{"timestamp":"2026-05-16T13:52:05.979Z","type":"agent-turn-complete","thread_id":"019e310e-85ee-70a2-b59d-4253b7950d38","turn_id":"019e310e-86b7-7a30-a409-9ab85ad8d750","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复 Agent/RAG 状态检测\"}"}
{"timestamp":"2026-05-16T13:55:29.474Z","type":"agent-turn-complete","thread_id":"019e310e-7f8f-7600-982d-f9d8b8041eb0","turn_id":"019e310e-8332-7f11-9901-80c3278a5e3c","input_preview":"修复一下Agent模块和RAG模块的实时状态检测问题\r\n分为未连接、连接错误、连接成功。\r\n当点进界面里会有自动检测状态\r\n如果报错，会弹窗说明状态错误的原因\r\n先使用[$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) [$grill-me](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\grill-me","input_message_count":1,"output_preview":"🥷 使用 `think + grill-me` 规划后的结论：建议做一个很小的闭环修复。\n\n**前提假设**\n- “Agent模块”指 `SuperAgent` 页面及 `/api/v1/chat/*` 能力。\n- “RAG模块”指 `LoveMaster/户外徒步大师` 页面及 `/api/v1/rag/*` 能力。\n- 状态文案按你说的三类固定为：`未连接`、`连接错误`、`连接成功`。\n-"}
{"timestamp":"2026-05-16T14:10:14.957Z","type":"agent-turn-complete","thread_id":"019e310e-7f8f-7600-982d-f9d8b8041eb0","turn_id":"019e3112-732b-73e3-a685-634f435db4f1","input_preview":"[$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) [$caveman](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\caveman\\\\SKILL.md) 开始执行计划\n","input_message_count":2,"output_preview":"▎[华为味] 闭环完成。问题根因：前端把“发送状态”当“模块连接状态”，页面进入时没有独立 health 检测。\n\n已改好：\n\n- Agent/RAG 各自新增模块健康接口，并经 gateway 转发。\n- 前端进入 `SuperAgent` / `户外徒步大师` 页面后自动检测，之后每 30 秒检测。\n- 状态收敛为三种：`未连接` / `连接错误` / `连接成功`。\n- 检测或请求报错时弹窗"}
{"timestamp":"2026-05-16T14:11:44.432Z","type":"agent-turn-complete","thread_id":"019e3120-a742-77e3-814d-ed018c64f989","turn_id":"019e3120-a85a-7e73-b2ff-3f9f09c3954f","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"重启项目\"}"}
{"timestamp":"2026-05-16T14:16:12.846Z","type":"agent-turn-complete","thread_id":"019e3120-a1aa-7c92-93bd-6868d5eec123","turn_id":"019e3120-a2c2-7e90-b4c5-79c1c6b47545","input_preview":"重启项目\n","input_message_count":1,"output_preview":"重启完成。\n\n当前状态：\n- 前端：`http://127.0.0.1:5173/`，HTTP 200\n- 网关：`http://127.0.0.1:8080/health`，HTTP 200\n- AI 服务：`http://127.0.0.1:8000/health`，HTTP 200\n- Docker：Postgres / Redis 均为 healthy\n\n有个小注意点：AI 服务现在是保留"}
{"timestamp":"2026-05-16T14:26:55.440Z","type":"agent-turn-complete","thread_id":"019e3120-a1aa-7c92-93bd-6868d5eec123","turn_id":"019e3127-c9df-7d53-adc1-c0f707fbf789","input_preview":"修复一下连接错误的问题\n[$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) [$caveman](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\caveman\\\\SKILL.md) \n","input_message_count":2,"output_preview":"修好了。根因：运行中的 AI 服务还是旧路由，`/api/v1/chat/health` 直连返回 404；前端因此显示 `连接错误`。\n\n已改：\n- [chat.go](C:/Users/14253/Desktop/ai-hiking/gateway/handler/chat.go:30)：Agent health 404 时 fallback 到 AI 服务 `/health`\n- [rag."}
{"timestamp":"2026-05-16T17:44:37.960Z","type":"agent-turn-complete","thread_id":"019e31e3-aa08-7ea2-a706-459dd1361202","turn_id":"019e31e3-ada2-7c20-8b84-b108752393a9","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"对接前后端真实逻辑\"}"}
{"timestamp":"2026-05-16T18:06:21.504Z","type":"agent-turn-complete","thread_id":"019e31e2-19f9-7102-a633-8f2c4c8edf28","turn_id":"019e31f1-3cdf-7fd1-ae0b-476c4af61021","input_preview":"continue\n","input_message_count":2,"output_preview":"已接好真实后端链路。\n\n改动重点：\n- Agent 前端现在复用持久 `chat_id`，后端历史可真实生效：[SuperAgent.tsx](</C:/Users/14253/Desktop/ai-hiking/frontend/src/pages/SuperAgent.tsx>)\n- 网关 SSE 不再手写 JSON/吞错误，`chat` 和 `rag` 都真实流式转发：[chat.go](<"}
{"timestamp":"2026-05-16T18:12:25.664Z","type":"agent-turn-complete","thread_id":"019e31fd-1998-7e70-ac88-d80cc7c7bbb5","turn_id":"019e31fd-1b60-7490-9e12-19c48544b1eb","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复 CSS 并新增 LLM 配置页\"}"}
{"timestamp":"2026-05-16T18:27:35.479Z","type":"agent-turn-complete","thread_id":"019e31f8-d6eb-7bf0-b3d4-c91f77376e2b","turn_id":"019e31fd-0ec7-72e2-8067-6d31abdcfcc3","input_preview":"修复问题\n先使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 规划一下任务\n1. 使用[$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 规范一下修复范围\n2.修复一下CSS展示失败的问题\n3.写一个llm配置的界面，只能通过路由的方式进入，前端界面没有入口\n主","input_message_count":1,"output_preview":"修好了。PUA 闭环：证据齐。\n\n改动：\n- CSS 展示失败：重启 5173 Vite，确认 `/src/index.css` 已编译 Tailwind，不再是 raw `@tailwind`；并把实际入口需要的 tokens/keyframes/motion CSS 放进 [frontend/src/index.css](C:/Users/14253/Desktop/ai-hiking/fro"}
{"timestamp":"2026-05-16T19:27:47.923Z","type":"agent-turn-complete","thread_id":"019e3242-19c0-7383-86f5-be9458c8d653","turn_id":"019e3242-1e9f-71b2-9600-7ff971b36994","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复RAG报错\"}"}
{"timestamp":"2026-05-16T19:40:26.991Z","type":"agent-turn-complete","thread_id":"019e3241-8450-7bc3-af7c-72dfe8f58666","turn_id":"019e3247-fdad-7b63-93a9-1e5e509e38ef","input_preview":"continue\n","input_message_count":2,"output_preview":"已修。RAG 空知识库时不再调用 embedding API，所以不会再把 `Error code: 404` 暴露给前端。\n\n改动：\n- [retriever.py](</C:/Users/14253/Desktop/ai-hiking/ai-service/rag/retriever.py:86>)：查询前先检查 memory/pgvector 是否有匹配文档，空则直接返回 `[]`。\n- ["}
{"timestamp":"2026-05-16T19:49:27.683Z","type":"agent-turn-complete","thread_id":"019e3241-8450-7bc3-af7c-72dfe8f58666","turn_id":"019e3252-d52a-7343-8a09-9b9cd11c44f0","input_preview":"1.配置一下embedding模型\r\nhttps://api-inference.modelscope.cn/v1\r\nms-36e40ce6-2e7d-40dd-bb59-e58dfe701aed\r\nQwen/Qwen3-Embedding-8B\r\n2.优化一下RAG表达，一些简单问题，比如 ：你是谁？你好之类的非技术型问题，不进行调用文档搜索回答，直接采用简单的回答方式\n使用 [$think](","input_message_count":4,"output_preview":"🥷 ▎[🟠 阿里味] 计划先对齐，范围先锁死。底层逻辑：配置归配置，RAG 意图路由归路由，别把 key 硬塞进业务代码。\n\n**推荐方案**\n暴力版：把 ModelScope embedding 直接写死进 `retriever.py`。不推荐，密钥进源码，后面必炸。\n\n做法：\n1. 后端新增独立 embedding 配置：`EMBEDDING_BASE_URL`、`EMBEDDING_AP"}
{"timestamp":"2026-05-16T19:56:16.529Z","type":"agent-turn-complete","thread_id":"019e3241-8450-7bc3-af7c-72dfe8f58666","turn_id":"019e3256-ac67-73f3-b36e-2ba1eefc9dbf","input_preview":"implement this plan\n","input_message_count":5,"output_preview":"已完成。\n\n改动重点：\n- 已配置 ModelScope embedding：`Qwen/Qwen3-Embedding-8B`，维度 `4096`，通过独立的 `EMBEDDING_*` 配置接入。\n- 已新增 `ai-service/.env`，并用 `.gitignore` 排除，避免泄露密钥。\n- 已优化 RAG 简单问候/身份类问题，比如“你好”“你是谁”，直接回答，不触发文档检索。\n-"}
````

## File: .omx/logs/turns-2026-05-17.jsonl
````
{"timestamp":"2026-05-17T07:04:21.885Z","type":"agent-turn-complete","thread_id":"019e34bf-c031-7d20-884b-8697d20a7a5b","turn_id":"019e34bf-c257-7370-b9da-ed31c2ee6211","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复模型获取错误\"}"}
{"timestamp":"2026-05-17T07:13:07.108Z","type":"agent-turn-complete","thread_id":"019e34bc-d302-79a3-a273-5fe32ee51183","turn_id":"019e34bf-9cc4-7372-a0db-b0de5bd2eee7","input_preview":"目前在http://localhost:5173/llm-config界面中，输入baseUrl和api key获取模型时，获取的模型不是正确的模型，请修复一下问题\n首先使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 进行计划\n再使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\p","input_message_count":1,"output_preview":"已经修好了。根因不在后端取模型，而在前端展示：`/llm-config` 拿到新模型列表后，又把旧的已选模型值当成搜索词二次过滤，所以看起来像“获取到的模型不对”。我在 [frontend/src/pages/LlmConfig.tsx](C:/Users/14253/Desktop/ai-hiking/frontend/src/pages/LlmConfig.tsx:57) 把“搜索词”和“选中"}
{"timestamp":"2026-05-17T07:24:47.695Z","type":"agent-turn-complete","thread_id":"019e34bc-d302-79a3-a273-5fe32ee51183","turn_id":"019e34cd-4079-71f3-ba5b-fa51ac614b66","input_preview":"增加一个功能，保存llm配置之后自动测速\n使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 进行修改范围制定和修改风格约束\n","input_message_count":2,"output_preview":"已经加上了，抓手很清楚：现在 [frontend/src/pages/LlmConfig.tsx](C:/Users/14253/Desktop/ai-hiking/frontend/src/pages/LlmConfig.tsx:253) 里点击“保存”后，会自动进入测速态，按钮禁用并显示加载中，然后把大模型和 Embedding 两组测速结果卡渲染出来，包含状态、耗时和返回模型数。测速逻辑收敛"}
{"timestamp":"2026-05-17T07:28:04.898Z","type":"agent-turn-complete","thread_id":"019e34d5-93b1-7981-b4e9-4ccb67284790","turn_id":"019e34d5-942b-76a2-8cdd-6ba142a86868","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复获取错误\"}"}
{"timestamp":"2026-05-17T07:37:54.501Z","type":"agent-turn-complete","thread_id":"019e34d5-3b9e-7e41-ba7a-e6c4b149d513","turn_id":"019e34d5-76e5-72e3-bd2e-484883b314fd","input_preview":"目前获取依旧是错误的，重新修复问题\n\r\n使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 进行修改范围制定和修改风格约束\n","input_message_count":1,"output_preview":"这次把病根改到了前端“按用途分流模型列表”这一层，不再只是修下拉框搜索。之前 `/models` 的混合返回会直接喂给两个卡片，所以大模型卡可能看到 embedding-only 模型；现在在 [llmConfig.ts](<C:/Users/14253/Desktop/ai-hiking/frontend/src/api/llmConfig.ts:166>) 增加了模型用途识别和 `filter"}
{"timestamp":"2026-05-17T07:47:40.380Z","type":"agent-turn-complete","thread_id":"019e34d5-3b9e-7e41-ba7a-e6c4b149d513","turn_id":"019e34e1-d4e8-7762-9074-a5c3f9f1a6eb","input_preview":"continue\n","input_message_count":3,"output_preview":"根因已经换清楚了：这次不是“获取模型接口还在拿错”，而是之前拿错后的坏值被写进了 `localStorage`，页面每次打开都会把它原样恢复，所以你会继续看到大模型卡里挂着 `text-embedding-3-small`。我在 [llmConfig.ts](<C:/Users/14253/Desktop/ai-hiking/frontend/src/api/llmConfig.ts:94>) 加"}
{"timestamp":"2026-05-17T09:08:39.719Z","type":"agent-turn-complete","thread_id":"019e3531-9e2b-75e0-87e5-82c549b1b953","turn_id":"019e3531-a285-7c01-9e84-a3e0a6009e94","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"添加Rerank模型与打分步骤\"}"}
{"timestamp":"2026-05-17T09:21:27.780Z","type":"agent-turn-complete","thread_id":"019e352f-f6ae-75d1-a576-7bf5eeb0d2cd","turn_id":"019e3532-aa32-7093-91e8-8af9ae80ae73","input_preview":"在http://localhost:5173/llm-config界面添加rerank模型的添加\r\n然后在RAG执行链路里面添加Rerank打分的步骤\r\n使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 进行规划\r\n然后使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SK","input_message_count":1,"output_preview":"已完成，闭环证据也跑完了。\n\n这次主要改了 [llmConfig.ts](C:/Users/14253/Desktop/ai-hiking/frontend/src/api/llmConfig.ts)、[LlmConfig.tsx](C:/Users/14253/Desktop/ai-hiking/frontend/src/pages/LlmConfig.tsx)、[config.py](C:/U"}
{"timestamp":"2026-05-17T09:47:27.644Z","type":"agent-turn-complete","thread_id":"019e3555-32aa-7581-aefd-bd04bff9edc3","turn_id":"019e3555-3763-7e13-a7a7-e21e0be3dd5e","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复RAG对话显示问题\"}"}
{"timestamp":"2026-05-17T10:07:51.704Z","type":"agent-turn-complete","thread_id":"019e3554-94f7-7a13-8b8d-3858ee673d08","turn_id":"019e3555-d3b8-7ce3-8538-ef3e779b88f1","input_preview":"为什么我已经配置了大模型，RAG对话的时候还是这样显示？修复一下问题\r\n先使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 进行修复规划\n接着使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 进行风格定调\n最后使用 [$tdd](C:\\\\Users\\\\1","input_message_count":1,"output_preview":"▎[🔴 华为味] 根因挖到底了：不是你页面上没配，而是配置没有打到后端运行时，AI service 还因为缺少全局 `OPENAI_API_KEY` 直接启动崩溃。503 是 gateway 连不上 8000，不是 RAG 业务本身炸了。\n\n已修复：\n\n- [config.py](C:/Users/14253/Desktop/ai-hiking/ai-service/config.py:35)："}
{"timestamp":"2026-05-17T13:55:01.501Z","type":"agent-turn-complete","thread_id":"019e3637-d137-7ee1-af68-ace590997faa","turn_id":"019e3637-d4a0-7953-a6d4-f5c6905d5ea6","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复RAG飞书知识库与输出\"}"}
{"timestamp":"2026-05-17T13:57:23.514Z","type":"agent-turn-complete","thread_id":"019e3637-0c5d-7492-8205-61c8653c23b8","turn_id":"019e3637-0d12-79f1-9509-717595fe1d44","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"title\":\"让 Super Agent 复用 llm-config 运行时配置\",\"description\":\"`ai-service/uvicorn.err.log` 还在反复报 `/api/v1/chat/health` 因缺少 `OPENAI_API_KEY` 而失败，但 RAG 已经能从 `/llm-config` 传运行时模型配置。把 Agent "}
{"timestamp":"2026-05-17T14:09:06.424Z","type":"agent-turn-complete","thread_id":"019e3637-5de3-7e10-99f9-54ce396e991f","turn_id":"019e3637-cf6d-7db1-bbce-4c674356aad2","input_preview":"使用 /pua规范一下修复范围和修复风格  \n修复一下目前RAG无法获取飞书知识库内容的问题，调用lark-cli进行链接筛查\r\n修复一下RAG的输出风格，参考/humanizer-zh的技能要求进行风格输出\r\n增加RAG输出时的内容，增加文档搜索输出比如搜索了多少篇文章（默认折叠），然后具体是什么文档内容\r\n增加RAG输出时的执行流程，比如使用**进行了**步骤。\r\n 使用/caveman 优化","input_message_count":1,"output_preview":"修好了。范围只动 RAG/飞书链路、RAG 前端展示、网关 fallback、测试、`MEMORY.md`。\n\n改动重点：\n- [ai-service/rag/feishu.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/feishu.py)：支持飞书 Wiki 链接筛查，走 `lark-cli wiki spaces get_node` 解"}
{"timestamp":"2026-05-17T14:25:29.457Z","type":"agent-turn-complete","thread_id":"019e3637-5de3-7e10-99f9-54ce396e991f","turn_id":"019e3651-8737-7133-bba7-53a193974faa","input_preview":"1.我的意思是你操作lark-cli进行api对接，本质上还是用api对接飞书知识库\r\n2.RAG流程指的是使用RAG的步骤，比如，调用embedding模型进行****等等\r\n[$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 使用技能规范一下修复范围和修复风格 \r\n 使用/caveman 优化一下无意义输出\n使用 [$think](C","input_message_count":3,"output_preview":"🥷 Brute-force 版：把 Feishu 读取全改成 `lark-cli api` 显式打 OpenAPI；RAG 流程事件改成真实技术步骤：embedding → vector search → rerank → context augment → LLM generate。\n\n▎[🟠 阿里味] 这次修范围要收口，抓手清楚：API 对接归 Feishu adapter，RAG 流程归"}
{"timestamp":"2026-05-17T14:35:14.429Z","type":"agent-turn-complete","thread_id":"019e3637-5de3-7e10-99f9-54ce396e991f","turn_id":"019e3654-436a-7f82-9350-d8351c8317ce","input_preview":"implement this plan\n最后使用 [$tdd](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\tdd\\\\SKILL.md) 进行结果验证\n","input_message_count":4,"output_preview":"已完成。\n\n改动核心：\n- [feishu.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/feishu.py:101)：新增 `call_lark_api()`，Wiki 节点解析、Wiki 节点列表、docs_ai fetch 都改为 `lark-cli api` 调 `/open-apis/...`。\n- [rag.py](C:/Use"}
{"timestamp":"2026-05-17T17:13:37.491Z","type":"agent-turn-complete","thread_id":"019e36ed-a71f-7fc0-bed3-cd9eeaea134c","turn_id":"019e36ed-a8c1-7081-a7fa-15a0366bd0dd","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"优化 LangChain RAG 流程\"}"}
{"timestamp":"2026-05-17T17:31:25.422Z","type":"agent-turn-complete","thread_id":"019e36ec-fb08-71c3-a815-8b264a74ad00","turn_id":"019e36f3-4d5a-7052-a784-342bbd42d36e","input_preview":"\n# Files mentioned by the user:\n\n## langchain-components.md: C:\\Users\\14253\\Desktop\\context\\langchain-components.md\n\n## My request for Codex:\n根据Langchian组件优化一下目前RAG流程的问题。\n[$pua](C:\\\\Users\\\\14253\\\\.cod","input_message_count":1,"output_preview":"已按 LangChain 组件思路把 RAG 流程补了一道“证据闸门”。\n\n改动点：\n- [augmenter.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/augmenter.py:13)：强化 `ChatPromptTemplate`，要求只基于文档回答、关键事实带来源编号，禁止文档外发挥；生成温度降到 `0.2`。\n- [augmen"}
{"timestamp":"2026-05-17T17:35:26.183Z","type":"agent-turn-complete","thread_id":"019e3701-998d-70d1-ae54-d4d195fcb075","turn_id":"019e3701-9a13-74e2-982e-c5da4acf156b","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"启动项目\"}"}
{"timestamp":"2026-05-17T17:39:09.151Z","type":"agent-turn-complete","thread_id":"019e3701-953a-72d0-ac5f-91d4a33c67d6","turn_id":"019e3701-960c-7062-8923-069a62326022","input_preview":"启动项目\n","input_message_count":1,"output_preview":"项目已经启动好，而且当前就是可用状态。我核验过这几项都正常：\n\n- 前端：[http://127.0.0.1:5173](http://127.0.0.1:5173) `HTTP 200`\n- Gateway：[http://127.0.0.1:8080/health](http://127.0.0.1:8080/health) 返回 `{\"ai_service\":\"ok\",\"service\":\""}
{"timestamp":"2026-05-17T18:36:28.159Z","type":"agent-turn-complete","thread_id":"019e3701-953a-72d0-ac5f-91d4a33c67d6","turn_id":"019e3734-d041-7030-9066-75a5c5a1cb5d","input_preview":"continue\n","input_message_count":4,"output_preview":"已完成。\n\n**改动**\n- RAG 上传流程已改成：统一接入/格式化 -> 正则降噪 -> 混合分块 -> 元数据标记 -> embedding -> PGVector。\n- RAG 查询流程已改成：问题 -> query 改写 -> 向量化 -> 混合检索 -> BM25 + RRF -> Reranker -> humanizer-zh 风格改写/输出。\n- AI 思考态已升级，`love-"}
````

## File: .omx/logs/turns-2026-05-18.jsonl
````
{"timestamp":"2026-05-18T04:40:20.743Z","type":"agent-turn-complete","thread_id":"019e3962-5a8f-7101-97d7-1435ef727c81","turn_id":"019e3962-5e3a-7273-918b-cb4342092987","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复RAG配置报错\"}"}
{"timestamp":"2026-05-18T04:54:21.072Z","type":"agent-turn-complete","thread_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","turn_id":"019e3962-58fd-7510-b844-03d941388356","input_preview":"修复一下这里RAG正常配置之后报错的问题\n1.使用  [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 计划修复方案\n2.使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 约束修复范围和风格\n3.使用 [$caveman](C:\\\\Users\\\\14253\\\\","input_message_count":1,"output_preview":"修好了。根因不是单纯配置页问题：AI service 当时没跑导致 gateway 503；服务拉起后又发现 pgvector 里混了旧 `8` 维向量和当前 `4096` 维向量，检索会报维度不一致并降级到空 memory。\n\n改动：\n- [retriever.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/retriever.py:74)"}
{"timestamp":"2026-05-18T05:10:18.452Z","type":"agent-turn-complete","thread_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","turn_id":"019e3972-fdad-7bf2-8708-0a4018104982","input_preview":"为什么我的飞书文档有相关内容，但还是获取不到这是什么原因\n1.使用  Think 计划修复方案\r\n2.使用 Pua 约束修复范围和风格\r\n3.使用 Caveman 减少无意义输出\r\n4.使用 Tdd进行修复完成的测试 \n","input_message_count":2,"output_preview":"原因找到了，并已修复。\n\n你的飞书文档本身有内容，但 RAG 检索查的是本地知识库/向量库，不是浏览器里当前打开的飞书页面。我查到当前库里的 `户外徒步知识文档.md` 没有 `feishu_doc_token / feishu_wiki_node_token / status=feishu` 元数据，所以它不是按“飞书同步来源”入库的。\n\n截图里 `0 篇文档 / 0 个片段` 的直接原因是：运"}
{"timestamp":"2026-05-18T05:36:31.172Z","type":"agent-turn-complete","thread_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","turn_id":"019e3985-d431-7880-a90a-28b34a7999b7","input_preview":"目前改写后的文字表述非常杂乱，请优化一下输出形式，不要markdown文档的 **格式\n1.使用  Think 计划修复方案\r\n2.使用 Pua 约束修复范围和风格\r\n3.使用 Caveman 减少无意义输出\r\n4.使用 Tdd进行修复完成的测试 \n","input_message_count":3,"output_preview":"已修。按 Think/Pua 收口后，只动 RAG 输出展示层，没有改检索、飞书同步、模型配置。\n\n改动点：\n\n- [text_processing.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/text_processing.py:66)：新增纯文本清洗，去掉 `**`、`#`、`[1]`、`<sup>`、代码块等噪声。\n- [augme"}
{"timestamp":"2026-05-18T06:19:10.997Z","type":"agent-turn-complete","thread_id":"019e395f-c99b-7563-9f9a-d5ef33cc59e5","turn_id":"019e39ae-3669-7ac2-a742-032d6fbe3252","input_preview":"优化一下输出回答表述，只回答prompt提出的问题，不要在正文中说，在**文档/知识中有所说明\n优化一下长文本的表达输出，采用分点的方式进行回答，提高信息密度和视觉美观度\n1.使用  Think 计划修复方案\r\n2.使用 Pua 约束修复范围和风格\r\n3.使用 Caveman 减少无意义输出\r\n4.使用 Tdd进行修复完成的测试 \n","input_message_count":4,"output_preview":"已修，范围只动 RAG 回答表达层。\n\n改动：\n- [augmenter.py](C:/Users/14253/Desktop/ai-hiking/ai-service/rag/augmenter.py:19)：Prompt 要求只回答问题本身，不写“根据文档 / 知识库 / 资料显示 / 检索内容提到”。\n- [augmenter.py](C:/Users/14253/Desktop/ai-hi"}
{"timestamp":"2026-05-18T07:07:56.659Z","type":"agent-turn-complete","thread_id":"019e39e9-7ddc-7a90-bc21-d1d840d142b0","turn_id":"019e39e9-7e5f-7370-adab-b6b592399f10","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"检查 Agent 模块流程\"}"}
{"timestamp":"2026-05-18T07:08:26.214Z","type":"agent-turn-complete","thread_id":"019e39e8-5f3d-71c1-a914-74ff757bd5ad","turn_id":"019e39e8-6026-7690-b2b1-572de03072fe","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"appId\":\"\",\"description\":\"Today’s RAG failure came from old `8`-dim vectors mixed with the new `4096`-dim embedding config. Codex can add a one-shot repair path that detects mismatche"}
{"timestamp":"2026-05-18T07:13:16.854Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e39e9-7d7a-7c60-aff9-4b53472a3621","input_preview":"检查一下目前的Agent模块流程\n","input_message_count":1,"output_preview":"已检查当前 Agent 模块流程，未改代码。\n\n**当前流程**\n前端 [SuperAgent.tsx](C:/Users/14253/Desktop/ai-hiking/frontend/src/pages/SuperAgent.tsx:159) 进入页面后自动请求 `/api/v1/chat/health`，每 30 秒复检；发送消息时走 [createStreamConnection](C:"}
{"timestamp":"2026-05-18T07:26:54.267Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e39f8-c436-7be2-b0f4-1fe9fd28e906","input_preview":"\n# Files mentioned by the user:\n\n## repo-context.md: C:\\Users\\14253\\Desktop\\yu-ai-agent-master\\repo-context.md\n\n## My request for Codex:\n阅读一下这个项目的agent模块的流程信息，并画一张Agent模块的流程图，然后根据本项目再画一张，对比一下，根据对比结果写分","input_message_count":2,"output_preview":"`humanizer-zh` 技能文件当前不可用，我按中文自然表达整理。已读两个项目上下文，未改代码。\n\n**Yu AI Agent 流程图**\n```mermaid\nflowchart TD\n  A[\"SuperAgent.vue 输入消息\"] --> B[\"chatWithManus(message)\"]\n  B --> C[\"EventSource GET /api/ai/manus/cha"}
{"timestamp":"2026-05-18T07:42:43.500Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e3a07-e716-7821-821d-78e2336312f0","input_preview":"参考Yu项目进行本项目agent流程优化，使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 进行优化计划\n再使用 [$grill-me](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\grill-me\\\\SKILL.md) 进行细则询问\n","input_message_count":3,"output_preview":"🥷 已按 `think + grill-me` 路径做计划，不进入实现。核心判断：**参考 Yu 项目，但不要照搬 Yu 的 Java 手写 Agent 框架；本项目应保留 LangGraph，把流程显式化、统一化。**\n\n**优化目标**\n把本项目 Agent 从现在的“规则分流 + 部分 LangGraph ReAct”改成“统一 ReAct 执行流”：\n\n```text\n用户输入\n  ->"}
{"timestamp":"2026-05-18T07:45:51.836Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e3a0c-476d-7542-8f99-59b7391bc61f","input_preview":"保留 LangGraph，只学习 Yu 项目的流程清晰度，不照搬 Yu 的手写 Agent 基类\n","input_message_count":4,"output_preview":"收到，边界确定：**保留 LangGraph，参考 Yu 的流程可见性和统一 ReAct 思路，不照搬 Java 手写基类。**\n\n第二问：工具调用事件展示到什么颗粒度？\n\n我的推荐答案：**中等颗粒度**。前端展示：\n- 第几步\n- 正在调用哪个工具\n- 工具参数的摘要\n- 工具结果的摘要\n- 最终回答\n\n不展示完整原始 JSON、不展示全部工具返回正文，避免聊天气泡噪音太大；完整信息可以放在 "}
{"timestamp":"2026-05-18T07:46:06.211Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e3a0c-82e1-7962-852e-c254092766c9","input_preview":"确认\n","input_message_count":5,"output_preview":"第三问：这次是否要把现有关键词分支全部移除，让“搜索 / 文件 / PDF / 普通问题”都统一进 LangGraph？\n\n我的推荐答案：**全部移除关键词分支**。保留分支会继续造成两套 Agent 逻辑并存，流程图上看起来优化了，实际行为还是不统一；如果担心文件/PDF 工具误触发，就通过 prompt 和工具描述约束，而不是前置 if/else。确认吗？"}
{"timestamp":"2026-05-18T07:47:46.631Z","type":"agent-turn-complete","thread_id":"019e39e9-4f72-7110-970d-db8bcb1d3bee","turn_id":"019e3a0e-013f-7b40-a28b-317483efc886","input_preview":"确认\n","input_message_count":6,"output_preview":"第四问：SSE 的 assistant 记忆回写要不要这次一起做？\n\n我的推荐答案：**一起做**。这是 Agent 流程闭环的一部分，不做的话多轮对话仍然只有用户消息持久化，LangGraph 每次拿到的历史会缺 assistant 回复，后续上下文质量会明显受影响。确认吗？"}
{"timestamp":"2026-05-18T07:58:13.462Z","type":"agent-turn-complete","thread_id":"019e3a17-84a0-7863-b9cc-5140bda95a00","turn_id":"019e3a17-8509-7002-b48b-db9ff22fe2f2","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"优化Agent模块执行链路\"}"}
{"timestamp":"2026-05-18T08:12:37.577Z","type":"agent-turn-complete","thread_id":"019e3a16-5a64-7103-8b3c-e70142c689e6","turn_id":"019e3a17-82f0-7cd2-b239-6e0134318da9","input_preview":"\n# Files mentioned by the user:\n\n## repo-context.md: C:\\Users\\14253\\Desktop\\yu-ai-agent-master\\repo-context.md\n\n## My request for Codex:\n阅读参考一下这个项目的Agent模块，然后根据Agent模块重新优化本项目的Agent模块内容，要完整的Agent执行链路和细","input_message_count":1,"output_preview":"已完成。按 Yu 项目参考，但保留本项目 LangGraph，没有照搬 Java 手写 Agent 基类。\n\n改动：\n- [agent.py](C:/Users/14253/Desktop/ai-hiking/ai-service/agent/agent.py:213)：Agent 流式执行统一走 LangGraph `astream`，移除“搜索/文件/PDF”关键词硬分支。\n- [agent."}
{"timestamp":"2026-05-18T13:25:36.232Z","type":"agent-turn-complete","thread_id":"019e3b30-5598-7233-bc1e-9a7647706db6","turn_id":"019e3b34-5627-7b62-a0ec-1d346e183ed6","input_preview":"\n# Files mentioned by the user:\n\n## repo-context.md: C:\\Users\\14253\\Desktop\\yu-ai-agent-master\\repo-context.md\n\n## My request for Codex:\n根据项目agent模块内容，帮我规划一下Agent模型应该需要有什么工具集。\n然后根据文档内容优化一下目前的Agent的ReA","input_message_count":1,"output_preview":"已完成，根目录新增完整 PRD：\n\n[Agent-PRD.md](<C:/Users/14253/Desktop/ai-hiking/Agent-PRD.md>)\n\n我按项目要求先重新生成并阅读了 `repo-context.md`，又读了 `MEMORY.md`、当前 Agent/ReAct/tool/MCP/memory/SSE 前端链路；随后用 Firecrawl CLI 读取了 LangC"}
{"timestamp":"2026-05-18T17:26:07.799Z","type":"agent-turn-complete","thread_id":"019e3c1f-726b-7160-868c-be93f2602b7c","turn_id":"019e3c1f-7600-76d3-9460-9112a863908a","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"制定徒步Agent改进方案\"}"}
{"timestamp":"2026-05-18T17:30:24.204Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c1f-70e4-7ab0-8a9a-5aaeb5c87977","input_preview":"目前Agent模块的工具集不符合项目主题，一个适用于户外徒步的Agent助手，没有使用的场景，请制定一下改进方案 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) \n","input_message_count":1,"output_preview":""}
{"timestamp":"2026-05-18T17:32:06.262Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c24-d014-78b2-82b9-1fed9cdd7559","input_preview":"回答一下我的疑问，这种Agent助手有必要做那种任务式规划再执行吗?\n","input_message_count":2,"output_preview":"Pivot\n\n有必要做，但不要做成“每次都像 Manus 那样列大计划再一步步执行”。\n\n我的判断是：户外徒步 Agent 需要的是**场景化任务规划**，不是通用任务执行器。因为徒步助手真正有价值的地方在于防漏项：路线、天气、装备、体能、撤退点、安全风险、导出行程，这些如果只靠普通聊天很容易漏。但如果用户只是问“三层穿衣法是什么”或“周末带什么装备”，再搞一套任务计划就显得笨重。\n\n建议分三档："}
{"timestamp":"2026-05-18T17:33:58.658Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c26-8946-7902-81f8-b33bc097fd88","input_preview":"加上新规划的这些tools，总共有多少个tools，太多tools不会显得很臃肿吗？\n","input_message_count":3,"output_preview":"按上一版方案算：**现有 7 个 + 新增 6 个 = 13 个工具**。\n\n但你这个担心是对的：**如果每轮都把 13 个工具全塞给模型，会很臃肿，也会增加误调用。**  \n所以我的建议不是“堆工具”，而是分层：\n\n- **底层通用工具**：搜索、网页读取、文件、PDF、下载、终端、终止。保留，但大多数时候不直接暴露。\n- **徒步场景工具**：路线简报、天气风险、装备清单、风险评估、知识库检索"}
{"timestamp":"2026-05-18T17:36:26.601Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c28-bee9-78a2-a2a4-67f2cd33e38e","input_preview":"目前的Agent执行链路是怎么样的，使用Prompt➡️ 这样告诉我\n","input_message_count":4,"output_preview":"按当前代码，Agent 执行链路大概是这样：\n\n```text\n用户 Prompt\n➡️ 前端 SuperAgent 发送 POST /api/v1/chat/sse\n➡️ Go Gateway 转发到 Python AI Service /chat/sse\n➡️ chat_sse 读取 chat_id 对应的历史消息\n➡️ 先把用户消息写入 FileChatMemory\n➡️ 创建 AIAgen"}
{"timestamp":"2026-05-18T17:38:36.406Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c2a-b9b2-7562-86b0-c6e4a2bb6379","input_preview":"目前这种Agent使用LangGraph是不是没有什么必要，因为不需要用户手动确认是否执行，没有目录文件夹，也不用Agent操控数据\n","input_message_count":5,"output_preview":"Pivot\n\n你这个判断基本是对的：**以目前形态看，LangGraph 的必要性不强。**\n\n现在它主要只承担了：\n\n```text\nPrompt\n➡️ ReAct 循环\n➡️ 工具调用\n➡️ 工具结果回填\n➡️ 流式输出\n```\n\n但项目暂时没有用到 LangGraph 最值钱的部分：\n\n```text\n人工确认 / interrupt\n➡️ checkpoint 恢复\n➡️ 多节点状态流转\n"}
{"timestamp":"2026-05-18T17:42:41.986Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c2e-6c7f-7193-b7c5-eea798990367","input_preview":"我的目的是做一个可以使用tools获取到目前的天气、地理位置等信息，给用户提供户外徒步方面建议的Agent。这个是核心目标，长一点就是收集多方资料，写成一个完整的markdown或者PDF文档输出。还有，在用户prompt输入的时候，有必要做一层query改写吗？\n","input_message_count":6,"output_preview":"有必要做一层，但我建议不要叫“query 改写”，而叫 **意图识别 + 槽位提取 + 检索改写**。\n\n你的核心目标不是通用 Agent，而是：\n\n```text\n用户 Prompt\n➡️ 识别徒步需求\n➡️ 提取地点 / 日期 / 天数 / 经验 / 偏好\n➡️ 调用天气、地理位置、路线资料、知识库等 tools\n➡️ 做徒步安全与装备判断\n➡️ 输出建议\n➡️ 必要时生成 Markdown "}
{"timestamp":"2026-05-18T17:44:54.549Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c30-812b-7892-948e-ade6e7e8e430","input_preview":"Agent的功能有必要和RAG彻底分开吗？\n","input_message_count":7,"output_preview":"不建议**彻底分开**。更准确的做法是：**架构上分层，产品上打通**。\n\nRAG 应该是 Agent 的一个核心工具，而不是另一个完全孤立的功能。你的目标是户外徒步助手，Agent 需要同时调用：\n\n```text\n天气 tool\n➡️ 地理位置 / 海拔 tool\n➡️ 路线资料搜索 tool\n➡️ RAG 知识库 tool\n➡️ 风险评估 tool\n➡️ Markdown / PDF 导出 "}
{"timestamp":"2026-05-18T17:50:12.852Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c34-952c-7a40-bdef-89736c2bb78d","input_preview":"目前我有一套记忆系统，但是目前的编排有点让我不满意，我该往什么方向进行修改\n","input_message_count":8,"output_preview":"🥷我的建议：**不要继续把记忆做成“每轮 Prompt 前自动压缩 + 自动提取 + 自动注入”的黑盒**。你应该把它改成一个更清晰的 **读记忆 / 用记忆 / 写记忆** 三段式编排。\n\n目前的问题大概是：\n\n```text\n用户 Prompt\n➡️ 读取历史\n➡️ MemoryManager.process_interaction(history, query)\n   ➡️ 压缩历史\n  "}
{"timestamp":"2026-05-18T17:56:59.851Z","type":"agent-turn-complete","thread_id":"019e3c1e-8308-7720-8ca8-64d1acc7c24c","turn_id":"019e3c38-10f7-7422-8445-8381a5d3ee48","input_preview":"将刚刚目前我们聊天的上下文进行总结，按照你的建议和计划，写成一个计划书，使用 [$humanizer-zh](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\humanizer-zh\\\\SKILL.md) 进行文本优化，将要执行的编排成多个任务，输出markdown文档。\n","input_message_count":9,"output_preview":"已写好计划书：[AI-Hiking-Agent改造计划书.md](C:/Users/14253/Desktop/ai-hiking/AI-Hiking-Agent改造计划书.md)。\n\n我也按项目要求重新生成了 `repo-context.md`，读取了 `MEMORY.md` 和你指定的 `humanizer-zh` 技能，并在 [MEMORY.md](C:/Users/14253/Deskto"}
{"timestamp":"2026-05-18T17:58:47.620Z","type":"agent-turn-complete","thread_id":"019e3c3d-5ac1-72b0-83b3-d5d425795057","turn_id":"019e3c3d-5ba6-72d3-958e-3a134b595067","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"Reply to greeting\"}"}
{"timestamp":"2026-05-18T17:58:54.529Z","type":"agent-turn-complete","thread_id":"019e3c3d-5687-72b3-b471-53527e4aef0c","turn_id":"019e3c3d-59f1-7383-95d8-f6affc75c383","input_preview":"hi\n","input_message_count":1,"output_preview":"你好，我在。需要我处理这个项目时，我会先按 `AGENTS.md` 生成并阅读 `repo-context.md` 和 `MEMORY.md`。"}
{"timestamp":"2026-05-18T17:59:39.470Z","type":"agent-turn-complete","thread_id":"019e3c3d-5687-72b3-b471-53527e4aef0c","turn_id":"019e3c3e-42bc-7d70-8729-674e8cac4664","input_preview":"你是什么模型？\n","input_message_count":2,"output_preview":"我是 Codex，基于 GPT-5 的编码代理，在这个 Codex 桌面环境里和你共享当前工作区。"}
{"timestamp":"2026-05-18T18:00:18.770Z","type":"agent-turn-complete","thread_id":"019e3c3d-3186-78c3-adce-9a8ea1e12314","turn_id":"019e3c3d-32a5-7f12-8636-7c62ec127155","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"appId\":\"\",\"description\":\"昨晚你刚把户外 Agent 的改造计划书和 PRD 写到位，里面最明确的未落地项就是把通用 7 工具收口成徒步场景工具。这个线程可以直接先做 `weather_lookup`、`geo_lookup`、`route_research` 的第一版，并接进现有 Agent 链路。\",\"prompt\":\"按根目录最新的"}
{"timestamp":"2026-05-18T18:01:31.818Z","type":"agent-turn-complete","thread_id":"019e3c3f-df8d-75c0-832b-79ccb2e624dd","turn_id":"019e3c3f-e020-7611-9078-359f0a0cfd5d","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"按计划改造项目模块\"}"}
````

## File: .omx/logs/turns-2026-05-19.jsonl
````
{"timestamp":"2026-05-19T02:21:48.329Z","type":"agent-turn-complete","thread_id":"019e3e09-df0b-70e0-b694-ad54e2bec4a6","turn_id":"019e3e09-df81-7cf3-8181-65af5c049522","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"配置 opencode 使用 tmux\"}"}
{"timestamp":"2026-05-19T02:24:16.960Z","type":"agent-turn-complete","thread_id":"019e3e09-6b8d-7983-a25f-31ce8f890ede","turn_id":"019e3e09-6c56-7d53-93dd-ea58e846e638","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"appId\":\"\",\"description\":\"今天刚完成 Agent Phase 1 改造，但前端还只是把 `approval_required` 当普通流事件看，后端的 `/api/v1/chat/confirm` 和 `/pending/{chat_id}` 已经在位。把确认面板接上后，高风险导出和写文件流程才真正可用。\",\"prompt\":\"按 AGE"}
{"timestamp":"2026-05-19T06:34:28.822Z","type":"agent-turn-complete","thread_id":"019e3ef1-3125-7ff2-b327-dfbd60b22117","turn_id":"019e3ef1-320d-78c0-90b3-57efb312f67c","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复这个问题\"}"}
{"timestamp":"2026-05-19T06:56:39.157Z","type":"agent-turn-complete","thread_id":"019e3f05-73b6-78c2-8c11-a368bf06d425","turn_id":"019e3f05-7459-7d91-afa7-6c398712505f","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"检查Agent工具集缺项\"}"}
{"timestamp":"2026-05-19T07:01:30.045Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f05-7306-7292-91df-bf6a1db66162","input_preview":"检查一下目前Agent模块工具集的配置是否完善，还缺少什么\n","input_message_count":1,"output_preview":"**结论**\n\nAgent 工具集“基础配置已对齐”，但还没到生产级完善。当前 14 个本地工具都已在实现映射和注册表中对齐：7 个基础可见工具 + 7 个徒步领域隐藏工具。意图路由也会按场景缩小工具暴露范围。\n\n**主要缺口**\n\n1. MCP 还没接入 Agent 主循环  \n   [mcp/client.py](C:/Users/14253/Desktop/ai-hiking/ai-serv"}
{"timestamp":"2026-05-19T07:11:51.603Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f10-02c9-7840-b17f-91494ec5a5b0","input_preview":"[$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 使用技能规划一下以上问题的修复方案。\n[$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 使用进技能约束一下最小修复范围\n[$caveman](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\ca","input_message_count":3,"output_preview":"🥷 **Pivot**：做最小闭环修复，不做大版本升级。\n\n▎[🟠 阿里味] 底层逻辑：先补“可治理、可观测、可验证”的配置缺口，别把 Phase 5 MCP/真 HITL 一口吃成架构返工。\n\n**前提假设**\n- 当前依赖保持 `langchain==0.3.0`、`langgraph==0.2.0`。\n- 不升级 LangChain 1.x，不引入新服务。\n- 本轮只修 Agent 工具"}
{"timestamp":"2026-05-19T07:30:05.886Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f15-2f15-7aa1-ad05-23ed6df56951","input_preview":"Another language model started to solve this problem and produced a summary of its thinking process. You also have access to the state of the tools that were used by that language model. Use this to b","input_message_count":5,"output_preview":"▎[🟠 阿里味] 闭环完成，数据在这。\n\n已实现 Agent 工具集最小修复范围：\n\n- 新增工具清单/健康接口：[api/tools.py](C:/Users/14253/Desktop/ai-hiking/ai-service/api/tools.py)\n- 注册接口路由：[main.py](C:/Users/14253/Desktop/ai-hiking/ai-service/main.p"}
{"timestamp":"2026-05-19T07:33:14.407Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f26-ed75-79e0-9595-13578eb7606d","input_preview":"MCP的作用是什么？\n","input_message_count":6,"output_preview":"MCP = **Model Context Protocol**。作用：让 Agent 用统一协议接外部工具、数据源、服务。\n\n在这个项目里，它主要是：\n\n1. **扩展工具集**  \n   让 Agent 后续能接外部工具，比如地图、天气、文档系统、浏览器、数据库、公司内部服务。\n\n2. **统一工具调用格式**  \n   不同服务不用各写一套接入逻辑，MCP server 暴露工具，Agent"}
{"timestamp":"2026-05-19T07:34:28.688Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f27-62b8-7cb1-b56f-3cf84abb985f","input_preview":"我是说本项目的MCP\n","input_message_count":7,"output_preview":"本项目 MCP 具体作用：**给 Agent 接入独立图片搜索工具**。\n\n当前有两块：\n\n1. **MCP Server**\n   [mcp-server/image_search/server.py](C:/Users/14253/Desktop/ai-hiking/mcp-server/image_search/server.py)\n\n   暴露 `search_images(query, "}
{"timestamp":"2026-05-19T07:40:19.604Z","type":"agent-turn-complete","thread_id":"019e3f2b-015c-7d43-b8d2-2c30e360c39b","turn_id":"019e3f2b-01e3-7352-a204-4ec14586cee6","input_preview":"# Overview\n\nGenerate 0 to 3 hyperpersonalized suggestions for what this user can do with Codex in this local project: C:\\Users\\14253\\Desktop\\ai-hiking\n\nGet an understanding of the user's intent and go","input_message_count":1,"output_preview":"{\"suggestions\":[{\"appId\":\"\",\"description\":\"今天你刚把 Agent 工具集后端审计和 `/api/v1/tools`、`/api/v1/tools/health` 补齐，但前端还看不到这批新数据。把 SuperAgent 接上工具清单和 MCP/本地工具健康状态后，你就不用再靠读代码确认当前到底暴露了什么能力。\",\"prompt\":\"按 AGENTS.md"}
{"timestamp":"2026-05-19T07:41:10.475Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f2a-eb81-79f3-bdbb-2051857d144b","input_preview":"启动项目\n","input_message_count":8,"output_preview":"项目已启动并验证通过。\n\n访问地址：\n\n- 前端 Agent：<http://127.0.0.1:5173/super-agent>\n- 前端 RAG：<http://127.0.0.1:5173/love-master>\n- Gateway：<http://127.0.0.1:8080/health>\n- AI Service：<http://127.0.0.1:8000/health>\n- 工"}
{"timestamp":"2026-05-19T08:03:18.730Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f3d-6a43-7d41-b1e4-2367bafe7eb1","input_preview":"\n# In app browser:\n- The user has the in-app browser open.\n- Current URL: http://127.0.0.1:5173/love-master\n\n## My request for Codex:\n修复一下500报错的问题\n","input_message_count":9,"output_preview":"已修复 500。\n\n根因：`/api/v1/chat/sse` 在进入 SSE 流之前就构造 `AIAgent()`，但当前主模型缺 `OPENAI_API_KEY`，`ChatOpenAI` 初始化直接抛异常，导致 HTTP 500。\n\n改动：\n\n- [ai-service/api/chat.py](C:/Users/14253/Desktop/ai-hiking/ai-service/api/"}
{"timestamp":"2026-05-19T08:26:16.579Z","type":"agent-turn-complete","thread_id":"019e3f03-c4ba-7e03-8656-c12ff782f3b2","turn_id":"019e3f48-6cfd-7013-a9d0-2e7e072789ab","input_preview":"Another language model started to solve this problem and produced a summary of its thinking process. You also have access to the state of the tools that were used by that language model. Use this to b","input_message_count":10,"output_preview":"不是缺新的模型。问题是 Agent 的 **Memory 子模块** 还在读后端 `.env` 里的 `OPENAI_API_KEY`，没有使用你在 `/llm-config` 保存并随请求传来的 LLM 配置。\n\n已修复：运行时 `model_settings.llm` 现在会同时传给：\n\n- Agent 主 LLM\n- Memory 的会话压缩 `SessionCompressor`\n- Me"}
{"timestamp":"2026-05-19T08:33:13.084Z","type":"agent-turn-complete","thread_id":"019e3f5d-c416-7731-a5d8-af5bceefb503","turn_id":"019e3f5d-c49d-73a3-893a-cd5ee0aa10c4","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"优化工具调用和思考动画\"}"}
{"timestamp":"2026-05-19T08:51:00.309Z","type":"agent-turn-complete","thread_id":"019e3f5c-1d36-7170-b332-9af526c5e71c","turn_id":"019e3f5d-c36b-73f1-a9f4-91eba5f0220c","input_preview":"1.优化一下项目这里的工具调用逻辑，我已经适配了高德地图的api，我进行提问之后，用户应该调用我目前的定位信息，然后获取地理位置进行回答。\n2.修复一下思考动画，要求和RAG模块一样 \n[$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md)  [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\","input_message_count":1,"output_preview":"已完成。\n\n改动重点：\n- [SuperAgent.tsx](C:\\Users\\14253\\Desktop\\ai-hiking\\frontend\\src\\pages\\SuperAgent.tsx:108)：发送 Agent 消息前读取浏览器定位，成功时随 `current_location` 发给后端；定位失败或拒绝时不阻断对话。\n- [models.py](C:\\Users\\14253\\Desk"}
{"timestamp":"2026-05-19T09:05:15.734Z","type":"agent-turn-complete","thread_id":"019e3f7b-44f6-7ce1-8a2e-485f2bb1f694","turn_id":"019e3f7b-45c4-7112-ad29-b845df8f5e13","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"修复工具调用与回答优化\"}"}
{"timestamp":"2026-05-19T09:35:05.219Z","type":"agent-turn-complete","thread_id":"019e3f96-8a65-7532-a386-7233087a13b4","turn_id":"019e3f96-8d53-7531-a463-fed70a028036","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"调整LLM策略与System Prompt\"}"}
{"timestamp":"2026-05-19T09:43:38.850Z","type":"agent-turn-complete","thread_id":"019e3f96-85cf-7c93-a593-d8b1c9014896","turn_id":"019e3f96-86b6-77d2-a89f-62da03e684c7","input_preview":"\n# Files mentioned by the user:\n\n## a5d25cd7-a5c5-48e8-bad5-af1eda56b4f1.png: C:/Users/14253/AppData/Local/Temp/a5d25cd7-a5c5-48e8-bad5-af1eda56b4f1.png\n\n## My request for Codex:\n##修复一下问题\n1.目前llm的策略不对","input_message_count":1,"output_preview":"▎[🔴 华为味] 闭环完成。根因不是模型笨，是策略给了它过度行动空间；现在把炮火收窄了。\n\n已修：\n\n- [prompts.py](C:/Users/14253/Desktop/ai-hiking/ai-service/agent/prompts.py:1)：System Prompt 改成图里那种 `<Role>/<Goal>/<Constraints>/<Tools>/<Format>/<E"}
{"timestamp":"2026-05-19T09:53:08.651Z","type":"agent-turn-complete","thread_id":"019e3f96-85cf-7c93-a593-d8b1c9014896","turn_id":"019e3fa5-66f9-7a43-adaa-5cee102cca7f","input_preview":"分析一下有没有必要增加语义缓存，还有RAG模块\n","input_message_count":2,"output_preview":""}
{"timestamp":"2026-05-19T09:56:06.470Z","type":"agent-turn-complete","thread_id":"019e3fa9-caa4-7d31-9dc4-770d2547214b","turn_id":"019e3fa9-cb1b-7200-9a58-50c9691f6818","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"查找任务退出方案\"}"}
{"timestamp":"2026-05-19T09:58:17.129Z","type":"agent-turn-complete","thread_id":"019e3fa8-e51c-76a3-a071-888dd38a852e","turn_id":"019e3faa-002f-74f2-8967-0f5fa9ea7fe7","input_preview":"目前Agent系统中有一个合理地让任务退出的组件吗\n","input_message_count":2,"output_preview":"有，但只能算“轻量退出工具”，还不是完整的任务退出组件。\n\n当前代码里有 `terminate`：\n\n- [terminate.py](C:/Users/14253/Desktop/ai-hiking/ai-service/tools/terminate.py:4)：定义了 `terminate(reason)`，说明是任务完成或无法继续时调用。\n- [agent.py](C:/Users/142"}
{"timestamp":"2026-05-19T10:17:45.517Z","type":"agent-turn-complete","thread_id":"019e3fa8-e51c-76a3-a071-888dd38a852e","turn_id":"019e3fb2-9f0c-7d53-85df-b2ee46057509","input_preview":"1.使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\think\\\\SKILL.md) 进行规划，然后使用 [$pua](C:\\\\Users\\\\14253\\\\.codex\\\\skills\\\\pua\\\\SKILL.md) 进行约束和行事分割调整，创建一个合理让Agent他退出的组件，最后使用 [$tdd](C:\\\\Users\\\\14253\\\\.agents","input_message_count":3,"output_preview":"完成了。现在 Agent 有了一个真正的轻量退出组件，而不是只靠 `terminate` 普通工具结果糊过去。\n\n改动核心：\n\n- 新增 [task_exit.py](C:/Users/14253/Desktop/ai-hiking/ai-service/agent/task_exit.py:51)：`AgentTaskExitController` 统一处理 `completed / waiti"}
{"timestamp":"2026-05-19T10:24:09.521Z","type":"agent-turn-complete","thread_id":"019e3fc3-7401-7cd1-9325-fc103cf69d31","turn_id":"019e3fc3-789e-7592-88da-0ceb940f0145","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"添加对话记忆进度条\"}"}
{"timestamp":"2026-05-19T10:35:39.104Z","type":"agent-turn-complete","thread_id":"019e3fc3-6efd-74b2-9051-78b4b234968d","turn_id":"019e3fc3-6ff3-7972-8d9d-01f813426cf6","input_preview":"根据目前的记忆系统，给Agent和RAG模块单个对话增加一个对话记忆进度条，要求UI统一 ，放在合适的地方，使用 [$design-taste-frontend](C:\\\\Users\\\\14253\\\\.agents\\\\skills\\\\design-taste-frontend\\\\SKILL.md) 进行设计，然后使用 [$think](C:\\\\Users\\\\14253\\\\.agents\\\\skil","input_message_count":1,"output_preview":"▎[Musk味] 已闭环：不是只把条放上去，而是把桌面和移动端都验证了，避免“看起来做完”的假交付。\n\n已完成：Agent 和 RAG 的单个对话顶部都新增了统一的“对话记忆”进度条，基于当前记忆系统的 60 条消息窗口计算进度。共享实现放在 [ConversationMemoryMeter.tsx](</C:/Users/14253/Desktop/ai-hiking/frontend/src/"}
{"timestamp":"2026-05-19T10:38:29.224Z","type":"agent-turn-complete","thread_id":"019e3fc3-6efd-74b2-9051-78b4b234968d","turn_id":"019e3fd0-6af8-74e0-9175-00c265d31b50","input_preview":"目前超过60条对话之后会怎么样\n","input_message_count":2,"output_preview":"目前超过 60 条后：\n\n1. **Agent 后端记忆会滑动截断**\n   `FileChatMemory` 的窗口是 `60` 条消息。超过后只保留最近 60 条，最旧的消息会从后端对话记忆文件里被丢掉。这里的“条”是 message，不是一轮对话；一轮用户+助手通常算 2 条，所以大约 30 轮。\n\n2. **Agent 前端历史仍会显示更长**\n   前端 `localStorage` 里"}
{"timestamp":"2026-05-19T11:58:26.671Z","type":"agent-turn-complete","thread_id":"019e4019-cce8-7f50-b853-79811d352298","turn_id":"019e4019-cf8d-7591-b0a9-1282ab31ddc9","input_preview":"You are a helpful assistant. You will be presented with a user prompt, and your job is to provide a short title for a task that will be created from that prompt.\nThe tasks typically have to do with co","input_message_count":1,"output_preview":"{\"title\":\"优化徒步天气流程\"}"}
````

## File: .omx/metrics.json
````json
{
  "total_turns": 95,
  "session_turns": 95,
  "last_activity": "2026-05-19T11:58:26.683Z",
  "session_input_tokens": 0,
  "session_output_tokens": 0,
  "session_total_tokens": 0
}
````

## File: .omx/state/hud-state.json
````json
{
  "last_turn_at": "2026-05-19T11:58:26.759Z",
  "turn_count": 94,
  "last_progress_at": "2026-05-19T11:58:26.759Z",
  "last_agent_output": "{\"title\":\"优化徒步天气流程\"}"
}
````

## File: .omx/state/notify-hook-state.json
````json
{
  "recent_turns": {
    "019e3b30-5598-7233-bc1e-9a7647706db6|019e3b34-5627-7b62-a0ec-1d346e183ed6|agent-turn-complete": 1779110736224,
    "019e3c1f-726b-7160-868c-be93f2602b7c|019e3c1f-7600-76d3-9460-9112a863908a|agent-turn-complete": 1779125167794,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c1f-70e4-7ab0-8a9a-5aaeb5c87977|agent-turn-complete": 1779125424198,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c24-d014-78b2-82b9-1fed9cdd7559|agent-turn-complete": 1779125526256,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c26-8946-7902-81f8-b33bc097fd88|agent-turn-complete": 1779125638653,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c28-bee9-78a2-a2a4-67f2cd33e38e|agent-turn-complete": 1779125786595,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c2a-b9b2-7562-86b0-c6e4a2bb6379|agent-turn-complete": 1779125916400,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c2e-6c7f-7193-b7c5-eea798990367|agent-turn-complete": 1779126161980,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c30-812b-7892-948e-ade6e7e8e430|agent-turn-complete": 1779126294544,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c34-952c-7a40-bdef-89736c2bb78d|agent-turn-complete": 1779126612846,
    "019e3c1e-8308-7720-8ca8-64d1acc7c24c|019e3c38-10f7-7422-8445-8381a5d3ee48|agent-turn-complete": 1779127019845,
    "019e3c3d-5ac1-72b0-83b3-d5d425795057|019e3c3d-5ba6-72d3-958e-3a134b595067|agent-turn-complete": 1779127127615,
    "019e3c3d-5687-72b3-b471-53527e4aef0c|019e3c3d-59f1-7383-95d8-f6affc75c383|agent-turn-complete": 1779127134523,
    "019e3c3d-5687-72b3-b471-53527e4aef0c|019e3c3e-42bc-7d70-8729-674e8cac4664|agent-turn-complete": 1779127179465,
    "019e3c3d-3186-78c3-adce-9a8ea1e12314|019e3c3d-32a5-7f12-8636-7c62ec127155|agent-turn-complete": 1779127218763,
    "019e3c3f-df8d-75c0-832b-79ccb2e624dd|019e3c3f-e020-7611-9078-359f0a0cfd5d|agent-turn-complete": 1779127291813,
    "019e3e09-df0b-70e0-b694-ad54e2bec4a6|019e3e09-df81-7cf3-8181-65af5c049522|agent-turn-complete": 1779157308324,
    "019e3e09-6b8d-7983-a25f-31ce8f890ede|019e3e09-6c56-7d53-93dd-ea58e846e638|agent-turn-complete": 1779157456955,
    "019e3ef1-3125-7ff2-b327-dfbd60b22117|019e3ef1-320d-78c0-90b3-57efb312f67c|agent-turn-complete": 1779172468817,
    "019e3f05-73b6-78c2-8c11-a368bf06d425|019e3f05-7459-7d91-afa7-6c398712505f|agent-turn-complete": 1779173799152,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f05-7306-7292-91df-bf6a1db66162|agent-turn-complete": 1779174090039,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f10-02c9-7840-b17f-91494ec5a5b0|agent-turn-complete": 1779174711595,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f15-2f15-7aa1-ad05-23ed6df56951|agent-turn-complete": 1779175805880,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f26-ed75-79e0-9595-13578eb7606d|agent-turn-complete": 1779175994402,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f27-62b8-7cb1-b56f-3cf84abb985f|agent-turn-complete": 1779176068683,
    "019e3f2b-015c-7d43-b8d2-2c30e360c39b|019e3f2b-01e3-7352-a204-4ec14586cee6|agent-turn-complete": 1779176419571,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f2a-eb81-79f3-bdbb-2051857d144b|agent-turn-complete": 1779176470469,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f3d-6a43-7d41-b1e4-2367bafe7eb1|agent-turn-complete": 1779177798725,
    "019e3f03-c4ba-7e03-8656-c12ff782f3b2|019e3f48-6cfd-7013-a9d0-2e7e072789ab|agent-turn-complete": 1779179176572,
    "019e3f5d-c416-7731-a5d8-af5bceefb503|019e3f5d-c49d-73a3-893a-cd5ee0aa10c4|agent-turn-complete": 1779179593076,
    "019e3f5c-1d36-7170-b332-9af526c5e71c|019e3f5d-c36b-73f1-a9f4-91eba5f0220c|agent-turn-complete": 1779180660303,
    "019e3f7b-44f6-7ce1-8a2e-485f2bb1f694|019e3f7b-45c4-7112-ad29-b845df8f5e13|agent-turn-complete": 1779181515729,
    "019e3f96-8a65-7532-a386-7233087a13b4|019e3f96-8d53-7531-a463-fed70a028036|agent-turn-complete": 1779183305214,
    "019e3f96-85cf-7c93-a593-d8b1c9014896|019e3f96-86b6-77d2-a89f-62da03e684c7|agent-turn-complete": 1779183818843,
    "019e3f96-85cf-7c93-a593-d8b1c9014896|019e3fa5-66f9-7a43-adaa-5cee102cca7f|agent-turn-complete": 1779184388645,
    "019e3fa9-caa4-7d31-9dc4-770d2547214b|019e3fa9-cb1b-7200-9a58-50c9691f6818|agent-turn-complete": 1779184566464,
    "019e3fa8-e51c-76a3-a071-888dd38a852e|019e3faa-002f-74f2-8967-0f5fa9ea7fe7|agent-turn-complete": 1779184697123,
    "019e3fa8-e51c-76a3-a071-888dd38a852e|019e3fb2-9f0c-7d53-85df-b2ee46057509|agent-turn-complete": 1779185865512,
    "019e3fc3-7401-7cd1-9325-fc103cf69d31|019e3fc3-789e-7592-88da-0ceb940f0145|agent-turn-complete": 1779186249514,
    "019e3fc3-6efd-74b2-9051-78b4b234968d|019e3fc3-6ff3-7972-8d9d-01f813426cf6|agent-turn-complete": 1779186939098,
    "019e3fc3-6efd-74b2-9051-78b4b234968d|019e3fd0-6af8-74e0-9175-00c265d31b50|agent-turn-complete": 1779187109218,
    "019e4019-cce8-7f50-b853-79811d352298|019e4019-cf8d-7591-b0a9-1282ab31ddc9|agent-turn-complete": 1779191906666
  },
  "last_event_at": "2026-05-19T11:58:26.668Z"
}
````

## File: .omx/state/session.json
````json
{
  "session_id": "019e4019-c724-74c1-8b97-ee896d9bea78",
  "native_session_id": "019e4019-c724-74c1-8b97-ee896d9bea78",
  "started_at": "2026-05-19T12:02:37.424Z",
  "cwd": "C:\\Users\\14253\\Desktop\\ai-hiking",
  "pid": 26832,
  "platform": "win32"
}
````

## File: .omx/state/sessions/019e30a2-25ee-7121-a02a-2e915835f249/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:adee2f9471d40536503b70c24ea048acf054dc1619c33d819b952deae529412b",
    "turn_id": "019e30a2-266d-7593-ba77-2404bcfae203",
    "created_at": "2026-05-16T11:53:22.862Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3104-76e4-7ac3-901b-8f37bd81ff00/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:baa435426a3b50060e456d9923d85b4600fb46a39e11aac96ac6b717ef6846e2",
    "turn_id": "019e3104-7793-7e72-a2f6-ab700bab9544",
    "created_at": "2026-05-16T13:40:52.914Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3637-0c5d-7492-8205-61c8653c23b8/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:247ffab64878d8e1b00d381844171260dfdd07b36fbb03dfac6c170f146507a0",
    "turn_id": "019e3637-0d12-79f1-9509-717595fe1d44",
    "created_at": "2026-05-17T13:54:09.688Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3637-5de3-7e10-99f9-54ce396e991f/skill-active-state.json
````json
{
  "version": 1,
  "active": true,
  "skill": "tdd",
  "keyword": "$tdd",
  "phase": "planning",
  "activated_at": "2026-05-17T14:25:52.949Z",
  "updated_at": "2026-05-17T14:25:52.949Z",
  "source": "keyword-detector",
  "session_id": "019e3637-5de3-7e10-99f9-54ce396e991f",
  "thread_id": "",
  "turn_id": "019e3654-436a-7f82-9350-d8351c8317ce",
  "active_skills": [
    {
      "skill": "tdd",
      "phase": "planning",
      "active": true,
      "activated_at": "2026-05-17T14:25:52.949Z",
      "updated_at": "2026-05-17T14:25:52.949Z",
      "session_id": "019e3637-5de3-7e10-99f9-54ce396e991f",
      "thread_id": "",
      "turn_id": "019e3654-436a-7f82-9350-d8351c8317ce"
    }
  ]
}
````

## File: .omx/state/sessions/019e3701-953a-72d0-ac5f-91d4a33c67d6/hud-state.json
````json
{
  "last_turn_at": "2026-05-17T18:36:28.263Z",
  "turn_count": 1,
  "last_progress_at": "2026-05-17T18:36:28.263Z",
  "last_agent_output": "已完成。\n\n**改动**\n- RAG 上传流程已改成：统一接入/格式化 -> 正则降噪 -> 混合分块 -> 元数据标记 -> embedding -> PGVector。\n- RAG 查询流程已改成"
}
````

## File: .omx/state/sessions/019e3701-953a-72d0-ac5f-91d4a33c67d6/notify-hook-state.json
````json
{
  "recent_turns": {
    "019e3701-953a-72d0-ac5f-91d4a33c67d6|019e3734-d041-7030-9066-75a5c5a1cb5d|agent-turn-complete": 1779042988147
  },
  "last_event_at": "2026-05-17T18:36:28.152Z"
}
````

## File: .omx/state/sessions/019e395f-c99b-7563-9f9a-d5ef33cc59e5/skill-active-state.json
````json
{
  "version": 1,
  "active": true,
  "skill": "tdd",
  "keyword": "Tdd",
  "phase": "planning",
  "activated_at": "2026-05-18T04:58:18.791Z",
  "updated_at": "2026-05-18T06:03:01.049Z",
  "source": "keyword-detector",
  "session_id": "019e395f-c99b-7563-9f9a-d5ef33cc59e5",
  "thread_id": "",
  "turn_id": "019e39ae-3669-7ac2-a742-032d6fbe3252",
  "active_skills": [
    {
      "skill": "tdd",
      "phase": "planning",
      "active": true,
      "activated_at": "2026-05-18T04:58:18.791Z",
      "updated_at": "2026-05-18T06:03:01.049Z",
      "session_id": "019e395f-c99b-7563-9f9a-d5ef33cc59e5",
      "thread_id": "",
      "turn_id": "019e39ae-3669-7ac2-a742-032d6fbe3252"
    }
  ]
}
````

## File: .omx/state/sessions/019e39e8-5f3d-71c1-a914-74ff757bd5ad/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:8e07092d64de3f08c1664cd19716e76cb913ea0d305e47ddd31aa32508d32990",
    "turn_id": "019e39e8-6026-7690-b2b1-572de03072fe",
    "created_at": "2026-05-18T07:06:37.218Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3a16-5a64-7103-8b3c-e70142c689e6/skill-active-state.json
````json
{
  "version": 1,
  "active": true,
  "skill": "tdd",
  "keyword": "Tdd",
  "phase": "planning",
  "activated_at": "2026-05-18T07:58:01.669Z",
  "updated_at": "2026-05-18T07:58:01.669Z",
  "source": "keyword-detector",
  "session_id": "019e3a16-5a64-7103-8b3c-e70142c689e6",
  "thread_id": "",
  "turn_id": "019e3a17-82f0-7cd2-b239-6e0134318da9",
  "active_skills": [
    {
      "skill": "tdd",
      "phase": "planning",
      "active": true,
      "activated_at": "2026-05-18T07:58:01.669Z",
      "updated_at": "2026-05-18T07:58:01.669Z",
      "session_id": "019e3a16-5a64-7103-8b3c-e70142c689e6",
      "thread_id": "",
      "turn_id": "019e3a17-82f0-7cd2-b239-6e0134318da9"
    }
  ]
}
````

## File: .omx/state/sessions/019e3c1e-8308-7720-8ca8-64d1acc7c24c/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "LIGHT",
    "destination": "explore",
    "reason": "question_or_explanation",
    "prompt_signature": "sha256:4682ff6c6ddb09ecfcbe9ce941809902c05afb7bbd6ccd72916a793e6b9eb176",
    "turn_id": "019e3c24-d014-78b2-82b9-1fed9cdd7559",
    "created_at": "2026-05-18T17:31:46.544Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3c3d-3186-78c3-adce-9a8ea1e12314/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:446afa6f9da6dd89b06b231f50e39394d759b257613e9b36f31e35ce2ac6c081",
    "turn_id": "019e3c3d-32a5-7f12-8636-7c62ec127155",
    "created_at": "2026-05-18T17:58:30.439Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3e06-b481-7b82-a53f-364e6e0c13c5/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:5561a723c4dd7b2b0c390eb968c30b73cd000807980345c2d8e905de22f53376",
    "turn_id": "019e3e06-b521-70e2-aa56-e0bf2d84d6fe",
    "created_at": "2026-05-19T02:18:16.253Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3e09-6b8d-7983-a25f-31ce8f890ede/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:5561a723c4dd7b2b0c390eb968c30b73cd000807980345c2d8e905de22f53376",
    "turn_id": "019e3e09-6c56-7d53-93dd-ea58e846e638",
    "created_at": "2026-05-19T02:21:11.791Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3f21-cb5f-70a3-8638-e836d7e5e93e/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:3dd0159d8425f2ce8f2a88fde42166351d0efd8eadecf11641b026b00d26c603",
    "turn_id": "019e3f21-cbda-7272-8d25-9e6f849a03c5",
    "created_at": "2026-05-19T07:27:27.097Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/sessions/019e3f2b-015c-7d43-b8d2-2c30e360c39b/prompt-routing-state.json
````json
{
  "version": 1,
  "last_triage": {
    "lane": "HEAVY",
    "destination": "autopilot",
    "reason": "implementation_research_goal",
    "prompt_signature": "sha256:2aa4beb8f7f3e630fa4c6f62def41d74e6aded78d316b5823ed03a1f88a62867",
    "turn_id": "019e3f2b-01e3-7352-a204-4ec14586cee6",
    "created_at": "2026-05-19T07:37:32.957Z"
  },
  "suppress_followup": true
}
````

## File: .omx/state/skill-active-state.json
````json
{
  "version": 1,
  "active": true,
  "skill": "tdd",
  "keyword": "Tdd",
  "phase": "reviewing",
  "activated_at": "2026-05-18T07:58:13.537Z",
  "updated_at": "2026-05-19T11:58:26.764Z",
  "source": "keyword-detector",
  "input_lock": null
}
````

## File: .omx/state/subagent-tracking.json
````json
{
  "schemaVersion": 1,
  "sessions": {
    "019e3701-953a-72d0-ac5f-91d4a33c67d6": {
      "session_id": "019e3701-953a-72d0-ac5f-91d4a33c67d6",
      "leader_thread_id": "019e3701-953a-72d0-ac5f-91d4a33c67d6",
      "updated_at": "2026-05-17T18:36:28.157Z",
      "threads": {
        "019e3701-953a-72d0-ac5f-91d4a33c67d6": {
          "thread_id": "019e3701-953a-72d0-ac5f-91d4a33c67d6",
          "kind": "leader",
          "first_seen_at": "2026-05-17T18:36:28.157Z",
          "last_seen_at": "2026-05-17T18:36:28.157Z",
          "last_turn_id": "019e3734-d041-7030-9066-75a5c5a1cb5d",
          "turn_count": 1
        }
      }
    }
  }
}
````

## File: .omx/state/team-leader-nudge.json
````json
{
  "last_nudged_by_team": {},
  "last_idle_nudged_by_team": {},
  "progress_by_team": {}
}
````

## File: .omx/state/tmux-hook-state.json
````json
{
  "total_injections": 0,
  "pane_counts": {},
  "session_counts": {},
  "recent_keys": {},
  "last_injection_ts": 0,
  "last_reason": "mode_not_allowed",
  "last_event_at": "2026-05-19T11:58:26.770Z"
}
````

## File: .repomixignore
````
# Ignore virtual environments
ai-service/.conda312/
ai-service/.venv/
.venv/
venv/
env/

# Ignore node modules and package lock files
node_modules/
package-lock.json
pnpm-lock.yaml
yarn.lock

# Ignore build output and temp files
dist/
build/
.tempmediaStorage/
artifacts/
.gemini/
.git/
*.exe
*.log
*.err

# Ignore repomix outputs to avoid recursion
repo-context.md
MEMORY.md
````

## File: .sisyphus/run-continuation/ses_1c4a6b54fffe1Eb5cRxJ3yYoki.json
````json
{
  "sessionID": "ses_1c4a6b54fffe1Eb5cRxJ3yYoki",
  "updatedAt": "2026-05-18T14:57:22.616Z",
  "sources": {
    "background-task": {
      "state": "idle",
      "updatedAt": "2026-05-18T14:57:22.616Z"
    }
  }
}
````

## File: .sisyphus/run-continuation/ses_1ce5e2737ffebAggBXgtATGn3a.json
````json
{
  "sessionID": "ses_1ce5e2737ffebAggBXgtATGn3a",
  "updatedAt": "2026-05-16T16:36:46.141Z",
  "sources": {
    "background-task": {
      "state": "idle",
      "updatedAt": "2026-05-16T16:36:46.141Z"
    }
  }
}
````

## File: .sisyphus/run-continuation/ses_1d2d113a8ffednNHMAhaQFHZsq.json
````json
{
  "sessionID": "ses_1d2d113a8ffednNHMAhaQFHZsq",
  "updatedAt": "2026-05-15T19:53:39.910Z",
  "sources": {
    "background-task": {
      "state": "idle",
      "updatedAt": "2026-05-15T19:53:39.910Z"
    }
  }
}
````

## File: 户外徒步知识文档.md
````markdown
# 户外徒步知识全指南

户外徒步作为一种融合了自然探索、体能锻炼与心灵放松的活动，近年来受到越来越多人的喜爱。它不仅是对个人意志与体能的考验，更是一次与自然深度对话的机会。然而，徒步并非简单的“走路”，其背后涉及系统的知识体系与严谨的安全准备。本文旨在为徒步爱好者提供一份全面、科学且实用的知识指南，内容涵盖徒步的基础认知、装备配置、路线规划、安全防范、体能训练及环保责任，帮助参与者建立理性、安全、可持续的户外理念。

## 一、什么是徒步？——从散步到系统的户外运动

徒步（Hiking）是指在自然环境中进行的中长距离步行活动，通常单程距离不少于5公里，区别于城市中的日常散步或短途健走。其核心目的在于通过持续性的行进过程，亲近自然、挑战自我、提升身心素质，并在过程中培养对环境的敬畏与责任感<sup>[1]</sup>。

### 徒步的核心目的
徒步的价值不仅体现在身体层面的锻炼，如增强心肺功能、提高耐力与协调性，更在于心理层面的成长。研究表明，规律参与百日徒步计划的人群，其焦虑指数平均下降42%，决策失误率减少29%，印证了徒步对现代人精神压力的有效缓解作用<sup>[1]</sup>。

### 主要类型分类
根据强度、形式和场景的不同，徒步可划分为多种类型：

- **按强度分级**：
  - 休闲级：适合初学者，里程≤10km，累计爬升≤500m；
  - 进阶级：具备一定基础者，需应对复杂地形；
  - 挑战级：高海拔、长距离、大爬升线路；
  - 大师级：仅限资深爱好者，常涉及极端气候与无人区穿越。

- **按组织形式**：
  - 轻装日穿：当日往返，不携带露营装备；
  - 重装露营：多日行程，背负帐篷、睡袋等物资；
  - 商业组织：由专业机构带队，提供交通、食宿服务；
  - 自主SOLO：独立完成路线规划与执行，要求极高的综合能力。

- **特殊场景徒步**：
  - 沙漠穿越：面临高温、缺水、风沙等挑战；
  - 雪地徒步：需掌握防滑、保暖与雪崩识别技能；
  - 峡谷探秘：注意落石、湿滑岩壁与突发山洪风险。

![三层穿衣法结构示意图](https://agent.qianwen.com/mos/f8b7fdecce384cfc97cc3228a78bb361/1df099caefe281976dfaa5715179d1af)

## 二、徒步装备系统详解

科学合理的装备配置是保障徒步安全与舒适的关键。一套完整的徒步装备应遵循功能性、轻量化与冗余备份三大原则，确保在各种环境下均能有效应对。

### （一）三层穿衣法：应对多变气候的核心原则

人体在运动过程中会产生大量汗液，若衣物无法及时排湿，将导致体温调节失衡，增加失温风险。因此，“三层穿衣法”成为国际通行的户外着装标准，其结构如下表所示：

| 层级 | 功能 | 推荐材质 | 使用场景 |
|------|------|----------|--------|
| 内层（排汗层） | 吸湿速干 | 美利奴羊毛、聚酯纤维 | 所有季节 |
| 中层（保暖层） | 温度调节 | 抓绒衣、羽绒服、合成棉服 | 春秋冬季、高海拔 |
| 外层（防护层） | 防风防水 | 冲锋衣裤、软壳衣 | 雨天、强风、低温 |

> **提示**：严禁穿着纯棉衣物进入山区，因其吸水后难以干燥，极易引发失温事故。

### （二）徒步鞋的选择与磨合

徒步鞋是徒步活动中最重要的装备之一，直接影响行走稳定性与足部健康。

- **关键指标**：
  - **防水性**：推荐选用GORE-TEX或FLT防水内衬技术产品，保持脚部干爽；
  - **抓地力**：Vibram大底具有优异的耐磨性与湿滑路面附着力；
  - **支撑性**：中高帮设计可有效保护脚踝，防止扭伤，尤其适用于崎岖地形。

- **尺码建议**：由于长时间行走会导致脚部轻微肿胀，建议选择比日常鞋码大0.5–1码的型号。

- **新鞋磨合**：禁止穿着全新徒步鞋进行长途徒步。出发前应在城市道路或低强度山径上累计行走不少于30公里，以适应鞋型并排除潜在磨脚点。

- **常见品牌推荐**：LOWA、Salomon、SCARPA、凯乐石（KAILAS）、探路者（TOREAD）等均为市场认可度较高的专业品牌。

### （三）背包配置与背负系统

背包不仅是装载工具，更是影响体力分配与背部健康的决定性因素。

- **容量匹配原则**：
  - 单日徒步：20–30L，满足基本补给与应急物品存放；
  - 两日露营：30–50L，容纳睡袋、帐篷等露营装备；
  - 多日重装：50L以上，适合远距离穿越任务。

- **背负系统要点**：
  - 腰带承担约70%的重量，必须紧贴髋骨上方；
  - 肩带调节至锁骨下方，避免压迫肩颈神经；
  - 试背时检查“45度法则”：双手前伸呈90度，双臂自然下垂后应能轻松触及背包两侧提手。

- **推荐品牌**：Osprey、Gregory、始祖鸟（Arc'teryx）、Deuter等品牌以其优秀的背负系统与耐用性著称。

### （四）其他必备装备清单

除服装与背包外，以下装备亦属徒步出行的基本配置：

- **登山杖**：减轻膝盖压力可达30%，长度建议为身高×0.66；
- **头灯+备用电池**：用于夜间行进或突发状况照明，确保续航时间超过预计行程；
- **导航工具**：手机APP（如“两步路”“奥维地图”）配合纸质地图与指南针使用，形成双重保障；
- **急救包**：包含碘伏、创可贴、绷带、止血带、抗过敏药及个人常用药品；
- **应急物品**：保温毯、救生哨、多功能刀具、垃圾袋、备用口罩与驱蚊液。

此外，建议携带不少于2升饮用水，并根据气温与行程适当增加；食物方面宜选择高能量、易消化的食品，如能量棒、坚果、八宝粥与盐丸。

## 三、路线规划与难度评估

一条科学合理的徒步路线不仅能带来良好的体验，更能最大限度规避潜在风险。路线规划需结合个人能力、天气条件与地理特征进行综合判断。

### （一）如何科学评估一条徒步路线？

中国登山协会推荐采用以下参数作为路线难度评估依据：

- 总里程
- 累计爬升
- 最高海拔
- 预估耗时

其中，预估耗时可通过以下公式计算：

> 总时间 = (距离 ÷ 3.2) + (爬升 ÷ 305) + 每小时休息5分钟

该公式综合考虑平地行进速度（约3.2km/h）与垂直爬升消耗（每305米加1小时），已被广泛应用于国内徒步圈的实际操作中。

### （二）路线筛选原则

对于初次接触徒步的新手，建议遵循“三六六原则”：

- 至少准备 **3升水**；
- 初次徒步不宜超过 **6公里** 或 **600米海拔差**；
- 行程控制在 **6小时内**。

同时，应优先选择成熟步道，避免进入未开发区域。可通过“两步路”“六只脚”等APP下载离线轨迹，并查看近期他人实际轨迹以确认路况是否通行。此外，务必选择设有下撤点的线路，避免陷入“只能进不能退”的困境。

### （三）热门推荐路线（按难度分级）

| 地点 | 路线名称 | 里程 | 爬升 | 难度 | 特色 |
|------|----------|------|------|------|------|
| 成都邛崃 | 休闲级步道 | 5–8km | <200m | 休闲级 | 全龄友好，路面平坦 |
| 西安 | 蓝关古道环穿 | 12km | ~800m | 初级 | 春季赏景佳选 |
| 云南丽江 | 虎跳峡高路 | 2–3天 | —— | 初级 | 金沙江峡谷壮丽景观 |
| 四川四姑娘山 | 长穿毕 | 3–4天 | —— | 中等 | 幺妹峰日照金山 |

> 注：部分路线信息参考自《徒步百科》及地方文旅部门发布的官方导览资料<sup>[1]</sup>。

## 四、安全须知与风险应对

安全是徒步活动不可逾越的底线。任何忽视风险的行为都可能造成严重后果，甚至危及生命。因此，必须建立系统的风险防控意识。

### （一）行前准备三大原则

1. **心理准备**：树立对自然的敬畏之心，杜绝侥幸心理与“打卡式”心态；
2. **团队管理**：建议4人以上结伴出行，实现“一人遇险，两人求助，一人陪护”的国际通用救援模式；
3. **行程报备**：将详细路线、进出山口位置、预计返回时间告知至少一名亲友，并约定联络机制。

### （二）极端天气应对策略

| 天气 | 风险 | 应对措施 |
|------|------|----------|
| 暴雨 | 山洪、滑坠、失温 | 远离河道，避入岩洞，更换干衣 |
| 雷电 | 雷击高危 | 下撤至低处，双脚并拢蹲姿，禁用电子设备 |
| 浓雾 | 迷路 | 使用GPS+纸质地图，原地等待或原路返回 |
| 暴雪 | 失温、地形覆盖 | 转移至背风区，更换干燥衣物，立即下撤 |

> 特别提醒：收到暴雨橙色及以上预警时，应直接取消行程；雷暴发生时，切勿停留在山顶、山脊或孤立树下。

### （三）常见伤病处理

#### 失温分级与应对

| 分级 | 体温 | 症状 | 处理方式 |
|------|------|------|----------|
| 轻度 | 33–35℃ | 寒战、言语不清 | 停止运动，换干衣，喝温糖水 |
| 重度 | <32℃ | 意识模糊、昏迷 | 严禁烤火，用睡袋包裹送医 |

> **重要警示**：重度失温患者严禁直接加热或饮用热水，否则可能导致心脏骤停。

#### 迷路应对流程

一旦发现偏离路线，应立即执行STOP原则：

- **S**（Stop）：停止前进，保持冷静；
- **T**（Think）：回忆最后已知位置；
- **O**（Observe）：观察周围地形与标志物；
- **P**（Plan）：制定下一步行动计划。

随后可通过“徒步0769”小程序获取精确坐标，并拨打110或120求助，清晰描述所处环境（如“溪流东侧巨石旁”）以便救援定位。

#### 动物伤害处置

- **蛇咬伤**：不切开、不吸毒、不解毒；固定伤肢，冲洗伤口，尽快就医；
- **蜂蜇伤**：拔除毒刺，冰敷，观察过敏反应；
- **蜱虫叮咬**：镊子垂直拔出，消毒后观察发热情况。

> 注意：抗蛇毒血清是唯一特效治疗手段，注射时间越早，存活率越高。

## 五、体能与心理准备

良好的体能储备是顺利完成徒步的基础，而稳定的心理状态则决定了面对困难时的决策质量。

### （一）基础体能训练建议

- 每周进行3–4次慢跑，每次20–30分钟，提升心肺耐力；
- 利用楼梯间进行爬楼训练，模拟山地爬升负荷；
- 加强核心肌群锻炼，如平板支撑、卷腹等动作，增强身体稳定性；
- 出发前一周进行一次模拟负重行走测试，检验装备适配性与体力储备。

### （二）心理建设要点

- 认知自身极限，学会“放弃”也是一种智慧；
- 遇恶劣天气、身体不适时果断终止行程；
- 杜绝“来都来了”心态，安全永远第一位；
- 不盲目挑战“网红野路线”，尊重管理部门划定的禁区。

> 根据《山地户外运动水平等级标准》，年满16周岁的参与者可根据培训经历与运动实践申请相应等级认证，四级及以上需参加中国登山协会授权赛事不少于六次，体现了“能力与路线匹配”的科学理念。

## 六、环保责任：践行LNT无痕山林原则

徒步不仅是个人的旅程，更是一种生态行为。每一位徒步者都应自觉承担起环境保护的责任，践行“无痕山林”（Leave No Trace, LNT）原则。

### LNT七大原则

1. **提前计划与准备**
2. **在可承受地面行进与露营**
3. **妥善处理废弃物**（带走所有垃圾）
4. **保持自然原貌**（不采摘植物、不刻画岩石）
5. **最小化野外用火影响**
6. **尊重野生动植物**（不投喂、不惊扰）
7. **尊重其他使用者**

> **特别提醒**：果皮降解需1年以上，亦会对野生动物造成误食风险，必须打包带走。

在实际操作中，可采取以下具体措施：
- 使用密封袋分类存放厨余与生活垃圾；
- 如厕时挖掘15厘米深的猫洞，事后回填并标记；
- 用矿泉水瓶收集细碎垃圾，防止渗漏；
- 优先使用便携炉具而非明火烹饪。

## 结语：让每一次出发都更安心

徒步不仅是脚步的丈量，更是心智的成长。唯有建立科学认知、做好充分准备、坚守环保底线，才能真正享受山野之美。愿每位徒步者都能平安归来，也为后来者留下一片纯净天地。正如《徒步百科》所倡导：“真正的探险，不是征服自然，而是学会与之共存。”<sup>[1]</sup>

[1]:http://www.zxhsd.com/kgsm/ts/2025/11/04/6716410.shtml "徒步百科：徒步帮|责编:许姗//汪昊宇 : 生活娱乐 :生活用书 :保健养生 :浙江新华书店网群"
[2]:https://m.dzplus.dzng.com/share/general/0/NEWS2874270EFMGUZPGTKPDI "序跋丨《徒步百科》推荐序_大众新闻_大众新媒体大平台"
[3]:https://www.douban.com/doubanapp/dispatch?uri=/review/17184809 "让我从户外菜鸟秒变安全达人（徒步百科）书评"
[4]:https://mall.96192.com/product/detail/1212472 "徒步中国"
[5]:https://book.douban.com/subject/37536789/ "徒步百科 (豆瓣)"
[6]:https://page.sm.cn/blm/midpage-317/index?h=iknow.v4_2.quark.cn&id=28_21800965cc7ad878aa74d45c348d9126 "户外徒步0基础入门，这份攻略请收好"
[7]:https://sz.people.com.cn/n2/2026/0107/c202846-41465718.html "“深圳远足径”导览上线"
[8]:https://www.toutiao.com/a7592038982356173364/ "深圳远足径导览上线啦！快来看看如何开启山海之旅 - 今日头条"
[9]:https://yjt.hubei.gov.cn/yjkp/yjkp/202603/t20260331_5903087.shtml "户外登山，安全为先-湖北省应急管理厅"
[10]:https://www.douyin.com/video/7633676080179711270 "户外徒步装备分享 #徒步 #大学生 #装备分享"
[11]:http://sd.cma.gov.cn/xwzx_3497/qxkp/202601/t20260109_7535458.html "山东省气象局-- 高山有界 越己知止——高山徒步切守安全与生态双底线"
````

## File: Agent-PRD.md
````markdown
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
````

## File: Agent三层记忆架构-实现文档.md
````markdown
# Agent 三层记忆架构 — 实现文档

## 1. 项目概述

### 1.1 目标

给 AI Agent 加上跨会话记忆。对话一长就超窗口、丢信息，这是个老问题。

### 1.2 思路

把记忆按时效性分三层：当前会话直接用原文，近期的压成摘要，长期知识存下来按需检索。全量加载 100 轮对话大概 50k tokens，压缩后不到 3k。

| 层 | 名称 | 时效 | Token 量 | 怎么存 |
|---|------|------|----------|--------|
| L0 | 工作记忆 | 当前会话 | 不限 | 对话原文直接放 prompt |
| L1 | 压缩记忆 | 近期会话 | ~500t/会话 | LLM 生成的摘要，JSON 文件 |
| L2 | 长期记忆 | 跨所有会话 | ~100t/条 | 结构化知识 + 向量索引 |

### 1.3 技术来源

| 本方案 | 来自哪 | 改了什么 |
|-------|--------|---------|
| L1 语义摘要 | Claude-Mem | 只留会话结束压缩，去掉了 6 个生命周期钩子 |
| L2 结构化知识 | OpenViking | 8 类缩到 3 类 |
| 向量检索 | 两者 | 扁平检索，不做目录递归 |
| Viking URI / 路径锁 / RedoLog | OpenViking | 没用，太重了 |

---

## 2. 系统架构

### 2.1 整体结构

```
┌─────────────────────────────────────────────────┐
│                   Agent 会话                     │
│                                                  │
│  Prompt 组装                                     │
│  ┌───────────────────────────────────────────┐  │
│  │ [System] + [L0 当前对话] + [L1 近期摘要]   │  │
│  │ + [L2 检索到的知识] + [用户输入]           │  │
│  └───────────────────────────────────────────┘  │
│                                                  │
│  会话结束                                        │
│  ┌───────────────────────────────────────────┐  │
│  │ 对话历史 → 压缩摘要(L1) → 提取知识(L2)     │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 2.2 数据流

写入（会话结束时）：

```
对话历史
  │
  ├─► LLM 压缩 ──► 会话摘要 ──► sessions/
  │
  └─► LLM 提取 ──► 结构化知识 ──► knowledge/
                                  ──► 向量化 ──► index/
```

读取（新会话启动时）：

```
1. L0：当前会话最近 N 轮（自动）
2. L1：最近 1~2 个摘要文件（直接读）
3. L2：用户输入 → embedding → 向量检索 → 相关知识
4. 组装：L0 + L1 + L2 + 用户输入
```

---

## 3. 目录结构与数据格式

### 3.1 目录

```
memory/
├── sessions/                   # L1：会话压缩摘要
│   ├── 2026-05-15.json
│   └── 2026-05-16.json
├── knowledge/                  # L2：结构化长期记忆
│   ├── preferences.json        # 用户偏好
│   ├── projects.json           # 项目背景
│   └── lessons.json            # 经验教训
└── index/                      # L2：向量索引
    ├── embeddings.faiss
    └── id_map.json             # 向量 ID → 知识条目映射
```

### 3.2 L1 会话摘要

`memory/sessions/YYYY-MM-DD.json`

```json
{
  "date": "2026-05-16",
  "summary": "用户在开发一个 RAG 项目，讨论了长上下文管理方案。最终采用三层记忆架构，融合 OpenViking 的分级加载和 Claude-Mem 的语义摘要压缩。",
  "topics": ["RAG", "长上下文", "记忆架构", "OpenViking", "Claude-Mem"],
  "decisions": [
    "采用三层记忆架构（L0/L1/L2）",
    "L1 用 LLM 语义摘要压缩",
    "L2 简化为 3 类知识"
  ],
  "action_items": ["实现完整代码", "写简历 demo"],
  "token_count_original": 15000,
  "token_count_summary": 300,
  "compression_ratio": 0.02
}
```

### 3.3 L2 结构化知识

`memory/knowledge/preferences.json`

```json
[
  {
    "id": "pref_001",
    "category": "coding_style",
    "content": "用户偏好 Python，喜欢类型注解和 docstring",
    "source_session": "2026-05-15",
    "confidence": 0.9,
    "updated_at": "2026-05-15T18:30:00"
  }
]
```

`memory/knowledge/projects.json`

```json
[
  {
    "id": "proj_001",
    "name": "RAG 三层记忆",
    "description": "基于 L0/L1/L2 的 Agent 上下文记忆系统",
    "tech_stack": ["Python", "FAISS", "OpenAI API"],
    "key_decisions": [
      "三层架构而非全量存储",
      "LLM 压缩而非截断"
    ],
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  }
]
```

`memory/knowledge/lessons.json`

```json
[
  {
    "id": "lesson_001",
    "type": "success",
    "content": "LLM 压缩摘要比截断效果好，信息密度高且语义完整",
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  },
  {
    "id": "lesson_002",
    "type": "failure",
    "content": "全量加载历史对话 Token 消耗太大，100 轮约 50k tokens",
    "source_session": "2026-05-16",
    "updated_at": "2026-05-16T18:40:00"
  }
]
```

### 3.4 L2 向量索引映射

`memory/index/id_map.json`

```json
{
  "0": {"knowledge_type": "preferences", "entry_id": "pref_001"},
  "1": {"knowledge_type": "projects", "entry_id": "proj_001"},
  "2": {"knowledge_type": "lessons", "entry_id": "lesson_001"}
}
```

---

## 4. 核心模块实现

### 4.1 配置

```python
# config.py
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class MemoryConfig:
    base_dir: Path = Path("./memory")
    sessions_dir: Path = field(init=False)
    knowledge_dir: Path = field(init=False)
    index_dir: Path = field(init=False)

    # L0
    max_recent_turns: int = 10

    # L1
    max_session_summaries: int = 5
    summary_max_tokens: int = 500

    # L2
    top_k: int = 5
    similarity_threshold: float = 0.7

    # LLM
    llm_model: str = "gpt-4o-mini"
    llm_api_base: str = "https://api.openai.com/v1"
    llm_api_key: str = ""

    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    def __post_init__(self):
        self.sessions_dir = self.base_dir / "sessions"
        self.knowledge_dir = self.base_dir / "knowledge"
        self.index_dir = self.base_dir / "index"
```

### 4.2 L1 会话压缩

```python
# compressor.py
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

class SessionCompressor:
    """把对话历史压成结构化摘要"""

    SUMMARY_PROMPT = """将以下对话历史压缩为结构化摘要。

输出 JSON，字段：
1. summary: 简洁摘要（不超过 300 字）
2. topics: 主要话题关键词（3~8 个）
3. decisions: 关键决策（如有）
4. action_items: 后续待办（如有）

对话历史：
{conversation}

只输出 JSON。"""

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )

    def compress(self, messages: list[dict]) -> dict:
        conversation = self._format_messages(messages)

        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": "你是对话压缩助手，只输出 JSON。"},
                {"role": "user", "content": self.SUMMARY_PROMPT.format(
                    conversation=conversation
                )}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )

        result = json.loads(response.choices[0].message.content)

        original_tokens = sum(len(m.get("content", "")) // 4 for m in messages)
        summary_tokens = len(result.get("summary", "")) // 4

        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": result.get("summary", ""),
            "topics": result.get("topics", []),
            "decisions": result.get("decisions", []),
            "action_items": result.get("action_items", []),
            "token_count_original": original_tokens,
            "token_count_summary": summary_tokens,
            "compression_ratio": round(summary_tokens / max(original_tokens, 1), 3)
        }

    def save(self, summary: dict) -> Path:
        self.config.sessions_dir.mkdir(parents=True, exist_ok=True)
        path = self.config.sessions_dir / f"{summary['date']}.json"
        path.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                        encoding="utf-8")
        return path

    def load_recent(self, n: int = None) -> list[dict]:
        n = n or self.config.max_session_summaries
        files = sorted(self.config.sessions_dir.glob("*.json"), reverse=True)
        return [json.loads(f.read_text(encoding="utf-8")) for f in files[:n]]

    def _format_messages(self, messages: list[dict]) -> str:
        return "\n".join(
            f"[{m.get('role', 'unknown')}] {m.get('content', '')}"
            for m in messages
        )
```

### 4.3 L2 知识提取

```python
# knowledge.py
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

class KnowledgeExtractor:
    """从对话摘要中提取结构化知识"""

    EXTRACT_PROMPT = """从以下对话摘要中提取三类知识：

1. preferences（用户偏好）: 写作风格、编码习惯、工具偏好
2. projects（项目背景）: 项目名称、技术栈、架构决策
3. lessons（经验教训）: 成功经验(type=success)或失败教训(type=failure)

摘要：{summary}
话题：{topics}

输出 JSON：
{{
  "preferences": [{{"category": "...", "content": "..."}}],
  "projects": [{{"name": "...", "description": "...", "tech_stack": [...], "key_decisions": [...]}}],
  "lessons": [{{"type": "success/failure", "content": "..."}}]
}}

某类没有就返回空数组。"""

    KNOWLEDGE_TYPES = ["preferences", "projects", "lessons"]

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )

    def extract(self, session_summary: dict) -> dict:
        response = self.client.chat.completions.create(
            model=self.config.llm_model,
            messages=[
                {"role": "system", "content": "你是知识提取助手，只输出 JSON。"},
                {"role": "user", "content": self.EXTRACT_PROMPT.format(
                    summary=session_summary.get("summary", ""),
                    topics=", ".join(session_summary.get("topics", []))
                )}
            ],
            response_format={"type": "json_object"},
            temperature=0
        )
        return json.loads(response.choices[0].message.content)

    def save(self, extracted: dict, session_date: str):
        """保存知识，和已有条目合并去重"""
        self.config.knowledge_dir.mkdir(parents=True, exist_ok=True)
        now = datetime.now().isoformat(timespec="seconds")

        for ktype in self.KNOWLEDGE_TYPES:
            path = self.config.knowledge_dir / f"{ktype}.json"
            existing = []
            if path.exists():
                existing = json.loads(path.read_text(encoding="utf-8"))

            new_items = extracted.get(ktype, [])
            for i, item in enumerate(new_items):
                entry_id = f"{ktype[:4]}_{len(existing) + i + 1:03d}"
                item["id"] = entry_id
                item["source_session"] = session_date
                item["updated_at"] = now

                # 同 content 跳过
                contents = {e.get("content", "") for e in existing}
                if item.get("content", "") not in contents:
                    existing.append(item)

            path.write_text(
                json.dumps(existing, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
```

### 4.4 L2 向量索引

```python
# vector_store.py
import json
from pathlib import Path
import numpy as np
from openai import OpenAI

class VectorStore:
    """FAISS 向量存储与检索"""

    def __init__(self, config):
        self.config = config
        self.client = OpenAI(
            base_url=config.llm_api_base,
            api_key=config.llm_api_key
        )
        self.index = None
        self.id_map = {}
        self._load_index()

    def _get_embeddings(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.config.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def _load_index(self):
        index_path = self.config.index_dir / "embeddings.faiss"
        map_path = self.config.index_dir / "id_map.json"

        if index_path.exists() and map_path.exists():
            import faiss
            self.index = faiss.read_index(str(index_path))
            self.id_map = json.loads(map_path.read_text(encoding="utf-8"))
        else:
            self._init_empty_index()

    def _init_empty_index(self):
        import faiss
        self.index = faiss.IndexFlatIP(self.config.embedding_dimension)
        self.id_map = {}
        self.config.index_dir.mkdir(parents=True, exist_ok=True)

    def add_knowledge(self, knowledge_type: str, entries: list[dict]):
        if not entries:
            return

        texts = []
        for entry in entries:
            text = entry.get("content", "") or entry.get("description", "")
            if entry.get("tech_stack"):
                text += f" 技术栈: {', '.join(entry['tech_stack'])}"
            texts.append(text)

        embeddings = self._get_embeddings(texts)
        vectors = np.array(embeddings, dtype=np.float32)

        import faiss
        faiss.normalize_L2(vectors)

        start_id = self.index.ntotal
        for i, entry in enumerate(entries):
            self.id_map[str(start_id + i)] = {
                "knowledge_type": knowledge_type,
                "entry_id": entry["id"]
            }

        self.index.add(vectors)
        self._save()

    def search(self, query: str, top_k: int = None) -> list[dict]:
        top_k = top_k or self.config.top_k

        if self.index.ntotal == 0:
            return []

        query_embedding = self._get_embeddings([query])
        query_vector = np.array(query_embedding, dtype=np.float32)

        import faiss
        faiss.normalize_L2(query_vector)

        scores, indices = self.index.search(query_vector, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or score < self.config.similarity_threshold:
                continue

            map_entry = self.id_map.get(str(idx))
            if not map_entry:
                continue

            ktype = map_entry["knowledge_type"]
            entry_id = map_entry["entry_id"]
            path = self.config.knowledge_dir / f"{ktype}.json"

            if path.exists():
                entries = json.loads(path.read_text(encoding="utf-8"))
                for e in entries:
                    if e["id"] == entry_id:
                        results.append({**e, "score": float(score), "knowledge_type": ktype})
                        break

        return sorted(results, key=lambda x: x["score"], reverse=True)

    def _save(self):
        import faiss
        faiss.write_index(self.index,
                          str(self.config.index_dir / "embeddings.faiss"))
        (self.config.index_dir / "id_map.json").write_text(
            json.dumps(self.id_map, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
```

### 4.5 记忆管理器

```python
# memory_manager.py
import json
from datetime import datetime
from config import MemoryConfig
from compressor import SessionCompressor
from knowledge import KnowledgeExtractor
from vector_store import VectorStore

class MemoryManager:
    """三层记忆统一管理"""

    def __init__(self, config: MemoryConfig = None):
        self.config = config or MemoryConfig()
        self._init_dirs()

        self.compressor = SessionCompressor(self.config)
        self.extractor = KnowledgeExtractor(self.config)
        self.vector_store = VectorStore(self.config)

        self.current_messages = []  # L0 工作记忆

    def _init_dirs(self):
        for d in [self.config.sessions_dir,
                  self.config.knowledge_dir,
                  self.config.index_dir]:
            d.mkdir(parents=True, exist_ok=True)

    # L0

    def add_message(self, role: str, content: str):
        self.current_messages.append({"role": role, "content": content})

    def get_working_memory(self) -> list[dict]:
        return self.current_messages[-self.config.max_recent_turns * 2:]

    # L1

    def get_recent_summaries(self, n: int = None) -> list[dict]:
        return self.compressor.load_recent(n)

    # L2

    def search_knowledge(self, query: str, top_k: int = None) -> list[dict]:
        return self.vector_store.search(query, top_k)

    # Prompt 组装

    def build_prompt(self, user_input: str) -> str:
        parts = []

        summaries = self.get_recent_summaries()
        if summaries:
            summary_text = "\n".join(
                f"- [{s['date']}] {s['summary']}" for s in summaries
            )
            parts.append(f"## 近期会话记忆\n{summary_text}")

        knowledge = self.search_knowledge(user_input)
        if knowledge:
            knowledge_text = "\n".join(
                f"- [{k['knowledge_type']}] {k.get('content') or k.get('description', '')}"
                for k in knowledge
            )
            parts.append(f"## 相关长期记忆\n{knowledge_text}")

        return "\n\n".join(parts) if parts else ""

    # 会话结束

    def end_session(self) -> dict:
        if not self.current_messages:
            return {}

        # L1 压缩
        summary = self.compressor.compress(self.current_messages)
        self.compressor.save(summary)

        # L2 提取
        extracted = self.extractor.extract(summary)
        self.extractor.save(extracted, summary["date"])

        # L2 向量化
        for ktype in KnowledgeExtractor.KNOWLEDGE_TYPES:
            items = extracted.get(ktype, [])
            if items:
                path = self.config.knowledge_dir / f"{ktype}.json"
                all_entries = json.loads(path.read_text(encoding="utf-8"))
                new_ids = {item.get("id") for item in items if item.get("id")}
                new_entries = [e for e in all_entries if e["id"] in new_ids]
                self.vector_store.add_knowledge(ktype, new_entries)

        self.current_messages = []

        return {
            "summary_saved": summary["date"],
            "knowledge_extracted": {
                ktype: len(extracted.get(ktype, []))
                for ktype in KnowledgeExtractor.KNOWLEDGE_TYPES
            },
            "compression_ratio": summary.get("compression_ratio", 0)
        }
```

---

## 5. 使用示例

### 5.1 基本使用

```python
from memory_manager import MemoryManager
from config import MemoryConfig

config = MemoryConfig(
    base_dir=Path("./memory"),
    llm_api_key="sk-xxx",
    llm_model="gpt-4o-mini",
    embedding_model="text-embedding-3-small"
)
memory = MemoryManager(config)

# 会话中：记录消息
memory.add_message("user", "我想做一个 RAG 项目")
memory.add_message("assistant", "好的，你希望 RAG 用在什么场景？")
memory.add_message("user", "用于企业知识库问答")
memory.add_message("assistant", "推荐用 FAISS + GPT-4o-mini 的方案...")

# 新会话：加载记忆
user_input = "上次我们讨论的 RAG 项目，进度怎么样了？"
context = memory.build_prompt(user_input)
# 输出：
# ## 近期会话记忆
# - [2026-05-16] 用户在开发一个 RAG 项目...
# ## 相关长期记忆
# - [projects] 基于 FAISS + GPT-4o-mini 的企业知识库问答系统

full_prompt = f"{context}\n\n用户: {user_input}"

# 会话结束：保存
result = memory.end_session()
# {"summary_saved": "2026-05-16",
#  "knowledge_extracted": {"preferences": 1, "projects": 1, "lessons": 0},
#  "compression_ratio": 0.02}
```

### 5.2 完整对话循环

```python
from openai import OpenAI

client = OpenAI(api_key=config.llm_api_key)

def chat(user_input: str) -> str:
    memory.add_message("user", user_input)

    memory_context = memory.build_prompt(user_input)

    messages = [
        {"role": "system", "content": f"你是一个有记忆的 AI 助手。\n\n{memory_context}"},
        *memory.get_working_memory()
    ]

    response = client.chat.completions.create(
        model=config.llm_model,
        messages=messages
    )
    reply = response.choices[0].message.content

    memory.add_message("assistant", reply)
    return reply

# 使用
print(chat("你好，我是小明"))
print(chat("帮我写一个 Python 爬虫"))
print(chat("记住我喜欢用 type hints"))

# 结束时保存
memory.end_session()
```

---

## 6. 依赖与安装

```txt
# requirements.txt
openai>=1.0.0
faiss-cpu>=1.7.0
numpy>=1.24.0
```

```bash
pip install -r requirements.txt
```

环境变量：

```bash
export OPENAI_API_KEY="sk-xxx"
export OPENAI_API_BASE="https://api.openai.com/v1"
```

---

## 7. Token 消耗对比

| 场景 | 全量加载 | 三层记忆 | 节省 |
|------|---------|---------|------|
| 5 轮对话 | ~5,000t | ~5,000t（L0 全量） | 0% |
| 20 轮对话 | ~20,000t | ~2,000t（L0+L1） | 90% |
| 100 轮对话 | ~50,000t | ~3,000t（L0+L1+L2） | 94% |
| 跨 10 个会话 | ~200,000t | ~4,000t（L1+L2） | 98% |

计算方式：

```
全量 = 所有历史消息 tokens 之和

三层 = L0(最近N轮原文) + L1(最近M个摘要×500) + L2(检索K条×100)
```

5 轮以内 L0 全量就够了，没省头。对话越长，分层优势越明显。

---

## 8. 后续可以做的

- 知识去重：LLM 判断新旧知识是否重复
- 知识衰减：长期没用的知识降权
- 多用户：按 user_id 分目录
- 记忆可视化：Web UI 浏览三层内容
- Rerank：检索结果精排
- 知识迭代：后续会话修正已有条目

---

## 9. 面试怎么说

> 我做了个三层记忆架构：L0 存当前对话原文，L1 用 LLM 把历史对话压成摘要，L2 从摘要里提取结构化知识做向量索引。新会话启动时加载 L1 摘要，再根据用户输入从 L2 语义检索相关知识。比全量加载省 90% 以上 Token。
>
> 为什么分三层？L0 保精度，L1 保连续性，L2 保长期积累。层级越深信息越密，消耗越低。
>
> 压缩用 LLM 而不是截断，因为截断丢语义边界，LLM 压缩能保留话题、决策、待办这些结构化信息。
````

## File: AI-Hiking-Agent改造计划书.md
````markdown
# AI Hiking Agent 改造计划书

> 目标：把当前通用 Agent 改成真正能服务户外徒步场景的助手。它要能查天气、查地理位置和路线资料，结合 RAG 知识库给出建议，并在需要时整理成 Markdown 或 PDF。

## 1. 当前结论

这次讨论后，方向已经比较清楚：项目不需要继续往"通用 Agent 框架展示"上堆能力。AI Hiking 的核心卖点应该是户外徒步决策，而不是让模型随意调用一堆工具。

当前 Agent 链路是：

```text
用户 Prompt
➡️ 前端 SuperAgent
➡️ Go Gateway
➡️ Python /chat/sse
➡️ 读取 FileChatMemory
➡️ MemoryManager 执行摘要和长期记忆检索
➡️ 拼接 SYSTEM_PROMPT + NEXT_STEP_PROMPT + 记忆
➡️ LangGraph ReAct 循环
➡️ 从固定 7 个工具里选择调用
➡️ 工具结果回填给模型
➡️ 输出最终回答
➡️ SSE 返回前端
➡️ 最终回复写回聊天记忆
```

它能跑，但还不像户外助手。主要问题有三个：

1. 工具是固定全量暴露的，模型每轮都能看到 `web_search`、`web_scraping`、`file_operation`、`resource_download`、`terminal`、`generate_pdf`、`terminate`。
2. RAG 和 Agent 在产品上像两个入口，在能力上还没有打通。Agent 没有把 RAG 当作徒步知识来源稳定使用。
3. 记忆系统有 L0/L1/L2 的设计，但运行时更像"执行前自动压缩和提取"，写入时机偏早，分类也不够贴近徒步任务。

我的判断是：保留当前底座，但不要继续把重点放在 LangGraph 或多工具堆叠上。下一步要做的是一条清楚的户外任务编排链路。

## 2. 产品定位

Agent 的核心目标：

```text
理解用户徒步需求
➡️ 提取地点、日期、天数、经验、装备、偏好
➡️ 调用天气、地理位置、路线资料、RAG 知识库等工具
➡️ 做风险、装备、行程判断
➡️ 输出清晰建议
➡️ 需要时生成 Markdown 或 PDF
```

典型用户请求：

- "这周末想去武功山，帮我看看适不适合徒步。"
- "北京周边两天一夜，新手，帮我规划一条安全路线。"
- "我想轻装去山里走 15 公里，需要带什么？"
- "把路线、天气、装备清单、风险提醒整理成一份 PDF。"

非目标：

- 不做通用电脑操作 Agent。
- 不开放任意终端执行能力给普通用户场景。
- 不把 RAG 做成另一个孤立产品。
- 不急着做重型 LangGraph checkpoint、interrupt、多 Agent 编排，除非文件导出和审批流程真的需要。

## 3. 架构取舍

### 3.1 Agent 和 RAG 不彻底分开

RAG 应该是 Agent 的知识工具，而不是独立于 Agent 的另一个系统。

推荐关系：

```text
RAG = 证据和知识来源
Agent = 任务编排和判断层
```

纯知识问答可以直接走 RAG，例如"三层穿衣法是什么"。复杂徒步任务进入 Agent，由 Agent 调用 RAG、天气、地理位置、路线资料，再整理建议。

### 3.2 LangGraph 暂时弱化

当前项目没有真正使用 LangGraph 最有价值的能力：

- 用户手动确认后恢复执行
- checkpoint 断点续跑
- 多节点状态流转
- 多 Agent 编排
- 复杂数据操作回滚

所以短期不要为了框架感继续加复杂度。更合适的路线是：

```text
短期：使用确定性 workflow 承接核心徒步场景
中期：保留 LangGraph 作为可选执行壳
后期：如果文件导出、审批、长任务恢复变多，再强化 LangGraph
```

### 3.3 Query 改写要做，但不要泛化

这里不需要每轮都做"润色式 query rewrite"。真正需要的是：

```text
意图识别
➡️ 槽位提取
➡️ 检索 query 构造
```

例子：

```text
用户：这周末想去武功山，帮我看看适不适合徒步
```

系统内部应抽取为：

```json
{
  "intent": "risk_assessment",
  "destination": "武功山",
  "date": "本周末",
  "activity": "徒步",
  "missing": ["出发城市", "经验水平", "是否露营"]
}
```

只有在调用搜索、RAG、路线资料时才构造检索 query，例如：

```text
武功山 本周末 天气 徒步 风险
武功山 徒步 路线 海拔 下撤点 近期路况
武功山 两天一夜 装备 安全
```

## 4. 目标执行链路

建议把 Agent 改成下面这条链路：

```text
用户 Prompt
➡️ Request Intake
   识别意图、提取槽位、检查是否缺少关键条件
➡️ Memory Read
   读取用户画像、当前行程状态、最近对话
➡️ Tool Plan
   根据场景选择 3 到 5 个工具
➡️ Tool Execution
   天气、地理位置、路线资料、RAG、网页资料
➡️ Outdoor Reasoning
   风险评估、装备建议、行程整理
➡️ Final Response
   返回干净的中文建议
➡️ Export
   用户需要时生成 Markdown 或 PDF
➡️ Memory Commit
   执行结束后再写入稳定偏好和当前行程状态
```

这条链路的重点是"先结构化，再调用工具，再做户外判断"。模型可以参与总结和推理，但不要让它决定所有流程。

## 5. 工具系统改造

### 5.1 工具不要只看数量

目前已有 7 个通用工具。后续如果加入天气、地理位置、路线资料、RAG、装备、风险、导出，总数会到 12 到 14 个。这个数量本身不危险，危险的是每一轮都把所有工具交给模型。

推荐做两层工具：

| 层级 | 用途 | 是否直接暴露给模型 |
| --- | --- | --- |
| 领域工具 | 天气、地理位置、路线、装备、风险、RAG、导出 | 是，按场景动态暴露 |
| 基础工具 | 搜索、网页读取、文件写入、PDF、下载、终端 | 默认不暴露，由领域工具内部调用 |

每轮实际暴露工具控制在 3 到 5 个。

### 5.2 v1 工具清单

建议第一版只做这些领域工具：

| 工具 | 作用 | 说明 |
| --- | --- | --- |
| `weather_lookup` | 查询目的地天气 | 返回温度、降水、风力、预警、来源和时间 |
| `geo_lookup` | 查询地理位置 | 返回经纬度、海拔、行政区、周边地形信息 |
| `route_research` | 收集路线资料 | 基于搜索、网页读取、RAG 汇总里程、爬升、耗时、下撤点 |
| `hiking_knowledge_search` | 查询户外知识库 | 封装现有 RAG，不让 Agent 凭空讲安全知识 |
| `gear_checklist` | 生成装备清单 | 根据天数、季节、路线强度、是否露营给清单 |
| `risk_assessment` | 徒步风险评估 | 汇总天气、海拔、里程、用户经验，输出风险等级 |
| `trip_report_export` | 导出文档 | 生成 Markdown，必要时再调用 PDF 工具 |

已有通用工具的处理方式：

- `web_search` 和 `web_scraping` 作为 `route_research` 内部能力。
- `generate_pdf` 作为 `trip_report_export` 内部能力。
- `file_operation` 只用于保存 Markdown 或中间 artifact，写入前需要确认。
- `resource_download` 暂不放进核心徒步链路，后续下载 GPX、图片、地图资料时再启用。
- `terminal` 从普通徒步场景中移除，只留给开发诊断或受控运维。
- `terminate` 可以继续保留，但不需要用户感知。

## 6. 记忆系统改造

当前 `MemoryManager.process_interaction(history, query)` 会在 Agent 执行前做知识更新，再把摘要和长期记忆塞进系统 Prompt。这个顺序不理想。

新的记忆编排应该是：

```text
执行前只读
➡️ 执行中更新当前任务状态
➡️ 执行后再判断哪些内容值得保存
```

### 6.1 记忆分类

建议分成四类：

| 类型 | 记录内容 | 示例 |
| --- | --- | --- |
| `ProfileMemory` | 稳定用户画像 | 常驻城市、徒步经验、膝盖问题、风险偏好 |
| `TripMemory` | 当前行程状态 | 目的地、日期、天数、人数、是否露营、已确认路线 |
| `ChatMemory` | 普通对话历史 | 最近 20 条对话，用于短期上下文 |
| `KnowledgeMemory` | 户外知识库 | 装备原则、安全知识、路线文档，这部分交给 RAG |

用户记忆和 RAG 知识库不要混在一起。"我膝盖不好"是用户记忆；"暴雨橙色预警应取消行程"是知识库内容。

### 6.2 写入规则

值得写入长期记忆：

- "我一般从上海出发。"
- "我没有露营经验。"
- "我膝盖不太好，尽量别安排大爬升。"
- "这次计划是周六去武功山，两天一夜。"

不值得写入长期记忆：

- "谢谢"
- "继续"
- 某次天气搜索结果
- 某次网页摘要
- 工具中间输出

建议新增一个 `MemoryCommitter`，只在最终回答生成后运行。它输出候选记忆，再按置信度和类型写入。

```text
最终回答 + 本轮结构化状态
➡️ Memory Candidate Extractor
➡️ Profile / Trip / Artifact 分类
➡️ 去重和置信度判断
➡️ 写入记忆
```

## 7. 任务拆分

### 任务 1：请求理解层

目标：把用户自然语言转成稳定的任务结构。

交付：

- 新增 `AgentIntent`：`knowledge_qa`、`route_plan`、`gear_check`、`risk_assessment`、`report_export`、`general_chat`。
- 新增槽位结构：目的地、日期、天数、出发地、经验水平、是否露营、团队人数、装备水平。
- 缺少关键槽位时先追问，不要强行调用工具。

验收：

- "这周末武功山适合去吗" 能识别为风险评估。
- "帮我做两天一夜攻略" 能识别为路线规划，并追问目的地。
- "三层穿衣法是什么" 能识别为知识问答。

### 任务 2：工具注册表升级

目标：让工具按场景和风险动态选择。

交付：

- 给工具元数据增加 `domain`、`scenarios`、`auto_allowed`、`requires_confirmation`、`result_policy`。
- 修正前后端字段不一致问题：统一使用 `needs_confirmation`。
- 普通徒步场景不暴露 `terminal`、`file_operation`、`resource_download`。

验收：

- 装备清单场景只激活 RAG、装备、风险或终止类工具。
- 导出场景才允许文件和 PDF 能力进入流程。
- 高风险工具调用可以生成确认事件。

### 任务 3：徒步资料工具

目标：让 Agent 能获取天气、地理位置和路线资料。

交付：

- `weather_lookup`：支持地点和日期，返回来源、时间、天气、温度、降水、风力、预警。
- `geo_lookup`：返回地点候选、坐标、海拔、行政区和基础地形描述。
- `route_research`：综合搜索、网页读取和 RAG，输出路线事实表。

验收：

- 用户问某地是否适合徒步时，必须有天气和路线资料参与判断。
- 工具结果必须带来源和查询时间。
- 没查到可靠资料时，回答要说明缺口，不能装作确认过。

### 任务 4：RAG 作为 Agent 工具

目标：让 Agent 使用已有知识库，不让户外安全知识靠模型硬编。

交付：

- 新增 `hiking_knowledge_search`，内部调用现有 RAG 检索。
- 返回结构包含 chunks、score、source、title、preview。
- Agent 最终回答中的安全建议要能追溯到 RAG 或实时工具。

验收：

- "失温怎么处理" 优先走 RAG。
- "新手徒步带什么" 能结合 RAG 和装备规则。
- RAG 没证据时，Agent 应说明资料不足。

### 任务 5：装备和风险判断

目标：把户外经验沉淀成稳定规则，减少模型自由发挥。

交付：

- `gear_checklist`：按单日、两天一夜、多日重装输出装备清单。
- `risk_assessment`：输出风险等级、主要风险、取消条件、替代方案。
- 明确硬规则，例如暴雨橙色及以上预警直接建议取消或改期。

验收：

- 新手、高海拔、暴雨、峡谷、夜行等场景能给出保守建议。
- 风险输出不要只说"注意安全"，要明确风险来源和处理动作。

### 任务 6：Markdown 和 PDF 输出

目标：把多方资料整理成可交付文档。

交付：

- 先生成结构化 Markdown，再按需转 PDF。
- 文档结构固定为：概览、路线资料、天气判断、装备清单、风险提醒、行程安排、资料来源。
- 写文件和生成 PDF 前要展示路径、摘要和影响范围。

验收：

- 用户说"整理成 PDF"时，先生成 Markdown 内容，再生成 PDF。
- 覆盖已有文件必须确认。
- 最终回答里给出 artifact 文件名和简短说明。

### 任务 7：记忆编排重构

目标：把记忆从黑盒注入改成任务上下文管理。

交付：

- 执行前只读 `ProfileMemory`、`TripMemory`、`ChatMemory`。
- 执行后通过 `MemoryCommitter` 写入稳定信息。
- `KnowledgeMemory` 交给 RAG，不和用户画像混用。

验收：

- 用户说"我膝盖不好"后，后续路线建议会自动避开大爬升。
- 某次天气结果不会写入长期偏好。
- 当前行程状态能被后续"继续完善这份攻略"复用。

### 任务 8：前端交互调整

目标：让用户看到的是徒步建议，不是工具日志。

交付：

- 快捷入口传 `scenario`，不只是填入一句文本。
- 最终回答保持干净。
- 工具调用、证据、来源、审批放到折叠面板。
- 导出文档时展示 artifact 区域。

验收：

- "生成行程"、"检查装备"、"风险提醒" 能触发不同后端场景。
- `thought/tool_call/tool_result` 不再直接混入主聊天正文。
- 用户能展开查看资料来源。

### 任务 9：测试和评估

目标：用固定用例判断改造是否真的变好。

交付：

- 后端测试：意图识别、槽位提取、工具选择、RAG 工具、风险规则、导出审批。
- 前端测试：场景入口、折叠执行过程、artifact 展示。
- 回归样例集：
  - 武功山周末风险评估
  - 北京周边两天一夜路线规划
  - 新手单日装备清单
  - 暴雨后峡谷徒步判断
  - 三层穿衣法知识问答
  - 生成 Markdown/PDF 攻略

验收：

- 每个样例都有稳定输出。
- 每个工具结果有来源或明确失败原因。
- 没有把终端工具暴露给普通用户请求。

## 8. 推荐实施顺序

### Phase 1：先把核心链路跑顺

优先级最高。先做请求理解、场景选择、工具过滤和 RAG 工具化。

完成后链路应变成：

```text
Prompt
➡️ Intent + Slots
➡️ Memory Read
➡️ 激活少量工具
➡️ RAG / 搜索 / 天气 / 地理位置
➡️ 风险和装备建议
➡️ 干净回答
```

### Phase 2：接入天气和地理位置

天气和地理位置是这个产品的关键工具。没有它们，Agent 只是普通户外问答。

第一版可以用公开接口或搜索兜底，但返回必须带来源和时间。后续再换更稳定的天气、地图 API。

### Phase 3：做文档输出

当路线、天气、装备和风险都能结构化后，再做 Markdown/PDF。不要先做漂亮 PDF。内容结构稳定比版式重要。

### Phase 4：重构记忆编排

把当前的执行前自动提取，改成执行后提交。先做 Profile 和 Trip 两类记忆，别急着把所有 L1/L2 设计一次性补满。

### Phase 5：再评估 LangGraph

如果后面需要审批恢复、长任务续跑、多步骤导出，可以继续强化 LangGraph。否则保留 workflow 会更轻。

## 9. 成功标准

改造后，用户输入：

```text
这周末想去武功山，两天一夜，新手，帮我看看适不适合去，顺便整理一份攻略。
```

系统应该做到：

1. 识别目的地、时间、天数、经验水平。
2. 查天气和地理位置。
3. 收集路线资料，包括里程、爬升、耗时和下撤点。
4. 查询户外知识库，补装备和安全原则。
5. 给出是否适合出行的判断。
6. 如果风险高，明确建议取消、改期或降低强度。
7. 输出装备清单和行程安排。
8. 用户确认后生成 Markdown 或 PDF。
9. 记录"新手"、"两天一夜偏好"等稳定信息，但不把天气结果写成长期记忆。

一句话判断是否成功：用户拿到的不是聊天答案，而是一份能辅助真实出行决策的资料包。
````

## File: ai-service/__init__.py
````python

````

## File: ai-service/.omc/project-memory.json
````json
{
  "version": "1.0.0",
  "lastScanned": 1779022272930,
  "projectRoot": "C:\\Users\\14253\\Desktop\\ai-hiking\\ai-service",
  "techStack": {
    "languages": [
      {
        "name": "Python",
        "version": null,
        "confidence": "high",
        "markers": [
          "requirements.txt"
        ]
      }
    ],
    "frameworks": [],
    "packageManager": "pip",
    "runtime": null
  },
  "build": {
    "buildCommand": null,
    "testCommand": "cd \"C:/Users/14253/Desktop/ai-hiking/ai-service\" && .conda312/Scripts/pytest.exe tests/test_feishu.py tests/test_rag_direct_answer.py -v --tb=short 2>&1",
    "lintCommand": null,
    "devCommand": null,
    "scripts": {}
  },
  "conventions": {
    "namingStyle": null,
    "importStyle": null,
    "testPattern": null,
    "fileOrganization": null
  },
  "structure": {
    "isMonorepo": false,
    "workspaces": [],
    "mainDirectories": [
      "tests"
    ],
    "gitBranches": null
  },
  "customNotes": [],
  "directoryMap": {
    "agent": {
      "path": "agent",
      "purpose": null,
      "fileCount": 4,
      "lastAccessed": 1779022272845,
      "keyFiles": [
        "advisors.py",
        "agent.py",
        "prompts.py",
        "__init__.py"
      ]
    },
    "api": {
      "path": "api",
      "purpose": "API routes",
      "fileCount": 5,
      "lastAccessed": 1779022272846,
      "keyFiles": [
        "chat.py",
        "models.py",
        "models_router.py",
        "rag.py",
        "__init__.py"
      ]
    },
    "mcp": {
      "path": "mcp",
      "purpose": null,
      "fileCount": 2,
      "lastAccessed": 1779022272847,
      "keyFiles": [
        "client.py",
        "__init__.py"
      ]
    },
    "memory": {
      "path": "memory",
      "purpose": null,
      "fileCount": 8,
      "lastAccessed": 1779022272848,
      "keyFiles": [
        "base.py",
        "compressor.py",
        "file_memory.py",
        "knowledge.py",
        "memory_manager.py"
      ]
    },
    "memory_data": {
      "path": "memory_data",
      "purpose": null,
      "fileCount": 5,
      "lastAccessed": 1779022272848,
      "keyFiles": [
        "chat-1778939095217.json",
        "chat-f5ff9a77-3929-4353-8e80-742e1c6946af.json",
        "test-1.json",
        "test-2.json",
        "verify-chat.json"
      ]
    },
    "rag": {
      "path": "rag",
      "purpose": null,
      "fileCount": 7,
      "lastAccessed": 1779022272849,
      "keyFiles": [
        "augmenter.py",
        "feishu.py",
        "loader.py",
        "reranker.py",
        "retriever.py"
      ]
    },
    "rag_docs": {
      "path": "rag_docs",
      "purpose": null,
      "fileCount": 0,
      "lastAccessed": 1779022272850,
      "keyFiles": []
    },
    "tests": {
      "path": "tests",
      "purpose": "Test files",
      "fileCount": 8,
      "lastAccessed": 1779022272850,
      "keyFiles": [
        "test_embedding_config.py",
        "test_feishu.py",
        "test_memory.py",
        "test_rag_direct_answer.py",
        "test_rag_rerank.py"
      ]
    },
    "tools": {
      "path": "tools",
      "purpose": null,
      "fileCount": 8,
      "lastAccessed": 1779022272851,
      "keyFiles": [
        "file_operation.py",
        "pdf_generation.py",
        "resource_download.py",
        "terminal.py",
        "terminate.py"
      ]
    },
    "workspace": {
      "path": "workspace",
      "purpose": null,
      "fileCount": 1,
      "lastAccessed": 1779022272852,
      "keyFiles": [
        "Python知识点总复习.pdf"
      ]
    },
    "__pycache__": {
      "path": "__pycache__",
      "purpose": null,
      "fileCount": 6,
      "lastAccessed": 1779022272853,
      "keyFiles": [
        "config.cpython-312.pyc",
        "config.cpython-313.pyc",
        "main.cpython-312.pyc",
        "main.cpython-313.pyc",
        "__init__.cpython-312.pyc"
      ]
    }
  },
  "hotPaths": [
    {
      "path": "rag\\feishu.py",
      "accessCount": 7,
      "lastAccessed": 1779022815548,
      "type": "file"
    },
    {
      "path": "",
      "accessCount": 5,
      "lastAccessed": 1779022430787,
      "type": "directory"
    },
    {
      "path": "api\\rag.py",
      "accessCount": 4,
      "lastAccessed": 1779022815638,
      "type": "file"
    },
    {
      "path": "tests\\test_feishu.py",
      "accessCount": 1,
      "lastAccessed": 1779022284431,
      "type": "file"
    },
    {
      "path": "requirements.txt",
      "accessCount": 1,
      "lastAccessed": 1779022456236,
      "type": "directory"
    },
    {
      "path": "config.py",
      "accessCount": 1,
      "lastAccessed": 1779022456794,
      "type": "file"
    }
  ],
  "userDirectives": []
}
````

## File: ai-service/.omc/state/agent-replay-b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27.jsonl
````
{"t":0,"agent":"system","event":"keyword_detected","keyword":"tdd"}
{"t":0,"agent":"system","event":"keyword_detected","keyword":"tdd"}
````

## File: ai-service/.omc/state/hud-stdin-cache.json
````json
{"session_id":"dacf2d60-50e5-4603-9c6e-db62701af3ee","transcript_path":"C:\\Users\\14253\\.claude\\projects\\C--Users-14253-Desktop-ai-hiking\\dacf2d60-50e5-4603-9c6e-db62701af3ee.jsonl","cwd":"C:\\Users\\14253\\Desktop\\ai-hiking\\ai-service","effort":{"level":"max"},"session_name":"Fix linked Feishu knowledge base sync","model":{"id":"deepseek-v4-pro[1m]","display_name":"deepseek-v4-pro[1m]"},"workspace":{"current_dir":"C:\\Users\\14253\\Desktop\\ai-hiking\\ai-service","project_dir":"C:\\Users\\14253\\Desktop\\ai-hiking","added_dirs":[]},"version":"2.1.143","output_style":{"name":"default"},"cost":{"total_cost_usd":4.656562,"total_duration_ms":2159617,"total_api_duration_ms":1091374,"total_lines_added":129,"total_lines_removed":6},"context_window":{"total_input_tokens":140985,"total_output_tokens":626,"context_window_size":1000000,"current_usage":{"input_tokens":185,"output_tokens":626,"cache_creation_input_tokens":0,"cache_read_input_tokens":140800},"used_percentage":14,"remaining_percentage":86},"exceeds_200k_tokens":false,"fast_mode":false,"thinking":{"enabled":true}}
````

## File: ai-service/.omc/state/last-tool-error.json
````json
{
  "tool_name": "Bash",
  "tool_input_preview": "{\"command\":\"cd \\\"C:/Users/14253/Desktop/ai-hiking/ai-service\\\" && python -c \\\"import ast, sys; [print(f'{node.name}:{node.lineno}') for node in ast.walk(ast.parse(open('rag/feishu.py').read())) if isi...",
  "error": "Exit code 1\nTraceback (most recent call last):\r\n  File \"<string>\", line 1, in <module>\r\n    import ast, sys; [print(f'{node.name}:{node.lineno}') for node in ast.walk(ast.parse(open('rag/feishu.py').read())) if isinstance(node, ast.FunctionDef)]\r\n                                                                                         ~~~~~~~~~~~~~~~~~~~~~~~~~~^^\r\nUnicodeDecodeError: 'gbk' codec can't decode byte 0x8e in position 35: illegal multibyte sequence",
  "timestamp": "2026-05-17T12:52:53.721Z",
  "retry_count": 2
}
````

## File: ai-service/.omc/state/sessions/a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a/hud-state.json
````json
{
  "timestamp": "2026-05-17T12:51:18.736Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-17T12:51:11.628Z",
  "sessionId": "a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a"
}
````

## File: ai-service/.omc/state/sessions/a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a/session-started.json
````json
{
  "session_id": "a3cfd4f9-8b7e-4c35-a1b0-eab2e67d011a",
  "started_at": "2026-05-17T12:51:12.806Z",
  "cwd": "C:\\Users\\14253\\Desktop\\ai-hiking\\ai-service",
  "pid": 3996
}
````

## File: ai-service/.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
````json
{
  "timestamp": "2026-05-16T09:22:07.406Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-16T08:49:32.702Z",
  "sessionId": "b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27"
}
````

## File: ai-service/.omc/state/sessions/dacf2d60-50e5-4603-9c6e-db62701af3ee/hud-state.json
````json
{
  "timestamp": "2026-05-17T12:40:40.530Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-17T12:26:08.205Z",
  "sessionId": "dacf2d60-50e5-4603-9c6e-db62701af3ee"
}
````

## File: ai-service/户外徒步知识文档.md
````markdown
# 户外徒步知识全指南

户外徒步作为一种融合了自然探索、体能锻炼与心灵放松的活动，近年来受到越来越多人的喜爱。它不仅是对个人意志与体能的考验，更是一次与自然深度对话的机会。然而，徒步并非简单的“走路”，其背后涉及系统的知识体系与严谨的安全准备。本文旨在为徒步爱好者提供一份全面、科学且实用的知识指南，内容涵盖徒步的基础认知、装备配置、路线规划、安全防范、体能训练及环保责任，帮助参与者建立理性、安全、可持续的户外理念。

## 一、什么是徒步？——从散步到系统的户外运动

徒步（Hiking）是指在自然环境中进行的中长距离步行活动，通常单程距离不少于5公里，区别于城市中的日常散步或短途健走。其核心目的在于通过持续性的行进过程，亲近自然、挑战自我、提升身心素质，并在过程中培养对环境的敬畏与责任感<sup>[1]</sup>。

### 徒步的核心目的
徒步的价值不仅体现在身体层面的锻炼，如增强心肺功能、提高耐力与协调性，更在于心理层面的成长。研究表明，规律参与百日徒步计划的人群，其焦虑指数平均下降42%，决策失误率减少29%，印证了徒步对现代人精神压力的有效缓解作用<sup>[1]</sup>。

### 主要类型分类
根据强度、形式和场景的不同，徒步可划分为多种类型：

- **按强度分级**：
  - 休闲级：适合初学者，里程≤10km，累计爬升≤500m；
  - 进阶级：具备一定基础者，需应对复杂地形；
  - 挑战级：高海拔、长距离、大爬升线路；
  - 大师级：仅限资深爱好者，常涉及极端气候与无人区穿越。

- **按组织形式**：
  - 轻装日穿：当日往返，不携带露营装备；
  - 重装露营：多日行程，背负帐篷、睡袋等物资；
  - 商业组织：由专业机构带队，提供交通、食宿服务；
  - 自主SOLO：独立完成路线规划与执行，要求极高的综合能力。

- **特殊场景徒步**：
  - 沙漠穿越：面临高温、缺水、风沙等挑战；
  - 雪地徒步：需掌握防滑、保暖与雪崩识别技能；
  - 峡谷探秘：注意落石、湿滑岩壁与突发山洪风险。

![三层穿衣法结构示意图](https://agent.qianwen.com/mos/f8b7fdecce384cfc97cc3228a78bb361/1df099caefe281976dfaa5715179d1af)

## 二、徒步装备系统详解

科学合理的装备配置是保障徒步安全与舒适的关键。一套完整的徒步装备应遵循功能性、轻量化与冗余备份三大原则，确保在各种环境下均能有效应对。

### （一）三层穿衣法：应对多变气候的核心原则

人体在运动过程中会产生大量汗液，若衣物无法及时排湿，将导致体温调节失衡，增加失温风险。因此，“三层穿衣法”成为国际通行的户外着装标准，其结构如下表所示：

| 层级 | 功能 | 推荐材质 | 使用场景 |
|------|------|----------|--------|
| 内层（排汗层） | 吸湿速干 | 美利奴羊毛、聚酯纤维 | 所有季节 |
| 中层（保暖层） | 温度调节 | 抓绒衣、羽绒服、合成棉服 | 春秋冬季、高海拔 |
| 外层（防护层） | 防风防水 | 冲锋衣裤、软壳衣 | 雨天、强风、低温 |

> **提示**：严禁穿着纯棉衣物进入山区，因其吸水后难以干燥，极易引发失温事故。

### （二）徒步鞋的选择与磨合

徒步鞋是徒步活动中最重要的装备之一，直接影响行走稳定性与足部健康。

- **关键指标**：
  - **防水性**：推荐选用GORE-TEX或FLT防水内衬技术产品，保持脚部干爽；
  - **抓地力**：Vibram大底具有优异的耐磨性与湿滑路面附着力；
  - **支撑性**：中高帮设计可有效保护脚踝，防止扭伤，尤其适用于崎岖地形。

- **尺码建议**：由于长时间行走会导致脚部轻微肿胀，建议选择比日常鞋码大0.5–1码的型号。

- **新鞋磨合**：禁止穿着全新徒步鞋进行长途徒步。出发前应在城市道路或低强度山径上累计行走不少于30公里，以适应鞋型并排除潜在磨脚点。

- **常见品牌推荐**：LOWA、Salomon、SCARPA、凯乐石（KAILAS）、探路者（TOREAD）等均为市场认可度较高的专业品牌。

### （三）背包配置与背负系统

背包不仅是装载工具，更是影响体力分配与背部健康的决定性因素。

- **容量匹配原则**：
  - 单日徒步：20–30L，满足基本补给与应急物品存放；
  - 两日露营：30–50L，容纳睡袋、帐篷等露营装备；
  - 多日重装：50L以上，适合远距离穿越任务。

- **背负系统要点**：
  - 腰带承担约70%的重量，必须紧贴髋骨上方；
  - 肩带调节至锁骨下方，避免压迫肩颈神经；
  - 试背时检查“45度法则”：双手前伸呈90度，双臂自然下垂后应能轻松触及背包两侧提手。

- **推荐品牌**：Osprey、Gregory、始祖鸟（Arc'teryx）、Deuter等品牌以其优秀的背负系统与耐用性著称。

### （四）其他必备装备清单

除服装与背包外，以下装备亦属徒步出行的基本配置：

- **登山杖**：减轻膝盖压力可达30%，长度建议为身高×0.66；
- **头灯+备用电池**：用于夜间行进或突发状况照明，确保续航时间超过预计行程；
- **导航工具**：手机APP（如“两步路”“奥维地图”）配合纸质地图与指南针使用，形成双重保障；
- **急救包**：包含碘伏、创可贴、绷带、止血带、抗过敏药及个人常用药品；
- **应急物品**：保温毯、救生哨、多功能刀具、垃圾袋、备用口罩与驱蚊液。

此外，建议携带不少于2升饮用水，并根据气温与行程适当增加；食物方面宜选择高能量、易消化的食品，如能量棒、坚果、八宝粥与盐丸。

## 三、路线规划与难度评估

一条科学合理的徒步路线不仅能带来良好的体验，更能最大限度规避潜在风险。路线规划需结合个人能力、天气条件与地理特征进行综合判断。

### （一）如何科学评估一条徒步路线？

中国登山协会推荐采用以下参数作为路线难度评估依据：

- 总里程
- 累计爬升
- 最高海拔
- 预估耗时

其中，预估耗时可通过以下公式计算：

> 总时间 = (距离 ÷ 3.2) + (爬升 ÷ 305) + 每小时休息5分钟

该公式综合考虑平地行进速度（约3.2km/h）与垂直爬升消耗（每305米加1小时），已被广泛应用于国内徒步圈的实际操作中。

### （二）路线筛选原则

对于初次接触徒步的新手，建议遵循“三六六原则”：

- 至少准备 **3升水**；
- 初次徒步不宜超过 **6公里** 或 **600米海拔差**；
- 行程控制在 **6小时内**。

同时，应优先选择成熟步道，避免进入未开发区域。可通过“两步路”“六只脚”等APP下载离线轨迹，并查看近期他人实际轨迹以确认路况是否通行。此外，务必选择设有下撤点的线路，避免陷入“只能进不能退”的困境。

### （三）热门推荐路线（按难度分级）

| 地点 | 路线名称 | 里程 | 爬升 | 难度 | 特色 |
|------|----------|------|------|------|------|
| 成都邛崃 | 休闲级步道 | 5–8km | <200m | 休闲级 | 全龄友好，路面平坦 |
| 西安 | 蓝关古道环穿 | 12km | ~800m | 初级 | 春季赏景佳选 |
| 云南丽江 | 虎跳峡高路 | 2–3天 | —— | 初级 | 金沙江峡谷壮丽景观 |
| 四川四姑娘山 | 长穿毕 | 3–4天 | —— | 中等 | 幺妹峰日照金山 |

> 注：部分路线信息参考自《徒步百科》及地方文旅部门发布的官方导览资料<sup>[1]</sup>。

## 四、安全须知与风险应对

安全是徒步活动不可逾越的底线。任何忽视风险的行为都可能造成严重后果，甚至危及生命。因此，必须建立系统的风险防控意识。

### （一）行前准备三大原则

1. **心理准备**：树立对自然的敬畏之心，杜绝侥幸心理与“打卡式”心态；
2. **团队管理**：建议4人以上结伴出行，实现“一人遇险，两人求助，一人陪护”的国际通用救援模式；
3. **行程报备**：将详细路线、进出山口位置、预计返回时间告知至少一名亲友，并约定联络机制。

### （二）极端天气应对策略

| 天气 | 风险 | 应对措施 |
|------|------|----------|
| 暴雨 | 山洪、滑坠、失温 | 远离河道，避入岩洞，更换干衣 |
| 雷电 | 雷击高危 | 下撤至低处，双脚并拢蹲姿，禁用电子设备 |
| 浓雾 | 迷路 | 使用GPS+纸质地图，原地等待或原路返回 |
| 暴雪 | 失温、地形覆盖 | 转移至背风区，更换干燥衣物，立即下撤 |

> 特别提醒：收到暴雨橙色及以上预警时，应直接取消行程；雷暴发生时，切勿停留在山顶、山脊或孤立树下。

### （三）常见伤病处理

#### 失温分级与应对

| 分级 | 体温 | 症状 | 处理方式 |
|------|------|------|----------|
| 轻度 | 33–35℃ | 寒战、言语不清 | 停止运动，换干衣，喝温糖水 |
| 重度 | <32℃ | 意识模糊、昏迷 | 严禁烤火，用睡袋包裹送医 |

> **重要警示**：重度失温患者严禁直接加热或饮用热水，否则可能导致心脏骤停。

#### 迷路应对流程

一旦发现偏离路线，应立即执行STOP原则：

- **S**（Stop）：停止前进，保持冷静；
- **T**（Think）：回忆最后已知位置；
- **O**（Observe）：观察周围地形与标志物；
- **P**（Plan）：制定下一步行动计划。

随后可通过“徒步0769”小程序获取精确坐标，并拨打110或120求助，清晰描述所处环境（如“溪流东侧巨石旁”）以便救援定位。

#### 动物伤害处置

- **蛇咬伤**：不切开、不吸毒、不解毒；固定伤肢，冲洗伤口，尽快就医；
- **蜂蜇伤**：拔除毒刺，冰敷，观察过敏反应；
- **蜱虫叮咬**：镊子垂直拔出，消毒后观察发热情况。

> 注意：抗蛇毒血清是唯一特效治疗手段，注射时间越早，存活率越高。

## 五、体能与心理准备

良好的体能储备是顺利完成徒步的基础，而稳定的心理状态则决定了面对困难时的决策质量。

### （一）基础体能训练建议

- 每周进行3–4次慢跑，每次20–30分钟，提升心肺耐力；
- 利用楼梯间进行爬楼训练，模拟山地爬升负荷；
- 加强核心肌群锻炼，如平板支撑、卷腹等动作，增强身体稳定性；
- 出发前一周进行一次模拟负重行走测试，检验装备适配性与体力储备。

### （二）心理建设要点

- 认知自身极限，学会“放弃”也是一种智慧；
- 遇恶劣天气、身体不适时果断终止行程；
- 杜绝“来都来了”心态，安全永远第一位；
- 不盲目挑战“网红野路线”，尊重管理部门划定的禁区。

> 根据《山地户外运动水平等级标准》，年满16周岁的参与者可根据培训经历与运动实践申请相应等级认证，四级及以上需参加中国登山协会授权赛事不少于六次，体现了“能力与路线匹配”的科学理念。

## 六、环保责任：践行LNT无痕山林原则

徒步不仅是个人的旅程，更是一种生态行为。每一位徒步者都应自觉承担起环境保护的责任，践行“无痕山林”（Leave No Trace, LNT）原则。

### LNT七大原则

1. **提前计划与准备**
2. **在可承受地面行进与露营**
3. **妥善处理废弃物**（带走所有垃圾）
4. **保持自然原貌**（不采摘植物、不刻画岩石）
5. **最小化野外用火影响**
6. **尊重野生动植物**（不投喂、不惊扰）
7. **尊重其他使用者**

> **特别提醒**：果皮降解需1年以上，亦会对野生动物造成误食风险，必须打包带走。

在实际操作中，可采取以下具体措施：
- 使用密封袋分类存放厨余与生活垃圾；
- 如厕时挖掘15厘米深的猫洞，事后回填并标记；
- 用矿泉水瓶收集细碎垃圾，防止渗漏；
- 优先使用便携炉具而非明火烹饪。

## 结语：让每一次出发都更安心

徒步不仅是脚步的丈量，更是心智的成长。唯有建立科学认知、做好充分准备、坚守环保底线，才能真正享受山野之美。愿每位徒步者都能平安归来，也为后来者留下一片纯净天地。正如《徒步百科》所倡导：“真正的探险，不是征服自然，而是学会与之共存。”<sup>[1]</sup>

[1]:http://www.zxhsd.com/kgsm/ts/2025/11/04/6716410.shtml "徒步百科：徒步帮|责编:许姗//汪昊宇 : 生活娱乐 :生活用书 :保健养生 :浙江新华书店网群"
[2]:https://m.dzplus.dzng.com/share/general/0/NEWS2874270EFMGUZPGTKPDI "序跋丨《徒步百科》推荐序_大众新闻_大众新媒体大平台"
[3]:https://www.douban.com/doubanapp/dispatch?uri=/review/17184809 "让我从户外菜鸟秒变安全达人（徒步百科）书评"
[4]:https://mall.96192.com/product/detail/1212472 "徒步中国"
[5]:https://book.douban.com/subject/37536789/ "徒步百科 (豆瓣)"
[6]:https://page.sm.cn/blm/midpage-317/index?h=iknow.v4_2.quark.cn&id=28_21800965cc7ad878aa74d45c348d9126 "户外徒步0基础入门，这份攻略请收好"
[7]:https://sz.people.com.cn/n2/2026/0107/c202846-41465718.html "“深圳远足径”导览上线"
[8]:https://www.toutiao.com/a7592038982356173364/ "深圳远足径导览上线啦！快来看看如何开启山海之旅 - 今日头条"
[9]:https://yjt.hubei.gov.cn/yjkp/yjkp/202603/t20260331_5903087.shtml "户外登山，安全为先-湖北省应急管理厅"
[10]:https://www.douyin.com/video/7633676080179711270 "户外徒步装备分享 #徒步 #大学生 #装备分享"
[11]:http://sd.cma.gov.cn/xwzx_3497/qxkp/202601/t20260109_7535458.html "山东省气象局-- 高山有界 越己知止——高山徒步切守安全与生态双底线"
````

## File: ai-service/agent/__init__.py
````python

````

## File: ai-service/agent/advisors.py
````python
logger = logging.getLogger("ai-service.agent")
⋮----
class LoggerAdvisor
⋮----
def __init__(self)
⋮----
def on_step(self, step_type, content: str | None = None)
⋮----
step = dict(step_type)
action = step.get("action") or step.get("type") or "step"
text = str(step.get("content", ""))
⋮----
action = str(step_type)
text = content or ""
step = {"type": action, "content": text}
⋮----
def get_steps(self) -> list
⋮----
def clear(self)
⋮----
class ReReadAdvisor
⋮----
def __init__(self, window_size: int | None = None, recent_n: int | None = None)
⋮----
def get_recent_context(self, history: list) -> list
⋮----
limit = max(self.recent_n * 2, 0)
⋮----
recent = history[-limit:] if len(history) > limit else history
````

## File: ai-service/agent/agent.py
````python
logger = logging.getLogger("ai-service.agent")
⋮----
MAX_STEPS = 6
MAX_EVENT_CHARS = 1200
MAX_ARGS_CHARS = 500
⋮----
BASE_TOOL_NAMES = [
⋮----
AVAILABLE_TOOL_MAP = {
⋮----
AVAILABLE_TOOLS = [AVAILABLE_TOOL_MAP[name] for name in BASE_TOOL_NAMES]
⋮----
INTENT_TOOL_NAMES: dict[AgentIntent, list[str]] = {
⋮----
def _unique_tool_names(names: list[str]) -> list[str]
⋮----
seen: set[str] = set()
result: list[str] = []
⋮----
def _prefetched_tool_names(context: AgentRequestContext) -> set[str]
⋮----
names: set[str] = set()
⋮----
tool = item.get("tool") if isinstance(item, dict) else None
⋮----
def select_tools_for_context(context: AgentRequestContext) -> list
⋮----
tool_names = ["terminate"]
⋮----
tool_names = ["risk_assessment", "terminate"]
⋮----
tool_names = INTENT_TOOL_NAMES.get(context.intent, INTENT_TOOL_NAMES[AgentIntent.GENERAL_CHAT])
⋮----
def validate_tool_configuration() -> dict[str, Any]
⋮----
available_names = set(AVAILABLE_TOOL_MAP)
registered_names = {md.name for md in tool_registry.list_all_tools()}
risk_names = set(TOOL_RISK_MAP)
intent_names = {
base_names = set(BASE_TOOL_NAMES)
⋮----
issues: list[dict[str, Any]] = []
⋮----
def add_issue(kind: str, names: set[str]) -> None
⋮----
def _approval_required_payload(tool_name: str, args: dict[str, Any]) -> str
⋮----
payload = {
⋮----
def _guard_tool_for_confirmation(tool)
⋮----
md = tool_registry.get(tool.name)
⋮----
async def guarded_runner(**kwargs) -> str
⋮----
def apply_tool_confirmation_guards(tools: list) -> list
⋮----
tool_registry = ToolRegistry()
⋮----
def _compact_text(value: Any, limit: int = MAX_EVENT_CHARS) -> str
⋮----
text = ""
⋮----
text = value
⋮----
text = json.dumps(value, ensure_ascii=False)
⋮----
text = str(value)
text = " ".join(text.split())
⋮----
def _jsonable(value: Any) -> Any
⋮----
def _strip_leading_numbered_lines(text: str) -> str
⋮----
lines = [line.strip() for line in text.splitlines() if line.strip()]
⋮----
stripped = []
⋮----
class AIAgent
⋮----
def __init__(self, memory_manager=None, llm_config: RuntimeLlmConfig | None = None)
⋮----
base_url = llm_config.base_url if llm_config and llm_config.base_url else settings.openai_base_url
api_key = llm_config.api_key if llm_config and llm_config.api_key else settings.openai_api_key
model = llm_config.model if llm_config and llm_config.model else settings.openai_model
⋮----
memory_model = model if llm_config and llm_config.model else None
config = MemoryConfig(
⋮----
@staticmethod
    def get_tool_registry() -> ToolRegistry
⋮----
def _build_system_prompt(self, context: AgentRequestContext, selected_tools: list) -> str
⋮----
slot_lines = []
⋮----
slots_text = "\n".join(slot_lines) if slot_lines else "- 未抽取到稳定槽位"
tool_names = "、".join(tool.name for tool in selected_tools) or "无"
location_text = "<Location>\n- 未提供当前位置\n</Location>"
⋮----
location_items = [
location_text = "<Location>\n" + ("\n".join(location_items) or "- 已授权但坐标为空") + "\n</Location>"
rewritten_text = context.rewritten_query or context.raw_query
prefetch_text = "<PrefetchedEvidence>\n- 无\n</PrefetchedEvidence>"
⋮----
result_lines = [
prefetch_text = "<PrefetchedEvidence>\n" + "\n".join(result_lines) + "\n</PrefetchedEvidence>"
⋮----
system_msg = (
⋮----
def _make_state_modifier(self, context: AgentRequestContext, selected_tools: list)
⋮----
def _state_modifier(state: dict) -> list
⋮----
def _rewrite_user_query(self, message: str) -> str
⋮----
rewritten = self._query_rewriter.humanize_for_answer(message)
⋮----
def _clean_final_answer(self, text: str) -> str
⋮----
cleaned = clean_display_text(text, preserve_lines=True, keep_list_markers=False)
cleaned = _strip_leading_numbered_lines(cleaned)
⋮----
def _is_current_location_weather_request(self, context: AgentRequestContext) -> bool
⋮----
text = context.raw_query
weather_words = ("天气", "适合", "能去", "可以去", "徒步吗", "去徒步")
⋮----
def _location_tool_args(self, context: AgentRequestContext) -> dict[str, Any]
⋮----
location = context.current_location
args: dict[str, Any] = {}
⋮----
def _weather_tool_args(self, context: AgentRequestContext, geo_result: dict[str, Any] | None = None) -> dict[str, Any]
⋮----
primary = (geo_result or {}).get("primary") or {}
⋮----
adcode = primary.get("adcode") or (location.adcode if location else None)
⋮----
async def _prefetch_current_location_weather(self, context: AgentRequestContext) -> list[dict[str, Any]]
⋮----
events: list[dict[str, Any]] = []
geo_args = self._location_tool_args(context)
⋮----
geo_result = await geo_lookup.ainvoke(geo_args)
⋮----
geo_result = {"ok": False, "message": f"geo_lookup 调用失败: {str(e)}"}
safe_geo = _jsonable(geo_result)
⋮----
weather_args = self._weather_tool_args(context, geo_result if isinstance(geo_result, dict) else None)
⋮----
weather_result = await weather_lookup.ainvoke(weather_args)
⋮----
weather_result = {"ok": False, "message": f"weather_lookup 调用失败: {str(e)}"}
safe_weather = _jsonable(weather_result)
⋮----
def _build_react_agent(self, context: AgentRequestContext)
⋮----
selected_tools = select_tools_for_context(context)
⋮----
def _build_messages(self, message: str, history: list | None = None) -> list
⋮----
messages = []
⋮----
role = msg.get("role", "")
content = msg.get("content", "")
⋮----
async def _inject_memory_context(self, history: list | None, message: str) -> None
⋮----
ctx = await asyncio.to_thread(self.memory_manager.build_runtime_context, history or [], message)
⋮----
commit_history = [*(history or []), {"role": "user", "content": message}]
⋮----
task_state = {"slots": context.slots.to_dict(), "intent": context.intent.value}
⋮----
async def _execute_agent(self, messages: list, context: AgentRequestContext, react_agent=None) -> dict
⋮----
agent = react_agent or self._build_react_agent(context)
⋮----
result = await agent.ainvoke(
output = ""
intermediate_steps = []
⋮----
content = self._message_content(msg)
⋮----
output = content
⋮----
exit_result = self.exit_controller.from_tool_result(
⋮----
exit_result = self.exit_controller.from_exception(e, context=context)
⋮----
context = understand_request(message, scenario=scenario, current_location=current_location)
⋮----
messages = self._build_messages(context.rewritten_query or message, history)
⋮----
result = await self._execute_agent(messages, context)
⋮----
def _message_content(self, msg: Any) -> str
⋮----
content = getattr(msg, "content", "")
⋮----
parts = []
⋮----
def _extract_tool_calls(self, msg: Any) -> list[dict]
⋮----
raw_calls = getattr(msg, "tool_calls", None) or []
additional = getattr(msg, "additional_kwargs", None) or {}
raw_calls = raw_calls or additional.get("tool_calls", [])
⋮----
calls = []
⋮----
function = call.get("function") or {}
name = call.get("name") or function.get("name") or ""
raw_args = call.get("args")
⋮----
raw_args = call.get("arguments", function.get("arguments", ""))
call_id = call.get("id") or call.get("tool_call_id") or ""
args_dict = raw_args if isinstance(raw_args, dict) else None
⋮----
def _iter_update_messages(self, update: Any)
⋮----
messages = payload.get("messages", [])
⋮----
messages = payload
⋮----
messages = [payload]
⋮----
messages = [messages]
⋮----
def _is_tool_message(self, node_name: str, msg: Any) -> bool
⋮----
msg_type = getattr(msg, "type", "")
⋮----
def _tool_result_name(self, msg: Any, pending_tools: dict[str, tuple[int, str]]) -> tuple[int, str]
⋮----
call_id = getattr(msg, "tool_call_id", "") or ""
⋮----
payload = json.loads(content)
⋮----
step = fallback_step or 1
req = tool_registry.get_call_request(tool_name, payload.get("args") or {})
risk_level = req.risk_level.value if req else RiskLevel.MEDIUM.value
⋮----
async def _stream_react_events(self, messages: list, context: AgentRequestContext) -> AsyncGenerator[dict, None]
⋮----
react_agent = self._build_react_agent(context)
⋮----
result = await self._execute_agent(messages, context, react_agent=react_agent)
⋮----
pending_tools: dict[str, tuple[int, str]] = {}
blocked_tool_call_ids: set[str] = set()
current_step = 0
final_text = ""
saw_update = False
⋮----
saw_update = True
⋮----
approval_event = self._approval_event_from_tool_message(
⋮----
step = current_step or 1
tool_result_event = {
⋮----
text_event = exit_result.text_event()
⋮----
tool_calls = self._extract_tool_calls(msg)
⋮----
req = tool_registry.get_call_request(call["name"], call.get("args_raw") or {})
⋮----
risk_level = req.risk_level.value
needs_confirmation = req.needs_confirmation
rate_exceeded = req.rate_limit_remaining is not None and req.rate_limit_remaining == 0
⋮----
risk_level = RiskLevel.MEDIUM.value
needs_confirmation = False
rate_exceeded = False
content = f"第 {current_step} 步：调用 {call['name']}，参数：{call['args']}"
⋮----
final_text = self._clean_final_answer(content)
⋮----
final_text = result.get("output", "任务已完成")
⋮----
exit_result = self.exit_controller.from_exception(
⋮----
assistant_parts: list[str] = []
````

## File: ai-service/agent/intake.py
````python
class AgentIntent(str, Enum)
⋮----
KNOWLEDGE_QA = "knowledge_qa"
ROUTE_PLAN = "route_plan"
GEAR_CHECK = "gear_check"
RISK_ASSESSMENT = "risk_assessment"
REPORT_EXPORT = "report_export"
GENERAL_CHAT = "general_chat"
⋮----
@dataclass
class HikingSlots
⋮----
destination: str | None = None
date: str | None = None
days: int | None = None
origin: str | None = None
experience: str | None = None
camping: bool | None = None
group_size: int | None = None
gear_level: str | None = None
season: str | None = None
⋮----
def to_dict(self) -> dict[str, object]
⋮----
@dataclass
class CurrentLocation
⋮----
latitude: float | None = None
longitude: float | None = None
accuracy: float | None = None
province: str | None = None
city: str | None = None
district: str | None = None
adcode: str | None = None
address: str | None = None
source: str | None = None
⋮----
@property
    def label(self) -> str
⋮----
@dataclass
class AgentRequestContext
⋮----
raw_query: str
intent: AgentIntent
slots: HikingSlots
current_location: CurrentLocation | None = None
rewritten_query: str | None = None
prefetched_tool_results: list[dict[str, object]] = field(default_factory=list)
missing_slots: list[str] = field(default_factory=list)
clarifying_question: str = ""
scenario: str | None = None
search_queries: list[str] = field(default_factory=list)
⋮----
@property
    def needs_clarification(self) -> bool
⋮----
SCENARIO_TO_INTENT = {
⋮----
CHINESE_NUMBERS = {
⋮----
SLOT_LABELS = {
⋮----
TIME_PREFIXES = (
⋮----
DESTINATION_PREFIXES = (
⋮----
GENERIC_DESTINATIONS = {
⋮----
def _normalize(text: str) -> str
⋮----
def _number_value(raw: str | None) -> int | None
⋮----
raw = raw.strip()
⋮----
def _parse_days(text: str) -> int | None
⋮----
match = re.search(r"(\d+|[一二两三四五六七八九十])\s*天", text)
⋮----
def _parse_date(text: str) -> str | None
⋮----
patterns = [
⋮----
match = re.search(r"(\d{1,2}\s*月\s*\d{1,2}\s*[日号])", text)
⋮----
def _clean_destination(candidate: str) -> str
⋮----
value = candidate.strip(" ，,。.!！?？：:；;、")
changed = True
⋮----
changed = False
⋮----
value = value[len(prefix):].strip(" ，,。.!！?？：:；;、")
⋮----
value = re.sub(r"(适合|安全吗|安全|怎么样|咋样|攻略|路线|行程|计划|PDF|Markdown).*$", "", value)
⋮----
def _parse_destination(text: str) -> str | None
⋮----
destination_patterns = [
⋮----
matches = re.findall(pattern, text)
⋮----
destination = _clean_destination(matches[-1])
⋮----
match = re.search(
⋮----
destination = _clean_destination(match.group(1))
⋮----
def _parse_origin(text: str) -> str | None
⋮----
match = re.search(r"(?:从|出发地是|我在)([A-Za-z0-9\u4e00-\u9fff·\-]{2,12})(?:出发|过去|去|周边|$)", text)
⋮----
def _parse_experience(text: str) -> str | None
⋮----
def _parse_group_size(text: str) -> int | None
⋮----
match = re.search(r"(\d+)\s*人", text)
⋮----
def _parse_gear_level(text: str) -> str | None
⋮----
def _parse_season(text: str) -> str | None
⋮----
def _float_value(value: object) -> float | None
⋮----
def _str_value(value: object) -> str | None
⋮----
text = str(value).strip()
⋮----
def _normalize_current_location(raw: CurrentLocation | dict | None) -> CurrentLocation | None
⋮----
raw_latitude = raw.get("latitude") if raw.get("latitude") is not None else raw.get("lat")
raw_longitude = raw.get("longitude") if raw.get("longitude") is not None else raw.get("lng")
location = CurrentLocation(
⋮----
def _should_use_current_location(text: str, intent: AgentIntent) -> bool
⋮----
location_words = ("附近", "周边", "当前位置", "我这里", "我这边", "本地")
weather_words = ("天气", "适合", "能去", "可以去", "徒步吗", "去徒步")
⋮----
def _detect_intent(text: str, scenario: str | None = None) -> AgentIntent
⋮----
normalized_scenario = (scenario or "").strip().lower()
⋮----
upper_text = text.upper()
⋮----
def _build_missing_slots(intent: AgentIntent, slots: HikingSlots) -> list[str]
⋮----
required: dict[AgentIntent, list[str]] = {
⋮----
missing: list[str] = []
slot_values = slots.to_dict()
⋮----
def _build_clarifying_question(missing_slots: list[str]) -> str
⋮----
labels = [SLOT_LABELS.get(slot, slot) for slot in missing_slots]
⋮----
target = labels[0]
⋮----
target = f"{labels[0]}和{labels[1]}"
⋮----
target = "、".join(labels[:-1]) + f"和{labels[-1]}"
⋮----
def _build_search_queries(intent: AgentIntent, slots: HikingSlots) -> list[str]
⋮----
destination = slots.destination
queries = [f"{destination} 徒步 路线 里程 爬升 下撤点"]
⋮----
days = f"{slots.days}天" if slots.days else ""
⋮----
text = _normalize(message)
location = _normalize_current_location(current_location)
intent = _detect_intent(text, scenario)
slots = HikingSlots(
⋮----
missing_slots = _build_missing_slots(intent, slots)
````

## File: ai-service/agent/prompts.py
````python
SYSTEM_PROMPT = """<Role>
⋮----
NEXT_STEP_PROMPT = """<DecisionPolicy>
````

## File: ai-service/agent/task_exit.py
````python
GraphRecursionError = None
⋮----
class AgentExitStatus(str, Enum)
⋮----
COMPLETED = "completed"
WAITING_FOR_USER = "waiting_for_user"
BUDGET_EXHAUSTED = "budget_exhausted"
ERROR = "error"
⋮----
@dataclass(slots=True)
class AgentExit
⋮----
status: AgentExitStatus
reason: str
final_text: str = ""
metadata: dict[str, Any] = field(default_factory=dict)
⋮----
def text_event(self) -> dict[str, Any] | None
⋮----
def done_event(self) -> dict[str, Any]
⋮----
class AgentTaskExitController
⋮----
_BUDGET_MARKERS = (
⋮----
def __init__(self, max_steps: int)
⋮----
def completed(self, reason: str = "agent_completed") -> AgentExit
⋮----
exit_status = AgentExitStatus(status)
⋮----
exit_status = AgentExitStatus.ERROR
⋮----
reason = self._extract_terminate_reason(content)
⋮----
status = AgentExitStatus.WAITING_FOR_USER
final_text = f"我需要你补充一个关键信息后再继续：{reason}"
⋮----
status = AgentExitStatus.COMPLETED
final_text = f"任务已结束：{reason}"
⋮----
final_text = "任务已完成。"
⋮----
def _is_budget_exhausted(self, exc: Exception) -> bool
⋮----
text = f"{type(exc).__name__} {str(exc)}".lower()
⋮----
def _budget_exhausted_message(self, context: Any | None) -> str
⋮----
def _has_prefetched_evidence(self, context: Any | None) -> bool
⋮----
results = getattr(context, "prefetched_tool_results", None) if context is not None else None
⋮----
def _extract_terminate_reason(self, content: str) -> str
⋮----
text = " ".join(str(content or "").split())
marker = "原因:"
⋮----
reason = text.split(marker, 1)[1].strip()
⋮----
def _looks_waiting_for_user(self, reason: str) -> bool
````

## File: ai-service/api/__init__.py
````python

````

## File: ai-service/api/chat.py
````python
logger = logging.getLogger("ai-service.chat")
chat_router = APIRouter(prefix="/chat")
⋮----
def _missing_llm_config_message() -> str
⋮----
def _request_llm_config(req: ChatRequest)
⋮----
def _request_current_location(req: ChatRequest) -> dict | None
⋮----
def _has_llm_api_key(req: ChatRequest) -> bool
⋮----
runtime_llm = _request_llm_config(req)
⋮----
def _get_memory(chat_id: str) -> FileChatMemory
⋮----
def _attach_confirmation_if_needed(event: dict, store, chat_id: str, step: int) -> None
⋮----
metadata = event.get("metadata")
⋮----
args = metadata.get("args_raw")
⋮----
args = metadata.get("args") if isinstance(metadata.get("args"), dict) else {}
⋮----
cid = store.add(
⋮----
@chat_router.post("/sync", response_model=ChatResponse)
async def chat_sync(req: ChatRequest)
⋮----
memory = _get_memory(req.chat_id)
history = memory.get_messages()
⋮----
agent = AIAgent(llm_config=_request_llm_config(req))
kwargs = {}
⋮----
result = await agent.aexecute(req.message, history, **kwargs)
⋮----
reply = result.get("output", str(result))
⋮----
@chat_router.get("/health")
async def chat_health()
⋮----
agent = AIAgent()
⋮----
err_str = str(e).lower()
⋮----
@chat_router.post("/sse")
async def chat_sse(req: ChatRequest)
⋮----
async def event_stream()
⋮----
assistant_parts: list[str] = []
done_sent = False
step = 0
store = get_store()
⋮----
stream = agent.aexecute_stream(req.message, history, **kwargs)
⋮----
event_type = event.get("type")
⋮----
done_sent = True
⋮----
assistant_reply = "".join(assistant_parts).strip()
⋮----
@chat_router.get("/history/{chat_id}")
async def chat_history(chat_id: str)
⋮----
"""Get chat history for a given chat_id."""
⋮----
memory = _get_memory(chat_id)
messages = memory.get_messages()
⋮----
@chat_router.post("/confirm", response_model=ConfirmResponse)
async def chat_confirm(req: ConfirmRequest)
⋮----
"""用户确认或拒绝某条高风险工具调用。"""
⋮----
action = req.action.strip().lower()
⋮----
rec = store.get(req.confirmation_id)
⋮----
@chat_router.get("/pending/{chat_id}", response_model=PendingConfirmationsResponse)
async def chat_pending(chat_id: str)
⋮----
pending = store.get_pending_by_chat(chat_id)
items = [
````

## File: ai-service/api/confirmation_store.py
````python
@dataclass
class PendingConfirmation
⋮----
confirmation_id: str
tool_name: str
args: dict
chat_id: str
step: int
status: str = "pending"
created_at: float = 0.0
⋮----
def __post_init__(self)
⋮----
class ConfirmationStore
⋮----
def __init__(self)
⋮----
cid = confirmation_id or str(uuid.uuid4())
⋮----
def get(self, confirmation_id: str) -> Optional[PendingConfirmation]
⋮----
def confirm(self, confirmation_id: str) -> bool
⋮----
rec = self._data.get(confirmation_id)
⋮----
def reject(self, confirmation_id: str) -> bool
⋮----
def get_pending_by_chat(self, chat_id: str) -> list[PendingConfirmation]
⋮----
def cleanup_expired(self, max_age: float = 3600) -> int
⋮----
now = time.time()
⋮----
expired = [
⋮----
_store: Optional[ConfirmationStore] = None
⋮----
def get_store() -> ConfirmationStore
⋮----
_store = ConfirmationStore()
````

## File: ai-service/api/models_router.py
````python
logger = logging.getLogger("ai-service.models")
models_router = APIRouter(prefix="/models")
⋮----
@models_router.post("/fetch", response_model=ModelsFetchResponse)
async def models_fetch(req: ModelsFetchRequest)
⋮----
base_url = req.base_url.rstrip("/")
url = f"{base_url}/models"
⋮----
resp = await client.get(
⋮----
data = resp.json()
raw = data.get("data", [])
model_ids = sorted(
````

## File: ai-service/api/models.py
````python
class ChatRequest(BaseModel)
⋮----
message: str
chat_id: str = "default"
scenario: Optional[str] = None
current_location: Optional["CurrentLocationPayload"] = None
model_settings: Optional["RuntimeModelSettings"] = None
⋮----
class ChatResponse(BaseModel)
⋮----
content: str
⋮----
class RAGUploadResponse(BaseModel)
⋮----
filename: str
chunks: int
status: str = "success"
⋮----
class RAGDocument(BaseModel)
⋮----
id: str
⋮----
status: Optional[str] = None
chunk_count: int
⋮----
class RuntimeLlmConfig(BaseModel)
⋮----
base_url: str = ""
api_key: str = ""
model: str = ""
⋮----
class CurrentLocationPayload(BaseModel)
⋮----
latitude: Optional[float] = None
longitude: Optional[float] = None
accuracy: Optional[float] = None
province: str = ""
city: str = ""
district: str = ""
adcode: str = ""
address: str = ""
source: str = ""
⋮----
class RuntimeEmbeddingConfig(RuntimeLlmConfig)
⋮----
dimensions: Optional[int] = None
⋮----
class RuntimeRerankConfig(RuntimeLlmConfig)
⋮----
class RuntimeModelSettings(BaseModel)
⋮----
llm: Optional[RuntimeLlmConfig] = None
embedding: Optional[RuntimeEmbeddingConfig] = None
rerank: Optional[RuntimeRerankConfig] = None
⋮----
class RAGQuery(BaseModel)
⋮----
question: str
⋮----
model_settings: Optional[RuntimeModelSettings] = None
⋮----
class SSEEvent(BaseModel)
⋮----
type: str  # thought, tool_call, tool_result, text, done, error
⋮----
metadata: Optional[dict] = None
⋮----
class ModelsFetchRequest(BaseModel)
⋮----
base_url: str
api_key: str
⋮----
class ModelsFetchResponse(BaseModel)
⋮----
models: list[str]
⋮----
class FeishuSyncRequest(BaseModel)
⋮----
"""同步飞书文档的请求参数。"""
⋮----
doc_token: str  # 文档 token 或完整 URL
title: str = ""  # 可选标题，默认从 URL 提取
doc_type: str = "docx"
⋮----
class FeishuDocRef(BaseModel)
⋮----
token: str
title: str
⋮----
class FeishuSyncResponse(BaseModel)
⋮----
documents: list[FeishuDocRef] = []
⋮----
class FeishuDefaultSyncRequest(BaseModel)
⋮----
space_id: Optional[str] = None
folder_token: Optional[str] = None
query: str = ""
⋮----
class FeishuDefaultSyncResponse(BaseModel)
⋮----
"""批量同步飞书文档的响应结果。"""
⋮----
synced_count: int = 0
⋮----
class ConfirmRequest(BaseModel)
⋮----
confirmation_id: str
action: str = "confirm"
⋮----
class ConfirmResponse(BaseModel)
⋮----
status: str
⋮----
class PendingConfirmationItem(BaseModel)
⋮----
tool_name: str
args: dict
step: int
⋮----
created_at: float
⋮----
class PendingConfirmationsResponse(BaseModel)
⋮----
chat_id: str
pending: list[PendingConfirmationItem]
````

## File: ai-service/api/rag.py
````python
logger = logging.getLogger("ai-service.rag")
rag_router = APIRouter(prefix="/rag")
⋮----
RAG_DOCS_DIR = Path("./rag_docs")
⋮----
DIRECT_ANSWER_PATTERNS = {
⋮----
def direct_rag_answer(question: str) -> str | None
⋮----
normalized = question.strip().lower().rstrip("。！？!?")
⋮----
def _runtime_llm_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict
⋮----
config = model_settings.llm
⋮----
def _runtime_embedding_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict
⋮----
config = model_settings.embedding
⋮----
def _runtime_rerank_kwargs_from_settings(model_settings: RuntimeModelSettings | None) -> dict
⋮----
config = model_settings.rerank
⋮----
def _parse_runtime_model_settings(raw: str | None) -> RuntimeModelSettings | None
⋮----
data = json.loads(raw)
⋮----
def _sse_event(event_type: str, content: str = "", metadata: dict | None = None) -> str
⋮----
payload = {"type": event_type, "content": content}
⋮----
def _preview_text(text: str, limit: int = 260) -> str
⋮----
normalized = clean_display_text(text)
⋮----
def _document_key(doc) -> str
⋮----
metadata = doc.metadata or {}
⋮----
value = metadata.get(key)
⋮----
def summarize_retrieved_documents(docs: list) -> dict
⋮----
"""Build a compact document-search summary for the frontend."""
grouped: dict[str, dict] = {}
⋮----
key = _document_key(doc)
current = grouped.setdefault(
⋮----
documents = list(grouped.values())
⋮----
def _dedupe_documents(docs: list) -> list
⋮----
seen_keys: set[str] = set()
deduped_docs = []
⋮----
meta = doc.metadata or {}
dedup_key = (
⋮----
@rag_router.get("/health")
async def rag_health()
⋮----
retriever = VectorStoreRetriever()
document_count = len([f for f in RAG_DOCS_DIR.iterdir() if f.is_file()])
⋮----
"""Upload a document for RAG processing."""
⋮----
file_path = RAG_DOCS_DIR / file.filename
content = await file.read()
⋮----
loader = DocumentLoader()
docs = loader.load_and_split(str(file_path))
⋮----
runtime_settings = _parse_runtime_model_settings(model_settings)
retriever = VectorStoreRetriever(**_runtime_embedding_kwargs_from_settings(runtime_settings))
⋮----
@rag_router.post("/query")
async def rag_query(req: RAGQuery)
⋮----
"""RAG query endpoint with SSE streaming."""
⋮----
async def event_stream()
⋮----
direct_answer = direct_rag_answer(req.question)
⋮----
# 检测飞书 URL 并实时抓取文档
feishu_docs: list = []
⋮----
links = find_feishu_links(req.question)
⋮----
loader = FeishuDocLoader()
⋮----
embedding_kwargs = _runtime_embedding_kwargs_from_settings(req.model_settings)
⋮----
retriever = VectorStoreRetriever(**embedding_kwargs)
⋮----
llm_kwargs = _runtime_llm_kwargs_from_settings(req.model_settings)
rewriter = QueryRewriter(**llm_kwargs)
⋮----
augmenter = ContextAugmenter(**llm_kwargs)
⋮----
augmenter = ContextAugmenter()
rerank_kwargs = _runtime_rerank_kwargs_from_settings(req.model_settings)
⋮----
reranker = Reranker(**rerank_kwargs)
⋮----
reranker = Reranker()
⋮----
queries = rewriter.rewrite(req.question)
⋮----
all_docs = []
retrieval_error = ""
⋮----
hybrid_search = getattr(retriever, "hybrid_search", None)
⋮----
all_docs = hybrid_search(queries, k=4, status_filter=req.status)
⋮----
all_docs = _dedupe_documents(all_docs)
⋮----
retrieval_error = str(e)
⋮----
all_docs = feishu_docs + all_docs
⋮----
all_docs = reranker.rerank(req.question, all_docs)
⋮----
humanize_for_answer = getattr(rewriter, "humanize_for_answer", None)
humanized_question = (
⋮----
document_summary = summarize_retrieved_documents(all_docs)
⋮----
has_streamed = False
stream_fn = getattr(augmenter, "augment_stream", None)
⋮----
has_streamed = True
⋮----
augmented = augmenter.augment(humanized_question, all_docs)
⋮----
context_preview = summarize_retrieved_documents(all_docs).get("documents", [])[:2]
augmented = (
⋮----
@rag_router.get("/documents")
async def rag_documents()
⋮----
docs = []
⋮----
@rag_router.post("/feishu/sync", response_model=FeishuSyncResponse)
async def feishu_sync(req: FeishuSyncRequest)
⋮----
doc_token = extract_doc_token(req.doc_token)
doc_refs: list[FeishuDocRef] = []
⋮----
docs = loader.load_and_split(
⋮----
@rag_router.post("/feishu/default-sync", response_model=FeishuDefaultSyncResponse)
async def feishu_default_sync(req: FeishuDefaultSyncRequest)
⋮----
space_id = req.space_id or settings.feishu_default_space_id
folder_token = req.folder_token or settings.feishu_default_folder_token
⋮----
syncer = FeishuDefaultSyncer(loader, retriever)
⋮----
synced = syncer.sync_from_folder(folder_token)
⋮----
synced = syncer.sync_from_space(space_id)
⋮----
doc_refs = [
````

## File: ai-service/api/tools.py
````python
tools_router = APIRouter(prefix="/tools")
⋮----
def _mcp_configured() -> bool
⋮----
def _external_keys_status() -> dict[str, bool]
⋮----
@tools_router.get("")
async def list_tools(include_hidden: bool = False)
⋮----
registry = AIAgent.get_tool_registry()
tools = registry.tools_api_response(include_hidden=include_hidden)
⋮----
@tools_router.get("/health")
async def tools_health()
⋮----
visible = registry.list_tools(include_hidden=False)
all_tools = registry.list_all_tools()
configured = _mcp_configured()
````

## File: ai-service/main.py
````python
logger = logging.getLogger("ai-service")
⋮----
@asynccontextmanager
async def lifespan(app: FastAPI)
⋮----
app = FastAPI(
⋮----
@app.get("/health")
async def health()
````

## File: ai-service/mcp/__init__.py
````python

````

## File: ai-service/mcp/client.py
````python
logger = logging.getLogger("ai-service.mcp")
⋮----
class MCPClient
⋮----
def __init__(self)
⋮----
async def connect_stdio(self, command: str, args: list[str] | None = None)
⋮----
args = []
⋮----
async def _send_request(self, method: str, params: dict | None = None) -> dict
⋮----
"""Send a JSON-RPC request to the MCP server."""
⋮----
request = {
⋮----
write_result = self.process.stdin.write((json.dumps(request) + "\n").encode())
⋮----
line = await asyncio.wait_for(self.process.stdout.readline(), timeout=10.0)
response = json.loads(line.decode())
⋮----
async def list_tools(self) -> list[dict]
⋮----
response = await self._send_request("list_tools")
tools = response.get("result", {}).get("tools", [])
⋮----
async def call_tool(self, tool_name: str, arguments: dict | None = None) -> Any
⋮----
"""Call a tool on the MCP server."""
⋮----
response = await self._send_request("call_tool", {
result = response.get("result", {})
content = result.get("content", [])
⋮----
def convert_to_langchain_tools(self) -> list
⋮----
"""Convert MCP tools to LangChain-compatible tools.
        This creates dynamic @tool-decorated functions for each MCP tool.
        """
lc_tools = []
⋮----
input_schema = tool_info.get("inputSchema", {})
⋮----
model = self._build_args_model(name, input_schema)
⋮----
lc_tool = StructuredTool.from_function(
⋮----
"""将 MCP inputSchema 转换为 Pydantic 参数模型。"""
⋮----
properties = schema.get("properties")
⋮----
type_map = {"string": str, "integer": int, "number": float, "boolean": bool}
fields = {}
⋮----
py_type = type_map.get(info.get("type", "string"), str)
⋮----
def _make_runner(self, name: str)
⋮----
async def runner(**kwargs) -> str
⋮----
result = await self.call_tool(name, kwargs)
⋮----
async def close(self)
⋮----
terminate_result = self.process.terminate()
⋮----
async def load_mcp_tools(server_configs: dict | None) -> list
⋮----
loaded = []
⋮----
command = config.get("command") if isinstance(config, dict) else None
⋮----
args = config.get("args", []) or []
client = MCPClient()
````

## File: ai-service/memory_data/chat-1778939095217.json
````json
{
  "chat_id": "chat-1778939095217",
  "messages": [
    {
      "role": "user",
      "content": "1"
    }
  ]
}
````

## File: ai-service/memory_data/chat-1f98ad51-d9d9-4da6-acf7-ba9d020e970d.json
````json
{
  "chat_id": "chat-1f98ad51-d9d9-4da6-acf7-ba9d020e970d",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "Sorry, need more steps to process this request."
    }
  ]
}
````

## File: ai-service/memory_data/chat-361239fe-5541-4c84-9caf-2af16fcd06d8.json
````json
{
  "chat_id": "chat-361239fe-5541-4c84-9caf-2af16fcd06d8",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "Sorry, need more steps to process this request."
    }
  ]
}
````

## File: ai-service/memory_data/chat-3da6ba32-288d-400e-b5ba-9b3cb01babb1.json
````json
{
  "chat_id": "chat-3da6ba32-288d-400e-b5ba-9b3cb01babb1",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "Sorry, need more steps to process this request."
    }
  ]
}
````

## File: ai-service/memory_data/chat-6ffb0cff-c060-4357-9864-a7dad4d4f1d1.json
````json
{
  "chat_id": "chat-6ffb0cff-c060-4357-9864-a7dad4d4f1d1",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "哈哈，看来您对徒步感兴趣啦！🎉\n\n不过现在信息还有点少，不好直接推荐。为了给您推荐合适的路线，想先了解一下：\n\n1. **您打算去哪里徒步？**（城市/区域/国家？）\n2. **大概什么时间出发？**（今天？周末？）\n3. **您希望的难度和时长？**（半日休闲、全天挑战、还是多日重装？）\n4. **偏好什么风景类型？**（山林、海边、湖泊、草原？）\n\n您先说说想法，我来帮您筛选好路线~ 😊"
    }
  ]
}
````

## File: ai-service/memory_data/chat-a8e377aa-cbb5-493a-9452-5c9ad55a17a9.json
````json
{
  "chat_id": "chat-a8e377aa-cbb5-493a-9452-5c9ad55a17a9",
  "messages": [
    {
      "role": "user",
      "content": "生成行程"
    }
  ]
}
````

## File: ai-service/memory_data/chat-dc3c1c3c-9197-4adb-bd24-ae3a3e4ef56a.json
````json
{
  "chat_id": "chat-dc3c1c3c-9197-4adb-bd24-ae3a3e4ef56a",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "你好！很高兴为你提供徒步决策帮助 🥾\n\n你问\"今天天气是否适合徒步\"，但还缺少一个**最关键的信息**——**你想去哪里徒步？**\n\n请告诉我你所在的城市或具体的徒步目的地（比如某个公园、山区或路线），我就能帮你查询今天的天气情况，并结合户外安全知识给你针对性建议！"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "看起来你还是在问 **今天是否适合徒步** 🚶‍♂️，但上一个问题我已经回复过了——**缺少最关键的信息**：你打算去哪里徒步？\n\n目前我知道的只有：\n- **时间**：今天\n- **目的地**：未指定\n\n不同城市、不同山区的天气和路况差别很大，今天有的地方晴好适合出行，有的地方可能下雨或有风，不适合徒步。所以我需要先确认：\n\n> **你打算去哪个城市或哪座山徒步？** 比如深圳的塘朗山、北京的香山、杭州的十里琅珰，或者你所在的城市某条路线都可以。\n\n等你说出目的地，我就能帮你查天气、并结合户外安全知识给出针对性建议 🌤️⛰️"
    }
  ]
}
````

## File: ai-service/memory_data/chat-f5ff9a77-3929-4353-8e80-742e1c6946af.json
````json
{
  "chat_id": "chat-f5ff9a77-3929-4353-8e80-742e1c6946af",
  "messages": [
    {
      "role": "user",
      "content": "保存 文件测试"
    }
  ]
}
````

## File: ai-service/memory_data/live-gateway-location-weather-check-dummy-2.json
````json
{
  "chat_id": "live-gateway-location-weather-check-dummy-2",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/live-gateway-location-weather-check-dummy-3.json
````json
{
  "chat_id": "live-gateway-location-weather-check-dummy-3",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/live-gateway-location-weather-check-dummy.json
````json
{
  "chat_id": "live-gateway-location-weather-check-dummy",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/live-location-weather-check-dummy-new.json
````json
{
  "chat_id": "live-location-weather-check-dummy-new",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/live-location-weather-check-dummy.json
````json
{
  "chat_id": "live-location-weather-check-dummy",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/live-location-weather-check.json
````json
{
  "chat_id": "live-location-weather-check",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/manual-missing-key-test.json
````json
{
  "chat_id": "manual-missing-key-test",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/missing-key-sse.json
````json
{
  "chat_id": "missing-key-sse",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: ai-service/memory_data/runtime-config-live-check.json
````json
{
  "chat_id": "runtime-config-live-check",
  "messages": [
    {
      "role": "user",
      "content": "ping"
    }
  ]
}
````

## File: ai-service/memory_data/runtime-config-missing.json
````json
{
  "chat_id": "runtime-config-missing",
  "messages": [
    {
      "role": "user",
      "content": "ping"
    }
  ]
}
````

## File: ai-service/memory_data/runtime-config-present.json
````json
{
  "chat_id": "runtime-config-present",
  "messages": [
    {
      "role": "user",
      "content": "ping"
    }
  ]
}
````

## File: ai-service/memory_data/runtime-llm-sse.json
````json
{
  "chat_id": "runtime-llm-sse",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    }
  ]
}
````

## File: ai-service/memory_data/test-1.json
````json
{
  "chat_id": "test-1",
  "messages": [
    {
      "role": "user",
      "content": "hi"
    }
  ]
}
````

## File: ai-service/memory_data/test-2.json
````json
{
  "chat_id": "test-2",
  "messages": [
    {
      "role": "user",
      "content": "hi"
    }
  ]
}
````

## File: ai-service/memory_data/test-chat-disabled.json
````json
{
  "chat_id": "test-chat-disabled",
  "messages": [
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    }
  ]
}
````

## File: ai-service/memory_data/test-chat-error.json
````json
{
  "chat_id": "test-chat-error",
  "messages": [
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    }
  ]
}
````

## File: ai-service/memory_data/test-chat-sse-123.json
````json
{
  "chat_id": "test-chat-sse-123",
  "messages": [
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    }
  ]
}
````

## File: ai-service/memory_data/test-chat-sync-123.json
````json
{
  "chat_id": "test-chat-sync-123",
  "messages": [
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    }
  ]
}
````

## File: ai-service/memory_data/verify-chat.json
````json
{
  "chat_id": "verify-chat",
  "messages": [
    {
      "role": "user",
      "content": "保存 文件测试"
    }
  ]
}
````

## File: ai-service/memory/__init__.py
````python
__all__ = [
````

## File: ai-service/memory/base.py
````python
class ChatMemory(ABC)
⋮----
@abstractmethod
    def add_message(self, role: str, content: str)
⋮----
@abstractmethod
    def get_messages(self) -> list[dict]
⋮----
@abstractmethod
    def clear(self)
````

## File: ai-service/memory/committer.py
````python
@dataclass
class MemoryCandidate
⋮----
type: str
subject: str
predicate: str
object: str
confidence: float = 0.8
⋮----
def to_item(self) -> dict[str, Any]
⋮----
class MemoryCommitter
⋮----
text = "\n".join(
⋮----
text = f"{text}\n{query}"
⋮----
candidates: list[MemoryCandidate] = []
⋮----
deduped: dict[tuple[str, str, str], MemoryCandidate] = {}
⋮----
key = (item.type, item.predicate, item.object)
current = deduped.get(key)
⋮----
def _profile_candidates(self, text: str) -> list[MemoryCandidate]
⋮----
origin = re.search(r"我(?:一般|通常|平时)?从([\u4e00-\u9fffA-Za-z0-9·\-]{2,12})出发", text)
⋮----
def _trip_candidates(self, task_state: dict) -> list[MemoryCandidate]
⋮----
slots = task_state.get("slots") or {}
⋮----
slots = slots.to_dict()
⋮----
stable = {
````

## File: ai-service/memory/compressor.py
````python
logger = logging.getLogger("ai-service.memory.compressor")
⋮----
class SessionCompressor
⋮----
def compress(self, history: list[dict]) -> str
⋮----
dialogue = [m for m in history if m.get("role") in ("user", "assistant")]
⋮----
def _compress_with_llm(self, dialogue: list[dict]) -> str
⋮----
conversation_text = "\n".join(
⋮----
prompt = (
⋮----
messages = [
result = self.llm.invoke(messages)
content = result.content.strip() if result.content else ""
⋮----
@staticmethod
    def _compress_fallback(dialogue: list[dict]) -> str
⋮----
"""Fallback: simple truncation-based summary when LLM is unavailable."""
⋮----
first_user = next((m["content"] for m in dialogue if m["role"] == "user"), "")
last_exchange = dialogue[-3:]
⋮----
summary_parts = []
⋮----
exchange_text = "; ".join(
````

## File: ai-service/memory/file_memory.py
````python
MEMORY_DIR = Path("./memory_data")
⋮----
WINDOW_SIZE = 60
⋮----
class FileChatMemory(ChatMemory)
⋮----
def __init__(self, chat_id: str = "default", save_dir: str | None = None)
⋮----
base_dir = Path(save_dir)
⋮----
def _load(self)
⋮----
data = json.loads(self.file_path.read_text("utf-8"))
⋮----
def _save(self)
⋮----
data = self._messages if self._list_format else {"chat_id": self.chat_id, "messages": self._messages}
⋮----
def add_message(self, role: str, content: str)
⋮----
def get_messages(self) -> list[dict]
⋮----
def clear(self)
````

## File: ai-service/memory/knowledge.py
````python
logger = logging.getLogger("ai-service.memory.knowledge")
⋮----
class KnowledgeExtractor
⋮----
def extract(self, text: str) -> list[dict]
⋮----
def _extract_with_llm(self, text: str) -> list[dict]
⋮----
prompt = (
⋮----
messages = [
result = self.llm.invoke(messages)
content = result.content.strip() if result.content else ""
⋮----
@staticmethod
    def _parse_result(content: str) -> list[dict]
⋮----
"""Parse LLM output into knowledge item list."""
⋮----
# Try to extract JSON array from response (handles markdown-wrapped JSON)
json_match = re.search(r"(\[.*?\])", content, re.DOTALL)
raw = json_match.group(1) if json_match else content
⋮----
items = json.loads(raw)
⋮----
# Validate and normalize
validated = []
````

## File: ai-service/memory/memory_manager.py
````python
logger = logging.getLogger("ai-service.memory")
⋮----
class MemoryConfig
⋮----
compressor_model: str = "gpt-4o-mini"
extractor_model: str = "gpt-4o-mini"
llm_base_url: str = ""
llm_api_key: str = ""
vector_store_path: str = "./memory_store"
top_k: int = 5
⋮----
class MemoryManager
⋮----
def __init__(self, config: Optional[MemoryConfig] = None)
⋮----
def get_session_context(self, history: list[dict]) -> str
⋮----
def get_relevant_knowledge(self, query: str) -> list[dict]
⋮----
def update_knowledge(self, history: list[dict]) -> int
⋮----
recent = []
⋮----
conversation_text = "\n".join(reversed(recent))
items = self.extractor.extract(conversation_text)
⋮----
def format_knowledge_context(self, query: str) -> str
⋮----
knowledge = self.get_relevant_knowledge(query)
⋮----
lines = []
⋮----
subj = item.get("subject", "")
pred = item.get("predicate", "")
obj = item.get("object", "")
⋮----
def process_interaction(self, history: list[dict], query: str) -> dict
⋮----
def build_runtime_context(self, history: list[dict], query: str) -> dict
⋮----
"""Commit stable profile/trip memories after final response generation."""
candidates = self.committer.extract_candidates(
````

## File: ai-service/memory/redis_memory.py
````python
logger = logging.getLogger("ai-service.memory")
WINDOW_SIZE = 20
⋮----
REDIS_AVAILABLE = True
⋮----
REDIS_AVAILABLE = False
⋮----
class RedisChatMemory(ChatMemory)
⋮----
def __init__(self, chat_id: str = "default")
⋮----
async def _ensure_client(self)
⋮----
def add_message(self, role: str, content: str)
⋮----
async def _add_message_async(self, role: str, content: str)
⋮----
client = await self._ensure_client()
msg = json.dumps({"role": role, "content": content}, ensure_ascii=False)
⋮----
def get_messages(self) -> list[dict]
⋮----
async def _get_messages_async(self) -> list[dict]
⋮----
raw_messages = await client.lrange(self.redis_key, 0, -1)
messages = []
⋮----
def clear(self)
⋮----
async def _clear_async(self)
````

## File: ai-service/memory/vector_store.py
````python
logger = logging.getLogger("ai-service.memory.vector_store")
⋮----
FAISS_AVAILABLE = False
⋮----
FAISS_AVAILABLE = True
⋮----
class VectorStore
⋮----
def __init__(self, store_path: str = "./memory_store")
⋮----
def add(self, items: list[dict]) -> None
⋮----
texts = [
⋮----
embeddings = self.embeddings.embed_documents(texts)
⋮----
def search(self, query: str, k: int = 5) -> list[dict]
⋮----
query_embedding = self.embeddings.embed_query(query)
⋮----
def _search_in_memory(self, query_embedding: list[float], k: int) -> list[dict]
⋮----
query_vec = np.array(query_embedding).reshape(1, -1)
⋮----
doc_array = np.array(self._embeddings)
similarities = np.dot(doc_array, query_vec.T).flatten() / (
top_indices = np.argsort(similarities)[-k:][::-1]
⋮----
def _save(self) -> None
⋮----
data = {"items": self._items, "embeddings": self._embeddings}
⋮----
def _load(self) -> None
⋮----
pkl_path = self.store_path / "knowledge.pkl"
⋮----
data = pickle.load(f)
⋮----
def clear(self) -> None
⋮----
@property
    def count(self) -> int
````

## File: ai-service/rag_docs/户外徒步知识文档.md
````markdown
# 户外徒步知识全指南

户外徒步作为一种融合了自然探索、体能锻炼与心灵放松的活动，近年来受到越来越多人的喜爱。它不仅是对个人意志与体能的考验，更是一次与自然深度对话的机会。然而，徒步并非简单的“走路”，其背后涉及系统的知识体系与严谨的安全准备。本文旨在为徒步爱好者提供一份全面、科学且实用的知识指南，内容涵盖徒步的基础认知、装备配置、路线规划、安全防范、体能训练及环保责任，帮助参与者建立理性、安全、可持续的户外理念。

## 一、什么是徒步？——从散步到系统的户外运动

徒步（Hiking）是指在自然环境中进行的中长距离步行活动，通常单程距离不少于5公里，区别于城市中的日常散步或短途健走。其核心目的在于通过持续性的行进过程，亲近自然、挑战自我、提升身心素质，并在过程中培养对环境的敬畏与责任感<sup>[1]</sup>。

### 徒步的核心目的
徒步的价值不仅体现在身体层面的锻炼，如增强心肺功能、提高耐力与协调性，更在于心理层面的成长。研究表明，规律参与百日徒步计划的人群，其焦虑指数平均下降42%，决策失误率减少29%，印证了徒步对现代人精神压力的有效缓解作用<sup>[1]</sup>。

### 主要类型分类
根据强度、形式和场景的不同，徒步可划分为多种类型：

- **按强度分级**：
  - 休闲级：适合初学者，里程≤10km，累计爬升≤500m；
  - 进阶级：具备一定基础者，需应对复杂地形；
  - 挑战级：高海拔、长距离、大爬升线路；
  - 大师级：仅限资深爱好者，常涉及极端气候与无人区穿越。

- **按组织形式**：
  - 轻装日穿：当日往返，不携带露营装备；
  - 重装露营：多日行程，背负帐篷、睡袋等物资；
  - 商业组织：由专业机构带队，提供交通、食宿服务；
  - 自主SOLO：独立完成路线规划与执行，要求极高的综合能力。

- **特殊场景徒步**：
  - 沙漠穿越：面临高温、缺水、风沙等挑战；
  - 雪地徒步：需掌握防滑、保暖与雪崩识别技能；
  - 峡谷探秘：注意落石、湿滑岩壁与突发山洪风险。

![三层穿衣法结构示意图](https://agent.qianwen.com/mos/f8b7fdecce384cfc97cc3228a78bb361/1df099caefe281976dfaa5715179d1af)

## 二、徒步装备系统详解

科学合理的装备配置是保障徒步安全与舒适的关键。一套完整的徒步装备应遵循功能性、轻量化与冗余备份三大原则，确保在各种环境下均能有效应对。

### （一）三层穿衣法：应对多变气候的核心原则

人体在运动过程中会产生大量汗液，若衣物无法及时排湿，将导致体温调节失衡，增加失温风险。因此，“三层穿衣法”成为国际通行的户外着装标准，其结构如下表所示：

| 层级 | 功能 | 推荐材质 | 使用场景 |
|------|------|----------|--------|
| 内层（排汗层） | 吸湿速干 | 美利奴羊毛、聚酯纤维 | 所有季节 |
| 中层（保暖层） | 温度调节 | 抓绒衣、羽绒服、合成棉服 | 春秋冬季、高海拔 |
| 外层（防护层） | 防风防水 | 冲锋衣裤、软壳衣 | 雨天、强风、低温 |

> **提示**：严禁穿着纯棉衣物进入山区，因其吸水后难以干燥，极易引发失温事故。

### （二）徒步鞋的选择与磨合

徒步鞋是徒步活动中最重要的装备之一，直接影响行走稳定性与足部健康。

- **关键指标**：
  - **防水性**：推荐选用GORE-TEX或FLT防水内衬技术产品，保持脚部干爽；
  - **抓地力**：Vibram大底具有优异的耐磨性与湿滑路面附着力；
  - **支撑性**：中高帮设计可有效保护脚踝，防止扭伤，尤其适用于崎岖地形。

- **尺码建议**：由于长时间行走会导致脚部轻微肿胀，建议选择比日常鞋码大0.5–1码的型号。

- **新鞋磨合**：禁止穿着全新徒步鞋进行长途徒步。出发前应在城市道路或低强度山径上累计行走不少于30公里，以适应鞋型并排除潜在磨脚点。

- **常见品牌推荐**：LOWA、Salomon、SCARPA、凯乐石（KAILAS）、探路者（TOREAD）等均为市场认可度较高的专业品牌。

### （三）背包配置与背负系统

背包不仅是装载工具，更是影响体力分配与背部健康的决定性因素。

- **容量匹配原则**：
  - 单日徒步：20–30L，满足基本补给与应急物品存放；
  - 两日露营：30–50L，容纳睡袋、帐篷等露营装备；
  - 多日重装：50L以上，适合远距离穿越任务。

- **背负系统要点**：
  - 腰带承担约70%的重量，必须紧贴髋骨上方；
  - 肩带调节至锁骨下方，避免压迫肩颈神经；
  - 试背时检查“45度法则”：双手前伸呈90度，双臂自然下垂后应能轻松触及背包两侧提手。

- **推荐品牌**：Osprey、Gregory、始祖鸟（Arc'teryx）、Deuter等品牌以其优秀的背负系统与耐用性著称。

### （四）其他必备装备清单

除服装与背包外，以下装备亦属徒步出行的基本配置：

- **登山杖**：减轻膝盖压力可达30%，长度建议为身高×0.66；
- **头灯+备用电池**：用于夜间行进或突发状况照明，确保续航时间超过预计行程；
- **导航工具**：手机APP（如“两步路”“奥维地图”）配合纸质地图与指南针使用，形成双重保障；
- **急救包**：包含碘伏、创可贴、绷带、止血带、抗过敏药及个人常用药品；
- **应急物品**：保温毯、救生哨、多功能刀具、垃圾袋、备用口罩与驱蚊液。

此外，建议携带不少于2升饮用水，并根据气温与行程适当增加；食物方面宜选择高能量、易消化的食品，如能量棒、坚果、八宝粥与盐丸。

## 三、路线规划与难度评估

一条科学合理的徒步路线不仅能带来良好的体验，更能最大限度规避潜在风险。路线规划需结合个人能力、天气条件与地理特征进行综合判断。

### （一）如何科学评估一条徒步路线？

中国登山协会推荐采用以下参数作为路线难度评估依据：

- 总里程
- 累计爬升
- 最高海拔
- 预估耗时

其中，预估耗时可通过以下公式计算：

> 总时间 = (距离 ÷ 3.2) + (爬升 ÷ 305) + 每小时休息5分钟

该公式综合考虑平地行进速度（约3.2km/h）与垂直爬升消耗（每305米加1小时），已被广泛应用于国内徒步圈的实际操作中。

### （二）路线筛选原则

对于初次接触徒步的新手，建议遵循“三六六原则”：

- 至少准备 **3升水**；
- 初次徒步不宜超过 **6公里** 或 **600米海拔差**；
- 行程控制在 **6小时内**。

同时，应优先选择成熟步道，避免进入未开发区域。可通过“两步路”“六只脚”等APP下载离线轨迹，并查看近期他人实际轨迹以确认路况是否通行。此外，务必选择设有下撤点的线路，避免陷入“只能进不能退”的困境。

### （三）热门推荐路线（按难度分级）

| 地点 | 路线名称 | 里程 | 爬升 | 难度 | 特色 |
|------|----------|------|------|------|------|
| 成都邛崃 | 休闲级步道 | 5–8km | <200m | 休闲级 | 全龄友好，路面平坦 |
| 西安 | 蓝关古道环穿 | 12km | ~800m | 初级 | 春季赏景佳选 |
| 云南丽江 | 虎跳峡高路 | 2–3天 | —— | 初级 | 金沙江峡谷壮丽景观 |
| 四川四姑娘山 | 长穿毕 | 3–4天 | —— | 中等 | 幺妹峰日照金山 |

> 注：部分路线信息参考自《徒步百科》及地方文旅部门发布的官方导览资料<sup>[1]</sup>。

## 四、安全须知与风险应对

安全是徒步活动不可逾越的底线。任何忽视风险的行为都可能造成严重后果，甚至危及生命。因此，必须建立系统的风险防控意识。

### （一）行前准备三大原则

1. **心理准备**：树立对自然的敬畏之心，杜绝侥幸心理与“打卡式”心态；
2. **团队管理**：建议4人以上结伴出行，实现“一人遇险，两人求助，一人陪护”的国际通用救援模式；
3. **行程报备**：将详细路线、进出山口位置、预计返回时间告知至少一名亲友，并约定联络机制。

### （二）极端天气应对策略

| 天气 | 风险 | 应对措施 |
|------|------|----------|
| 暴雨 | 山洪、滑坠、失温 | 远离河道，避入岩洞，更换干衣 |
| 雷电 | 雷击高危 | 下撤至低处，双脚并拢蹲姿，禁用电子设备 |
| 浓雾 | 迷路 | 使用GPS+纸质地图，原地等待或原路返回 |
| 暴雪 | 失温、地形覆盖 | 转移至背风区，更换干燥衣物，立即下撤 |

> 特别提醒：收到暴雨橙色及以上预警时，应直接取消行程；雷暴发生时，切勿停留在山顶、山脊或孤立树下。

### （三）常见伤病处理

#### 失温分级与应对

| 分级 | 体温 | 症状 | 处理方式 |
|------|------|------|----------|
| 轻度 | 33–35℃ | 寒战、言语不清 | 停止运动，换干衣，喝温糖水 |
| 重度 | <32℃ | 意识模糊、昏迷 | 严禁烤火，用睡袋包裹送医 |

> **重要警示**：重度失温患者严禁直接加热或饮用热水，否则可能导致心脏骤停。

#### 迷路应对流程

一旦发现偏离路线，应立即执行STOP原则：

- **S**（Stop）：停止前进，保持冷静；
- **T**（Think）：回忆最后已知位置；
- **O**（Observe）：观察周围地形与标志物；
- **P**（Plan）：制定下一步行动计划。

随后可通过“徒步0769”小程序获取精确坐标，并拨打110或120求助，清晰描述所处环境（如“溪流东侧巨石旁”）以便救援定位。

#### 动物伤害处置

- **蛇咬伤**：不切开、不吸毒、不解毒；固定伤肢，冲洗伤口，尽快就医；
- **蜂蜇伤**：拔除毒刺，冰敷，观察过敏反应；
- **蜱虫叮咬**：镊子垂直拔出，消毒后观察发热情况。

> 注意：抗蛇毒血清是唯一特效治疗手段，注射时间越早，存活率越高。

## 五、体能与心理准备

良好的体能储备是顺利完成徒步的基础，而稳定的心理状态则决定了面对困难时的决策质量。

### （一）基础体能训练建议

- 每周进行3–4次慢跑，每次20–30分钟，提升心肺耐力；
- 利用楼梯间进行爬楼训练，模拟山地爬升负荷；
- 加强核心肌群锻炼，如平板支撑、卷腹等动作，增强身体稳定性；
- 出发前一周进行一次模拟负重行走测试，检验装备适配性与体力储备。

### （二）心理建设要点

- 认知自身极限，学会“放弃”也是一种智慧；
- 遇恶劣天气、身体不适时果断终止行程；
- 杜绝“来都来了”心态，安全永远第一位；
- 不盲目挑战“网红野路线”，尊重管理部门划定的禁区。

> 根据《山地户外运动水平等级标准》，年满16周岁的参与者可根据培训经历与运动实践申请相应等级认证，四级及以上需参加中国登山协会授权赛事不少于六次，体现了“能力与路线匹配”的科学理念。

## 六、环保责任：践行LNT无痕山林原则

徒步不仅是个人的旅程，更是一种生态行为。每一位徒步者都应自觉承担起环境保护的责任，践行“无痕山林”（Leave No Trace, LNT）原则。

### LNT七大原则

1. **提前计划与准备**
2. **在可承受地面行进与露营**
3. **妥善处理废弃物**（带走所有垃圾）
4. **保持自然原貌**（不采摘植物、不刻画岩石）
5. **最小化野外用火影响**
6. **尊重野生动植物**（不投喂、不惊扰）
7. **尊重其他使用者**

> **特别提醒**：果皮降解需1年以上，亦会对野生动物造成误食风险，必须打包带走。

在实际操作中，可采取以下具体措施：
- 使用密封袋分类存放厨余与生活垃圾；
- 如厕时挖掘15厘米深的猫洞，事后回填并标记；
- 用矿泉水瓶收集细碎垃圾，防止渗漏；
- 优先使用便携炉具而非明火烹饪。

## 结语：让每一次出发都更安心

徒步不仅是脚步的丈量，更是心智的成长。唯有建立科学认知、做好充分准备、坚守环保底线，才能真正享受山野之美。愿每位徒步者都能平安归来，也为后来者留下一片纯净天地。正如《徒步百科》所倡导：“真正的探险，不是征服自然，而是学会与之共存。”<sup>[1]</sup>

[1]:http://www.zxhsd.com/kgsm/ts/2025/11/04/6716410.shtml "徒步百科：徒步帮|责编:许姗//汪昊宇 : 生活娱乐 :生活用书 :保健养生 :浙江新华书店网群"
[2]:https://m.dzplus.dzng.com/share/general/0/NEWS2874270EFMGUZPGTKPDI "序跋丨《徒步百科》推荐序_大众新闻_大众新媒体大平台"
[3]:https://www.douban.com/doubanapp/dispatch?uri=/review/17184809 "让我从户外菜鸟秒变安全达人（徒步百科）书评"
[4]:https://mall.96192.com/product/detail/1212472 "徒步中国"
[5]:https://book.douban.com/subject/37536789/ "徒步百科 (豆瓣)"
[6]:https://page.sm.cn/blm/midpage-317/index?h=iknow.v4_2.quark.cn&id=28_21800965cc7ad878aa74d45c348d9126 "户外徒步0基础入门，这份攻略请收好"
[7]:https://sz.people.com.cn/n2/2026/0107/c202846-41465718.html "“深圳远足径”导览上线"
[8]:https://www.toutiao.com/a7592038982356173364/ "深圳远足径导览上线啦！快来看看如何开启山海之旅 - 今日头条"
[9]:https://yjt.hubei.gov.cn/yjkp/yjkp/202603/t20260331_5903087.shtml "户外登山，安全为先-湖北省应急管理厅"
[10]:https://www.douyin.com/video/7633676080179711270 "户外徒步装备分享 #徒步 #大学生 #装备分享"
[11]:http://sd.cma.gov.cn/xwzx_3497/qxkp/202601/t20260109_7535458.html "山东省气象局-- 高山有界 越己知止——高山徒步切守安全与生态双底线"
````

## File: ai-service/rag/__init__.py
````python

````

## File: ai-service/rag/augmenter.py
````python
logger = logging.getLogger("ai-service.rag.augmenter")
⋮----
_RAG_SYSTEM = """你是 AI Hiking 的中文知识助手。请按下面风格回答：
⋮----
_RAG_HUMAN = """---
⋮----
_NO_DOCS_MSG = "我没在知识库里找到和「{question}」直接相关的文档。\n\n可以换个更具体的关键词，或先上传/同步相关资料后再查。"
⋮----
_META_PHRASE_RE = re.compile(
_META_SENTENCE_RE = re.compile(
_SENTENCE_RE = re.compile(r"[^。！？!?]+[。！？!?]?")
⋮----
_CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
_LATIN_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,}")
_CJK_STOP_CHARS = set("的是了在和与及或并就都而很也还把被让对中为到从个吗呢啊")
_STOP_TERMS = {
_QUERY_EXPANSIONS = {
_GENERIC_QUERY_TERMS = {"徒步", "户外", "指南", "相关", "内容", "信息"}
⋮----
def _build_context(docs: list[Document]) -> str
⋮----
"""Format documents into context string."""
parts = []
⋮----
metadata = doc.metadata or {}
source = metadata.get("title") or metadata.get("file_name") or metadata.get("source", "未知来源")
⋮----
def _clip_display_snippet(text: str, question: str, limit: int) -> str
⋮----
terms = sorted(_terms_from_text(question), key=len, reverse=True)
hit = -1
⋮----
hit = text.find(term)
⋮----
start = max(0, hit - limit // 3)
end = min(len(text), start + limit)
⋮----
start = max(0, end - limit)
⋮----
prefix = "..." if start > 0 else ""
suffix = "..." if end < len(text) else ""
⋮----
def _build_display_context(docs: list[Document], question: str, max_docs: int = 2, limit: int = 220) -> str
⋮----
snippet = clean_display_text(doc.page_content)
snippet = _clip_display_snippet(snippet, question, limit)
⋮----
def _question_focus_terms(question: str) -> set[str]
⋮----
terms = {term for term in _terms_from_text(question) if term not in _GENERIC_QUERY_TERMS and len(term) >= 2}
⋮----
def _build_display_snippets(docs: list[Document], question: str, max_docs: int = 3, limit: int = 180) -> list[str]
⋮----
candidates: list[tuple[int, str]] = []
fallback: list[str] = []
seen: set[str] = set()
focus_terms = _question_focus_terms(question)
⋮----
score = sum(1 for term in focus_terms if term and term in snippet)
⋮----
def _strip_answer_meta(text: str) -> str
⋮----
text = _META_SENTENCE_RE.sub("", text)
text = _META_PHRASE_RE.sub("", text)
text = re.sub(r"^(?:所以|因此|综上)[，,:：]?", "", text.strip())
⋮----
def _split_answer_sentences(text: str) -> list[str]
⋮----
sentences = [m.group(0).strip() for m in _SENTENCE_RE.finditer(text) if m.group(0).strip()]
⋮----
def _has_numbered_lines(text: str) -> bool
⋮----
lines = [line.strip() for line in text.splitlines() if line.strip()]
⋮----
def _format_answer_text(text: str) -> str
⋮----
cleaned = clean_display_text(text, preserve_lines=True, keep_list_markers=True)
cleaned = _strip_answer_meta(cleaned)
⋮----
normalized = " ".join(cleaned.split())
sentences = _split_answer_sentences(normalized)
⋮----
def _fallback_answer(question: str, docs: list[Document]) -> str
⋮----
snippets = _build_display_snippets(docs, question)
⋮----
question_text = clean_display_text(question)
facts: list[str] = []
⋮----
sentences = _split_answer_sentences(snippet)
start = 0
⋮----
start = idx
⋮----
sentence = sentence.strip()
⋮----
sentence = sentence[len(question_text):].strip(" ，,:：")
⋮----
facts = snippets
⋮----
def _terms_from_text(text: str) -> set[str]
⋮----
"""Extract lightweight search terms without adding a tokenizer dependency."""
lowered = text.lower()
terms = {m.group(0) for m in _LATIN_RE.finditer(lowered) if m.group(0) not in _STOP_TERMS}
⋮----
cjk_chars_added = False
⋮----
seq = match.group(0)
⋮----
term = seq[idx:idx + n]
⋮----
cjk_chars_added = True
⋮----
def _expand_query_terms(terms: set[str]) -> set[str]
⋮----
expanded = set(terms)
⋮----
def _document_search_text(doc: Document) -> str
⋮----
meta_text = " ".join(
⋮----
def has_relevant_evidence(question: str, docs: list[Document]) -> bool
⋮----
"""Return True when retrieved docs have direct lexical evidence for the question."""
⋮----
question_terms = _expand_query_terms(_terms_from_text(question))
⋮----
doc_terms = _terms_from_text(_document_search_text(doc))
⋮----
class ContextAugmenter
⋮----
"""Augments user questions with retrieved context using LangChain ChatPromptTemplate."""
⋮----
def augment(self, question: str, docs: list[Document]) -> str
⋮----
context = _build_context(docs)
⋮----
messages = self._prompt.format_messages(context=context, question=question)
response = self.llm.invoke(messages)
content = response.content if hasattr(response, "content") else str(response)
⋮----
fallback = _fallback_answer(question, docs)
⋮----
async def augment_stream(self, question: str, docs: list[Document]) -> AsyncIterator[str]
⋮----
"""Stream augmented response token by token."""
⋮----
chunks: list[str] = []
⋮----
answer = _format_answer_text("".join(chunks))
⋮----
def inject_knowledge(self, question: str, knowledge_items: list[dict[str, Any]]) -> str
⋮----
"""Build a prompt enriched with extracted knowledge items from the memory system."""
⋮----
parts: list[str] = []
⋮----
kind = item.get("type", "常识")
confidence = item.get("confidence", 0.0)
prefix = f"  (置信度: {confidence:.0%})" if confidence > 0 else ""
⋮----
knowledge_block = "\n\n".join(parts)
````

## File: ai-service/rag/feishu.py
````python
_LARK_CLI_PATH = shutil.which("lark-cli") or "lark-cli"
⋮----
logger = logging.getLogger("ai-service.rag.feishu")
⋮----
DOC_TOKEN_RE = re.compile(r"/(docx?|bitable|base|sheets?|slides|mindnote)/([A-Za-z0-9_-]{12,})")
WIKI_NODE_RE = re.compile(r"/wiki/([A-Za-z0-9_-]{12,})")
WIKI_SPACE_RE = re.compile(r"(?:/wiki/(?:space|spaces)/|[?&]space_id=)([A-Za-z0-9_-]{6,})")
FEISHU_URL_RE = re.compile(r"https?://[^\s<>'\"]*feishu\.cn/[^\s<>'\"]+")
SUPPORTED_FETCH_TYPES = {"doc", "docx", "file"}
_DOWNLOADABLE_TYPES = {"file", "md", "txt", "csv", "markdown"}
⋮----
_LARK_CLI_TIMEOUT = 30
⋮----
@dataclass(frozen=True)
class FeishuLinkInfo
⋮----
raw: str
kind: str
token: str
doc_type: str = "docx"
⋮----
def _run_lark_cli(args: list[str]) -> dict
⋮----
cmd = [_LARK_CLI_PATH] + args + ["--format", "json"]
⋮----
result = subprocess.run(
⋮----
stderr = result.stderr.strip() or "unknown error"
⋮----
data = json.loads(result.stdout)
⋮----
raw_error = data.get("error")
⋮----
error_msg = raw_error.get("message") or raw_error.get("type") or "unknown"
⋮----
error_msg = f"{error_msg}；{raw_error['hint']}"
⋮----
error_msg = data.get("msg", raw_error or "unknown")
⋮----
"""Call Feishu OpenAPI through lark-cli's generic api command."""
args = ["api", method.upper(), path]
⋮----
def _html_to_text(html: str) -> str
⋮----
soup = BeautifulSoup(html, "lxml")
⋮----
def _normalize_doc_type(doc_type: str) -> str
⋮----
normalized = doc_type.lower()
⋮----
def find_feishu_links(text: str) -> list[FeishuLinkInfo]
⋮----
links: list[FeishuLinkInfo] = []
⋮----
def inspect_feishu_link(url_or_token: str) -> FeishuLinkInfo
⋮----
value = url_or_token.strip()
⋮----
doc_match = DOC_TOKEN_RE.search(value)
⋮----
wiki_match = WIKI_NODE_RE.search(value)
⋮----
space_match = WIKI_SPACE_RE.search(value)
⋮----
def extract_doc_token(url_or_token: str) -> str
⋮----
def resolve_wiki_node(node_token: str, obj_type: str = "wiki") -> dict
⋮----
params = {"token": node_token}
⋮----
data = call_lark_api(
node = data.get("data", {}).get("node", {})
⋮----
"""List Wiki nodes in a space or under a parent node."""
params = {
⋮----
inner = data.get("data", {})
⋮----
def walk_wiki_nodes(space_id: str, max_pages: int = 200) -> list[dict]
⋮----
"""Walk a Wiki space tree breadth-first and return all visible nodes."""
nodes: list[dict] = []
queue: list[str] = [""]
pages = 0
⋮----
parent = queue.pop(0)
page_token = ""
⋮----
page = list_wiki_nodes(
⋮----
page_token = page["page_token"]
⋮----
class FeishuDocLoader
⋮----
"""飞书文档加载器：通过 lark-cli 抓取文档内容 → 分块 → 返回 LangChain Document 列表。
    用法:
        loader = FeishuDocLoader()
        docs = loader.load_and_split("AbCdEf1234567890abcdef", title="需求文档")
        retriever.add_documents(docs, status="feishu")
    """
⋮----
def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200)
⋮----
def download_file(self, file_token: str) -> dict
⋮----
"""通过 drive API 下载 file 类型文档。
        Args:
            file_token: 飞书文件 token。
        Returns:
            {"markdown": str, "title": str, "doc_id": str}
        """
⋮----
saved_path = data.get("saved_path", "")
content_type = data.get("content_type", "")
⋮----
text = ""
⋮----
text = f.read()
⋮----
title = ""
⋮----
title = Path(saved_path).stem
⋮----
def fetch_content(self, doc_token: str, doc_type: str = "docx") -> dict
⋮----
"""通过 lark-cli API 获取文档内容。
        对于 file 类型文档，使用 drive download 下载；
        对于 doc/docx 类型文档，使用 docs_ai fetch 抓取。
        Args:
            doc_token: 飞书文档 token。
            doc_type: 文档类型。
        Returns:
            {"markdown": str, "title": str, "doc_id": str}
        """
⋮----
body = {
⋮----
document = inner.get("document", inner)
⋮----
html_content = (
doc_id = document.get("document_id") or inner.get("document_id") or doc_token
⋮----
title = document.get("title") or inner.get("title") or ""
title_match = re.search(r"<title>(.*?)</title>", html_content)
⋮----
title = title_match.group(1)
⋮----
text = _html_to_text(html_content)
⋮----
def _resolve_document_ref(self, doc_ref: str, doc_type: str = "docx") -> tuple[str, str, dict]
⋮----
"""Resolve a document URL/token into fetchable doc token, type, and metadata."""
link = inspect_feishu_link(doc_ref)
metadata: dict = {}
⋮----
node = resolve_wiki_node(link.token)
obj_type = _normalize_doc_type(node.get("obj_type", "docx"))
⋮----
resolved_type = _normalize_doc_type(doc_type or link.doc_type)
⋮----
resolved_type = link.doc_type
⋮----
"""抓取并拆分飞书文档为 LangChain Document 列表。
        Args:
            doc_token: 飞书文档 token。
            title: 文档标题，默认使用飞书 API 返回的标题。
            doc_type: 文档类型，写入 metadata 备用。
        Returns:
            拆分后的 Document 列表。
        """
⋮----
fetched = self.fetch_content(resolved_token, doc_type=resolved_type)
content = fetched["markdown"]
doc_title = title or extra_metadata.get("title") or fetched["title"] or resolved_token
⋮----
docs = self.splitter.create_documents([content])
⋮----
"""搜索飞书空间中的文档。
    Args:
        query: 搜索关键词，空字符串表示浏览全部。
        space_id: 知识库空间 ID（与 folder_token 互斥）。
        folder_token: 文件夹 token（与 space_id 互斥）。
        page_size: 每页数量（1-20）。
        page_token: 翻页 token。
    Returns:
        {"results": [...], "has_more": bool, "page_token": str, "total": int}
    """
args = ["drive", "+search", "--page-size", str(page_size)]
⋮----
data = _run_lark_cli(args)
⋮----
class FeishuDefaultSyncer
⋮----
"""飞书默认文档同步器：从配置的空间/文件夹批量拉取文档并同步到向量存储。
    用法:
        syncer = FeishuDefaultSyncer(loader, retriever)
        result = syncer.sync_from_space("space_id_xxx")
        # 或
        result = syncer.sync_from_folder("folder_token_xxx")
    """
⋮----
def __init__(self, loader: FeishuDocLoader, retriever)
⋮----
def sync_from_space(self, space_id: str) -> list[dict]
⋮----
"""从知识库空间同步所有文档。
        Args:
            space_id: 知识库空间 ID。
        Returns:
            已同步的文档摘要列表。
        """
⋮----
def sync_from_folder(self, folder_token: str) -> list[dict]
⋮----
"""从文件夹同步所有文档。
        Args:
            folder_token: 文件夹 token。
        Returns:
            已同步的文档摘要列表。
        """
⋮----
"""遍历所有页面并逐文档同步。"""
⋮----
synced: list[dict] = []
⋮----
page = 0
⋮----
result = search_feishu_docs(
⋮----
meta = item.get("result_meta", {})
doc_token = meta.get("token", "")
doc_type = meta.get("doc_types", "docx").lower()
doc_title = meta.get("title_highlighted", "")
⋮----
icon_info_str = meta.get("icon_info", "")
⋮----
icon_info = json.loads(icon_info_str)
file_token = icon_info.get("token", "")
⋮----
doc_token = file_token
⋮----
docs = self.loader.load_and_split(
⋮----
time.sleep(0.3)  # 请求间隔，避免触发频率限制
⋮----
page_token = result["page_token"]
⋮----
def _sync_wiki_space(self, space_id: str) -> list[dict]
⋮----
"""Traverse a Wiki knowledge base and sync supported document nodes."""
⋮----
nodes = walk_wiki_nodes(space_id)
⋮----
doc_type = _normalize_doc_type(node.get("obj_type", ""))
node_token = node.get("node_token", "")
doc_title = node.get("title", "")
````

## File: ai-service/rag/loader.py
````python
class DocumentLoader
⋮----
def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200)
⋮----
def load_file(self, file_path: str) -> str
⋮----
"""Load file content based on extension."""
path = Path(file_path)
⋮----
ext = path.suffix.lower()
⋮----
def _load_docx(self, path: Path) -> str
⋮----
"""Extract paragraph text from a docx file with the standard library."""
⋮----
xml_bytes = archive.read("word/document.xml")
root = ET.fromstring(xml_bytes)
namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
paragraphs: list[str] = []
⋮----
text = "".join(node.text or "" for node in paragraph.findall(".//w:t", namespace)).strip()
⋮----
def split(self, text: str) -> list[Document]
⋮----
chunks: list[Document] = []
sections = [part.strip() for part in re.split(r"\n{2,}", text) if part.strip()]
⋮----
def load_and_split(self, file_path: str) -> list[Document]
⋮----
"""Load and split a file in one call."""
raw_text = self.load_file(file_path)
unified_text = normalize_text(raw_text)
cleaned_text = denoise_text(unified_text)
docs = self.split(cleaned_text)
⋮----
title = self._extract_title(unified_text, path)
chunk_count = len(docs)
⋮----
content_hash = hashlib.sha1(f"{path.name}:{index}:{doc.page_content}".encode("utf-8")).hexdigest()
⋮----
def _extract_title(self, text: str, path: Path) -> str
⋮----
line = line.strip()
````

## File: ai-service/rag/reranker.py
````python
logger = logging.getLogger("ai-service.rag.reranker")
⋮----
class Reranker
⋮----
@property
    def enabled(self) -> bool
⋮----
def rerank(self, query: str, docs: list[Document]) -> list[Document]
⋮----
payload = {
data = self._post_json(payload)
reranked_docs = self._documents_from_response(data, docs)
⋮----
def _post_json(self, payload: dict[str, Any]) -> dict[str, Any]
⋮----
headers = {
url = f"{self.base_url}/rerank"
⋮----
response = self._client.post(url, json=payload, headers=headers, timeout=self.timeout_seconds)
⋮----
response = client.post(url, json=payload, headers=headers)
⋮----
def _documents_from_response(self, data: dict[str, Any], docs: list[Document]) -> list[Document]
⋮----
raw_results = data.get("results") or data.get("data") or []
⋮----
scored_docs: list[Document] = []
⋮----
index = item.get("index")
⋮----
score = item.get("relevance_score", item.get("score"))
metadata = {
````

## File: ai-service/rag/retriever.py
````python
logger = logging.getLogger("ai-service.rag")
⋮----
def _cosine_similarity(a: list[float], b: list[float]) -> float
⋮----
dot = sum(x * y for x, y in zip(a, b))
norm_a = sum(x * x for x in a) ** 0.5
norm_b = sum(x * x for x in b) ** 0.5
⋮----
class _PGVectorClient
⋮----
def __init__(self, db_url: str)
⋮----
def _get_conn(self)
⋮----
def _ensure_table(self)
⋮----
conn = self._get_conn()
⋮----
def add_documents(self, docs: list[Document], embeddings: list[list[float]])
⋮----
doc_id = doc.metadata.get("id") or str(uuid.uuid4())
meta = doc.metadata or {}
⋮----
def similarity_search(self, query_embedding: list[float], k: int = 4) -> list[tuple[str, str, dict, float]]
⋮----
query_dimensions = len(query_embedding)
rows = conn.execute(
⋮----
def list_documents(self, status_filter: Optional[str] = None, limit: int = 5000) -> list[Document]
⋮----
docs: list[Document] = []
⋮----
metadata = json.loads(metadata)
⋮----
def has_documents(self, status_filter: Optional[str] = None) -> bool
⋮----
row = conn.execute(
⋮----
def document_count(self) -> int
⋮----
row = conn.execute("SELECT COUNT(*) FROM rag_documents WHERE embedding IS NOT NULL").fetchone()
⋮----
def close(self)
⋮----
class VectorStoreRetriever
⋮----
def _try_connect_pgvector(self)
⋮----
count = self._pg_client.document_count()
⋮----
@property
    def storage_mode(self) -> str
⋮----
def _embed_texts(self, texts: list[str]) -> list[list[float]]
⋮----
def _embed_query(self, query: str) -> list[float]
⋮----
def add_documents(self, docs: list[Document], status: Optional[str] = None)
⋮----
texts = [doc.page_content for doc in docs]
embs = self._embed_texts(texts)
⋮----
def similarity_search(self, query: str, k: int = 4, status_filter: Optional[str] = None) -> list[Document]
⋮----
query_emb = self._embed_query(query)
rows = self._pg_client.similarity_search(query_emb, k=k * 2)
docs = [
⋮----
results = self._store.similarity_search(query, k=k * 2)
⋮----
def bm25_search(self, query: str, k: int = 4, status_filter: Optional[str] = None) -> list[Document]
⋮----
docs = self._all_documents(status_filter=status_filter)
ranked = bm25_rank(query, docs, k=k)
results: list[Document] = []
⋮----
def hybrid_search(self, queries: list[str], k: int = 4, status_filter: Optional[str] = None) -> list[Document]
⋮----
rank_lists: list[list[Document]] = []
⋮----
vector_docs = self.similarity_search(query, k=k, status_filter=status_filter)
⋮----
bm25_docs = self.bm25_search(query, k=k, status_filter=status_filter)
⋮----
def _all_documents(self, status_filter: Optional[str] = None) -> list[Document]
⋮----
@staticmethod
    def _apply_status_filter(docs: list[Document], status_filter: Optional[str] = None) -> list[Document]
````

## File: ai-service/rag/rewriter.py
````python
logger = logging.getLogger("ai-service.rag.rewriter")
⋮----
_REWRITE_SYSTEM = """你是一个查询改写专家。给定用户的原始问题，生成2-3个语义不同但相关的检索查询。
⋮----
_HUMANIZER_SYSTEM = """你是中文问题改写编辑。把用户问题改成适合 RAG 生成回答的自然中文。
⋮----
_FALLBACK_TEMPLATES = [
⋮----
class QueryRewriter
⋮----
def rewrite(self, question: str) -> list[str]
⋮----
def _semantic_rewrite(self, question: str) -> list[str]
⋮----
messages = [
response = self.llm.invoke(messages)
content = response.content if hasattr(response, "content") else str(response)
⋮----
queries = json.loads(content)
⋮----
def _template_rewrite(self, question: str) -> list[str]
⋮----
queries = [question]
⋮----
def humanize_for_answer(self, question: str) -> str
⋮----
normalized = " ".join(question.strip().split())
⋮----
response = self.llm.invoke([
⋮----
content = str(content).strip().strip("\"'")
⋮----
def _fallback_humanize(self, question: str) -> str
⋮----
replacements = {
text = question
⋮----
text = text.replace(old, new)
text = " ".join(text.split()).strip()
````

## File: ai-service/rag/text_processing.py
````python
_CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
_LATIN_RE = re.compile(r"[a-z0-9][a-z0-9_-]{1,}")
_NOISE_RE = re.compile(r"[^\w\s\u4e00-\u9fff]", re.UNICODE)
_SPACES_RE = re.compile(r"[ \t\f\v]+")
_BLANK_LINES_RE = re.compile(r"\n{3,}")
````

## File: ai-service/requirements.txt
````
fastapi==0.115.0
uvicorn[standard]==0.30.0
langchain==0.3.0
langchain-community==0.3.0
langchain-openai==0.2.0
langchain-core==0.3.0
langchain-postgres==0.0.12
psycopg[binary]>=3.2.0
langgraph==0.2.0
openai==1.50.0
redis==5.1.0
python-dotenv==1.0.1
httpx==0.27.0
beautifulsoup4==4.12.0
lxml==5.3.0
reportlab==4.2.0
faiss-cpu==1.9.0.post1
numpy>=2.0.0
````

## File: ai-service/tests/__init__.py
````python

````

## File: ai-service/tests/conftest.py
````python
def pytest_configure(config)
⋮----
def pytest_pyfunc_call(pyfuncitem)
⋮----
test_func = pyfuncitem.obj
⋮----
kwargs = {
````

## File: ai-service/tests/test_advisors.py
````python
class TestLoggerAdvisor
⋮----
@pytest.fixture
    def advisor(self)
⋮----
def test_on_step_stores_step(self, advisor)
⋮----
def test_on_step_multiple(self, advisor)
⋮----
steps_data = [
⋮----
def test_on_step_with_tool_specifics(self, advisor)
⋮----
step = {
⋮----
stored = advisor.get_steps()[0]
⋮----
def test_get_steps_returns_copy(self, advisor)
⋮----
steps = advisor.get_steps()
⋮----
def test_clear_removes_all_steps(self, advisor)
⋮----
def test_clear_then_add(self, advisor)
⋮----
def test_initial_state_empty(self, advisor)
⋮----
class TestReReadAdvisor
⋮----
def test_fewer_messages_returns_all(self, advisor)
⋮----
messages = [
context = advisor.get_recent_context(messages)
⋮----
def test_exactly_at_boundary(self, advisor)
⋮----
messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(6)]
⋮----
def test_exceeds_boundary_trims_oldest(self, advisor)
⋮----
messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(10)]
⋮----
def test_empty_messages(self, advisor)
⋮----
def test_single_message(self, advisor)
⋮----
messages = [{"role": "user", "content": "hello"}]
⋮----
def test_custom_recent_n(self)
⋮----
advisor = ReReadAdvisor(recent_n=5)
messages = [{"role": "user", "content": str(i)} for i in range(20)]
⋮----
def test_large_recent_n(self)
⋮----
advisor = ReReadAdvisor(recent_n=100)
messages = [{"role": "user", "content": "a"}, {"role": "assistant", "content": "b"}]
⋮----
def test_preserves_message_order(self, advisor)
⋮----
messages = [{"role": "user" if i % 2 == 0 else "assistant", "content": str(i)} for i in range(20)]
⋮----
expected = messages[-6:]
⋮----
def test_different_message_formats(self, advisor)
````

## File: ai-service/tests/test_agent_execution_flow.py
````python
def collect_async(async_iterable)
⋮----
async def _collect()
⋮----
class FakeStreamingAgent
⋮----
def __init__(self, updates)
⋮----
async def astream(self, payload, **kwargs)
⋮----
class FakeFailingStreamingAgent
⋮----
def __init__(self, exc)
⋮----
class FakeFailingInvokeAgent
⋮----
async def ainvoke(self, payload, **kwargs)
⋮----
def test_agent_stream_routes_search_requests_through_langgraph(monkeypatch)
⋮----
fake_agent = FakeStreamingAgent([
⋮----
async def fail_if_called(*args, **kwargs)
⋮----
ai_agent = agent_module.AIAgent()
events = collect_async(ai_agent.aexecute_stream("搜索北京周边徒步路线"))
⋮----
def test_agent_stream_exits_gracefully_when_step_budget_is_exhausted(monkeypatch)
⋮----
"""A LangGraph step-budget failure should become a controlled Agent exit, not raw model/runtime text."""
⋮----
fake_agent = FakeFailingStreamingAgent(RuntimeError("Sorry, need more steps to process this request."))
⋮----
ai_agent = AIAgent()
events = collect_async(ai_agent.aexecute_stream("今天的天气适合去徒步吗"))
⋮----
text_events = [event for event in events if event["type"] == "text"]
done_event = events[-1]
⋮----
def test_agent_sync_execute_exits_gracefully_when_step_budget_is_exhausted(monkeypatch)
⋮----
fake_agent = FakeFailingInvokeAgent(RuntimeError("Sorry, need more steps to process this request."))
⋮----
result = asyncio.run(AIAgent().aexecute("帮我规划一个复杂徒步任务"))
⋮----
def test_agent_stream_emits_react_tool_chain_details(monkeypatch)
⋮----
events = collect_async(ai_agent.aexecute_stream("帮我推荐北京周边徒步路线"))
⋮----
event_types = [event["type"] for event in events]
⋮----
tool_call = next(event for event in events if event["type"] == "tool_call")
⋮----
tool_result = next(event for event in events if event["type"] == "tool_result")
⋮----
def test_agent_stream_stops_when_terminate_tool_returns(monkeypatch)
⋮----
final_text = "".join(event["content"] for event in events if event["type"] == "text")
⋮----
def test_agent_prompt_contains_current_location_guidance(monkeypatch)
⋮----
context = understand_request(
prompt = ai_agent._build_system_prompt(context, select_tools_for_context(context))
⋮----
def test_agent_prompt_uses_structured_system_template(monkeypatch)
⋮----
context = understand_request("今天的天气适合去徒步吗")
⋮----
expected_tags = [
⋮----
def test_agent_stream_prefetches_current_location_weather_before_final_answer(monkeypatch)
⋮----
tool_calls = []
captured_prompts = []
captured_tool_names = []
⋮----
async def fake_geo_ainvoke(payload)
⋮----
async def fake_weather_ainvoke(payload)
⋮----
def fake_create_react_agent(*args, **kwargs)
⋮----
state_modifier = kwargs["state_modifier"]
⋮----
events = collect_async(
⋮----
def test_agent_stream_uses_llm_query_rewrite_metadata(monkeypatch)
⋮----
class FakeLLM
⋮----
def invoke(self, messages)
⋮----
rewrite_event = next(
⋮----
def test_agent_stream_emits_approval_required_for_high_risk_tool(monkeypatch)
⋮----
events = collect_async(ai_agent.aexecute_stream("写入徒步计划"))
⋮----
approval = next(event for event in events if event["type"] == "approval_required")
⋮----
tool_results = [event for event in events if event["type"] == "tool_result"]
⋮----
def test_chat_sse_persists_assistant_reply_and_emits_single_done(monkeypatch)
⋮----
stored_messages = []
⋮----
class FakeMemory
⋮----
def __init__(self, chat_id)
⋮----
def add_message(self, role, content)
⋮----
def get_messages(self)
⋮----
class FakeAgent
⋮----
def __init__(self, *args, **kwargs)
⋮----
async def aexecute_stream(self, message, history=None)
⋮----
client = TestClient(app)
response = client.post(
⋮----
events = []
⋮----
line = line.decode("utf-8")
⋮----
def test_chat_sse_passes_current_location_to_agent(monkeypatch)
⋮----
received = {}
⋮----
async def aexecute_stream(self, message, history=None, **kwargs)
````

## File: ai-service/tests/test_agent_intake.py
````python
def test_weather_risk_intake_uses_current_location_when_destination_missing()
⋮----
context = understand_request(
⋮----
def test_current_location_normalization_preserves_zero_coordinates()
⋮----
def test_risk_assessment_intake_extracts_destination_and_date()
⋮----
context = understand_request("这周末武功山适合去吗")
⋮----
def test_route_plan_without_destination_requires_clarification()
⋮----
context = understand_request("帮我做两天一夜攻略")
⋮----
def test_layering_question_is_knowledge_qa_without_missing_slots()
⋮----
context = understand_request("三层穿衣法是什么")
⋮----
def test_request_scenario_overrides_heuristic_intent()
⋮----
context = understand_request("继续完善这份攻略", scenario="report_export")
````

## File: ai-service/tests/test_agent.py
````python
class FakeStreamingAgent
⋮----
def __init__(self, updates)
⋮----
async def astream(self, payload, **kwargs)
⋮----
def collect_async(async_iterable)
⋮----
async def _collect()
⋮----
def _make_tool_call_update(tool_name: str, args: dict, call_id: str = "call-1")
⋮----
def test_get_tool_registry_returns_tool_registry_instance()
⋮----
registry = AIAgent.get_tool_registry()
⋮----
def test_get_tool_registry_has_expected_tools()
⋮----
expected_tools = {
registered_names = {md.name for md in registry.list_tools()}
⋮----
def test_get_tool_registry_is_singleton()
⋮----
"""get_tool_registry() 多次调用应返回同一个注册表实例（模块级单例）。"""
⋮----
# ─── Test: tool_call metadata 富化 ────────────────────────
⋮----
def test_tool_call_metadata_has_risk_fields(monkeypatch)
⋮----
"""tool_call 事件的 metadata 应包含 risk_level / needs_confirmation / rate_limit_exceeded。"""
⋮----
fake = FakeStreamingAgent(
⋮----
agent = AIAgent()
events = collect_async(agent.aexecute_stream("test"))
⋮----
tool_call = next(e for e in events if e["type"] == "tool_call")
meta = tool_call["metadata"]
⋮----
def test_low_risk_tool_metadata(monkeypatch)
⋮----
def test_medium_risk_tool_metadata(monkeypatch)
⋮----
def test_high_risk_tool_metadata(monkeypatch)
⋮----
def test_critical_risk_tool_metadata(monkeypatch)
⋮----
def test_unknown_tool_falls_back_to_medium_risk(monkeypatch)
⋮----
def test_rate_limited_tool_detection(monkeypatch)
⋮----
bucket = tool_registry._buckets["terminal"]
````

## File: ai-service/tests/test_chat_confirmation_fields.py
````python
def test_confirmation_uses_needs_confirmation_metadata_key()
⋮----
store = ConfirmationStore()
event = {
⋮----
confirmation_id = event["metadata"].get("confirmation_id")
⋮----
record = store.get(confirmation_id)
⋮----
def test_confirmation_ignores_legacy_needs_confirm_key()
````

## File: ai-service/tests/test_chat_health.py
````python
def test_chat_health_unconfigured(monkeypatch)
⋮----
client = TestClient(app)
response = client.get("/api/v1/chat/health")
⋮----
data = response.json()
⋮----
def test_chat_health_agent_raises_key_error(monkeypatch)
⋮----
class BrokenAIAgent
⋮----
def __init__(self, *args, **kwargs)
⋮----
def test_chat_sse_missing_openai_key_returns_stream_error(monkeypatch)
⋮----
response = client.post(
⋮----
body = response.text
⋮----
def test_chat_sse_accepts_runtime_llm_settings_without_env_key(monkeypatch)
⋮----
captured = {}
⋮----
class FakeAgent
⋮----
def __init__(self, *args, llm_config=None, **kwargs)
⋮----
async def aexecute_stream(self, message, history=None, scenario=None)
⋮----
def test_chat_sync_missing_openai_key_returns_503(monkeypatch)
````

## File: ai-service/tests/test_chat_memory_integration.py
````python
def test_agent_memory_initialization_enabled(monkeypatch)
⋮----
agent = AIAgent()
⋮----
def test_agent_memory_uses_runtime_llm_config_when_env_key_missing(monkeypatch)
⋮----
runtime = RuntimeLlmConfig(
⋮----
def test_agent_memory_initialization_disabled(monkeypatch)
⋮----
def test_chat_sync_endpoint_memory_integration(monkeypatch)
⋮----
dummy_chat_id = "test-chat-sync-123"
dummy_message = "测试徒步路线"
⋮----
mock_memory_ctx = {
⋮----
mock_agent_instance = MagicMock()
async def mock_ainvoke(*args, **kwargs)
⋮----
client = TestClient(app)
response = client.post(
⋮----
data = response.json()
⋮----
def test_chat_sse_endpoint_memory_integration(monkeypatch)
⋮----
dummy_chat_id = "test-chat-sse-123"
dummy_message = "测试流式响应"
⋮----
lines = [line if isinstance(line, str) else line.decode("utf-8") for line in response.iter_lines() if line]
events = []
⋮----
text_events = [e for e in events if e.get("type") == "text"]
⋮----
def test_chat_memory_disabled_no_calls(monkeypatch)
⋮----
dummy_chat_id = "test-chat-disabled"
dummy_message = "测试内存关闭"
⋮----
def test_chat_memory_exception_fallback(monkeypatch)
⋮----
dummy_chat_id = "test-chat-error"
dummy_message = "测试内存报错 fallback"
````

## File: ai-service/tests/test_confirmation.py
````python
class TestConfirmationStore
⋮----
def test_add_and_get(self)
⋮----
store = ConfirmationStore()
cid = store.add("delete_file", {"path": "/tmp/x"}, chat_id="chat-1", step=0)
rec = store.get(cid)
⋮----
def test_add_with_custom_id(self)
⋮----
cid = "my-custom-id"
returned = store.add(
⋮----
def test_get_nonexistent(self)
⋮----
def test_confirm(self)
⋮----
cid = store.add("delete_file", {}, chat_id="chat-1", step=0)
⋮----
def test_confirm_twice_returns_false(self)
⋮----
def test_reject(self)
⋮----
def test_confirm_rejected_returns_false(self)
⋮----
def test_get_pending_by_chat(self)
⋮----
c1 = store.add("tool1", {}, chat_id="chat-1", step=0)
c2 = store.add("tool2", {}, chat_id="chat-1", step=1)
c3 = store.add("tool3", {}, chat_id="chat-2", step=0)
⋮----
pending = store.get_pending_by_chat("chat-1")
ids = {r.confirmation_id for r in pending}
⋮----
def test_get_pending_excludes_confirmed(self)
⋮----
cid = store.add("tool1", {}, chat_id="chat-1", step=0)
⋮----
def test_cleanup_expired(self)
⋮----
rec = store.get(c1)
⋮----
cleaned = store.cleanup_expired(max_age=50)
⋮----
def test_get_store_singleton(self)
⋮----
s1 = get_store()
s2 = get_store()
⋮----
@pytest.fixture
def client()
⋮----
class TestConfirmHttpEndpoint
⋮----
def test_confirm_valid(self, client)
⋮----
store = get_store()
cid = store.add("danger_tool", {"key": "val"}, chat_id="chat-1", step=0)
⋮----
resp = client.post("/api/v1/chat/confirm", json={
⋮----
data = resp.json()
⋮----
def test_reject_valid(self, client)
⋮----
cid = store.add("danger_tool", {}, chat_id="chat-1", step=0)
⋮----
def test_confirm_not_found(self, client)
⋮----
def test_confirm_already_resolved(self, client)
⋮----
def test_confirm_invalid_action(self, client)
⋮----
def test_get_pending(self, client)
⋮----
resp = client.get("/api/v1/chat/pending/chat-1")
⋮----
def test_get_pending_empty(self, client)
⋮----
resp = client.get("/api/v1/chat/pending/empty-chat")
⋮----
def test_tool_call_interception_adds_confirmation_id()
⋮----
tool_event = {
⋮----
metadata = tool_event.get("metadata")
⋮----
cid = store.add(
⋮----
rec = store.get(tool_event["metadata"]["confirmation_id"])
⋮----
def test_tool_call_without_needs_confirm_not_stored()
````

## File: ai-service/tests/test_embedding_config.py
````python
def test_settings_loads_independent_embedding_config(monkeypatch)
⋮----
settings = Settings().load()
⋮----
def test_settings_loads_without_global_chat_api_key(monkeypatch)
⋮----
def test_settings_loads_independent_rerank_config(monkeypatch)
⋮----
def test_rag_retriever_uses_embedding_config(monkeypatch)
⋮----
captured = {}
⋮----
class Embeddings
⋮----
def __init__(self, **kwargs)
⋮----
def test_memory_vector_store_uses_embedding_config(monkeypatch, tmp_path)
````

## File: ai-service/tests/test_feishu.py
````python
FEISHU_EXTERNAL_ERROR_MARKERS = (
⋮----
def _skip_if_feishu_external_error(exc: Exception) -> None
⋮----
message = str(exc)
⋮----
# ── Cycle 1: _run_lark_cli tracer bullet ──────────────────────────
⋮----
class TestRunLarkCli
⋮----
"""Verify the lark-cli subprocess wrapper works end-to-end."""
⋮----
def test_calls_lark_cli_and_returns_parsed_json(self)
⋮----
"""Tracer bullet: a real lark-cli call returns ok=True with data."""
result = _run_lark_cli(["drive", "+search", "--query", "test", "--page-size", "1"])
⋮----
def test_returns_results_with_expected_search_fields(self)
⋮----
result = _run_lark_cli(["drive", "+search", "--query", "test", "--page-size", "2"])
data = result["data"]
⋮----
def test_raises_on_invalid_command(self)
⋮----
def test_lark_cli_resolved_to_full_path(self)
⋮----
class TestSearchFeishuDocs
⋮----
def test_search_with_keyword_returns_results(self)
⋮----
result = search_feishu_docs(query="test", page_size=3)
⋮----
def test_results_contain_document_metadata(self)
⋮----
result = search_feishu_docs(query="test", page_size=2)
⋮----
meta = item["result_meta"]
⋮----
def test_pagination_fields_present(self)
⋮----
result = search_feishu_docs(query="test", page_size=1)
⋮----
def test_empty_query_browses_all_documents(self)
⋮----
result = search_feishu_docs(query="", page_size=2)
⋮----
def test_page_size_respected(self)
⋮----
def test_pagination_advances_with_page_token(self)
⋮----
page1 = search_feishu_docs(query="test", page_size=2)
⋮----
page2 = search_feishu_docs(
⋮----
class TestFeishuDocLoader
⋮----
@pytest.fixture(autouse=True)
    def setup(self)
⋮----
search = search_feishu_docs(query="test", page_size=1)
⋮----
def test_fetch_content_returns_markdown_and_title(self)
⋮----
fetched = self.loader.fetch_content(self.doc_token)
⋮----
def test_load_and_split_returns_documents_with_metadata(self)
⋮----
docs = self.loader.load_and_split(self.doc_token, doc_type=self.doc_type)
⋮----
def test_load_and_split_respects_custom_title(self)
⋮----
custom_title = "My Custom Document Title"
docs = self.loader.load_and_split(
⋮----
def test_load_and_split_uses_fetched_title_when_no_custom(self)
⋮----
expected_title = fetched["title"]
⋮----
def test_chunk_overlap_is_respected(self)
⋮----
overlap_end = docs[0].page_content[-50:]
⋮----
def test_fetch_content_returns_clean_text_without_html_tags(self)
⋮----
content = fetched["markdown"]
⋮----
def test_detect_feishu_in_question_with_url()
⋮----
question = "请总结 https://xxx.feishu.cn/docx/AbCdEf1234567890abcdef 的内容"
token = extract_doc_token(question)
⋮----
question2 = "看看这篇 https://xxx.feishu.cn/doc/XyZ0987654321AbCdEfGhIj 说了什么"
token2 = extract_doc_token(question2)
⋮----
def test_detect_feishu_returns_none_for_plain_text()
⋮----
question = "什么是RAG？它有什么用途？"
result = extract_doc_token(question)
⋮----
def test_fetch_feishu_from_question_url_end_to_end()
⋮----
loader = FeishuDocLoader()
⋮----
doc_token = search["results"][0]["result_meta"]["token"]
⋮----
question = f"这篇文章在说什么？https://feishu.cn/docx/{doc_token}"
extracted = extract_doc_token(question)
⋮----
fetched = loader.fetch_content(extracted)
⋮----
def test_html_to_text_strips_tags_and_preserves_content()
⋮----
html = "<h1>Test Title</h1><p>Hello <b>World</b></p><ul><li>Item 1</li><li>Item 2</li></ul>"
text = _html_to_text(html)
⋮----
def test_html_to_text_handles_empty_html()
⋮----
# ── Cycle 4: extract_doc_token + FeishuDefaultSyncer ──────────────
⋮----
class TestExtractDocToken
⋮----
"""Verify URL-to-token extraction."""
⋮----
def test_extracts_token_from_docx_url(self)
⋮----
url = "https://xxx.feishu.cn/docx/AbCdEf1234567890abcdef"
⋮----
def test_extracts_token_from_doc_url(self)
⋮----
url = "https://xxx.feishu.cn/doc/XyZ0987654321AbCdEfGhIj"
⋮----
def test_extracts_token_from_bitable_url(self)
⋮----
url = "https://xxx.feishu.cn/bitable/BTbL1234567890abcdefgh"
⋮----
def test_extracts_wiki_node_token_from_url(self)
⋮----
url = "https://xxx.feishu.cn/wiki/WIKINodeToken1234567890ab"
⋮----
def test_inspects_wiki_link_as_node(self)
⋮----
link = inspect_feishu_link(url)
⋮----
def test_passes_through_plain_token(self)
⋮----
token = "SREndflzEonZnIxyGBEcLtEmnuQ"
⋮----
def test_raises_on_invalid_url(self)
⋮----
def test_resolve_wiki_node_uses_lark_api_get_node(monkeypatch)
⋮----
calls = []
⋮----
def fake_run(args)
⋮----
node = resolve_wiki_node("WIKINodeToken1234567890ab")
⋮----
def test_list_wiki_nodes_uses_lark_api_space_nodes_endpoint(monkeypatch)
⋮----
page = list_wiki_nodes("space123", parent_node_token="parent123", page_size=20)
⋮----
def test_loader_fetches_wiki_node_underlying_document(monkeypatch)
⋮----
docs = FeishuDocLoader(chunk_size=200, chunk_overlap=20).load_and_split(
⋮----
class TestFeishuDefaultSyncer
⋮----
def test_sync_from_space_returns_summary(self)
⋮----
space_id = settings.feishu_default_space_id
⋮----
results = self.syncer.sync_from_space(space_id)
⋮----
doc = results[0]
⋮----
def test_sync_from_folder_returns_summary(self)
⋮----
folder_token = settings.feishu_default_folder_token
⋮----
results = self.syncer.sync_from_folder(folder_token)
⋮----
def test_sync_errors_are_recorded_not_raised(self)
⋮----
results = self.syncer._sync_all(space_id="non_existent_space_12345")
⋮----
def test_add_documents_stores_in_memory(self)
⋮----
token = search["results"][0]["result_meta"]["token"]
⋮----
docs = loader.load_and_split(token, title="Integration Test Doc")
⋮----
initial_count = len(self.retriever.documents)
⋮----
def test_synced_documents_are_retrievable(self)
⋮----
results = self.retriever.similarity_search("test", k=2, status_filter="feishu")
⋮----
cls_name = type(e).__name__.lower()
msg = str(e).lower()
````

## File: ai-service/tests/test_file_memory.py
````python
@pytest.fixture
def memory(tmp_path)
⋮----
save_dir = tmp_path / "chat_data"
⋮----
class TestFileChatMemory
⋮----
def test_init_creates_directory(self, tmp_path)
⋮----
save_dir = tmp_path / "new_chat"
mem = FileChatMemory("chat_1", save_dir=str(save_dir))
⋮----
def test_add_and_get_messages(self, memory)
⋮----
messages = mem.get_messages()
⋮----
def test_clear_removes_all_messages(self, memory)
⋮----
def test_get_messages_returns_copy(self, memory)
⋮----
msgs = mem.get_messages()
⋮----
def test_sliding_window_trims_old_messages(self, tmp_path)
⋮----
save_dir = tmp_path / "sliding"
mem = FileChatMemory("sliding_test", save_dir=str(save_dir))
⋮----
max_messages = 60
⋮----
role = "user" if i % 2 == 0 else "assistant"
⋮----
# 验证裁剪后保留的是最新的消息
⋮----
def test_sliding_window_boundary(self, tmp_path)
⋮----
save_dir = tmp_path / "boundary"
mem = FileChatMemory("boundary_test", save_dir=str(save_dir))
⋮----
# ── 持久化测试 ──
⋮----
def test_persistence_saves_to_disk(self, memory)
⋮----
"""测试消息被持久化到磁盘文件"""
⋮----
json_path = save_dir / "messages.json"
⋮----
data = json.load(f)
⋮----
def test_persistence_loads_from_disk(self, tmp_path)
⋮----
save_dir = tmp_path / "persist"
⋮----
mem1 = FileChatMemory("p_chat", save_dir=str(save_dir))
⋮----
mem2 = FileChatMemory("p_chat", save_dir=str(save_dir))
messages = mem2.get_messages()
⋮----
def test_empty_disk_file_returns_empty_list(self, tmp_path)
⋮----
save_dir = tmp_path / "empty"
⋮----
mem = FileChatMemory("empty_chat", save_dir=str(save_dir))
⋮----
def test_corrupted_disk_file_handling(self, tmp_path)
⋮----
save_dir = tmp_path / "corrupted"
⋮----
mem = FileChatMemory("corrupted_chat", save_dir=str(save_dir))
⋮----
def test_multiple_sessions_isolated(self, tmp_path)
⋮----
base_dir = tmp_path / "multi"
mem_a = FileChatMemory("chat_a", save_dir=str(base_dir / "chat_a"))
mem_b = FileChatMemory("chat_b", save_dir=str(base_dir / "chat_b"))
````

## File: ai-service/tests/test_hiking_domain_tools.py
````python
@pytest.mark.asyncio
async def test_geo_lookup_supports_amap_reverse_geocode(monkeypatch)
⋮----
class FakeResponse
⋮----
def raise_for_status(self)
⋮----
def json(self)
⋮----
class FakeClient
⋮----
def __init__(self, *args, **kwargs)
⋮----
async def __aenter__(self)
⋮----
async def __aexit__(self, exc_type, exc, tb)
⋮----
async def get(self, url, params)
⋮----
result = await geo_lookup.ainvoke({"latitude": 39.9042, "longitude": 116.4074})
⋮----
@pytest.mark.asyncio
async def test_weather_lookup_uses_coordinates_before_amap_weather(monkeypatch)
⋮----
calls = []
⋮----
def __init__(self, payload)
⋮----
result = await weather_lookup.ainvoke({
````

## File: ai-service/tests/test_hiking_knowledge_tool.py
````python
def test_hiking_knowledge_search_returns_traceable_chunks(monkeypatch)
⋮----
class FakeRetriever
⋮----
def hybrid_search(self, queries, k=4, status_filter=None)
⋮----
result = asyncio.run(hiking_knowledge.hiking_knowledge_search.ainvoke({"query": "失温怎么处理"}))
⋮----
def test_hiking_knowledge_search_reports_empty_evidence(monkeypatch)
⋮----
result = asyncio.run(hiking_knowledge.hiking_knowledge_search.ainvoke({"query": "不存在的路线"}))
````

## File: ai-service/tests/test_hiking_tool_selection.py
````python
def tool_names(tools)
⋮----
def test_gear_check_exposes_only_hiking_safe_tools()
⋮----
context = understand_request("新手单日徒步装备清单")
⋮----
names = tool_names(select_tools_for_context(context))
⋮----
def test_current_location_weather_question_exposes_geo_and_weather_tools()
⋮----
context = understand_request(
⋮----
def test_prefetched_current_location_weather_reduces_followup_tools()
⋮----
def test_general_chat_exposes_only_termination_control()
⋮----
context = understand_request("你好")
⋮----
def test_report_export_exposes_export_tools_but_not_terminal()
⋮----
context = understand_request("把武功山路线整理成 PDF")
⋮----
def test_all_registered_tool_functions_are_addressable_by_name()
⋮----
required = {
⋮----
def test_tool_configuration_validation_reports_current_setup_ok()
⋮----
result = validate_tool_configuration()
````

## File: ai-service/tests/test_mcp_client.py
````python
@pytest.mark.asyncio
async def test_connect_stdio_success()
⋮----
mock_process = AsyncMock()
⋮----
c = MCPClient()
⋮----
@pytest.mark.asyncio
async def test_connect_stdio_failure()
⋮----
@pytest.mark.asyncio
async def test_send_request_sends_json_rpc_and_returns_response()
⋮----
mock_stdin = AsyncMock()
mock_stdout = AsyncMock()
⋮----
mock_process = AsyncMock(spec=asyncio.subprocess.Process)
⋮----
response = await c._send_request("list_tools")
⋮----
written_data = mock_stdin.write.call_args[0][0]
sent = json.loads(written_data)
⋮----
@pytest.mark.asyncio
async def test_send_request_not_connected()
⋮----
@pytest.mark.asyncio
async def test_send_request_timeout()
⋮----
@pytest.mark.asyncio
async def test_list_tools_returns_tools_and_caches()
⋮----
tools_data = [
⋮----
result = await c.list_tools()
⋮----
@pytest.mark.asyncio
async def test_list_tools_empty_on_error()
⋮----
@pytest.mark.asyncio
async def test_call_tool_calls_mcp_and_returns_content()
⋮----
expected_content = [{"type": "text", "text": "42"}]
⋮----
result = await c.call_tool("calculator", {"expression": "6*7"})
⋮----
@pytest.mark.asyncio
async def test_call_tool_error_returns_error_string()
⋮----
result = await c.call_tool("calculator")
⋮----
@pytest.mark.asyncio
async def test_convert_to_langchain_tools_creates_decorated_tools()
⋮----
lc_tools = c.convert_to_langchain_tools()
⋮----
tool_fn = lc_tools[0]
⋮----
result = await tool_fn.ainvoke({"query": "hello"})
⋮----
@pytest.mark.asyncio
async def test_convert_to_langchain_tools_empty()
⋮----
@pytest.mark.asyncio
async def test_load_tools_from_config_returns_empty_when_disabled()
⋮----
tools = await load_mcp_tools(None)
⋮----
@pytest.mark.asyncio
async def test_load_tools_from_config_namespaces_loaded_tools()
⋮----
mock_tool = MagicMock()
⋮----
tools = await load_mcp_tools({
⋮----
@pytest.mark.asyncio
async def test_close_terminates_process_and_waits()
⋮----
@pytest.mark.asyncio
async def test_close_no_process()
⋮----
@pytest.mark.asyncio
async def test_close_already_terminated()
````

## File: ai-service/tests/test_memory_committer.py
````python
def test_profile_memory_candidates_capture_stable_hiking_preferences()
⋮----
committer = MemoryCommitter()
⋮----
candidates = committer.extract_candidates(
⋮----
facts = {(item["type"], item["predicate"], item["object"]) for item in candidates}
⋮----
def test_trip_memory_candidates_store_structured_state_not_weather_result()
⋮----
trip = next(item for item in candidates if item["type"] == "TripMemory")
````

## File: ai-service/tests/test_memory.py
````python
class TestSessionCompressor
⋮----
@pytest.fixture(autouse=True)
    def _mock_llm(self)
⋮----
patcher = patch("memory.compressor.ChatOpenAI")
mock_cls = patcher.start()
⋮----
@pytest.fixture(autouse=True)
    def _imports(self)
⋮----
def test_compress_empty_history_returns_empty_string(self)
⋮----
compressor = self.SessionCompressor()
⋮----
def test_compress_no_dialogue_messages_returns_empty(self)
⋮----
"""Only system messages (no user/assistant) returns empty string."""
⋮----
history = [
⋮----
def test_fallback_used_when_llm_raises(self)
⋮----
"""When ChatOpenAI.invoke raises, fallback compression is used."""
⋮----
result = compressor.compress(history)
⋮----
def test_fallback_contains_expected_fields(self)
⋮----
def test_llm_success_returns_llm_output(self)
⋮----
def test_llm_empty_content_falls_back(self)
⋮----
def test_single_message_handled(self)
⋮----
history = [{"role": "user", "content": "你是谁？"}]
⋮----
def test_llm_called_with_correct_prompt(self)
⋮----
messages = args[0]
⋮----
class TestKnowledgeExtractor
⋮----
patcher = patch("memory.knowledge.ChatOpenAI")
⋮----
def test_extract_short_text_returns_empty(self)
⋮----
extractor = self.KnowledgeExtractor()
⋮----
def test_extract_empty_text_returns_empty(self)
⋮----
def test_extract_whitespace_text_returns_empty(self)
⋮----
"""Whitespace-only text returns empty list."""
⋮----
def test_extract_llm_failure_returns_empty(self)
⋮----
"""When ChatOpenAI.invoke raises, returns empty list."""
⋮----
result = extractor.extract("用户说他们喜欢编程，特别是Python语言。")
⋮----
def test_extract_llm_success_parses_json(self)
⋮----
knowledge_json = json.dumps([
⋮----
result = extractor.extract("用户说他们喜欢编程，用MacBook Pro。")
⋮----
def test_extract_llm_markdown_wrapped_json(self)
⋮----
markdown_wrapped = "```json\n[\n  {\"type\": \"fact\", \"subject\": \"用户\", \"predicate\": \"住在\", \"object\": \"北京\"}\n]\n```"
⋮----
result = extractor.extract("你好，用户刚才说他自己住在北京，这是他的个人偏好。")
⋮----
def test_extract_invalid_json_returns_empty(self)
⋮----
result = extractor.extract("用户说了一些话。")
⋮----
def test_parse_result_validates_required_fields(self)
⋮----
raw = json.dumps([
result = KE._parse_result(raw)
⋮----
def test_parse_result_empty_content(self)
⋮----
def test_parse_result_not_a_list(self)
⋮----
"""LLM returns a dict instead of list → empty list."""
⋮----
# ── Cycle 3: VectorStore ─────────────────────────────────────────────
⋮----
class TestVectorStore
⋮----
"""Verify vector store: add/search/save/load/clear with mocked embeddings."""
⋮----
@pytest.fixture(autouse=True)
    def _mock_embeddings(self)
⋮----
"""Mock OpenAIEmbeddings so no real API call is made."""
patcher = patch("memory.vector_store.OpenAIEmbeddings")
⋮----
@pytest.fixture(autouse=True)
    def _imports(self, tmp_path)
⋮----
def make_store(self)
⋮----
"""Helper: create a VectorStore with mocked embedding responses."""
store = self.VectorStore(store_path=self.store_path)
# Make sure _load doesn't interfere — empty store at start
⋮----
def _setup_mock_embeddings(self, store, num_items=3, dim=4)
⋮----
doc_vectors = []
⋮----
vec = [0.0] * dim
⋮----
def test_add_items_increases_count(self)
⋮----
store = self.make_store()
⋮----
def test_add_empty_items_does_nothing(self)
⋮----
def test_search_empty_store_returns_empty(self)
⋮----
def test_search_returns_relevant_items(self)
⋮----
results = store.search("red related query", k=2)
⋮----
def test_search_respects_top_k(self)
⋮----
items = [
⋮----
results = store.search("query", k=3)
⋮----
def test_embedding_failure_does_not_crash(self)
⋮----
def test_query_embedding_failure_returns_empty(self)
⋮----
results = store.search("query")
⋮----
def test_clear_removes_all_items(self)
⋮----
def test_save_and_load_roundtrip(self)
⋮----
store_a = self.make_store()
⋮----
store_b = self.VectorStore(store_path=self.store_path)
⋮----
class TestMemoryManager
⋮----
@pytest.fixture(autouse=True)
    def _mock_all(self)
⋮----
patcher1 = patch("memory.memory_manager.SessionCompressor")
patcher2 = patch("memory.memory_manager.KnowledgeExtractor")
patcher3 = patch("memory.memory_manager.VectorStore")
⋮----
def test_process_interaction_calls_update_and_returns_context(self)
⋮----
manager = self.MemoryManager()
history = [{"role": "user", "content": "我喜欢Python"}]
result = manager.process_interaction(history, "用户喜欢什么？")
⋮----
def test_get_session_context_delegates_to_compressor(self)
⋮----
history = [{"role": "user", "content": "hi"}]
⋮----
def test_get_relevant_knowledge_delegates_to_vector_store(self)
⋮----
result = manager.get_relevant_knowledge("test query")
⋮----
def test_update_knowledge_empty_history(self)
⋮----
def test_update_knowledge_extracts_and_stores(self)
⋮----
count = manager.update_knowledge(history)
⋮----
def test_update_knowledge_only_user_assistant(self)
⋮----
call_args = self.mock_extractor.extract.call_args[0][0]
⋮----
def test_format_knowledge_context_empty(self)
⋮----
def test_format_knowledge_context_formats_items(self)
⋮----
"""Format knowledge context produces readable bullet list."""
⋮----
result = manager.format_knowledge_context("query")
⋮----
def test_memory_config_defaults(self)
⋮----
config = self.MemoryConfig()
⋮----
def test_custom_config_used(self)
⋮----
manager = self.MemoryManager(config=config)
⋮----
# VectorStore created with custom path
⋮----
def test_runtime_llm_config_passed_to_memory_llm_components(self)
⋮----
config = self.MemoryConfig(
````

## File: ai-service/tests/test_models_router.py
````python
@pytest.fixture
def app()
⋮----
app = FastAPI()
⋮----
@pytest.fixture
def client(app)
⋮----
class TestModelsFetchEndpoint
⋮----
def test_successful_fetch(self, client)
⋮----
async def mock_get(url, headers=None, **kwargs)
⋮----
response = client.post("/models/fetch", json={
⋮----
data = response.json()
⋮----
def test_empty_models(self, client)
⋮----
def test_http_error(self, client)
⋮----
resp = Response(401, request=httpx.Request("GET", url))
⋮----
def test_connection_error(self, client)
⋮----
def test_trailing_slash_handling(self, client)
⋮----
captured_url = []
⋮----
def test_api_key_in_header(self, client)
⋮----
captured_headers = {}
⋮----
def test_malformed_response_data(self, client)
⋮----
{"id": ""},          # 空 id 应被过滤
⋮----
class TestModelsFetchRequestModel
⋮----
def test_valid_request(self)
⋮----
req = ModelsFetchRequest(base_url="https://api.openai.com", api_key="sk-key")
⋮----
def test_missing_base_url(self)
⋮----
def test_missing_api_key(self)
⋮----
class TestModelsFetchResponseModel
⋮----
def test_valid_response(self)
⋮----
resp = ModelsFetchResponse(models=["gpt-4", "gpt-3.5"])
⋮----
def test_empty_models_list(self)
⋮----
resp = ModelsFetchResponse(models=[])
````

## File: ai-service/tests/test_rag_augmenter.py
````python
def test_augmenter_no_docs_returns_fallback()
⋮----
augmenter = ContextAugmenter()
result = augmenter.augment("徒步安全", [])
⋮----
def test_augmenter_no_llm_returns_context()
⋮----
augmenter = ContextAugmenter(api_key="")  # no api_key → no LLM
docs = [Document(page_content="徒步安全指南内容", metadata={"source": "test"})]
result = augmenter.augment("徒步安全", docs)
⋮----
def test_augmenter_no_llm_does_not_dump_full_markdown_context()
⋮----
augmenter = ContextAugmenter(api_key="")
long_content = "
⋮----
docs = [
⋮----
result = augmenter.augment("徒步的核心目的", docs)
⋮----
def test_augmenter_no_llm_snippet_centers_question_terms()
⋮----
intro = "背景介绍" * 120
content = f"{intro}。徒步的核心目的在于亲近自然、挑战自我、提升身心素质。后续说明" * 3
docs = [Document(page_content=content, metadata={"source": "upload", "title": "户外徒步知识文档.md"})]
⋮----
def test_augmenter_no_llm_points_drop_truncated_neighbor_sentences()
⋮----
def test_augmenter_no_llm_points_drop_repeated_question_heading()
⋮----
def test_augmenter_with_llm_invokes_model(monkeypatch)
⋮----
invoked = {}
⋮----
class FakeAIMessage
⋮----
content = "根据指南，徒步需注意安全。"
⋮----
class FakeChatModel
⋮----
def invoke(self, prompt)
⋮----
async def astream(self, prompt)
⋮----
class FakeChunk
⋮----
content = chunk
⋮----
augmenter = ContextAugmenter(api_key="test-key", base_url="http://fake", model="test")
docs = [Document(page_content="安全内容", metadata={"source": "test"})]
⋮----
def test_augmenter_rejects_weakly_related_docs_even_with_llm(monkeypatch)
⋮----
result = augmenter.augment("量子物理是什么", docs)
⋮----
def test_augmenter_prompt_requires_grounded_plain_text(monkeypatch)
⋮----
content = "根据文档，徒步要带**足够的水**。[1]"
⋮----
docs = [Document(page_content="徒步要带水。", metadata={"source": "test"})]
result = augmenter.augment("徒步要带什么", docs)
⋮----
prompt_text = "\n".join(getattr(message, "content", "") for message in invoked["prompt"])
⋮----
def test_augmenter_formats_long_answer_into_dense_points(monkeypatch)
⋮----
content = (
⋮----
def test_augmenter_stream_outputs_plain_text(monkeypatch)
⋮----
class Ch
⋮----
docs = [Document(page_content="徒步的主要目的是亲近自然。", metadata={"source": "test"})]
⋮----
async def collect()
⋮----
chunks = []
⋮----
result = asyncio.run(collect())
⋮----
def test_augmenter_stream_returns_async_iterator(monkeypatch)
⋮----
"""augment_stream should return an async iterator of string chunks."""
⋮----
content = "chunk"
⋮----
content = c
⋮----
docs = [Document(page_content="徒步内容", metadata={"source": "test"})]
⋮----
chunks = asyncio.run(collect())
⋮----
def test_inject_knowledge_returns_prompt()
⋮----
"""inject_knowledge should build a prompt string from knowledge items."""
⋮----
items = [
result = augmenter.inject_knowledge("徒步准备", items)
````

## File: ai-service/tests/test_rag_direct_answer.py
````python
def test_simple_greeting_skips_retrieval(monkeypatch)
⋮----
class RetrieverShouldNotRun
⋮----
def __init__(self)
⋮----
client = TestClient(app)
⋮----
body = "\n".join(line for line in response.iter_lines() if line)
````

## File: ai-service/tests/test_rag_loader_pipeline.py
````python
def test_document_loader_cleans_chunks_and_tags_metadata(tmp_path)
⋮----
source = tmp_path / "gear.md"
⋮----
loader = DocumentLoader(chunk_size=24, chunk_overlap=4)
docs = loader.load_and_split(str(source))
⋮----
joined = "\n".join(doc.page_content for doc in docs)
````

## File: ai-service/tests/test_rag_rerank.py
````python
def test_rag_query_reranks_documents_before_augmentation(monkeypatch)
⋮----
seen = {}
⋮----
class FakeRetriever
⋮----
def similarity_search(self, query, k=2, status_filter=None)
⋮----
class FakeRewriter
⋮----
def rewrite(self, question)
⋮----
class FakeReranker
⋮----
@property
        def enabled(self)
⋮----
def rerank(self, query, docs)
⋮----
class FakeAugmenter
⋮----
def augment(self, question, docs)
⋮----
async def no_sleep(*_args, **_kwargs)
⋮----
client = TestClient(app)
⋮----
body = response.read().decode("utf-8")
⋮----
def test_rag_query_uses_hybrid_retrieval_and_humanized_question(monkeypatch)
⋮----
storage_mode = "pgvector"
⋮----
def hybrid_search(self, queries, k=4, status_filter=None)
⋮----
def humanize_for_answer(self, question)
⋮----
def test_rag_query_passes_runtime_model_settings(monkeypatch)
⋮----
def __init__(self, **kwargs)
⋮----
payload = {
⋮----
def test_rag_query_retries_default_embedding_when_runtime_embedding_returns_empty(monkeypatch)
⋮----
seen = {"retrievers": []}
⋮----
def test_rag_query_emits_process_steps_and_document_summary(monkeypatch)
⋮----
storage_mode = "memory"
⋮----
def test_rag_upload_passes_runtime_embedding_settings(monkeypatch, tmp_path)
⋮----
class FakeLoader
⋮----
def load_and_split(self, path)
⋮----
def add_documents(self, docs, status=None)
⋮----
runtime_settings = {
⋮----
response = client.post(
````

## File: ai-service/tests/test_rag_retrieve_and_output.py
````python
def test_document_search_summary_uses_plain_text_preview()
⋮----
docs = [
⋮----
summary = summarize_retrieved_documents(docs)
preview = summary["documents"][0]["content"]
⋮----
def test_rag_retrieves_documents_and_generates_answer(monkeypatch)
⋮----
seen = {}
⋮----
class FakeRetriever
⋮----
storage_mode = "memory"
⋮----
def similarity_search(self, query, k=2, status_filter=None)
⋮----
class FakeRewriter
⋮----
def rewrite(self, question)
⋮----
class FakeReranker
⋮----
@property
        def enabled(self)
⋮----
class FakeAugmenter
⋮----
def augment(self, question, docs)
⋮----
async def no_sleep(*_args, **_kwargs)
⋮----
client = TestClient(app)
⋮----
body = response.read().decode("utf-8")
⋮----
def test_rag_no_documents_returns_friendly_message(monkeypatch)
⋮----
def test_rag_irrelevant_retrieval_is_treated_as_no_match(monkeypatch)
⋮----
def test_feishu_file_type_download(monkeypatch, tmp_path)
⋮----
loader = FeishuDocLoader()
⋮----
downloaded_file = tmp_path / "test_doc.md"
⋮----
def fake_call_lark_api(method, path, params=None, data=None)
⋮----
result = loader.fetch_content("fake_file_token", doc_type="file")
⋮----
def test_feishu_wiki_permission_fallback_to_download(monkeypatch, tmp_path)
⋮----
downloaded_file = tmp_path / "wiki_doc.md"
⋮----
docs = loader.load_and_split(
````

## File: ai-service/tests/test_rag_retriever.py
````python
def test_retriever_add_and_search(monkeypatch)
⋮----
class FakeEmbeddings
⋮----
def embed_query(self, text)
⋮----
def embed_documents(self, texts)
⋮----
retriever = VectorStoreRetriever()
docs = [
⋮----
results = retriever.similarity_search("徒步", k=2)
⋮----
def test_retriever_storage_mode(monkeypatch)
⋮----
def test_retriever_no_dedup_in_add(monkeypatch)
⋮----
doc = Document(page_content="重复内容", metadata={"source": "test"})
⋮----
results = retriever.similarity_search("重复", k=5)
⋮----
def test_hybrid_search_uses_bm25_and_rrf_when_vector_order_is_weak(monkeypatch)
⋮----
def force_memory_store(self)
⋮----
results = retriever.hybrid_search(["炉具安全"], k=2)
````

## File: ai-service/tests/test_rag_rewriter.py
````python
def test_rewriter_returns_list_of_strings()
⋮----
rewriter = QueryRewriter()
result = rewriter.rewrite("徒步安全")
⋮----
def test_rewriter_includes_original_question()
⋮----
def test_rewriter_fallback_without_llm()
⋮----
result = rewriter.rewrite("登山装备")
⋮----
def test_rewriter_semantic_with_llm(monkeypatch)
⋮----
class FakeAIMessage
⋮----
content = '["登山需要什么装备", "户外徒步装备清单", "登山安全注意事项"]'
⋮----
class FakeChatModel
⋮----
def invoke(self, messages)
⋮----
rewriter = QueryRewriter(api_key="test-key", base_url="http://fake", model="test")
````

## File: ai-service/tests/test_reranker.py
````python
class _Response
⋮----
def __init__(self, payload)
⋮----
def raise_for_status(self)
⋮----
def json(self)
⋮----
class _Client
⋮----
def post(self, url, **kwargs)
⋮----
def test_reranker_orders_documents_and_writes_scores()
⋮----
client = _Client({
docs = [
⋮----
reranker = Reranker(
⋮----
results = reranker.rerank("query", docs)
⋮----
def test_reranker_disabled_returns_original_documents()
⋮----
reranker = Reranker(base_url="", api_key="", model="", enabled=True)
````

## File: ai-service/tests/test_retriever.py
````python
class _EmbeddingShouldNotRun
⋮----
calls = 0
⋮----
def embed_query(self, query: str)
⋮----
class _EmptyPGClient
⋮----
def __init__(self)
⋮----
def has_documents(self, status_filter=None)
⋮----
def similarity_search(self, *args, **kwargs)
⋮----
class _RecordingConnection
⋮----
def execute(self, sql, params=None)
⋮----
def fetchall(self)
⋮----
def test_pgvector_empty_status_filter_returns_without_embedding()
⋮----
embeddings = _EmbeddingShouldNotRun()
pg_client = _EmptyPGClient()
retriever = object.__new__(retriever_module.VectorStoreRetriever)
⋮----
def test_pgvector_similarity_search_filters_to_query_dimensions()
⋮----
client = object.__new__(retriever_module._PGVectorClient)
conn = _RecordingConnection()
⋮----
query_embedding = [0.1, 0.2, 0.3]
rows = client.similarity_search(query_embedding, k=2)
⋮----
def test_hybrid_search_keeps_bm25_when_pgvector_embedding_fails()
⋮----
class FailingEmbeddings
⋮----
def embed_query(self, query)
⋮----
class SearchFailingPGClient
⋮----
def similarity_search(self, query_embedding, k=4)
⋮----
def list_documents(self, status_filter=None)
⋮----
results = retriever.hybrid_search(["徒步的核心目的"], k=4, status_filter="feishu")
````

## File: ai-service/tests/test_tools_api.py
````python
def _tool_names(payload)
⋮----
def test_tools_api_lists_visible_tools_by_default()
⋮----
client = TestClient(app)
⋮----
response = client.get("/api/v1/tools")
⋮----
data = response.json()
names = _tool_names(data)
⋮----
terminal = next(item for item in data["tools"] if item["function"]["name"] == "terminal")
⋮----
terminate = next(item for item in data["tools"] if item["function"]["name"] == "terminate")
⋮----
def test_tools_api_can_include_hidden_domain_tools()
⋮----
response = client.get("/api/v1/tools?include_hidden=true")
⋮----
hiking_tool = next(
⋮----
def test_tools_health_reports_registry_and_mcp_readiness()
⋮----
response = client.get("/api/v1/tools/health")
````

## File: ai-service/tools/__init__.py
````python
__all__ = [
````

## File: ai-service/tools/file_operation.py
````python
WORKSPACE_DIR = Path("./workspace")
⋮----
def _resolve_path(path: str) -> Path
⋮----
full_path = (WORKSPACE_DIR / path).resolve()
⋮----
@tool
async def file_operation(operation: str, path: str, content: str | None = None) -> str
⋮----
resolved = _resolve_path(path)
⋮----
target = resolved if resolved.exists() else WORKSPACE_DIR
items = []
⋮----
suffix = "/" if item.is_dir() else ""
````

## File: ai-service/tools/hiking_domain.py
````python
logger = logging.getLogger("ai-service.hiking_domain")
⋮----
WORKSPACE_DIR = Path("./workspace")
⋮----
def _now_iso() -> str
⋮----
def _safe_filename(value: str, suffix: str) -> str
⋮----
stem = "".join(c if c.isalnum() or c in " _-" else "_" for c in value).strip()
stem = re.sub(r"\s+", "_", stem)[:50] or "hiking_trip"
⋮----
def _resolve_workspace_path(path: str) -> Path
⋮----
target = (WORKSPACE_DIR / path).resolve()
workspace = WORKSPACE_DIR.resolve()
⋮----
AMAP_WEATHER_URL = "https://restapi.amap.com/v3/weather/weatherInfo"
AMAP_REVERSE_GEO_URL = "https://restapi.amap.com/v3/geocode/regeo"
⋮----
WIND_DIRECTION_MAP: dict[str, str] = {
⋮----
def _parse_amap_weather(response: dict, destination: str, date: str | None) -> dict[str, Any]
⋮----
lives = response.get("lives", [])
forecasts = response.get("forecasts", [])
⋮----
live = lives[0]
⋮----
forecast_data = forecasts[0]
casts = forecast_data.get("casts", [])
forecast_list: list[dict] = []
⋮----
today = casts[0] if casts else {}
⋮----
"""查询徒步目的地的天气信息（通过高德天气 API）。
    返回实时天气或未来 4 天预报，包括温度、风力、湿度等。
    """
destination = (destination or "").strip()
adcode = (adcode or "").strip()
⋮----
geo_result = await _reverse_geocode(longitude=longitude, latitude=latitude)
⋮----
primary = geo_result.get("primary") or {}
adcode = str(primary.get("adcode") or "")
destination = str(primary.get("city") or primary.get("district") or primary.get("name") or "")
⋮----
extensions = "base" if date else "all"
params: dict[str, str] = {
⋮----
resp = await client.get(AMAP_WEATHER_URL, params=params)
⋮----
data = resp.json()
⋮----
result = _parse_amap_weather(data, destination or adcode or "当前位置", date)
⋮----
AMAP_GEO_URL = "https://restapi.amap.com/v3/geocode/geo"
⋮----
def _parse_amap_geo(response: dict, destination: str) -> dict[str, Any]
⋮----
geocodes = response.get("geocodes", [])
⋮----
candidates: list[dict] = []
⋮----
location = geo.get("location", "")
⋮----
formatted_address = geo.get("formatted_address", "")
province = geo.get("province", "")
city = geo.get("city", "")
district = geo.get("district", "")
adcode = geo.get("adcode", "")
level = geo.get("level", "")
⋮----
first = candidates[0]
terrain = "山地/丘陵可能性较高" if any(x in destination for x in ("山", "峰", "岭", "峡谷")) else "地形待核验"
⋮----
def _parse_amap_regeo(response: dict, destination: str) -> dict[str, Any]
⋮----
regeocode = response.get("regeocode") or {}
address_component = regeocode.get("addressComponent") or {}
⋮----
province = address_component.get("province", "")
city = address_component.get("city") or province
district = address_component.get("district", "")
adcode = address_component.get("adcode", "")
formatted_address = regeocode.get("formatted_address", "")
primary = {
⋮----
async def _reverse_geocode(longitude: float, latitude: float) -> dict[str, Any]
⋮----
resp = await client.get(AMAP_REVERSE_GEO_URL, params=params)
⋮----
"""查询徒步目的地的地理位置信息（通过高德地理编码 API）。
    返回坐标、行政区、城市等地理信息。
    """
⋮----
has_coordinates = latitude is not None and longitude is not None
⋮----
result = await _reverse_geocode(longitude=longitude, latitude=latitude)
⋮----
primary = result.get("primary") or {}
⋮----
resp = await client.get(AMAP_GEO_URL, params=params)
⋮----
result = _parse_amap_geo(data, destination)
⋮----
"""Build route research queries and a structured facts envelope."""
⋮----
day_text = f"{days}天" if days else ""
queries = [
⋮----
trip_days = days or 1
is_camping = bool(camping) or trip_days >= 2 or gear_level == "重装"
⋮----
items = {
⋮----
text = " ".join(x for x in [destination, weather, route, experience] if x)
reasons: list[str] = []
level = "low"
recommendation = "可以继续规划，但要补齐天气、路线和撤退点信息。"
⋮----
severe_weather = any(word in text for word in ("暴雨", "雷暴", "橙色预警", "红色预警", "大风预警"))
⋮----
level = "high"
⋮----
recommendation = "建议取消或改期，不建议进入山区、峡谷或长距离路线。"
⋮----
level = "high" if level == "high" else "medium"
⋮----
level = "medium"
⋮----
title = (title or "徒步攻略").strip()
content = content or ""
normalized_format = (format or "markdown").strip().lower()
⋮----
md_name = file_name or _safe_filename(title, ".md")
⋮----
md_path = _resolve_workspace_path(md_name)
markdown = content if content.lstrip().startswith("#") else f"
⋮----
pdf_result = await generate_pdf.ainvoke({"title": title, "content": markdown})
````

## File: ai-service/tools/hiking_knowledge.py
````python
logger = logging.getLogger("ai-service.tools.hiking_knowledge")
⋮----
def _preview(text: str, limit: int = 220) -> str
⋮----
cleaned = clean_display_text(text or "")
⋮----
def _score_from_metadata(metadata: dict[str, Any]) -> float | None
⋮----
value = metadata.get(key)
⋮----
@tool
async def hiking_knowledge_search(query: str, k: int = 4) -> dict[str, Any]
⋮----
normalized_query = (query or "").strip()
⋮----
retriever = VectorStoreRetriever()
docs = retriever.hybrid_search([normalized_query], k=k, status_filter="hiking")
⋮----
chunks = []
⋮----
metadata = doc.metadata or {}
source = metadata.get("source") or metadata.get("file_name") or "unknown"
title = metadata.get("title") or metadata.get("file_name") or source
````

## File: ai-service/tools/pdf_generation.py
````python
WORKSPACE_DIR = Path("./workspace")
⋮----
@tool
async def generate_pdf(title: str, content: str) -> str
⋮----
safe_filename = "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:50]
filepath = WORKSPACE_DIR / f"{safe_filename}.pdf"
⋮----
doc = SimpleDocTemplate(
⋮----
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
body_style = ParagraphStyle(
⋮----
elements = []
⋮----
paragraph = paragraph.strip()
````

## File: ai-service/tools/resource_download.py
````python
WORKSPACE_DIR = Path("./workspace")
⋮----
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".txt", ".md", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".csv", ".json", ".xml", ".html", ".zip"}
⋮----
@tool
async def resource_download(url: str, save_path: str | None = None) -> str
⋮----
response = await client.get(url)
⋮----
content = response.content
⋮----
filename = url.split("/")[-1].split("?")[0]
⋮----
filename = "downloaded_file"
save_path = filename
⋮----
ext = Path(save_path).suffix.lower()
⋮----
allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
⋮----
file_path = (WORKSPACE_DIR / save_path).resolve()
````

## File: ai-service/tools/risk_classifier.py
````python
class RiskLevel(str, Enum)
⋮----
LOW = "low"
MEDIUM = "medium"
HIGH = "high"
CRITICAL = "critical"
⋮----
TOOL_RISK_MAP: dict[str, RiskLevel] = {
⋮----
def classify_tool(tool_name: str, default: RiskLevel = RiskLevel.MEDIUM) -> RiskLevel
⋮----
def requires_confirmation(level: RiskLevel) -> bool
````

## File: ai-service/tools/terminal.py
````python
ALLOWED_COMMANDS = {
⋮----
BLOCKED_PATTERNS = ["rm", "sudo", "curl", "wget", "chmod", "chown", "kill", "dd", ">"]
⋮----
def _is_safe(command: str) -> tuple[bool, str]
⋮----
cmd_parts = command.strip().split()
⋮----
base_cmd = cmd_parts[0]
⋮----
# Check whitelist
⋮----
@tool
async def terminal(command: str) -> str
⋮----
"""Execute a shell command in a sandboxed environment. Only whitelisted commands are allowed.
    Allowed: ls, cat, pwd, echo, python, pip, mkdir, cp, mv, whoami, date, head, tail, wc, sort, grep, find
    Blocked: rm, sudo, curl, wget, chmod, chown, kill, dd
    """
⋮----
process = await asyncio.create_subprocess_shell(
⋮----
output = ""
````

## File: ai-service/tools/terminate.py
````python
@tool
async def terminate(reason: str = "") -> str
⋮----
"""Call this when the task is complete or cannot continue further.
    Args:
        reason: Optional reason for terminating
    """
msg = "任务已被 Agent 终止"
````

## File: ai-service/tools/tool_registry.py
````python
@dataclass
class ToolValidationResult
⋮----
valid: bool
error: str | None = None
⋮----
@dataclass
class ToolCallRequest
⋮----
name: str
args: dict[str, Any]
risk_level: RiskLevel
needs_confirmation: bool
rate_limit_remaining: int | None = None
⋮----
@property
    def requires_confirmation(self) -> bool
⋮----
@dataclass
class ToolMetadata
⋮----
description: str
parameters: dict[str, Any]
risk_level: RiskLevel | None = None
rate_limit_per_minute: int = 30
requires_confirmation: bool | None = None
needs_confirmation: bool | None = None
domain: str = "general"
scenarios: tuple[str, ...] | list[str] = field(default_factory=tuple)
auto_allowed: bool = True
result_policy: str = "raw"
hidden: bool = False
⋮----
def __post_init__(self) -> None
⋮----
class TokenBucket
⋮----
def __init__(self, capacity: int, fill_rate: float) -> None
⋮----
def _refill(self) -> None
⋮----
now = time.monotonic()
elapsed = now - self.last_refill
⋮----
def consume(self, tokens: int = 1) -> bool
⋮----
@property
    def remaining(self) -> int
⋮----
class ToolRegistry
⋮----
def __init__(self) -> None
⋮----
def register(self, metadata: ToolMetadata) -> None
⋮----
name = metadata.name
⋮----
# 按 rate_limit_per_minute 创建令牌桶（capacity = rate, fill = rate/60）
rate = metadata.rate_limit_per_minute
⋮----
def register_many(self, metadata_list: list[ToolMetadata]) -> None
⋮----
"""批量注册工具。"""
⋮----
# ── 读取 ──────────────────────────────────────────────
⋮----
def get(self, name: str) -> ToolMetadata | None
⋮----
"""按名称获取工具元数据，不存在时返回 None。"""
⋮----
def list_tools(self, include_hidden: bool = False) -> list[ToolMetadata]
⋮----
"""返回已注册工具列表。
        默认只返回基础可见工具，保持现有 API 行为；领域工具可通过
        include_hidden=True 或 get(name) 访问。
        """
⋮----
def list_all_tools(self) -> list[ToolMetadata]
⋮----
"""返回所有工具，包含按场景动态暴露的领域工具。"""
⋮----
def __contains__(self, name: str) -> bool
⋮----
def __len__(self) -> int
⋮----
# ── 验证 ──────────────────────────────────────────────
⋮----
def validate_call(self, name: str, args: dict[str, Any]) -> ToolValidationResult
⋮----
"""验证工具调用请求。
        检查：
          1. 工具是否已注册。
          2. 是否超出速率限制。
        Args:
            name: 工具名称。
            args: 调用参数（当前仅做格式检查，可通过自定义 validator 扩展）。
        Returns:
            ToolValidationResult，包含验证通过/失败状态和错误信息。
        """
md = self._tools.get(name)
⋮----
# 检查速率限制
bucket = self._buckets.get(name)
⋮----
remaining_sec = int(
⋮----
def get_risk_level(self, name: str) -> RiskLevel
⋮----
def needs_confirmation(self, name: str) -> bool
⋮----
def get_call_request(self, name: str, args: dict[str, Any]) -> ToolCallRequest | None
⋮----
remaining = bucket.remaining if bucket else None
⋮----
def tools_api_response(self, include_hidden: bool = False) -> list[dict[str, Any]]
⋮----
result = []
````

## File: ai-service/tools/web_scraping.py
````python
@tool
async def web_scraping(url: str) -> str
⋮----
headers = {
response = await client.get(url, headers=headers)
⋮----
soup = BeautifulSoup(response.text, "lxml")
⋮----
main = soup.find("main") or soup.find("article") or soup.find("body")
⋮----
text = main.get_text(separator="\n", strip=True)
⋮----
text = soup.get_text(separator="\n", strip=True)
⋮----
lines = [line.strip() for line in text.split("\n") if line.strip()]
content = "\n".join(lines[:200])
````

## File: ai-service/tools/web_search.py
````python
@tool
async def web_search(query: str) -> str
⋮----
url = "https://api.duckduckgo.com/"
params = {"q": query, "format": "json", "no_html": 1, "skip_disambig": 1}
⋮----
response = await client.get(url, params=params)
data = response.json()
⋮----
abstract = data.get("AbstractText", "")
source = data.get("AbstractSource", "")
heading = data.get("Heading", "")
⋮----
result = f"标题: {heading}\n来源: {source}\n摘要: {abstract}"
⋮----
# Fallback to related topics
topics = data.get("RelatedTopics", [])
results = []
⋮----
result = "\n".join(results) if results else f"未找到关于「{query}」的明确结果。"
````

## File: docker-compose.yml
````yaml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg16
    container_name: ai-hiking-postgres
    ports:
      - "5432:5432"
    environment:
      POSTGRES_DB: ai_hiking
      POSTGRES_USER: ai_hiking
      POSTGRES_PASSWORD: ai_hiking
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ai_hiking"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - ai-hiking-net
  redis:
    image: redis:7-alpine
    container_name: ai-hiking-redis
    ports:
      - "5379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - ai-hiking-net
volumes:
  pgdata:
  redis-data:
networks:
  ai-hiking-net:
    driver: bridge
````

## File: frontend/index.html
````html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <title>ai-hiking - AI Agent 系统</title>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.tsx"></script>
</body>
</html>
````

## File: frontend/package.json
````json
{
  "name": "ai-hiking-frontend",
  "private": true,
  "version": "0.0.1",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "node --test tests/*.test.mjs",
    "preview": "vite preview"
  },
  "dependencies": {
    "lucide-react": "^1.16.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.26.0"
  },
  "devDependencies": {
    "@types/react": "^18.3.3",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.1",
    "autoprefixer": "^10.5.0",
    "postcss": "^8.5.14",
    "tailwindcss": "^3.4.19",
    "typescript": "^5.5.3",
    "vite": "^5.4.0"
  }
}
````

## File: frontend/postcss.config.cjs
````javascript

````

## File: frontend/public/favicon.svg
````xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="12" fill="#1a3c2a"/>
  <path d="M10 48 25 20l8 15 6-10 15 23H10Z" fill="#f5f5f0"/>
  <path d="M25 20 33 35l-5-2-4 5-4-5-6 3 11-16Z" fill="#9bd3ad"/>
</svg>
````

## File: frontend/src/api/config.ts
````typescript

````

## File: frontend/src/api/conversationMemory.ts
````typescript
export type ConversationMemoryLevel = 'empty' | 'steady' | 'high' | 'full'
⋮----
export interface ConversationMemoryProgress {
  used: number
  capacity: number
  percent: number
  level: ConversationMemoryLevel
  label: string
}
⋮----
function clamp(value: number, min: number, max: number)
⋮----
export function getConversationMemoryProgress(
  messages: readonly unknown[],
  capacity = CONVERSATION_MEMORY_WINDOW,
): ConversationMemoryProgress
````

## File: frontend/src/api/llmConfig.ts
````typescript
import { API } from './config'
⋮----
export type ModelProvider = 'openai-compatible'
⋮----
export interface LlmModelConfig {
  provider: ModelProvider
  baseUrl: string
  apiKey: string
  model: string
}
⋮----
export interface EmbeddingModelConfig {
  provider: ModelProvider
  baseUrl: string
  apiKey: string
  model: string
  dimensions: number
}
⋮----
export interface RerankModelConfig {
  provider: ModelProvider
  baseUrl: string
  apiKey: string
  model: string
}
⋮----
export interface LlmSettings {
  llm: LlmModelConfig
  embedding: EmbeddingModelConfig
  rerank: RerankModelConfig
  updatedAt: string | null
}
⋮----
interface StorageLike {
  getItem(key: string): string | null
  setItem(key: string, value: string): void
  removeItem(key: string): void
}
⋮----
getItem(key: string): string | null
setItem(key: string, value: string): void
removeItem(key: string): void
⋮----
function browserStorage(): StorageLike | null
⋮----
function isRecord(value: unknown): value is Record<string, unknown>
⋮----
function normalizeProvider(value: unknown, fallback: ModelProvider): ModelProvider
⋮----
function normalizeText(value: unknown, fallback: string): string
⋮----
function normalizeSecret(value: unknown): string
⋮----
function normalizeNumber(value: unknown, fallback: number, min: number, max: number): number
⋮----
export function normalizeLlmSettings(value: unknown): LlmSettings
⋮----
export function loadLlmSettings(storage: StorageLike | null = browserStorage()): LlmSettings
⋮----
export function saveLlmSettings(value: unknown, storage: StorageLike | null = browserStorage()): LlmSettings
⋮----
export function clearLlmSettings(storage: StorageLike | null = browserStorage()): LlmSettings
⋮----
export function maskApiKey(value: string): string
⋮----
export interface ModelInfo {
  id: string
  object?: string
  created?: number
  owned_by?: string
  type?: string
  modality?: string
  capabilities?: string[]
  architecture?: {
    modality?: string
    input_modalities?: string[]
    output_modalities?: string[]
    type?: string
  }
}
⋮----
export interface ModelsResponse {
  object?: string
  data?: ModelInfo[]
  models?: string[]
}
⋮----
export interface SpeedTestMeasurement {
  latencyMs: number
  modelCount: number
}
⋮----
export type ModelUsage = 'llm' | 'embedding' | 'rerank'
type InferredModelUsage = ModelUsage | 'other' | 'unknown'
⋮----
export interface RuntimeModelSettingsPayload {
  llm?: {
    base_url: string
    api_key: string
    model: string
  }
  embedding?: {
    base_url: string
    api_key: string
    model: string
    dimensions: number
  }
  rerank?: {
    base_url: string
    api_key: string
    model: string
  }
}
⋮----
export interface RagQueryPayload {
  question: string
  status: string | null
  model_settings?: RuntimeModelSettingsPayload
}
⋮----
export function filterModelList(models: ModelInfo[], query: string): ModelInfo[]
⋮----
function collectModelHints(model: ModelInfo): string
⋮----
function inferModelUsageFromHints(hints: string, fallback: 'llm' | 'unknown'): InferredModelUsage
⋮----
function inferModelUsage(model: ModelInfo): ModelUsage | 'other'
⋮----
export function filterModelsByUsage(models: ModelInfo[], usage: ModelUsage): ModelInfo[]
⋮----
function sanitizeStoredModel(model: string, usage: ModelUsage, fallback: string): string
⋮----
export function repairModelSelection(
  currentModel: string,
  usage: ModelUsage,
  candidates: ModelInfo[],
): string
⋮----
type FetchLike = (input: RequestInfo | URL, init?: RequestInit) => Promise<Response>
⋮----
function defaultFetch(): FetchLike
⋮----
function defaultNow(): number
⋮----
export function canRunSpeedTest(baseUrl: string, apiKey: string): boolean
⋮----
function hasRunnableModelConfig(config:
⋮----
export function buildRuntimeModelSettings(settings: LlmSettings = loadLlmSettings()): RuntimeModelSettingsPayload
⋮----
export function buildRagQueryPayload(
  question: string,
  status: string | null,
  settings: LlmSettings = loadLlmSettings(),
): RagQueryPayload
⋮----
export async function fetchModels(
  baseUrl: string,
  apiKey: string,
  fetcher: FetchLike = defaultFetch(),
): Promise<ModelInfo[]>
⋮----
export async function measureModelLatency(
  baseUrl: string,
  apiKey: string,
  options: {
    fetcher?: FetchLike
    now?: () => number
  } = {},
): Promise<SpeedTestMeasurement>
````

## File: frontend/src/api/ragStream.ts
````typescript
export interface RagSourceDocument {
  title: string
  source: string
  content: string
  chunks?: number
  token?: string
  docType?: string
}
⋮----
export interface RagSearchSummary {
  searchedCount: number
  matchedChunks: number
  documents: RagSourceDocument[]
}
⋮----
export interface RagStreamState {
  content: string
  processSteps: string[]
  searchSummary: RagSearchSummary | null
}
⋮----
export interface RagStreamEventLike {
  type: string
  content: string
  metadata?: Record<string, unknown>
}
⋮----
export function createEmptyRagStreamState(): RagStreamState
⋮----
function toNumber(value: unknown, fallback = 0): number
⋮----
function toText(value: unknown, fallback = ''): string
⋮----
function normalizeDocuments(value: unknown): RagSourceDocument[]
⋮----
function normalizeSearchSummary(metadata: Record<string, unknown> | undefined): RagSearchSummary | null
⋮----
export function applyRagStreamEvent(
  state: RagStreamState,
  event: RagStreamEventLike,
): RagStreamState
````

## File: frontend/src/api/sse.ts
````typescript
export interface SSEEvent {
  type: 'thought' | 'process' | 'documents' | 'tool_call' | 'tool_result' | 'approval_required' | 'artifact' | 'text' | 'done' | 'error'
  content: string
  metadata?: Record<string, unknown>
}
⋮----
export interface StreamHandlers {
  onMessage: (event: SSEEvent) => void
  onError: (error: string) => void
  onOpen?: () => void
  onDone?: () => void
}
⋮----
export interface CreateStreamOptions {
  method?: string
  body?: string
  onMessage: (event: SSEEvent) => void
  onError: (error: string) => void
  onOpen?: () => void
  onDone?: () => void
}
⋮----
function parseSSELine(line: string): SSEEvent | null
⋮----
async function responseErrorMessage(response: Response)
⋮----
export async function createStreamConnection(
  url: string,
  options: CreateStreamOptions
): Promise<() => void>
⋮----
const cleanup = () =>
⋮----
export function createSSEConnection(
  url: string,
  handlers: StreamHandlers
): () => void
⋮----
function connect()
````

## File: frontend/src/App.css
````css
:root {
⋮----
* {
⋮----
body {
⋮----
.app-layout {
⋮----
.sidebar {
⋮----
.sidebar-brand {
⋮----
.sidebar-brand-icon {
⋮----
.sidebar-brand-icon svg {
⋮----
.sidebar-brand-text {
⋮----
.sidebar-nav {
⋮----
.sidebar-nav-item {
⋮----
.sidebar-nav-item:hover {
⋮----
.sidebar-nav-item.active {
⋮----
.sidebar-nav-item:active {
⋮----
.sidebar-nav-icon {
⋮----
.sidebar-nav-icon svg {
⋮----
.sidebar-decoration {
⋮----
.main-wrapper {
⋮----
.top-header {
⋮----
.header-title {
⋮----
.header-actions {
⋮----
.header-icon-btn {
⋮----
.header-icon-btn:hover {
⋮----
.header-icon-btn:active {
⋮----
.header-icon-btn svg {
⋮----
.header-avatar {
⋮----
.header-avatar svg {
⋮----
.page-content {
⋮----
.home-hero {
⋮----
.home-hero h1 {
⋮----
.home-hero p {
⋮----
.module-cards {
⋮----
.module-card {
⋮----
.module-card:hover {
⋮----
.module-card-header {
⋮----
.module-card-icon {
⋮----
.module-card:hover .module-card-icon {
⋮----
.module-card-icon svg {
⋮----
.module-card-title {
⋮----
.module-card-badge {
⋮----
.module-card-desc {
⋮----
.module-card-btn {
⋮----
.module-card-btn:hover {
⋮----
.module-card-btn:active {
⋮----
.module-card-btn svg {
⋮----
.module-card-btn:hover svg {
⋮----
.recent-chats {
⋮----
.recent-chats-header {
⋮----
.recent-chats-title {
⋮----
.recent-chats-title svg {
⋮----
.recent-chats-more {
⋮----
.recent-chats-more:hover {
⋮----
.recent-chat-item {
⋮----
.recent-chat-item:last-child {
⋮----
.recent-chat-item:hover {
⋮----
.recent-chat-item:active {
⋮----
.recent-chat-left {
⋮----
.recent-chat-icon {
⋮----
.recent-chat-item:hover .recent-chat-icon {
⋮----
.recent-chat-icon svg {
⋮----
.recent-chat-text {
⋮----
.recent-chat-right {
⋮----
.chat-page-wrapper {
⋮----
.chat-page-header {
⋮----
.chat-page-header h2 {
⋮----
.chat-page-header p {
⋮----
.chat-main {
⋮----
.chat-messages-area {
⋮----
.chat-sidebar-right {
⋮----
.welcome-card {
⋮----
.welcome-card:hover {
⋮----
.welcome-card-icon {
⋮----
.welcome-card:hover .welcome-card-icon {
⋮----
.welcome-card-icon svg {
⋮----
.welcome-card-content h4 {
⋮----
.welcome-card-content p {
⋮----
.message-list {
⋮----
.message-row {
⋮----
.message-row.user {
⋮----
.message-avatar {
⋮----
.message-avatar:hover {
⋮----
.message-avatar svg {
⋮----
.message-row.user .message-avatar {
⋮----
.message-bubble {
⋮----
.message-bubble:hover {
⋮----
.message-row.assistant .message-bubble {
⋮----
.message-row.user .message-bubble {
⋮----
.message-time {
⋮----
.chat-input-wrapper {
⋮----
.chat-input-box {
⋮----
.chat-input-box:focus-within {
⋮----
.chat-input-box input {
⋮----
.chat-input-box input::placeholder {
⋮----
.chat-input-actions {
⋮----
.chat-image-btn {
⋮----
.chat-image-btn:hover {
⋮----
.chat-image-btn:active {
⋮----
.chat-image-btn svg {
⋮----
.chat-send-btn {
⋮----
.chat-send-btn:hover {
⋮----
.chat-send-btn:active {
⋮----
.chat-send-btn:disabled {
⋮----
.chat-send-btn svg {
⋮----
.quick-tags {
⋮----
.quick-tag {
⋮----
.quick-tag:hover {
⋮----
.quick-tag:active {
⋮----
.quick-tag svg {
⋮----
.itinerary-panel h3 {
⋮----
.itinerary-stat {
⋮----
.itinerary-stat:hover {
⋮----
.itinerary-stat-icon {
⋮----
.itinerary-stat:hover .itinerary-stat-icon {
⋮----
.itinerary-stat-icon svg {
⋮----
.itinerary-stat-label {
⋮----
.itinerary-stat-value {
⋮----
.itinerary-detail-link {
⋮----
.itinerary-detail-link:hover {
⋮----
.equipment-card {
⋮----
.equipment-card h4 {
⋮----
.equipment-card p {
⋮----
.day-itinerary {
⋮----
.day-itinerary-item {
⋮----
.day-itinerary-item strong {
⋮----
.day-itinerary-item p {
⋮----
.message-actions-row {
⋮----
.message-action-btn {
⋮----
.message-action-btn:hover {
⋮----
.message-action-btn:active {
⋮----
.message-action-btn svg {
⋮----
.typing-indicator {
⋮----
.loading-dots {
⋮----
.loading-dots span {
⋮----
.loading-dots span:nth-child(1) { animation-delay: -0.32s; }
.loading-dots span:nth-child(2) { animation-delay: -0.16s; }
⋮----
::-webkit-scrollbar {
⋮----
::-webkit-scrollbar-track {
⋮----
::-webkit-scrollbar-thumb {
⋮----
::-webkit-scrollbar-thumb:hover {
⋮----
*,
````

## File: frontend/src/App.tsx
````typescript
import { Routes, Route, NavLink, useLocation } from 'react-router-dom'
import {
  Mountain,
  Home,
  Search,
  Bot,
} from 'lucide-react'
import HomePage from './pages/Home'
import LoveMaster from './pages/LoveMaster'
import SuperAgent from './pages/SuperAgent'
import LlmConfig from './pages/LlmConfig'
⋮----
function App()
⋮----
const getHeaderTitle = () =>
⋮----
<NavLink
            to="/love-master"
className=
⋮----
<NavLink
            to="/super-agent"
className=
````

## File: frontend/src/components/AiAvatar.tsx
````typescript
import { Heart, Bot } from 'lucide-react'
⋮----
interface AiAvatarProps {
  type: 'love' | 'agent'
  size?: number
}
⋮----
function AiAvatar(
````

## File: frontend/src/components/ChatRoom.tsx
````typescript
import { useState, useRef, useEffect, useCallback } from 'react'
import AiAvatar from './AiAvatar'
import ConnectionStatus from './ConnectionStatus'
import { createStreamConnection, SSEEvent } from '../api/sse'
⋮----
interface Message {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}
⋮----
interface ChatRoomProps {
  apiEndpoint: string
  sseEndpoint: string
  healthEndpoint: string
  aiName: string
  aiAvatar: 'love' | 'agent'
}
⋮----
type ConnectionState = 'disconnected' | 'connected' | 'error'
type HealthPayload = Record<string, unknown>
⋮----
function isHealthPayload(payload: HealthPayload | string | null): payload is HealthPayload
⋮----
function payloadMessage(payload: HealthPayload | string | null): string
⋮----
async function readResponsePayload(response: Response): Promise<HealthPayload | string | null>
⋮----
function responseErrorMessage(response: Response, payload: HealthPayload | string | null): string
⋮----
function formatConnectionError(error: unknown): string
⋮----
function alertDedupeKey(aiName: string, reason: string): string
⋮----
function AiThinking()
⋮----
// Save messages to localStorage
⋮----
// Ignore storage errors
⋮----
// Auto scroll to bottom
⋮----
const handleKeyDown = (e: React.KeyboardEvent) =>
⋮----
const handleClear = () =>
⋮----
onChange=
````

## File: frontend/src/components/ConnectionStatus.tsx
````typescript
interface ConnectionStatusProps {
  status: 'disconnected' | 'connected' | 'error'
}
⋮----
function ConnectionStatus(
````

## File: frontend/src/components/ConversationMemoryMeter.tsx
````typescript
import { Database } from 'lucide-react'
import { getConversationMemoryProgress } from '../api/conversationMemory'
⋮----
interface ConversationMemoryMeterProps {
  messages: readonly unknown[]
}
⋮----
function ConversationMemoryMeter(
````

## File: frontend/src/index.css
````css
@tailwind base;
@tailwind components;
@tailwind utilities;
⋮----
:root {
⋮----
@layer base {
⋮----
body {
⋮----
.typing-indicator {
⋮----
.loading-dots {
⋮----
.loading-dots span {
⋮----
.loading-dots span:nth-child(1) {
⋮----
.loading-dots span:nth-child(2) {
⋮----
.ai-thinking {
⋮----
.ai-thinking-core {
⋮----
.ai-thinking-core span {
⋮----
.ai-thinking-core span:nth-child(2) {
⋮----
.ai-thinking-core span:nth-child(3) {
⋮----
.ai-thinking-line {
⋮----
.ai-thinking-line::after {
⋮----
.ai-thinking-label {
⋮----
.conversation-memory-meter {
⋮----
.conversation-memory-meter-label {
⋮----
.conversation-memory-meter-track {
⋮----
.conversation-memory-meter-fill {
⋮----
.conversation-memory-meter[data-level="empty"] .conversation-memory-meter-fill {
⋮----
.conversation-memory-meter[data-level="high"] .conversation-memory-meter-fill {
⋮----
.conversation-memory-meter[data-level="full"] .conversation-memory-meter-fill {
⋮----
.conversation-memory-meter-value {
⋮----
.t-panel-slide {
.t-panel-slide[data-open="true"] {
⋮----
.t-icon-swap {
.t-icon-swap .t-icon {
.t-icon-swap[data-state="a"] .t-icon[data-icon="a"],
.t-icon-swap[data-state="a"] .t-icon[data-icon="b"],
⋮----
.chat-sidebar {
.chat-sidebar[data-open="false"] {
.chat-sidebar-inner {
.chat-sidebar[data-open="false"] .chat-sidebar-inner {
⋮----
@layer utilities {
⋮----
.scrollbar-thin::-webkit-scrollbar {
.scrollbar-thin::-webkit-scrollbar-track {
.scrollbar-thin::-webkit-scrollbar-thumb {
.scrollbar-thin::-webkit-scrollbar-thumb:hover {
⋮----
.stagger-1 { animation-delay: 0ms; }
.stagger-2 { animation-delay: 50ms; }
.stagger-3 { animation-delay: 100ms; }
.stagger-4 { animation-delay: 150ms; }
.stagger-5 { animation-delay: 200ms; }
.stagger-6 { animation-delay: 250ms; }
⋮----
*,
⋮----
.t-panel-slide,
````

## File: frontend/src/main.tsx
````typescript
import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
````

## File: frontend/src/pages/Home.tsx
````typescript
import { Link } from 'react-router-dom'
import { Search, Bot, ArrowRight } from 'lucide-react'
````

## File: frontend/src/pages/LlmConfig.tsx
````typescript
import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  Brain,
  ChevronDown,
  Database,
  Gauge,
  KeyRound,
  ListFilter,
  Loader2,
  RefreshCw,
  RotateCcw,
  Save,
  Server,
  Settings2,
  SlidersHorizontal,
} from 'lucide-react'
import {
  clearLlmSettings,
  DEFAULT_LLM_SETTINGS,
  EmbeddingModelConfig,
  canRunSpeedTest,
  filterModelList,
  filterModelsByUsage,
  fetchModels,
  LlmModelConfig,
  LlmSettings,
  loadLlmSettings,
  maskApiKey,
  measureModelLatency,
  ModelInfo,
  ModelUsage,
  repairModelSelection,
  RerankModelConfig,
  saveLlmSettings,
} from '../api/llmConfig'
⋮----
type SpeedTestStatus = 'idle' | 'testing' | 'success' | 'error' | 'skipped'
⋮----
interface SpeedTestState {
  status: SpeedTestStatus
  latencyMs: number | null
  modelCount: number | null
  message: string
  testedAt: string | null
}
⋮----
function formatTimestamp(value: string | null, fallback: string)
⋮----
function createIdleSpeedState(): SpeedTestState
⋮----
function createTestingSpeedState(): SpeedTestState
⋮----
function createSkippedSpeedState(reason: string): SpeedTestState
⋮----
function createIdleSpeedTests(): Record<ModelUsage, SpeedTestState>
⋮----
function createTestingSpeedTests(): Record<ModelUsage, SpeedTestState>
⋮----
function speedStatusLabel(status: SpeedTestStatus)
⋮----
function usageLabel(usage: ModelUsage): string
⋮----
function speedStatusClassName(status: SpeedTestStatus)
⋮----
const handleSelect = (modelId: string) =>
⋮----
const updateLlm = <K extends keyof LlmModelConfig>(field: K, value: LlmModelConfig[K]) =>
⋮----
const updateEmbedding = <K extends keyof EmbeddingModelConfig>(field: K, value: EmbeddingModelConfig[K]) =>
⋮----
const updateRerank = <K extends keyof RerankModelConfig>(field: K, value: RerankModelConfig[K]) =>
⋮----
const handleSave = async () =>
⋮----
const handleReset = () =>
⋮----
{/* Header */}
⋮----
{/* Summary Cards */}
````

## File: frontend/src/pages/LoveMaster.tsx
````typescript
import { useState, useRef, useEffect, useCallback } from 'react'
import { Mountain, User, BookOpen, Send, Backpack, Tent, CloudSun, ThumbsUp, ThumbsDown, Upload, MessageSquare, Trash2, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import { API } from '../api/config'
import { createStreamConnection, SSEEvent } from '../api/sse'
import { buildRagQueryPayload, buildRuntimeModelSettings } from '../api/llmConfig'
import { applyRagStreamEvent, RagSearchSummary } from '../api/ragStream'
import ConversationMemoryMeter from '../components/ConversationMemoryMeter'
⋮----
interface Message {
  role: 'user' | 'assistant'
  content: string
  time?: string
  isStreaming?: boolean
  processSteps?: string[]
  searchSummary?: RagSearchSummary | null
}
⋮----
interface ChatSession {
  id: string
  title: string
  date: string
  messages: Message[]
}
⋮----
function generateId()
⋮----
function getTodayDate()
⋮----
function sourceLabel(source: string)
⋮----
function loadSessions(): ChatSession[]
⋮----
function saveSessions(sessions: ChatSession[])
⋮----
function AiThinking()
⋮----
try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
⋮----
try { localStorage.setItem(STORAGE_KEY, JSON.stringify(session.messages)) } catch { /* ignore */ }
⋮----
try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
⋮----
const handleKeyDown = (e: React.KeyboardEvent) =>
⋮----
const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) =>
⋮----
// Reset input so same file can be re-uploaded
⋮----
const handleClear = () =>
⋮----
try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
⋮----
{/* Left Sidebar - Chat History */}
⋮----
onClick=
⋮----
{/* Main Chat Area */}
⋮----
{/* Header */}
⋮----
{/* Messages Area */}
⋮----
来源：
⋮----
onChange=
````

## File: frontend/src/pages/SuperAgent.tsx
````typescript
import { useState, useRef, useEffect, useCallback, useMemo } from 'react'
import {
  Mountain,
  User,
  Flag,
  Send,
  Image,
  ClipboardList,
  CheckCircle2,
  AlertTriangle,
  Map,
  ThumbsUp,
  ThumbsDown,
  MessageSquare,
  Trash2,
  PanelLeftClose,
  PanelLeftOpen,
} from 'lucide-react'
import { API } from '../api/config'
import { buildRuntimeModelSettings } from '../api/llmConfig'
import { createStreamConnection, SSEEvent } from '../api/sse'
import ConversationMemoryMeter from '../components/ConversationMemoryMeter'
⋮----
interface Message {
  role: 'user' | 'assistant'
  content: string
  time?: string
  isStreaming?: boolean
  traceEvents?: AgentTraceEvent[]
  artifacts?: AgentArtifact[]
}
⋮----
interface ChatSession {
  id: string
  title: string
  date: string
  messages: Message[]
}
⋮----
type AgentScenario = 'route_plan' | 'gear_check' | 'risk_assessment' | 'report_export'
type AgentTraceEvent = Pick<SSEEvent, 'type' | 'content' | 'metadata'>
type AgentArtifact = Pick<SSEEvent, 'content' | 'metadata'>
type BrowserLocation = {
  latitude: number
  longitude: number
  accuracy?: number
  source: 'browser'
}
⋮----
function shouldRequestCurrentLocation(text: string)
⋮----
function createChatId()
⋮----
function getOrCreateChatId()
⋮----
function generateId()
⋮----
function getTodayDate()
⋮----
function loadSessions(): ChatSession[]
⋮----
function saveSessions(sessions: ChatSession[])
⋮----
function getBrowserLocation(timeout = 3000): Promise<BrowserLocation | null>
⋮----
function AiThinking()
⋮----
try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
⋮----
try { localStorage.setItem(STORAGE_KEY, JSON.stringify(session.messages)) } catch { /* ignore */ }
⋮----
try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
⋮----
const handleKeyDown = (e: React.KeyboardEvent) =>
⋮----
const handleClear = () =>
⋮----
} catch { /* ignore */ }
⋮----
{/* Left Sidebar - Chat History */}
⋮----
onClick=
⋮----
{/* Main Chat Area */}
⋮----
{/* Header */}
⋮----
{/* Messages Area */}
⋮----
{/* Scrollable messages */}
⋮----
{/* Input */}
⋮----
setInput(e.target.value)
setSelectedScenario(null)
⋮----
setInput(tag.text)
setSelectedScenario(tag.scenario)
````

## File: frontend/src/vite-env.d.ts
````typescript

````

## File: frontend/tailwind.config.cjs
````javascript
/** @type {import('tailwindcss').Config} */
````

## File: frontend/tests/appLayout.test.mjs
````javascript

````

## File: frontend/tests/conversationMemory.test.mjs
````javascript
async function loadConversationMemoryModule()
````

## File: frontend/tests/llmConfig.test.mjs
````javascript
async function loadConfigModule()
⋮----
// Replace the import with inline config
⋮----
function createMemoryStorage(initial =
⋮----
getItem: (key)
setItem: (key, value)
removeItem: (key)
⋮----
fetcher: async (input, init) =>
⋮----
json: async () => (
````

## File: frontend/tests/ragStream.test.mjs
````javascript
async function loadRagStreamModule()
````

## File: frontend/tests/superAgent.test.mjs
````javascript

````

## File: frontend/tests/thinkingAnimation.test.mjs
````javascript

````

## File: frontend/tsconfig.json
````json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
````

## File: frontend/tsconfig.node.json
````json
{
  "compilerOptions": {
    "composite": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "allowSyntheticDefaultImports": true
  },
  "include": ["vite.config.ts"]
}
````

## File: frontend/vite.config.ts
````typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
````

## File: gateway/.omc/state/hud-stdin-cache.json
````json
{"session_id":"b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27","transcript_path":"C:\\Users\\14253\\.claude\\projects\\C--Users-14253-Desktop-ai-hiking\\b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27.jsonl","cwd":"C:\\Users\\14253\\Desktop\\ai-hiking\\gateway","effort":{"level":"max"},"session_name":"feishu-rag-sync","model":{"id":"deepseek-v4-pro[1m]","display_name":"deepseek-v4-pro[1m]"},"workspace":{"current_dir":"C:\\Users\\14253\\Desktop\\ai-hiking\\gateway","project_dir":"C:\\Users\\14253\\Desktop\\ai-hiking","added_dirs":[]},"version":"2.1.143","output_style":{"name":"default"},"cost":{"total_cost_usd":4.910549,"total_duration_ms":2328735,"total_api_duration_ms":1225037,"total_lines_added":384,"total_lines_removed":121},"context_window":{"total_input_tokens":118105,"total_output_tokens":671,"context_window_size":1000000,"current_usage":{"input_tokens":217,"output_tokens":671,"cache_creation_input_tokens":0,"cache_read_input_tokens":117888},"used_percentage":12,"remaining_percentage":88},"exceeds_200k_tokens":false,"fast_mode":false,"thinking":{"enabled":true}}
````

## File: gateway/.omc/state/last-tool-error.json
````json
{
  "tool_name": "Bash",
  "tool_input_preview": "{\"command\":\"cd \\\"C:/Users/14253/Desktop/ai-hiking/ai-service\\\" && OPENAI_API_KEY=test python -c \\\"\\nimport sys\\nsys.path.insert(0, '.')\\n\\n# 1. Config verification\\nfrom config import settings\\nprint(...",
  "error": "Exit code 1\nTraceback (most recent call last):\r\n  File \"C:\\Users\\14253\\Desktop\\ai-hiking\\ai-service\\rag\\feishu.py\", line 46, in _run_lark_cli\r\n    result = subprocess.run(\r\n        cmd,\r\n    ...<3 lines>...\r\n        encoding=\"utf-8\",\r\n    )\r\n  File \"E:\\miniconda3\\Lib\\subprocess.py\", line 554, in run\r\n    with Popen(*popenargs, **kwargs) as process:\r\n         ~~~~~^^^^^^^^^^^^^^^^^^^^^^\r\n  File \"E:\\miniconda3\\Lib\\subprocess.py\", line 1039, in __init__\r\n    self._execute_child(args, executable, pr...",
  "timestamp": "2026-05-16T09:26:44.188Z",
  "retry_count": 1
}
````

## File: gateway/.omc/state/sessions/b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27/hud-state.json
````json
{
  "timestamp": "2026-05-16T09:25:23.523Z",
  "backgroundTasks": [],
  "sessionStartTimestamp": "2026-05-16T08:49:32.702Z",
  "sessionId": "b0fc1b59-b3c2-4835-8a6a-0f9f258f2c27"
}
````

## File: gateway/config/config_test.go
````go
package config
⋮----
import (
	"os"
	"testing"
)
⋮----
"os"
"testing"
⋮----
func TestLoadDefaults(t *testing.T)
⋮----
func TestLoadFromEnv(t *testing.T)
⋮----
func TestGetEnvWithFallback(t *testing.T)
⋮----
func TestGetEnvWithValue(t *testing.T)
⋮----
func TestGetEnvEmptyValueUsesFallback(t *testing.T)
````

## File: gateway/config/config.go
````go
package config
⋮----
import "os"
⋮----
type Config struct {
	Port           string
	AIServiceURL   string
	AllowedOrigins string
}
⋮----
func Load() *Config
⋮----
func getEnv(key, fallback string) string
````

## File: gateway/go.mod
````
module github.com/ai-hiking/gateway

go 1.22

require (
	github.com/gin-contrib/cors v1.7.2
	github.com/gin-gonic/gin v1.10.0
)

require (
	github.com/bytedance/sonic v1.11.6 // indirect
	github.com/bytedance/sonic/loader v0.1.1 // indirect
	github.com/cloudwego/base64x v0.1.4 // indirect
	github.com/cloudwego/iasm v0.2.0 // indirect
	github.com/gabriel-vasile/mimetype v1.4.3 // indirect
	github.com/gin-contrib/sse v0.1.0 // indirect
	github.com/go-playground/locales v0.14.1 // indirect
	github.com/go-playground/universal-translator v0.18.1 // indirect
	github.com/go-playground/validator/v10 v10.20.0 // indirect
	github.com/goccy/go-json v0.10.2 // indirect
	github.com/json-iterator/go v1.1.12 // indirect
	github.com/klauspost/cpuid/v2 v2.2.7 // indirect
	github.com/kr/text v0.2.0 // indirect
	github.com/leodido/go-urn v1.4.0 // indirect
	github.com/mattn/go-isatty v0.0.20 // indirect
	github.com/modern-go/concurrent v0.0.0-20180306012644-bacd9c7ef1dd // indirect
	github.com/modern-go/reflect2 v1.0.2 // indirect
	github.com/pelletier/go-toml/v2 v2.2.2 // indirect
	github.com/twitchyliquid64/golang-asm v0.15.1 // indirect
	github.com/ugorji/go/codec v1.2.12 // indirect
	golang.org/x/arch v0.8.0 // indirect
	golang.org/x/crypto v0.23.0 // indirect
	golang.org/x/net v0.25.0 // indirect
	golang.org/x/sys v0.20.0 // indirect
	golang.org/x/text v0.15.0 // indirect
	google.golang.org/protobuf v1.34.1 // indirect
	gopkg.in/yaml.v3 v3.0.1 // indirect
)
````

## File: gateway/handler/chat_test.go
````go
package handler
⋮----
import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"encoding/json"
"net/http"
"net/http/httptest"
"strings"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestChatSyncProxiesToAIService(t *testing.T)
⋮----
func TestChatSyncAIUnreachable(t *testing.T)
⋮----
func TestChatSSEWithQueryParam(t *testing.T)
⋮----
func TestChatSSEWithPostBody(t *testing.T)
⋮----
var body map[string]any
⋮----
func TestChatSSEMissingMessage(t *testing.T)
⋮----
func TestChatHistoryProxiesToAIService(t *testing.T)
⋮----
func TestChatHealthReturnsOk(t *testing.T)
⋮----
func TestChatHealthFallsBackToGeneralHealth(t *testing.T)
⋮----
var body map[string]string
⋮----
func TestChatHealthBothEndpointsUnreachable(t *testing.T)
⋮----
func TestNewChatHandler(t *testing.T)
````

## File: gateway/handler/chat.go
````go
package handler
⋮----
import (
	"bufio"
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"github.com/gin-gonic/gin"
)
⋮----
"bufio"
"bytes"
"encoding/json"
"fmt"
"io"
"net/http"
⋮----
"github.com/gin-gonic/gin"
⋮----
type ChatHandler struct {
	aiServiceURL string
}
⋮----
func NewChatHandler(aiServiceURL string) *ChatHandler
⋮----
func (h *ChatHandler) ChatSync(c *gin.Context)
⋮----
func (h *ChatHandler) ChatHealth(c *gin.Context)
⋮----
func (h *ChatHandler) ChatSSE(c *gin.Context)
⋮----
var requestBody io.Reader
⋮----
var req map[string]any
⋮----
func (h *ChatHandler) ChatHistory(c *gin.Context)
⋮----
func proxyRequest(c *gin.Context, method, url string, body io.Reader)
⋮----
func proxyStreamRequest(c *gin.Context, method, url string, body io.Reader, contentType string)
⋮----
func proxyHealthRequest(c *gin.Context, module, url, fallbackURL string)
````

## File: gateway/handler/health_test.go
````go
package handler
⋮----
import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"encoding/json"
"net/http"
"net/http/httptest"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestHealthHandlerReturnsOk(t *testing.T)
⋮----
var body map[string]string
⋮----
func TestHealthHandlerAIUnreachable(t *testing.T)
⋮----
func TestHealthHandlerAIError(t *testing.T)
⋮----
func TestNewHealthHandler(t *testing.T)
````

## File: gateway/handler/health.go
````go
package handler
⋮----
import (
	"fmt"
	"io"
	"net/http"
	"time"
	"github.com/gin-gonic/gin"
)
⋮----
"fmt"
"io"
"net/http"
"time"
⋮----
"github.com/gin-gonic/gin"
⋮----
type HealthHandler struct {
	aiServiceURL string
}
⋮----
func NewHealthHandler(aiServiceURL string) *HealthHandler
⋮----
func (h *HealthHandler) Health(c *gin.Context)
````

## File: gateway/handler/models_test.go
````go
package handler
⋮----
import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"net/http/httptest"
"strings"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestModelsFetchSuccess(t *testing.T)
⋮----
func TestModelsFetchMissingBaseURL(t *testing.T)
⋮----
func TestModelsFetchInvalidBody(t *testing.T)
⋮----
func TestModelsFetchUpstreamUnreachable(t *testing.T)
⋮----
func TestModelsFetchUpstreamError(t *testing.T)
⋮----
func TestNewModelsHandler(t *testing.T)
````

## File: gateway/handler/models.go
````go
package handler
⋮----
import (
	"fmt"
	"io"
	"net/http"
	"github.com/gin-gonic/gin"
)
⋮----
"fmt"
"io"
"net/http"
⋮----
"github.com/gin-gonic/gin"
⋮----
type ModelsHandler struct {
	aiServiceURL string
}
⋮----
func NewModelsHandler(aiServiceURL string) *ModelsHandler
⋮----
func (h *ModelsHandler) ModelsFetch(c *gin.Context)
⋮----
var req struct {
		BaseURL string `json:"base_url"`
		APIKey  string `json:"api_key"`
	}
````

## File: gateway/handler/rag_extended_test.go
````go
package handler
⋮----
import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"encoding/json"
"net/http"
"net/http/httptest"
"strings"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestRagUploadProxiesToAIService(t *testing.T)
⋮----
func TestRagDocumentsListsDocuments(t *testing.T)
⋮----
func TestRagHealthReturnsOk(t *testing.T)
⋮----
func TestRagHealthFallsBackToGeneralHealth(t *testing.T)
⋮----
var body map[string]string
⋮----
func TestFeishuSyncProxiesToAIService(t *testing.T)
⋮----
func TestFeishuDefaultSyncProxiesToAIService(t *testing.T)
⋮----
func TestRagQueryAIServiceErrorNonStream(t *testing.T)
⋮----
func TestRagQueryAIServiceUnreachable(t *testing.T)
⋮----
func TestDirectRagAnswer你好(t *testing.T)
⋮----
func TestDirectRagAnswer你是谁(t *testing.T)
⋮----
func TestDirectRagAnswer谢谢(t *testing.T)
⋮----
func TestDirectRagAnswerHello(t *testing.T)
⋮----
func TestDirectRagAnswerUnknownReturnsEmpty(t *testing.T)
⋮----
func TestDirectRagAnswerInvalidBodyReturnsEmpty(t *testing.T)
⋮----
func TestRagKnowledgeBaseIsEmptyHealthCheckFails(t *testing.T)
⋮----
func TestIsRagEmbeddingNotFoundLine(t *testing.T)
⋮----
func TestNewRAGHandler(t *testing.T)
````

## File: gateway/handler/rag_test.go
````go
package handler
⋮----
import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"net/http/httptest"
"strings"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestRagQueryFallsBackForEmptyMemoryEmbedding404(t *testing.T)
⋮----
func TestRagQueryDirectAnswerSkipsAIService(t *testing.T)
````

## File: gateway/handler/rag.go
````go
package handler
⋮----
import (
	"bufio"
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"github.com/gin-gonic/gin"
)
⋮----
"bufio"
"bytes"
"context"
"encoding/json"
"fmt"
"io"
"net/http"
"strings"
⋮----
"github.com/gin-gonic/gin"
⋮----
type RAGHandler struct {
	aiServiceURL string
}
⋮----
func NewRAGHandler(aiServiceURL string) *RAGHandler
⋮----
func (h *RAGHandler) RagUpload(c *gin.Context)
⋮----
func (h *RAGHandler) RagHealth(c *gin.Context)
⋮----
func (h *RAGHandler) RagQuery(c *gin.Context)
⋮----
func (h *RAGHandler) RagDocuments(c *gin.Context)
⋮----
func (h *RAGHandler) FeishuSync(c *gin.Context)
⋮----
func (h *RAGHandler) FeishuDefaultSync(c *gin.Context)
⋮----
func (h *RAGHandler) proxyRagQuery(c *gin.Context, url string)
⋮----
func isRagEmbeddingNotFoundLine(line string) bool
⋮----
// SSE 格式中 JSON 键值对可能带或不带空格，所以用更灵活的方式匹配
⋮----
func directRagAnswerFromBody(body []byte) string
⋮----
var req struct {
		Question string `json:"question"`
	}
⋮----
func writeDirectRagAnswer(c *gin.Context, answer string)
⋮----
func (h *RAGHandler) ragKnowledgeBaseIsEmpty(ctx context.Context) bool
⋮----
var health struct {
		Storage   string `json:"storage"`
		Documents int    `json:"documents"`
	}
⋮----
func writeEmptyRagFallback(c *gin.Context, flusher http.Flusher)
````

## File: gateway/main.go
````go
package main
⋮----
import (
	"fmt"
	"time"
	"github.com/gin-gonic/gin"
	"github.com/ai-hiking/gateway/config"
	"github.com/ai-hiking/gateway/handler"
	"github.com/ai-hiking/gateway/middleware"
)
⋮----
"fmt"
"time"
⋮----
"github.com/gin-gonic/gin"
⋮----
"github.com/ai-hiking/gateway/config"
"github.com/ai-hiking/gateway/handler"
"github.com/ai-hiking/gateway/middleware"
⋮----
func main()
````

## File: gateway/middleware/cors_test.go
````go
package middleware
⋮----
import (
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"net/http/httptest"
"testing"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestCORSMiddlewareParsesMultipleOrigins(t *testing.T)
⋮----
func TestCORSMiddlewareEmptyOriginsRejects(t *testing.T)
⋮----
func TestCORSMiddlewarePreflight(t *testing.T)
⋮----
func TestCORSMiddlewareAllowedMethods(t *testing.T)
````

## File: gateway/middleware/cors.go
````go
package middleware
⋮----
import (
	"net/http"
	"strings"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"strings"
⋮----
"github.com/gin-contrib/cors"
"github.com/gin-gonic/gin"
⋮----
func CORSMiddleware(allowedOrigins string) gin.HandlerFunc
⋮----
// 空来源时返回空中间件以避免 gin-contrib/cors panic，直接拒绝所有跨域请求
````

## File: gateway/middleware/ratelimit_test.go
````go
package middleware
⋮----
import (
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"net/http/httptest"
"strings"
"testing"
"time"
⋮----
"github.com/gin-gonic/gin"
⋮----
func TestRateLimitAllowsWithinLimit(t *testing.T)
⋮----
func TestRateLimitBlocksExcess(t *testing.T)
⋮----
func TestRateLimitTokensRefill(t *testing.T)
⋮----
func TestRateLimitPerIPTracking(t *testing.T)
````

## File: gateway/middleware/ratelimit.go
````go
package middleware
⋮----
import (
	"net/http"
	"sync"
	"time"
	"github.com/gin-gonic/gin"
)
⋮----
"net/http"
"sync"
"time"
⋮----
"github.com/gin-gonic/gin"
⋮----
type bucket struct {
	tokens    int
	lastCheck time.Time
}
⋮----
func RateLimitMiddleware(rate int, per time.Duration) gin.HandlerFunc
⋮----
var mu sync.Mutex
````

## File: LangChain组件学习指南.md
````markdown
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
````

## File: mcp-server/image_search/requirements.txt
````
mcp[cli]>=1.0.0
httpx>=0.27.0
````

## File: mcp-server/image_search/server.py
````python
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "")
⋮----
mcp = FastMCP("image-search", description="Search for images using Pexels API")
⋮----
@mcp.tool()
async def search_images(query: str, count: int = 5) -> str
⋮----
response = await client.get(
⋮----
data = response.json()
⋮----
results = []
⋮----
parser = argparse.ArgumentParser(description="Image Search MCP Server")
⋮----
args = parser.parse_args()
````

## File: memory_data/missing-key-sse.json
````json
{
  "chat_id": "missing-key-sse",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    }
  ]
}
````

## File: memory_data/runtime-llm-sse.json
````json
{
  "chat_id": "runtime-llm-sse",
  "messages": [
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    },
    {
      "role": "user",
      "content": "今天的天气适合去徒步吗"
    },
    {
      "role": "assistant",
      "content": "ok:route_plan"
    }
  ]
}
````

## File: memory_data/test-chat-disabled.json
````json
{
  "chat_id": "test-chat-disabled",
  "messages": [
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    },
    {
      "role": "user",
      "content": "测试内存关闭"
    },
    {
      "role": "assistant",
      "content": "Mocked Disabled Response"
    }
  ]
}
````

## File: memory_data/test-chat-error.json
````json
{
  "chat_id": "test-chat-error",
  "messages": [
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    },
    {
      "role": "user",
      "content": "测试内存报错 fallback"
    },
    {
      "role": "assistant",
      "content": "Mocked Recovery Response"
    }
  ]
}
````

## File: memory_data/test-chat-sse-123.json
````json
{
  "chat_id": "test-chat-sse-123",
  "messages": [
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    },
    {
      "role": "user",
      "content": "测试流式响应"
    },
    {
      "role": "assistant",
      "content": "Mocked SSE Response"
    }
  ]
}
````

## File: memory_data/test-chat-sync-123.json
````json
{
  "chat_id": "test-chat-sync-123",
  "messages": [
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    },
    {
      "role": "user",
      "content": "测试徒步路线"
    },
    {
      "role": "assistant",
      "content": "Mocked Sync Response"
    }
  ]
}
````

## File: PRD.md
````markdown
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
````

## File: PROJECT_ANALYSIS.md
````markdown
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
````
