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

interface Message {
  role: 'user' | 'assistant'
  content: string
  time?: string
  isStreaming?: boolean
  traceEvents?: AgentTraceEvent[]
  artifacts?: AgentArtifact[]
}

interface ChatSession {
  id: string
  title: string
  date: string
  messages: Message[]
}

type AgentScenario = 'route_plan' | 'gear_check' | 'risk_assessment' | 'report_export'
type AgentTraceEvent = Pick<SSEEvent, 'type' | 'content' | 'metadata'>
type AgentArtifact = Pick<SSEEvent, 'content' | 'metadata'>
type BrowserLocation = {
  latitude: number
  longitude: number
  accuracy?: number
  source: 'browser'
}

function shouldRequestCurrentLocation(text: string) {
  return /天气|适合|能去|可以去|徒步吗|去徒步|附近|周边|当前位置|我这里|我这边/.test(text)
}

function isAffirmativeRouteReply(text: string) {
  return /^(需要|要|好|好的|可以|行|安排|推荐|继续)$/.test(text.trim())
}

function shouldRequestRouteFollowupLocation(text: string, messages: Message[]) {
  if (!isAffirmativeRouteReply(text)) return false
  const lastAssistant = [...messages].reverse().find(message => message.role === 'assistant')
  return Boolean(lastAssistant?.content.includes('要不要我继续给你推荐附近的户外徒步路线'))
}

const quickTags = [
  { icon: ClipboardList, text: '生成行程', scenario: 'route_plan' as AgentScenario },
  { icon: CheckCircle2, text: '检查装备', scenario: 'gear_check' as AgentScenario },
  { icon: AlertTriangle, text: '风险提醒', scenario: 'risk_assessment' as AgentScenario },
  { icon: Map, text: '推荐路线', scenario: 'route_plan' as AgentScenario },
]

const traceLabels: Partial<Record<SSEEvent['type'], string>> = {
  thought: '思考',
  tool_call: '工具调用',
  tool_result: '工具结果',
  approval_required: '需要确认',
}

const STORAGE_KEY = 'ai-hiking-agent-chat'
const SESSIONS_KEY = 'ai-hiking-agent-sessions'
const CHAT_ID_KEY = 'ai-hiking-agent-chat-id'
const ACTIVE_SESSION_KEY = 'ai-hiking-agent-active-session'

function createChatId() {
  if (typeof crypto !== 'undefined' && 'randomUUID' in crypto) {
    return `chat-${crypto.randomUUID()}`
  }
  return `chat-${Date.now()}-${Math.random().toString(36).slice(2)}`
}

function getOrCreateChatId() {
  try {
    const saved = localStorage.getItem(CHAT_ID_KEY)
    if (saved) return saved

    const next = createChatId()
    localStorage.setItem(CHAT_ID_KEY, next)
    return next
  } catch {
    return createChatId()
  }
}

function generateId() {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function getTodayDate() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}

function loadSessions(): ChatSession[] {
  try {
    const saved = localStorage.getItem(SESSIONS_KEY)
    return saved ? JSON.parse(saved) : []
  } catch { return [] }
}

function saveSessions(sessions: ChatSession[]) {
  try { localStorage.setItem(SESSIONS_KEY, JSON.stringify(sessions)) } catch { /* ignore */ }
}

function getBrowserLocation(timeout = 3000): Promise<BrowserLocation | null> {
  if (typeof navigator === 'undefined' || !navigator.geolocation) {
    return Promise.resolve(null)
  }

  return new Promise(resolve => {
    navigator.geolocation.getCurrentPosition(
      position => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
          source: 'browser',
        })
      },
      () => resolve(null),
      {
        enableHighAccuracy: false,
        maximumAge: 10 * 60 * 1000,
        timeout,
      },
    )
  })
}

function AiThinking() {
  return (
    <div className="ai-thinking" role="status" aria-label="AI 正在思考">
      <span className="ai-thinking-core">
        <span />
        <span />
        <span />
      </span>
      <span className="ai-thinking-line" />
      <span className="ai-thinking-label">思考中</span>
    </div>
  )
}

