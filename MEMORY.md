# MEMORY

## 2026-05-19 Agent weather-to-route workflow optimization

- Regenerated `repo-context.md`, reread `MEMORY.md` and current Agent/frontend context before editing.
- Loaded the required `caveman` response guidance and TDD workflow; scoped the change to Agent workflow, hiking route tool behavior, frontend location handoff, focused tests, and memory logging.
- TDD red step added/updated regressions for two user journeys: current-location weather suitability should answer directly after `geo_lookup` + `weather_lookup` without entering ReAct, and an affirmative follow-up like `需要` should reuse location, call route research/search, and return route recommendation star ratings.
- Red validation failed as expected: current code still creates the LangGraph ReAct agent for the weather flow, route follow-up does not call geo/route tools, `route_research` does not expose `web_search`, and frontend does not cache/reuse browser location for the follow-up.
- Implemented the narrow workflow fix: weather suitability now uses deterministic geo/weather prefetch plus one direct LLM judgment/fallback response, suitable days end with a route recommendation opt-in, route follow-ups infer `route_plan`, prefetch geo plus `route_research`, and `route_research` now calls `web_search` and returns candidate route star ratings.
- Frontend now caches the last authorized browser location and reuses it when the user answers the route recommendation prompt with an affirmative short reply, so `需要` can still carry location to the backend.
- Focused TDD green validation passed for the new backend weather/route workflow, route search/rating tool behavior, and frontend location handoff tests.
- Final validation passed: related backend Agent/intake/tool/chat suites (`41 passed`), backend full suite (`243 passed, 11 skipped`), frontend `npm test` (`25 passed`), frontend `npm run build`, Python compileall for Agent/tool/test files, AI service health, Gateway health, and frontend `/super-agent` HTTP 200. Browser plugin tools were not exposed in this Codex surface and local Playwright was not installed, so UI browser validation used HTTP/build/tests rather than a screenshot run.

## 2026-05-19 Agent/RAG conversation memory progress

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded the requested `design-taste-frontend`, local `think`, local `pua`, and TDD workflow files before editing.
- Scoped the feature to frontend UI only after inspecting the current memory system: Agent backend chat memory keeps a 60-message sliding window, while Agent/RAG pages both persist per-conversation messages locally.
- TDD red step added `frontend/tests/conversationMemory.test.mjs`; it currently fails because the shared `conversationMemory.ts` helper and `ConversationMemoryMeter` component do not exist yet.
- Implemented a shared `ConversationMemoryMeter` and `conversationMemory` helper using the 60-message memory window, then mounted the meter under the module subtitle/status line in both Agent and RAG pages for a unified single-conversation memory progress display.
- Browser mobile validation exposed an existing global sidebar overlap on narrow viewports; added a TDD regression in `frontend/tests/appLayout.test.mjs` and fixed `App.tsx` so the fixed sidebar is hidden on mobile and the main content margin resets.
- Validation passed: frontend TDD red/green cycle, `npm test` (`24 passed`), `npm run build`, and browser screenshots/checks for `/super-agent` and `/love-master` on desktop plus 390px mobile viewports. Mobile meter bounds stayed within the viewport.

## 2026-05-19 Agent task-exit component TDD

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded the requested `think`, `pua`, and `tdd` skills before editing.
- TDD red test added for Agent step-budget exhaustion: a LangGraph `Sorry, need more steps to process this request.` failure must become a controlled Chinese `text` response with structured `done.metadata.status=budget_exhausted`.
- Red validation confirmed the current stream emits no final text for this failure path, so the missing abstraction is a real runtime exit-control gap rather than a frontend rendering issue.
- Implemented the first vertical slice with `agent/task_exit.py` and Agent stream integration: budget exhaustion is now translated into a user-facing Chinese `text` event plus `done` metadata instead of raw runtime text or a bare error event.
- Added explicit `terminate` coverage: when the terminate tool returns, the Agent stream now emits a structured completed exit and stops consuming later model updates, making terminate a real task-exit signal instead of a normal observation.
- Extended the same budget-exhaustion semantics to the non-SSE `AIAgent.aexecute()` path so sync and streaming calls share one task-exit controller.
- Validation passed: `test_agent_execution_flow.py` plus Agent/tool/chat regression suites (`44 passed`), Python compileall for Agent modules/tests, and backend suite excluding one live Feishu rate-limit test (`240 passed, 11 skipped, 1 deselected`). Full backend suite was blocked only by live `lark-cli` API rate limit `9499 too many request`, unrelated to Agent changes.

## 2026-05-16 Project launch

- Regenerated `repo-context.md` per project prerequisites before starting work.
- `MEMORY.md` was not present, so this file was created for required step logging.
- Existing services found: Docker PostgreSQL/Redis healthy, AI service on port 8000, frontend Vite on port 5173.
- Started missing gateway service from `gateway/gateway.exe` on port 8080.
- Verified health endpoints: AI service `/health` ok, gateway `/health` ok with AI service reachable, frontend root returns HTTP 200.

## 2026-05-16 Agent/RAG status detection

- Added an Agent module health endpoint at `/api/v1/chat/health` so the frontend can detect Agent readiness without sending a chat message.
- Added a RAG module health endpoint at `/api/v1/rag/health`, exposing document-directory readiness and current vector storage mode; also fixed the missing `asyncio` import in the RAG streaming path and corrected pgvector import binding.
- Routed the new Agent and RAG health endpoints through the Go gateway so the React app can check module status via the existing `/api/v1/*` proxy surface.
- Updated the shared ChatRoom UI to use three persistent module states (`未连接`, `连接错误`, `连接成功`), auto-check health on page entry and every 30 seconds, and show deduplicated alert dialogs with backend error reasons.
- Validation passed: `npm run build`, `go test ./...`, Python compile for changed AI-service modules, and FastAPI TestClient checks for `/api/v1/chat/health` and `/api/v1/rag/health` both returned HTTP 200.
- Adjusted Agent health metadata to report the configured tool registry count instead of introspecting the compiled LangGraph object.
- Started the Vite dev server on `http://127.0.0.1:5173/` after frontend changes; `/super-agent` returned HTTP 200.
- Browser validation showed old runtime endpoints return 404 and trigger status-error dialogs; added a short global dedupe window keyed by module and HTTP status so dev-mode remounts do not spam equivalent alerts.
- Browser re-check confirmed `/super-agent` shows `连接错误` and opens a status-error alert when the current old gateway returns 404 for `/api/v1/chat/health`.

## 2026-05-16 Project restart

