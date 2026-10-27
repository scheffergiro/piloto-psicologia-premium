# QA e comparação visual — 23/10/2026

**Aguardando avaliação visual do solicitante. Sem merge automático.**

Referência congelada: `demo-ilana-naves@eaef856f5a998071115d73a98eb99bf2a2e8bfc8`,
incluindo PRs #10 e #11. A comparação usa o HTML/CSS/renderer originais dessa
revisão com conteúdo sintético de comprimento comparável. O script substitui
somente dados e strings de identidade na cópia de QA; não altera o repositório
de referência. Não coloca a foto, contatos ou textos pessoais da cliente na
entrega. O desenho de reserva tem a mesma proporção 682/863 da foto de referência.

## Capturas para avaliar

| Estado | Desktop 1440×900 | Mobile 390×844 |
| --- | --- | --- |
| Demo padrão, sem foto | [Hero](visual/default-hero-1440.png) · [Página completa](visual/default-1440.png) | [Hero](visual/default-hero-390.png) · [Página completa](visual/default-390.png) |
| Referência final com dados sintéticos | [Hero](visual/reference-hero-1440.png) · [Página completa](visual/reference-1440.png) | [Hero](visual/reference-hero-390.png) · [Página completa](visual/reference-390.png) |
| Template com fixture equivalente | [Hero](visual/equivalent-hero-1440.png) · [Página completa](visual/equivalent-1440.png) | [Hero](visual/equivalent-hero-390.png) · [Página completa](visual/equivalent-390.png) |
| Segundo perfil: nome longo, seções removidas | [Hero](visual/second-hero-1440.png) | [Hero](visual/second-hero-390.png) |

