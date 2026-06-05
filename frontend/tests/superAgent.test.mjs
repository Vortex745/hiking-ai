import assert from 'node:assert/strict'
import { existsSync, readFileSync } from 'node:fs'
import { test } from 'node:test'

const source = readFileSync(new URL('../src/pages/SuperAgent.tsx', import.meta.url), 'utf8')
const ragSource = readFileSync(new URL('../src/pages/HikingRAG.tsx', import.meta.url), 'utf8')
const geminiThreadSource = readFileSync(new URL('../src/components/assistant-ui/gemini/GeminiThread.tsx', import.meta.url), 'utf8')
const apiConfigSource = readFileSync(new URL('../src/api/config.ts', import.meta.url), 'utf8')
const appSource = readFileSync(new URL('../src/App.tsx', import.meta.url), 'utf8')
const homeSource = readFileSync(new URL('../src/pages/Home.tsx', import.meta.url), 'utf8')
const indexHtml = readFileSync(new URL('../index.html', import.meta.url), 'utf8')
const floatingSidebarSource = readFileSync(new URL('../src/components/FloatingSidebar.tsx', import.meta.url), 'utf8')
const publicDir = new URL('../public/', import.meta.url)

test('RAG public entry uses hiking-rag as the canonical route', () => {
  assert.match(homeSource, /to="\/hiking-rag"/)
  assert.doesNotMatch(homeSource, /to="\/love-master"/)
  assert.match(appSource, /to="\/hiking-rag"/)
  assert.match(appSource, /<Route path="\/hiking-rag" element=\{<HikingRAG \/>\} \/>/)
  assert.match(appSource, /<Route path="\/love-master" element=\{<Navigate to="\/hiking-rag" replace \/>\} \/>/)
})

test('public pages include a search result description', () => {
  assert.match(indexHtml, /<meta name="description" content="[^"]*徒步[^"]*" \/>/)
})