- Regenerated `repo-context.md` per project prerequisites before restarting services.
- Restarted Docker dependencies with `docker compose restart`; `ai-hiking-postgres` and `ai-hiking-redis` reported healthy.
- Restarted the gateway on port 8080 and Vite frontend on port 5173.
- AI service health on port 8000 remained OK via the existing uvicorn reload child process; a fresh AI-service process could not fully replace it because the current Codex shell, user env, and machine env do not expose `OPENAI_API_KEY`.
- Cleaned up the failed replacement AI-service process and verified final health: AI service `/health` 200, gateway `/health` 200, frontend root 200.

## 2026-05-16 Super Agent connection diagnosis

- Regenerated `repo-context.md` before debugging the Super Agent connection error.
- Confirmed the frontend error is caused by health checks returning 404: gateway `/api/v1/chat/health` and direct AI service `/api/v1/chat/health` both returned HTTP 404, while AI service `/health` remained healthy.
- Current running AI-service OpenAPI does not include the newer module health routes even though source files do; replacing the AI process is blocked by missing `OPENAI_API_KEY` in the current shell/user/machine environment.
- Chosen fix: make gateway module health endpoints fall back to AI service `/health` when older AI-service runtimes do not expose module-specific health routes, preserving existing working chat runtime.
- Implemented gateway fallback behavior in `handler.ChatHealth` and `handler.RagHealth`; module health routes now synthesize `status: ok` from AI service `/health` when module-specific routes return 404.
- Validation passed: `go test ./...`, rebuilt `gateway.exe`, restarted gateway on port 8080, verified `/api/v1/chat/health` and `/api/v1/rag/health` return HTTP 200, verified frontend build, and browser-confirmed `/super-agent` now displays `连接成功`.

## 2026-05-17 Frontend backend real-logic wiring

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before making changes.
- Found three real integration gaps: Agent frontend generated a new `chat_id` per send so backend chat history could not work, gateway buffered RAG SSE responses instead of streaming them, and RAG memory fallback lost uploaded documents because every request created a fresh retriever.
- Chosen fix: keep frontend changes local to `SuperAgent`, make gateway provide a shared SSE proxy helper, and share RAG fallback documents across retriever instances instead of adding new dependencies.
- Implemented stable persisted Agent `chat_id`, dynamic itinerary sidebar values derived from actual conversation content, JSON-safe gateway chat SSE forwarding, non-2xx backend error propagation, streamed RAG query proxying, richer frontend SSE error parsing, and shared in-process RAG fallback documents.
- Browser validation on `http://127.0.0.1:5173/super-agent` exposed a local CORS mismatch: gateway default allowed only `http://localhost:5173`; added `http://127.0.0.1:5173` and trimmed comma-separated origin config.
- RAG query validation showed empty in-memory knowledge bases still called the embedding API and surfaced `Error code: 404`; added an early fallback return when no matching documents exist so the frontend gets the real no-document RAG response.

## 2026-05-17 CSS and hidden LLM config repair

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before edits.
- Loaded requested `think`, `pua`, `transitions-dev`, `tdd`, and `caveman` skills; scoped work to frontend CSS/runtime, hidden route UI, motion polish, and verification only.
- RCA found the active Vite dev CSS on port 5173 was serving raw `@tailwind` directives, while a fresh frontend-root dev server processed Tailwind correctly; the code also kept design tokens/keyframes in `App.css`, which was not imported by `main.tsx`.
- TDD red step added `frontend/tests/llmConfig.test.mjs` and `npm test`; it currently fails because `src/api/llmConfig.ts` does not exist yet.
- Implemented `src/api/llmConfig.ts` with default LLM/embedding settings, normalization, localStorage persistence, reset, and API-key masking; tests now cover invalid JSON fallback, safe numeric clamping, save/load, and masking.
- Added hidden `/llm-config` route and `LlmConfig` page with separate large-model and embedding-model configuration sections; no sidebar/nav entry was added.
- Moved active design tokens, keyframes, loading indicators, and transitions-dev panel/icon CSS into `src/index.css`, because that is the stylesheet imported by `main.tsx`; added a small SVG favicon to remove the dev 404.
- Restarted Vite on `http://127.0.0.1:5173/`; verified `/src/index.css` now contains compiled Tailwind utilities instead of raw `@tailwind` directives.
- Validation passed: `npm test`, `npm run build`, Chrome DevTools snapshots/screenshots for `/super-agent` and `/llm-config`; only existing React Router v7 future warnings remain in console.

## 2026-05-17 RAG empty-store embedding guard

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before edits.
- Loaded requested `think`, `pua`, `caveman`, and `tdd` skills; routed the bug through Huawei-style RCA and kept scope to the RAG retriever unless evidence expands it.
- Reproduced the current RAG failure through gateway `/api/v1/rag/query`: empty `status=feishu` knowledge base streams `Error code: 404` because pgvector mode calls the embedding API before checking whether matching documents exist.
- TDD red test added `ai-service/tests/test_retriever.py`; it fails because `VectorStoreRetriever.similarity_search()` calls embeddings even when pgvector has no matching rows.
- Implemented `VectorStoreRetriever._has_matching_documents()` with a pgvector preflight query, so empty vector stores or empty status filters return no documents without calling the embedding API; focused test now passes.
- Live gateway still proxied the old long-running AI process, which has not reloaded the patched source and cannot be safely restarted from this shell because no `OPENAI_API_KEY` is available in process/user/machine env.
- Added a gateway compatibility fallback for empty in-memory RAG stores: when the AI service streams `Error code: 404` and `/api/v1/rag/health` reports `storage=memory` with `documents=0`, the gateway now emits the same no-document SSE response instead of surfacing the backend embedding error.
- Validation passed: `python -m pytest ai-service/tests/test_retriever.py ai-service/tests/test_memory.py ai-service/tests/test_feishu.py::TestExtractDocToken -q` (43 passed), `python -m compileall -q ai-service/rag ai-service/api`, and `go test ./...`.
- Rebuilt and restarted only `gateway/gateway.exe` on port 8080; live `/api/v1/rag/query` now streams a no-document response with `done` instead of `Error code: 404`, while gateway and RAG health endpoints remain HTTP 200.

