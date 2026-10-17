import React, { useEffect, useId, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import SlideTransition from '../../../../../third_party/slides-generator-template/src/components/SlideTransition.jsx';
import './style.css';

const deck = window.__HANDBOOK_SLIDES__ || {};
const slides = Array.isArray(deck.slides) ? deck.slides : [];
const english = String(deck.language || '').toLowerCase().startsWith('en');
const words = english ? {
  previous: 'Previous', next: 'Next', contents: 'Contents', progress: 'Progress',
  theme: 'Toggle theme', fullscreen: 'Fullscreen', notes: 'Notes', source: 'Source',
  language: 'Other language', related: 'Related documents', review: 'Review concepts',
  close: 'Close', reset: 'Reset', play: 'Play', pause: 'Pause', step: 'Next step',
  reveal: 'Reveal', hide: 'Hide', choose: 'Choose an option', check: 'Check answer',
  correct: 'Correct', incorrect: 'Try again', explanation: 'Explanation',
  copy: 'Copy', copied: 'Copied', objective: 'Learning objective', details: 'Details',
  select: 'Select a component', compare: 'Compare two options', noSlides: 'No slides available',
  noNotes: 'No notes for this slide', slide: 'Slide', of: 'of', results: 'Result',
  flip: 'Flip card', front: 'Question', back: 'Answer', card: 'Card',
  nextCard: 'Next card', previousCard: 'Previous card',
  editPrompt: 'Edit your version', original: 'Original prompt',
  showOriginal: 'Show original', hideOriginal: 'Hide original', guidance: 'Practice guidance',
  threshold: 'Threshold', bounds: 'Available range', mayMatch: 'May match', canSkip: 'Can skip',
  enterNumber: 'Enter a number to see the result', invalidParameter: 'Parameter data is unavailable',
  possibleReason: 'The range allows at least one matching value; actual records may still differ.',
  skipReason: 'No value in the range can satisfy this condition.',
} : {
  previous: '이전', next: '다음', contents: '목차', progress: '진행률',
  theme: '테마 전환', fullscreen: '전체 화면', notes: '발표자 노트', source: '원문',
  language: '다른 언어', related: '관련 문서', review: '개념 다시 보기',
  close: '닫기', reset: '초기화', play: '실행', pause: '일시정지', step: '다음 단계',
  reveal: '보기', hide: '숨기기', choose: '선택하세요', check: '정답 확인',
  correct: '정답입니다', incorrect: '다시 생각해 보세요', explanation: '해설',
  copy: '복사', copied: '복사됨', objective: '학습 목표', details: '자세히',
  select: '구성 요소를 선택하세요', compare: '두 항목 비교', noSlides: '슬라이드가 없습니다',
  noNotes: '이 슬라이드의 노트가 없습니다', slide: '슬라이드', of: '/', results: '결과',
  flip: '카드 뒤집기', front: '앞면', back: '뒷면', card: '카드',
  nextCard: '다음 카드', previousCard: '이전 카드',
  editPrompt: '직접 수정하기', original: '원본 프롬프트',
  showOriginal: '원본 보기', hideOriginal: '원본 숨기기', guidance: '연습 안내',
  threshold: '기준값', bounds: '값의 범위', mayMatch: '읽을 가능성', canSkip: '건너뛰기',
  enterNumber: '결과를 보려면 숫자를 입력하세요', invalidParameter: '매개변수 데이터를 사용할 수 없습니다',
  possibleReason: '범위에 조건을 만족하는 값이 있을 수 있지만, 실제 데이터 존재 여부는 알 수 없습니다.',
  skipReason: '범위 안의 어떤 값도 이 조건을 만족할 수 없습니다.',
};

function safeUrl(value) {
  if (typeof value !== 'string' || !value.trim()) return null;
  const url = value.trim();
  if (/[\x00-\x1f\x7f]/.test(url)) return null;
  if (url.startsWith('//')) return null;
  if (/^(https?:|mailto:)/i.test(url) || /^(\/|\.\/|\.\.\/|#)/.test(url)) return url;
  if (!/^[a-z][a-z\d+.-]*:/i.test(url) && !url.startsWith('//')) return url;
  return null;
}

// A small allowlist protects the standalone viewer if a generated deck contains raw HTML.
function cleanHtml(html) {
  if (typeof html !== 'string' || !html) return '';
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const tags = new Set('p br strong em b i u s code pre blockquote ul ol li h1 h2 h3 h4 h5 h6 table thead tbody tr th td a img hr details summary kbd sub sup mark'.split(' '));
  const walk = (node) => {
    for (const child of [...node.children]) {
      if (!tags.has(child.tagName.toLowerCase())) {
        if (['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'FORM', 'INPUT', 'BUTTON', 'SVG'].includes(child.tagName)) child.remove();
        else { walk(child); child.replaceWith(...child.childNodes); }
        continue;
      }
      for (const attr of [...child.attributes]) {
        const name = attr.name.toLowerCase();
        const valid = name === 'title' || (child.tagName === 'IMG' && ['src', 'alt'].includes(name)) || (child.tagName === 'A' && name === 'href') || (['TH', 'TD'].includes(child.tagName) && ['colspan', 'rowspan'].includes(name));
        if (!valid || (['src', 'href'].includes(name) && !safeUrl(attr.value) && !/^data:image\/(?:png|jpeg|gif|webp);base64,/i.test(attr.value))) child.removeAttribute(attr.name);
      }
      if (child.tagName === 'A') child.setAttribute('rel', 'noopener noreferrer');
      walk(child);
    }
  };
  walk(doc.body);
  return doc.body.innerHTML;
}

function RichText({ html, className = '' }) {
  return <div className={className} dangerouslySetInnerHTML={{ __html: cleanHtml(html) }} />;
}

function Label({ children }) { return <span className="ui-label">{children}</span>; }

function ResetButton({ onClick }) {
  return <button type="button" className="subtle-button" onClick={onClick}>{words.reset}</button>;
}

function ItemDetail({ item }) {
  if (!item) return null;
  return <div className="interaction-detail" role="status" aria-live="polite">
    <strong>{item.label || item.title}</strong>
    <p>{item.detail || item.description || item.result || ''}</p>
  </div>;
}

function Steps({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [index, setIndex] = useState(-1);
  const [running, setRunning] = useState(false);
  useEffect(() => {
    if (!running) return undefined;
    const timer = window.setInterval(() => setIndex((value) => Math.min(value + 1, items.length - 1)), Math.max(400, Number(data.intervalMs) || 1200));
    return () => window.clearInterval(timer);
  }, [running, items.length, data.intervalMs]);
  useEffect(() => { if (index >= items.length - 1) setRunning(false); }, [index, items.length]);
  if (!items.length) return null;
  return <div className="interaction">
    <div className="interaction-toolbar">
      <button type="button" onClick={() => { if (index >= items.length - 1) setIndex(-1); setRunning(!running); }}>{running ? words.pause : words.play}</button>
      <button type="button" disabled={index >= items.length - 1} onClick={() => { setRunning(false); setIndex((value) => value + 1); }}>{words.step}</button>
      <ResetButton onClick={() => { setRunning(false); setIndex(-1); }} />
    </div>
    <ol className="step-track">
      {items.map((item, i) => <li key={i} className={i <= index ? 'is-active' : ''}>
        <button type="button" aria-current={i === index ? 'step' : undefined} onClick={() => { setRunning(false); setIndex(i); }}>
          <span className="step-number">{i + 1}</span><span>{item.label || `${words.step} ${i + 1}`}</span>
        </button>
      </li>)}
    </ol>
    <ItemDetail item={items[index]} />
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Architecture({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [index, setIndex] = useState(-1);
  if (!items.length) return null;
  return <div className="interaction">
    <div className="interaction-heading"><Label>{words.select}</Label><ResetButton onClick={() => setIndex(-1)} /></div>
    <div className="architecture-grid">
      {items.map((item, i) => <button key={i} type="button" className={`architecture-node ${index === i ? 'is-selected' : ''}`} aria-pressed={index === i} onClick={() => setIndex(i)}>
        <span className="node-index">{String(i + 1).padStart(2, '0')}</span><strong>{item.label || item.title}</strong>
      </button>)}
    </div>
    <ItemDetail item={items[index]} />
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Comparison({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [selected, setSelected] = useState(items.length > 1 ? [0, 1] : [0]);
  if (!items.length) return null;
  const pick = (index) => setSelected((prior) => prior.includes(index) ? prior.length > 1 ? prior.filter((value) => value !== index) : prior : [...prior.slice(-1), index]);
  return <div className="interaction">
    <div className="interaction-heading"><Label>{words.compare}</Label><ResetButton onClick={() => setSelected(items.length > 1 ? [0, 1] : [0])} /></div>
    <div className="choice-row">{items.map((item, i) => <button key={i} type="button" className={`choice-pill ${selected.includes(i) ? 'is-selected' : ''}`} aria-pressed={selected.includes(i)} onClick={() => pick(i)}>{item.label || item.title}</button>)}</div>
    <div className="comparison-grid">{selected.map((i) => <ItemDetail key={i} item={items[i]} />)}</div>
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Scenario({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [index, setIndex] = useState(-1);
  if (!items.length) return null;
  return <div className="interaction">
    <div className="interaction-heading"><Label>{data.prompt || words.choose}</Label><ResetButton onClick={() => setIndex(-1)} /></div>
    <div className="choice-row">{items.map((item, i) => <button key={i} type="button" className={`choice-pill ${index === i ? 'is-selected' : ''}`} aria-pressed={index === i} onClick={() => setIndex(i)}>{item.label || item.title}</button>)}</div>
    <ItemDetail item={items[index]} />
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Reveal({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [opened, setOpened] = useState([]);
  const toggle = (i) => setOpened((prior) => prior.includes(i) ? prior.filter((value) => value !== i) : [...prior, i]);
  if (!items.length) return null;
  return <div className="interaction">
    <div className="interaction-heading"><Label>{data.prompt || words.reveal}</Label><ResetButton onClick={() => setOpened([])} /></div>
    <div className="reveal-list">{items.map((item, i) => <div className="reveal-item" key={i}>
      <button type="button" aria-expanded={opened.includes(i)} onClick={() => toggle(i)}><span>{item.label || item.title}</span><span aria-hidden="true">{opened.includes(i) ? '−' : '+'}</span></button>
      {opened.includes(i) && <div className="reveal-content" role="status">{item.detail || item.description || item.result}</div>}
    </div>)}</div>
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Quiz({ data }) {
  const options = Array.isArray(data.options) ? data.options : [];
  const [selection, setSelection] = useState(-1);
  const [checked, setChecked] = useState(false);
  if (!options.length) return null;
  const correct = selection === Number(data.correctIndex);
  return <div className="interaction quiz">
    <div className="interaction-heading"><Label>{data.question || words.choose}</Label><ResetButton onClick={() => { setSelection(-1); setChecked(false); }} /></div>
    <div className="quiz-options" role="radiogroup" aria-label={data.question || words.choose}>
      {options.map((option, i) => <button type="button" role="radio" aria-checked={selection === i} className={`quiz-option ${selection === i ? 'is-selected' : ''}`} key={i} onClick={() => { setSelection(i); setChecked(false); }}><span>{String.fromCharCode(65 + i)}</span>{typeof option === 'string' ? option : option.label}</button>)}
    </div>
    <button type="button" disabled={selection < 0} onClick={() => setChecked(true)}>{words.check}</button>
    {checked && <div className={`quiz-feedback ${correct ? 'is-correct' : 'is-incorrect'}`} role="status" aria-live="polite"><strong>{correct ? words.correct : words.incorrect}</strong>{data.explanation && <p><strong>{words.explanation}: </strong>{data.explanation}</p>}</div>}
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Flashcard({ data }) {
  const items = Array.isArray(data.items) ? data.items : [];
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  if (!items.length) return null;
  const current = items[index];
  const move = (next) => { setIndex(Math.max(0, Math.min(items.length - 1, next))); setFlipped(false); };
  return <div className="interaction flashcard" onKeyDown={(event) => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); move(index - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); move(index + 1); }
  }}>
    <div className="interaction-heading"><Label>{words.card} {index + 1} / {items.length}</Label><ResetButton onClick={() => { setIndex(0); setFlipped(false); }} /></div>
    <button type="button" className="flashcard-face" aria-pressed={flipped} onClick={() => setFlipped((value) => !value)}>
      <span className="flashcard-side">{flipped ? words.back : words.front}</span>
      <span className="flashcard-text">{flipped ? current.detail || '' : current.label || ''}</span>
      <span className="flashcard-hint">{words.flip} ↻</span>
    </button>
    <div className="interaction-toolbar flashcard-controls">
      <button type="button" disabled={index === 0} onClick={() => move(index - 1)}>← {words.previousCard}</button>
      <button type="button" disabled={index === items.length - 1} onClick={() => move(index + 1)}>{words.nextCard} →</button>
    </div>
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function Practice({ data }) {
  const original = typeof data.prompt === 'string' ? data.prompt : '';
  const [draft, setDraft] = useState(original);
  const [showOriginal, setShowOriginal] = useState(false);
  const editorId = useId();
  if (!original && !data.guidance) return null;
  return <div className="interaction practice">
    <div className="interaction-heading"><Label>{words.guidance}</Label><ResetButton onClick={() => { setDraft(original); setShowOriginal(false); }} /></div>
    {data.guidance && <p className="practice-guidance">{data.guidance}</p>}
    <label className="practice-label" htmlFor={editorId}>{words.editPrompt}</label>
    <textarea id={editorId} spellCheck="false" value={draft} onChange={(event) => setDraft(event.target.value)} rows={Math.min(14, Math.max(6, original.split('\n').length + 2))} />
    <div className="interaction-toolbar practice-controls">
      <CopyButton text={draft} />
      <button type="button" aria-expanded={showOriginal} onClick={() => setShowOriginal((value) => !value)}>{showOriginal ? words.hideOriginal : words.showOriginal}</button>
    </div>
    {showOriginal && <div className="practice-original" role="region" aria-label={words.original}><strong>{words.original}</strong><pre>{original}</pre></div>}
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

function rangeCanMatch(minimum, maximum, operator, threshold) {
  if (operator === '>') return maximum > threshold;
  if (operator === '>=') return maximum >= threshold;
  if (operator === '<') return minimum < threshold;
  if (operator === '<=') return minimum <= threshold;
  return false;
}

function Parameter({ data }) {
  const inputId = useId();
  const rangeId = useId();
  const minimum = data.minimum;
  const maximum = data.maximum;
  const initial = data.threshold;
  const validData = typeof minimum === 'number' && Number.isFinite(minimum)
    && typeof maximum === 'number' && Number.isFinite(maximum) && minimum <= maximum
    && typeof initial === 'number' && Number.isFinite(initial)
    && ['>', '>=', '<', '<='].includes(data.operator);
  const [rawThreshold, setRawThreshold] = useState(String(initial ?? ''));
  if (!validData) return <div className="interaction" role="status">{words.invalidParameter}</div>;
  const entered = rawThreshold.trim() !== '' && Number.isFinite(Number(rawThreshold));
  const threshold = entered ? Number(rawThreshold) : initial;
  const low = Math.min(minimum, maximum, initial, threshold);
  const high = Math.max(minimum, maximum, initial, threshold);
  const padding = Math.max(3, Math.ceil((high - low) / 2));
  const sliderMinimum = Math.floor(low - padding);
  const sliderMaximum = Math.ceil(high + padding);
  const matches = entered && rangeCanMatch(minimum, maximum, data.operator, threshold);
  const reset = () => setRawThreshold(String(initial));
  return <div className="interaction parameter">
    <div className="interaction-heading"><Label>{data.field || words.bounds}</Label><ResetButton onClick={reset} /></div>
    <div className="parameter-summary">
      <span>min: <strong>{minimum}</strong></span>
      <code>{data.field || 'value'} {data.operator} {entered ? threshold : '…'}</code>
      <span>max: <strong>{maximum}</strong></span>
    </div>
    <label className="parameter-label" htmlFor={rangeId}>{words.threshold}</label>
    <div className="parameter-controls">
      <input id={rangeId} type="range" min={sliderMinimum} max={sliderMaximum} step="any" value={threshold} aria-valuetext={String(threshold)} onChange={(event) => setRawThreshold(event.target.value)} />
      <input id={inputId} type="number" inputMode="decimal" step="any" value={rawThreshold} aria-label={words.threshold} onChange={(event) => setRawThreshold(event.target.value)} />
    </div>
    <div className={`parameter-result ${entered ? matches ? 'may-match' : 'can-skip' : ''}`} role="status" aria-live="polite">
      <strong>{entered ? matches ? words.mayMatch : words.canSkip : words.enterNumber}</strong>
      {entered && <p>{matches ? words.possibleReason : words.skipReason}</p>}
    </div>
    {data.model_note && <p className="model-note">{data.model_note}</p>}
  </div>;
}

const interactions = { steps: Steps, architecture: Architecture, comparison: Comparison, scenario: Scenario, reveal: Reveal, quiz: Quiz, flashcard: Flashcard, practice: Practice, parameter: Parameter };

function Interaction({ interaction }) {
  const Component = interactions[interaction?.type];
  const data = { ...(interaction?.data || {}), model_note: interaction?.model_note ?? interaction?.data?.model_note };
  return Component ? <Component data={data} /> : null;
}

function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);
  const timer = useRef();
  useEffect(() => () => window.clearTimeout(timer.current), []);
  const copy = async () => {
    try {
      if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(text);
      else {
        const input = document.createElement('textarea');
        input.value = text; document.body.appendChild(input); input.select();
        try { if (!document.execCommand('copy')) throw new Error('Copy failed'); }
        finally { input.remove(); }
      }
      setCopied(true);
      window.clearTimeout(timer.current);
      timer.current = window.setTimeout(() => setCopied(false), 1800);
    } catch { setCopied(false); }
  };
  return <button type="button" className="copy-button" onClick={copy} aria-label={copied ? words.copied : words.copy}>{copied ? words.copied : words.copy}</button>;
}

function CodeCopy({ containerRef, slideId }) {
  const [blocks, setBlocks] = useState([]);
  useEffect(() => {
    const root = containerRef.current;
    if (!root) return;
    const code = [...root.querySelectorAll('pre')];
    setBlocks(code.map((node, i) => ({ id: i, text: node.textContent || '' })));
  }, [containerRef, slideId]);
  return blocks.length ? <div className="code-copy-row">{blocks.map((block) => <CopyButton key={block.id} text={block.text} />)}</div> : null;
}

function Slide({ slide, index }) {
  const contentRef = useRef(null);
  const interaction = slide.interaction || {};
  return <section className="slide-card" aria-label={`${words.slide} ${index + 1}: ${slide.title || ''}`}>
    <div className="slide-eyebrow"><span>{String(index + 1).padStart(2, '0')} / {String(slides.length).padStart(2, '0')}</span><span>{slide.section || deck.title || ''}</span></div>
    <div className="slide-main">
      <header><h1>{slide.title || deck.title}</h1>{slide.objective && <p className="objective"><strong>{words.objective}</strong> {slide.objective}</p>}</header>
      <div className="slide-content" ref={contentRef}>
        <RichText html={slide.body_html} className="rich-text" />
        <CodeCopy containerRef={contentRef} slideId={slide.id} />
        <Interaction key={`${slide.id || index}-${interaction.type || ''}`} interaction={interaction} />
      </div>
    </div>
    {slide.source?.heading && <footer className="slide-source">{slide.source.heading}</footer>}
  </section>;
}

function App() {
  const [index, setIndex] = useState(0);
  const [tocOpen, setTocOpen] = useState(false);
  const [notesOpen, setNotesOpen] = useState(false);
  const [reviewOpen, setReviewOpen] = useState(false);
  const [dark, setDark] = useState(() => window.matchMedia?.('(prefers-color-scheme: dark)').matches || false);
  const [studyMode, setStudyMode] = useState(false);
  const [reducedMotion, setReducedMotion] = useState(() => window.matchMedia?.('(prefers-reduced-motion: reduce)').matches || false);
  const shellRef = useRef(null);
  const headingRef = useRef(null);
  const slide = slides[index];
  const nav = (value) => { setIndex(Math.max(0, Math.min(slides.length - 1, value))); setTocOpen(false); setReviewOpen(false); };
  useEffect(() => { document.documentElement.dataset.slidesTheme = dark ? 'dark' : 'light'; }, [dark]);
  useEffect(() => {
    const query = window.matchMedia?.('(prefers-reduced-motion: reduce)');
    if (!query) return undefined;
    const update = () => setReducedMotion(query.matches);
    query.addEventListener?.('change', update);
    return () => query.removeEventListener?.('change', update);
  }, []);
  useEffect(() => { document.title = `${slide?.title || deck.title || 'Slides'} — Work Handbook`; headingRef.current?.focus(); }, [index, slide?.title]);
  useEffect(() => {
    const onKey = (event) => {
      if (event.altKey || event.ctrlKey || event.metaKey || /^(INPUT|TEXTAREA|SELECT)$/.test(event.target?.tagName) || event.target?.isContentEditable || event.target?.closest?.('.interaction')) return;
      if (event.key === 'Escape') { setTocOpen(false); setNotesOpen(false); setReviewOpen(false); return; }
      if (['ArrowRight', 'PageDown'].includes(event.key)) { event.preventDefault(); setIndex((value) => Math.min(slides.length - 1, value + 1)); }
      if (['ArrowLeft', 'PageUp'].includes(event.key)) { event.preventDefault(); setIndex((value) => Math.max(0, value - 1)); }
      if (event.key === 'Home') { event.preventDefault(); setIndex(0); }
      if (event.key === 'End') { event.preventDefault(); setIndex(slides.length - 1); }
      if (event.key.toLowerCase() === 'f') shellRef.current?.requestFullscreen?.();
      if (event.key.toLowerCase() === 'n') setNotesOpen((value) => !value);
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);
  if (!slide) return <div className="empty-state">{words.noSlides}</div>;
  const sourceLink = safeUrl(deck.source_url);
  const alternateLink = safeUrl(deck.alternate_url);
  const related = Array.isArray(deck.related) ? deck.related : [];
  return <div className={`app-shell ${studyMode ? 'study-mode' : 'present-mode'}`} ref={shellRef}>
    <a className="skip-link" href="#slide-content">{english ? 'Skip to slide' : '슬라이드로 건너뛰기'}</a>
    <header className="app-header">
      <button type="button" className="brand" onClick={() => nav(0)} aria-label={deck.title || 'Work Handbook'}><span className="brand-mark">W</span><span>{deck.title || 'Work Handbook'}</span></button>
      <div className="header-actions">
        <button type="button" onClick={() => setTocOpen(true)} aria-expanded={tocOpen}>{words.contents}</button>
        <button type="button" onClick={() => setStudyMode((value) => !value)} aria-pressed={studyMode}>{studyMode ? (english ? 'Present' : '발표 모드') : (english ? 'Study' : '학습 모드')}</button>
        <button type="button" onClick={() => setDark((value) => !value)} aria-label={words.theme}>{dark ? '☀' : '☾'}</button>
      </div>
    </header>
    <main id="slide-content" className="presentation-main">
      <div tabIndex={-1} ref={headingRef} className="focus-anchor" aria-live="polite" aria-atomic="true">{words.slide} {index + 1} {words.of} {slides.length}: {slide.title}</div>
      {reducedMotion ? <Slide key={slide.id || index} slide={slide} index={index} /> : <SlideTransition slideKey={slide.id || index} variant="fade"><Slide slide={slide} index={index} /></SlideTransition>}
      <nav className="slide-controls" aria-label={english ? 'Slide navigation' : '슬라이드 이동'}>
        <button type="button" disabled={index === 0} onClick={() => nav(index - 1)}>← {words.previous}</button>
        <div className="progress-wrap"><div className="progress-track" role="progressbar" aria-label={words.progress} aria-valuemin={1} aria-valuemax={slides.length} aria-valuenow={index + 1}><span style={{ width: `${((index + 1) / slides.length) * 100}%` }} /></div><small>{index + 1} / {slides.length}</small></div>
        <button type="button" disabled={index === slides.length - 1} onClick={() => nav(index + 1)}>{words.next} →</button>
      </nav>
    </main>
    <footer className="app-footer">
      <div className="footer-actions">
        <button type="button" onClick={() => setReviewOpen(true)}>{words.review}</button>
        <button type="button" onClick={() => setNotesOpen((value) => !value)} aria-expanded={notesOpen}>{words.notes}</button>
        <button type="button" onClick={() => document.fullscreenElement ? document.exitFullscreen?.() : shellRef.current?.requestFullscreen?.()}>{words.fullscreen}</button>
      </div>
      <div className="footer-links">
        {sourceLink && <a href={sourceLink}>{words.source} ↗</a>}
        {alternateLink && <a href={alternateLink} lang={english ? 'ko' : 'en'}>{words.language} ↗</a>}
        {related.filter((item) => safeUrl(typeof item === 'string' ? item : item.href || item.url)).map((item, i) => <a key={i} href={safeUrl(typeof item === 'string' ? item : item.href || item.url)}>{typeof item === 'string' ? words.related : item.label || item.title || words.related} ↗</a>)}
      </div>
    </footer>
    {notesOpen && <aside className="notes-panel" aria-label={words.notes}><div className="panel-title"><h2>{words.notes}</h2><button type="button" onClick={() => setNotesOpen(false)}>{words.close}</button></div>{slide.notes_html ? <RichText html={slide.notes_html} className="rich-text" /> : <p>{words.noNotes}</p>}</aside>}
    {(tocOpen || reviewOpen) && <div className="overlay" onClick={() => { setTocOpen(false); setReviewOpen(false); }}><aside className="drawer" onClick={(event) => event.stopPropagation()} aria-label={reviewOpen ? words.review : words.contents}><div className="panel-title"><h2>{reviewOpen ? words.review : words.contents}</h2><button type="button" onClick={() => { setTocOpen(false); setReviewOpen(false); }}>{words.close}</button></div><ol>{slides.map((item, i) => <li key={item.id || i}><button type="button" aria-current={i === index ? 'page' : undefined} onClick={() => nav(i)}><span>{String(i + 1).padStart(2, '0')}</span><span><strong>{item.title}</strong>{(reviewOpen ? item.objective : item.section) && <small>{reviewOpen ? item.objective : item.section}</small>}</span></button></li>)}</ol></aside></div>}
  </div>;
}

createRoot(document.getElementById('root')).render(<App />);
