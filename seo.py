"""Metadados e arquivos de SEO para landing pages estáticas. Sem dependências."""
import html
import json
import re
from urllib.parse import urlsplit, urljoin
from xml.sax.saxutils import escape as xml_escape


def https_url(value, field):
    try:
        parts = urlsplit(value)
        valid = parts.scheme == 'https' and parts.hostname and not parts.username and not parts.password
        parts.port
    except ValueError:
        valid = False
    if not valid or any(c.isspace() for c in value) or '\\' in value:
        raise ValueError(field + ': informe URL HTTPS válida.')
    return parts


def aplicar_seo(page, data, experimental=False):
    mode = data.get('MODO', 'demo').strip().lower()
    if mode not in ('demo', 'publicado'):
        raise ValueError('MODO deve ser demo ou publicado.')
    title = data.get('SEO_TITULO', '').strip()
    description = data.get('SEO_DESCRICAO', '').strip()
    canonical = data.get('URL_SITE', '').strip()
    if canonical:
        parts = https_url(canonical, 'URL_SITE')
        if parts.query or parts.fragment or parts.path not in ('', '/'):
            raise ValueError('URL_SITE: use somente a origem do site, como https://seu-dominio.com/.')
        canonical = canonical.rstrip('/') + '/'
    production = mode == 'publicado'
    if production:
        if not all((title, description, canonical)):
            raise ValueError('Modo publicado exige URL_SITE, SEO_TITULO e SEO_DESCRICAO.')
        pending = [key for key, value in data.items() if any(marker in value.lower() for marker in (
            'a confirmar', 'a preencher', 'a personalizar', 'a configurar', 'nome da profissional', 'crp: xxx'))]
        if pending:
            raise ValueError('Substitua os textos provisórios antes de publicar: ' + ', '.join(pending))
        if not data.get('NOME', '').strip():
            raise ValueError('Preencha NOME antes de publicar.')
        page = re.sub(r'<div class="notice">.*?</div>', '', page, count=1, flags=re.S)
        page = re.sub(r'<div class="(?:wrap )?disclaimer"[^>]*>.*?</div>', '', page, count=1, flags=re.S)
        page = re.sub(r'<dialog class="demo-dialog"[^>]*>.*?</dialog>', '', page, count=1, flags=re.S)
        page = page.replace(' · Prévia não oficial', '')
        page = page.replace('Demonstração comercial · Não é um canal oficial de atendimento', html.escape(data['NOME']))
        page = page.replace('Espaço reservado para uma fotografia autorizada', html.escape(data['PROFISSAO']))
        page = re.sub(r'aria-label="Área reservada para fotografia profissional[^"]*"', 'aria-label="Identidade visual profissional"', page)
        if not data.get('WHATSAPP', '').strip():
            page = page.replace('<a class="whatsapp-float"', '<a hidden class="whatsapp-float"')
        if not any(data.get(k, '').strip() for k in ('ENDERECO_LOCAL', 'ENDERECO_LOGRADOURO', 'ENDERECO_CIDADE')):
            page = re.sub(r'<address>.*?</address>', '', page, count=1, flags=re.S)
    else:
        title = 'Demonstração | ' + (title or data['NOME'] + ' · ' + data['PROFISSAO'])
        if experimental and not description:
            description = ('Demonstração comercial não oficial de página para ' + data['NOME'] +
                           ', ' + data['PROFISSAO'] + ' em ' + data['CIDADE'] +
                           ', sujeita à aprovação profissional.')
        else:
            description = 'Demonstração comercial não oficial, sujeita à aprovação profissional. ' + description
    robots = 'index,follow' if production and not experimental else 'noindex,nofollow'
    page = re.sub(r'<meta name="robots"[^>]*>', '<meta name="robots" content="' + robots + '">', page, count=1)
    page = re.sub(r'<title>.*?</title>', lambda _: '<title>' + html.escape(title) + '</title>', page, count=1, flags=re.S)
    page = re.sub(r'<meta name="description"[^>]*>', lambda _: '<meta name="description" content="' + html.escape(description, quote=True) + '">', page, count=1)
    tags = []
    def meta(key, value):
        tags.append('<meta property="' + key + '" content="' + html.escape(value, quote=True) + '">')
    meta('og:type', 'website'); meta('og:locale', 'pt_BR')
    meta('og:title', title); meta('og:description', description)
    if production and not experimental:
        tags.append('<link rel="canonical" href="' + html.escape(canonical, quote=True) + '">')
        meta('og:url', canonical); meta('og:site_name', data['NOME'])
    social = data.get('IMAGEM_SOCIAL', '').strip()
    if social:
        https_url(social, 'IMAGEM_SOCIAL')
        if not data.get('IMAGEM_SOCIAL_ALT', '').strip():
            raise ValueError('Informe IMAGEM_SOCIAL_ALT ao configurar a imagem de compartilhamento.')
        meta('og:image', social); meta('og:image:alt', data['IMAGEM_SOCIAL_ALT'])
    if production and not experimental:
        person = {'@type':'Person', '@id':canonical+'#profissional', 'name':data['NOME'], 'jobTitle':data['PROFISSAO'], 'url':canonical}
        if data.get('INSTAGRAM_URL', '').strip(): person['sameAs'] = [data['INSTAGRAM_URL'].strip()]
        if data.get('FOTO', '').strip(): person['image'] = urljoin(canonical, data['FOTO'].strip())
        graph = {'@context':'https://schema.org', '@graph':[
            person,
            {'@type':'WebSite','@id':canonical+'#site','url':canonical,'name':data['NOME'],'inLanguage':'pt-BR','publisher':{'@id':canonical+'#profissional'}},
            {'@type':'WebPage','@id':canonical+'#pagina','url':canonical,'name':title,'description':description,'inLanguage':'pt-BR','isPartOf':{'@id':canonical+'#site'},'about':{'@id':canonical+'#profissional'}}
        ]}
        # Evita que texto de configuração encerre a tag script de JSON-LD.
        payload = json.dumps(graph, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
        tags.append('<script type="application/ld+json">' + payload + '</script>')
    page = page.replace('</head>', '\n'.join(tags) + '\n</head>', 1)
    files = {'robots.txt':'User-agent: *\nAllow: /\n', 'sitemap.xml':None}
    if production and not experimental:
        files['robots.txt'] += '\nSitemap: ' + canonical + 'sitemap.xml\n'
        files['sitemap.xml'] = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>' + xml_escape(canonical) + '</loc></url></urlset>\n'
        # O domínio definitivo deve ser o indexável. Os endereços técnicos permanecem noindex.
        files['_headers'] = '# Indexação principal definida no meta robots do HTML.\n'
        if not urlsplit(canonical).hostname.endswith('.pages.dev'):
            files['_headers'] += 'https://:project.pages.dev/*\n  X-Robots-Tag: noindex, nofollow\n\n'
        files['_headers'] += 'https://:version.:project.pages.dev/*\n  X-Robots-Tag: noindex, nofollow\n'
    else:
        files['_headers'] = '/*\n  X-Robots-Tag: noindex, nofollow\n'
    return page, files