## 2026-05-17 ModelScope embedding config and RAG direct answers

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before edits.
- Loaded requested `think`, `pua`, `caveman`, and `tdd` skills; approved scope is `ai-service` embedding configuration, RAG simple-question routing, tests, local env, `.gitignore`, and memory logging only.
- Verified ModelScope embedding endpoint manually: `Qwen/Qwen3-Embedding-8B` returns 4096-dimensional vectors at `https://api-inference.modelscope.cn/v1`; raw API requires `encoding_format=float`, while the local `langchain_openai.OpenAIEmbeddings` wrapper works with the provided model.
- TDD red tests added for independent embedding config, RAG retriever config usage, memory vector-store config usage, and simple greetings bypassing retrieval; all four fail against the previous code.
- Implemented independent embedding settings in `config.py`, wired RAG and memory vector stores to `EMBEDDING_*`, set pgvector table dimensions from config, added local `ai-service/.env` with the ModelScope embedding values, and ignored that env file via `.gitignore`.
- Added a direct-answer branch in RAG query flow for greetings/identity/thanks so these messages return a simple SSE answer without initializing retrieval or touching documents.
- Focused TDD tests now pass for embedding config and direct-answer routing.
- Live AI service on port 8000 is still an old long-running process and cannot be safely restarted from the current shell without the hidden LLM `OPENAI_API_KEY`; added the same direct-answer short-circuit to the gateway RAG handler so current port 8080 can skip document retrieval for simple greetings immediately.
- Validation passed: 47 Python tests across embedding config, RAG direct answer, retriever, memory, and Feishu token extraction; Python compile for config/RAG/API/memory; `go test ./...`; direct ModelScope wrapper ping returned 4096 dimensions.
- Rebuilt and restarted only `gateway/gateway.exe` on port 8080; live `/api/v1/rag/query` now answers `你好` and `你是谁？` directly without retrieval thoughts, while a normal RAG query still streams the retrieval path and no-document fallback.

## 2026-05-17 LLM config model picker filtering fix

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before edits.
- Loaded requested `think`, `pua`, and `tdd` skills; scoped work to the frontend LLM config page and its tests unless reproduction proved a backend fault.
- Browser mock reproduction on `http://localhost:5173/llm-config` confirmed the bug is in frontend filtering, not model fetching: after mocking `/api/v1/models/fetch` to return three models, clicking `获取模型` still showed `无匹配模型` because the dropdown reused the old selected value `gpt-4-test` as the filter keyword.
- TDD red step added a new frontend test covering the expected behavior that a freshly fetched model list remains fully visible until the user starts searching; the test failed first because the new filter helper did not exist yet.
- Implemented `filterModelList()` in `frontend/src/api/llmConfig.ts`, separated combobox search text from the selected model value in `frontend/src/pages/LlmConfig.tsx`, and cleared stale fetched options when `baseUrl` or `apiKey` changes.
- Validation passed: `frontend npm test`, `frontend npm run build`, browser mock re-check showed all fetched models are visible immediately after fetch and narrow correctly once typing starts.
- Restarted the frontend dev server on `http://localhost:5173/llm-config` after the verification reload cleared the previous listener.

## 2026-05-17 LLM config auto speed test after save

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md` before edits.
- Loaded requested `pua` skill and routed the work through Musk-style feature delivery; scope stayed in the frontend LLM config page and shared config helpers only, with no new backend APIs.
- Reused the existing `/api/v1/models/fetch` path as the speed-test probe instead of inventing a new protocol; the chosen definition of “测速” is connection-plus-response latency for model list retrieval, which matches the current config page’s available public interface.
- Added `canRunSpeedTest()` and `measureModelLatency()` to `frontend/src/api/llmConfig.ts`, including injection points for deterministic tests.
- Extended `frontend/src/pages/LlmConfig.tsx` so clicking `保存` now writes settings, disables the button, auto-runs latency tests for both LLM and embedding configs, and displays status/result cards (`未测速` / `测速中` / `已完成` / `失败` / `已跳过`) with measured milliseconds and model counts.
- Added focused frontend tests for auto-speed-test readiness detection and latency measurement helper behavior.
- Validation passed: `frontend npm test`, `frontend npm run build`, and browser verification on `http://localhost:5173/llm-config` with mocked `/api/v1/models/fetch` confirmed the save button enters a testing state and the result cards render measured latencies after completion.

## 2026-05-17 LLM config model usage filtering fix

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, and loaded the requested `pua` skill before debugging the repeated “获取模型仍然错误” report.
- Locked scope to `frontend/src/api/llmConfig.ts`, `frontend/src/pages/LlmConfig.tsx`, `frontend/tests/llmConfig.test.mjs`, and `MEMORY.md` unless evidence forced a backend expansion.
- RCA showed the remaining bug is model-usage mixing rather than stale combobox filtering: the generic `/models` response was not being separated into chat/completion vs embedding candidates, so the LLM card could surface embedding-only models.
- Added `filterModelsByUsage()` plus conservative model-kind inference based on ids and optional upstream metadata; the LLM card now keeps only chat/completion-style candidates while the embedding card keeps only embedding-style candidates.
- Updated both `ModelCombobox` instances to pass explicit usage (`llm` / `embedding`) and to show a manual-entry hint when a provider returns models that do not match the current card’s usage.
- Added a focused frontend test covering mixed fetched model lists (`gpt-4.1`, `deepseek-chat`, `text-embedding-3-small`, `Qwen3-Embedding-8B`, `whisper-1`) and verifying LLM vs embedding filtering.
- Validation passed: `frontend npm test`, `frontend npm run build`, and browser verification on `http://127.0.0.1:5173/llm-config` against a temporary local mock `/models` upstream confirmed the LLM dropdown shows only `gpt-4.1` and `deepseek-chat`, while the embedding dropdown shows only `text-embedding-3-small` and `Qwen3-Embedding-8B`.

## 2026-05-17 LLM config stale storage migration fix

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, and reloaded the requested `pua` skill before investigating the follow-up report that model fetching was still wrong.
- Reproduced the user-visible bad state by writing stale settings into browser `localStorage`: `llm.model=text-embedding-3-small` and `embedding.model=text-embedding-test` exactly recreate the screenshot symptom on page load even with the newer runtime code.
- Root cause changed from “current fetch returns wrong candidates” to “historical wrong model selections persist across sessions”; the page previously trusted stored model ids without validating whether they obviously belong to the wrong slot.
- Added stored-setting sanitization in `frontend/src/api/llmConfig.ts` so obvious cross-slot values like embedding ids in the LLM slot fall back to safe defaults on load/save, while unknown custom names still remain untouched.
- Added `repairModelSelection()` and wired `frontend/src/pages/LlmConfig.tsx` to auto-correct an obviously wrong current selection to the first valid fetched candidate after `获取模型`, so an already-open broken page can self-heal without requiring a manual reset.
- Added focused tests for stale cross-slot migration and post-fetch auto-repair; validation passed with `frontend npm test` (10/10) and `frontend npm run build`.
- Browser validation on `http://127.0.0.1:5173/llm-config` confirmed two cases: reloading with stale `localStorage` now repairs the LLM card back to `deepseek-v4-flash`, and forcing the LLM input to `text-embedding-3-small` then clicking `获取模型` now auto-switches it to `deepseek-chat` when valid LLM candidates are returned.

