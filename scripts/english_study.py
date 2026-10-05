"""Count handbook prose and render reviewed bilingual English study entries."""
from __future__ import annotations
import argparse
from collections import Counter
import datetime as dt
import hashlib
import html
import json
from pathlib import Path
import re
import markdown
from bs4 import BeautifulSoup, Comment

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'vocabulary': ('한영 실무 어휘 사전', 'Practical bilingual vocabulary'),
    'idioms': ('숙어·관용 표현·연어', 'Idioms, expressions, and collocations'),
    'phrasal-verbs': ('업무에서 쓰는 구동사', 'Phrasal verbs at work'),
    'workplace': ('면접·회사에서 쓰는 문장', 'Interview and workplace expressions'),
}
TOKEN = re.compile(r"[a-z0-9_]+(?:['-][a-z0-9_]+)*")
FIELDS = ('id','category','term','meaning_ko','usage_ko','usage_en','example_en','example_ko','register')
STOP = set('a an the and or to of in on for with is are was were be been being this that these those it its as by from at not no can may must will should do does did has have had i we you they he she our your their then than if so only also'.split())
BLOCKS = ('p','li','td','th','h1','h2','h3','h4','h5','h6','blockquote','div')


def tokens(text):
    return TOKEN.findall(text.lower().replace('’', "'"))


def prose_blocks(text):
    text = re.sub(r'\A---\s*\n.*?\n---\s*(?:\n|$)', '', text, count=1, flags=re.S)
    rendered = markdown.markdown(text, extensions=['tables','pymdownx.superfences','admonition','pymdownx.tabbed','attr_list'])
    soup = BeautifulSoup(rendered, 'html.parser')
    for node in soup.find_all(string=lambda x:isinstance(x,Comment)): node.extract()
    for node in soup.select('pre, code, script, style'): node.replace_with('\0')
    grouped = []
    previous = None
    for node in soup.find_all(string=True):
        parent = node.find_parent(BLOCKS)
        key = id(parent) if parent else id(node)
        if key != previous:
            grouped.append([])
            previous = key
        grouped[-1].append(str(node))
    blocks=[]
    for parts in grouped:
        text=re.sub(r'https?://\S+|www\.\S+', '\0', ''.join(parts))
        for line in text.split('\0'):
            block=tokens(line)
            if block: blocks.append(block)
    return blocks


def corpus(root):
    root=Path(root); hashes={}; blocks={}
    for path in sorted((root/'docs/en').rglob('*.md')):
        relative=path.relative_to(root/'docs/en').as_posix()
        if relative.startswith('english-study/'): continue
        raw=path.read_bytes(); hashes[relative]=hashlib.sha256(raw).hexdigest()
        blocks[relative]=prose_blocks(raw.decode())
    return {'hashes':hashes,'blocks':blocks}


def load_entries(root):
    data=json.loads((Path(root)/'learning/english-entries.json').read_text())
    if not isinstance(data,dict) or not isinstance(data.get('entries'),list): raise ValueError('entries must be a list')
    seen=set(); terms=set()
    for row in data['entries']:
        if not isinstance(row,dict): raise ValueError('entry must be an object')
        for key in FIELDS:
            value=row.get(key)
            if not isinstance(value,str) or not value.strip() or '\n' in value or '\r' in value:
                raise ValueError(f'invalid entry field: {key}')
        if not re.fullmatch(r'[a-z][a-z0-9-]*',row['id']) or row['id'] in seen: raise ValueError('invalid or duplicate entry id')
        seen.add(row['id'])
        term=(row['category'],row['term'].casefold())
        if term in terms: raise ValueError('duplicate category term')
        terms.add(term)
        if row['category'] not in CATEGORIES or row['register'] not in ('neutral','informal','formal'): raise ValueError('invalid category or register')
        forms=row.get('forms')
        if not isinstance(forms,list) or not forms or not all(isinstance(x,str) and x.strip() and '\n' not in x and '\r' not in x and tokens(x) for x in forms): raise ValueError('invalid forms')
        normalized=[' '.join(tokens(x)) for x in forms]
        if len(set(normalized))!=len(forms): raise ValueError('duplicate normalized forms')
        sources=row.get('sources',[])
        if not isinstance(sources,list) or not all(isinstance(s,str) and re.fullmatch(r'https://[^\s<>\[\](){}\\\"\']+',s) for s in sources): raise ValueError('invalid reference URLs')
    return data['entries']


