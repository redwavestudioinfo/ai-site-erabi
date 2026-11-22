from pathlib import Path
import importlib.util,json,re,sys,unittest
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class Links(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.titles=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='a':self.links.append(attrs.get('href',''))
        if tag=='title':self.titles+=1
class ProjectTest(unittest.TestCase):
    def test_all_local_links_exist(self):
        pages=list((ROOT/'site').rglob('*.html'))
        self.assertGreaterEqual(len(pages),6)
        for page in pages:
            with self.subTest(page=page.name):
                html=page.read_text(encoding='utf-8');p=Links();p.feed(html)
                self.assertEqual(p.titles,1)
                for link in p.links:
                    if link.startswith('/') and not link.startswith('//'):
                        target=ROOT/'site'/link.lstrip('/').split('#')[0]
                        if link=='/':target=ROOT/'site'/'index.html'
                        self.assertTrue(target.exists(),f'Broken local link: {page.name} -> {link}')
    def test_ad_links_are_not_fabricated(self):
        for page in (ROOT/'site').rglob('*.html'):
            content=page.read_text(encoding='utf-8')
            self.assertNotIn('pub.a8.net/',content,'Do not invent affiliate tracking links')

    def test_approved_affiliate_link_disclosed(self):
        approved_link='https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E'
        approved_pixel='https://www19.a8.net/0.gif?a8mat=4BGR8X+DJM182+348+4SNX5E'
        for path in ('index.html','compare.html'):
            page=(ROOT/'site'/path).read_text(encoding='utf-8')
            self.assertEqual(page.count(approved_link),1)
            self.assertEqual(page.count(approved_pixel),1)
            self.assertIn('PR・広告',page)
            self.assertIn('rel="nofollow"',page)
    def test_v3_home_editorial_navigation_and_seo(self):
        html=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        for required in ('id="comparison"','id="services"','id="chooser"','id="articles"',
                         'id="purpose"','id="budget"','id="picker-result"',
                         '「無料で作れる」','PR・広告'):
            with self.subTest(required=required):
                self.assertIn(required,html)
        self.assertIn('google-site-verification',html)
        self.assertIn('gdwm3uodac9SUT8E0ySPk1PbU5tpjHOP52BWKDZ4WbQ',html)
        self.assertEqual(html.count('https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E'),1)
        self.assertNotIn('おすすめ第1位',html)
        self.assertNotIn('QUICK FINDER',html)
        self.assertNotIn('browser-preview',html)

    def test_v3_comparison_and_local_assets(self):
        html=(ROOT/'site'/'compare.html').read_text(encoding='utf-8')
        self.assertIn('class="compare-highlights"',html)
        css=(ROOT/'site'/'assets'/'styles.css').read_text(encoding='utf-8')
        js=(ROOT/'site'/'assets'/'app.js').read_text(encoding='utf-8')
        for token in ('.cover-layout','.feature-table','.service-story','.chooser-paper',
                      '.compare-highlights','@media','--serif'):
            self.assertIn(token,css)
        self.assertNotIn('hero-v2',css)
        self.assertIn('purpose.addEventListener',js)
        self.assertIn('budget.addEventListener',js)

    def test_renderer_keeps_v3_and_tracking(self):
        source=(ROOT/'scripts'/'render_pages.py').read_text(encoding='utf-8')
        html_source=(ROOT/'data'/'home-v3.html').read_text(encoding='utf-8')
        self.assertIn("home-v3.html",source)
        self.assertIn('class="cover"',html_source)
        self.assertIn('class="compare-sheet"',html_source)
        self.assertIn('https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E',html_source)
        self.assertIn('PR・広告',html_source)

    def test_content_guides_and_official_examples(self):
        home=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        compare=(ROOT/'site'/'compare.html').read_text(encoding='utf-8')
        body=(ROOT/'data'/'home-v3.html').read_text(encoding='utf-8')
        for path in ('domain-renewal.html','edit-after-publish.html'):
            p=ROOT/'site'/'articles'/path
            self.assertTrue(p.exists(),f'Unpublished guide: {path}')
            html=p.read_text(encoding='utf-8')
            self.assertIn('参照した公式情報',html)
            self.assertIn('/compare.html',html)
            self.assertIn('2026年11月22日',html)
            self.assertIn('/articles/'+path,home)
            self.assertIn('/articles/'+path,compare)
            self.assertIn('/articles/'+path,body)
        self.assertIn('id="examples"',home)
        self.assertIn('https://wild-tooth-7849.lolipop.website/',home)
        self.assertIn('https://ja.wix.com/explore/websites',home)
        self.assertIn('https://portal-jp.jimdo.com/how-to-use-aibuilder01',home)
        approved='https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E'
        pixel='https://www19.a8.net/0.gif?a8mat=4BGR8X+DJM182+348+4SNX5E'
        self.assertEqual(home.count(approved),1)
        self.assertEqual(compare.count(approved),1)
        for path in ('domain-renewal.html','edit-after-publish.html'):
            html=(ROOT/'site'/'articles'/path).read_text(encoding='utf-8')
            self.assertNotIn(approved,html)
            self.assertNotIn(pixel,html)

    def test_guide_source_parity(self):
        renderer=(ROOT/'scripts'/'render_pages.py').read_text(encoding='utf-8')
        topics=json.loads((ROOT/'data'/'editorial-topics.json').read_text(encoding='utf-8'))
        for id,path in [('domain_renewal','domain-renewal.html'),
                        ('ai_editing_workflow','edit-after-publish.html')]:
            topic=next(t for t in topics if t['id']==id)
            self.assertEqual(topic['status'],'published')
            self.assertEqual(topic['page'],'articles/'+path)
            self.assertIn(path,renderer)
            self.assertTrue((ROOT/'data'/'articles'/path).exists())

    def test_all_sources_are_https_and_unique(self):
        data=json.loads((ROOT/'data/sources.json').read_text(encoding='utf-8'))
        ids=[s['id'] for s in data]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertTrue(all(s['url'].startswith('https://') for s in data))
    def test_monitor_function_from_fixture(self):
        spec=importlib.util.spec_from_file_location('monitor',ROOT/'scripts/check_sources.py')
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        sources=[{'id':'x','url':'https://example.com/','title':'Example'}]
        response=lambda url:(b'<html><body><h1>Cost</h1><script>noise()</script></body></html>',200)
        first,change=module.audit(sources,{},response)
        self.assertEqual(first['x']['state'],'baseline');self.assertEqual(change,[])
        second,change=module.audit(sources,first,response)
        self.assertEqual(second['x']['state'],'unchanged');self.assertEqual(change,[])
        third,change=module.audit(sources,first,lambda u:(b'<h1>New cost</h1>',200))
        self.assertEqual(third['x']['state'],'changed');self.assertEqual(len(change),1)
        failed,change=module.audit(sources,first,lambda u:1/0)
        self.assertEqual(failed['x']['state'],'unavailable');self.assertEqual(change,[])
    def test_project_requires_no_python_dependencies(self):
        self.assertFalse((ROOT/'requirements.txt').exists())
if __name__=='__main__':unittest.main()
