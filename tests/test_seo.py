import copy
import json
import re
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from gerar import gerar

class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=[];self.links=[];self.assets=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='a': self.links.append(a.get('href',''))
        if tag in ('script','img') and a.get('src'): self.assets.append(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet': self.assets.append(a['href'])

class GenerationContractTest(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.config=self.root/'cliente.json';self.output=self.root/'public'
        self.data=json.loads((ROOT/'cliente.json').read_text())
    def generate(self):
        self.config.write_text(json.dumps(self.data,ensure_ascii=False))
        gerar(self.config,self.output)
        return (self.output/'index.html').read_text()
    def snapshot(self):
        return {str(p.relative_to(self.output)):p.read_bytes() for p in self.output.rglob('*') if p.is_file()}
    def production(self):
        # Reserved example.org; this fixture never publishes or contacts a person.
        self.data.update(MODO='publicado',URL_SITE='https://example.org',SEO_TITULO='Título de teste & segurança',SEO_DESCRICAO='Descrição revisada',CRP='Registro de teste')
        def clean(v):
            if isinstance(v,str):
                for old in ('a confirmar','fictício','fictícia','fictícios','a personalizar','a configurar'): v=v.replace(old,'revisado')
                return v
            if isinstance(v,list): return [clean(x) for x in v]
            if isinstance(v,dict): return {k:clean(x) for k,x in v.items()}
            return v
        self.data=clean(self.data)
    def test_demo_is_not_indexable(self):
        page=self.generate();self.assertIn('content="noindex,nofollow"',page)
        self.assertNotIn('rel="canonical"',page);self.assertNotIn('application/ld+json',page)
        self.assertFalse((self.output/'sitemap.xml').exists())
        self.assertIn('X-Robots-Tag: noindex, nofollow',(self.output/'_headers').read_text())
        self.assertNotIn('Disallow: /',(self.output/'robots.txt').read_text())
    def test_production_outputs_are_consistent_and_safe(self):
        self.production();name='Teste </script><script>alert(1)</script>'
        self.data['NOME']=name;self.data['HOME']['name_lines']=[name]
        page=self.generate();self.assertIn('content="index,follow"',page)
        self.assertIn('rel="canonical" href="https://example.org/"',page)
        self.assertNotIn('class="preview-note"',page);self.assertNotIn('Perfil fictício',page)
        self.assertNotIn('<script>alert(1)</script>',page)
        graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S)[1])['@graph']
        self.assertEqual(graph[0]['name'],name)
        self.assertEqual(ElementTree.parse(self.output/'sitemap.xml').find('.//{*}loc').text,'https://example.org/')
        self.assertIn('Sitemap: https://example.org/sitemap.xml',(self.output/'robots.txt').read_text())
    def test_demo_switch_removes_old_sitemap(self):
        self.production();self.generate();self.data['MODO']='demo';self.generate()
        self.assertFalse((self.output/'sitemap.xml').exists())
        self.assertNotIn('Sitemap:',(self.output/'robots.txt').read_text())
    def test_publication_rejects_invalid_inputs(self):
        self.production()
        for k,v in [('MODO','typo'),('URL_SITE','https://example.org/?x=1'),('URL_SITE','javascript:alert(1)'),('SEO_TITULO',''),('CRP','CRP: XXX')]:
            old=self.data[k];self.data[k]=v
            with self.subTest(field=k),self.assertRaises(ValueError):self.generate()
            self.data[k]=old
    def test_fictitious_profile_cannot_be_published_accidentally(self):
        self.data.update(MODO='publicado',URL_SITE='https://example.org',SEO_TITULO='Teste',SEO_DESCRICAO='Teste',CRP='Registro revisado')
        with self.assertRaises(ValueError):self.generate()
    def test_optional_social_image_requires_alt(self):
        self.data['IMAGEM_SOCIAL']='https://example.org/card.jpg'
        with self.assertRaises(ValueError):self.generate()
        self.data['IMAGEM_SOCIAL_ALT']='Imagem de teste';self.assertIn('property="og:image:alt"',self.generate())
    def test_default_generation_is_deterministic(self):
        self.generate();before=self.snapshot();self.generate();self.assertEqual(before,self.snapshot())
    def test_versioned_public_matches_complete_generated_file_set(self):
        self.generate()
        saved={str(p.relative_to(ROOT/'public')):p.read_bytes() for p in (ROOT/'public').rglob('*') if p.is_file()}
        self.assertEqual(saved,self.snapshot())
    def test_all_whatsapp_links_share_encoded_message(self):
        # Synthetic number for isolated URL-encoding test only; no network request is made.
        self.data['HOME']['whatsapp']={'number':'5511999999999','message':'Mensagem & dúvida?'}
        page=self.generate();p=Links();p.feed(page)
        links=[v for v in p.links if v.startswith('https://wa.me/')]
        self.assertGreaterEqual(len(links),6);self.assertEqual(len(set(links)),1)
        self.assertEqual(parse_qs(urlsplit(links[0]).query)['text'],['Mensagem & dúvida?'])
    def test_empty_contacts_never_create_external_links(self):
        p=Links();p.feed(self.generate());self.assertFalse(any(x.startswith('https://') for x in p.links))
        self.assertNotIn('id="whatsapp"',(self.output/'index.html').read_text())
    def test_urls_are_validated_before_modifying_output(self):
        self.generate();before=self.snapshot()
        for href in ('javascript:alert(1)','https://a.invalid/ x','https://user:pass@a.invalid','http://a.invalid','https://a.invalid\\evil'):
            self.data['HOME']['contacts']=[{'label':'Instagram','url':href}]
            with self.subTest(href=href),self.assertRaises(ValueError):self.generate()
            self.assertEqual(before,self.snapshot())
    def test_invalid_configuration_preserves_previous_output(self):
        self.generate();before=self.snapshot();self.data['TOKENS']={'olive':'red; background:url(evil)'}
        with self.assertRaises(ValueError):self.generate()
        self.assertEqual(before,self.snapshot())
    def test_name_lines_are_data_and_must_match_identity(self):
        self.data['HOME']['name_lines']=['Outra pessoa']
        with self.assertRaises(ValueError):self.generate()
    def test_escaping_does_not_expand_client_template_syntax(self):
        text='<img src=x onerror=alert(1)> {{SECTIONS}} [[SLOT:HEAD]]'
        self.data['HOME']['title']=text;page=self.generate()
        self.assertIn('&lt;img src=x onerror=alert(1)&gt; {{SECTIONS}} [[SLOT:HEAD]]',page)
        self.assertNotIn('<img src=x',page)
    def test_anchor_integrity_for_default_and_minimal_profiles(self):
        for cfg in ('cliente.json','examples/alexandre.json'):
            self.data=json.loads((ROOT/cfg).read_text());p=Links();p.feed(self.generate())
            self.assertEqual(len(p.ids),len(set(p.ids)))
            for href in p.links:
                if href.startswith('#'):self.assertIn(href[1:],p.ids)
    def test_second_profile_does_not_leak_first_and_is_reproducible(self):
        self.generate();first=self.snapshot();a=copy.deepcopy(self.data)
        self.data=json.loads((ROOT/'examples/alexandre.json').read_text());page=self.generate()
        for text in ('Clara','Beatriz','Ramos','como-posso-ajudar','id="duvidas"','conversion-bridge','highlights-grid'):
            self.assertNotIn(text,page)
        self.data=a;self.generate();self.assertEqual(first,self.snapshot())
    def test_variable_item_counts_and_optional_sections(self):
        h=self.data['HOME'];h['highlights']=['Um','Dois','Três','Quatro']
        h['sections'][1]['items']*=2
        self.assertEqual(self.generate().count('<article>'),9)
        h['sections']=[];h['faq']=[];h['highlights']=[];h['bridge']['enabled']=False
        page=self.generate();self.assertNotIn('href="#sobre"',page);self.assertNotIn('class="section faq"',page)
    def test_optional_exterior_and_resource_are_explicit(self):
        for ident in ('exterior','recurso'):
            self.data['HOME']['sections'].append(dict(id=ident,nav='Seção opcional',eyebrow='Exemplo',title='Conteúdo configurado',paragraphs=['Texto sintético'],items=[],note='',cta=''))
        page=self.generate();self.assertIn('id="recurso"',page);self.assertIn('href="#exterior"',page)
    def test_orphan_cta_is_rejected(self):
        self.data['HOME']['cta_url']='#ausente'
        with self.assertRaises(ValueError):self.generate()
    def test_custom_https_cta_is_escaped(self):
        self.data['HOME']['cta_url']='https://example.invalid/agendar?a=1&b=2'
        self.assertIn('href="https://example.invalid/agendar?a=1&amp;b=2"',self.generate())
    def test_disallowed_tokens_and_css_injection_are_rejected(self):
        for tokens in ({'unknown':'#ffffff'},{'sans':'Arial;}</style><script>'},{'gutter':'url(evil)'}):
            self.data['TOKENS']=tokens
            with self.subTest(tokens=tokens),self.assertRaises(ValueError):self.generate()
    def test_assets_exist_and_no_client_data_is_shipped(self):
        page=self.generate();p=Links();p.feed(page)
        for asset in p.assets:self.assertTrue((self.output/asset).is_file(),asset)
        for term in ('Ilana','Honorato','Aflorar','5562994579466','psi.ilananaves'):
            self.assertNotIn(term,page)
        self.assertFalse(any('ilana' in str(p).lower() for p in self.output.rglob('*')))
    def test_evidence_is_optional_variable_and_requires_authorization(self):
        self.data['HOME']['metrics']=[{'value':'2','label':'Indicador de teste'}]
        self.assertIn('Indicador de teste',self.generate())
        self.data['HOME']['metrics'][0]['value']='2 mil'
        with self.assertRaises(ValueError):self.generate()
        self.data['HOME']['metrics']=[]
        self.data['HOME']['testimonials']=[{'text':'Conteúdo sintético isolado','author':'Autoria de teste'}]
        with self.assertRaises(ValueError):self.generate()
        self.data['HOME'].update(testimonials_authorized=True,testimonials_source='Fonte de teste')
        self.assertIn('Conteúdo sintético isolado',self.generate())

    def test_root_legacy_fields_are_rejected_even_when_empty_without_changing_output(self):
        self.generate();before=self.snapshot()
        destinations = {'WHATSAPP':'HOME.whatsapp.number',
                        'WHATSAPP_MENSAGEM':'HOME.whatsapp.message',
                        'INSTAGRAM_URL':'HOME.contacts', 'FOTO':'HOME.photo.file'}
        for key,destination in destinations.items():
            for value in ('', 'valor legado divergente'):
                self.data[key]=value
                with self.subTest(field=key,value=value):
                    with self.assertRaises(ValueError) as error: self.generate()
                    self.assertIn(key,str(error.exception))
                    self.assertIn(destination,str(error.exception))
                    self.assertIn('mesmo vazios',str(error.exception))
                    self.assertEqual(before,self.snapshot())
                del self.data[key]

    def test_home_is_the_only_source_for_internal_seo_adapters(self):
        from scripts.config import load
        self.production()
        h=self.data['HOME']
        h['whatsapp']={'number':'5511999999999','message':'Mensagem de teste & dúvida?'}
        h['contacts']=[{'label':'Instagram','url':'https://example.org/perfil'}]
        h['photo'].update(file='assets/reserva.png',alt='Reserva geométrica sintética')
        page=self.generate()
        _,seo,assets=load(self.config,ROOT/'src')
        self.assertEqual(seo['WHATSAPP'],h['whatsapp']['number'])
        self.assertEqual(seo['WHATSAPP_MENSAGEM'],h['whatsapp']['message'])
        self.assertEqual(seo['INSTAGRAM_URL'],h['contacts'][0]['url'])
        self.assertEqual(seo['FOTO'],h['photo']['file'])
        self.assertIn(h['photo']['file'],assets)
        graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',page,re.S)[1])['@graph']
        self.assertEqual(graph[0]['sameAs'],['https://example.org/perfil'])
        self.assertEqual(graph[0]['image'],'https://example.org/assets/reserva.png')
        self.assertIn('alt="Reserva geométrica sintética"',page)
        self.assertIn('https://wa.me/5511999999999?text=',page)

    def test_bridge_enabled_without_online_is_rejected_without_changing_output(self):
        self.generate();before=self.snapshot()
        h=self.data['HOME'];h['sections']=[s for s in h['sections'] if s['id']!='online']
        with self.assertRaisesRegex(ValueError,'HOME.bridge.enabled=true exige a seção online em HOME.sections'):
            self.generate()
        self.assertEqual(before,self.snapshot())

    def test_bridge_is_rendered_only_when_explicitly_enabled_with_online(self):
        h=self.data['HOME']
        self.assertIn('class="conversion-bridge"',self.generate())
        h['bridge']['enabled']=False
        self.assertNotIn('class="conversion-bridge"',self.generate())
        h['sections']=[s for s in h['sections'] if s['id']!='online']
        self.assertNotIn('class="conversion-bridge"',self.generate())

    def test_all_shipped_examples_use_home_only_and_generate(self):
        legacy={'WHATSAPP','WHATSAPP_MENSAGEM','INSTAGRAM_URL','FOTO'}
        for config in [ROOT/'cliente.json',*sorted((ROOT/'examples').glob('*.json'))]:
            with self.subTest(config=config.name):
                self.data=json.loads(config.read_text())
                self.assertFalse(legacy & self.data.keys())
                self.generate()

    def test_legacy_configuration_fails_with_actionable_error(self):
        del self.data['VERSAO']
        with self.assertRaisesRegex(ValueError,'v2'):self.generate()

if __name__=='__main__':unittest.main()
