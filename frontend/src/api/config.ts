const configuredApiBase = import.meta.env?.VITE_API_BASE_URL?.trim().replace(/\/+$/, '')

const API_BASE = configuredApiBase || '/api/v1'

export const API = {
  chatSSE: `${API_BASE}/chat/sse`,
  chatSync: `${API_BASE}/chat/sync`,
  chatHealth: `${API_BASE}/chat/health`,
  chatConfirm: `${API_BASE}/chat/confirm`,
  chatPending: (chatId: string) => `${API_BASE}/chat/pending/${encodeURIComponent(chatId)}`,
  chatHistory: (chatId: string) => `${API_BASE}/chat/history/${encodeURIComponent(chatId)}`,

  modelsFetch: `${API_BASE}/models/fetch`,

  ragQuery: `${API_BASE}/rag/query`,
  ragUpload: `${API_BASE}/rag/upload`,
  ragHealth: `${API_BASE}/rag/health`,
  ragDocuments: `${API_BASE}/rag/documents`,
  ragHistory: (chatId: string) => `${API_BASE}/rag/history/${encodeURIComponent(chatId)}`,
} as const