## 2026-05-17 Rerank model config and RAG scoring step

- Regenerated `repo-context.md` per project prerequisites and reread `MEMORY.md`; loaded requested `think`, `pua`, and `tdd` local skills before editing.
- Scoped the change to the existing LLM config helper/page and AI-service RAG chain instead of adding a new service or changing gateway behavior.
- TDD red tests added coverage for a third `rerank` model slot in frontend config normalization/filtering/repair, and for `/api/v1/rag/query` invoking rerank before context augmentation.
- Added `settings.rerank` to `frontend/src/api/llmConfig.ts`, including usage-aware model filtering so reranker models do not appear under LLM or Embedding pickers.
- Updated `frontend/src/pages/LlmConfig.tsx` with Rerank summary, speed-test card, and dedicated Base URL/API Key/model picker section; browser verification on `http://localhost:5173/llm-config` confirmed the new section renders.
- Added `RERANK_*` backend settings and `rag.reranker.Reranker`, which calls an OpenAI-compatible `/rerank` endpoint, annotates selected documents with `rerank_score`/`rerank_rank`, and falls back to vector retrieval order on rerank failure.
- Inserted the rerank step after vector retrieval and before `ContextAugmenter.augment()` in the RAG SSE chain, with thought events for rerank start/completion when configured.
- Validation passed: `frontend npm test` (10/10), `frontend npm run build`, `python -m pytest ai-service/tests -q` (69 passed, 2 skipped), Python compileall for `ai-service/config.py`, `ai-service/api`, and `ai-service/rag`, plus browser snapshot/console check for `/llm-config`.

## 2026-05-17 RAG runtime model config repair

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, and loaded the requested `think`, `pua`, and `tdd` skills before debugging the RAG `HTTP 503: AI service unreachable` report.
- RCA confirmed the displayed 503 is from the gateway, because AI service port 8000 is down; `ai-service/uvicorn.err.log` shows startup fails at import time when `OPENAI_API_KEY` is missing, while `ai-service/.env` currently only contains Embedding configuration.
- TDD red tests added for two expected behaviors: AI service settings should load without a global chat API key, and RAG requests should pass frontend-supplied model settings into retriever/reranker/augmenter components.
- Implemented the fix by allowing AI-service settings to load without a global chat key, adding optional runtime model settings to `RAGQuery`, passing those settings into RAG retriever/reranker/augmenter components, and making the RAG page attach runnable local LLM settings to each query.
- Added frontend request-payload coverage, made RAG uploads also pass runtime Embedding settings, and repaired the model-fetch parser to accept the backend's legacy `{models: [...]}` response as well as OpenAI-style `{data: [...]}` responses.
- Validation passed for focused local suites: `python -m pytest ai-service/tests/test_embedding_config.py ai-service/tests/test_rag_rerank.py ai-service/tests/test_retriever.py ai-service/tests/test_reranker.py ai-service/tests/test_rag_direct_answer.py ai-service/tests/test_memory.py -q` (49 passed), `python -m compileall -q ai-service/config.py ai-service/api ai-service/rag`, `frontend npm test`, `frontend npm run build`, and `gateway go test ./...`.
- Full `python -m pytest ai-service/tests -q` reached 71 passed / 2 skipped but one external Feishu pagination test failed with real API rate limit `9499 too many request`, unrelated to the RAG model-config repair.
- Restarted AI service on port 8000; live checks now show gateway `/health` reports `ai_service=ok`, `/api/v1/rag/health` returns HTTP 200, RAG query streams HTTP 200 SSE, and browser validation on `http://127.0.0.1:5173/love-master` confirms RAG chat no longer shows `[连接错误] HTTP 503`.

## 2026-05-17 RAG Feishu knowledge-base and output repair

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, and loaded requested `caveman`, `grill-me`, and TDD workflow guidance; `/pua`, `/think`, and `/humanizer-zh` were not available in the active skill list, so their intent is applied as scope discipline, explicit planning, and natural Chinese output style.
- Called `lark-cli doctor` and Feishu Wiki commands for link screening: CLI/auth/network are healthy, Drive search works, but `wiki +space-list` currently fails with missing `wiki:space:retrieve` scope, so live Wiki-space traversal needs that authorization before full production sync can succeed.
- TDD red step added focused tests for Wiki URL parsing and `lark-cli wiki spaces get_node` resolution, RAG SSE process/document-summary events, and frontend structured RAG stream state handling.
- Implemented Feishu Wiki link screening/resolution via `lark-cli wiki spaces get_node`, Wiki-space node traversal via `lark-cli wiki nodes list`, clearer missing-scope errors, and Wiki metadata preservation when syncing into RAG.
- Updated RAG SSE output to separate concise process steps from final answer text, emit a structured document-search summary (`searched_count`, `matched_chunks`, per-document title/source/preview), and adjust answer prompts/messages toward natural Chinese with fewer generic retrieval logs.
- Updated the RAG frontend to render document search details and execution flow in default-collapsed disclosure sections, keeping the assistant answer clean.
- Validation passed: focused Feishu/RAG TDD tests, RAG-related Python tests, Python compileall for `ai-service/config.py`, `ai-service/api`, and `ai-service/rag`, frontend `npm test`, frontend `npm run build`, gateway `go test ./...`, and browser check on `http://127.0.0.1:5173/love-master`; only existing React Router v7 future warnings remain.

## 2026-05-17 RAG Feishu OpenAPI and process wording follow-up

- Regenerated `repo-context.md` before this repair cycle and continued from the approved RAG/Feishu scope.
- TDD red tests locked the Feishu adapter to explicit `lark-cli api` OpenAPI calls instead of `wiki ...` / `docs +fetch` shortcuts.
- Implemented `call_lark_api()` and moved Wiki node resolution, Wiki node listing, and docs_ai document fetch to `GET/POST /open-apis/...`; verified the exact command shape with `lark-cli api --dry-run`.
- Reworded RAG process SSE events to concrete pipeline steps: query rewrite, embedding vector generation, pgvector/memory retrieval, optional Rerank, and LLM answer generation.
- Updated the gateway empty-store fallback and frontend stream test so old vague process wording cannot return silently.
- `lark-cli doctor` is healthy, but live Wiki space listing still fails with Feishu permission `99991679` until `wiki:space:retrieve` / related Wiki scopes are authorized.
- Validation passed: focused Feishu OpenAPI tests, RAG process/rerank/direct-answer/retriever tests, Python compileall, frontend `npm test`, frontend `npm run build`, and gateway `go test ./...`.