Para consulta da referência original e suas evidências aprovadas, ver
[PR #10](https://github.com/scheffergiro/demo-ilana-naves/pull/10) e
[PR #11](https://github.com/scheffergiro/demo-ilana-naves/pull/11).

## Comparação medida

Chromium headless, HTTP local, fontes locais carregadas, movimento reduzido,
sem ocultar conteúdo ou alterar a altura da viewport. Valores abaixo coincidem
entre referência sintética e template equivalente:

| Viewport | Altura do Hero | Retrato (largura × altura) | Final do CTA |
| --- | --- | --- | --- |
| 320×740 | 974,0 | 246,4 × 311,8 | 1016,5 |
| 390×844 | 1021,7 | 308,0 × 389,7 | 1064,2 |
| 768×900 | 715,4 | 338,9 × 428,9 | 758,1 |
| 1366×768 | 707,0 | 471,0 × 595,9 | 755,8 |
| 1440×900 | 750,5 | 471,0 × 595,9 | 799,3 |
| 1280×720 | 687,4 | 433,0 × 547,9 | 736,1 |

- Geometria de Hero, nome, retrato e CTA: maior diferença medida **0 CSS px**
  em x/y/largura/altura nas seis viewports com a fixture equivalente.
- Nome, retrato e CTA: famílias/tamanhos tipográficos, cores, fundos, bordas,
  raios e sombras computados coincidem nos mesmos cenários.
- Alturas das seções reutilizáveis até o FAQ coincidem, após correção do
  espaçamento indevido quando `recurso` está presente.
- `motion.js` é idêntico byte a byte ao da revisão final.
- [Matriz bruta](visual/qa.json) · [Diferenças medidas](visual/comparacao.json).

Não se declara igualdade de pixels. A referência sintética conserva o menu
hardcoded da matriz e alguns botões/links de contato de seu renderer original;
o template os deriva da configuração e remove canais ausentes. Por isso o
rodapé e a altura da seção de contato podem diferir. Na comparação mobile, a
remoção dos botões de contato sem destino reduz a seção em 150 px; é intencional.
A seta genérica no CTA sem WhatsApp também substitui intencionalmente seu ícone,
com a mesma dimensão. Não se inventou número para igualar a imagem.

O conteúdo sintético tem quebras próprias: em 1280×720, o CTA termina abaixo da
dobra **tanto na referência sintética quanto no template**, ao contrário da
medição com os textos originais da Ilana. Não se comprimiu o layout para produzir
um resultado artificial. No mobile, o CTA exige rolagem, como na composição final
aprovada. Nomes longos usam escala menor e podem acrescentar linhas.

Inspecionadas visualmente as capturas desktop e mobile do padrão, as páginas
completas equivalentes e a composição do segundo perfil. Hero, retrato acima do
nome no mobile, hierarquia, grids, faixas, divisórias, botões e rodapé preservam
a direção aprovada. Isso é evidência de implementação, não aprovação estética.

## Verificações executadas

- **37 testes Python**: modos demo/publicado, canonical/sitemap/headers/JSON-LD,
  escaping, configuração inválida preservando a saída, URLs, tokens, isolamento
  A→B→A, reprodutibilidade, conjunto completo de arquivos versionados, alt,
  assinatura de imagem, travessia, symlinks/hard links e manifesto de saída.
- **39 cenários Chromium**: 24 renderizações (quatro perfis × seis viewports),
  12 cenários sem JS e três cenários de movimento/foco/âncora/recarga.
- Nas três configurações geradas: sem overflow horizontal, imagem quebrada,
  âncora órfã ou erro JavaScript nas viewports medidas. Fontes locais carregadas.
- Menu por teclado abre/fecha; Escape devolve foco. Skip link transfere foco ao
  conteúdo. FAQ opera por Enter. Sem JS, menu e conteúdo continuam disponíveis.
- Movimento normal inicia a abertura; foco e preferência reduzida dinâmica
  cancelam animações; navegação/recarga em âncora não repete abertura do Hero.
  O QA aguarda o cancelamento observável, evitando depender de pausa fixa de 100 ms.
- `node --check` nos dois scripts de UI e `git diff --check`: passaram.
- Assets pessoais ausentes do conteúdo/saída; hashes das fontes/licenças
  conferidos; Ilana e Playbook permanecem com árvores de trabalho limpas.

## Reproduzir

Build e testes não exigem dependências Python externas. QA de navegador opcional
usa Playwright e Chromium já instalados no ambiente desta execução; esses itens
não integram o runtime do site nem alteram locks.

```bash
python3 -B gerar.py
python3 -B -m unittest discover -s tests -v
python3 -B scripts/prepare_visual_qa.py --reference /caminho/demo-ilana-naves
python3 -m http.server 8765 --bind 127.0.0.1 --directory preview/visual/web
# Em outro terminal:
python3 -B scripts/qa_browser.py --url http://127.0.0.1:8765
```

A preparação exige referência limpa no SHA exato. Lê os arquivos e não executa
o gerador nem modifica Git/fontes da Ilana. As cópias e capturas novas ficam em
`preview/visual/`, ignorado pelo Git. Sirva apenas o diretório web de QA.

## Revisão pontual de configuração da PR #20

A estratégia de portabilidade visual foi aprovada pelo solicitante. Esta revisão
altera somente o contrato de configuração, sem modificar design ou composição.
Baseline da comparação antes/depois: commit
`ee66e8313c3162c3ffd6fd4b0381499b26957a6f` da própria PR.

- Removidos `WHATSAPP`, `WHATSAPP_MENSAGEM`, `INSTAGRAM_URL` e `FOTO` do nível
  principal de `cliente.json` e dos três exemplos. A validação rejeita essas
  chaves mesmo vazias e indica o caminho correspondente em `HOME`.
- Preservado o adaptador interno de SEO: número/mensagem, Instagram e fotografia
  continuam derivados exclusivamente de `HOME`. Teste de produção verifica
  os adaptadores, os links e os campos `sameAs`/`image` do JSON-LD.
- `HOME.bridge.enabled=true` sem seção `online` agora falha explicitamente,
  antes de alterar a saída. Testados ativação com `online`, desativação com e
  sem `online`, erro de inconsistência e preservação da saída anterior.
- **42 testes Python passaram**, incluindo sincronização integral de `public/`,
  os cinco novos testes e o caso de seções removidas com bridge explicitamente
  desativada. `git diff --check` passou.
- Regenerados os quatro perfis (`cliente.json`, Clara, Alexandre e geometria):
  **45 arquivos de saída idênticos byte a byte** aos anteriores, conferidos por
  SHA-256, incluindo HTML, CSS, scripts, fontes, licenças, imagem e metadados.
- **16 comparações Chromium antes/depois** (quatro perfis × 320×740, 390×844,
  768×900 e 1440×900), via HTTP local e movimento reduzido: todos os retângulos
  medidos do conteúdo/cabeçalho/rodapé e as capturas completas (SHA-256) ficaram
  idênticos, sem overflow horizontal. As capturas já versionadas permanecem
  válidas e não foram substituídas.

Nenhuma alteração em `src/`, `public/`, renderer, `seo.py`, fontes, botões,
ícones ou animações. Playbook, Ilana, Starter, skills e locks não foram
modificados. Mudanças mantidas na mesma branch e PR #20, sem merge.

## Limitações

Chromium headless local; sem dispositivos físicos, outros motores, leitor de
tela, auditoria WCAG completa, teste de headers na hospedagem ou benchmark de
performance. A checagem de imagem é de assinatura/tamanho, não decodificador ou
scanner. Contatos não foram acionados externamente. Configurações v1 precisam
ser migradas para o esquema documentado; não há conversão silenciosa.
Nenhuma demo real, publicação definitiva, merge ou adoção metodológica nova.
