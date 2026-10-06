/* Keep the existing i18n links; transfer only one tab's next reading position. */
(() => {
  const KEY = 'handbook:language-reading-position:v1';
  const TTL = 60000;
  const ARTICLE = 'article.md-content__inner';
  const HEADINGS = 'h1,h2,h3,h4,h5,h6';
  const BLOCKS = `${HEADINGS},p,li,pre,tr,blockquote`;
  const clamp = (value) => Math.max(0, Math.min(1, value));
  const top = (element) => element.getBoundingClientRect().top + window.scrollY;
  const visible = (element) => element.getClientRects().length && element.getBoundingClientRect().height > 0;
  const line = () => Math.max(0, document.querySelector('.md-header')?.getBoundingClientRect().bottom || 0) + 16;
  const limit = () => Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
  const route = (url) => url.pathname + url.search;

  function outline(article) {
    return [...article.querySelectorAll(HEADINGS)].filter((element) => !element.closest('.tabbed-content'));
  }

  function section(article, headings, index) {
    const heading = headings[index];
    const next = headings[index + 1];
    const nodes = [...article.querySelectorAll(BLOCKS)].filter((element) => {
      if (!visible(element)) return false;
      if (element.tagName === 'P' && element.closest('li,blockquote,td,th')) return false;
      if (element !== heading && !(heading.compareDocumentPosition(element) & 4)) return false;
      return !next || Boolean(element.compareDocumentPosition(next) & 4);
    });
    return { nodes, start: top(heading), end: next ? top(next) : top(article) + article.getBoundingClientRect().height };
  }

  function capture(article, target) {
    const headings = outline(article);
    if (!headings.length) return null;
    const readingY = window.scrollY + line();
    let index = 0;
    headings.forEach((heading, i) => { if (top(heading) <= readingY) index = i; });
    const current = section(article, headings, index);
    let block = 0;
    current.nodes.forEach((element, i) => { if (top(element) <= readingY) block = i; });
    const node = current.nodes[block];
    if (!node) return null;
    const start = top(node);
    const end = current.nodes[block + 1] ? top(current.nodes[block + 1]) : current.end;
    const tab = node.closest('.tabbed-set');
    return {
      version: 1, target: route(target), time: Date.now(),
      shape: headings.map((h) => h.tagName).join(','), heading: index,
      signature: current.nodes.map((n) => n.tagName).join(','), block,
      fraction: clamp((readingY - start) / Math.max(1, end - start)),
      sectionFraction: clamp((readingY - current.start) / Math.max(1, current.end - current.start)),
      pageFraction: clamp(window.scrollY / Math.max(1, limit())),
      edge: window.scrollY <= 2 ? 'top' : limit() - window.scrollY <= 2 ? 'bottom' : null,
      tab: tab ? [...article.querySelectorAll('.tabbed-set')].indexOf(tab) : -1,
    };
  }

  document.addEventListener('click', (event) => {
    const link = event.target.closest?.('.md-header a[hreflang],a[data-reading-language-switch]');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') || (link.target && link.target !== '_self')) return;
    const target = new URL(link.href, window.location.href);
    if (target.origin !== window.location.origin || route(target) === route(window.location)) return;
    const article = document.querySelector(ARTICLE);
    if (!article) return;
    try {
      const state = capture(article, target);
      if (state) window.sessionStorage.setItem(KEY, JSON.stringify(state));
    } catch { /* Storage restrictions must not break the original language link. */ }
  }, true);

  document.addEventListener('keydown', (event) => {
    if (event.code !== 'KeyL' || !event.altKey || !event.shiftKey || event.ctrlKey || event.metaKey || event.repeat || event.isComposing || event.defaultPrevented) return;
    const editing = (element) => element?.closest?.('input,textarea,select,[contenteditable]:not([contenteditable="false"]),[role="textbox"]');
    if (editing(event.target) || editing(document.activeElement)) return;
    const links = [...document.querySelectorAll('a[data-reading-language-switch]'), ...document.querySelectorAll('.md-header a[hreflang]')];
    const link = links.find((item) => {
      const target = new URL(item.href, window.location.href);
      return ['ko', 'en'].includes(item.hreflang) && item.hreflang !== document.documentElement.lang && target.origin === window.location.origin && route(target) !== route(window.location);
    });
    if (!link) return;
    event.preventDefault();
    link.click();
  });

  function initialize() {
    const control = document.querySelector('.md-header .md-select > button');
    if (control) {
      control.setAttribute('aria-keyshortcuts', 'Alt+Shift+L');
      control.title = document.documentElement.lang === 'ko'
        ? '한·영 전환: Alt+Shift+L (Mac: ⌥⇧L)'
        : 'Switch language: Alt+Shift+L (Mac: ⌥⇧L)';
    }
    restore();
  }

  function valid(state) {
    return state && state.version === 1 && state.target === route(window.location) &&
      Number.isFinite(state.time) && Date.now() - state.time >= 0 && Date.now() - state.time < TTL &&
      typeof state.shape === 'string' && typeof state.signature === 'string' &&
      Number.isInteger(state.heading) && state.heading >= 0 && Number.isInteger(state.block) && state.block >= 0 &&
      Number.isInteger(state.tab) && state.tab >= -1 &&
      ['fraction', 'sectionFraction', 'pageFraction'].every((key) => Number.isFinite(state[key]) && state[key] >= 0 && state[key] <= 1) &&
      [null, 'top', 'bottom'].includes(state.edge);
  }

  function restore() {
    let state;
    try {
      const raw = window.sessionStorage.getItem(KEY);
      if (!raw) return;
      window.sessionStorage.removeItem(KEY);
      state = JSON.parse(raw);
    } catch { return; }
    if (!valid(state)) return;
    const article = document.querySelector(ARTICLE);
    if (!article) return;

    // Prompt tab order differs by locale. Show the destination language's panel.
    if (state.tab >= 0) {
      const tab = article.querySelectorAll('.tabbed-set')[state.tab];
      const labelText = document.documentElement.lang === 'ko' ? '한국어' : 'English';
      const label = tab && [...tab.querySelectorAll('.tabbed-labels label')].find((item) => item.textContent.trim() === labelText);
      if (label) label.click();
    }

    let stopped = false;
    let observer;
    let timer;
    const deadline = Date.now() + 2000;
    const stop = () => {
      stopped = true;
      observer?.disconnect();
      clearTimeout(timer);
      ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach((type) => window.removeEventListener(type, stop));
      window.removeEventListener('load', apply);
    };
    const apply = () => {
      if (stopped) return;
      if (Date.now() > deadline) { stop(); return; }
      const headings = outline(article);
      let y = state.pageFraction * limit();
      if (state.edge === 'top') y = 0;
      else if (state.edge === 'bottom') y = limit();
      else if (headings.map((h) => h.tagName).join(',') === state.shape && headings[state.heading]) {
        const current = section(article, headings, state.heading);
        y = current.start + state.sectionFraction * (current.end - current.start) - line();
        if (current.nodes.map((n) => n.tagName).join(',') === state.signature && current.nodes[state.block]) {
          const start = top(current.nodes[state.block]);
          const end = current.nodes[state.block + 1] ? top(current.nodes[state.block + 1]) : current.end;
          y = start + state.fraction * (end - start) - line();
        }
      }
      window.scrollTo({ top: Math.max(0, Math.min(limit(), y)), behavior: 'instant' });
    };
    ['wheel', 'touchstart', 'pointerdown', 'keydown'].forEach((type) => window.addEventListener(type, stop, { passive: true }));
    window.addEventListener('load', apply, { once: true });
    if (window.ResizeObserver) {
      observer = new ResizeObserver(() => window.requestAnimationFrame(apply));
      observer.observe(article);
    }
    document.fonts?.ready.then(() => window.requestAnimationFrame(apply));
    window.requestAnimationFrame(apply);
    timer = setTimeout(stop, 2000);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initialize, { once: true });
  else initialize();
})();
