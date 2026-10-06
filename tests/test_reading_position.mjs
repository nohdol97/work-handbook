import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { JSDOM } from 'jsdom';

const runtime = readFileSync(new URL('../docs/assets/javascripts/reading-position.js', import.meta.url), 'utf8');
const KEY = 'handbook:language-reading-position:v1';
const source = '<h1 data-y="100">제목</h1><h2 id="한국어" data-y="300">절</h2><p data-y="400">문단</p><pre data-y="600">코드</pre><h2 data-y="1000">다음</h2>';
const translated = '<h1 data-y="100">Title</h1><h2 id="translated" data-y="500">Section</h2><p data-y="700">Paragraph</p><pre data-y="1100">Code</pre><h2 data-y="1900">Next</h2>';

function page(t, { en = false, content = en ? translated : source, state, url, blocked = false } = {}) {
  const dom = new JSDOM(`<html lang="${en ? 'en' : 'ko'}"><header class="md-header"><div class="md-select"><button class="md-header__button" aria-label="Select language" title="Language">L</button></div><a hreflang="ko" href="/topic/">한국어</a><a hreflang="en" href="/en/topic/">English</a></header><article class="md-content__inner">${content}</article><input><textarea></textarea><select></select><div contenteditable="true">edit</div><a id="ordinary" href="/elsewhere/">Other</a></html>`, { url: url || `https://example.test/${en ? 'en/' : ''}topic/`, runScripts: 'outside-only' });
  const w = dom.window;
  t.after(() => w.close());
  let scroll = 0;
  const calls = [];
  Object.defineProperty(w, 'scrollY', { get: () => scroll });
  Object.defineProperty(w, 'innerHeight', { value: 500 });
  Object.defineProperty(w.document.documentElement, 'scrollHeight', { value: 3000, configurable: true });
  w.scrollTo = ({ top }) => { scroll = top; calls.push(top); };
  w.HTMLElement.prototype.getBoundingClientRect = function () {
    if (this.matches('.md-header')) return { top: 0, bottom: 64, height: 64 };
    const y = this.matches('article') ? 100 : Number(this.dataset.y || 0);
    const height = this.closest('[hidden]') ? 0 : this.matches('article') ? 2600 : 100;
    return { top: y - scroll, bottom: y - scroll + height, height };
  };
  w.HTMLElement.prototype.getClientRects = function () { return this.closest('[hidden]') ? [] : [this.getBoundingClientRect()]; };
  let resize;
  w.ResizeObserver = class { constructor(fn) { resize = fn; } observe() {} disconnect() { resize = undefined; } };
  w.requestAnimationFrame = (fn) => { fn(); return 1; };
  if (state) w.sessionStorage.setItem(KEY, state);
  if (blocked) Object.defineProperty(w, 'sessionStorage', { get() { throw new Error('blocked'); } });
  const clicks = [];
  // Prevent jsdom navigation after the runtime has processed each real DOM event.
  w.addEventListener('click', (event) => { if (event.target.closest('a')) { clicks.push(event.target.closest('a')); event.preventDefault(); } });
  w.eval(runtime);
  w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
  return { w, calls, clicks, setScroll: (y) => { scroll = y; }, resize: () => resize?.(), link: w.document.querySelector(`a[hreflang="${en ? 'ko' : 'en'}"]`), saved: () => w.sessionStorage.getItem(KEY) };
}
function click(p, options = {}, link = p.link) {
  link.dispatchEvent(new p.w.MouseEvent('click', { bubbles: true, cancelable: true, button: 0, ...options }));
}
function capture(t, options = {}) {
  const p = page(t, options); p.setScroll(420); click(p); return p.saved();
}
function shortcut(p, overrides = {}, target = p.w.document.body) {
  const event = new p.w.KeyboardEvent('keydown', { bubbles: true, cancelable: true, altKey: true, shiftKey: true, key: '¬', code: 'KeyL', ...overrides });
  target.dispatchEvent(event); return event;
}

test('physical Alt+Shift+L switches language and advertises the shortcut', (t) => {
  const p = page(t); p.setScroll(420);
  const event = shortcut(p);
  assert.equal(p.clicks.length, 1, 'shortcut should activate the existing language link');
  assert.equal(p.clicks[0], p.link);
  assert.ok(p.saved(), 'shortcut captures reading position');
  assert.equal(event.defaultPrevented, true);
  const control = p.w.document.querySelector('.md-select > button.md-header__button');
  assert.equal(control.getAttribute('aria-keyshortcuts'), 'Alt+Shift+L');
  assert.match(control.title, /Alt\+Shift\+L/);
});

test('shortcut ignores editing, IME, repeated keys and extra modifiers', (t) => {
  const p = page(t);
  for (const selector of ['input', 'textarea', 'select', '[contenteditable]']) shortcut(p, {}, p.w.document.querySelector(selector));
  for (const overrides of [{ isComposing: true }, { repeat: true }, { ctrlKey: true }, { metaKey: true }, { altKey: false }, { shiftKey: false }, { code: 'KeyK', key: 'k' }]) shortcut(p, overrides);
  assert.equal(p.clicks.length, 0);
  assert.equal(p.saved(), null);
});

