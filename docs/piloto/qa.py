"""QA local do piloto; requer Playwright e Chromium. Não altera o site."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/piloto'; URL='http://127.0.0.1:8765'
MEASURE='''() => {
const box=s=>{let e=document.querySelector(s),r=e.getBoundingClientRect(),c=getComputedStyle(e);return {x:r.x,y:r.y,width:r.width,height:r.height,font:c.fontFamily,size:c.fontSize,color:c.color,background:c.backgroundColor,border:c.border,radius:c.borderRadius}};
return {hero:box('.hero'),portrait:box('.portrait'),name:box('h1'),cta:box('.hero-contact'),overflow:document.documentElement.scrollWidth>innerWidth,fonts:document.fonts.check('16px "DM Sans"')&&document.fonts.check('16px "Playfair Display"'),orphans:[...document.querySelectorAll('a[href^="#"]')].filter(e=>!document.getElementById(e.hash.slice(1))).map(e=>e.hash),broken:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src),external:[...document.querySelectorAll('a[href]')].filter(e=>/^https?:/.test(e.getAttribute('href'))).map(e=>e.href),h1:document.querySelectorAll('h1').length,robots:document.querySelector('meta[name="robots"]').content,canonical:!!document.querySelector('link[rel="canonical"]'),jsonld:!!document.querySelector('script[type="application/ld+json"]')};}'''
records=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for w,h in [(320,740),(390,844),(768,900),(1280,720),(1366,768),(1440,900)]:
  ctx=b.new_context(viewport={'width':w,'height':h},reduced_motion='reduce');page=ctx.new_page();errors=[];responses=[]
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r: responses.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  page.goto(URL+'/preview/pilot-baseline/');page.evaluate('document.fonts.ready');base=page.evaluate(MEASURE)
  if w in (390,1440):page.screenshot(path=str(OUT/f'baseline-hero-{w}.png'))
  page.goto(URL+'/public/');page.evaluate('document.fonts.ready');page.wait_for_timeout(100);data=page.evaluate(MEASURE)
  assert not data['overflow'] and not data['orphans'] and not data['broken'] and not data['external']
  assert data['fonts'] and data['h1']==1 and data['robots']=='noindex,nofollow' and not data['canonical'] and not data['jsonld']
  # Componentes/paleta/fontes preservados; nome e conteúdo têm medidas próprias.
  for selector in ('hero','portrait'):
   for key in (('width','height','font','size','color','background','border','radius') if selector=='portrait' else ('x','width','font','size','color','background','border','radius')):
    assert data[selector][key]==base[selector][key],(w,selector,key,data[selector],base[selector])
  if w in (390,1440):
   page.screenshot(path=str(OUT/f'demo-{w}.png'),full_page=True);page.screenshot(path=str(OUT/f'demo-hero-{w}.png'))
   page.locator('.hero-contact').hover();page.screenshot(path=str(OUT/f'hover-{w}.png'))
  if w<=1080:
   t=page.locator('.menu-toggle');t.focus();page.keyboard.press('Enter');assert t.get_attribute('aria-expanded')=='true'
   if w==390:page.screenshot(path=str(OUT/'menu-390.png'))
   page.keyboard.press('Escape');assert t.get_attribute('aria-expanded')=='false';assert t.evaluate('(e)=>e===document.activeElement')
   t.click();page.locator('#navigation a[href="#sobre"]').click();assert t.get_attribute('aria-expanded')=='false'
  page.locator('a.skip-link').focus();page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='conteudo'
  summary=page.locator('summary').first;summary.focus();page.keyboard.press('Enter');assert page.locator('details').first.get_attribute('open') is not None
  page.keyboard.press('Enter');assert page.locator('details').first.get_attribute('open') is None
  page.locator('.hero-contact').click();page.wait_for_timeout(100);assert page.url.endswith('#contato')
  assert page.locator('#contato').is_visible()
  if w in (390,1440):page.screenshot(path=str(OUT/f'contato-{w}.png'))
  assert not errors and not responses,(errors,responses)
  records.append(dict(viewport=[w,h],checks='layout/fontes/âncoras/CTA/FAQ/teclado/SEO/assets',measurements=data,baseline=base,errors=errors,http_errors=responses));ctx.close()
 for w in (320,390,768,1440):
  ctx=b.new_context(viewport={'width':w,'height':900},java_script_enabled=False);page=ctx.new_page();page.goto(URL+'/public/');page.evaluate('document.fonts.ready')
  assert page.locator('#navigation').is_visible() and page.locator('.menu-toggle').is_hidden()
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.locator('summary').first.click();assert page.locator('details').first.get_attribute('open') is not None
  records.append(dict(viewport=[w,900],javascript=False,result='navegação, FAQ e conteúdo disponíveis'));ctx.close()
 for w in (390,768,1440):
  ctx=b.new_context(viewport={'width':w,'height':900});page=ctx.new_page();page.goto(URL+'/public/')
  page.wait_for_timeout(100);initial=page.evaluate('document.getAnimations().filter(a=>a.id==="hero-entrance").length');assert initial>0
  page.locator('.hero-contact').focus();assert not page.locator('.hero-contact').evaluate('(e)=>e.getAnimations().some(a=>a.id==="hero-entrance")')
  page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(50);assert not page.evaluate('document.getAnimations().length')
  page.goto(URL+'/public/#sobre');page.reload();page.wait_for_timeout(100);assert not page.evaluate('document.getAnimations().some(a=>a.id==="hero-entrance")')
  page.emulate_media(reduced_motion='no-preference');page.goto(URL+'/public/');page.wait_for_timeout(1100)
  page.locator('#abordagem').scroll_into_view_if_needed();page.wait_for_timeout(80);scroll_animations=page.evaluate('document.getAnimations().length');assert scroll_animations>0
  page.wait_for_timeout(500);page.locator('#inicio').scroll_into_view_if_needed();page.locator('#abordagem').scroll_into_view_if_needed();page.wait_for_timeout(50);assert not page.evaluate('document.getAnimations().length')
  page.goto(URL+'/public/#sobre');page.wait_for_timeout(100);page.goto(URL+'/public/#abordagem');page.go_back();assert page.url.endswith('#sobre');page.go_forward();assert page.url.endswith('#abordagem')
  page.goto(URL+'/public/#inicio');page.wait_for_timeout(100);assert not page.url.endswith('#inicio');page.reload();page.wait_for_timeout(100);assert not page.evaluate('document.getAnimations().some(a=>a.id==="hero-entrance")')
  records.append(dict(viewport=[w,900],motion='entrada/foco/reduce dinâmico/scroll único/reload/histórico',initial_animations=initial,scroll_animations=scroll_animations));ctx.close()
 # Ausência de APIs opcionais: conteúdo continua disponível.
 ctx=b.new_context(viewport={'width':390,'height':844});ctx.add_init_script('delete window.IntersectionObserver; delete Element.prototype.animate;');page=ctx.new_page();page.goto(URL+'/public/');assert page.locator('h1').is_visible();assert page.locator('.hero-contact').is_visible();records.append(dict(optional_apis=False,result='conteúdo e CTA visíveis'));ctx.close()
 b.close()
(OUT/'qa.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print(f'{len(records)} cenários aprovados')
