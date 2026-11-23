"""Copy validated static site for Cloudflare Pages; optionally produce sitemap.

SITE_URL defaults to the published production URL for Cloudflare deployments.
Set SITE_URL explicitly for other deployments; an empty value omits sitemap/canonical tags.
"""
from pathlib import Path
import os,re,shutil,sys
from html import escape as html_escape
from urllib.parse import urlparse
from xml.sax.saxutils import escape
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'site';DEST=ROOT/'dist'

def main():
    if DEST.exists():shutil.rmtree(DEST)
    shutil.copytree(SRC,DEST)
    # Cloudflare Pages automatically uses clean URLs (/compare instead of /compare.html).
    # All internal URLs, canonicals and sitemap locations must use the same final URL.
    def public_path(p):
        path='/'+p.relative_to(DEST).as_posix()
        return '/' if path=='/index.html' else path[:-5] if path.endswith('.html') else path

    def normalize_internal_links(markup):
        def replace_link(match):
            path=match.group(2)
            clean='/' if path=='/index.html' else path[:-5] if path.endswith('.html') else path
            return match.group(1)+clean+match.group(3)
        return re.sub(r'(href=")(/[^"#?]*?\.html)(["#?])',replace_link,markup)

    urls=[]
    for p in sorted(DEST.rglob('*.html')):
        if p.name=='404.html':continue
        urls.append(public_path(p))
    contact=os.environ.get('CONTACT_URL','').strip()
    if contact:
        ct=urlparse(contact)
        if ct.scheme!='https' or not ct.netloc:
            raise ValueError('CONTACT_URL must be a full https:// URL')
        about=DEST/'about.html'
        contents=about.read_text(encoding='utf-8')
        contents=contents.replace('<p>正式な問い合わせ窓口は公開前に設定します。現在の配布版には連絡先がないため、公開前の最終チェック項目として残しています。</p>',
            f'<p>お問い合わせは <a href="{html_escape(contact,quote=True)}" target="_blank" rel="noopener noreferrer">こちらの窓口</a> からご連絡ください。</p>')
        contents=contents.replace('<div class="notice">正式公開前に運営者の連絡窓口を追加してください。個人情報や事業名は許可なく記載しません。</div>','')
        about.write_text(contents,encoding='utf-8')
    url=os.environ.get('SITE_URL','https://ai-site-erabi.pages.dev').strip().rstrip('/')
    if url:
        parsed=urlparse(url)
        if parsed.scheme!='https' or not parsed.netloc or parsed.path not in ('','/'):
            raise ValueError('SITE_URL must look like https://example.pages.dev')
        for p in DEST.rglob('*.html'):
            if p.name=='404.html':continue
            canonical=url+public_path(p)
            markup=normalize_internal_links(p.read_text(encoding='utf-8'))
            markup=markup.replace('</head>',f'<link rel="canonical" href="{canonical}"></head>')
            p.write_text(markup,encoding='utf-8')
        locs=[url+p for p in urls]
        sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{escape(loc)}</loc></url>\n' for loc in locs)+'</urlset>\n'
        (DEST/'sitemap.xml').write_text(sitemap,encoding='utf-8')
        # Simple alternate sitemap for troubleshooting XML processing in Search Console.
        # URLs stay identical to canonical URLs in the XML sitemap.
        (DEST/'sitemap.txt').write_text(''.join(loc+'\n' for loc in locs),encoding='utf-8')
        (DEST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+url+'/sitemap.xml\nSitemap: '+url+'/sitemap.txt\n',encoding='utf-8')
    else:
        for p in DEST.rglob('*.html'):
            if p.name!='404.html':
                p.write_text(normalize_internal_links(p.read_text(encoding='utf-8')),encoding='utf-8')
        (DEST/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
    print(f'Built {len(urls)} public pages to {DEST}; SITE_URL '+('configured' if url else 'not yet configured'))

if __name__=='__main__':main()
