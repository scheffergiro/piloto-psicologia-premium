import json
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse
parser=argparse.ArgumentParser(description='QA Chromium opcional; requer Playwright e Chromium instalados.')
parser.add_argument('--url',default='http://127.0.0.1:8765')
parser.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'preview/visual/capturas')
parser.add_argument('--chromium',default='/usr/bin/chromium')
args=parser.parse_args();OUT=args.output;OUT.mkdir(parents=True,exist_ok=True)
measure='''() => {
const box = s => {const e=document.querySelector(s);if(!e)return null; const r=e.getBoundingClientRect(); const c=getComputedStyle(e);return {x:r.x,y:r.y,width:r.width,height:r.height,bottom:r.bottom,font:c.fontFamily,fontSize:c.fontSize,color:c.color,background:c.backgroundColor,border:c.border,borderRadius:c.borderRadius,shadow:c.boxShadow}};
return {hero:box('.hero'),name:box('h1'),portrait:box('.portrait'),cta:box('.hero-contact'),header:box('.site-header'),sections:[...document.querySelectorAll('main>section')].map(e=>({id:e.id,height:e.getBoundingClientRect().height,top:e.getBoundingClientRect().top})),overflow:document.documentElement.scrollWidth>innerWidth,fonts:document.fonts.check('16px "DM Sans"')&&document.fonts.check('16px "Playfair Display"'),orphans:[...document.querySelectorAll('a[href^="#"]')].filter(e=>!document.getElementById(e.hash.slice(1))).map(e=>e.hash),broken:[...document.images].filter(e=>!e.complete||!e.naturalWidth).map(e=>e.src)}
}'''
records=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path=args.chromium,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(320,740),(390,844),(768,900),(1366,768),(1440,900),(1280,720)]:
  for profile in ('reference','equivalent','default','second'):
   ctx=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
   page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
   page.goto(f'{args.url}/{profile}/');page.evaluate('document.fonts.ready');page.wait_for_timeout(100)
   data=page.evaluate(measure);data.update(profile=profile,viewport=[width,height],errors=errors)
   if width in (390,1440):
    page.screenshot(path=str(OUT/f'{profile}-{width}.png'),full_page=True)
    page.screenshot(path=str(OUT/f'{profile}-hero-{width}.png'))
   if profile!='reference':
    if width<=1080:
     t=page.locator('.menu-toggle');t.focus();page.keyboard.press('Enter');assert t.get_attribute('aria-expanded')=='true'
     page.keyboard.press('Escape');assert t.get_attribute('aria-expanded')=='false';assert t.evaluate('(e)=>e===document.activeElement')
    page.locator('a.skip-link').focus();page.keyboard.press('Enter');assert page.evaluate('document.activeElement.id')=='conteudo'
    if page.locator('details').count():
     page.locator('summary').first.focus();page.keyboard.press('Enter');assert page.locator('details').first.get_attribute('open') is not None
    assert not data['overflow'],(profile,width,'overflow');assert not data['orphans'],data['orphans'];assert not data['broken'];assert not errors
   records.append(data);ctx.close()
 for width in (320,390,768,1440):
  for profile in ('default','second','equivalent'):
   ctx=browser.new_context(viewport={'width':width,'height':900},java_script_enabled=False)
   page=ctx.new_page();page.goto(f'{args.url}/{profile}/')
   assert page.locator('#navigation').is_visible();assert page.locator('.menu-toggle').is_hidden()
   assert page.locator('h1').is_visible();assert page.locator('.hero-contact').is_visible()
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(profile,width,'noJS overflow')
   records.append({'profile':profile,'viewport':[width,900],'javascript':False,'navigation':'visible','overflow':False});ctx.close()
 for width in (390,768,1440):
  ctx=browser.new_context(viewport={'width':width,'height':900});page=ctx.new_page()
  page.goto(args.url+'/default/');page.evaluate('document.fonts.ready')
  count=page.evaluate('document.getAnimations().length');page.locator('.hero-contact').focus()
  page.emulate_media(reduced_motion='reduce');page.wait_for_function('!document.getAnimations().some(a=>a.id==="hero-entrance")',timeout=3000)
  assert not page.evaluate('document.getAnimations().some(a=>a.id==="hero-entrance")')
  page.goto(args.url+'/default/#sobre');page.reload();page.wait_for_timeout(150)
  assert not page.evaluate('document.getAnimations().some(a=>a.id==="hero-entrance")')
  records.append({'profile':'default','viewport':[width,900],'motion':'initial/dynamic-reduce/focus/anchor-reload','initialAnimations':count});ctx.close()
 browser.close()
(OUT/'qa.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
print('QA concluído:',len(records),'cenários')
for r in records:
 if r.get('profile') in ('reference','equivalent') and 'hero'in r:
  print(r['profile'],r['viewport'],'hero',round(r['hero']['height'],1),'portrait',round(r['portrait']['width'],1),round(r['portrait']['height'],1),'cta bottom',round(r['cta']['bottom'],1))