test('real language click restores the translated block and round trips', (t) => {
  const ko = page(t); ko.setScroll(420); const href = ko.link.getAttribute('href'); click(ko);
  assert.equal(ko.link.getAttribute('href'), href);
  const en = page(t, { en: true, state: ko.saved(), url: 'https://example.test/en/topic/#old' });
  assert.equal(en.w.scrollY, 820, 'halfway through translated paragraph remains at reading line');
  assert.equal(en.saved(), null, 'state consumed once');
  click(en);
  const back = page(t, { state: en.saved() });
  assert.equal(back.w.scrollY, 420);
});

test('theme language handlers cannot swallow reading position capture', (t) => {
  const p = page(t); p.setScroll(420);
  p.link.addEventListener('click', (event) => { event.stopPropagation(); event.preventDefault(); });
  click(p);
  assert.ok(p.saved(), 'capture precedes the theme language menu handler');
});

test('path binding, expiry and malformed data leave native scroll untouched', (t) => {
  const saved = capture(t);
  for (const state of [saved.replace('/en/topic/', '/en/other/'), JSON.stringify({ ...JSON.parse(saved), time: Date.now() - 60001 }), '{broken', JSON.stringify({ ...JSON.parse(saved), fraction: 4 })]) {
    const p = page(t, { en: true, state });
    assert.deepEqual(p.calls, []);
    assert.equal(p.saved(), null);
  }
  assert.deepEqual(page(t, { en: true }).calls, [], 'reload with no transfer does not restore');
});

test('modified clicks, new tabs and ordinary links bypass capture; blocked storage still navigates', (t) => {
  const p = page(t);
  for (const options of [{ ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true }, { button: 1 }]) click(p, options);
  p.link.target = '_blank'; click(p); p.link.removeAttribute('target');
  click(p, {}, p.w.document.querySelector('#ordinary'));
  assert.equal(p.saved(), null);
  const blocked = page(t, { blocked: true });
  assert.doesNotThrow(() => click(blocked));
  assert.equal(blocked.clicks[0], blocked.link);
});

test('section fallback handles missing blocks; heading mismatch uses page progress', (t) => {
  const saved = capture(t);
  const missing = page(t, { en: true, state: saved, content: translated.replace('<pre data-y="1100">Code</pre>', '').replace('data-y="1900"', 'data-y="2250"') });
  assert.equal(missing.w.scrollY, 920, 'reading point is two sevenths through translated section');
  const changed = page(t, { en: true, state: saved, content: translated.replace('<h2 id="translated"', '<h3 id="translated"').replace('Section</h2>', 'Section</h3>') });
  assert.equal(changed.w.scrollY, 420, 'same overall page progress when headings differ');
});

test('hidden panel content does not shift visible block correspondence', (t) => {
  const ko = source.replace('<pre', '<div hidden class="tabbed-content"><h3>Hidden</h3><p data-y="430">Hidden paragraph</p></div><pre');
  const en = translated.replace('<pre', '<div hidden class="tabbed-content"><h4>Hidden translation</h4><p data-y="900">Hidden</p><p data-y="1000">Extra</p></div><pre');
  const p = page(t, { en: true, content: en, state: capture(t, { content: ko }) });
  assert.equal(p.w.scrollY, 820);
});

test('top and bottom remain edges', (t) => {
  for (const y of [0, 2500]) {
    const p = page(t); p.setScroll(y); click(p);
    const dest = page(t, { en: true, state: p.saved() });
    assert.equal(dest.w.scrollY, y);
  }
});

test('late layout correction stops immediately after user input', (t) => {
  const p = page(t, { en: true, state: capture(t) });
  p.w.document.querySelector('p').dataset.y = '900'; p.resize();
  assert.equal(p.w.scrollY, 920);
  p.w.dispatchEvent(new p.w.Event('wheel'));
  p.setScroll(123); p.w.document.querySelector('p').dataset.y = '1000'; p.resize();
  assert.equal(p.w.scrollY, 123);
});

 test('long code and table rows retain their internal reading progress', (t) => {
  for (const tag of ['pre', 'tr']) {
    const koContent = tag === 'pre' ? source : source.replace('<pre data-y="600">코드</pre>', '<table><tbody><tr data-y="600"><td>값</td></tr></tbody></table>');
    const enContent = tag === 'pre' ? translated : translated.replace('<pre data-y="1100">Code</pre>', '<table><tbody><tr data-y="1100"><td>Value</td></tr></tbody></table>');
    const ko = page(t, { content: koContent }); ko.setScroll(720); click(ko);
    const en = page(t, { en: true, content: enContent, state: ko.saved() });
    assert.equal(en.w.scrollY, 1420, `halfway through ${tag} remains halfway`);
  }
});
