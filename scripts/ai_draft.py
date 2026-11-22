"""Optional FREE-tier Gemini drafting from approved editorial briefs.

Produces DRAFTS only, NEVER pushes to public site. No key -> safe skip.
Disable billing on your AI API project to maintain a true 0-yen budget.
No search grounding, tools, caching, or paid add-ons are requested.
"""
import json,os,sys,urllib.request,urllib.error
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
KEY=os.environ.get('GEMINI_API_KEY')
MODEL=os.environ.get('GEMINI_MODEL','gemini-3.5-flash-lite')

def main():
    if not KEY:
        print('GEMINI_API_KEY missing. Safe skip, no billable API call.');return 0
    topics=json.loads((ROOT/'data/editorial-topics.json').read_text(encoding='utf-8'))
    sources={s['id']:s for s in json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))}
    pending=[t for t in topics if t.get('status')=='draft_requested']
    if not pending:
        print('No editorial requests.');return 0
    topic=pending[0] # hard limit: 1 draft per run
    refs=[sources[sid] for sid in topic['source_ids']]
    instructions='''You are writing a Japanese editorial DRAFT for a small factual comparison site.
STRICT RULES:
- Treat all source titles as places to verify, NOT as evidence of specific facts.
- Do not browse or claim to have accessed any linked page.
- Do not invent prices, review ratings, test experiences, quotes, dates, or legal claims.
- For product-specific facts you cannot independently verify, write [要検証: ...].
- Put [広告・PR] nowhere: the draft contains NO affiliate links.
- Explain meaningful limitations, cancellation/renewal checks and free vs trial differences.
- End with an editorial fact-check checklist and the official source URLs.
- This is a draft for human review; never imply it is ready for automatic publication.
'''
    prompt=instructions+'\nTOPIC: '+topic['title']+'\nINTENT: '+topic['query_intent']+'\nOFFICIAL SOURCE URLs TO CHECK:\n'+ '\n'.join(s['title']+' '+s['url'] for s in refs)
    request={'contents':[{'parts':[{'text':prompt}]}], 'generationConfig':{'temperature':0.15,'maxOutputTokens':2000}}
    endpoint=f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent'
    req=urllib.request.Request(endpoint,data=json.dumps(request).encode('utf-8'),headers={'Content-Type':'application/json','x-goog-api-key':KEY},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=45) as resp:body=json.load(resp)
    except urllib.error.HTTPError as e:
        print('Draft generation failed with HTTP',e.code,': free tier might be unavailable or quota exhausted. No retry.',file=sys.stderr);return 0
    except Exception as e:
        print('Draft generation failed safely:',type(e).__name__,file=sys.stderr);return 0
    candidates=body.get('candidates',[])
    parts=(candidates[0].get('content') or {}).get('parts',[]) if candidates else []
    draft='\n'.join(x.get('text','') for x in parts).strip()
    if not draft:print('No draft text returned; safe skip');return 0
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d')
    out=ROOT/'drafts'/f'{stamp}_{topic["id"]}.md'
    out.write_text('# DRAFT / REQUIRES FACT CHECK\n\n'+draft+'\n',encoding='utf-8')
    print('Created local draft:',out.name)
    return 0

if __name__=='__main__':raise SystemExit(main())