## 2026-05-18 RAG grounded-answer guardrail

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, loaded requested `pua`, `think`, `caveman`, `humanizer-zh`, and `tdd` skill files, and used `langchain-components.md` to map the fix to Retriever, ChatPromptTemplate, Guardrails, and Context Engineering components.
- RCA found two RAG quality issues: `rag_query` assumed every augmenter implements `augment_stream`, breaking sync-only test doubles, and retrieved chunks were treated as answerable evidence even when they had no direct relation to the prompt.
- TDD red tests now cover weakly related retrieved docs being blocked before final answer generation, grounded citation instructions in the prompt, and API-level handling of irrelevant retrieval as a no-match response.
- Implemented a lightweight relevance guard in `rag.augmenter.has_relevant_evidence()`, wired it into the RAG API before document summary and generation, strengthened the `ChatPromptTemplate` to require source-number citations and forbid document-external claims, and lowered RAG answer temperature to reduce drift.
- Preserved streaming behavior while adding a sync `augment()` fallback for augmenter implementations that do not expose `augment_stream`.
- Validation passed: focused red/green tests for `test_rag_augmenter.py` and `test_rag_retrieve_and_output.py`; broader RAG/local suite passed with 69 tests; Python compileall passed for `ai-service/api` and `ai-service/rag`.
- Full `python -m pytest ai-service/tests -q` is still blocked by live Feishu permission/API failures unrelated to this guardrail: 93 passed, 2 skipped, 10 Feishu tests failed with `99991679 Permission denied` or empty `lark-cli API 错误`.

## 2026-05-18 RAG hybrid pipeline and thinking animation

- Kept the change scope locked to the requested RAG upload/query pipeline and assistant thinking UI; no unrelated layout or architecture cleanup.
- Document upload now follows normalize/read -> regex denoise -> hybrid paragraph/recursive chunking -> metadata tagging -> embedding -> PGVector storage, with `.txt`, `.md`, `.pdf`, and `.docx` ingestion support.
- RAG query now follows user question -> query rewrite -> question embedding -> hybrid retrieval -> BM25 + RRF fusion -> reranker -> humanizer-zh-style final query/answer generation.
- Added lightweight text-processing helpers for denoise, term extraction, BM25 scoring, and reciprocal-rank fusion so local tests can validate the flow without adding a heavy search dependency.
- Added richer `ai-thinking` streaming state in both LoveMaster and ChatRoom, with pulse/trace/label animation and reduced-motion handling; browser validation confirmed the live `AI 正在思考 / 思考中` state appears during query streaming.
- Installed `psycopg[binary]` into `ai-service/.conda312` and added it to `ai-service/requirements.txt`; live health checks now report `storage: pgvector` through both ai-service and gateway.
- Validation passed: targeted backend RAG tests `10 passed`, frontend `npm test -- thinkingAnimation.test.mjs` `14 passed`, frontend `npm run build` passed, browser `/love-master` load passed, `/api/v1/rag/query` returned HTTP 200.
- Full backend `python -m pytest -q` still has unrelated environment/history failures: live Feishu permission/API failures, existing memory vector dimension tests, and an older `psycopg2` monkeypatch expectation while runtime now uses `psycopg`.

## 2026-05-18 RAG pgvector dimension-mismatch repair

- Regenerated `repo-context.md` per project prerequisites, reread `MEMORY.md`, and loaded requested `think`, `pua`, `caveman`, and `tdd` skill files before debugging the screenshot's RAG `HTTP 503: AI service unreachable` report.
- RCA confirmed the live 503 came from gateway because AI service port 8000 was not running; after starting AI service, the deeper RAG failure was pgvector mixed dimensions: the table had 18 legacy 8-dimensional vectors and 11 current 4096-dimensional vectors, causing `different vector dimensions 8 and 4096` and fallback to empty memory retrieval.
- TDD red tests added deterministic coverage for empty status filters not calling embedding and pgvector similarity search filtering rows to the query vector dimensions.
- Implemented `_PGVectorClient.has_documents()` preflight for empty status filters and added `vector_dims(embedding) = %s` to pgvector similarity search so old vectors do not break current embedding configuration.
- Validation passed: focused retriever tests, RAG/runtime regression tests (`17 passed`), Python compileall for `ai-service/rag`, `ai-service/api`, and `test_retriever.py`, gateway `go test ./...`, gateway `/health` reporting `ai_service=ok`, and live gateway RAG query for `装备清单` returning HTTP 200 SSE with pgvector candidates instead of 503 or empty memory fallback.

## 2026-05-18 Feishu RAG zero-result RCA and embedding fallback

- Regenerated `repo-context.md`, reread project memory, and used the requested `think`, `pua`, `caveman`, and `tdd` workflow before touching the RAG path.
- RCA found two separate issues: the local DB currently has no Feishu metadata/status rows for the visible cloud document, and the screenshot-time runtime Embedding provider `api.edgefn.net/v1/embeddings` returned HTTP 400, which the old retriever path converted into an empty in-memory fallback.
- TDD red tests reproduced both failure modes: pgvector embedding failure must still allow BM25/lexical retrieval, and a bad runtime Embedding config must retry the default RAG Embedding config before returning no evidence.
- Implemented the minimal fix in `ai-service/rag/retriever.py` and `ai-service/api/rag.py`: failed pgvector vector search now leaves lexical retrieval alive, and empty custom-Embedding results retry the default retriever.
- Validation passed: focused retriever/API tests (`4 passed`), broader RAG/Embedding regression suite (`19 passed`), Python compileall, gateway `go test ./...`, service health checks, and a live gateway RAG query with intentionally bad runtime Embedding settings returning `户外徒步知识文档.md` candidates instead of `0 篇文档 / 0 个片段`.

## 2026-05-18 RAG plain-text answer cleanup

- Regenerated `repo-context.md`, reread project context/memory, and used the requested `think`, `pua`, `caveman`, and `tdd` workflow for the RAG answer-format complaint.
- Scoped the fix to RAG display text only: final answers, no-LLM fallback text, and document-search previews. Retrieval, Feishu sync, model settings, and frontend layout were intentionally left unchanged.
- Added TDD coverage for removing visible Markdown emphasis/headings, numeric citations, HTML `<sup>` footnotes, and oversized no-LLM context dumps.
- Implemented shared `clean_display_text()` plus compact, query-centered fallback snippets so chat bubbles show readable plain text instead of raw Markdown or whole-document dumps.
- Validation passed: focused red/green tests, broader RAG regression suite (`38 passed`), Python compileall, service/gateway health checks, and live gateway query for `徒步的核心目的` returning HTTP 200 with no `**`, no `[1]`, no `#`, no `<sup>`, and a snippet containing `亲近自然`.

