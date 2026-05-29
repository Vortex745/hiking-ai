import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { test } from 'node:test'

const source = readFileSync(new URL('../src/pages/SuperAgent.tsx', import.meta.url), 'utf8')
const ragSource = readFileSync(new URL('../src/pages/LoveMaster.tsx', import.meta.url), 'utf8')
const geminiThreadSource = readFileSync(new URL('../src/components/assistant-ui/gemini/GeminiThread.tsx', import.meta.url), 'utf8')

test('quick actions send explicit Agent scenario', () => {
  assert.match(source, /scenario: 'route_plan'/)
  assert.match(source, /scenario: 'gear_check'/)
  assert.match(source, /scenario: 'risk_assessment'/)
  assert.match(source, /const payload: Record<string, unknown> = \{ message: text, chat_id: chatId, scenario: selectedScenario \}/)
})

test('agent requests include saved runtime LLM settings', () => {
  assert.match(source, /import \{ buildRuntimeModelSettings \} from '\.\.\/api\/llmConfig'/)
  assert.match(source, /const modelSettings = buildRuntimeModelSettings\(\)/)
  assert.match(source, /payload\.model_settings = modelSettings/)
  assert.match(source, /body: JSON\.stringify\(payload\)/)
})

test('agent requests include browser current location when available', () => {
  assert.match(source, /function getBrowserLocation/)
  assert.match(source, /navigator\.geolocation\.getCurrentPosition/)
  assert.match(source, /await getBrowserLocation\(/)
  assert.match(source, /payload\.current_location = currentLocation/)
})

test('weather and nearby questions wait longer for browser location authorization', () => {
  assert.match(source, /function shouldRequestCurrentLocation/)
  assert.match(source, /天气\|适合\|能去\|可以去\|徒步吗\|去徒步\|附近\|周边\|当前位置\|我这里\|我这边/)
  assert.match(source, /getBrowserLocation\(\(shouldRequestCurrentLocation\(text\) \|\| needsRouteFollowupLocation\) \? 10000 : 3000\)/)
})

test('route recommendation follow-up can reuse authorized browser location', () => {
  assert.match(source, /const lastLocationRef = useRef<BrowserLocation \| null>\(null\)/)
  assert.match(source, /function shouldRequestRouteFollowupLocation/)
  assert.match(source, /要不要我继续给你推荐附近的户外徒步路线/)
  assert.match(source, /lastLocationRef\.current = currentLocation/)
  assert.match(source, /payload\.current_location = lastLocationRef\.current/)
})

test('agent trace events stay out of primary assistant text', () => {
  const thoughtBranch = /if \(event\.type === 'thought'\) \{\s*appendTraceEvent\(event\)/s
  const toolCallBranch = /else if \(event\.type === 'tool_call'\) \{\s*appendTraceEvent\(event\)/s
  const toolResultBranch = /else if \(event\.type === 'tool_result'\) \{\s*appendTraceEvent\(event\)/s

  assert.match(source, thoughtBranch)
  assert.match(source, toolCallBranch)
  assert.match(source, toolResultBranch)
  assert.match(geminiThreadSource, /toolName === "traceEvents"/)
  assert.match(geminiThreadSource, /LifecycleHoverPanel/)
  assert.match(geminiThreadSource, /Agent 技术生命周期/)
})

test('artifact events render in artifact area', () => {
  assert.match(source, /else if \(event\.type === 'artifact'\) \{\s*appendArtifact\(event\)/s)
  assert.match(source, /msg\.artifacts && msg\.artifacts\.length > 0/)
})

test('agent empty streaming state uses RAG thinking animation', () => {
  assert.match(geminiThreadSource, /function AiThinking/)
  assert.match(geminiThreadSource, /<AiThinking(?:\s+text=\{thinkingText\})? \/>/)
  assert.doesNotMatch(geminiThreadSource, /typing-indicator/)
  assert.doesNotMatch(geminiThreadSource, /▌/)
})

test('message overflow menu exposes the technical lifecycle on hover', () => {
  assert.match(geminiThreadSource, /title="思考流程"/)
  assert.match(geminiThreadSource, /onMouseEnter=\{\(\) => setShowLifecycle\(true\)\}/)
  assert.match(geminiThreadSource, /RAG 技术生命周期/)
})

test('Agent and RAG stream text through the client-side typewriter queue', () => {
  assert.match(source, /createTypewriterStreamQueue/)
  assert.match(source, /textStream\.enqueue\(event\.content\)/)
  assert.match(source, /textStream\.finishWhenIdle\(finishStreaming\)/)
  assert.match(ragSource, /createTypewriterStreamQueue/)
  assert.match(ragSource, /textStream\.enqueue\(event\.content\)/)
  assert.match(ragSource, /textStream\.finishWhenIdle\(finishStreaming\)/)
})

test('regenerate replaces the stale turn atomically instead of blanking the thread', () => {
  assert.match(source, /handleSend\(lastUserText, \{ replaceFromIndex: lastUserIdx \}\)/)
  assert.match(ragSource, /handleSend\(lastUserText, \{ replaceFromIndex: lastUserIdx \}\)/)
  assert.doesNotMatch(source, /setMessages\(prev => prev\.slice\(0, lastUserIdx\)\)/)
  assert.doesNotMatch(ragSource, /setMessages\(prev => prev\.slice\(0, lastUserIdx\)\)/)
  assert.doesNotMatch(source, /setTimeout\(\(\) => handleSend\(lastUserText\), 0\)/)
  assert.doesNotMatch(ragSource, /setTimeout\(\(\) => handleSend\(lastUserText\), 0\)/)
})

test('lifecycle panel can be pinned and dragged inside the page', () => {
  assert.match(geminiThreadSource, /aria-label=\{pinned \? '取消钉住流程' : '钉住流程'\}/)
  assert.match(geminiThreadSource, /data-lifecycle-panel=\{pinned \? 'pinned' : 'hover'\}/)
  assert.match(geminiThreadSource, /handleLifecycleDragStart/)
  assert.match(geminiThreadSource, /window\.addEventListener\('pointermove'/)
  assert.match(geminiThreadSource, /clampLifecyclePosition/)
})
