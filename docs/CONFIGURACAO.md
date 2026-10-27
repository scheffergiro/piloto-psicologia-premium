# Configuração v2

A fonte da Home está em `src/`. A fonte editorial é `cliente.json` (ou o arquivo
passado em `--config`); a geração não depende dos repositórios de referência,
Playbook, skills ou frameworks. Python 3.9+ e biblioteca padrão bastam.

## Preparar uma demo

1. Crie o repositório isolado do lead a partir deste template.
2. Copie `examples/clara.json` para a configuração do lead. Use apenas dados
   confirmados e substitua todos os exemplos fictícios.
3. Coloque uma foto autorizada em `src/assets/`, configure `HOME.photo.file`
   como `assets/foto.jpg`, alt e dimensões reais. Vazio mantém reserva editorial.
4. Preencha textos, contatos e seções no JSON. Gere com `gerar.py`.
5. Execute a suíte, revise desktop/mobile e a jornada antes de publicar qualquer
   demo no repositório do lead. Este trabalho não publica demo real de cliente.

```bash
python3 -B gerar.py --config examples/clara.json --output preview/clara
python3 -m http.server 8000 --directory preview/clara
```

`--output` aceita diretório externo ou `public/`/`preview/` dentro do projeto.
Não use fontes ou a raiz do repositório como destino. A saída contém um manifesto:
assets gerenciados anteriores deixam de existir quando são desconfigurados.
Arquivos alheios ao manifesto são preservados. Não coloque fotos diretamente na
saída; a fonte autorizada deve ficar em `src/assets/`.

## Campos

| Campo | Uso |
| --- | --- |
| `VERSAO` | `2`; configurações v1 falham explicitamente |
| `NOME`, `PROFISSAO`, `CRP` | Identificação profissional confirmada; `NOME` também alimenta SEO |
| `MODO` | `demo` ou `publicado` |
| `URL_SITE`, `SEO_TITULO`, `SEO_DESCRICAO` | Domínio definitivo e metadados; exigidos para publicado |
| `IMAGEM_SOCIAL`, `IMAGEM_SOCIAL_ALT` | Imagem HTTPS opcional para Open Graph e alt obrigatório |
| `HOME.brand` | Nome curto de apresentação no cabeçalho/rodapé |
| `HOME.name_lines` | Lista das linhas editoriais do nome; deve corresponder a `NOME`; linhas podem quebrar para acomodar nomes longos |
| `HOME.initials` | Reserva visual quando não há foto |
| `HOME.eyebrow`, `modality`, `title`, `subtitle`, `microcopy` | Abertura, modalidade e textos do Hero |
| `HOME.photo` | `file`, `alt`, `width`, `height`; JPG/PNG/WebP local autorizado, até 12 MB |
| `HOME.whatsapp` | `number` confirmado (país+DDD+número, só dígitos) e `message`; número vazio não gera links WhatsApp |
| `HOME.cta` | Rótulo do CTA de cabeçalho e Hero |
| `HOME.cta_url` | Destino comum opcional, HTTPS ou âncora existente; precede WhatsApp nos CTAs editoriais |
| `HOME.fallback_cta` | Texto usado quando não há destino configurado; direciona a `#contato` |
| `HOME.highlights` | Lista de características confirmadas; `[]` remove a faixa |
| `HOME.sections` | Lista de seções, em ordem de referência; remova o objeto para ocultar |
| `HOME.bridge` | `enabled`, `eyebrow`, `title`, `cta`; `enabled=true` exige a seção `online`; a faixa aparece após ela; `\n` quebra o título |
| `HOME.faq_heading` | `eyebrow`, `title`, `intro` |
| `HOME.faq` | Lista de `{question, answer}`; `[]` remove FAQ e seus links |
| `HOME.contacts` | Lista de `{label, url}` HTTPS; Instagram/Doctoralia têm ícones; URL vazia não produz link |
| `HOME.contact` | `eyebrow`, `title`, `text`, `cta`, `microcopy`; sem canais não há ação externa fictícia |
| `HOME.preview_note`, `floating_label` | Aviso de demo e texto do flutuante; altere o aviso ao preparar dados reais |
| `HOME.footer_text`, `footer_status` | Apresentação e aviso do rodapé; `\n` quebra texto; status só na demo |
| `HOME.metrics` | Opcional: lista de `{value, label}`; números confirmados, sem quantidade fixa |
| `HOME.testimonials` | Opcional: lista de `{text, author}`; exige `testimonials_authorized: true` e `testimonials_source` não vazia; autorização explícita é responsabilidade do configurador |
| `TOKENS` | Overrides explícitos de tokens; `{}` preserva os valores da referência |

