import { chromium } from '@playwright/test';
import { mkdir, readFile, writeFile } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
const root=resolve('_workspace/handbook-slides'), evidence=resolve('_workspace/slide-qa/study');
await mkdir(evidence,{recursive:true});
const manifest=JSON.parse(await readFile(join(root,'manifest.json'),'utf8')).pages;
const executablePath=process.env.CHROME_PATH || (process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':undefined);
const browser=await chromium.launch({headless:true,...(executablePath?{executablePath}:{})});
const context=await browser.newContext({viewport:{width:320,height:568},reducedMotion:'reduce'});await context.setOffline(true);const page=await context.newPage();
const failures=[],observations=[],errors=[];page.on('pageerror',e=>errors.push(e.message));
function assert(ok,message){if(!ok)throw new Error(message);}
function fileFor(key){const [lang,...parts]=key.split('/'),rel=parts.join('/');return join(root,lang,rel.endsWith('index.md')?rel.replace(/index\.md$/,'index.html'):rel.replace(/\.md$/,'/index.html'));}
async function audit(label){const result=await page.evaluate(()=>{
 const issues=[],units=[...document.querySelectorAll('.study-unit')],normalize=s=>s.replace(/\s+/g,' ').trim();
 if(document.querySelector('.app-shell')?.dataset.viewMode!=='study')issues.push('not study mode');
 if(document.querySelector('[data-layout-status="pending"]'))issues.push('pending source content');
 const visible=e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>1&&r.height>1&&s.display!=='none'&&s.visibility!=='hidden';};
 for(const e of [document.documentElement,document.body,...document.querySelectorAll('.app-shell *')]){
  if(!visible(e)||e.closest('.measure,.assistive-navigation'))continue;
  const r=e.getBoundingClientRect(),s=getComputedStyle(e),label=`${e.tagName}.${e.className}`.slice(0,90);
  if(r.left < -2||r.right>innerWidth+2||e.scrollWidth>e.clientWidth+2)issues.push(`${label}: horizontal overflow`);
  if(![document.documentElement,document.body].includes(e)&&e.scrollHeight>e.clientHeight+2)issues.push(`${label}: nested vertical overflow (${s.overflowY})`);
 }
 for(const unit of units){
  if(/정적 원문 표기입니다|Static source notation\./.test(unit.textContent))issues.push(`obsolete notation notice ${unit.dataset.unitId}`);
  const source=window.__HANDBOOK_SLIDES__.slides.find(s=>(s.unit_id||s.id)===unit.dataset.unitId);
  if(!source){issues.push('unit absent from schema');continue;}
  const html=source.content_blocks?.length?source.content_blocks.map(b=>typeof b==='string'?b:b.html||'').join(''):source.body_html;
  const parsed=new DOMParser().parseFromString(html||'','text/html');const expected=normalize(parsed.body.textContent),actual=normalize(unit.textContent);
  const sourceWalker=parsed.createTreeWalker(parsed.body,NodeFilter.SHOW_TEXT);while(sourceWalker.nextNode()){const chunk=normalize(sourceWalker.currentNode.textContent);if(chunk&&!actual.includes(chunk))issues.push(`missing source text ${unit.dataset.unitId}: ${chunk.slice(0,50)}`);}
  const walker=document.createTreeWalker(unit,NodeFilter.SHOW_TEXT);while(walker.nextNode()){
   const n=walker.currentNode,p=n.parentElement;if(!n.textContent.trim()||!visible(p))continue;const range=document.createRange();range.selectNodeContents(n);
   if(parseFloat(getComputedStyle(p).fontSize)<14)issues.push(`small font ${getComputedStyle(p).fontSize}`);
   for(const r of range.getClientRects())if(r.left < -2||r.right>innerWidth+2)issues.push(`text horizontal overflow ${n.textContent.slice(0,40)}`);
   for(let a=p;a&&a!==document.body;a=a.parentElement){const s=getComputedStyle(a);if(/hidden|clip/.test(s.overflow+s.overflowX+s.overflowY)){const b=a.getBoundingClientRect();for(const r of range.getClientRects())if(r.left<b.left-2||r.right>b.right+2||r.top<b.top-2||r.bottom>b.bottom+2)issues.push(`clipped text ${n.textContent.slice(0,40)}`);}}
  }
 }
 return {issues:[...new Set(issues)],units:units.map(u=>u.dataset.unitId),pageHeight:document.documentElement.scrollHeight};
});observations.push({label,...result});if(result.issues.length){failures.push({label,issues:result.issues});if(failures.length<=20)console.log(`Study audit ${label}: ${result.issues.slice(0,2).join('; ')}`);}return result;}
try{
 const keys=process.env.SLIDES_STUDY_SAMPLE?Object.keys(manifest).filter(k=>/flink\.md|networking\.md|qlora-training\.md|vocabulary\.md|foundations\.md|production-operations\.md/.test(k)):Object.keys(manifest);
 for(const width of [320,1280]){
  await page.setViewportSize({width,height:width===320?568:720});let sections=0;
  for(const key of keys){
   await page.goto(pathToFileURL(fileFor(key)).href);await page.locator('.study-unit').first().waitFor();
   assert(await page.locator('.app-shell').getAttribute('data-view-mode')==='study',`default mode ${key}`);
   const groups=await page.evaluate(()=>[...new Map(window.__HANDBOOK_SLIDES__.slides.map(s=>[s.section_id,{section:s.section_id,unit:s.unit_id||s.id}])).values()]);
   const expected=await page.evaluate(()=>window.__HANDBOOK_SLIDES__.slides.map(s=>s.unit_id||s.id));const seen=new Set();
   for(const group of groups){await page.evaluate(g=>location.hash=new URLSearchParams({mode:'study',...g}).toString(),group);await page.waitForFunction(s=>document.querySelector('.slide-card')?.dataset.sectionId===s,group.section);const result=await audit(`${key} ${width} ${group.section}`);result.units.forEach(u=>seen.add(u));sections++;}
   assert(expected.every(id=>seen.has(id)),`unvisited source units ${key}`);
   if((keys.indexOf(key)+1)%25===0)console.log(`Study sweep progress ${width}px: ${keys.indexOf(key)+1}/${keys.length} decks, ${sections} sections`);
  }
  console.log(`Study source sweep: ${keys.length} decks, ${sections} sections at ${width}px`);
 }
 for(const [width,height] of [[320,568],[390,844],[768,1024],[1280,720],[844,390]])for(const lang of ['ko','en']){
  await page.setViewportSize({width,height});
  for(const [path,section,unit] of [['data-platform/flink','watermark','watermark:timeline'],['aws-cloud/networking','sg-nacl','sg-nacl:comparison'],['data-platform/production-operations','schema-break','schema-break:change'],['english-study/vocabulary','vocab-check','vocab-check:meaning-usage'],['prompts/flink','flink-01','flink-01:purpose-input-output'],['ai-model-development/qlora-training','qlora-flow','qlora-flow:prepare']]){
   await page.goto(pathToFileURL(fileFor(`${lang}/${path}.md`)).href+'#'+new URLSearchParams({mode:'study',section,unit}));await page.locator('.study-unit').first().waitFor();await audit(`${lang}/${path} reviewed ${width}x${height}`);await page.screenshot({path:join(evidence,`${section}-${lang}-${width}x${height}.png`),fullPage:true});
  }
  await page.goto(pathToFileURL(fileFor(`${lang}/data-platform/foundations.md`)).href);await page.locator('.study-unit').first().waitFor();const parameter=await page.evaluate(()=>{const s=window.__HANDBOOK_SLIDES__.slides.find(s=>s.interaction?.type==='parameter');return {unit:s.unit_id||s.id,section:s.section_id};});await page.evaluate(p=>location.hash=new URLSearchParams({mode:'study',...p}).toString(),parameter);const number=page.locator('input[type="number"]');await number.waitFor();
  for(const [input,result] of [['300','may-match'],['500','can-skip'],['1000','can-skip']]){await number.fill(input);await page.locator(`.parameter-result.${result}`).waitFor();await audit(`Statistics study ${lang} ${width}x${height} ${input}`);if(input==='300'&&[390,1280].includes(width))await page.screenshot({path:join(evidence,`statistics-study-${lang}-${width}x${height}.png`),fullPage:true});if(width===320&&input==='300'){const parameterAX=await page.locator('.parameter').ariaSnapshot();assert(/slider/.test(parameterAX)&&/spinbutton/.test(parameterAX)&&/status/.test(parameterAX),'parameter accessible roles missing');await writeFile(join(evidence,`aria-statistics-${lang}.txt`),parameterAX);}}await page.getByRole('button',{name:/^(초기화|Reset)$/}).click();assert(await number.inputValue()==='1000','study reset expected1000');
 }
 for(const lang of ['ko','en']){
  await page.setViewportSize({width:320,height:568});await page.goto(pathToFileURL(fileFor(`${lang}/data-platform/flink.md`)).href+'#mode=study&section=watermark&unit=watermark:timeline');await page.locator('.study-unit').first().waitFor();await page.addStyleTag({content:'.study-unit .rich-text {font-size:200% !important}'});await page.evaluate(()=>dispatchEvent(new Event('resize')));await page.waitForTimeout(250);await audit(`Study enlarged ${lang} 320`);const unit=new URLSearchParams(new URL(page.url()).hash.slice(1)).get('unit');await page.setViewportSize({width:844,height:390});await page.waitForTimeout(250);await audit(`Study enlarged rotated ${lang}`);assert(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('unit')===unit,'study rotation changed reading unit');await page.screenshot({path:join(evidence,`study-enlarged-rotated-${lang}.png`),fullPage:true});
 }
 await page.setViewportSize({width:390,height:844});await page.goto(pathToFileURL(fileFor('ko/data-platform/flink.md')).href+'#mode=study&unit=watermark:timeline&section=watermark');await page.locator('.study-unit').first().waitFor();await audit('watermark mode baseline');
 const section=await page.locator('.slide-card').getAttribute('data-section-id');
 await page.evaluate(()=>document.activeElement.blur());await page.keyboard.press('ControlOrMeta+Home');await page.evaluate(()=>window.scrollTo(0,0));const top=await page.evaluate(()=>scrollY);await page.keyboard.press('PageDown');await page.waitForTimeout(200);assert(await page.evaluate(()=>scrollY)>top,'study PageDown did not scroll page');assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study PageDown changed section');await page.keyboard.press('Home');await page.waitForTimeout(200);await page.keyboard.press('End');await page.waitForTimeout(200);assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study Home/End changed section');

 const readingUnit=new URLSearchParams(new URL(page.url()).hash.slice(1)).get('unit');
 await page.locator('[data-mode-toggle]').click();await page.waitForFunction(()=>document.querySelector('.app-shell')?.dataset.viewMode==='presentation');assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'mode switch changed section');assert(new URLSearchParams(new URL(page.url()).hash.slice(1)).get('unit')===readingUnit,'mode switch changed reading unit');
 await page.locator('[data-mode-toggle]').click();await page.waitForFunction(()=>document.querySelector('.app-shell')?.dataset.viewMode==='study');assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study return changed section');
 await page.reload();await page.locator('.study-unit').first().waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study reload changed section');
 await page.screenshot({path:join(evidence,'watermark-study-390x844.png'),fullPage:true});
 const alternate=page.locator('.app-footer [data-language-link]');const publicHref=await alternate.getAttribute('href');const path=publicHref.split('#')[0].split('/slides/')[1];await alternate.evaluate((e,href)=>e.href=href,pathToFileURL(join(root,path,'index.html')).href+'#'+publicHref.split('#')[1]);await alternate.click();await page.locator('.study-unit').first().waitFor();assert(await page.locator('.app-shell').getAttribute('data-view-mode')==='study','language switch lost study mode');assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study language section mismatch');await page.goBack();await page.locator('.study-unit').first().waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study Back section mismatch');await page.goForward();await page.locator('.study-unit').first().waitFor();assert(await page.locator('.slide-card').getAttribute('data-section-id')===section,'study Forward section mismatch');await page.goBack();await page.locator('.study-unit').first().waitFor();
 const ax=await page.locator('.app-shell').ariaSnapshot();assert(/button "발표 모드"/.test(ax)&&/heading.*Watermark/.test(ax),'accessible mode/title missing');await writeFile(join(evidence,'aria-watermark.txt'),ax);
 const cdp=await context.newCDPSession(page);const tree=await cdp.send('Accessibility.getFullAXTree');await writeFile(join(evidence,'accessibility-tree.json'),JSON.stringify(tree,null,2));assert(tree.nodes.some(n=>n.role?.value==='button'&&n.name?.value==='발표 모드'),'AX mode button missing');
 assert(!errors.length,errors.join('; '));assert(!failures.length,`${failures.length} study sections failed; see study/audit.json`);
 console.log('Study default/mode/position/source completeness, source sweep and accessibility tree PASS');
}finally{await writeFile(join(evidence,'audit.json'),JSON.stringify({observations,failures,errors,screenReaderScope:'Chromium accessibility tree only; not actual VoiceOver speech'},null,2));await browser.close();}
