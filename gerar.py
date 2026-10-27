#!/usr/bin/env python3
"""Gera a Home premium em public/ usando configuração v2, sem dependências."""
import argparse
import json
import re
from pathlib import Path
from scripts.config import load, require
from scripts.home import values
from seo import aplicar_seo

BASE = Path(__file__).resolve().parent
SOURCE = BASE / 'src'
MANIFEST = '.generated-files.json'


def safe_output(output):
    output = Path(output).absolute()
    require(not any(p.is_symlink() for p in (output,*output.parents)), 'Saída não pode usar symlinks.')
    resolved = output.resolve()
    require(resolved != BASE and not BASE.is_relative_to(resolved), 'Saída não pode substituir o repositório ou seus ancestrais.')
    if resolved.is_relative_to(BASE):
        require(resolved.relative_to(BASE).parts[0] in ('public','preview'), 'Dentro do repositório, use public/ ou preview/.')
    return output


def gerar(config_path, output_path, *, experimental=False):
    output = safe_output(output_path)
    data, seo, assets = load(Path(config_path), SOURCE)
    replacements = values(data, bool(assets))
    source = (SOURCE / 'home.html').read_text(encoding='utf-8')
    needed = set(re.findall(r'{{([A-Z_]+)}}',source))
    require(needed <= replacements.keys(), 'Placeholder interno desconhecido.')
    # Single substitution: client strings never become executable template syntax.
    page = re.sub(r'{{([A-Z_]+)}}',lambda m:replacements[m[1]],source)
    if data['TOKENS']:
        theme = ':root{' + ''.join('--'+k+':'+v+';' for k,v in data['TOKENS'].items()) + '}'
        page = page.replace('</head>','<style>'+theme+'</style>\n</head>',1)
    page, seo_files = aplicar_seo(page,seo,experimental=experimental)
    files={'index.html':page.encode(), **assets}
    for name in ('styles.css','motion.js','navigation.js'):
        files[name]=(SOURCE/name).read_bytes()
    for name in ('PlayfairDisplay.ttf','DMSans.ttf','PlayfairDisplay-OFL.txt','DMSans-OFL.txt'):
        files['assets/fonts/'+name]=(SOURCE/'assets/fonts'/name).read_bytes()
    for name,content in seo_files.items():
        if content is not None: files[name]=content.encode()
    old=[]
    manifest=output/MANIFEST
    require(not manifest.is_symlink() and (not manifest.exists() or manifest.stat().st_nlink==1),'Manifesto não pode usar links.')
    if manifest.exists():
        old=json.loads((output/MANIFEST).read_text())
        require(isinstance(old,list) and all(isinstance(x,str) for x in old),'Manifesto de geração inválido.')
    # Preflight every read/write/removal, including a previous generation manifest.
    for name in set(old)|set(files)|{MANIFEST,'sitemap.xml','assets/retrato.css'}:
        relative=Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts and ':' not in name and '\\' not in name,'Caminho inválido no manifesto.')
        target=output/relative
        require(not any(p.is_symlink() for p in (target,*target.parents)),'Saída contém symlink: '+name)
        require(not target.is_dir(),'Arquivo de saída é diretório: '+name)
        require(not target.exists() or target.stat().st_nlink == 1,'Saída contém hard link: '+name)
    files[MANIFEST]=(json.dumps(sorted(files),ensure_ascii=False,indent=2)+'\n').encode()
    output.mkdir(parents=True,exist_ok=True)
    for name,content in files.items():
        dest=output/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
    for name in set(old)|{'sitemap.xml','assets/retrato.css'}:
        if name not in files: (output/name).unlink(missing_ok=True)
    print('Home premium gerada: '+str(output/'index.html'))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=BASE/'cliente.json')
    parser.add_argument('--output',type=Path,default=BASE/'public')
    args=parser.parse_args()
    try: gerar(args.config,args.output)
    except (ValueError,KeyError,OSError) as error: parser.exit(1,'Erro: '+str(error)+'\n')
