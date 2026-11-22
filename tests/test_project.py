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