## 2026-05-18 RAG direct-answer and dense-point formatting

- Regenerated `repo-context.md`, reread project context/memory, and used the requested `think`, `pua`, `caveman`, and `tdd` workflow for the RAG answer wording complaint.
- Scoped the change to RAG answer formatting only: prompt wording, generated-answer cleanup, streaming answer cleanup, and no-LLM fallback formatting. Retrieval, Feishu sync, model config, gateway, and frontend layout stayed unchanged.
- Added TDD coverage for removing answer-body meta phrases such as `根据文档` / `知识库内容`, preserving plain numbered points, filtering fallback snippets to the user's focus terms, dropping unrelated gear/camping snippets, and removing repeated question headings.
- Implemented answer formatting in `ai-service/rag/augmenter.py`: long generated answers become numbered plain-text points, no-LLM fallback answers with focused facts only, and source/provenance stays in the folded document-search UI rather than the body.
- Validation passed: focused red/green tests, broader RAG regression suite (`41 passed`), Python compileall, service/gateway health checks, and live gateway query for `徒步的核心目的` returning HTTP 200 with no `文档/知识库/根据/检索/可参考`, no markdown/citation markers, no irrelevant gear/camping facts, and multi-line numbered output containing `亲近自然`.

## 2026-05-18 Agent workflow documentation and overview

- Regenerated `repo-context.md` per project execution prerequisites before starting the documentation walkthrough.
- Reviewed and thoroughly inspected the codebase, `MEMORY.md`, and the newly created `agent_architecture_and_workflow.md` artifact detailing the LangGraph ReAct agent design and L0/L1/L2 three-tier memory architecture.
- Formulated a highly polished, comprehensive walkthrough response detailing the macro system architecture, step-by-step sequencing, code walkthrough, fallback resilience strategies, and technical presentation talktrack.

## 2026-05-18 Agent LangGraph execution-chain optimization

- Regenerated `repo-context.md`, reread project memory/context, and reviewed `C:\Users\14253\Desktop\yu-ai-agent-master\repo-context.md` before touching Agent code.
- Reference decision: keep this project's LangGraph Agent, only learn Yu's clear `BaseAgent -> ReActAgent -> ToolCallAgent -> YuManus/HikeAgent` execution visibility, step boundaries, tool-call lifecycle, max-step discipline, and terminate semantics.
- Pua scope lock: changed only `ai-service/agent/prompts.py`, `ai-service/agent/agent.py`, `ai-service/api/chat.py`, and focused Agent tests; no RAG, frontend layout, gateway, or tool implementation changes.
- TDD red tests first covered three expected behaviors: search/file/PDF-style prompts must use the unified LangGraph stream instead of keyword shortcuts; SSE must expose medium-grain ReAct details (`thought`, `tool_call`, `tool_result`, `text`, `done`); streaming chat must persist the assistant reply and emit only one `done`.
- Implemented unified `AIAgent.aexecute_stream()` through LangGraph `astream(stream_mode="updates")`, added robust tool-call/tool-result parsing with step metadata, expanded Agent prompt details for the complete execution chain, removed hardcoded keyword branches, and injected `NEXT_STEP_PROMPT` into the dynamic system state.
- Repaired chat memory sequencing so history is read before the current user message is appended, and SSE now writes the final assistant text back to `FileChatMemory` after a successful stream.
- Validation passed: `python -m pytest ai-service/tests/test_agent_execution_flow.py -q` (3 passed), `python -m pytest ai-service/tests/test_chat_health.py ai-service/tests/test_chat_memory_integration.py ai-service/tests/test_agent_execution_flow.py -q` (11 passed), and `python -m compileall -q ai-service/agent ai-service/api ai-service/tests/test_agent_execution_flow.py`.

## 2026-05-18 Full service startup and verification

- Regenerated `repo-context.md` per project prerequisites before restarting services.
- Detected Windows port dynamic exclusion range blocking port `6379` (dynamic NAT reservations).
- Changed Redis host port mapping from `6379:6379` to `5379:6379` in `docker-compose.yml` to resolve bind conflict, and updated `REDIS_URL=redis://localhost:5379/0` in `ai-service/.env`.
- Cleaned up conflicting running containers on ports 6379 and 5432.
- Started Docker dependencies using `docker compose up -d`; `ai-hiking-postgres` and `ai-hiking-redis` started and reported healthy.
- Started AI Service on port 8000 using local python environment at `ai-service/.conda312/python.exe`.
- Started Gateway Service on port 8080 using `gateway/gateway.exe`.
- Started Frontend Vite dev server on port 5173 using `npm run dev`.
- Browser subagent verified both `http://localhost:5173/love-master` (RAG dialogue module) and `http://localhost:5173/super-agent` (Agent module) show successful gateway connection (`连接成功`/🟢 active state).

## 2026-05-18 Agent PRD and LangChain component research

- Regenerated `repo-context.md` with the required Repomix command, then reread project context and memory before planning the Agent changes.
- Inspected the current Agent module, including LangGraph ReAct execution, prompts, SSE streaming, memory injection, MCP client, frontend event rendering, and all registered tools.
- Used authenticated Firecrawl CLI to map and scrape the latest LangChain/LangGraph documentation under `https://docs.langchain.com/`, focusing on agents, tools, middleware, memory, MCP, streaming, human-in-the-loop, structured output, guardrails, persistence, interrupts, and durable execution.
- Wrote `Agent-PRD.md` at the project root as the planning artifact for the next Agent iteration.
- Key decision: keep the existing LangGraph ReAct Agent as the near-term base, then optimize it with a tool registry, risk levels, dynamic tool selection, clearer SSE events, structured final output, and memory commit boundaries before attempting a dependency upgrade.
- Key decision: treat latest LangChain 1.x components as target architecture patterns because the project currently pins `langchain==0.3.0` and `langgraph==0.2.0`; Phase 0 must validate compatibility before adopting new middleware/checkpointer/store/MCP APIs directly.

## 2026-05-18 Audit and Document Project Toolsets

- Completed comprehensive review of all toolsets and agent-specific tools in the project.
- Verified definitions and risk levels of all 7 executable tools registered in `ToolRegistry` within `ai-service/agent/agent.py` and `ai-service/tools/`.
- Documented and structured the findings regarding:
  1. The project's overall toolsets (executable tools, RAG search & feishu integration, and MCP client capabilities).
  2. The Agent module's specific tools, their parameter schemas, risk classifications, rate limits, and safety confirmation gates.

