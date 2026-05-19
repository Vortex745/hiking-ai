import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'
import ts from 'typescript'

async function loadRagStreamModule() {
  const source = await readFile(resolve('src/api/ragStream.ts'), 'utf8')
  const transpiled = ts.transpileModule(source, {
    compilerOptions: {
      module: ts.ModuleKind.ES2020,
      target: ts.ScriptTarget.ES2020,
    },
  }).outputText

  return import(`data:text/javascript;base64,${Buffer.from(transpiled).toString('base64')}`)
}

test('applies structured RAG process and document-search events', async () => {
  const {
    createEmptyRagStreamState,
    applyRagStreamEvent,
  } = await loadRagStreamModule()

  let state = createEmptyRagStreamState()
  state = applyRagStreamEvent(state, {
    type: 'process',
    content: '调用 lark-cli api 筛查飞书链接/知识库节点',
  })
  state = applyRagStreamEvent(state, {
    type: 'documents',
    content: '已检索 2 篇相关文档，共 3 个片段',
    metadata: {
      searched_count: 2,
      matched_chunks: 3,
      documents: [
        {
          title: '徒步安全手册',
          source: 'feishu',
          content: '高原徒步需要提前适应海拔。',
        },
      ],
    },
  })
  state = applyRagStreamEvent(state, {
    type: 'text',
    content: '建议先降低强度。',
  })

  assert.deepEqual(state.processSteps, ['调用 lark-cli api 筛查飞书链接/知识库节点'])
  assert.equal(state.searchSummary?.searchedCount, 2)
  assert.equal(state.searchSummary?.matchedChunks, 3)
  assert.equal(state.searchSummary?.documents[0].title, '徒步安全手册')
  assert.equal(state.content, '建议先降低强度。')
})