function SuperAgent() {
  const [messages, setMessages] = useState<Message[]>(() => {
    try {
      const saved = localStorage.getItem(STORAGE_KEY)
      return saved ? JSON.parse(saved) : []
    } catch { return [] }
  })
  const [sessions, setSessions] = useState<ChatSession[]>(loadSessions)
  const [activeSessionId, setActiveSessionId] = useState<string | null>(() => {
    try {
      const saved = localStorage.getItem(ACTIVE_SESSION_KEY)
      if (saved) return saved
      const savedMessages = localStorage.getItem(STORAGE_KEY)
      if (savedMessages) {
        const msgs = JSON.parse(savedMessages)
        if (msgs.length > 0) return generateId()
      }
      return null
    } catch { return null }
  })
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [input, setInput] = useState('')
  const [selectedScenario, setSelectedScenario] = useState<AgentScenario | null>(null)
  const [isSending, setIsSending] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connected' | 'error'>('disconnected')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const cleanupRef = useRef<(() => void) | null>(null)
  const chatIdRef = useRef(getOrCreateChatId())
  const lastLocationRef = useRef<BrowserLocation | null>(null)

  // Persist
  useEffect(() => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(messages)) } catch { /* ignore */ }
  }, [messages])

  // Persist sessions
  useEffect(() => {
    saveSessions(sessions)
  }, [sessions])

  useEffect(() => {
    if (activeSessionId) {
      try { localStorage.setItem(ACTIVE_SESSION_KEY, activeSessionId) } catch { /* ignore */ }
    } else {
      try { localStorage.removeItem(ACTIVE_SESSION_KEY) } catch { /* ignore */ }
    }
  }, [activeSessionId])

  useEffect(() => {
    if (!activeSessionId || messages.length === 0) return
    const lastMsg = messages[messages.length - 1]
    if (lastMsg?.isStreaming) return
    const firstUserMsg = messages.find(m => m.role === 'user')
    const title = firstUserMsg ? firstUserMsg.content.slice(0, 30) + (firstUserMsg.content.length > 30 ? '...' : '') : '新对话'
    setSessions(prev => {
      const existing = prev.find(s => s.id === activeSessionId)
      if (existing) {
        return prev.map(s => s.id === activeSessionId ? { ...s, title, date: getTodayDate(), messages } : s)
      }
      return [{ id: activeSessionId, title, date: getTodayDate(), messages }, ...prev].slice(0, 50)
    })
  }, [activeSessionId, messages])

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => { scrollToBottom() }, [messages, scrollToBottom])

  useEffect(() => { return () => { cleanupRef.current?.() } }, [])

  // Health check
  const checkHealth = useCallback(async () => {
    try {
      const resp = await fetch(API.chatHealth, { method: 'GET' })
      if (resp.ok) setConnectionStatus('connected')
      else setConnectionStatus('error')
    } catch { setConnectionStatus('error') }
  }, [])

  useEffect(() => {
    checkHealth()
    const id = setInterval(checkHealth, 30000)
    return () => clearInterval(id)
  }, [checkHealth])

  const appendToLastMessage = useCallback((text: string) => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last && last.role === 'assistant') {
        updated[updated.length - 1] = { ...last, content: last.content + text, isStreaming: true }
      }
      return updated
    })
  }, [])

  const appendTraceEvent = useCallback((event: SSEEvent) => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last && last.role === 'assistant') {
        updated[updated.length - 1] = {
          ...last,
          traceEvents: [...(last.traceEvents || []), {
            type: event.type,
            content: event.content,
            metadata: event.metadata,
          }],
          isStreaming: true,
        }
      }
      return updated
    })
  }, [])

  const appendArtifact = useCallback((event: SSEEvent) => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last && last.role === 'assistant') {
        updated[updated.length - 1] = {
          ...last,
          artifacts: [...(last.artifacts || []), {
            content: event.content,
            metadata: event.metadata,
          }],
          isStreaming: true,
        }
      }
      return updated
    })
  }, [])

  const finalizeStreaming = useCallback(() => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last?.isStreaming) updated[updated.length - 1] = { ...last, isStreaming: false }
      return updated
    })
  }, [])

  const createNewSession = useCallback(() => {
    if (messages.length > 0 && activeSessionId) {
      const firstUserMsg = messages.find(m => m.role === 'user')
      const title = firstUserMsg ? firstUserMsg.content.slice(0, 30) + (firstUserMsg.content.length > 30 ? '...' : '') : '新对话'
      setSessions(prev => {
        const filtered = prev.filter(s => s.id !== activeSessionId)
        return [{ id: activeSessionId, title, date: getTodayDate(), messages }, ...filtered].slice(0, 50)
      })
    }
    const newId = generateId()
    setActiveSessionId(newId)
    setMessages([])
    const next = createChatId()
    localStorage.setItem(CHAT_ID_KEY, next)
    chatIdRef.current = next
    try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
  }, [messages, activeSessionId])

  const loadSession = useCallback((session: ChatSession) => {
    if (activeSessionId && messages.length > 0) {
      const firstUserMsg = messages.find(m => m.role === 'user')
      const title = firstUserMsg ? firstUserMsg.content.slice(0, 30) + (firstUserMsg.content.length > 30 ? '...' : '') : '新对话'
      setSessions(prev => {
        const filtered = prev.filter(s => s.id !== activeSessionId)
        const existing = prev.find(s => s.id === activeSessionId)
        if (existing) {
          return [{ ...existing, title, date: getTodayDate(), messages }, ...filtered].slice(0, 50)
        }
        return [{ id: activeSessionId, title, date: getTodayDate(), messages }, ...filtered].slice(0, 50)
      })
    }
    setActiveSessionId(session.id)
    setMessages(session.messages)
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(session.messages)) } catch { /* ignore */ }
  }, [activeSessionId, messages])

  const deleteSession = useCallback((e: React.MouseEvent, sessionId: string) => {
    e.stopPropagation()
    setSessions(prev => prev.filter(s => s.id !== sessionId))
    if (activeSessionId === sessionId) {
      setActiveSessionId(null)
      setMessages([])
      const next = createChatId()
      localStorage.setItem(CHAT_ID_KEY, next)
      chatIdRef.current = next
      try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
    }
  }, [activeSessionId])

  const handleSend = useCallback(async () => {
    const text = input.trim()
    if (!text || isSending) return

    if (!activeSessionId) {
      setActiveSessionId(generateId())
    }

    setInput('')
    setSelectedScenario(null)
    setIsSending(true)

    const now = new Date()
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
    const chatId = chatIdRef.current

    setMessages(prev => [...prev, { role: 'user', content: text, time: timeStr }])
    setMessages(prev => [...prev, { role: 'assistant', content: '', isStreaming: true }])

    try {
      const modelSettings = buildRuntimeModelSettings()
      const payload: Record<string, unknown> = { message: text, chat_id: chatId, scenario: selectedScenario }
      if (Object.keys(modelSettings).length > 0) {
        payload.model_settings = modelSettings
      }
      const needsRouteFollowupLocation = shouldRequestRouteFollowupLocation(text, messages)
      const cachedRouteLocation = needsRouteFollowupLocation ? lastLocationRef.current : null
      const currentLocation = cachedRouteLocation
        || await getBrowserLocation((shouldRequestCurrentLocation(text) || needsRouteFollowupLocation) ? 10000 : 3000)
      if (currentLocation) {
        lastLocationRef.current = currentLocation
        payload.current_location = currentLocation
      } else if (needsRouteFollowupLocation && lastLocationRef.current) {
        payload.current_location = lastLocationRef.current
      }

      const cleanup = await createStreamConnection(API.chatSSE, {
        method: 'POST',
        body: JSON.stringify(payload),
        onOpen: () => setConnectionStatus('connected'),
        onMessage: (event: SSEEvent) => {
          if (event.type === 'thought') {
            appendTraceEvent(event)
          } else if (event.type === 'tool_call') {
            appendTraceEvent(event)
          } else if (event.type === 'tool_result') {
            appendTraceEvent(event)
          } else if (event.type === 'approval_required') {
            appendTraceEvent(event)
          } else if (event.type === 'artifact') {
            appendArtifact(event)
          } else if (event.type === 'text') {
            appendToLastMessage(event.content)
          } else if (event.type === 'done') {
            finalizeStreaming()
          } else if (event.type === 'error') {
            appendToLastMessage(`\n\n[错误] ${event.content}`)
            finalizeStreaming()
          }
        },
        onError: (error: string) => {
          appendToLastMessage(`\n\n[连接错误] ${error}`)
          finalizeStreaming()
          setConnectionStatus('error')
        },
        onDone: () => setConnectionStatus('connected'),
      })
      cleanupRef.current = cleanup
    } catch (error) {
      appendToLastMessage(`\n\n[错误] ${error instanceof Error ? error.message : '请求失败'}`)
      finalizeStreaming()
    } finally {
      setIsSending(false)
    }
  }, [input, isSending, activeSessionId, selectedScenario, messages, appendToLastMessage, appendTraceEvent, appendArtifact, finalizeStreaming])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleClear = () => {
    setMessages([])
    try {
      localStorage.removeItem(STORAGE_KEY)
      const next = createChatId()
      localStorage.setItem(CHAT_ID_KEY, next)
      chatIdRef.current = next
    } catch { /* ignore */ }
  }

  return (
    <div className="flex h-[calc(100vh-56px)] overflow-hidden">
      {/* Left Sidebar - Chat History */}
      <div
        className="chat-sidebar border-r border-border bg-white flex flex-col max-md:hidden"
        data-open={sidebarOpen}
        style={{ width: 260, minWidth: 260 }}
      >
        <div className="chat-sidebar-inner" style={{ width: 260 }}>
          <div className="p-4 border-b border-border">
            <button
              onClick={createNewSession}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-primary text-white rounded-sm text-sm transition-all duration-200 ease-[var(--ease-out)] hover:bg-primary-hover active:scale-[0.97]"
            >
              <MessageSquare className="w-4 h-4" />
              新建对话
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-3">
            <div className="text-xs text-text-muted mb-2 px-1">对话记录</div>
            {sessions.length === 0 && (
              <div className="text-sm text-text-secondary text-center py-8 px-2">
                暂无历史对话<br />
                <span className="text-xs">点击上方新建对话开始</span>
              </div>
            )}
            {sessions.map((session) => (
              <div
                key={session.id}
                onClick={() => loadSession(session)}
                className={`group flex items-center gap-2 px-3 py-2.5 rounded-sm cursor-pointer transition-all duration-200 ease-[var(--ease-out)] mb-1 ${
                  activeSessionId === session.id
                    ? 'bg-primary/10 text-primary-light'
                    : 'hover:bg-black/[0.02] text-text-primary'
                }`}
              >
                <MessageSquare className="w-4 h-4 shrink-0 text-text-muted" />
                <div className="flex-1 min-w-0">
                  <div className="text-sm truncate">{session.title}</div>
                  <div className="text-[11px] text-text-muted">{session.date}</div>
                </div>
                <button
                  onClick={(e) => deleteSession(e, session.id)}
                  className="opacity-0 group-hover:opacity-100 p-1 rounded hover:bg-red-50 text-text-muted hover:text-red-500 transition-all duration-200"
                  title="删除对话"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-center pt-6 pb-4 shrink-0 relative">
          <button
            onClick={() => setSidebarOpen(prev => !prev)}
            className="absolute left-4 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center rounded-sm text-text-muted hover:text-text-primary hover:bg-black/[0.04] transition-all duration-200 ease-[var(--ease-out)] active:scale-90"
            title={sidebarOpen ? '收起侧边栏' : '展开侧边栏'}
          >
            <div className="t-icon-swap" data-state={sidebarOpen ? 'a' : 'b'}>
              <span className="t-icon flex items-center justify-center" data-icon="a">
                <PanelLeftClose className="w-[18px] h-[18px]" />
              </span>
              <span className="t-icon flex items-center justify-center" data-icon="b">
                <PanelLeftOpen className="w-[18px] h-[18px]" />
              </span>
            </div>
          </button>
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-1">Agent 模块</h2>
            <p className="text-sm text-text-secondary">
              行动对话 · 行程规划与执行
              <span className={`ml-2 inline-block w-2 h-2 rounded-full align-middle ${
                connectionStatus === 'connected' ? 'bg-green-500' :
                connectionStatus === 'error' ? 'bg-red-500' : 'bg-gray-400'
              }`} />
            </p>
            <ConversationMemoryMeter messages={messages} />
          </div>
        </div>

        <div className="flex flex-1 overflow-hidden">
          {/* Messages Area */}
          <div className="flex-1 flex flex-col overflow-hidden">
            {/* Scrollable messages */}
            <div className="flex-1 overflow-y-auto scrollbar-thin px-8">
              {messages.length === 0 && (
                <div className="flex items-start gap-3 bg-white border border-border rounded-lg p-4 mb-5 max-w-[600px]">
                  <div className="w-10 h-10 rounded-lg bg-primary/10 text-primary-light flex items-center justify-center shrink-0">
                    <Flag className="w-6 h-6" strokeWidth={1.5} />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold mb-1 text-text-primary">告诉我你的徒步计划，我将为你规划路线、安排任务，并提供安全建议。</h4>
                    <p className="text-[13px] text-text-secondary leading-relaxed">你可以描述目的地、天数、偏好或关注点，我会帮助你制定更合适的行程。</p>
                  </div>
                </div>
              )}

              <div className="flex flex-col gap-4">
                {messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`flex gap-3 items-start ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
                    style={{ animation: `msgEnter 300ms var(--ease-out) ${Math.min(i * 40, 200)}ms both` }}
                  >
                    <div className={`w-9 h-9 rounded-full flex items-center justify-center text-white shrink-0 transition-transform duration-200 ease-[var(--ease-out)] hover:scale-105 ${msg.role === 'user' ? 'bg-primary' : 'bg-primary-light'}`}>
                      {msg.role === 'user' ? <User className="w-5 h-5" /> : <Mountain className="w-5 h-5" />}
                    </div>
                    <div className="max-w-[600px]">
                      <div className={`rounded-lg p-3 text-sm leading-relaxed transition-shadow duration-200 ease-[var(--ease-out)] hover:shadow-sm ${msg.role === 'user' ? 'bg-[#f5f5f0] text-text-primary' : 'bg-white border border-border'}`}>
                        {msg.role === 'assistant' ? (
                          <>
                            {msg.content || msg.isStreaming ? (
                              <span>
                                {msg.content && (
                                  <span className="whitespace-pre-wrap">
                                    {msg.content}
                                  </span>
                                )}
                                {!msg.content && msg.isStreaming && <AiThinking />}
                                {msg.content && msg.isStreaming && <span className="typing-indicator">▌</span>}
                              </span>
                            ) : (
                              <AiThinking />
                            )}
                            {msg.artifacts?.length ? (
                              <div className="mt-3 border-t border-border pt-3">
                                {msg.artifacts.map((artifact, artifactIndex) => (
                                  <div key={artifactIndex} className="flex items-start gap-2 text-xs text-text-secondary">
                                    <ClipboardList className="w-4 h-4 text-primary-light mt-0.5 shrink-0" />
                                    <span>{artifact.content}</span>
                                  </div>
                                ))}
                              </div>
                            ) : null}
                            {msg.traceEvents?.length ? (
                              <details className="mt-3 border-t border-border pt-3 text-xs text-text-secondary">
                                <summary className="cursor-pointer text-text-muted hover:text-primary-light">执行过程</summary>
                                <div className="mt-2 space-y-2">
                                  {msg.traceEvents.map((trace, traceIndex) => (
                                    <div key={traceIndex} className="leading-relaxed">
                                      <span className="font-medium text-text-primary">{traceLabels[trace.type] || trace.type}：</span>
                                      <span>{trace.content}</span>
                                    </div>
                                  ))}
                                </div>
                              </details>
                            ) : null}
                          </>
                        ) : (
                          <span>{msg.content}</span>
                        )}
                      </div>
                      {msg.time && (
                        <div className={`flex items-center gap-2 mt-1 ${msg.role === 'user' ? 'justify-start' : 'justify-end'}`}>
                          <span className="text-xs text-text-muted">{msg.time}</span>
                          {msg.role === 'assistant' && !msg.isStreaming && (
                            <span className="flex items-center gap-1">
                              <button className="text-text-muted hover:text-primary-light p-1 transition-all duration-200 ease-[var(--ease-out)] active:scale-90"><ThumbsUp className="w-4 h-4" /></button>
                              <button className="text-text-muted hover:text-primary-light p-1 transition-all duration-200 ease-[var(--ease-out)] active:scale-90"><ThumbsDown className="w-4 h-4" /></button>
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="shrink-0 px-8 pt-4 pb-6 border-t border-border bg-white">
              <div className="flex items-center gap-3 bg-bg-body rounded-lg px-4 py-2 border border-border transition-all duration-200 ease-[var(--ease-out)] focus-within:border-primary/40 focus-within:shadow-[0_0_0_3px_rgba(45,106,79,0.08)]">
                <input
                  id="agent-chat-input"
                  name="agent-chat-input"
                  type="text"
                  placeholder="输入你的徒步计划需求..."
                  value={input}
                  onChange={(e) => {
                    setInput(e.target.value)
                    setSelectedScenario(null)
                  }}
                  onKeyDown={handleKeyDown}
                  className="flex-1 bg-transparent outline-none text-sm text-text-primary py-2 placeholder:text-text-muted"
                />
                <div className="flex items-center gap-2">
                  <button
                    className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-border text-text-muted transition-all duration-200 ease-[var(--ease-out)] active:scale-90"
                    type="button"
                    aria-label="添加图片"
                    title="添加图片"
                  >
                    <Image className="w-[18px] h-[18px]" />
                  </button>
                  <button
                    className="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center hover:bg-primary-hover transition-all duration-200 ease-[var(--ease-out)] disabled:bg-text-muted disabled:cursor-not-allowed active:scale-[0.93]"
                    onClick={handleSend}
                    disabled={!input.trim() || isSending}
                    type="button"
                    aria-label="发送"
                    title="发送"
                  >
                    <Send className="w-[18px] h-[18px]" />
                  </button>
                </div>
              </div>
              <div className="flex gap-2.5 mt-3 flex-wrap">
                {quickTags.map((tag) => (
                  <button
                    key={tag.text}
                    className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-bg-body border rounded-full text-[13px] transition-all duration-200 ease-[var(--ease-out)] active:scale-[0.96] ${
                      selectedScenario === tag.scenario && input === tag.text
                        ? 'border-primary-light text-primary-light bg-primary/[0.05]'
                        : 'border-border text-text-secondary hover:border-primary-light hover:text-primary-light hover:bg-primary/[0.05]'
                    }`}
                    onClick={() => {
                      setInput(tag.text)
                      setSelectedScenario(tag.scenario)
                    }}
                  >
                    <tag.icon className="w-3.5 h-3.5" />
                    <span>{tag.text}</span>
                  </button>
                ))}
                {messages.length > 0 && (
                  <button
                    className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-bg-body border border-border rounded-full text-[13px] text-text-muted hover:text-red-500 hover:border-red-300 transition-all duration-200 ease-[var(--ease-out)] active:scale-[0.96]"
                    onClick={handleClear}
                  >
                    清空对话
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SuperAgent