def rank(data, entries):
    texts={path:[' '.join(block) for block in blocks] for path,blocks in data['blocks'].items()}
    result=[]
    for row in entries:
        forms=sorted({' '.join(tokens(x)) for x in row['forms']},key=lambda x:(-len(x),x))
        pattern=re.compile(r'(?<![a-z0-9_\'-])(?:'+'|'.join(re.escape(x) for x in forms)+r')(?![a-z0-9_\'-])')
        hits={path:sum(len(pattern.findall(block)) for block in blocks) for path,blocks in texts.items()}
        result.append({**row,'count':sum(hits.values()),'documents':sum(bool(n) for n in hits.values()),'sources_in_corpus':sorted(path for path,n in hits.items() if n)})
        result[-1]['sources']=result[-1].pop('sources_in_corpus')
        result[-1]['references']=row.get('sources',[])
    return sorted(result,key=lambda x:(-x['count'],x['term'].casefold(),x['id']))


def candidates(data, limit=100):
    words=Counter(); phrases=Counter()
    for blocks in data['blocks'].values():
        for block in blocks:
            words.update(x for x in block if x not in STOP and len(x)>2 and re.fullmatch(r"[a-z]+(?:['-][a-z]+)*",x))
            for size in (2,3,4):
                phrases.update(' '.join(block[i:i+size]) for i in range(len(block)-size+1) if any(x not in STOP for x in block[i:i+size]))
    def top(counts):return [{'term':term,'count':count} for term,count in sorted(counts.items(),key=lambda x:(-x[1],x[0]))[:limit]]
    return {'documents':len(data['hashes']),'words':top(words),'phrases':top(phrases)}


def escape(text):
    text=html.escape(text,quote=False)
    return re.sub(r'([\\`*_[\]{}|])',r'\\\1',text)


def front(slug,date):
    return f'---\nid: english-study-{slug}\nstatus: studied\nlast_updated: {date}\nlast_reviewed: {date}\nknowledge_ids: []\n---\n\n'


def intro(lang, docs):
    if lang=='ko':
        return f'집계 대상은 영어 본문 **{docs}개 문서**다. 코드·메타데이터·URL·이 영어 학습 영역은 제외한다. 활용형은 각 항목에 명시한 형태만 합산한다. **이 핸드북 안의 출현 횟수**이며 일반 영어·구어체의 빈도 순위가 아니다. 같은 분류 안에서 횟수 내림차순, 동률은 영문 표제어순이다. 철자 기준 집계이므로 동형어의 뜻·품사를 자동 구분하지 않으며, 떨어진 목적어를 포함한 구동사는 명시된 형태만 센다.\n\n예문은 중급 기술 설명·업무·면접 연습을 위해 새로 작성했다. 원문 인용이나 실제 업무 경험이 아니다. **0회 표현은 별도 보충 자료**이며 원문에 나온 것으로 간주하지 않는다.\n\n'
    return f'The corpus contains **{docs} English document{"" if docs == 1 else "s"}**. Counts exclude code, metadata, URLs, and this English study section. Only the listed forms are combined. These are **occurrences in this handbook**, not frequency rankings for general or spoken English. Each category is sorted by count, then alphabetically for ties. Counts match written forms without distinguishing senses or parts of speech. Separated phrasal verbs count only when that form is listed.\n\nExamples are newly written for intermediate technical, workplace, and interview practice. They are not source quotations or claims of work experience. **Zero-count expressions are separate supplements**, not expressions found in the corpus.\n\n'


def lead(lang, docs):
    if lang=='ko':
        return f'영어 본문 **{docs}개 문서의 빈도순**으로 학습한다. 새로 작성한 한영 예문으로 중급 기술 설명·업무 대화를 연습하자. **0회 표현은 보충 자료**다. [집계 기준](index.md#counting-method)\n\n'
    return f'Start with the most frequent expressions across **{docs} handbook pages**. Practice with newly written bilingual examples for intermediate workplace English. **Zero-count items are supplements.** [How counts work](index.md#counting-method)\n\n'


