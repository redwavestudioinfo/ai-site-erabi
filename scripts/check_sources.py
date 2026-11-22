"""Audit official source pages; record changes, never alter editorial claims.

Standard library only. Errors and blocked fetches are recorded as 'unavailable',
not misrepresented as verified changes. Called weekly from GitHub Actions.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
MAX_BYTES=500_000

class MainTextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ignored=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','svg','noscript'):self.ignored+=1
    def handle_endtag(self,tag):
        if tag in ('script','style','svg','noscript') and self.ignored:self.ignored-=1
    def handle_data(self,data):
        if not self.ignored and data.strip():self.parts.append(data)

def text_fingerprint(raw:bytes)->str:
    parser=MainTextParser();parser.feed(raw.decode('utf-8','replace'))
    content=' '.join(parser.parts)
    normalized=re.sub(r'\s+',' ',content).strip()
    return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

def audit(sources,old_state,reader):
    report={};changes=[]
    timestamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
    for source in sources:
        sid=source['id'];prior=old_state.get(sid,{})
        try:
            raw,status=reader(source['url'])
            digest=text_fingerprint(raw)
            prev=prior.get('sha256')
            change='changed' if prev and prev!=digest else ('baseline' if not prev else 'unchanged')
            report[sid]={'url':source['url'],'checked_at':timestamp,'http_status':status,'state':change,'sha256':digest}
            if change=='changed':changes.append({'id':sid,'title':source['title'],'url':source['url']})
        except Exception as e:
            report[sid]={'url':source['url'],'checked_at':timestamp,'state':'unavailable','error':str(e)[:180]}
    return report,changes

def live_reader(url):
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; AISiteErabiSourceCheck/1.0; manual-review-only)'})
    with urllib.request.urlopen(req,timeout=17) as response:
        return response.read(MAX_BYTES),response.status

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--fixture-dir',type=Path);args=parser.parse_args()
    sources=json.loads((DATA/'sources.json').read_text(encoding='utf-8'))
    state_path=DATA/'source-state.json'
    old=json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    if args.fixture_dir:
        def reader(url):
            slug=next(s['id'] for s in sources if s['url']==url)
            return (args.fixture_dir/(slug+'.html')).read_bytes(),200
    else:reader=live_reader
    report,changes=audit(sources,old,reader)
    state_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# Official source check','',f'Last run: {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}', '',
           f'Changes requiring manual review: {len(changes)}', '',
           '| Source | Status |','|---|---|']
    for src in sources:
        res=report[src['id']]; lines.append(f'| [{src["title"]}]({src["url"]}) | {res["state"]} |')
    lines+=['','Changes do not automatically overwrite product claims or publish new articles.','']
    (DATA/'last-check.md').write_text('\n'.join(lines),encoding='utf-8')
    for c in changes:print('REVIEW REQUIRED:',c['id'],c['url'])
    for sid,item in report.items():
        if item['state']=='unavailable':print('SOURCE UNAVAILABLE:',sid,item.get('error',''))
    print(f'Audited {len(report)} sources; {len(changes)} content changes; '+str(sum(v['state']=='unavailable' for v in report.values()))+' unavailable')

if __name__=='__main__':main()
