import { useState, useRef, useEffect, useCallback } from 'react'
import AiAvatar from './AiAvatar'
import ConnectionStatus from './ConnectionStatus'
import { createStreamConnection, SSEEvent } from '../api/sse'

interface Message {
  role: 'user' | 'assistant'
  content: string
  isStreaming?: boolean
}

interface ChatRoomProps {
  apiEndpoint: string
  sseEndpoint: string
  healthEndpoint: string
  aiName: string
  aiAvatar: 'love' | 'agent'
}

const STORAGE_KEY_PREFIX = 'ai-hiking-chat-'
const ALERT_DEDUP_WINDOW_MS = 10000
let lastGlobalAlert = { key: '', time: 0 }

type ConnectionState = 'disconnected' | 'connected' | 'error'
type HealthPayload = Record<string, unknown>

function isHealthPayload(payload: HealthPayload | string | null): payload is HealthPayload {
  return typeof payload === 'object' && payload !== null
}

function payloadMessage(payload: HealthPayload | string | null): string {
  if (typeof payload === 'string') return payload.trim()
  if (!isHealthPayload(payload)) return ''

  const value = payload.detail ?? payload.error ?? payload.message
  if (typeof value === 'string') return value.trim()
  if (value === undefined || value === null) return ''

  try {
    return JSON.stringify(value)
  } catch {
    return String(value)
  }
}

async function readResponsePayload(response: Response): Promise<HealthPayload | string | null> {
  const contentType = response.headers.get('content-type') || ''
  try {
    if (contentType.includes('application/json')) {
      return await response.json() as HealthPayload
    }
    return await response.text()
  } catch {
    return null
  }
}

function responseErrorMessage(response: Response, payload: HealthPayload | string | null): string {
  return payloadMessage(payload) || `HTTP ${response.status}: ${response.statusText || '请求失败'}`
}

function formatConnectionError(error: unknown): string {
  if (error instanceof DOMException && error.name === 'AbortError') {
    return '状态检测超时，请确认网关和 AI 服务已启动'
  }
  if (error instanceof Error) return error.message
  return '状态检测失败，请稍后重试'
}