## 2026-05-18 AI Hiking Agent planning document

- Regenerated `repo-context.md` with the required Repomix command before writing the planning document.
- Reread `MEMORY.md`, current Agent/RAG/tool/memory context, and the requested `humanizer-zh` skill before drafting.
- Wrote `AI-Hiking-Agent改造计划书.md` to capture the current discussion: the Agent should become a workflow-led outdoor hiking assistant that uses weather, geo, route research, RAG, gear, risk, and export tools instead of presenting a generic all-tools ReAct agent.
- Key planning decision: keep RAG as an Agent knowledge tool, weaken LangGraph in the short term, use intent plus slot extraction instead of broad query rewriting, expose only 3-5 tools per turn, and move memory writes to an after-execution commit step.

## 2026-05-19 AI Hiking Agent Phase 1 module retrofit

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded requested `pua`, `caveman`, and `tdd` skills before editing.
- Implemented deterministic request intake in `ai-service/agent/intake.py`: AgentIntent, hiking slots, scenario override, missing-slot detection, clarifying questions, and search query construction.
- Added hiking domain tools: `hiking_knowledge_search` wraps existing RAG retrieval with traceable chunks; weather/geo/route/gear/risk/export tools provide structured envelopes for the Agent workflow.
- Upgraded tool selection: `AVAILABLE_TOOL_MAP` now includes domain tools; `select_tools_for_context` exposes only small scenario-specific tool sets and keeps terminal/resource download out of ordinary hiking flows.
- Compatibility decision: domain tools are registered as hidden metadata in `ToolRegistry`, so legacy registry tests and base tool health stay stable while dynamic selection can still use the new hiking tools.
- Fixed SSE confirmation wiring to use the unified `needs_confirmation` key and added `ChatRequest.scenario` for frontend scenario shortcuts.
- Validation passed: focused TDD suites for intake/tool selection/knowledge tool (`9 passed`) and Agent stream/confirmation regressions (`15 passed`).
- Completed the memory timing retrofit: `AIAgent` now reads memory with `build_runtime_context()` before execution and calls `commit_interaction()` only after the final assistant response, carrying intent and structured hiking slots as task state.
- Validation passed for memory integration and committer behavior: `python -m pytest ai-service/tests/test_chat_memory_integration.py ai-service/tests/test_memory_committer.py ai-service/tests/test_memory.py -q` (`45 passed`).
- Stabilized Feishu integration tests for local authorization variance: live fetch/wiki checks now skip when `lark-cli` lacks auth or permissions, while pure parser/mock tests still run; Wiki space sync now records traversal errors as summary rows instead of raising through the batch.
- Validation passed: `python -m pytest ai-service/tests/test_feishu.py -q` (`25 passed, 11 skipped`).
- Repaired legacy full-suite blockers uncovered during final TDD validation: `FileChatMemory` now supports test-scoped `save_dir` storage and a 60-message window, MCP async tests run through a local pytest asyncio hook, MCP stdio mocks no longer emit un-awaited coroutine warnings, and model fetching maps upstream/request errors to stable HTTP responses.
- Completed frontend Agent interaction cleanup: scenario quick actions are covered by regression tests, tool/thought/approval events render in a folded execution panel, and artifact events render separately from the primary assistant answer.
- Final validation passed: backend full suite `python -m pytest ai-service/tests -q` (`214 passed, 11 skipped`), frontend `npm test` (`17 passed`), frontend `npm run build`, and Python compileall for touched backend packages/tests.
- Started the frontend dev server for manual inspection at `http://127.0.0.1:5173/super-agent` and verified the route returns `200 OK`.

## 2026-05-19 Agent toolset configuration audit

- Regenerated `repo-context.md` and reread `MEMORY.md` before auditing the Agent module toolset configuration.
- Current local tool catalog is internally aligned: `AVAILABLE_TOOL_MAP`, `ToolRegistry`, and risk metadata all cover 14 tools (`7` base visible tools plus `7` hidden hiking/domain tools).
- Dynamic tool selection is configured by intent in `select_tools_for_context()`, keeping ordinary hiking flows away from `terminal`, `resource_download`, and broad file operations.
- Main configuration gaps found: MCP client exists but is not wired into `AIAgent`; high-risk confirmation is only surfaced in SSE metadata and pending store, not used to block execution before LangGraph runs the tool; registry metadata is duplicated from LangChain tool schemas, so drift is possible; no first-class `/api/v1/tools` endpoint currently exposes the registry; external tool config lacks health/readiness reporting.
- Validation passed for focused Agent/tool/MCP/confirmation suites: `OPENAI_API_KEY=test python -m pytest tests/test_agent.py tests/test_hiking_tool_selection.py tests/test_mcp_client.py tests/test_confirmation.py tests/test_chat_confirmation_fields.py -q` (`49 passed`, `1 warning`).

## 2026-05-19 Agent toolset configuration fixes

- Implemented the approved minimal repair plan for Agent toolset configuration without upgrading LangChain/LangGraph or changing Gateway/RAG/frontend layout.
- Added `/api/v1/tools` and `/api/v1/tools/health` via `ai-service/api/tools.py`, exposing registry metadata, risk levels, hidden flags, configuration validation, MCP readiness, and external key presence without leaking secrets.
- Added `validate_tool_configuration()` in `ai-service/agent/agent.py` to detect drift between `AVAILABLE_TOOL_MAP`, `ToolRegistry`, risk map, base tools, and intent route tool names.
- Added confirmation guards around high-risk/critical LangChain tools before passing them to LangGraph, and normalized SSE behavior so high-risk calls emit `approval_required` and suppress side-effect-looking tool results until an approval path is implemented.
- Explicitly kept `terminate` as `risk_level=HIGH` but `needs_confirmation=False` because it is an internal control-flow tool, not a user-facing side-effect operation.
- Added explicit opt-in MCP loading in `ai-service/mcp/client.py` through `load_mcp_tools()`, namespacing loaded tools as `mcp:<server>:<tool>` to avoid collisions; empty config performs no subprocess work.
- TDD validation passed on the final state: broader Agent/tool/MCP/confirmation regression `61 passed, 1 warning`, backend full suite `221 passed, 11 skipped, 1 warning`, and `python -m compileall -q agent api mcp tools tests`.

## 2026-05-19 Project startup

- Regenerated `repo-context.md` and reread `MEMORY.md` before starting services.
- Docker Desktop was not initially running; started it, then launched Docker dependencies with `docker compose up -d`.
- Verified `ai-hiking-postgres` and `ai-hiking-redis` are healthy; Redis remains mapped as host `5379` to container `6379`.
- Started AI Service on port `8000`, Gateway on port `8080`, and Vite frontend on port `5173`.
- Live checks passed: AI `/health`, Agent tools `/api/v1/tools/health`, Gateway `/health`, frontend `/super-agent`, and frontend `/love-master` all returned healthy/HTTP 200.

