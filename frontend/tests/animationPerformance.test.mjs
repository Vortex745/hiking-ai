import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'

test('GSAP sidebar animation is scoped, reduced-motion aware, and not replayed by session count', async () => {
  const source = await readFile(resolve('src/components/FloatingSidebar.tsx'), 'utf8')

  assert.match(source, /function prefersReducedMotion/)
  assert.match(source, /gsap\.killTweensOf\(\[container, \.\.\.items\]\)/)
  assert.match(source, /autoAlpha/)
  assert.match(source, /force3D/)
  assert.match(source, /dependencies: \[isOpen, mounted\]/)
})

test('lifecycle panel drag uses compositor transform instead of layout left top updates', async () => {
  const source = await readFile(resolve('src/components/assistant-ui/gemini/GeminiThread.tsx'), 'utf8')

  assert.match(source, /translate3d\(\$\{position\.x\}px, \$\{position\.y\}px, 0\)/)
  assert.match(source, /requestAnimationFrame\(applyDragPosition\)/)
  assert.match(source, /gsap\.set\(panel/)
  assert.doesNotMatch(source, /left: `\$\{position\.x\}px`/)
  assert.doesNotMatch(source, /top: `\$\{position\.y\}px`/)
})

test('CSS motion tokens avoid layout-heavy and zero-scale animation defaults', async () => {
  const css = await readFile(resolve('src/index.css'), 'utf8')
  const home = await readFile(resolve('src/pages/Home.tsx'), 'utf8')
  const config = await readFile(resolve('src/pages/LlmConfig.tsx'), 'utf8')

  assert.doesNotMatch(css, /--panel-blur/)
  assert.doesNotMatch(css, /scale\(0\)/)
  assert.doesNotMatch(css, /will-change:\s*width/)
  assert.match(css, /translate3d\(0, var\(--panel-translate-y\), 0\)/)
  assert.doesNotMatch(home, /group-hover:gap/)
  assert.doesNotMatch(config, /transition-all/)
})