test('public crawler guidance files are served as text assets', () => {
  const robotsUrl = new URL('robots.txt', publicDir)
  const llmsUrl = new URL('llms.txt', publicDir)
  assert.equal(existsSync(robotsUrl), true)
  assert.equal(existsSync(llmsUrl), true)
  assert.match(readFileSync(robotsUrl, 'utf8'), /^User-agent: \*/m)
  assert.match(readFileSync(llmsUrl, 'utf8'), /^# AI智能徒步助手/m)
  assert.match(readFileSync(llmsUrl, 'utf8'), /\[首页\]\(https:\/\/530745\.xyz\/\)/)
})

test('shared chat composer exposes accessible input and icon button names', () => {
  assert.match(geminiThreadSource, /aria-label="输入徒步问题"/)
  assert.match(geminiThreadSource, /name="message"/)
  assert.match(geminiThreadSource, /aria-label="发送消息"/)
  assert.match(geminiThreadSource, /title="发送消息"/)
  assert.match(geminiThreadSource, /aria-label="停止生成"/)
  assert.match(geminiThreadSource, /title="停止生成"/)
})

test('floating conversation sidebar gives icon-only buttons accessible names', () => {
  assert.match(floatingSidebarSource, /aria-label="关闭历史对话"/)
  assert.match(floatingSidebarSource, /title="关闭历史对话"/)
  assert.match(floatingSidebarSource, /aria-label="删除对话"/)
  assert.match(floatingSidebarSource, /title="删除对话"/)
})

test('floating conversation sidebar keeps text readable over light chat content', () => {
  assert.match(floatingSidebarSource, /bg-\[#202124\]\/95/)
  assert.match(floatingSidebarSource, /bg-white text-\[#202124\]/)
  assert.match(floatingSidebarSource, /text-white\/80 mt-0\.5/)
})

test('homepage hero content stays above the decorative video layer', () => {
  assert.match(homeSource, /<video[\s\S]*aria-hidden="true"/)
  assert.match(homeSource, /z-\[1\][^"]*pointer-events-none/)
  assert.match(homeSource, /z-\[2\][^"]*isolate/)
})

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

test('agent high-risk tool confirmation routes are configured', () => {
  assert.match(apiConfigSource, /chatConfirm: `\$\{API_BASE\}\/chat\/confirm`/)
  assert.match(apiConfigSource, /chatPending: \(chatId: string\) => `\$\{API_BASE\}\/chat\/pending\/\$\{encodeURIComponent\(chatId\)\}`/)
})

test('agent page posts confirm and reject actions for pending tools', () => {
  assert.match(source, /const handleToolConfirmation = useCallback/)
  assert.match(source, /fetch\(API\.chatConfirm/)
  assert.match(source, /confirmation_id: confirmationId/)
  assert.match(source, /action/)
  assert.match(source, /appendConfirmedToolResult/)
  assert.match(source, /onConfirmTool=\{handleToolConfirmation\}/)
})

test('agent trace panel renders high-risk confirmation controls', () => {
  assert.match(geminiThreadSource, /onConfirmTool\?: \(confirmationId: string, action: 'confirm' \| 'reject'\) => void/)
  assert.match(geminiThreadSource, /onConfirmTool/)
  assert.match(geminiThreadSource, /event\?\.type === 'approval_required'/)
  assert.match(geminiThreadSource, /event\?\.metadata\?\.confirmation_id/)
  assert.match(geminiThreadSource, /title="确认执行工具"/)
  assert.match(geminiThreadSource, /title="拒绝执行工具"/)
})

test('agent page hydrates persisted server history by stable chat id', () => {
  assert.match(source, /const CHAT_ID_KEY = 'ai-hiking-agent-chat-id'/)
  assert.match(source, /API\.chatHistory\(chatId\)/)
  assert.match(source, /normalizeServerMessages/)
  assert.match(source, /setMessages\(prev => \(prev\.length === 0 \? restored : prev\)\)/)
})

test('RAG page hydrates persisted server history by stable chat id', () => {
  assert.match(ragSource, /const CHAT_ID_KEY = 'ai-hiking-rag-chat-id'/)
  assert.match(ragSource, /API\.ragHistory\(chatId\)/)
  assert.match(ragSource, /normalizeServerMessages/)
  assert.match(ragSource, /setMessages\(prev => \(prev\.length === 0 \? restored : prev\)\)/)
  assert.match(ragSource, /buildRagQueryPayload\(text, null, undefined, chatId\)/)
})

test('RAG page exposes a visible document upload action', () => {
  assert.match(ragSource, /ref=\{fileInputRef\}/)
  assert.match(ragSource, /type="file"/)
  assert.match(ragSource, /name="file"/)
  assert.match(ragSource, /onChange=\{handleFileUpload\}/)
  assert.match(ragSource, /onUploadClick=\{\(\) => fileInputRef\.current\?\.click\(\)\}/)
  assert.match(geminiThreadSource, /onUploadClick\?: \(\) => void/)
  assert.match(geminiThreadSource, /Paperclip/)
  assert.match(geminiThreadSource, /title="上传文档"/)
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
  assert.match(geminiThreadSource, /Download/)
  assert.match(geminiThreadSource, /metadata\.download_url/)
  assert.match(geminiThreadSource, /fetch\(url\)/)
  assert.match(geminiThreadSource, /a\.download = filename/)
  assert.match(geminiThreadSource, /URL\.createObjectURL\(blob\)/)
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

test('Agent and RAG messages render markdown emphasis as bold text', () => {
  assert.match(geminiThreadSource, /const MARKDOWN_BOLD_PATTERN = \/\(\\\*\\\*\(\?=\\S\)\[\\s\\S\]\*\?\\S\\\*\\\*\)\/g/)
  assert.match(geminiThreadSource, /raw\.split\(MARKDOWN_BOLD_PATTERN\)/)
  assert.match(geminiThreadSource, /<strong key=\{i\} className="font-bold">/)
})

test('legacy ChatRoom keeps a stable chat id for Redis-backed history', () => {
  const chatRoomSource = readFileSync(new URL('../src/components/ChatRoom.tsx', import.meta.url), 'utf8')

  assert.match(chatRoomSource, /const CHAT_ID_KEY_PREFIX = 'ai-hiking-chat-id-'/)
  assert.match(chatRoomSource, /const chatIdRef = useRef\(getOrCreateChatId\(aiName\)\)/)
  assert.match(chatRoomSource, /const chatId = chatIdRef\.current/)
  assert.match(chatRoomSource, /chatHistoryEndpoint\(sseEndpoint, chatIdRef\.current\)/)
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
