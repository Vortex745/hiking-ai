import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import ts from 'typescript'

async function loadConfigModule() {
  const configPath = resolve('src/api/config.ts')
  const configSource = await readFile(configPath, 'utf8')
  const llmConfigPath = resolve('src/api/llmConfig.ts')
  const llmConfigSource = await readFile(llmConfigPath, 'utf8')

  // Replace the import with inline config
  const sourceWithoutImport = llmConfigSource.replace(
    "import { API } from './config'",
    configSource.replace('export const API =', 'const API =')
  )

  const transpiled = ts.transpileModule(sourceWithoutImport, {
    compilerOptions: {
      module: ts.ModuleKind.ES2020,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText

  return import(`data:text/javascript;base64,${Buffer.from(transpiled).toString('base64')}`)
}

function createMemoryStorage(initial = {}) {
  const store = new Map(Object.entries(initial))
  return {
    getItem: (key) => store.get(key) ?? null,
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
  }
}

test('normalizes partial LLM settings with defaults and safe numeric ranges', async () => {
  const {
    DEFAULT_LLM_SETTINGS,
    normalizeLlmSettings,
  } = await loadConfigModule()

  const settings = normalizeLlmSettings({
    llm: {
      provider: 'deepseek',
      baseUrl: ' https://api.deepseek.com/v1 ',
      apiKey: ' test-key ',
      model: '',
    },
    embedding: {
      dimensions: 99999,
    },
  })

  assert.equal(settings.llm.provider, 'openai-compatible')
  assert.equal(settings.llm.baseUrl, 'https://api.deepseek.com/v1')
  assert.equal(settings.llm.apiKey, 'test-key')
  assert.equal(settings.llm.model, DEFAULT_LLM_SETTINGS.llm.model)
  assert.equal(settings.embedding.model, DEFAULT_LLM_SETTINGS.embedding.model)
  assert.equal(settings.rerank.model, DEFAULT_LLM_SETTINGS.rerank.model)
  assert.equal(settings.embedding.dimensions, 4096)
})

test('loads defaults when stored JSON is invalid', async () => {
  const {
    DEFAULT_LLM_SETTINGS,
    LLM_SETTINGS_STORAGE_KEY,
    loadLlmSettings,
  } = await loadConfigModule()

  const storage = createMemoryStorage({
    [LLM_SETTINGS_STORAGE_KEY]: '{bad json',
  })

  assert.deepEqual(loadLlmSettings(storage), DEFAULT_LLM_SETTINGS)
})

test('saves normalized settings to provided storage', async () => {
  const {
    LLM_SETTINGS_STORAGE_KEY,
    loadLlmSettings,
    saveLlmSettings,
  } = await loadConfigModule()

  const storage = createMemoryStorage()
  const saved = saveLlmSettings({
    llm: {
      provider: 'custom',
      baseUrl: ' http://localhost:11434/v1 ',
      apiKey: '',
      model: 'qwen3:8b',
    },
    embedding: {
      provider: 'custom',
      baseUrl: ' http://localhost:11434/v1 ',
      apiKey: '',
      model: 'nomic-embed-text',
      dimensions: 768,
    },
    rerank: {
      provider: 'custom',
      baseUrl: ' http://localhost:11434/v1 ',
      apiKey: '',
      model: 'bge-reranker-large',
    },
  }, storage)

  assert.equal(JSON.parse(storage.getItem(LLM_SETTINGS_STORAGE_KEY)).llm.baseUrl, 'http://localhost:11434/v1')
  assert.equal(JSON.parse(storage.getItem(LLM_SETTINGS_STORAGE_KEY)).rerank.model, 'bge-reranker-large')
  assert.deepEqual(loadLlmSettings(storage), saved)
})

test('masks API keys without exposing full secret', async () => {
  const { maskApiKey } = await loadConfigModule()

  assert.equal(maskApiKey('sk-1234567890abcdef'), 'sk-1...cdef')
  assert.equal(maskApiKey('short'), '已设置')
  assert.equal(maskApiKey(''), '未设置')
})

test('keeps the full fetched model list visible until the user starts searching', async () => {
  const { filterModelList } = await loadConfigModule()

  const models = [
    { id: 'gpt-4o-mini' },
    { id: 'gpt-4.1' },
    { id: 'claude-3.7-sonnet' },
  ]

  assert.deepEqual(
    filterModelList(models, '').map(model => model.id),
    ['gpt-4o-mini', 'gpt-4.1', 'claude-3.7-sonnet'],
  )
  assert.deepEqual(
    filterModelList(models, '4.1').map(model => model.id),
    ['gpt-4.1'],
  )
})

test('filters fetched model lists by intended usage', async () => {
  const { filterModelsByUsage } = await loadConfigModule()

  const models = [
    { id: 'gpt-4.1' },
    { id: 'deepseek-chat' },
    { id: 'text-embedding-3-small' },
    { id: 'Qwen3-Embedding-8B' },
    { id: 'bge-reranker-large' },
    { id: 'Qwen3-Reranker-8B' },
    { id: 'whisper-1' },
  ]

  assert.deepEqual(
    filterModelsByUsage(models, 'llm').map(model => model.id),
    ['gpt-4.1', 'deepseek-chat'],
  )
  assert.deepEqual(
    filterModelsByUsage(models, 'embedding').map(model => model.id),
    ['text-embedding-3-small', 'Qwen3-Embedding-8B'],
  )
  assert.deepEqual(
    filterModelsByUsage(models, 'rerank').map(model => model.id),
    ['bge-reranker-large', 'Qwen3-Reranker-8B'],
  )
})

test('migrates stale cross-slot model names back to safe defaults', async () => {
  const {
    DEFAULT_LLM_SETTINGS,
    normalizeLlmSettings,
  } = await loadConfigModule()

  const settings = normalizeLlmSettings({
    llm: {
      model: 'text-embedding-3-small',
    },
    embedding: {
      model: 'deepseek-chat',
    },
    rerank: {
      model: 'text-embedding-3-small',
    },
  })

  assert.equal(settings.llm.model, DEFAULT_LLM_SETTINGS.llm.model)
  assert.equal(settings.embedding.model, DEFAULT_LLM_SETTINGS.embedding.model)
  assert.equal(settings.rerank.model, DEFAULT_LLM_SETTINGS.rerank.model)
})

test('repairs obviously wrong current selections after fetching candidates', async () => {
  const { repairModelSelection } = await loadConfigModule()

  const llmCandidates = [
    { id: 'deepseek-chat' },
    { id: 'deepseek-reasoner' },
  ]

  const embeddingCandidates = [
    { id: 'text-embedding-3-small' },
    { id: 'Qwen3-Embedding-8B' },
  ]
  const rerankCandidates = [
    { id: 'bge-reranker-large' },
    { id: 'Qwen3-Reranker-8B' },
  ]

  assert.equal(
    repairModelSelection('text-embedding-3-small', 'llm', llmCandidates),
    'deepseek-chat',
  )
  assert.equal(
    repairModelSelection('deepseek-chat', 'embedding', embeddingCandidates),
    'text-embedding-3-small',
  )
  assert.equal(
    repairModelSelection('text-embedding-3-small', 'rerank', rerankCandidates),
    'bge-reranker-large',
  )
  assert.equal(
    repairModelSelection('custom-private-model', 'llm', llmCandidates),
    'custom-private-model',
  )
})

test('can detect whether a config is ready for auto speed tests', async () => {
  const { canRunSpeedTest } = await loadConfigModule()

  assert.equal(canRunSpeedTest('https://api.example.com/v1', 'sk-test'), true)
  assert.equal(canRunSpeedTest('  ', 'sk-test'), false)
  assert.equal(canRunSpeedTest('https://api.example.com/v1', ''), false)
})

test('builds RAG query payload with runnable model settings only', async () => {
  const { buildRagQueryPayload } = await loadConfigModule()

  const payload = buildRagQueryPayload('查一下知识库', null, {
    llm: {
      provider: 'openai-compatible',
      baseUrl: ' https://chat.example/v1 ',
      apiKey: ' chat-key ',
      model: ' chat-model ',
    },
    embedding: {
      provider: 'openai-compatible',
      baseUrl: 'https://embed.example/v1',
      apiKey: 'embedding-key',
      model: 'embed-model',
      dimensions: 4096,
    },
    rerank: {
      provider: 'openai-compatible',
      baseUrl: '',
      apiKey: 'rerank-key',
      model: 'rerank-model',
    },
    updatedAt: null,
  })

  assert.equal(payload.question, '查一下知识库')
  assert.equal(payload.status, null)
  assert.deepEqual(payload.model_settings.llm, {
    base_url: 'https://chat.example/v1',
    api_key: 'chat-key',
    model: 'chat-model',
  })
  assert.deepEqual(payload.model_settings.embedding, {
    base_url: 'https://embed.example/v1',
    api_key: 'embedding-key',
    model: 'embed-model',
    dimensions: 4096,
  })
  assert.equal(payload.model_settings.rerank, undefined)
})

test('measures model latency through the existing models fetch endpoint', async () => {
  const { measureModelLatency } = await loadConfigModule()

  const calls = []
  const measurement = await measureModelLatency('https://api.example.com/v1', 'sk-test', {
    fetcher: async (input, init) => {
      calls.push({ input, init })
      return {
        ok: true,
        json: async () => ({
          data: [{ id: 'gpt-4o-mini' }, { id: 'gpt-4.1' }],
        }),
      }
    },
    now: (() => {
      const values = [100, 248]
      return () => values.shift()
    })(),
  })

  assert.equal(calls.length, 1)
  assert.equal(calls[0].input, 'https://gateway-262534-6-1364947792.sh.run.tcloudbase.com/api/v1/models/fetch')
  assert.equal(measurement.latencyMs, 148)
  assert.equal(measurement.modelCount, 2)
  assert.equal(JSON.parse(calls[0].init.body).base_url, 'https://api.example.com/v1')
  assert.equal(JSON.parse(calls[0].init.body).api_key, 'sk-test')
})

test('fetchModels accepts legacy backend models arrays', async () => {
  const { fetchModels } = await loadConfigModule()

  const models = await fetchModels('https://api.example.com/v1', 'sk-test', async () => ({
    ok: true,
    json: async () => ({
      models: ['deepseek-chat', 'text-embedding-3-small'],
    }),
  }))

  assert.deepEqual(models, [
    { id: 'deepseek-chat' },
    { id: 'text-embedding-3-small' },
  ])
})
