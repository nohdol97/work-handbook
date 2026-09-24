import fs from 'node:fs';
import path from 'node:path';
import { JSDOM } from 'jsdom';
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
globalThis.window = dom.window;
globalThis.document = dom.window.document;
const { default: mermaid } = await import('mermaid');
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });
function* files(dir) {
  for (const entry of fs.readdirSync(dir, {withFileTypes: true})) {
    const name = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* files(name);
    else if (entry.isFile() && name.endsWith('.md')) yield name;
  }
}
let count = 0;
let failures = 0;
for (const file of process.argv.slice(2).length ? process.argv.slice(2) : [...files('docs/ko'), ...files('docs/en')]) {
  for (const match of fs.readFileSync(file, 'utf8').matchAll(/^```mermaid\s*\n([\s\S]*?)^```\s*$/gm)) {
    try { await mermaid.parse(match[1]); count++; }
    catch { console.error(`Invalid Mermaid: ${file}`); failures++; }
  }
}
console.log(`Mermaid: ${count} valid, ${failures} invalid`);
process.exitCode = failures ? 1 : 0;
