import { chromium } from '@playwright/test';
import { readdir, readFile, mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = resolve('_workspace/handbook-slides');
const manifest = JSON.parse(await readFile(join(root, 'manifest.json'), 'utf8')).pages;
const chrome = process.env.CHROME_PATH || (process.platform === 'darwin' ?
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
const browser = await chromium.launch({ headless: true, ...(chrome ? { executablePath: chrome } : {}) });
const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
await context.setOffline(true);
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
page.on('request', request => {
  if (/^https?:/i.test(request.url())) errors.push(`unexpected network request: ${request.url()}`);
});

function assert(condition, message) { if (!condition) throw new Error(message); }
function fileFor(key) {
  const [lang, ...parts] = key.split('/');
  const rel = parts.join('/');
  return join(root, lang, rel.endsWith('/index.md') || rel === 'index.md' ?
    rel.replace(/index\.md$/, 'index.html') : rel.replace(/\.md$/, '/index.html'));
}
async function open(key) {
  await page.goto(pathToFileURL(fileFor(key)).href);
  await page.locator('.slide-card').first().waitFor();
  assert(await page.locator('.slide-card').count() === 1, `slide renderer missing: ${key}`);
  assert(await page.locator('h1').first().isVisible(), `title missing: ${key}`);
}
async function selectType(type) {
  const index = await page.evaluate(t => window.__HANDBOOK_SLIDES__.slides.findIndex(s => s.interaction?.type === t), type);
  assert(index >= 0, `missing ${type} interaction`);
  await page.getByRole('button', { name: /^(목차|Contents)$/ }).click();
  await page.locator('.drawer ol button').nth(index).click();
  await page.locator('.slide-card').waitFor();
}
async function exercise(key, type, selector, expected) {
  await open(key);
  await selectType(type);
  await page.locator(selector).first().click();
  await page.locator(expected).first().waitFor();
  assert(await page.locator(expected).first().isVisible(), `${type} did not react: ${key}`);
  await page.locator('.interaction').getByRole('button', { name: /^(초기화|Reset)$/ }).first().click();
}

try {
  const keys = Object.keys(manifest);
  assert(keys.length === 166, `expected 166 public pages, got ${keys.length}`);
  for (const key of keys) await open(key);
  await open('ko/data-platform/architecture.md');
  const initial = await page.locator('.slide-eyebrow').innerText();
  await page.keyboard.press('ArrowRight');
  await page.waitForFunction(previous => document.querySelector('.slide-eyebrow')?.innerText !== previous, initial);
  assert((await page.locator('.slide-eyebrow').innerText()) !== initial, 'keyboard next failed');
  await page.keyboard.press('ArrowLeft');
  await page.waitForFunction(previous => document.querySelector('.slide-eyebrow')?.innerText === previous, initial);
  assert((await page.locator('.slide-eyebrow').innerText()) === initial, 'keyboard previous failed');
  await exercise('ko/data-platform/architecture.md', 'steps', '.interaction-toolbar button:nth-child(2)', '.step-track .is-active');
  await exercise('ko/data-platform/architecture.md', 'architecture', '.architecture-node', '.interaction-detail');
  await exercise('ko/data-platform/architecture.md', 'comparison', '.choice-pill', '.comparison-grid .interaction-detail');
  await exercise('ko/data-platform/production-operations.md', 'scenario', '.choice-pill', '.interaction-detail');
  await exercise('ko/english-study/workplace.md', 'flashcard', '.flashcard-face', '.flashcard-face[aria-pressed="true"]');
  await open('ko/prompts/foundations.md');
  await selectType('practice');
  const input = page.locator('.practice textarea');
  await input.fill('edited learning prompt');
  assert(await input.inputValue() === 'edited learning prompt', 'practice edit failed');
  await page.locator('.interaction').getByRole('button', { name: /초기화|Reset/ }).click();
  assert(await input.inputValue() !== 'edited learning prompt', 'practice reset failed');
  await open('ko/data-platform/foundations.md');
  await selectType('parameter');
  const threshold = page.locator('.parameter input[type="number"]');
  await page.locator('.parameter-result.can-skip').waitFor();
  assert(await page.locator('.parameter-result.can-skip').isVisible(), 'source threshold should skip');
  await threshold.fill('300');
  await page.locator('.parameter-result.may-match').waitFor();
  await threshold.fill('500');
  await page.locator('.parameter-result.can-skip').waitFor();
  await page.locator('.parameter').getByRole('button', { name: /초기화|Reset/ }).click();
  assert(await threshold.inputValue() === '1000', 'parameter reset failed');
  await open('ko/data-platform/architecture.md');
  await selectType('quiz');
  const correct = await page.evaluate(() => window.__HANDBOOK_SLIDES__.slides.find(s => s.interaction?.type === 'quiz').interaction.data.correctIndex);
  await page.locator('.quiz-option').nth(correct).click();
  await page.getByRole('button', { name: /정답 확인|Check answer/ }).click();
  assert(await page.locator('.quiz-feedback.is-correct').isVisible(), 'quiz calculation failed');
  for (const width of [1280, 390]) {
    await page.setViewportSize({ width, height: width === 390 ? 844 : 720 });
    await open('ko/data-platform/architecture.md');
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth + 1);
    assert(!overflow, `horizontal viewport overflow at ${width}`);
    const card = page.locator('.slide-card');
    assert(await card.isVisible(), `card invisible at ${width}`);
  }
  await mkdir(resolve('_workspace/slide-qa'), { recursive: true });
  await page.screenshot({ path: resolve('_workspace/slide-qa/architecture-mobile.png'), fullPage: true });
  assert(errors.length === 0, `browser errors: ${errors.join('; ')}`);
  console.log(`Browser slides: ${keys.length} offline pages, 8 interactions, keyboard and 2 viewports PASS`);
} finally {
  await browser.close();
}
