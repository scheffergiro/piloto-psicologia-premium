from pathlib import Path
import json,shutil,sys
import argparse
sys.dont_write_bytecode=True
parser=argparse.ArgumentParser(description='Prepara comparação com dados sintéticos; referência estritamente em leitura.')
parser.add_argument('--reference',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parents[1];ref=args.reference.resolve();work=root/'preview/visual'
import subprocess
revision=subprocess.check_output(['git','-C',str(ref),'rev-parse','HEAD'],text=True).strip()
if revision!='eaef856f5a998071115d73a98eb99bf2a2e8bfc8': raise SystemExit('Referência deve estar na revisão final aprovada eaef856.')
if subprocess.check_output(['git','-C',str(ref),'status','--porcelain'],text=True).strip(): raise SystemExit('Referência contém alterações locais; não serão usadas.')
work.mkdir(parents=True,exist_ok=True)
# Equivalence fixture exercises every reusable section with synthetic editorial data.
d=json.loads((root/'cliente.json').read_text());h=d['HOME']
for ident,title in [('exterior','Atendimento em diferentes contextos.'),('recurso','Um recurso para conhecer e refletir.')]:
 h['sections'].append(dict(id=ident,nav='Contextos' if ident=='exterior' else '',eyebrow='SEÇÃO OPCIONAL',title=title,paragraphs=['Este conteúdo é inteiramente sintético e serve para comparar o ritmo editorial da composição aprovada. Ative esta seção apenas com informações confirmadas para a profissional.','Os títulos, textos e condições podem ser definidos pela configuração sem modificar os componentes visuais do site.'],items=[],note='',cta='Consultar canais de contato' if ident=='exterior' else ''))
h['photo'].update(file='assets/reserva.png',alt='Reserva geométrica de retrato; não representa uma pessoa')
# Use the checked-in neutral geometric fixture, never a client photograph.
(work/'geometria.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
sys.path.insert(0,str(root));from gerar import gerar
gerar(work/'geometria.json',work/'generated-equivalent')
gerar(root/'examples/alexandre.json',work/'generated-second')
# Same synthetic values through original renderer and original template/styles.
# Avoid importing the template's package under the reference's module names.
sys.path.insert(0,str(ref/'scripts'));import home
original=json.loads((ref/'content/site.json').read_text())
original['identity']['name']=d['NOME'];original['identity']['description']=d['SEO_DESCRICAO']
for k in ('title','subtitle','highlights','faq'):original['home'][k]=h[k]
original['home']['credential']=d['CRP'];original['home']['photo'].update(file='reserva.png',alt=h['photo']['alt'])
original['home']['whatsapp']['number']=None
original['home']['sections']=[{**s,'id':'aflorar' if s['id']=='recurso' else s['id']} for s in h['sections']]
original['contacts']={'Instagram':'#contato'}
v=home.values(original,True);template=(ref/'src/home.html').read_text()
# Hardcoded identity/copy in the original HTML is replaced only in this QA fixture.
template=template.replace('Ilana Honorato Naves · Psicóloga',d['NOME']+' · '+d['PROFISSAO']).replace('Ilana Naves',h['brand']).replace('Análise Transacional','Abordagem').replace('Aflorar Feminino','Recurso opcional')
template=template.replace('Psicóloga · Atendimento online',d['PROFISSAO']+' · '+h['modality']).replace('ESCUTA E CUIDADO EM PORTUGUÊS',h['eyebrow']).replace('Psicoterapia online em português.<br>Brasil e exterior.',h['footer_text'].replace('\n','<br>'))
# Renderer hardcodes some bridge/FAQ/contact copy; align only fixture strings to compare geometry.
body=v['SECTIONS']
body=body.replace('UM PRIMEIRO PASSO',h['bridge']['eyebrow']).replace('Cuidar de si pode começar <br>com uma conversa.',h['bridge']['title'].replace('\n','<br>'))
body=body.replace('Algumas respostas para começar com mais clareza.',h['faq_heading']['intro']).replace('O primeiro passo pode ser uma conversa.',h['contact']['title']).replace('Você pode esclarecer dúvidas e conhecer as possibilidades de acompanhamento antes de decidir iniciar. Entre em contato pelos canais abaixo.',h['contact']['text']).replace('Atendimento exclusivamente online · Em português',h['contact']['microcopy'])
# Original expects an Instagram link for its client resource; omit unavailable channel.
import re
body=re.sub(r'<a class="text-link"[^>]*>Conhecer o perfil da autora.*?</a>','',body)
v['SECTIONS']=body
page=re.sub(r'{{([A-Z_]+)}}',lambda m:v[m[1]],template)
out=work/'reference-synthetic';out.mkdir(exist_ok=True)
(out/'index.html').write_text(page)
shutil.copyfile(ref/'src/styles.css',out/'styles.css');shutil.copyfile(ref/'src/motion.js',out/'motion.js')
shutil.copytree(ref/'src/assets/fonts',out/'assets/fonts',dirs_exist_ok=True)
shutil.copyfile(root/'src/assets/reserva.png',out/'assets/reserva.png')
# Write reference fixture metadata; no original contact/image is shipped.
(out/'fixture.json').write_text(json.dumps({'revision':'eaef856f5a998071115d73a98eb99bf2a2e8bfc8','synthetic':True}))

web=work/'web';web.mkdir(exist_ok=True)
for src,name in [(root/'public','default'),(work/'generated-equivalent','equivalent'),(work/'generated-second','second'),(work/'reference-synthetic','reference')]:
    shutil.copytree(src,web/name,dirs_exist_ok=True)
print('Sirva somente '+str(web)+' e execute scripts/qa_browser.py.')