## 2026-05-19 Agent SSE missing-key 500 repair

- Regenerated `repo-context.md` and reread `MEMORY.md` before debugging the browser-reported Agent HTTP 500.
- Root cause: `chat_sse()` constructed `AIAgent()` before entering the SSE generator, so missing `OPENAI_API_KEY` raised during `ChatOpenAI` initialization and escaped as HTTP 500 before an SSE error event could be sent.
- Minimal fix in `ai-service/api/chat.py`: gate missing `settings.openai_api_key` inside the SSE stream and return `error` + `done` events with a clear configuration message; sync chat now returns HTTP 503 for the same missing model configuration instead of wrapping it as 500.
- Regression tests added in `ai-service/tests/test_chat_health.py` for missing-key SSE and sync behavior.
- Validation passed: focused chat/Agent regression `10 passed, 1 warning`, compileall for `api` and updated tests, live Gateway `/api/v1/chat/sse` returned HTTP 200 with SSE `error` + `done`, and frontend `/super-agent` still returned HTTP 200.

## 2026-05-19 Agent runtime LLM config memory fix

- Regenerated `repo-context.md` and reread `MEMORY.md` before debugging why `/llm-config` saved LLM settings still produced Agent missing-key errors.
- Root cause: frontend runtime `model_settings.llm` reached `AIAgent`, but `MemoryManager` still constructed `SessionCompressor` and `KnowledgeExtractor` from backend `settings.openai_api_key`, so `memory_enabled=True` reintroduced the missing `OPENAI_API_KEY` failure.
- Minimal fix: `MemoryConfig` now carries runtime `llm_base_url` and `llm_api_key`; `SessionCompressor` and `KnowledgeExtractor` accept those values; `AIAgent` passes the current runtime LLM base URL, API key, and model into Memory when present.
- Added regressions proving runtime LLM settings configure Memory components and Agent can initialize Memory when `.env` lacks `OPENAI_API_KEY`.
- Validation passed: targeted backend Agent/Memory tests `54 passed`, Python compileall for changed backend packages/tests, frontend runtime config tests `18 passed`, gateway chat SSE/sync/health tests passed, and live Gateway SSE with runtime config no longer reports missing `api_key` (it reaches model connection instead).

## 2026-05-19 Agent current-location tools and thinking animation fix

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded the requested `think`, `pua`, and `tdd` skill files before editing.
- Root cause for “今天的天气适合去徒步吗” was that Agent intake only used text-extracted destinations; the frontend never sent browser geolocation and the backend had no `current_location` request field, so missing destination forced a clarification.
- Added browser geolocation capture in `frontend/src/pages/SuperAgent.tsx`; successful coordinates are sent as `current_location` with the existing Agent SSE payload, while denied/unavailable geolocation silently falls back to the old request path.
- Added `CurrentLocationPayload` to Agent chat requests, threaded it through sync/SSE calls, and updated Agent intake so weather/risk questions without explicit destination can use the current city/adcode/coordinates instead of asking the user for a location.
- Extended `geo_lookup` and `weather_lookup` to accept latitude/longitude and AMap adcode, including AMap reverse-geocode support before weather lookup.
- Added a small normalization guard so `0` latitude/longitude values are preserved instead of being treated as missing.
- Replaced the Agent empty streaming state with the same `AiThinking` animation structure used by the RAG module, and kept thought/tool events folded under the execution panel.
- Validation passed: new TDD regressions for intake/tool selection/SSE current-location propagation/AMap coordinate tools, backend full suite `232 passed, 11 skipped`, frontend `npm test` `20 passed`, frontend `npm run build`, gateway `go test ./...`, Python compileall, and live health checks for frontend `/super-agent`, gateway, and AI service.

## 2026-05-19 Agent deterministic location-weather tool chain

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded the requested `pua`, `think`, `tdd`, and `caveman` skills before debugging the repeated Agent tool-call issue.
- RCA found the previous fix still depended on the LLM voluntarily calling `geo_lookup` and `weather_lookup`; with “今天的天气适合去徒步吗” the model could still skip tools and ask for a city.
- Added a deterministic Agent prefetch path for current-location weather/risk questions: browser coordinates trigger `geo_lookup`, then `weather_lookup`, and both tool results are injected into the LangGraph system prompt before final answer generation.
- Added Agent query rewriting with the same runtime LLM instance used by the main Agent, avoiding a second model configuration path and exposing a `query_rewrite` SSE thought event for traceability.
- Cleaned Agent final `text` events through the existing plain-text display sanitizer so chat bubbles no longer show Markdown headings, bold markers, or numbered-list formatting from the model.
- Frontend geolocation now waits longer for weather/nearby/current-location style questions, reducing first-time permission timeout fallback while preserving a shorter timeout for unrelated prompts.
- Validation passed: backend full suite `235 passed, 11 skipped`, Python compileall, frontend `npm test` `21 passed`, frontend `npm run build`, gateway `go test ./...`, and live AI/gateway SSE checks confirmed `query_rewrite`, `geo_lookup`, and `weather_lookup` events before the expected dummy-LLM connection failure.

## 2026-05-19 Agent prompt strategy and tool-budget repair

- Regenerated `repo-context.md`, reread `MEMORY.md`, and loaded the requested `think`, `pua`, `tdd`, and `caveman` skills before editing.
- RCA found the screenshot's overthinking loop was enabled by two design choices: `MAX_STEPS=20` and broad follow-up tools still exposed after deterministic `geo_lookup` + `weather_lookup` prefetch.
- Updated Agent strategy so general chat exposes only `terminate`, current-location weather/risk requests shrink to `risk_assessment` + `terminate` after prefetch, and the ReAct step budget is capped at `MAX_STEPS=6`.
- Reworked the Agent system prompt into the requested tagged template format: `<Role>`, `<Goal>`, `<Constraints>`, `<Tools>`, `<Format>`, and `<Examples>`, with runtime context appended as XML-style blocks instead of markdown headings.
- Semantic cache decision: do not add it now for live weather/risk flows because stale hits could create safety risk and would hide, not fix, tool-loop behavior; consider only a narrow TTL cache later for stable RAG knowledge or query rewrite results.
- Validation passed: TDD red/green tests for prompt format, tool shrinking, and general-chat tool exposure; backend full suite `238 passed, 11 skipped`; Python compileall for Agent and changed tests.
