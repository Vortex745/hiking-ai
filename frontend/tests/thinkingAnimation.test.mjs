import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'

test('RAG and chat views render the richer AI thinking animation', async () => {
  const loveMaster = await readFile(resolve('src/pages/LoveMaster.tsx'), 'utf8')
  const superAgent = await readFile(resolve('src/pages/SuperAgent.tsx'), 'utf8')
  const chatRoom = await readFile(resolve('src/components/ChatRoom.tsx'), 'utf8')
  const css = await readFile(resolve('src/index.css'), 'utf8')

  assert.match(loveMaster, /ai-thinking/)
  assert.match(superAgent, /ai-thinking/)
  assert.match(chatRoom, /ai-thinking/)
  assert.match(css, /\.ai-thinking/)
  assert.match(css, /@keyframes thinkingPulse/)
  assert.match(css, /prefers-reduced-motion/)
})
