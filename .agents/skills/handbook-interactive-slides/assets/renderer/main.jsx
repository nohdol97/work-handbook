import React, { useEffect, useLayoutEffect, useId, useRef, useState } from 'react';
import { createRoot } from 'react-dom/client';
import './style.css';

const deck = window.__HANDBOOK_SLIDES__ || {};
const slides = Array.isArray(deck.slides) ? deck.slides : [];
const english = String(deck.language || '').toLowerCase().startsWith('en');
const words = english ? {
 previous:'Previous slide',next:'Next slide',contents:'Contents',notes:'Notes',source:'Source',language:'한국어',close:'Close',reset:'Reset',threshold:'Threshold',bounds:'Available range',mayMatch:'May match',canSkip:'Can skip',enterNumber:'Enter a number',invalidParameter:'Parameter unavailable',possibleReason:'The range allows a matching value; this does not prove a record exists.',skipReason:'No value in this range satisfies the condition.',hint:'Swipe ↔ · Tap margins · ← →',noNotes:'Supplementary notes are not available.',
} : {
 previous:'이전 슬라이드',next:'다음 슬라이드',contents:'목차',notes:'보충 노트',source:'원문',language:'English',close:'닫기',reset:'초기화',threshold:'기준값',bounds:'값의 범위',mayMatch:'읽을 가능성',canSkip:'건너뛰기',enterNumber:'숫자를 입력하세요',invalidParameter:'매개변수 없음',possibleReason:'범위에 조건을 만족하는 값이 있을 수 있지만, 실제 데이터 존재 여부는 알 수 없습니다.',skipReason:'범위 안의 어떤 값도 이 조건을 만족할 수 없습니다.',hint:'좌우 스와이프 · 여백 터치 · ← →',noNotes:'별도 보충 노트가 없습니다.',
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
  const tags = new Set('p br strong em b i u s code pre blockquote ul ol li h1 h2 h3 h4 h5 h6 table caption thead tbody tfoot tr th td a img hr details summary kbd sub sup mark'.split(' '));
  const walk = (node) => {
    for (const child of [...node.children]) {
      if (!tags.has(child.tagName.toLowerCase())) {
        if (['SCRIPT', 'STYLE', 'IFRAME', 'OBJECT', 'EMBED', 'FORM', 'INPUT', 'BUTTON', 'SVG'].includes(child.tagName)) child.remove();
        else { walk(child); child.replaceWith(...child.childNodes); }
        continue;
      }
      for (const attr of [...child.attributes]) {
        const name = attr.name.toLowerCase();
        const valid = name === 'title' || (child.tagName === 'CODE' && name === 'class' && /^language-[a-z0-9_-]+$/i.test(attr.value)) || (child.tagName === 'IMG' && ['src', 'alt'].includes(name)) || (child.tagName === 'A' && name === 'href') || (['TH', 'TD'].includes(child.tagName) && ['colspan', 'rowspan', 'scope'].includes(name));
        if (!valid || (['src', 'href'].includes(name) && !safeUrl(attr.value) && !/^data:image\/(?:png|jpeg|gif|webp);base64,/i.test(attr.value))) child.removeAttribute(attr.name);
      }
      if (child.tagName === 'A') child.setAttribute('rel', 'noopener noreferrer');
      if (child.tagName === 'DETAILS') child.setAttribute('open', '');
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

// Split source DOM, retaining inline markup, links, table headings and code order.
// Measurement uses the same typography as the visible slide, never a scale transform.
function fragments(html, narrow) {
  const doc = new DOMParser().parseFromString(cleanHtml(html), 'text/html');
  const result = [];
  const add = (node) => {
    if (!node.textContent.trim() && !node.querySelector?.('img')) return;
    const tag = node.tagName;
    if (['DIV','SECTION','ARTICLE'].includes(tag)) { [...node.children].forEach(add); return; }
    if (tag === 'TABLE') {
      const rows = [...node.querySelectorAll('tr')];
      const headers = rows.shift();
      const count = headers?.children.length || 0;
      const groups = narrow && count > 3 ? Array.from({length:count-1},(_,i)=>[0,i+1]) : [Array.from({length:count},(_,i)=>i)];
      for (const row of rows) for (const group of groups) {
        const cells = (r, head) => group.map(i => `<${head?'th':'td'}>${r.children[i]?.innerHTML || ''}</${head?'th':'td'}>`).join('');
        result.push(`<table><thead><tr>${cells(headers,true)}</tr></thead><tbody><tr>${cells(row,false)}</tr></tbody></table>`);
      }
      return;
    }
    if (tag === 'UL' || tag === 'OL') {
      [...node.children].forEach((li,i)=>result.push(`<${tag.toLowerCase()}${tag==='OL'?` start="${i+1}"`:''}>${li.outerHTML}</${tag.toLowerCase()}>`)); return;
    }
    result.push(node.outerHTML || `<p>${node.textContent}</p>`);
  };
  [...doc.body.childNodes].forEach(add);
  const grouped=[];
  for(let i=0;i<result.length;i++){
    let chunk=result[i];
    while(/^<h[1-6][ >]/i.test(result[i])&&i+1<result.length){chunk+=result[++i];}
    grouped.push(chunk);
  }
  return grouped;
}

function splitFragment(html) {
  const doc = new DOMParser().parseFromString(html, 'text/html');
  const elements=[...doc.body.children];
  if(elements.length>1){
    const heading=elements.shift().outerHTML;
    const parts=splitFragment(elements.map(e=>e.outerHTML).join(''));
    return parts.length>1 ? [heading+parts[0],...parts.slice(1)] : [html];
  }
  const root = doc.body.firstElementChild;
  if (!root || root.textContent.length < 2 || root.matches('table,pre,svg,img')) return [html];
  // DOM ranges preserve emphasis and links across a continuation.
  const text = root.textContent;
  const midpoint = Math.floor(text.length / 2);
  const boundaries = [...text.matchAll(/(?:[.!?。]\s+|\n)/g)].map(m=>m.index+m[0].length).filter(n=>n>0&&n<text.length);
  if (!boundaries.length) return [html];
  const cut = boundaries.reduce((a,b)=>Math.abs(b-midpoint)<Math.abs(a-midpoint)?b:a);
  const walker = doc.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let node, offset=0, target;
  while ((node=walker.nextNode())) { if (offset+node.length >= cut) { target=node; break; } offset+=node.length; }
  if (!target) return [html];
  const left=doc.createRange(),right=doc.createRange();
  left.selectNodeContents(root); left.setEnd(target,cut-offset);
  right.selectNodeContents(root); right.setStart(target,cut-offset);
  return [left,right].map(range=>{const copy=root.cloneNode(false);copy.append(range.cloneContents());return copy.outerHTML;});
}

// On a single page, adjacent comparison rows share their column headings.
// Each new page still begins with the complete table header.
function appendHtml(leftHtml, rightHtml) {
  if(!leftHtml)return rightHtml;
  const parser=new DOMParser();
  const left=parser.parseFromString(leftHtml,'text/html');
  const right=parser.parseFromString(rightHtml,'text/html');
  const previous=left.body.lastElementChild,next=right.body.firstElementChild;
  if(previous?.tagName==='TABLE'&&next?.tagName==='TABLE'
      &&previous.tHead?.innerHTML===next.tHead?.innerHTML
      &&previous.tHead&&next.tHead){
    const body=previous.tBodies[0]||previous.createTBody();
    for(const row of [...(next.tBodies[0]?.rows||[])])body.append(row);
    next.remove();
    return left.body.innerHTML+right.body.innerHTML;
  }
  return leftHtml+rightHtml;
}

function pendingNotice() { return `<p>${english?'This source block needs a reviewed layout for this screen. Read the complete block using the Source link below.':'이 원문 블록은 현재 화면에 맞는 설명 구성을 검토 중입니다. 아래 원문 링크에서 전체 내용을 읽을 수 있습니다.'}</p>`; }

function studyHtml(unit) {
  const source=Array.isArray(unit.content_blocks)&&unit.content_blocks.length?unit.content_blocks.map(b=>typeof b==='string'?b:b.html||'').join(''):unit.body_html;
  const doc=new DOMParser().parseFromString(cleanHtml(source),'text/html');
  for(const pre of doc.querySelectorAll('pre')){
    if(pre.querySelector('code.language-mermaid')||/[┌┐└┘├┤│─]/.test(pre.textContent)){
      const note=doc.createElement('p');
      note.textContent=english?'Static source notation. Long lines wrap on small screens; use the original document for its spatial layout. Arrows and labels below are preserved as source text.':'정적 원문 표기입니다. 작은 화면에서는 긴 줄이 줄바꿈되므로 공간 배치는 원문 문서에서 확인하세요. 아래 화살표와 이름은 원문 텍스트 그대로 유지합니다.';
      pre.before(note);
    }
  }
  if(innerWidth>=600)return doc.body.innerHTML;
  for(const table of doc.querySelectorAll('table')){
    const rows=[...table.rows],head=rows[0];
    if(!head||head.cells.length<=3||table.querySelector('[colspan],[rowspan]')||table.tHead?.rows.length>1)continue;
    const replacement=doc.createDocumentFragment();
    for(let column=1;column<head.cells.length;column++){
      const copy=doc.createElement('table');
      if(table.caption)copy.append(table.caption.cloneNode(true));
      for(const [index,row] of rows.entries()){
        const group=index===0?(copy.tHead||copy.createTHead()):(copy.tBodies[0]||copy.createTBody());
        const tr=group.insertRow();
        for(const n of [0,column])if(row.cells[n])tr.append(row.cells[n].cloneNode(true));
      }
      replacement.append(copy);
    }
    table.replaceWith(replacement);
  }
  return doc.body.innerHTML;
}

function positionKey(slide) { return slide.unit_id || slide.id; }
function sectionKey(slide) { return slide.section_id || slide.source?.section_id || slide.id; }
function locationState() { const params=new URLSearchParams(location.hash.slice(1));return {unit:params.get('unit'),section:params.get('section'),part:Number(params.get('part')||0),panel:params.get('panel')==='parameter'?'parameter':'content',mode:params.get('mode')==='presentation'?'presentation':'study'}; }
function App() {
  const [mode,setMode]=useState(locationState().mode);
  const [pages,setPages]=useState([]),[index,setIndex]=useState(0),[dialog,setDialog]=useState(null),[dialogPage,setDialogPage]=useState(0);
  const [notePages,setNotePages]=useState([]),[tocPages,setTocPages]=useState([]);
  const measure=useRef(), shell=useRef(), dialogRef=useRef(), returnFocus=useRef(), pointer=useRef();
  const reading=useRef(locationState());
  const page=pages[index],slide=page?.slide;
  const writeLocation=(p,replace=false)=>{
    if(!p)return;
    const activeUnit=mode==='study'&&p.units?.some(s=>positionKey(s)===reading.current.unit)?reading.current.unit:positionKey(p.slide);
    const state={unit:activeUnit,section:sectionKey(p.slide),part:p.part,panel:p.parameter?'parameter':'content',mode}; reading.current=state;
    const hash=new URLSearchParams(state).toString();
    if(location.hash.slice(1)!==hash)history[replace?'replaceState':'pushState'](null,'',`#${hash}`);
  };
  const nav=(value)=>{const n=Math.max(0,Math.min(pages.length-1,value));if(n===index)return;setIndex(n);writeLocation(pages[n]);if(mode==='study')window.scrollTo(0,0);};
  const changeMode=()=>{const next=mode==='study'?'presentation':'study';reading.current={...reading.current,mode:next};history.pushState(null,'',`#${new URLSearchParams(reading.current)}`);setMode(next);};
  useLayoutEffect(()=>{
    let timer;
    const rebuild=()=>{
      const host=measure.current;if(!host)return;
      const width=shell.current.clientWidth;
      if(mode==='study'){
        shell.current.style.height='auto';
        const next=[];
        for(const item of slides){
          let group=next.at(-1);
          if(!group||sectionKey(group.slide)!==sectionKey(item)){group={mode:'study',slide:item,units:[],part:0,parameter:false,pending:false};next.push(group);}
          group.units.push(item);
        }
        setPages(next);
        let found=next.findIndex(p=>p.units.some(s=>positionKey(s)===reading.current.unit));
        if(found<0)found=next.findIndex(p=>sectionKey(p.slide)===reading.current.section);
        setIndex(Math.max(0,found));
        return;
      }
      const height=window.visualViewport?.height || window.innerHeight;
      shell.current.style.height=`${height}px`;
      const header=shell.current.querySelector('.app-header').getBoundingClientRect().height;
      const footer=shell.current.querySelector('.app-footer').getBoundingClientRect().height;
      const available=height-header-footer-24;
      host.style.width=`${Math.min(1100,width)-32}px`;
      const next=[];
      for (const item of slides) {
        host.innerHTML=`<h1>${cleanHtml(item.title||deck.title)}</h1>`;
        const titleHeight=host.getBoundingClientRect().height;
        const budget=Math.max(80,available-titleHeight-24);
        const fits=(html)=>{host.innerHTML=`<div class="rich-text">${html}</div>`;return host.getBoundingClientRect().height<=budget && host.scrollWidth<=host.clientWidth;};
        const source=Array.isArray(item.content_blocks)&&item.content_blocks.length ? item.content_blocks.map(b=>typeof b==='string'?b:b.html||'').join('') : item.body_html;
        const pending=fragments(source||'',width<600), atoms=[];
        while(pending.length){const html=pending.shift();if(fits(html)){atoms.push(html);continue;}const divided=splitFragment(html);if(divided.length===1){atoms.push(pendingNotice());continue;}pending.unshift(...divided);}
        let body='',part=0;
        const emit=()=>{next.push({mode:'presentation',slide:item,html:body,part:part++,parameter:false,pending:body.includes('현재 화면에 맞는 설명')||body.includes('needs a reviewed layout')});body='';};
        for(const atom of atoms){const combined=appendHtml(body,atom);if(body&&!fits(combined)){emit();body=atom;}else body=combined;}
        if(body||!atoms.length)emit();
        if(item.interaction?.type==='parameter')next.push({mode:'presentation',slide:item,html:'',part:part++,parameter:true});
      }
      setPages(next);
      const state=reading.current;
      let found=next.findIndex(p=>positionKey(p.slide)===state.unit&&(state.panel==='parameter'?p.parameter:!p.parameter&&p.part===state.part));
      if(found<0)found=next.findIndex(p=>positionKey(p.slide)===state.unit);
      if(found<0)found=next.findIndex(p=>sectionKey(p.slide)===state.section);
      setIndex(Math.max(0,found));
    };
    rebuild();
    const resize=()=>{clearTimeout(timer);timer=setTimeout(rebuild,100);};
    window.addEventListener('resize',resize);window.visualViewport?.addEventListener('resize',resize);
    const observer=new ResizeObserver(resize);observer.observe(document.documentElement);
    document.fonts?.ready.then(rebuild);
    return()=>{clearTimeout(timer);window.removeEventListener('resize',resize);window.visualViewport?.removeEventListener('resize',resize);observer.disconnect();};
  },[mode]);
  useEffect(()=>{
    const restore=()=>{reading.current=locationState();const s=reading.current;if(s.mode!==mode){setMode(s.mode);return;}let n=pages.findIndex(p=>positionKey(p.slide)===s.unit&&(s.panel==='parameter'?p.parameter:!p.parameter&&p.part===s.part));if(n<0)n=pages.findIndex(p=>sectionKey(p.slide)===s.section);setIndex(Math.max(0,n));if(mode==='study')requestAnimationFrame(()=>{const target=shell.current.querySelector(`.study-unit[data-unit-id="${CSS.escape(s.unit||'')}"]`);target?.scrollIntoView({block:'start'});});};
    window.addEventListener('popstate',restore);window.addEventListener('hashchange',restore);
    return()=>{window.removeEventListener('popstate',restore);window.removeEventListener('hashchange',restore);};
  },[pages,mode]);
  useEffect(()=>{if(page&&page.mode===mode&&reading.current.mode===mode){document.title=`${slide.title} — Work Handbook`;writeLocation(page,true);}},[page]);
  useEffect(()=>{
    if(mode!=='study'||!page)return;
    const target=shell.current.querySelector(`.study-unit[data-unit-id="${CSS.escape(reading.current.unit||'')}"]`);
    if(target&&page.units?.[0]&&positionKey(page.units[0])!==reading.current.unit)target.scrollIntoView({block:'start'});
    const update=()=>{
      const units=[...shell.current.querySelectorAll('.study-unit')];
      const current=units.find(el=>el.getBoundingClientRect().bottom>100);
      if(!current)return;
      reading.current={...reading.current,unit:current.dataset.unitId,mode};
      history.replaceState(null,'',`#${new URLSearchParams(reading.current)}`);
      const link=shell.current.querySelector('[data-language-link]');
      if(link)link.hash=new URLSearchParams({section:reading.current.section,unit:reading.current.unit,mode}).toString();
    };
    window.addEventListener('scroll',update,{passive:true});
    return()=>window.removeEventListener('scroll',update);
  },[page,mode]);
  const close=()=>{setDialog(null);requestAnimationFrame(()=>returnFocus.current?.focus());};
  const open=(kind,event,preserve=false)=>{
    if(!preserve){returnFocus.current=event.currentTarget;setDialogPage(0);setDialog(kind);}
    const host=measure.current;
    const viewportHeight=window.visualViewport?.height||innerHeight;
    host.className='measure';
    host.style.width=`${Math.min(760,shell.current.clientWidth-24)}px`;
    const heading=kind==='toc'?words.contents:words.notes;
    const fitsPanel=(content)=>{
      // Measure the whole modal with the actual CSS, including enlarged controls,
      // header, footer, borders, padding and flex gaps. No guessed chrome budget.
      host.innerHTML=`<section class="dialog" style="max-height:none;width:100%"><header class="panel-title"><h2>${heading}</h2><button>${words.close}</button></header>${content}<nav class="dialog-pagination"><button>−</button><span>1 / 999</span><button>+</button></nav></section>`;
      const panel=host.firstElementChild;
      return panel.getBoundingClientRect().height<=viewportHeight-24 && panel.scrollWidth<=panel.clientWidth;
    };
    if(kind==='toc'){
      const groups=[];let group=[];
      const markup=items=>`<ol class="toc-list">${items.map(item=>`<li><button>${cleanHtml(item.slide.title)}</button></li>`).join('')}</ol>`;
      for(const item of toc){
        if(group.length&&!fitsPanel(markup([...group,item]))){groups.push(group);group=[];}
        group.push(item);
      }
      if(group.length)groups.push(group);setTocPages(groups);if(preserve)setDialogPage(n=>Math.min(n,Math.max(0,groups.length-1)));
    }
    if(kind==='notes'){
      const noteSlide=mode==='study'?(page.units?.find(unit=>positionKey(unit)===reading.current.unit)||slide):slide;
      const queue=fragments(noteSlide.notes_html||`<p>${words.noNotes}</p>`,innerWidth<600),out=[];
      while(queue.length){const h=queue.shift();if(!fitsPanel(`<div class="rich-text">${h}</div>`)){const pieces=splitFragment(h);if(pieces.length>1){queue.unshift(...pieces);continue;}out.push(pendingNotice());continue;}out.push(h);}
      setNotePages(out);if(preserve)setDialogPage(n=>Math.min(n,Math.max(0,out.length-1)));
    }
    host.innerHTML='';host.className='measure rich-text';

  };
  useEffect(()=>{if(dialog)dialogRef.current?.querySelector('button')?.focus();},[dialog]);
  useEffect(()=>{
    if(!dialog)return;
    let timer;
    const repaginate=()=>{clearTimeout(timer);timer=setTimeout(()=>{
      open(dialog,null,true);
      requestAnimationFrame(()=>{if(!dialogRef.current?.contains(document.activeElement))dialogRef.current?.querySelector('button')?.focus();});
    },160);};
    window.addEventListener('resize',repaginate);window.visualViewport?.addEventListener('resize',repaginate);
    return()=>{clearTimeout(timer);window.removeEventListener('resize',repaginate);window.visualViewport?.removeEventListener('resize',repaginate);};
  },[dialog,slide]);
  useEffect(()=>{
    const key=(event)=>{
      if(dialog){
        if(event.key==='Escape'){event.preventDefault();close();}
        if(event.key==='Tab'){
          const items=[...dialogRef.current.querySelectorAll('button:not(:disabled),a[href],input')];const first=items[0],last=items.at(-1);
          if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus();}
          else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus();}
        }return;
      }
      if(event.altKey||event.ctrlKey||event.metaKey||event.shiftKey||event.isComposing||window.getSelection()?.toString()||event.target.closest?.('input,textarea,select,button,a,[contenteditable],.interaction'))return;
      if(event.key==='ArrowRight'||(mode==='presentation'&&event.key==='PageDown')){event.preventDefault();nav(index+1);}
      if(event.key==='ArrowLeft'||(mode==='presentation'&&event.key==='PageUp')){event.preventDefault();nav(index-1);}
      if(mode==='presentation'&&event.key==='Home'){event.preventDefault();nav(0);}if(mode==='presentation'&&event.key==='End'){event.preventDefault();nav(pages.length-1);}
    };window.addEventListener('keydown',key);return()=>window.removeEventListener('keydown',key);
  },[dialog,index,pages,mode]);
  const controls='a,button,input,select,textarea,svg,pre,code,table,.interaction,[contenteditable]';
  const excluded=(target)=>target.closest(`${controls},p,li,h1,h2,h3,h4,blockquote`);
  useEffect(()=>{
    // A second finger anywhere on the page invalidates the complete gesture.
    const cancelMulti=event=>{if(event.pointerType==='touch'&&!event.isPrimary)pointer.current=null;};
    window.addEventListener('pointerdown',cancelMulti,true);
    return()=>window.removeEventListener('pointerdown',cancelMulti,true);
  },[]);
  const down=(event)=>{
    const touch=event.pointerType==='touch';
    pointer.current=event.button===0&&event.isPrimary&&!window.getSelection()?.toString()&&
      !(touch?event.target.closest(controls):excluded(event.target))?
      {x:event.clientX,y:event.clientY,id:event.pointerId,scroll:window.scrollY,time:performance.now(),touch,tap:!excluded(event.target)}:null;
  };
  const move=(event)=>{
    const start=pointer.current;if(!start||start.id!==event.pointerId)return;
    const dx=Math.abs(event.clientX-start.x),dy=Math.abs(event.clientY-start.y);
    if(start.touch&&dy>10&&dy>dx)pointer.current=null;
  };
  const up=(event)=>{
    const start=pointer.current;pointer.current=null;
    if(!start||start.id!==event.pointerId||Math.abs(window.scrollY-start.scroll)>2||window.getSelection()?.toString())return;
    const dx=event.clientX-start.x,dy=event.clientY-start.y;
    // Touch implicit capture retains the start target; inspect the actual end point too.
    const end=document.elementFromPoint(event.clientX,event.clientY);
    if(!end||!event.currentTarget.contains(end))return;
    if(start.touch&&Math.abs(dx)>=60&&Math.abs(dx)>=1.5*Math.abs(dy)&&performance.now()-start.time<=1000&&!end.closest(controls)){
      nav(index+(dx<0?1:-1));return;
    }
    if(!start.tap||excluded(end)||Math.hypot(dx,dy)>6)return;
    const rect=event.currentTarget.getBoundingClientRect();nav(index+(event.clientX<rect.left+rect.width/2?-1:1));
  };
  const toc=mode==='study'?pages.map((p,i)=>({slide:p.slide,index:i})):slides.map(s=>({slide:s,index:pages.findIndex(p=>p.slide===s)}));
  const count=dialog==='notes'?notePages.length:tocPages.length;
  const alternate=safeUrl(deck.alternate_url);
  const alternateHash=slide?new URLSearchParams({section:sectionKey(slide),unit:reading.current.unit||positionKey(slide),panel:page?.parameter?'parameter':'content',mode}).toString():'';
  return <div className={`app-shell ${mode}-mode`} data-view-mode={mode} ref={shell}>
    <div className="measure rich-text" ref={measure} aria-hidden="true" />
    <div className="viewer" inert={dialog?'':undefined} aria-hidden={dialog?true:undefined}>
      <header className="app-header"><a href={safeUrl(deck.source_url)||'#'} aria-label={words.source}>Work Handbook</a><div className="header-controls"><button data-mode-toggle onClick={changeMode}>{mode==='study'?(english?'Present':'발표 모드'):(english?'Study':'학습 모드')}</button><button onClick={e=>open('toc',e)} aria-haspopup="dialog">{words.contents}</button></div></header>
      <main className="presentation-main" onPointerDown={down} onPointerMove={move} onPointerUp={up} onPointerCancel={()=>{pointer.current=null;}}>
        {page&&<section className="slide-card" data-unit-id={positionKey(slide)} data-section-id={sectionKey(slide)} data-part={page.part} data-layout-status={page.pending?'pending':'rendered'} aria-label={slide.title}>
          <h1>{slide.title}</h1>
          {mode==='study'?<div className="study-units">{page.units?.map((unit,i)=><article className="study-unit" key={positionKey(unit)} data-unit-id={positionKey(unit)} data-section-id={sectionKey(unit)}>
            {i>0&&unit.title!==slide.title&&<h2>{unit.title}</h2>}
            <RichText className="rich-text" html={studyHtml(unit)}/>
            {unit.interaction?.type==='parameter'&&<Parameter data={{...unit.interaction.data,model_note:unit.interaction.model_note}}/>}
          </article>)}</div>:<div className="slide-content"><RichText className="rich-text" html={page.html}/>{page.parameter&&<Parameter data={{...slide.interaction.data,model_note:slide.interaction.model_note}}/>}</div>}
        </section>}
      </main>
      <footer className="app-footer"><div className="footer-row"><span aria-live="polite">{index+1} / {pages.length}</span><button onClick={e=>open('notes',e)}>{words.notes}</button><a data-source-link href={safeUrl(slide?.source?.url)||`${safeUrl(deck.source_url)||''}${slide?.source?.anchor?'#'+slide.source.anchor:''}`}>{words.source}</a>{alternate&&<a data-language-link href={`${alternate.split('#')[0]}#${alternateHash}`}>{words.language}</a>}</div><small>{words.hint}</small></footer>
      <nav className="assistive-navigation" aria-label={english?'Slide navigation':'슬라이드 이동'}><button disabled={index===0} onClick={()=>nav(index-1)}>{words.previous}</button><button disabled={index===pages.length-1} onClick={()=>nav(index+1)}>{words.next}</button></nav>
    </div>
    {dialog&&<div className="overlay"><section className="dialog" ref={dialogRef} role="dialog" aria-modal="true" aria-label={dialog==='toc'?words.contents:words.notes}>
      <header className="panel-title"><h2>{dialog==='toc'?words.contents:words.notes}</h2><button onClick={close}>{words.close}</button></header>
      {dialog==='toc'?<ol className="toc-list" start={1+tocPages.slice(0,dialogPage).reduce((n,items)=>n+items.length,0)}>{(tocPages[dialogPage]||[]).map(item=><li key={positionKey(item.slide)}><button aria-current={item.slide===slide?'page':undefined} onClick={()=>{nav(item.index);close();}}>{item.slide.title}</button></li>)}</ol>:<RichText className="rich-text" html={notePages[dialogPage]}/>}
      <nav className="dialog-pagination" aria-label={english?'Panel pages':'패널 페이지'}><button aria-label={english?'Previous panel page':'이전 패널 페이지'} disabled={dialogPage===0} onClick={()=>setDialogPage(n=>n-1)}>−</button><span>{dialogPage+1} / {count}</span><button aria-label={english?'Next panel page':'다음 패널 페이지'} disabled={dialogPage>=count-1} onClick={()=>setDialogPage(n=>n+1)}>+</button></nav>
    </section></div>}
  </div>;
}
createRoot(document.getElementById('root')).render(<App/>);
