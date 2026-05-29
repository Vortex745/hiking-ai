import { useState, useRef, useEffect, useCallback, useMemo } from 'react'
import { API } from '../api/config'
import { buildRuntimeModelSettings } from '../api/llmConfig'
import { createStreamConnection, SSEEvent } from '../api/sse'
import { createTypewriterStreamQueue } from '../api/typewriterStream'
import { useExternalStoreRuntime, AssistantRuntimeProvider, ThreadMessage } from "@assistant-ui/react"
import { GeminiThread } from '../components/assistant-ui/gemini/GeminiThread'
import { FloatingSidebar } from '../components/FloatingSidebar'
import { Menu, X, MessageSquare, Trash2, ClipboardList, CheckCircle2, AlertTriangle, Map } from 'lucide-react'

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

const convertMessage = (msg: Message, index: number): ThreadMessage => {
  const content: any[] = [{ type: "text", text: msg.content || (msg.isStreaming ? "" : " ") }];

  if (msg.traceEvents && msg.traceEvents.length > 0) {
    content.push({
      type: "tool-call",
      toolCallId: `trace-${index}`,
      toolName: "traceEvents",
      args: msg.traceEvents
    });
  }
  if (msg.artifacts && msg.artifacts.length > 0) {
    content.push({
      type: "tool-call",
      toolCallId: `artifact-${index}`,
      toolName: "artifacts",
      args: msg.artifacts
    });
  }

  return {
    id: `msg-${index}`,
    role: msg.role,
    content: content,
    status: (msg.isStreaming ? { type: "running" } : { type: "complete" }),
    createdAt: new Date(),
    metadata: {},
  } as unknown as ThreadMessage;
};

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

  const textStream = useMemo(
    () => createTypewriterStreamQueue(appendToLastMessage, { chunkSize: 3, intervalMs: 14 }),
    [appendToLastMessage],
  )

  useEffect(() => {
    return () => textStream.reset()
  }, [textStream])

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

  const handleSend = useCallback(async (
    textOverride?: string,
    options: { replaceFromIndex?: number } = {},
  ) => {
    const text = typeof textOverride === 'string' ? textOverride.trim() : input.trim()
    if (!text || isSending) return

    if (!activeSessionId) {
      setActiveSessionId(generateId())
    }

    setInput('')
    setSelectedScenario(null)
    setIsSending(true)
    textStream.reset()

    const now = new Date()
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
    const chatId = chatIdRef.current
    const replaceFromIndex = options.replaceFromIndex
    const contextMessages = typeof replaceFromIndex === 'number'
      ? messages.slice(0, Math.max(0, replaceFromIndex))
      : messages
    const nextUserMessage: Message = { role: 'user', content: text, time: timeStr }
    const nextAssistantMessage: Message = { role: 'assistant', content: '', isStreaming: true }

    setMessages(prev => {
      const base = typeof replaceFromIndex === 'number'
        ? prev.slice(0, Math.max(0, replaceFromIndex))
        : prev
      return [...base, nextUserMessage, nextAssistantMessage]
    })

    const finishStreaming = () => {
      finalizeStreaming()
      setIsSending(false)
      cleanupRef.current = null
    }

    try {
      const modelSettings = buildRuntimeModelSettings()
      const payload: Record<string, unknown> = { message: text, chat_id: chatId, scenario: selectedScenario }
      if (Object.keys(modelSettings).length > 0) {
        payload.model_settings = modelSettings
      }
      const needsRouteFollowupLocation = shouldRequestRouteFollowupLocation(text, contextMessages)
      const cachedRouteLocation = needsRouteFollowupLocation ? lastLocationRef.current : null
      const currentLocation = cachedRouteLocation
        || await getBrowserLocation((shouldRequestCurrentLocation(text) || needsRouteFollowupLocation) ? 10000 : 3000)
      if (currentLocation) {
        lastLocationRef.current = currentLocation
        payload.current_location = currentLocation
      } else if (needsRouteFollowupLocation && lastLocationRef.current) {
        payload.current_location = lastLocationRef.current
      }

      const cleanup = createStreamConnection(API.chatSSE, {
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
            textStream.enqueue(event.content)
          } else if (event.type === 'done') {
            textStream.finishWhenIdle(finishStreaming)
          } else if (event.type === 'error') {
            textStream.flushNow()
            appendToLastMessage(`\n\n[错误] ${event.content}`)
            finishStreaming()
          }
        },
        onError: (error: string) => {
          textStream.flushNow()
          appendToLastMessage(`\n\n[连接错误] ${error}`)
          finishStreaming()
          setConnectionStatus('error')
        },
        onDone: () => {
          textStream.finishWhenIdle(finishStreaming)
          setConnectionStatus('connected')
        },
      })
      cleanupRef.current = cleanup
    } catch (error) {
      textStream.flushNow()
      appendToLastMessage(`\n\n[错误] ${error instanceof Error ? error.message : '请求失败'}`)
      finishStreaming()
    }
  }, [input, isSending, activeSessionId, selectedScenario, messages, appendToLastMessage, appendTraceEvent, appendArtifact, finalizeStreaming, textStream])

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

  /** Regenerate: remove the last assistant response, re-send the last user prompt */
  const handleRegenerate = useCallback(() => {
    if (isSending) return
    // Find the last user message (reverse search for TS < es2023 compat)
    let lastUserIdx = -1
    for (let i = messages.length - 1; i >= 0; i--) {
      if (messages[i].role === 'user') { lastUserIdx = i; break }
    }
    if (lastUserIdx === -1) return
    const lastUserText = messages[lastUserIdx].content
    handleSend(lastUserText, { replaceFromIndex: lastUserIdx })
  }, [messages, isSending, handleSend])

  const runtime = useExternalStoreRuntime({
    messages: messages.map(convertMessage),
    isRunning: isSending || messages.some(m => m.isStreaming),
    onNew: async (appendMessage) => {
      const text = appendMessage.content.find((p): p is {type: "text", text: string} => p.type === "text")?.text || "";
      handleSend(text);
    },
    onCancel: async () => {
      if (cleanupRef.current) {
        cleanupRef.current();
        cleanupRef.current = null;
      }
      textStream.reset();
      finalizeStreaming();
      setIsSending(false)
    }
  });

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="flex h-full w-full overflow-hidden relative">
        {/* Floating Sidebar (Drawer) */}
        <FloatingSidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          sessions={sessions}
          activeSessionId={activeSessionId}
          onNewSession={createNewSession}
          onLoadSession={loadSession}
          onDeleteSession={deleteSession}
        />

        {/* Main Gemini Thread Area */}
        <div className="flex-1 flex flex-col relative overflow-hidden bg-transparent">
          {/* Header Toggle Button */}
          {!sidebarOpen && (
            <button
              onClick={() => setSidebarOpen(true)}
              className="absolute top-6 left-6 z-40 w-10 h-10 flex items-center justify-center rounded-full bg-black/40 backdrop-blur-md border border-white/10 text-white/80 hover:text-white hover:bg-black/50 transition-colors duration-150 ease-[var(--ease-out)] shadow-sm press-scale"
              title="展开历史对话"
            >
              <Menu className="w-5 h-5" />
            </button>
          )}
          <GeminiThread
            emptyTitle="告诉我你的徒步计划，我将为你规划路线、安排任务，并提供安全建议。"
            onRegenerate={handleRegenerate}
            realMessageCount={messages.length}
          />
        </div>
      </div>
    </AssistantRuntimeProvider>
  )
}

export default SuperAgent
