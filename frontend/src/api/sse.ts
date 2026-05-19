export interface SSEEvent {
  type: 'thought' | 'process' | 'documents' | 'tool_call' | 'tool_result' | 'approval_required' | 'artifact' | 'text' | 'done' | 'error'
  content: string
  metadata?: Record<string, unknown>
}

export interface StreamHandlers {
  onMessage: (event: SSEEvent) => void
  onError: (error: string) => void
  onOpen?: () => void
  onDone?: () => void
}

export interface CreateStreamOptions {
  method?: string
  body?: string
  onMessage: (event: SSEEvent) => void
  onError: (error: string) => void
  onOpen?: () => void
  onDone?: () => void
}

function parseSSELine(line: string): SSEEvent | null {
  const trimmed = line.trim()
  const jsonStr = trimmed.startsWith('data:')
    ? trimmed.slice(5).trim()
    : trimmed
  if (!jsonStr) return null
  try {
    return JSON.parse(jsonStr) as SSEEvent
  } catch {
    return null
  }
}

async function responseErrorMessage(response: Response) {
  const fallback = `HTTP ${response.status}: ${response.statusText || '请求失败'}`
  const text = await response.text().catch(() => '')
  if (!text.trim()) return fallback

  try {
    const payload = JSON.parse(text) as Record<string, unknown>
    const message = payload.detail ?? payload.error ?? payload.message
    if (typeof message === 'string' && message.trim()) {
      return `HTTP ${response.status}: ${message.trim()}`
    }
  } catch {
    // Plain-text error bodies are useful as-is.
  }

  return `HTTP ${response.status}: ${text.trim()}`
}

export async function createStreamConnection(
  url: string,
  options: CreateStreamOptions
): Promise<() => void> {
  let aborted = false

  const cleanup = () => {
    aborted = true
  }

  try {
    const response = await fetch(url, {
      method: options.method || 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: options.body,
    })

    if (!response.ok) {
      options.onError(await responseErrorMessage(response))
      return cleanup
    }

    options.onOpen?.()

    const reader = response.body?.getReader()
    if (!reader) {
      options.onError('Response body is not readable')
      return cleanup
    }

    const decoder = new TextDecoder()
    let buffer = ''

    while (!aborted) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        const trimmed = line.trim()
        if (!trimmed) continue

        const event = parseSSELine(trimmed)
        if (event) {
          options.onMessage(event)
          if (event.type === 'done') {
            options.onDone?.()
          }
        }
      }
    }
  } catch (error) {
    if (!aborted) {
      options.onError(error instanceof Error ? error.message : 'Connection failed')
    }
  }

  return cleanup
}

export function createSSEConnection(
  url: string,
  handlers: StreamHandlers
): () => void {
  let aborted = false
  let retryCount = 0
  const maxRetries = 3

  function connect() {
    if (aborted) return

    const eventSource = new EventSource(url)

    eventSource.onopen = () => {
      retryCount = 0
      handlers.onOpen?.()
    }

    eventSource.onmessage = (event) => {
      const parsed = parseSSELine(event.data)
      if (parsed) {
        handlers.onMessage(parsed)
        if (parsed.type === 'done') {
          handlers.onDone?.()
          eventSource.close()
        }
      }
    }

    eventSource.onerror = () => {
      eventSource.close()
      if (!aborted && retryCount < maxRetries) {
        retryCount++
        const delay = Math.min(1000 * Math.pow(2, retryCount), 10000)
        setTimeout(connect, delay)
      } else if (!aborted) {
        handlers.onError('连接失败，请检查网络后重试')
      }
    }

    return eventSource
  }

  const es = connect()

  return () => {
    aborted = true
    es?.close()
  }
}