Cada seção contém `id`, `nav`, `eyebrow`, `title`, `paragraphs`, `items`, `note`,
`cta`. `items` é uma lista de `{title, text}`, sem quantidade artificial fixa.
`nav` vazio omite o link do menu/rodapé. `note` e `cta` podem ficar vazios.
IDs reutilizáveis, em ordem: `sobre`, `como-posso-ajudar`, `abordagem`, `online`,
`exterior`, `recurso`. Os dois últimos são opcionais e ausentes por padrão.
O antigo componente do e-book torna-se `recurso`, sem conteúdo ou link da autora.

Os CTAs compartilham `cta_url` ou o WhatsApp com a mesma mensagem codificada.
O flutuante aparece somente com WhatsApp confirmado e permanece destinado a esse
canal. Com ausência de contatos, CTAs iniciais conduzem à seção informativa; ela
não mostra um botão que apenas retornaria à própria seção. Os exemplos não
incluem nenhum número ou link de contato inventado.

## Fonte única e dependência da faixa editorial

No esquema v2, `WHATSAPP`, `WHATSAPP_MENSAGEM`, `INSTAGRAM_URL` e `FOTO` no nível
principal são rejeitados, **mesmo vazios**, com indicação do campo correto:

| Campo legado a remover | Fonte operacional única |
| --- | --- |
| `WHATSAPP` | `HOME.whatsapp.number` |
| `WHATSAPP_MENSAGEM` | `HOME.whatsapp.message` |
| `INSTAGRAM_URL` | Item de `HOME.contacts` com `label: "Instagram"` e `url` |
| `FOTO` | `HOME.photo.file`, com alt e dimensões em `HOME.photo` |

Não há precedência entre valores duplicados: remova as chaves antigas e preencha
somente `HOME`. O adaptador interno continua derivando os nomes exigidos por
`seo.py` a partir de `HOME`, preservando links, mensagem, imagem e `sameAs` nos
dados estruturados; esses nomes internos não são campos de configuração v2.

`HOME.bridge.enabled=true` exige uma seção com `id: "online"` em `HOME.sections`.
Sem ela, a geração falha com erro claro antes de modificar a saída, em vez de
omitir a faixa solicitada. Ao remover `online`, defina também
`HOME.bridge.enabled=false`. Com `false`, a faixa fica desativada, com ou sem
`online`; os demais campos do objeto `bridge` continuam obrigatórios.

## Tokens explícitos

Cores `olive`, `dark`, `cream`, `beige`, `gold`, `ink`, `muted`, `line`, `white`,
`focus`: `#RRGGBB`. Famílias `serif` e `sans`: lista CSS de nomes de fontes,
sem regras arbitrárias. As famílias locais disponíveis são Playfair Display e
DM Sans, com Georgia/Arial como fallback. Outra família precisa estar disponível
no dispositivo ou ter integração local/licença preparada separadamente.
Dimensões `title-size`, `space-section`, `gutter`: valores em `px` ou `rem`.
Exemplo: `"TOKENS": {"olive": "#566744", "serif": "Georgia, serif"}`.
A configuração não aceita CSS arbitrário e não muda a composição da página.

## Migração de v1

O esquema com campos numerados do layout Retrato foi substituído. Não há renderer
v1 ou conversão silenciosa: use o exemplo v2 e transfira textos confirmados para
`HOME.sections`, perguntas para `HOME.faq`, contatos para `HOME.contacts`, foto
para `HOME.photo` e evidências autorizadas para as listas opcionais. Os campos
SEO de identificação e metadados conservam os mesmos nomes; remova as quatro
chaves legadas acima, inclusive quando vazias. O programa falha se receber configuração
sem `VERSAO=2`, antes de modificar a saída.

## Publicação

Somente depois de substituir todos os placeholders, confirmar dados e obter
aprovação visual, defina `MODO=publicado`, `URL_SITE` e os metadados. O gerador
preserva `seo.py`: canonical, Open Graph, Person/WebSite/WebPage, sitemap, robots e
headers para domínios técnicos. Não há deploy automático. Testes de produção usam
somente `example.org` em diretórios temporários; não publicam um perfil fictício.
