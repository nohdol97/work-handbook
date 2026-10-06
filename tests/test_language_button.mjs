import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import test from 'node:test';
import { JSDOM } from 'jsdom';
const file = new URL('../docs/assets/javascripts/language-button.js', import.meta.url);
const script = readFileSync(file, 'utf8');
const KEY = 'handbook:language-button:v1';
function page(t, { en = false, saved, blocked = false, opposite = true } = {}) {
  const dom = new JSDOM(`<html lang="${en ? 'en' : 'ko'}"><header class="md-header"><div class="md-select" id="languages"><a hreflang="${en ? 'ko' : 'en'}" href="${opposite ? (en ? '/topic/' : '/en/topic/') : 'https://other.test/'}">Language</a></div><div class="md-select" id="other">Other selector</div></header></html>`, { url: `https://example.test/${en ? 'en/' : ''}topic/`, runScripts: 'outside-only' });
  t.after(() => dom.window.close());
  const w = dom.window;
  Object.defineProperty(w, 'innerWidth', { value: 1000, writable: true });
  Object.defineProperty(w, 'innerHeight', { value: 800, writable: true });
  w.HTMLElement.prototype.getBoundingClientRect = function () { return { left: parseFloat(this.style.left) || 0, top: parseFloat(this.style.top) || 0, width: 48, height: 48 }; };
  if (saved) w.localStorage.setItem(KEY, saved);
  if (blocked) Object.defineProperty(w, 'localStorage', { get() { throw new Error('blocked'); } });
  let navigation = 0;
  // Stand-in for the reading-position document capture listener.
  w.document.addEventListener('click', (event) => { if (event.target.matches('[data-reading-language-switch]')) navigation++; }, true);
  w.addEventListener('click', (event) => event.preventDefault());
  w.eval(script); w.document.dispatchEvent(new w.Event('DOMContentLoaded'));
  const button = w.document.querySelector('.language-switch-float');
  const pointer = (type, x, y, extra = {}) => {
    const event = new w.MouseEvent(type, { bubbles: true, cancelable: true, clientX: x, clientY: y, button: 0, ...extra });
    Object.defineProperty(event, 'pointerId', { value: 1 });
    Object.defineProperty(event, 'pointerType', { value: extra.pointerType || 'mouse' });
    button.dispatchEvent(event);
  };
  return { w, button, pointer, navigation: () => navigation, saved: () => w.localStorage.getItem(KEY) };
}
test('one-click opposite locale link replaces only the language dropdown', (t) => {
  for (const en of [false, true]) {
    const p = page(t, { en });
    assert.ok(p.button, 'floating language link must exist');
    assert.equal(p.button.textContent, en ? '한' : 'EN');
    assert.equal(p.button.getAttribute('href'), en ? '/topic/' : '/en/topic/');
    assert.equal(p.button.getAttribute('aria-keyshortcuts'), 'Alt+Shift+L');
    assert.ok(p.button.getAttribute('aria-label'));
    assert.match(p.button.title, /Alt\+Shift\+L/);
    assert.equal(p.w.document.querySelector('#languages').hidden, true);
    assert.equal(p.w.document.querySelector('#other').hidden, false);
    p.button.click(); assert.equal(p.navigation(), 1);
  }
});
test('no safe counterpart preserves the header menu', (t) => {
  const p = page(t, { opposite: false });
  assert.equal(p.button, null);
  assert.equal(p.w.document.querySelector('#languages').hidden, false);
});
test('drag clamps, persists only normalized coordinates, and suppresses pending navigation', (t) => {
  const p = page(t);
  p.pointer('pointerdown', 960, 760); p.pointer('pointermove', -300, -300); p.pointer('pointerup', -300, -300); p.button.click();
  assert.equal(p.navigation(), 0, 'drag click must not reach document reading-state capture');
  assert.equal(parseFloat(p.button.style.left), 12); assert.equal(parseFloat(p.button.style.top), 12);
  assert.deepEqual(JSON.parse(p.saved()), { x: 0, y: 0 });
  const dest = page(t, { en: true, saved: p.saved() });
  assert.equal(parseFloat(dest.button.style.left), 12);
  p.button.click(); assert.equal(p.navigation(), 1, 'later ordinary click works');
});
test('small pointer movement still clicks and touch pointer drags work', (t) => {
  const p = page(t);
  p.pointer('pointerdown', 960, 760); p.pointer('pointermove', 963, 761); p.pointer('pointerup', 963, 761); p.button.click();
  assert.equal(p.navigation(), 1);
  p.pointer('pointerdown', 960, 760, { pointerType: 'touch' }); p.pointer('pointermove', 900, 700); p.pointer('pointerup', 900, 700); p.button.click();
  assert.equal(p.navigation(), 1);
});
test('keyboard movement, resize, Space, and blocked persistence remain usable', (t) => {
  const p = page(t, { blocked: true });
  const key = (key, shiftKey = false) => p.button.dispatchEvent(new p.w.KeyboardEvent('keydown', { key, shiftKey, bubbles: true, cancelable: true }));
  const initial = parseFloat(p.button.style.left);
  key('ArrowLeft'); assert.equal(parseFloat(p.button.style.left), initial - 10);
  key('ArrowLeft', true); assert.equal(parseFloat(p.button.style.left), initial - 50);
  p.w.innerWidth = 375; p.w.innerHeight = 300; p.w.dispatchEvent(new p.w.Event('resize'));
  assert.ok(parseFloat(p.button.style.left) <= 315);
  assert.ok(parseFloat(p.button.style.top) <= 240);
  key(' '); assert.equal(p.navigation(), 1);
});

test('fresh keyboard activation after drag is never swallowed', (t) => {
  const p = page(t);
  p.pointer('pointerdown', 960, 760); p.pointer('pointermove', 860, 660); p.pointer('pointerup', 860, 660);
  p.w.document.body.dispatchEvent(new p.w.KeyboardEvent('keydown', { key: 'L', code: 'KeyL', altKey: true, shiftKey: true, bubbles: true }));
  p.button.click();
  assert.equal(p.navigation(), 1);
});
