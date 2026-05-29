import { useState, useRef, useEffect, useCallback, useMemo } from 'react'
import { MessageSquare, Trash2, Menu, X } from 'lucide-react'
import { API } from '../api/config'
import { createStreamConnection, SSEEvent } from '../api/sse'
import { createTypewriterStreamQueue } from '../api/typewriterStream'
import { buildRagQueryPayload, buildRuntimeModelSettings } from '../api/llmConfig'
import { applyRagStreamEvent, RagSearchSummary } from '../api/ragStream'
import ConversationMemoryMeter from '../components/ConversationMemoryMeter'
import { useExternalStoreRuntime, AssistantRuntimeProvider, ThreadMessage } from "@assistant-ui/react"
import { GeminiThread } from '../components/assistant-ui/gemini/GeminiThread'
import { FloatingSidebar } from '../components/FloatingSidebar'

interface Message {
  role: 'user' | 'assistant'
  content: string
  time?: string
  isStreaming?: boolean
  processSteps?: string[]
  searchSummary?: RagSearchSummary | null
}

interface ChatSession {
  id: string
  title: string
  date: string
  messages: Message[]
}

const STORAGE_KEY = 'ai-hiking-rag-chat'
const SESSIONS_KEY = 'ai-hiking-rag-sessions'
const ACTIVE_SESSION_KEY = 'ai-hiking-rag-active-session'

function generateId() {
  return `session-${Date.now()}-${Math.random().toString(36).slice(2, 9)}`
}

function getTodayDate() {
  const now = new Date()
  return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
}

function sourceLabel(source: string) {
  if (source === 'feishu') return '飞书'
  if (source === 'upload') return '上传文档'
  if (source === 'unknown') return '未知来源'
  return source
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

const convertMessage = (msg: Message, index: number): ThreadMessage => {
  const content: any[] = [{ type: "text", text: msg.content || (msg.isStreaming ? "" : " ") }];

  if (msg.processSteps && msg.processSteps.length > 0) {
    content.push({
      type: "tool-call",
      toolCallId: `step-${index}`,
      toolName: "processSteps",
      args: msg.processSteps
    });
  }
  if (msg.searchSummary) {
    content.push({
      type: "tool-call",
      toolCallId: `search-${index}`,
      toolName: "searchSummary",
      args: msg.searchSummary
    });
  }

  return {
    id: `msg-${index}`,
    role: msg.role,
    content: content as any,
    status: (msg.isStreaming ? { type: "running" } : { type: "complete" }) as any,
    createdAt: new Date(),
    metadata: {},
  } as unknown as ThreadMessage;
};

function LoveMaster() {
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
  const [isSending, setIsSending] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<'disconnected' | 'connected' | 'error'>('disconnected')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const cleanupRef = useRef<(() => void) | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  // Persist messages
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

  useEffect(() => {
    return () => { cleanupRef.current?.() }
  }, [])

  // Health check
  const checkHealth = useCallback(async () => {
    try {
      const resp = await fetch(API.ragHealth, { method: 'GET' })
      if (resp.ok) setConnectionStatus('connected')
      else setConnectionStatus('error')
    } catch { setConnectionStatus('error') }
  }, [])

  useEffect(() => {
    checkHealth()
    const id = setInterval(checkHealth, 30000)
    return () => clearInterval(id)
  }, [checkHealth])

  const updateLastAssistant = useCallback((updater: (message: Message) => Message) => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last && last.role === 'assistant') {
        updated[updated.length - 1] = updater(last)
      }
      return updated
    })
  }, [])

  const appendToLastMessage = useCallback((text: string) => {
    updateLastAssistant(last => ({ ...last, content: last.content + text, isStreaming: true }))
  }, [updateLastAssistant])

  const textStream = useMemo(
    () => createTypewriterStreamQueue(appendToLastMessage, { chunkSize: 3, intervalMs: 14 }),
    [appendToLastMessage],
  )

  useEffect(() => {
    return () => textStream.reset()
  }, [textStream])

  const applyStreamEventToLastMessage = useCallback((event: SSEEvent) => {
    updateLastAssistant(last => {
      const next = applyRagStreamEvent({
        content: last.content,
        processSteps: last.processSteps ?? [],
        searchSummary: last.searchSummary ?? null,
      }, event)

      return {
        ...last,
        content: next.content,
        processSteps: next.processSteps,
        searchSummary: next.searchSummary,
        isStreaming: true,
      }
    })
  }, [updateLastAssistant])

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
    setIsSending(true)
    textStream.reset()

    const now = new Date()
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
    const replaceFromIndex = options.replaceFromIndex
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
      const cleanup = createStreamConnection(API.ragQuery, {
        method: 'POST',
        body: JSON.stringify(buildRagQueryPayload(text, null)),
        onOpen: () => setConnectionStatus('connected'),
        onMessage: (event: SSEEvent) => {
          if (event.type === 'done') {
            textStream.finishWhenIdle(finishStreaming)
          } else if (event.type === 'error') {
            textStream.flushNow()
            appendToLastMessage(`\n\n[错误] ${event.content}`)
            finishStreaming()
          } else if (event.type === 'text') {
            textStream.enqueue(event.content)
          } else {
            applyStreamEventToLastMessage(event)
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
  }, [input, isSending, activeSessionId, appendToLastMessage, applyStreamEventToLastMessage, finalizeStreaming, textStream])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    const formData = new FormData()
    formData.append('file', file)
    const runtimeModelSettings = buildRuntimeModelSettings()
    if (Object.keys(runtimeModelSettings).length > 0) {
      formData.append('model_settings', JSON.stringify(runtimeModelSettings))
    }

    try {
      const resp = await fetch(API.ragUpload, { method: 'POST', body: formData })
      if (resp.ok) {
        const data = await resp.json()
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `已上传文档「${data.filename}」，共切分为 ${data.chunks} 个片段，可用于检索。`,
          time: new Date().toTimeString().slice(0, 5),
        }])
        setConnectionStatus('connected')
      } else {
        const err = await resp.json()
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `[上传失败] ${err.detail || resp.statusText}`,
          time: new Date().toTimeString().slice(0, 5),
        }])
      }
    } catch {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: '[上传失败] 网络错误，请检查后端服务是否启动',
        time: new Date().toTimeString().slice(0, 5),
      }])
    }
    // Reset input so same file can be re-uploaded
    e.target.value = ''
  }

  const handleClear = () => {
    setMessages([])
    try { localStorage.removeItem(STORAGE_KEY) } catch { /* ignore */ }
  }

  /** Regenerate: remove the last assistant response, re-send the last user prompt */
  const handleRegenerate = useCallback(() => {
    if (isSending) return
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
      setIsSending(false);
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
            emptyTitle="徒步知识问答，有什么我可以帮您？"
            onRegenerate={handleRegenerate}
            realMessageCount={messages.length}
          />
        </div>
      </div>
    </AssistantRuntimeProvider>
  )
}

export default LoveMaster
