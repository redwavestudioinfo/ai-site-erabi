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
    def test_v2_home_guided_navigation_and_seo(self):
        html=(ROOT/'site'/'index.html').read_text(encoding='utf-8')
        for required in ('id="choose"','id="services"','id="quick-compare"','id="how-to"',
                         'id="purpose"','id="budget"','id="picker-result"',
                         'AIでホームページ。','PR・広告'):
            with self.subTest(required=required):
                self.assertIn(required,html)
        self.assertIn('google-site-verification',html)
        self.assertIn('gdwm3uodac9SUT8E0ySPk1PbU5tpjHOP52BWKDZ4WbQ',html)
        self.assertEqual(html.count('https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E'),1)
        self.assertNotIn('おすすめ第1位',html)

    def test_v2_comparison_and_local_assets(self):
        html=(ROOT/'site'/'compare.html').read_text(encoding='utf-8')
        self.assertIn('class="compare-highlights"',html)
        self.assertIn('表は横にもスクロールできます',html)
        css=(ROOT/'site'/'assets'/'styles.css').read_text(encoding='utf-8')
        js=(ROOT/'site'/'assets'/'app.js').read_text(encoding='utf-8')
        for token in ('.hero-v2','.service-grid','.picker-v2','.compare-highlights','@media'):
            self.assertIn(token,css)
        self.assertIn('purpose.addEventListener',js)
        self.assertIn('budget.addEventListener',js)

    def test_renderer_keeps_v2_and_tracking(self):
        source=(ROOT/'scripts'/'render_pages.py').read_text(encoding='utf-8')
        self.assertIn('class="hero hero-v2"',source)
        self.assertIn('class="compare-highlights"',source)
        self.assertIn('https://px.a8.net/svt/ejp?a8mat=4BGR8X+DJM182+348+4SNX5E',source)

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
