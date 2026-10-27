"""Validação do contrato v2 e leitura de assets antes de modificar a saída."""
import json
import re
from pathlib import Path
from seo import https_url

IDS = ('sobre', 'como-posso-ajudar', 'abordagem', 'online', 'exterior', 'recurso')
COLORS = ('olive','dark','cream','beige','gold','ink','muted','line','white','focus')

def require(condition, message):
    if not condition:
        raise ValueError(message)

def text(value, label, required=True):
    require(isinstance(value, str) and (not required or bool(value.strip())), label + ': esperado texto' + (' não vazio.' if required else '.'))
    return value

def fields(obj, names, label):
    require(isinstance(obj, dict), label + ': esperado objeto.')
    require(set(names) <= obj.keys(), label + ': campos ausentes: ' + ', '.join(sorted(set(names)-obj.keys())))

def safe_asset(root, name):
    text(name, 'asset')
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts and ':' not in name and '\\' not in name and re.fullmatch(r'assets/[a-zA-Z0-9_./-]+', name), 'Asset deve usar caminho relativo dentro de src/assets/.')
    source = root / name
    require(not any(p.is_symlink() for p in [source, *source.parents] if p != root.parent), 'Asset não pode usar symlink.')
    require(source.resolve().is_relative_to((root / 'assets').resolve()), 'Asset fora de src/assets/.')
    require(source.is_file() and source.stat().st_nlink == 1, 'Asset ausente ou hard link: ' + name)
    data = source.read_bytes()
    ext = source.suffix.lower()
    valid = (ext in ('.jpg','.jpeg') and data.startswith(b'\xff\xd8\xff') or ext == '.png' and data.startswith(b'\x89PNG\r\n\x1a\n') or ext == '.webp' and data[:4] == b'RIFF' and data[8:12] == b'WEBP')
    require(valid and len(data) <= 12*1024*1024, 'Imagem inválida ou maior que 12 MB.')
    return data

