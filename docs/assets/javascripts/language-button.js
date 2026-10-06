/* Reuse the generated alternate URL and remember only the button's position. */
(() => {
  function setup() {
    if (document.querySelector('.language-switch-float')) return;
    const other = document.documentElement.lang === 'ko' ? 'en' : 'ko';
    const original = [...document.querySelectorAll('.md-header a[hreflang]')].find((link) => {
      const url = new URL(link.href, location.href);
      return link.hreflang === other && url.origin === location.origin && url.pathname !== location.pathname;
    });
    if (!original) return;
    const button = document.createElement('a');
    button.className = 'language-switch-float';
    button.dataset.readingLanguageSwitch = 'true';
    button.setAttribute('href', original.getAttribute('href'));
    button.hreflang = other;
    button.textContent = other === 'en' ? 'EN' : '한';
    button.setAttribute('aria-label', other === 'en' ? 'Switch to English' : '한국어로 전환');
    button.setAttribute('aria-keyshortcuts', 'Alt+Shift+L');
    button.title = `${other === 'en' ? 'English' : '한국어'} · Alt+Shift+L (Mac: Option+Shift+L) · 드래그로 이동 / Drag to move · ←↑↓→`;
    document.body.append(button);

    const KEY = 'handbook:language-button:v1';
    let position = { x: 1, y: 1 };
    try {
      const saved = JSON.parse(localStorage.getItem(KEY));
      if (saved && ['x', 'y'].every((key) => Number.isFinite(saved[key]) && saved[key] >= 0 && saved[key] <= 1)) position = { x: saved.x, y: saved.y };
    } catch { /* Position remains usable when storage is restricted. */ }
    function bounds() {
      const rect = button.getBoundingClientRect();
      return { x: Math.max(0, window.innerWidth - rect.width - 24), y: Math.max(0, window.innerHeight - rect.height - 24) };
    }
    function render() {
      const span = bounds();
      button.style.left = `${12 + position.x * span.x}px`;
      button.style.top = `${12 + position.y * span.y}px`;
    }
    function move(x, y) {
      const span = bounds();
      position = { x: span.x ? Math.max(0, Math.min(1, (x - 12) / span.x)) : 0, y: span.y ? Math.max(0, Math.min(1, (y - 12) / span.y)) : 0 };
      render();
    }
    function save() {
      try { localStorage.setItem(KEY, JSON.stringify(position)); } catch { /* Optional persistence. */ }
    }
    render();
    const menu = original.closest('.md-select');
    if (menu) { menu.hidden = true; menu.dataset.floatingLanguageReplaced = 'true'; }
    window.addEventListener('resize', render);

    let pointer;
    let suppressClick = false;
    button.addEventListener('pointerdown', (event) => {
      if (event.button !== 0 || event.isPrimary === false) return;
      suppressClick = false;
      const rect = button.getBoundingClientRect();
      pointer = { id: event.pointerId, x: event.clientX, y: event.clientY, left: rect.left, top: rect.top, dragged: false };
      button.setPointerCapture?.(event.pointerId);
    });
    button.addEventListener('pointermove', (event) => {
      if (!pointer || event.pointerId !== pointer.id) return;
      const dx = event.clientX - pointer.x;
      const dy = event.clientY - pointer.y;
      if (Math.hypot(dx, dy) >= 6) pointer.dragged = true;
      if (!pointer.dragged) return;
      event.preventDefault();
      button.classList.add('is-dragging');
      move(pointer.left + dx, pointer.top + dy);
    });
    function finish(event) {
      if (!pointer || event.pointerId !== pointer.id) return;
      suppressClick = pointer.dragged;
      if (pointer.dragged) save();
      pointer = null;
      button.classList.remove('is-dragging');
    }
    button.addEventListener('pointerup', finish);
    button.addEventListener('pointercancel', finish);
    button.addEventListener('lostpointercapture', finish);
    button.addEventListener('dragstart', (event) => event.preventDefault());
    // Window capture runs before the reading-position listener on document.
    window.addEventListener('click', (event) => {
      if (suppressClick && button.contains(event.target)) {
        suppressClick = false;
        event.preventDefault();
        event.stopPropagation();
      }
    }, true);
    // A keyboard action is a fresh intent, including the global language shortcut.
    window.addEventListener('keydown', () => { suppressClick = false; }, true);
    button.addEventListener('keydown', (event) => {
      const directions = { ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1] };
      if (event.ctrlKey || event.metaKey || event.altKey || event.isComposing) return;
      if (directions[event.key]) {
        event.preventDefault();
        const rect = button.getBoundingClientRect();
        const [dx, dy] = directions[event.key];
        const step = event.shiftKey ? 40 : 10;
        move(rect.left + dx * step, rect.top + dy * step);
        save();
      } else if (event.key === ' ' && !event.repeat) {
        event.preventDefault();
        suppressClick = false;
        button.click();
      } else if (event.key === 'Enter') suppressClick = false;
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', setup, { once: true });
  else setup();
})();
