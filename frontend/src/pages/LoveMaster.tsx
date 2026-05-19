import { useState, useRef, useEffect, useCallback } from 'react'
import { Mountain, User, BookOpen, Send, Backpack, Tent, CloudSun, ThumbsUp, ThumbsDown, Upload, MessageSquare, Trash2, PanelLeftClose, PanelLeftOpen } from 'lucide-react'
import { API } from '../api/config'
import { createStreamConnection, SSEEvent } from '../api/sse'
import { buildRagQueryPayload, buildRuntimeModelSettings } from '../api/llmConfig'
import { applyRagStreamEvent, RagSearchSummary } from '../api/ragStream'
import ConversationMemoryMeter from '../components/ConversationMemoryMeter'

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

const quickTags = [
  { icon: Mountain, text: '高原反应' },
  { icon: Backpack, text: '装备清单' },
  { icon: Tent, text: '营地选择' },
  { icon: CloudSun, text: '天气判断' },
]

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

  const handleSend = useCallback(async () => {
    const text = input.trim()
    if (!text || isSending) return

    if (!activeSessionId) {
      setActiveSessionId(generateId())
    }

    setInput('')
    setIsSending(true)

    const now = new Date()
    const timeStr = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`

    setMessages(prev => [...prev, { role: 'user', content: text, time: timeStr }])
    setMessages(prev => [...prev, { role: 'assistant', content: '', isStreaming: true }])

    try {
      const cleanup = await createStreamConnection(API.ragQuery, {
        method: 'POST',
        body: JSON.stringify(buildRagQueryPayload(text, null)),
        onOpen: () => setConnectionStatus('connected'),
        onMessage: (event: SSEEvent) => {
          if (event.type === 'done') {
            finalizeStreaming()
          } else if (event.type === 'error') {
            appendToLastMessage(`\n\n[错误] ${event.content}`)
            finalizeStreaming()
          } else {
            applyStreamEventToLastMessage(event)
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
  }, [input, isSending, activeSessionId, appendToLastMessage, applyStreamEventToLastMessage, finalizeStreaming])

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
            <h2 className="text-2xl font-bold mb-1">RAG 模块</h2>
            <p className="text-sm text-text-secondary">
              知识对话 · 徒步问答与检索
              <span className={`ml-2 inline-block w-2 h-2 rounded-full align-middle ${
                connectionStatus === 'connected' ? 'bg-green-500' :
                connectionStatus === 'error' ? 'bg-red-500' : 'bg-gray-400'
              }`} />
            </p>
            <ConversationMemoryMeter messages={messages} />
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto scrollbar-thin px-8">
          {messages.length === 0 && (
            <div className="flex items-start gap-3 bg-white border border-border rounded-lg p-4 mb-5 max-w-[600px]">
              <div className="w-10 h-10 rounded-lg bg-primary/10 text-primary-light flex items-center justify-center shrink-0">
                <BookOpen className="w-6 h-6" strokeWidth={1.5} />
              </div>
              <div>
                <h4 className="text-sm font-semibold mb-1 text-text-primary">你好！我是你的徒步知识助手。</h4>
                <p className="text-[13px] text-text-secondary leading-relaxed">你可以向我提问关于徒步路线、装备、天气、安全注意事项等方面的问题，我会基于可靠的知识库为你提供参考。</p>
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
                    {msg.content || msg.isStreaming ? (
                      <div>
                        {msg.content && (
                          <div className="whitespace-pre-wrap">
                            {msg.content}
                            {msg.isStreaming && <span className="typing-indicator">▌</span>}
                          </div>
                        )}
                        {!msg.content && msg.isStreaming && <AiThinking />}

                        {msg.role === 'assistant' && msg.searchSummary && (
                          <details className="mt-3 border-t border-border pt-2 text-[12px] text-text-secondary">
                            <summary className="cursor-pointer select-none font-medium text-text-primary">
                              文档搜索 · {msg.searchSummary.searchedCount} 篇文档 / {msg.searchSummary.matchedChunks} 个片段
                            </summary>
                            <div className="mt-2 space-y-2">
                              {msg.searchSummary.documents.length === 0 ? (
                                <div className="text-text-muted">没有检索到可引用文档。</div>
                              ) : msg.searchSummary.documents.map((doc, idx) => (
                                <div key={`${doc.title}-${idx}`} className="border-l-2 border-primary/25 pl-2">
                                  <div className="font-medium text-text-primary">
                                    {idx + 1}. {doc.title}
                                  </div>
                                  <div className="text-text-muted">
                                    来源：{sourceLabel(doc.source)}
                                    {doc.chunks ? ` · ${doc.chunks} 个片段` : ''}
                                  </div>
                                  {doc.content && (
                                    <div className="mt-1 whitespace-pre-wrap text-text-secondary">
                                      {doc.content}
                                    </div>
                                  )}
                                </div>
                              ))}
                            </div>
                          </details>
                        )}

                        {msg.role === 'assistant' && msg.processSteps && msg.processSteps.length > 0 && (
                          <details className="mt-2 border-t border-border pt-2 text-[12px] text-text-secondary">
                            <summary className="cursor-pointer select-none font-medium text-text-primary">
                              执行流程 · {msg.processSteps.length} 步
                            </summary>
                            <ol className="mt-2 list-decimal pl-4 space-y-1">
                              {msg.processSteps.map((step, idx) => (
                                <li key={`${step}-${idx}`}>{step}</li>
                              ))}
                            </ol>
                          </details>
                        )}
                      </div>
                    ) : (
                      <div className="loading-dots"><span /><span /><span /></div>
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
              id="rag-chat-input"
              name="rag-chat-input"
              type="text"
              placeholder="输入你的徒步知识问题..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              className="flex-1 bg-transparent outline-none text-sm text-text-primary py-2 placeholder:text-text-muted"
            />
            <div className="flex items-center gap-2">
              <input
                ref={fileInputRef}
                id="rag-document-upload"
                name="rag-document-upload"
                type="file"
                className="hidden"
                onChange={handleFileUpload}
                accept=".txt,.md,.pdf,.doc,.docx"
              />
              <button
                className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-border text-text-muted transition-all duration-200 ease-[var(--ease-out)] active:scale-90"
                onClick={() => fileInputRef.current?.click()}
                type="button"
                aria-label="上传文档"
                title="上传文档"
              >
                <Upload className="w-[18px] h-[18px]" />
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
                className="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-bg-body border border-border rounded-full text-[13px] text-text-secondary hover:border-primary-light hover:text-primary-light hover:bg-primary/[0.05] transition-all duration-200 ease-[var(--ease-out)] active:scale-[0.96]"
                onClick={() => setInput(tag.text)}
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
  )
}

export default LoveMaster
