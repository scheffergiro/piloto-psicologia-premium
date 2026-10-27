"""Editorial Home contract; no external runtime or unescaped editorial HTML."""
from html import escape
from .contact import contact_link, floating_link, WHATSAPP_ICON

SOCIAL_ICONS = {
    'Instagram': '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".7"/>',
    'Doctoralia': '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M9 9h6M12 6v6M8 16h8"/>',
}

ARROW = '<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 19 19 5M5 5h14v14"/></svg>'

def values(content, asset):
    e = lambda v: escape(v, quote=True)
    h = content['HOME']
    if asset:
        p = h['photo']
        portrait = f'<img src="{e(p["file"])}" alt="{e(p["alt"])}" width="{p["width"]}" height="{p["height"]}" fetchpriority="high">'
    else:
        portrait = f'<div class="portrait-pending" role="img" aria-label="Retrato autorizado ainda não configurado"><span aria-hidden="true">{e(h["initials"])}</span><p>Espaço reservado para<br>um retrato autorizado.</p><small>{e(h["footer_status"])}</small></div>'
    if content['MODO']=='publicado' and not asset:
        portrait = f'<div class="portrait-pending" role="img" aria-label="Identidade profissional"><span aria-hidden="true">{e(h["initials"])}</span></div>'
    body = '<section class="highlights" aria-label="Características do atendimento"><div class="wrap highlights-grid">'
    for n, label in enumerate(h['highlights']):
        icon = ('<rect x="3" y="5" width="18" height="13" rx="2"/><path d="M8 22h8M12 18v4"/>', '<path d="M4 5h16v12H9l-5 4V5Z"/><path d="M8 9h8M8 13h5"/>', '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c5 5 5 13 0 18-5-5-5-13 0-18Z"/>')[n % 3]
        body += f'<div><svg class="highlight-icon" viewBox="0 0 24 24" aria-hidden="true">{icon}</svg><p>{e(label)}</p></div>'
    body += '</div></section>'
    if not h['highlights']: body = ''
    if h.get('metrics'):
        body += '<section class="metrics" aria-label="Indicadores profissionais"><div class="wrap metrics-grid">'
        for m in h['metrics']:
            body += '<div class="metric"><span class="metric-value">'+e(m['value'])+'</span><span class="metric-label">'+e(m['label'])+'</span></div>'
        body += '</div></section>'
    for s in h['sections']:
        ident = s['id']
        body += f'<section class="section {ident}" id="{ident}" aria-labelledby="{ident}-title"><div class="wrap section-grid"><header><p class="eyebrow">{e(s["eyebrow"])}</p><h2 id="{ident}-title">{e(s["title"])}</h2></header><div class="section-copy">'
        body += ''.join(f'<p>{e(p)}</p>' for p in s['paragraphs'])
        if s.get('note'):
            body += f'<p class="editorial-note">{e(s["note"])}</p>'
        if s.get('cta'):
            body += contact_link(h, s['cta'])
        body += '</div>'
        if s.get('items'):
            body += '<div class="topic-grid">'
            for n, item in enumerate(s['items'], 1):
                marker = '' if ident == 'online' else f'<span class="number" aria-hidden="true">0{n}</span>'
                body += f'<article>{marker}<h3>{e(item["title"])}</h3><p>{e(item["text"])}</p></article>'
            body += '</div>'
        body += '</div></section>'
        if ident == 'online' and h['bridge']['enabled']:
            b = h['bridge']
            body += '<section class="conversion-bridge" aria-labelledby="bridge-title"><div class="wrap"><p class="eyebrow">' + e(b['eyebrow']) + '</p><h2 id="bridge-title">' + e(b['title']).replace('\n', '<br>') + '</h2>' + contact_link(h, b['cta']) + '</div></section>'
    if h.get('testimonials'):
        body += '<section class="section testimonials" aria-label="Depoimentos autorizados"><div class="wrap"><div class="testimonials-grid">'
        for review in h['testimonials']:
            body += '<blockquote><p>'+e(review['text'])+'</p><footer><cite>'+e(review['author'])+'</cite></footer></blockquote>'
        body += '</div><p class="testimonials-note">'+e(h['testimonials_source'])+'</p></div></section>'
    if h['faq']:
        body += '<section class="section faq" id="duvidas" aria-labelledby="faq-title"><div class="wrap section-grid"><header><p class="eyebrow">' + e(h['faq_heading']['eyebrow']) + '</p><h2 id="faq-title">' + e(h['faq_heading']['title']) + '</h2><p>' + e(h['faq_heading']['intro']) + '</p></header><div class="questions">'
        for item in h['faq']:
            body += f'<details><summary>{e(item["question"])}</summary><p>{e(item["answer"])}</p></details>'
        body += '</div></div></section>'
    c = h['contact']
    body += '<section class="section contato" id="contato" aria-labelledby="contact-title"><div class="wrap section-grid"><header><p class="eyebrow">' + e(c['eyebrow']) + '</p><h2 id="contact-title">' + e(c['title']) + '</h2></header><div class="section-copy"><p>' + e(c['text']) + '</p><div class="contact-actions">'
    if h['whatsapp']['number'] or h['cta_url'] and h['cta_url'] != '#contato':
        body += contact_link(h, c['cta'])
    for channel in h['contacts']:
        label, href = channel['label'], channel['url']
        if not href: continue
        icon = '<svg class="social-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + SOCIAL_ICONS.get(label, '') + '</svg>'
        body += f'<a class="button" href="{e(href)}" target="_blank" rel="noopener noreferrer">{icon} {e(label)}</a>'
    body += '</div><p class="microcopy">' + e(c['microcopy']) + '</p></div></div></section>'
    body = body.replace('<span aria-hidden="true">↗</span>', ARROW)
    nav = ''.join(f'<a href="#{e(s["id"])}">{e(s["nav"])}</a>' for s in h['sections'] if s.get('nav'))
    faq_nav = '<a href="#duvidas">Dúvidas frequentes</a>' if h['faq'] else ''
    full = content['NOME'] + ' · ' + content['PROFISSAO']
    return {'HERO_CLASS':' long-name' if len(content['NOME'])>30 else '', 'TITLE':e(content['NOME']), 'NAME':' '.join('<span>'+e(part)+'</span>' for part in h['name_lines']),
            'DESCRIPTION':e(content['SEO_DESCRICAO']), 'BRAND':e(h['brand']), 'FULL_IDENTITY':e(full),
            'EYEBROW':e(h['eyebrow']), 'PROFESSION':e(content['PROFISSAO'] + (' · ' + h['modality'] if h['modality'] else '')),
            'STATUS':e(content['CRP']), 'HEADING':e(h['title']), 'INTRODUCTION':e(h['subtitle']),
            'HERO_MICROCOPY':e(h['microcopy']), 'SECTIONS':body, 'PHOTO':portrait,
            'NAV':nav + faq_nav, 'FOOTER_NAV':nav, 'FAQ_NAV':faq_nav,
            'FOOTER_TEXT':e(h['footer_text']).replace('\n','<br>'),
            'FOOTER_STATUS':e(h['footer_status']) if content['MODO']=='demo' else '',
            'PREVIEW_NOTE':'<div class="preview-note">'+e(h['preview_note'])+'</div>' if content['MODO']=='demo' else '',
            'HEADER_CTA':contact_link(h, h['cta'], classes='button nav-cta'),
            'HERO_CTA':contact_link(h, h['cta'], icon=WHATSAPP_ICON, classes='button hero-contact'),
            'FLOAT':floating_link(h)}