def load(path, source):
    data = json.loads(path.read_text(encoding='utf-8'))
    fields(data, ('VERSAO','NOME','PROFISSAO','CRP','MODO','URL_SITE','SEO_TITULO','SEO_DESCRICAO','IMAGEM_SOCIAL','IMAGEM_SOCIAL_ALT','TOKENS','HOME'), 'configuração v2')
    require(data['VERSAO'] == 2, 'Use VERSAO=2; consulte docs/CONFIGURACAO.md.')
    legacy = {
        'WHATSAPP': 'HOME.whatsapp.number',
        'WHATSAPP_MENSAGEM': 'HOME.whatsapp.message',
        'INSTAGRAM_URL': 'HOME.contacts (label=Instagram)',
        'FOTO': 'HOME.photo.file',
    }
    obsolete = sorted(data.keys() & legacy.keys())
    require(not obsolete, 'Configuração v2: remova os campos legados do nível principal, mesmo vazios; use somente HOME: ' +
            ', '.join(key + ' → ' + legacy[key] for key in obsolete))
    for k,v in data.items():
        if k not in ('VERSAO','TOKENS','HOME'): text(v,k,False)
    for k in ('NOME','PROFISSAO','CRP','MODO'): text(data[k],k)
    require(data['MODO'] in ('demo','publicado'), 'MODO deve ser demo ou publicado.')
    h=data['HOME']
    fields(h, ('brand','name_lines','initials','eyebrow','modality','photo','whatsapp','cta','cta_url','fallback_cta','title','subtitle','microcopy','highlights','sections','bridge','faq_heading','faq','contacts','contact','footer_text','footer_status','preview_note','floating_label'), 'HOME')
    for k in ('brand','initials','eyebrow','cta','fallback_cta','title','subtitle','microcopy','footer_text','footer_status','preview_note','floating_label'): text(h[k],k)
    text(h['modality'],'modality',False)
    require(isinstance(h['name_lines'],list) and h['name_lines'], 'name_lines: use uma lista não vazia.')
    for v in h['name_lines']: text(v,'name_lines')
    require(' '.join(' '.join(h['name_lines']).split()) == ' '.join(data['NOME'].split()), 'name_lines deve corresponder ao NOME completo.')
    require(isinstance(h['highlights'], list), 'highlights: esperado array.')
    for v in h['highlights']: text(v,'highlight')
    require(isinstance(h['sections'],list), 'sections: esperado array.')
    seen=[]
    for s in h['sections']:
        fields(s,('id','nav','eyebrow','title','paragraphs','items','note','cta'),'section')
        require(s['id'] in IDS and s['id'] not in seen, 'Seção desconhecida ou duplicada.')
        seen.append(s['id'])
        for k in ('eyebrow','title'): text(s[k],k)
        for k in ('nav','note','cta'): text(s[k],k,False)
        require(isinstance(s['paragraphs'],list) and s['paragraphs'], 'paragraphs: esperado array não vazio.')
        for v in s['paragraphs']: text(v,'paragraph')
        require(isinstance(s['items'],list), 'items: esperado array.')
        for item in s['items']:
            fields(item,('title','text'),'item')
            text(item['title'],'item.title');text(item['text'],'item.text')
    require(seen == sorted(seen,key=IDS.index), 'Preserve a ordem das seções da Home aprovada.')
    fields(h['bridge'],('enabled','eyebrow','title','cta'),'bridge')
    require(type(h['bridge']['enabled']) is bool, 'bridge.enabled deve ser booleano.')
    require(not h['bridge']['enabled'] or 'online' in seen,
            'HOME.bridge.enabled=true exige a seção online em HOME.sections; adicione-a ou defina HOME.bridge.enabled=false.')
    for k in ('eyebrow','title','cta'): text(h['bridge'][k],'bridge.'+k)
    fields(h['faq_heading'],('eyebrow','title','intro'),'faq_heading')
    for k in ('eyebrow','title','intro'): text(h['faq_heading'][k],'faq_heading.'+k)
    fields(h['contact'],('eyebrow','title','text','cta','microcopy'),'contact')
    for k in ('eyebrow','title','text','cta','microcopy'): text(h['contact'][k],'contact.'+k)
    require(isinstance(h['faq'],list), 'faq: esperado array.')
    for q in h['faq']:
        fields(q,('question','answer'),'faq')
        text(q['question'],'question');text(q['answer'],'answer')
    fields(h['whatsapp'],('number','message'),'whatsapp')
    phone=text(h['whatsapp']['number'],'number',False)
    text(h['whatsapp']['message'],'message',False)
    require(not phone or re.fullmatch(r'[1-9][0-9]{7,14}',phone), 'WhatsApp: somente país, DDD e número confirmado.')
    require(isinstance(h['contacts'],list), 'contacts: esperado array.')
    for c in h['contacts']:
        fields(c,('label','url'),'contacts');text(c['label'],'label');text(c['url'],'url',False)
        if c['url']: https_url(c['url'],'contacts.url')
    text(h['cta_url'],'cta_url',False)
    if h['cta_url']:
        if h['cta_url'].startswith('#'): require(h['cta_url'][1:] in seen+['inicio','contato']+(['duvidas'] if h['faq'] else []), 'CTA com âncora órfã.')
        else: https_url(h['cta_url'],'cta_url')
    fields(h['photo'],('file','alt','width','height'),'photo')
    p=h['photo'];text(p['file'],'photo.file',False);text(p['alt'],'photo.alt',bool(p['file']))
    for k in ('width','height'): require(type(p[k]) is int and 0<p[k]<=10000, 'Dimensão de foto inválida.')
    assets={}
    if p['file']: assets[p['file']]=safe_asset(source,p['file'])
    tokens=data['TOKENS'];require(isinstance(tokens,dict), 'TOKENS: esperado objeto.')
    for k,v in tokens.items():
        require(k in (*COLORS,'serif','sans','title-size','space-section','gutter'), 'Token desconhecido: '+k)
        if k in COLORS: require(isinstance(v,str) and re.fullmatch(r'#[0-9a-fA-F]{6}',v), 'Token de cor exige #RRGGBB.')
        elif k in ('serif','sans'): require(isinstance(v,str) and re.fullmatch(r"[a-zA-Z0-9 ,'\"-]+",v) and len(v)<160, 'Família de fonte inválida.')
        else: require(isinstance(v,str) and re.fullmatch(r'[0-9.]+(?:px|rem)',v), 'Token de dimensão exige px ou rem.')
    # Preserve opt-in professional evidence without fixed artificial item counts.
    for key in ('metrics','testimonials'):
        require(isinstance(h.get(key,[]),list), key+': esperado array.')
    for m in h.get('metrics',[]):
        fields(m,('value','label'),'metric')
        require(isinstance(m['value'],str) and re.fullmatch(r'[0-9]+(?:[,.][0-9]+)?',m['value']), 'Métrica exige número confirmado.')
        text(m['label'],'metric.label')
    if h.get('testimonials'):
        require(h.get('testimonials_authorized') is True,'Depoimentos exigem testimonials_authorized=true e autorização aplicável.')
        text(h.get('testimonials_source'),'testimonials_source')
        for review in h['testimonials']:
            fields(review,('text','author'),'testimonial')
            text(review['text'],'testimonial.text');text(review['author'],'testimonial.author')
    # SEO remains a flat contract; scan the whole editorial config before production.
    seo={k:v for k,v in data.items() if isinstance(v,str)}
    # Internal SEO adapter only: these names are never accepted as root configuration.
    seo.update(WHATSAPP=phone, WHATSAPP_MENSAGEM=h['whatsapp']['message'], FOTO=p['file'], INSTAGRAM_URL=next((c['url'] for c in h['contacts'] if c['label']=='Instagram'),''))
    seo['EDITORIAL_VALIDACAO']=json.dumps(h,ensure_ascii=False)
    if data['MODO']=='publicado':
        require('fictício' not in seo['EDITORIAL_VALIDACAO'].lower() and 'fictícia' not in seo['EDITORIAL_VALIDACAO'].lower(), 'Substitua os perfis fictícios antes de publicar.')
    return data,seo,assets