def build(root, updated=None):
    root=Path(root); data=corpus(root); entries=load_entries(root); rows=rank(data,entries)
    report_path=root/'reviews/english-frequency.json'
    if updated is None and report_path.exists():
        try: updated=json.loads(report_path.read_text()).get('updated')
        except (ValueError,AttributeError): pass
    updated=updated or dt.date.today().isoformat();dt.date.fromisoformat(updated)
    report={'updated':updated,'scope':'docs/en/**/*.md except english-study; prose only; listed forms; case insensitive','corpus':data['hashes'],'entries_sha256':hashlib.sha256((root/'learning/english-entries.json').read_bytes()).hexdigest(),'counts':[{key:row[key] for key in ('id','category','term','count','documents','sources')} for row in rows]}
    outputs={'reviews/english-frequency.json':json.dumps(report,ensure_ascii=False,indent=2)+'\n'}
    for lang in ('ko','en'):
        ko=lang=='ko'; idx=0 if ko else 1
        index=front('index',updated)+'# '+('실전 영어 학습' if ko else 'Practical English study')+'\n\n'+lead(lang,len(data['hashes']))
        index+=('## 학습 순서\n\n각 페이지의 상위 빈도부터 읽고, 예문을 소리 내어 말한 뒤 본인의 상황에 맞게 바꾼다. 면접에서는 실제로 한 일과 가정한 설계를 분명히 구분한다.\n\n' if ko else '## How to study\n\nStart with the highest counts on each page. Say each example aloud, then adapt it to your situation. In interviews, distinguish your real work from a hypothetical design.\n\n')
        for category,titles in CATEGORIES.items():
            selected=[r for r in rows if r['category']==category]
            index+=f'- [{titles[idx]}]({category}.md): {len(selected)}'+('개\n' if ko else (' entry\n' if len(selected)==1 else ' entries\n'))
            body=front(category,updated)+f'# {titles[idx]}\n\n'+lead(lang,len(data['hashes']))
            if not selected:body+=('검토한 항목이 아직 없다.\n' if ko else 'No reviewed entries yet.\n')
            for zero in (False,True):
                group=[r for r in selected if (r['count']==0)==zero]
                if not group:continue
                title=(('보충 표현 — 원문 출현 0회' if ko else 'Supplement — zero corpus occurrences') if zero else ('문서에 나온 표현 — 빈도순' if ko else 'Expressions in the corpus — by frequency'))
                body+=f'## {title}\n\n'
                for row in group:
                    label={'neutral':('중립','neutral'),'informal':('구어·비격식','informal'),'formal':('격식','formal')}[row['register']][idx]
                    body+=f"### {escape(row['term'])} {{#{row['id']}}}\n\n"
                    body+=f"**{row['count']}"+('회 · ' if ko else (' occurrence · ' if row['count']==1 else ' occurrences · '))+str(row['documents'])+('개 문서 · ' if ko else (' document · ' if row['documents']==1 else ' documents · '))+label+'**\n\n'
                    body+=f"**{escape(row['meaning_ko'])}**\n\n{escape(row['usage_ko' if ko else 'usage_en'])}\n\n"
                    body+=f"> {escape(row['example_en'])}\n>\n> {escape(row['example_ko'])}\n\n"
                    body+=('집계한 형태: ' if ko else 'Counted forms: ')+', '.join(escape(x) for x in row['forms'])+'.\n\n'
                    if row['sources']:
                        body+=('본문 예: ' if ko else 'Example source pages: ')+', '.join(f'[{escape(p.removesuffix(".md"))}](../{p})' for p in row['sources'][:3])+'.\n\n'
                    if row['references']:
                        body+=('용법 참고: ' if ko else 'Usage references: ')+', '.join(f'[{n+1}]({u})' for n,u in enumerate(row['references']))+'.\n\n'
            outputs[f'docs/{lang}/english-study/{category}.md']=body.rstrip('\n')+'\n'
        index+='\n## '+('집계 기준' if ko else 'How counts work')+' {#counting-method}\n\n'+intro(lang,len(data['hashes']))
        index+=('## 문서가 추가될 때\n\n새 영어 본문의 빈도를 먼저 확인한 뒤 어휘와 표현을 선별·보완한다. 기존 항목도 새 횟수로 다시 정렬한다. 구어체 보충 표현은 0회 구역에 유지하며, 예문의 뜻·자연스러움·격식을 다시 검토한다.\n\n[기술 용어집](../glossary/index.md)은 개념 정의, 이 영역은 단어와 문장을 실제로 쓰는 연습에 초점을 둔다.\n' if ko else '## When documents are added\n\nReview frequency candidates from the new English content before selecting or updating entries. Existing entries are ranked again using current counts. Spoken supplements stay in the zero-count section until they appear in the corpus. Review meaning, naturalness, and register again.\n\nThe [technical glossary](../glossary/index.md) explains concepts; this section practices using words and sentences.\n')
        outputs[f'docs/{lang}/english-study/index.md']=index
    return outputs


def run(root,write=False):
    root=Path(root)
    try: outputs=build(root,updated=dt.date.today().isoformat() if write else None)
    except (OSError,ValueError,TypeError,KeyError) as exc:return [f'English study input error: {exc}']
    errors=[]
    for name in outputs:
        path=root/name
        if any(p.is_symlink() for p in (path,*path.parents) if p!=root and p.is_relative_to(root)):
            errors.append(f'English study destination is a symlink: {name}')
    if errors:return errors
    for name,expected in outputs.items():
        path=root/name
        if write:
            path.parent.mkdir(parents=True,exist_ok=True);path.write_text(expected)
        elif not path.is_file() or path.read_text()!=expected:errors.append(f'English study stale or missing: {name}')
    return errors


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=ROOT)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--write',action='store_true');mode.add_argument('--check',action='store_true');mode.add_argument('--candidates',action='store_true')
    args=parser.parse_args()
    if args.candidates:print(json.dumps(candidates(corpus(args.root)),ensure_ascii=False,indent=2));return 0
    errors=run(args.root,args.write)
    for error in errors:print(error)
    print(f'English study: {len(errors)} errors');return int(bool(errors))


if __name__=='__main__':raise SystemExit(main())
