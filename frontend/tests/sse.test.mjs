import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import ts from 'typescript'

async function loadSseModule() {
  const source = await readFile(resolve('src/api/sse.ts'), 'utf8')
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.ES2020,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText

  return import(`data:text/javascript;base64,${Buffer.from(transpiled).toString('base64')}`)
}

test('parses SSE frames with multiple data lines and CRLF separators', async () => {
  const { parseSSEFrame } = await loadSseModule()

  assert.deepEqual(parseSSEFrame('data: {"type":"text","content":"hi"}\r\n'), {
    type: 'text',
    content: 'hi',
  })
  assert.equal(parseSSEFrame(': keepalive\r\n\r\n'), null)
})

test('createStreamConnection returns a cleanup function before stream completion', async () => {
  const { createStreamConnection } = await loadSseModule()
  const originalFetch = globalThis.fetch
  const events = []
  let doneCalled = false

  globalThis.fetch = async () => new Response(new ReadableStream({
    start(controller) {
      const encoder = new TextEncoder()
      controller.enqueue(encoder.encode('data: {"type":"text","content":"hello"}\n\n'))
      setTimeout(() => {
        controller.enqueue(encoder.encode('data: {"type":"done","content":""}\n\n'))
        controller.close()
      }, 20)
    },
  }), {
    status: 200,
    headers: { 'content-type': 'text/event-stream' },
  })

  try {
    const cleanup = createStreamConnection('/stream', {
      onMessage: event => events.push(event),
      onError: error => events.push({ type: 'error', content: error }),
      onDone: () => { doneCalled = true },
    })

    assert.equal(typeof cleanup, 'function')
    await new Promise(resolve => setTimeout(resolve, 50))
    assert.equal(events[0].type, 'text')
    assert.equal(events[0].content, 'hello')
    assert.equal(events.at(-1).type, 'done')
    assert.equal(doneCalled, true)
    cleanup()
  } finally {
    globalThis.fetch = originalFetch
  }
})
