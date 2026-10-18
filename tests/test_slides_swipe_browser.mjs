import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const evidence=resolve('_workspace/slide-qa/swipe');
await mkdir(evidence,{recursive:true});
const chrome=process.env.CHROME_PATH||(process.platform==='darwin'?'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome':undefined);
const browser=await chromium.launch({headless:true,...(chrome?{executablePath:chrome}:{})});
const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
await context.setOffline(true);
const page=await context.newPage(), cdp=await context.newCDPSession(page), observations=[],errors=[];
page.on('pageerror',e=>errors.push(e.message));
const assert=(value,message)=>{if(!value)throw new Error(message);};
const index=()=>page.locator('.app-footer .footer-row > span').innerText().then(s=>Number(s.split('/')[0]));
async function open(mode,path='data-platform/architecture') {
  await page.goto(pathToFileURL(resolve(`_workspace/handbook-slides/ko/${path}/index.html`)).href+`#mode=${mode}`);
  await page.locator('.slide-card').waitFor();
  await page.waitForFunction(mode=>document.querySelector('.app-shell')?.dataset.viewMode===mode,mode);
  await page.waitForTimeout(300); // Initial resize pagination, before measuring a gesture target.
}
async function touch(type,points) {await cdp.send('Input.dispatchTouchEvent',{type,touchPoints:points.map(([x,y,id=0])=>({x,y,id}))});}
async function swipe(x1,y1,x2,y2,{cancel=false,multi=false,duration=120}={}) {
  const points=(x,y)=>multi?[[x,y,0],[x+5,y+25,1]]:[[x,y,0]];
  await touch('touchStart',points(x1,y1));
  for(let i=1;i<=6;i++) {await page.waitForTimeout(duration/6);await touch('touchMove',points(x1+(x2-x1)*i/6,y1+(y2-y1)*i/6));}
  await touch(cancel?'touchCancel':'touchEnd',[]);
}
async function headingY() {return page.locator('.slide-card h1').evaluate(e=>{const r=e.getBoundingClientRect();return Math.min(innerHeight-100,r.top+r.height/2);});}
async function expectIndex(expected,label) {
  await page.waitForFunction(expected=>Number(document.querySelector('.app-footer .footer-row > span')?.textContent.split('/')[0])===expected,expected,{timeout:2000}).catch(()=>{});
  await page.waitForTimeout(100); // Detect a second synthetic-click navigation after touch end.
  const actual=await index();observations.push({label,expected,actual});assert(actual===expected,`${label}: expected slide ${expected}, got ${actual}`);
}
async function unchanged(label,action) {const before=await index();await action();await expectIndex(before,label);}
try {
  for(const mode of ['study','presentation']) {
    await open(mode);let y=await headingY();
    await swipe(300,y,100,y);await expectIndex(2,`${mode}: real touch left advances exactly one`);
    y=await headingY();await swipe(100,y,300,y);await expectIndex(1,`${mode}: right returns one`);
    y=await headingY();await unchanged(`${mode}: first boundary`,()=>swipe(100,y,300,y));
    await swipe(230,y,170,y);await expectIndex(2,`${mode}: exact 60px threshold`);
    await swipe(170,await headingY(),230,await headingY());await expectIndex(1,`${mode}: threshold returns one`);
    y=await headingY();await unchanged(`${mode}: 59px below threshold`,()=>swipe(230,y,171,y));
    await unchanged(`${mode}: short drag`,()=>swipe(220,y,180,y));
    await unchanged(`${mode}: diagonal drag`,()=>swipe(280,y,180,y+90));
    await unchanged(`${mode}: vertical intent cannot become horizontal navigation`,async()=>{await touch('touchStart',[[280,y]]);await touch('touchMove',[[278,y+20]]);await touch('touchMove',[[100,y+25]]);await touch('touchEnd',[]);});
    await unchanged(`${mode}: slow drag`,()=>swipe(300,y,100,y,{duration:1100}));
    await unchanged(`${mode}: cancelled touch`,()=>swipe(300,y,100,y,{cancel:true}));
    await unchanged(`${mode}: two fingers`,()=>swipe(290,y,90,y,{multi:true}));
    await page.evaluate(()=>{const r=document.createRange();r.selectNodeContents(document.querySelector('.slide-card h1'));getSelection().removeAllRanges();getSelection().addRange(r);});
    await unchanged(`${mode}: selected text`,()=>swipe(300,y,100,y));
    await page.evaluate(()=>getSelection().removeAllRanges());
    await unchanged(`${mode}: mouse drag`,async()=>{await page.mouse.move(300,y);await page.mouse.down();await page.mouse.move(100,y,{steps:8});await page.mouse.up();});
    await page.evaluate(()=>getSelection().removeAllRanges());
    // Controlled semantic targets isolate exclusions from any particular document's layout.
    for(const markup of ['<a href="#ignored">link</a>','<button>control</button>','<input type="number" value="300">','<input type="range">','<select><option>option</option></select>','<textarea>text</textarea>','<svg><rect width="100%" height="100%" /></svg>','<pre>code sample</pre>','<code>inline code</code>','<table><tbody><tr><td>table cell</td></tr></tbody></table>','<div class="interaction">diagram</div>','<div contenteditable="true">editable</div>']) {
      const tag=markup.match(/^<([^ >]+)/)[1];
      await page.evaluate(markup=>{const host=document.createElement('div');host.id='swipe-exclusion-fixture';host.style.cssText='position:fixed;left:70px;top:300px;width:250px;height:80px;z-index:20';host.innerHTML=markup;const target=host.firstElementChild;target.style.cssText='display:block;width:250px;height:80px;margin:0';target.addEventListener('click',e=>e.preventDefault());document.querySelector('.slide-card').append(host);},markup);
      await unchanged(`${mode}: ${tag} start excluded`,()=>swipe(280,330,90,330));
      await page.locator('#swipe-exclusion-fixture').evaluate(e=>{e.style.left='40px';e.style.width='100px';e.firstElementChild.style.width='100px';});
      await unchanged(`${mode}: ${tag} end excluded`,()=>swipe(300,330,90,330));
      await page.locator('#swipe-exclusion-fixture').evaluate(e=>e.remove());
    }
    await page.evaluate(()=>document.activeElement.blur());
    if(mode==='presentation')await page.keyboard.press('End');
    else {await page.evaluate(()=>{const units=window.__HANDBOOK_SLIDES__.slides,last=units.at(-1);location.hash=new URLSearchParams({mode:'study',section:last.section_id,unit:last.unit_id||last.id}).toString();});}
    await page.waitForTimeout(300);
    assert(await page.locator('.app-footer .footer-row > span').evaluate(e=>{const [a,b]=e.textContent.split('/').map(Number);return a===b;}),`${mode}: test did not reach last slide`);
    y=await headingY();await unchanged(`${mode}: last boundary`,()=>swipe(300,y,100,y));
  }
  await open('study','data-platform/flink');
  await page.evaluate(()=>location.hash=new URLSearchParams({mode:'study',section:'watermark'}).toString());
  await page.waitForFunction(()=>document.querySelector('.slide-card')?.dataset.sectionId==='watermark');
  await page.evaluate(()=>scrollTo(0,0));
  const initialScroll=await page.evaluate(()=>scrollY);
  await unchanged('study: vertical touch keeps section',()=>swipe(200,650,200,300));
  const actualScroll=await page.evaluate(()=>scrollY);assert(actualScroll>initialScroll+20,'study: native vertical touch did not scroll');
  observations.push({label:'study: native vertical scrolling',expected:'increase >20px',actual:actualScroll-initialScroll});
  assert(!errors.length,errors.join('\n'));
  console.log(`Mobile swipe: ${observations.length} checks PASS`);
} catch(error) {errors.push(error.message);console.error(error.message);process.exitCode=1;}
finally {await writeFile(resolve(evidence,'audit.json'),JSON.stringify({observations,errors},null,2));await browser.close();}
