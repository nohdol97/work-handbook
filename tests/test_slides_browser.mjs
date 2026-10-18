import { chromium } from '@playwright/test';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const root = resolve('_workspace/handbook-slides');
const evidence = resolve('_workspace/slide-qa/study/presentation');
await mkdir(evidence, { recursive: true });
const manifest = JSON.parse(await readFile(join(root, 'manifest.json'), 'utf8')).pages;
const chrome = process.env.CHROME_PATH || (process.platform === 'darwin' ? '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' : undefined);
const browser = await chromium.launch({ headless: true, ...(chrome ? { executablePath: chrome } : {}) });
const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, reducedMotion: 'reduce' });
await context.setOffline(true);
const page = await context.newPage();
const errors = [], failures = [], observations = [];
page.on('pageerror', error => errors.push(error.message));
page.on('request', request => { if (/^https?:/i.test(request.url())) errors.push(`unexpected network request: ${request.url()}`); });
function assert(condition, message) { if (!condition) throw new Error(message); }
function fileFor(key) {
  const [lang, ...parts] = key.split('/');
  const rel = parts.join('/');
  return join(root, lang, rel.endsWith('/index.md') || rel === 'index.md' ? rel.replace(/index\.md$/, 'index.html') : rel.replace(/\.md$/, '/index.html'));
}
async function open(key, match) {
  await page.goto(pathToFileURL(fileFor(key)).href+'#mode=presentation');
  await page.locator('.slide-card').first().waitFor();
  await page.waitForTimeout(250); // Same-file hash navigation may overlap the renderer's 100ms resize pagination.
  if (match) {
    const id = await page.evaluate(pattern => (() => {const s=window.__HANDBOOK_SLIDES__.slides.find(s => s.section_id===pattern)||window.__HANDBOOK_SLIDES__.slides.find(s => new RegExp(pattern, 'i').test(s.title));return s?.unit_id || s?.id})(), match);
    assert(id, `missing representative ${match}: ${key}`);
    await page.evaluate(id => { location.hash = new URLSearchParams({mode:'presentation',unit:id,part:0}).toString(); }, id);
    await page.waitForTimeout(150);
  }
}
async function selectParameter(unit) {
  await page.evaluate(unit => { location.hash = new URLSearchParams({mode:'presentation',unit,panel:'parameter'}).toString(); }, unit);
  await page.waitForFunction(unit => document.querySelector('.slide-card')?.dataset.unitId === unit &&
    new URLSearchParams(location.hash.slice(1)).get('panel') === 'parameter' &&
    !!document.querySelector('.slide-card .parameter input[type="number"]'), unit);
  await page.locator('.parameter input[type="number"]').waitFor({state:'visible'});
}
async function audit(label, allowPending = false) {
  const issues = await page.evaluate(allowPending => {
    const issues = [], tolerance = 2;
    if(!allowPending && document.querySelector('.slide-card')?.dataset.layoutStatus==='pending') issues.push('reviewed content cannot fit: pending fallback');
    const visible = e => { const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.visibility!=='hidden'&&s.display!=='none'&&Number(s.opacity)!==0&&r.width>1&&r.height>1; };
    for (const e of [document.documentElement, document.body, ...document.querySelectorAll('.app-shell *')]) {
      if (!visible(e) || e.closest('.sr-only,.visually-hidden,.focus-anchor,.skip-link,.measure,.assistive-navigation')) continue;
      const r=e.getBoundingClientRect(),s=getComputedStyle(e);
      if (r.width<=2 || r.height<=2) continue;
      const name=`${e.tagName}.${e.className}`.slice(0,100);
      if(e.scrollWidth>e.clientWidth+tolerance || e.scrollHeight>e.clientHeight+tolerance) issues.push(`${name}: internal overflow ${e.scrollWidth}x${e.scrollHeight}/${e.clientWidth}x${e.clientHeight} (${s.overflow})`);
      if(r.left < -tolerance || r.top < -tolerance || r.right>innerWidth+tolerance || r.bottom>innerHeight+tolerance) issues.push(`${name}: outside viewport ${[r.left,r.top,r.right,r.bottom].map(Math.round)}`);
    }
    const contentLast=document.querySelector('.slide-card .rich-text')?.lastElementChild;
    if(contentLast && /^H[2-6]$/.test(contentLast.tagName)) issues.push(`orphan heading: ${contentLast.textContent}`);
    const walker=document.createTreeWalker(document.querySelector('.slide-card'),NodeFilter.SHOW_TEXT);
    while(walker.nextNode()) {
      const n=walker.currentNode,p=n.parentElement;if(!n.textContent.trim()||!visible(p))continue;
      const s=getComputedStyle(p);if(parseFloat(s.fontSize)<14 && p.closest('.slide-content'))issues.push(`small content font ${s.fontSize}: ${n.textContent.slice(0,50)}`);
      const range=document.createRange();range.selectNodeContents(n);
      for(const r of range.getClientRects())if(r.left < -2||r.top < -2||r.right>innerWidth+2||r.bottom>innerHeight+2)issues.push(`text outside viewport: ${n.textContent.slice(0,60)}`);
      for(let a=p;a&&a!==document.body;a=a.parentElement){const style=getComputedStyle(a);if(/hidden|clip/.test(style.overflow+style.overflowX+style.overflowY)){const b=a.getBoundingClientRect();for(const r of range.getClientRects())if(r.left<b.left-2||r.right>b.right+2||r.top<b.top-2||r.bottom>b.bottom+2)issues.push(`text clipped by ${a.className}: ${n.textContent.slice(0,50)}`);}}
    }
    return [...new Set(issues)];
  }, allowPending);
  const layoutStatus=await page.locator('.slide-card').getAttribute('data-layout-status');
  observations.push({label,issues,layoutStatus,reviewStatus:allowPending?'unreviewed, pending permitted':'reviewed representative'});
  if(issues.length) console.log(`Geometry: ${label}: ${issues.slice(0,2).join('; ')}`);
  if(issues.length)failures.push(`${label}: ${issues.slice(0,8).join('; ')}`);
}
const representatives = [
  ['data-platform/flink.md','watermark','watermark'],
  ['aws-cloud/networking.md','sg-nacl','sg-nacl'],
  ['data-platform/production-operations.md','schema-break','schema-break'],
  ['english-study/vocabulary.md','vocab-check','english-check'],
  ['prompts/flink.md','flink-01','prompt'],
  ['ai-model-development/qlora-training.md','qlora-flow','qlora'],
];
try {
  const keys=Object.keys(manifest);
  for(const key of (process.env.SLIDES_SKIP_LOAD ? [] : keys)){await open(key);assert(await page.locator('h1').first().isVisible(),`title missing ${key}`);const forbidden=await page.evaluate(()=>window.__HANDBOOK_SLIDES__.slides.filter(s=>['quiz','flashcard','practice'].includes(s.interaction?.type)).length);assert(!forbidden,`assessment/edit gate remains ${key}`);}
  console.log(process.env.SLIDES_SKIP_LOAD ? 'Loading smoke skipped for focused audit' : `Loading: ${keys.length} offline decks PASS (separate from explanation quality)`);
  for(const [width,height] of [[320,568],[390,844],[768,1024],[1280,720],[844,390]]){
    await page.setViewportSize({width,height});
    for(const lang of ['ko','en'])for(const [path,match,name] of representatives){
      const key=`${lang}/${path}`;
      if(!manifest[key]){failures.push(`missing sample ${key}`);continue;}
      try{await open(key,match);const section=await page.locator('.slide-card').getAttribute('data-section-id');let continuations=0;const visibleText=[];do {visibleText.push(await page.locator('.slide-content').innerText());await audit(`${key} ${width}x${height} part${continuations}`);await page.keyboard.press('ArrowRight');await page.waitForTimeout(20);continuations++;} while(continuations<100 && await page.locator('.slide-card').getAttribute('data-section-id')===section);observations.push({label:`${key} ${width}x${height} visible meaning`,text:visibleText.join('\n')});if(name==='prompt' && /===\s*"|```/.test(visibleText.join(' '))) failures.push(`${key} ${width}: raw Markdown syntax exposed`);if(name==='watermark')for(const expected of ['10:01:03','10:01:05','10:01:10','late','idle'])if(!visibleText.join(' ').toLowerCase().includes(expected))failures.push(`${key} ${width}: missing visible ${expected}`);if(name==='sg-nacl')for(const expected of ['Security Group','NACL','ENI'])if(!visibleText.join(' ').includes(expected))failures.push(`${key} ${width}: missing visible ${expected}`);if(name==='schema-break')for(const expected of ['BIGINT','STRING','Producer','Dashboard'])if(!visibleText.join(' ').includes(expected))failures.push(`${key} ${width}: missing visible ${expected}`);await open(key,match);await page.screenshot({path:join(evidence,`${name}-${lang}-${width}x${height}.png`)});}catch(error){failures.push(error.message);}
    }
  }
  await page.setViewportSize({width:390,height:844});
  await open('en/data-platform/flink.md','Watermark');
  const zoomUnit=await page.locator('.slide-card').getAttribute('data-unit-id');
  await page.addStyleTag({content:'.rich-text {font-size:200% !important}'});
  await page.evaluate(()=>window.dispatchEvent(new Event('resize')));await page.waitForTimeout(250);await audit('Watermark 200% text');
  await page.setViewportSize({width:844,height:390});await page.waitForTimeout(250);await audit('Watermark 200% text rotated');
  assert(await page.locator('.slide-card').getAttribute('data-unit-id')===zoomUnit,'rotation lost explanation unit');
  await page.setViewportSize({width:390,height:844});
  await open('ko/data-platform/architecture.md');
  const position = () => page.evaluate(()=>location.hash);
  const settleNavigation = async () => {
    await page.waitForFunction(() => {
      const params = new URLSearchParams(location.hash.slice(1));
      const card = document.querySelector('.slide-card');
      return card?.dataset.unitId === params.get('unit') &&
        Number(card.dataset.part) === Number(params.get('part') || 0) &&
        Boolean(card.querySelector('.parameter')) === (params.get('panel') === 'parameter');
    });
  };
  const backgroundPoint = async side => {
    const point = await page.locator('.presentation-main').evaluate((main, side) => {
      const r = main.getBoundingClientRect();
      const x = side === 'left' ? r.left + 3 : r.right - 3;
      const y = r.top + r.height / 2;
      const target = document.elementFromPoint(x, y);
      return {x, y, isBackground: target === main, target: target?.tagName + '.' + target?.className};
    }, side);
    assert(point.isBackground, `navigation target is content instead of main padding: ${point.target}`);
    return point;
  };
  await settleNavigation();
  const first = await position();
  await page.keyboard.press('ArrowLeft');await settleNavigation();assert(await position()===first,'first slide wrapped');
  await page.keyboard.press('ArrowRight');await page.waitForFunction(previous=>location.hash!==previous,first);await settleNavigation();assert(await position()!==first,'keyboard next failed');
  await page.keyboard.press('ArrowLeft');await page.waitForFunction(expected=>location.hash===expected,first);await settleNavigation();assert(await position()===first,'keyboard previous failed');
  let margin = await backgroundPoint('left');await page.mouse.click(margin.x,margin.y);await settleNavigation();assert(await position()===first,'first background click wrapped');
  margin = await backgroundPoint('right');await page.mouse.click(margin.x,margin.y);await page.waitForFunction(previous=>location.hash!==previous,first);await settleNavigation();assert(await position()!==first,'right background navigation failed');
  margin = await backgroundPoint('left');await page.mouse.click(margin.x,margin.y);await page.waitForFunction(expected=>location.hash===expected,first);await settleNavigation();assert(await position()===first,'left background navigation failed');
  const dragStart=await backgroundPoint('left'),dragEnd=await backgroundPoint('right');
  await page.mouse.move(dragStart.x,dragStart.y);await page.mouse.down();await page.mouse.move(dragEnd.x,dragEnd.y,{steps:10});await page.mouse.up();await settleNavigation();assert(await position()===first,'drag navigated');
  await page.keyboard.press('End');await settleNavigation();const last=await position();await page.keyboard.press('ArrowRight');await settleNavigation();assert(await position()===last,'last slide wrapped');
  margin=await backgroundPoint('right');await page.mouse.click(margin.x,margin.y);await settleNavigation();assert(await position()===last,'last background click wrapped');
  await open('ko/data-platform/foundations.md');
  const parameterId=await page.evaluate(()=>(() => {const s=window.__HANDBOOK_SLIDES__.slides.find(s=>s.interaction?.type==='parameter');return s?.unit_id || s?.id})());
  assert(parameterId,'Statistics parameter missing');
  await page.evaluate(id=>location.hash=new URLSearchParams({mode:'presentation',unit:id,panel:'content',part:0}).toString(),parameterId);
  await page.waitForFunction(id=>document.querySelector('.slide-card')?.dataset.unitId===id&&!document.querySelector('.parameter'),parameterId);
  await page.evaluate(()=>document.activeElement.blur());
  for(let i=0;i<30 && !await page.locator('input[type="number"]').count();i++){await page.keyboard.press('ArrowRight');await page.waitForTimeout(30);}await page.locator('input[type="number"]').waitFor();
  const threshold=page.locator('input[type="number"]');
  for(const [input,result] of [['300','may-match'],['500','can-skip'],['1000','can-skip']]){
    const beforeInput=await position();await threshold.fill(input);assert(await position()===beforeInput,'number input navigated');await page.locator(`.parameter-result.${result}`).waitFor();await audit(`statistics ${input} -> ${result}`);await page.screenshot({path:join(evidence,`statistics-${input}-390x844.png`)});
  }
  await threshold.fill('300');
  for(const [width,height] of [[320,568],[844,390],[390,844]]){await page.setViewportSize({width,height});await page.waitForTimeout(300);assert(await threshold.count()===1,'resize lost visible parameter panel');assert(await threshold.inputValue()==='300','resize lost parameter input');await page.locator('.parameter-result.may-match').waitFor();await audit(`parameter resize preserves300 ${width}x${height}`);}
  for(const [width,height] of [[320,568],[390,844],[768,1024],[1280,720],[844,390]]){
    await page.setViewportSize({width,height});await open('ko/data-platform/foundations.md');await selectParameter(parameterId);
    await threshold.waitFor();
    for(const [input,result] of [['300','may-match'],['1000','can-skip']]){await threshold.fill(input);await page.locator(`.parameter-result.${result}`).waitFor();await audit(`Statistics ${width}x${height} ${input}`);await page.screenshot({path:join(evidence,`statistics-${input}-${width}x${height}.png`)});}
    for(const name of [/^(목차|Contents)$/,/^(보충 노트|Notes)$/]){await page.getByRole('button',{name}).click();await page.getByRole('dialog').waitFor();await audit(`${name} ${width}x${height}`);await page.keyboard.press('Escape');}
  }
  await page.setViewportSize({width:390,height:844});await open('ko/data-platform/foundations.md');await selectParameter(parameterId);await threshold.waitFor();
  const beforeSlider=await position();const slider=page.locator('input[type="range"]');await slider.focus();await page.keyboard.press('ArrowRight');assert(await position()===beforeSlider,'slider arrow navigated');
  const sliderRect=await slider.boundingBox();await page.mouse.move(sliderRect.x+sliderRect.width/2,sliderRect.y+sliderRect.height/2);await page.mouse.down();await page.mouse.move(sliderRect.x+sliderRect.width-5,sliderRect.y+sliderRect.height/2,{steps:10});await page.mouse.up();assert(await position()===beforeSlider,'slider drag navigated');
  await page.getByRole('button',{name:/^(초기화|Reset)$/}).click();assert(await threshold.inputValue()==='1000','reset expected1000');
  const tabTo=async locator=>{for(let i=0;i<50;i++){if(await locator.evaluate(e=>e===document.activeElement))return;await page.keyboard.press('Tab');}throw new Error('keyboard target unreachable');};
  await tabTo(threshold);await page.keyboard.press('ControlOrMeta+A');await page.keyboard.type('300');await page.locator('.parameter-result.may-match').waitFor();
  await tabTo(page.getByRole('button',{name:/^(초기화|Reset)$/}));await page.keyboard.press('Enter');assert(await threshold.inputValue()==='1000','keyboard reset failed');
  await tabTo(page.getByRole('button',{name:/^(목차|Contents)$/}));await page.keyboard.press('Enter');await page.getByRole('dialog').waitFor();await page.keyboard.press('Tab');await page.keyboard.press('Enter');await page.getByRole('dialog').waitFor({state:'hidden'});assert(!await page.getByRole('dialog').count(),'keyboard TOC selection failed');
  const selectedPosition=await position();await tabTo(page.getByRole('button',{name:/^(다음 슬라이드|Next slide)$/}));await page.keyboard.press('Enter');assert(await position()!==selectedPosition,'accessible keyboard next failed');
  await open('ko/data-platform/foundations.md');await selectParameter(parameterId);await threshold.waitFor();
  await page.setViewportSize({width:1280,height:720});await page.waitForTimeout(250);await page.evaluate(()=>document.activeElement.blur());await threshold.waitFor();await threshold.fill('300');await audit('statistics desktop longest result');await page.screenshot({path:join(evidence,'statistics-300-1280x720.png')});await page.setViewportSize({width:390,height:844});await page.waitForTimeout(250);
  await page.getByRole('button',{name:/^(목차|Contents)$/}).click();
  const dialog=page.getByRole('dialog');await dialog.waitFor();await audit('contents open');await page.screenshot({path:join(evidence,'contents-390x844.png')});
  for(let i=0;i<25;i++){await page.keyboard.press('Tab');assert(await page.evaluate(()=>!!document.activeElement.closest('[role="dialog"]')),'TOC focus escaped');}
  await page.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});assert(!await dialog.count(),'Escape failed');
  await page.waitForFunction(()=>/^(목차|Contents)$/.test(document.activeElement?.textContent||''));
  assert(await page.getByRole('button',{name:/^(목차|Contents)$/}).evaluate(e=>e===document.activeElement),'TOC focus restore failed');
  await page.getByRole('button',{name:/^(보충 노트|Notes)$/}).click();await dialog.waitFor();await audit('notes open');await page.screenshot({path:join(evidence,'notes-390x844.png')});await page.keyboard.press('Escape');
  // Select text and click a link with navigation canceled: neither gesture may advance a slide.
  await open('ko/data-platform/flink.md','watermark');const beforeSelection=await position();
  const textRect=await page.locator('.slide-content p').first().boundingBox();await page.mouse.move(textRect.x+5,textRect.y+10);await page.mouse.down();await page.mouse.move(textRect.x+textRect.width-5,textRect.y+textRect.height-5,{steps:10});await page.mouse.up();assert(await position()===beforeSelection,'text selection triggered slide navigation');await page.evaluate(()=>getSelection().removeAllRanges());
  const source=page.locator('.app-footer [data-source-link]');await source.evaluate(e=>e.addEventListener('click',event=>event.preventDefault(),{once:true}));await source.click();assert(await position()===beforeSelection,'link click advanced slide');
  assert(!await page.getByRole('radio').count(),'quiz radios remain');
  await open('ko/data-platform/flink.md','Watermark');const hash=new URL(page.url()).hash;await page.reload();assert(new URL(page.url()).hash===hash,'reload lost unit');
  const alternate=page.locator('.app-footer [data-language-link]');const alternateParams=new URLSearchParams((await alternate.getAttribute('href')).split('#')[1]);assert(alternateParams.get('section')===new URLSearchParams(hash.slice(1)).get('section'),'language switch loses semantic section');
  // Resolve the generated public alternate path into the same offline artifact tree, then actually follow the link.
  const beforeLanguageSection=await page.locator('.slide-card').getAttribute('data-section-id');const originalUrl=page.url();
  const publicAlternate=await alternate.getAttribute('href');const alternatePath=publicAlternate.split('#')[0].split('/slides/')[1];assert(alternatePath,'alternate slide route missing');
  await alternate.evaluate((e,href)=>e.href=href,pathToFileURL(join(root,alternatePath,alternatePath.endsWith('.html')?'':'index.html')).href+'#'+publicAlternate.split('#')[1]);await alternate.click();await page.locator('.slide-card').waitFor();await page.waitForTimeout(150);assert(await page.locator('.slide-card').getAttribute('data-section-id')===beforeLanguageSection,'actual language navigation changed semantic section');
  await page.reload();await page.locator('.slide-card').waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===beforeLanguageSection,'alternate reload changed section');
  await page.goBack();await page.locator('.slide-card').waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===beforeLanguageSection,'browser Back changed section');await page.goForward();await page.locator('.slide-card').waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===beforeLanguageSection,'browser Forward changed section');
  await page.getByRole('button',{name:/^(목차|Contents)$/}).click();await page.setViewportSize({width:844,height:390});await page.waitForTimeout(250);await audit('TOC rotated open');
  await page.addStyleTag({content:'.dialog {font-size:200% !important}'});await page.evaluate(()=>window.dispatchEvent(new Event('resize')));await page.waitForTimeout(250);await audit('TOC enlarged open');await page.keyboard.press('Escape');
  assert(!errors.length,errors.join('; '));
  await writeFile(join(evidence,'audit.json'),JSON.stringify({observations,failures,errors},null,2));
  assert(!failures.length,failures.join('\n'));
  console.log('Representative bilingual viewport, parameter boundaries, focus, unit position PASS');
} finally {await writeFile(join(evidence,'audit.json'),JSON.stringify({observations,failures,errors},null,2));await browser.close();}
