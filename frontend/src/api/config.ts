const isDev = import.meta.env?.DEV ?? false

const API_BASE = isDev
  ? '/api/v1'
  : 'https://gateway-262534-6-1364947792.sh.run.tcloudbase.com/api/v1'

export const API = {
  chatSSE: `${API_BASE}/chat/sse`,
  chatSync: `${API_BASE}/chat/sync`,
  chatHealth: `${API_BASE}/chat/health`,

  modelsFetch: `${API_BASE}/models/fetch`,

  ragQuery: `${API_BASE}/rag/query`,
  ragUpload: `${API_BASE}/rag/upload`,
  ragHealth: `${API_BASE}/rag/health`,
  ragDocuments: `${API_BASE}/rag/documents`,
} as const
