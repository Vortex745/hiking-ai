import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import ts from 'typescript'

async function loadConversationMemoryModule() {
  const source = await readFile(resolve('src/api/conversationMemory.ts'), 'utf8')
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.ES2020,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText

  return import(`data:text/javascript;base64,${Buffer.from(transpiled).toString('base64')}`)
}

test('calculates single-conversation memory progress from the 60-message window', async () => {
  const {
    CONVERSATION_MEMORY_WINDOW,
    getConversationMemoryProgress,
  } = await loadConversationMemoryModule()

  assert.equal(CONVERSATION_MEMORY_WINDOW, 60)
  assert.deepEqual(getConversationMemoryProgress([]), {
    used: 0,
    capacity: 60,
    percent: 0,
    level: 'empty',
    label: '0 / 60',
  })
  assert.deepEqual(getConversationMemoryProgress(new Array(30).fill({ role: 'user', content: 'x' })), {
    used: 30,
    capacity: 60,
    percent: 50,
    level: 'steady',
    label: '30 / 60',
  })
  assert.deepEqual(getConversationMemoryProgress(new Array(66).fill({ role: 'assistant', content: 'x' })), {
    used: 60,
    capacity: 60,
    percent: 100,
    level: 'full',
    label: '60 / 60',
  })
})

test('Agent and RAG pages share one conversation memory meter component', async () => {
  const [agentSource, ragSource, meterSource] = await Promise.all([
    readFile(resolve('src/pages/SuperAgent.tsx'), 'utf8'),
    readFile(resolve('src/pages/LoveMaster.tsx'), 'utf8'),
    readFile(resolve('src/components/ConversationMemoryMeter.tsx'), 'utf8'),
  ])

  assert.match(agentSource, /<ConversationMemoryMeter messages=\{messages\} \/>/)
  assert.match(ragSource, /<ConversationMemoryMeter messages=\{messages\} \/>/)
  assert.match(meterSource, /getConversationMemoryProgress\(messages\)/)
  assert.match(meterSource, /对话记忆/)
})