function alertDedupeKey(aiName: string, reason: string): string {
  const statusMatch = reason.match(/\b([45]\d\d)\b/)
  return `${aiName}:${statusMatch ? `HTTP ${statusMatch[1]}` : reason}`
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

function ChatRoom({ apiEndpoint, sseEndpoint, healthEndpoint, aiName, aiAvatar }: ChatRoomProps) {
  const [messages, setMessages] = useState<Message[]>(() => {
    try {
      const saved = localStorage.getItem(`${STORAGE_KEY_PREFIX}${aiName}`)
      return saved ? JSON.parse(saved) : []
    } catch {
      return []
    }
  })

  const [input, setInput] = useState('')
  const [connectionStatus, setConnectionStatus] = useState<ConnectionState>('disconnected')
  const [isSending, setIsSending] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const cleanupRef = useRef<(() => void) | null>(null)
  const lastAlertedErrorRef = useRef('')

  // Save messages to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(`${STORAGE_KEY_PREFIX}${aiName}`, JSON.stringify(messages))
    } catch {
      // Ignore storage errors
    }
  }, [messages, aiName])

  // Auto scroll to bottom
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cleanupRef.current?.()
    }
  }, [])

  const reportConnectionError = useCallback((message: string, showAlert = true) => {
    const reason = message.trim() || '状态检测失败，请稍后重试'
    const dedupeKey = alertDedupeKey(aiName, reason)
    const now = Date.now()
    setConnectionStatus('error')

    if (
      showAlert &&
      lastAlertedErrorRef.current !== reason &&
      (lastGlobalAlert.key !== dedupeKey || now - lastGlobalAlert.time > ALERT_DEDUP_WINDOW_MS)
    ) {
      window.alert(`${aiName} 状态错误：${reason}`)
      lastAlertedErrorRef.current = reason
      lastGlobalAlert = { key: dedupeKey, time: now }
    }
  }, [aiName])

  const checkConnectionStatus = useCallback(async (showAlert = true) => {
    if (!healthEndpoint) {
      setConnectionStatus('disconnected')
      return
    }

    const controller = new AbortController()
    const timeoutId = window.setTimeout(() => controller.abort(), 5000)

    try {
      const response = await fetch(healthEndpoint, {
        method: 'GET',
        headers: { Accept: 'application/json' },
        signal: controller.signal,
      })
      const payload = await readResponsePayload(response)

      if (!response.ok) {
        throw new Error(responseErrorMessage(response, payload))
      }

      const moduleStatus = isHealthPayload(payload) && typeof payload.status === 'string'
        ? payload.status.toLowerCase()
        : 'ok'

      if (!['ok', 'ready', 'success'].includes(moduleStatus)) {
        throw new Error(payloadMessage(payload) || `模块状态异常：${moduleStatus}`)
      }

      setConnectionStatus('connected')
      lastAlertedErrorRef.current = ''
    } catch (error) {
      reportConnectionError(formatConnectionError(error), showAlert)
    } finally {
      window.clearTimeout(timeoutId)
    }
  }, [healthEndpoint, reportConnectionError])

  useEffect(() => {
    if (!healthEndpoint) return

    checkConnectionStatus(true)
    const intervalId = window.setInterval(() => checkConnectionStatus(true), 30000)

    return () => {
      window.clearInterval(intervalId)
    }
  }, [checkConnectionStatus, healthEndpoint])

  const appendToLastMessage = useCallback((text: string) => {
    setMessages(prev => {
      const updated = [...prev]
      const last = updated[updated.length - 1]
      if (last && last.role === 'assistant') {
        updated[updated.length - 1] = {
          ...last,
          content: last.content + text,
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
      if (last && last.isStreaming) {
        updated[updated.length - 1] = { ...last, isStreaming: false }
      }
      return updated
    })
  }, [])

  const handleSend = useCallback(async () => {
    const text = input.trim()
    if (!text || isSending) return

    setInput('')
    setIsSending(true)

    setMessages(prev => [...prev, { role: 'user', content: text }])
    setMessages(prev => [...prev, { role: 'assistant', content: '', isStreaming: true }])

    const chatId = `chat-${Date.now()}`

    try {
      if (sseEndpoint) {
        const cleanup = await createStreamConnection(
          sseEndpoint,
          {
            method: 'POST',
            body: JSON.stringify({ message: text, chat_id: chatId }),
            onOpen: () => {
              setConnectionStatus('connected')
            },
            onMessage: (event: SSEEvent) => {
              if (event.type === 'thought') {
                appendToLastMessage(`[${event.content}]\n`)
              } else if (event.type === 'tool_call') {
                appendToLastMessage(`🔧 ${event.content}\n`)
              } else if (event.type === 'tool_result') {
                appendToLastMessage(`📋 ${event.content}\n`)
              } else if (event.type === 'text') {
                appendToLastMessage(event.content)
              } else if (event.type === 'done') {
                finalizeStreaming()
                setConnectionStatus('connected')
              } else if (event.type === 'error') {
                appendToLastMessage(`\n\n[错误] ${event.content}`)
                finalizeStreaming()
                reportConnectionError(event.content || 'Agent 请求失败')
              }
            },
            onError: (error: string) => {
              appendToLastMessage(`\n\n[连接错误] ${error}`)
              finalizeStreaming()
              reportConnectionError(error)
            },
          }
        )
        cleanupRef.current = cleanup
      } else {
        const response = await fetch(apiEndpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question: text,
            status: aiAvatar === 'love' ? 'single' : null,
          }),
        })

        if (!response.ok) {
          const payload = await readResponsePayload(response)
          throw new Error(responseErrorMessage(response, payload))
        }

        const reader = response.body?.getReader()
        if (reader) {
          const decoder = new TextDecoder()
          let buffer = ''
          let streamFailed = false
          setConnectionStatus('connected')

          while (true) {
            const { done, value } = await reader.read()
            if (done) break

            buffer += decoder.decode(value, { stream: true })
            const lines = buffer.split('\n')
            buffer = lines.pop() || ''

            for (const line of lines) {
              const trimmed = line.trim()
              if (!trimmed || !trimmed.startsWith('data: ')) continue

              try {
                const event = JSON.parse(trimmed.slice(6)) as SSEEvent
                if (event.type === 'text') {
                  appendToLastMessage(event.content)
                } else if (event.type === 'thought') {
                  appendToLastMessage(`[${event.content}]\n`)
                } else if (event.type === 'done') {
                  finalizeStreaming()
                  setConnectionStatus('connected')
                } else if (event.type === 'error') {
                  streamFailed = true
                  appendToLastMessage(`\n\n[错误] ${event.content}`)
                  finalizeStreaming()
                  reportConnectionError(event.content || 'RAG 请求失败')
                }
              } catch {
                // Skip unparseable lines
              }
            }
          }
          finalizeStreaming()
          if (!streamFailed) setConnectionStatus('connected')
        } else {
          const data = await response.json()
          appendToLastMessage(data.answer || data.content || '已收到你的消息。')
          finalizeStreaming()
          setConnectionStatus('connected')
        }
      }
    } catch (error) {
      const reason = formatConnectionError(error)
      appendToLastMessage(`\n\n[错误] ${reason}`)
      finalizeStreaming()
      reportConnectionError(reason)
    } finally {
      setIsSending(false)
    }
  }, [
    input,
    isSending,
    apiEndpoint,
    sseEndpoint,
    aiAvatar,
    appendToLastMessage,
    finalizeStreaming,
    reportConnectionError,
  ])

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleClear = () => {
    setMessages([])
    try {
      localStorage.removeItem(`${STORAGE_KEY_PREFIX}${aiName}`)
    } catch {
      // Ignore
    }
  }

  return (
    <div className="chat-room">
      <ConnectionStatus status={connectionStatus} />
      <div className="chat-messages">
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: 'var(--text-secondary)', padding: '40px 20px' }}>
            <p>开始与 {aiName} 对话吧！</p>
            <p style={{ fontSize: '0.85rem', marginTop: 8 }}>
              {aiAvatar === 'agent'
                ? '可以尝试：搜索 AI 新闻、保存文件、生成 PDF 等'
                : '可以尝试：问情感问题、上传恋爱知识文档等'}
            </p>
          </div>
        )}

        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.role === 'assistant' && <AiAvatar type={aiAvatar} />}
            <div className="message-content">
              {msg.content || msg.isStreaming ? (
                <div>
                  {msg.content ? (
                    <>
                      {msg.content}
                      {msg.isStreaming && <span className="typing-indicator">▌</span>}
                    </>
                  ) : (
                      <AiThinking />
                  )}
                </div>
              ) : (
                <div className="loading-dots">
                  <span /><span /><span />
                </div>
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <textarea
          ref={inputRef}
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="输入你的问题..."
          rows={1}
          disabled={isSending}
        />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={!input.trim() || isSending}
        >
          {isSending ? '发送中' : '发送'}
        </button>
        {messages.length > 0 && (
          <button
            className="send-btn"
            onClick={handleClear}
            style={{ background: 'var(--text-secondary)' }}
            title="清空对话"
          >
            清空
          </button>
        )}
      </div>
    </div>
  )
}

export default ChatRoom
