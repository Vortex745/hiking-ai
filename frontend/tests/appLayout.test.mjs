import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'

test('global app layout does not let fixed sidebar cover mobile chat pages', async () => {
  const appSource = await readFile(resolve('src/App.tsx'), 'utf8')

  assert.match(appSource, /h-\[100dvh\]/)
  assert.doesNotMatch(appSource, /h-screen/)
  assert.match(appSource, /<nav className="[^"]*fixed top-6 left-1\/2/)
  assert.match(appSource, /<main className="[^"]*w-full h-full/)
  assert.doesNotMatch(appSource, /ml-sidebar/)
})
