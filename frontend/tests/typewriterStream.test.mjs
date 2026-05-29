import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import ts from 'typescript'

async function loadTypewriterModule() {
  const source = await readFile(resolve('src/api/typewriterStream.ts'), 'utf8')
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.ES2020,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText

  return import(`data:text/javascript;base64,${Buffer.from(transpiled).toString('base64')}`)
}

function createScheduler() {
  const jobs = new Map()
  let nextId = 1

  return {
    setTimer(fn) {
      const id = nextId++
      jobs.set(id, fn)
      return id
    },
    clearTimer(id) {
      jobs.delete(id)
    },
    runOne() {
      const first = jobs.entries().next()
      if (first.done) return false
      const [id, fn] = first.value
      jobs.delete(id)
      fn()
      return true
    },
    get size() {
      return jobs.size
    },
  }
}

test('typewriter queue releases large SSE text payloads in small chunks', async () => {
  const { createTypewriterStreamQueue } = await loadTypewriterModule()
  const scheduler = createScheduler()
  const chunks = []
  let finished = false

  const queue = createTypewriterStreamQueue(
    chunk => chunks.push(chunk),
    { chunkSize: 2, intervalMs: 1, setTimer: scheduler.setTimer, clearTimer: scheduler.clearTimer },
  )

  queue.enqueue('hello')
  queue.finishWhenIdle(() => { finished = true })

  assert.deepEqual(chunks, [])
  assert.equal(finished, false)

  scheduler.runOne()
  assert.deepEqual(chunks, ['he'])
  assert.equal(finished, false)

  scheduler.runOne()
  scheduler.runOne()
  assert.deepEqual(chunks, ['he', 'll', 'o'])
  assert.equal(finished, true)
})

test('typewriter queue can flush pending text before surfacing errors', async () => {
  const { createTypewriterStreamQueue } = await loadTypewriterModule()
  const scheduler = createScheduler()
  const chunks = []
  let finished = false

  const queue = createTypewriterStreamQueue(
    chunk => chunks.push(chunk),
    { chunkSize: 2, intervalMs: 1, setTimer: scheduler.setTimer, clearTimer: scheduler.clearTimer },
  )

  queue.enqueue('partial')
  queue.finishWhenIdle(() => { finished = true })
  queue.flushNow()

  assert.deepEqual(chunks, ['partial'])
  assert.equal(finished, true)
  assert.equal(scheduler.size, 0)
})
