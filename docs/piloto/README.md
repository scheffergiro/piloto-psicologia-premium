# Piloto operacional — Helena Duarte Reis

Demo independente, inteiramente fictícia, do Template Premium de Psicologia 2.0. Não representa uma profissional real, não recebe solicitações e não foi publicada como site oficial. Aprovação visual humana e merge ficam com o solicitante.

## Origem e integridade

Verificação remota pelo conector GitHub em 27/10/2026:

- Template: `scheffergiro/template-landing-psicologia`, main `53c4016cb0a8071f5b4db5bc91ba833d6b98eeb4`, merge da [PR #20](https://github.com/scheffergiro/template-landing-psicologia/pull/20).
- Piloto: `scheffergiro/piloto-psicologia-premium`, main inicial `2e604fe1289d2e2b1f95f118e3919a2d86fd3674`.
- Ambos têm a árvore `53a1aa6c909fd9c21f4c6707f3963268087ab0b8`: os 135 arquivos, caminhos, modos e hashes Git blob coincidem. A árvore local também foi conferida. Históricos independentes; não se trata de um fork com ancestralidade compartilhada.
- Após personalizar, 133 dos 135 arquivos originais permanecem byte a byte iguais. Mudaram somente `cliente.json` e o `public/index.html` gerado. Documentação e evidências foram acrescentadas nesta pasta.
- `src/`, geradores, testes, CSS, JavaScript, fontes, licenças, skills e demais arquivos originais intactos. O template remoto recebeu apenas consultas.

[Auditoria e hashes SHA-256 de public/](integridade.json).

## Configuração

O único arquivo de configuração alterado é [`../../cliente.json`](../../cliente.json).

- Identidade: Helena Duarte Reis, personagem fictícia; nome curto e três linhas editoriais próprios.
- Apresentação, temas ilustrativos, quatro seções, percurso em três etapas, faixa editorial e quatro FAQs personalizados.
- “Escuta em contexto” é uma abordagem inventada **apenas para layout**, explicitamente identificada como tal; não é modalidade terapêutica ou credencial.
- `TOKENS: {}` mantém paleta, tipografia e dimensões padrão da referência portada da Ilana. Nenhum componente foi redesenhado.
- `HOME.photo.file: ""` usa a reserva editorial nativa com iniciais HR. Nenhuma fotografia de pessoa real foi adicionada.
- `HOME.whatsapp.number: ""`, `HOME.contacts: []`, sem métricas, depoimentos ou avaliações.
- O esquema exige `CRP` como texto não vazio. Foi usado **“Personagem fictícia · sem registro profissional”**, sem número ou registro inventado.
- CTAs sem destino usam o rótulo configurável `fallback_cta` e levam a `#contato`, onde estão os limites da demo. Não existe canal externo nem botão flutuante de WhatsApp.
- `MODO: "demo"`, URL definitiva vazia, noindex/nofollow no HTML e em `_headers`, sem canonical, sitemap ou JSON-LD profissional.

## Capturas e inspeção visual

Capturas com fontes carregadas e movimento reduzido, para comparar estados estáveis:

| Visão | Desktop 1440×900 | Mobile 390×844 |
| --- | --- | --- |
| Página completa | [Demo desktop](demo-1440.png) | [Demo mobile](demo-390.png) |
| Primeira dobra | [Hero desktop](demo-hero-1440.png) | [Hero mobile](demo-hero-390.png) |
| Template antes da personalização | [Baseline desktop](baseline-hero-1440.png) | [Baseline mobile](baseline-hero-390.png) |
| CTA em hover | [Desktop](hover-1440.png) | [Mobile](hover-390.png) |
| Destino do CTA | [Contato desktop](contato-1440.png) | [Contato mobile](contato-390.png) |

[Menu mobile aberto e foco visível](menu-390.png).

Inspeção das páginas completas, dos Heroes e do menu: composição editorial, hierarquia serifada/sans, alternância de fundos, divisores, sombras da reserva, botões e empilhamento preservados; sem sobreposição ou cortes de conteúdo observados. O nome novo e os textos mudam as quebras e alturas da página, como esperado. Não há alegação de identidade de pixels com a cliente Ilana ou de equivalência estética já aprovada pelo solicitante.

Na primeira dobra de 390×844, a reserva vem antes do nome, e descrição/CTA exigem rolagem. Isso já ocorre na configuração padrão do template; não foi redesenhado neste piloto. As medições de Hero e retrato, incluindo os estilos computados, ficam em `qa.json`; dimensões fixas do retrato e estilos coincidem com a baseline nas seis larguras. A altura do Hero em telas estreitas varia com o conteúdo.

## Validação executada

- **42/42 testes Python aprovados**, incluindo sincronização de todo `public/`, validação, escaping, segurança de assets, SEO demo/produção simulada e isolamento entre perfis. [Log](testes.txt).
- **14 cenários Chromium aprovados**, executados especificamente nesta demo: seis viewports (320×740, 390×844, 768×900, 1280×720, 1366×768 e 1440×900); quatro cenários sem JS; três cenários de movimento/histórico; um sem APIs opcionais. [Resultados completos](qa.json) · [Script reproduzível](qa.py).
- Sem overflow horizontal, imagens quebradas, âncoras órfãs, erros JavaScript ou respostas HTTP >=400 nos seis cenários principais. Fontes locais carregadas, um H1, metadados demo e ausência de links externos conferidos.
- Menu por teclado, Escape e retorno de foco; fechamento ao navegar; skip link; FAQ abre/fecha por teclado; CTA chega a `#contato`.
- Entrada do Hero, cancelamento por foco, movimento reduzido dinâmico, revelação de scroll sem repetição, âncora profunda/recarga, Início/recarga e Voltar/Avançar verificados.
- Nova geração em diretório temporário tem exatamente o mesmo conjunto de arquivos e bytes de `public/`. Todos os assets gerados mantidos; ausência de sitemap e de foto pessoal confirmada.
- Varredura de todo `public/` para nomes/contatos conhecidos dos exemplos e de clientes anteriores: nenhuma ocorrência. Lista e resultados em `integridade.json`. A documentação histórica herdada pode citar projetos de origem; isso não é conteúdo distribuído no site.
- `node --check src/motion.js`, `node --check src/navigation.js` e `git diff --check` passaram.

## Reproduzir

Na raiz do piloto, com Python 3.9+:

```bash
python3 -B gerar.py
python3 -B -m unittest discover -s tests -v
```

Para QA opcional, é necessário Playwright Python e Chromium em `/usr/bin/chromium`, disponíveis no ambiente utilizado. Não são dependências do site. Preparar baseline da revisão original e servir somente localmente:

```bash
mkdir -p preview
git show 2e604fe1289d2e2b1f95f118e3919a2d86fd3674:cliente.json > preview/pilot-baseline.json
python3 -B gerar.py --config preview/pilot-baseline.json --output preview/pilot-baseline
python3 -m http.server 8765 --bind 127.0.0.1
```

Em outro terminal:

```bash
python3 -B docs/piloto/qa.py
```

## Dificuldades e limites

1. A personalização funcional exigiu apenas editar o JSON e executar o gerador, sem mudanças manuais de HTML/CSS/JS. O renderer impõe ordem/IDs de seções e campos obrigatórios; os exemplos e `docs/CONFIGURACAO.md` foram suficientes para este perfil.
2. O campo CRP obrigatório não possui um estado estruturado “ausente”; a identificação demonstrativa em texto resolveu o piloto sem inventar credencial.
3. Na primeira execução, três testes de produção simulada falharam: a fixture limpa `fictícia` em minúsculas, mas não `FICTÍCIA`. Os rótulos editoriais foram ajustados no JSON para `DEMONSTRATIVA`; a condição fictícia continua explícita no perfil. Nenhum teste ou gerador foi alterado.
4. A comparação inicial de QA tentou exigir a mesma altura do Hero com textos diferentes. O critério foi corrigido para comparar estilos e dimensões fixas, mantendo as alturas reais registradas. Transições CSS de foco também foram distinguidas da animação de entrada do Hero no teste.
5. O proxy do terminal recusou a conexão Git. Origem, main remota e entrega foram tratados pelo conector GitHub; isso não indica falha de autenticação. O sandbox bloqueou sockets do servidor/navegador; a execução local foi autorizada pelo ambiente, sem deploy público.
6. QA em Chromium headless local. Sem dispositivos físicos, Firefox/WebKit, leitor de tela, auditoria WCAG integral, benchmark de performance ou verificação de headers reais em hospedagem. `_headers` foi validado como artefato; o servidor Python não o aplica.
7. A comparação é com o template pós-merge confirmado, que já porta a referência Ilana; não foi necessário acessar ou redistribuir conteúdo pessoal da cliente. A manutenção técnica do acabamento está demonstrada; a aprovação estética permanece humana.

Skills locais `scheffer-sites` e `codemakers-design` consultadas conforme AGENTS.md. Playbook central `c058ebeb3065e9200717720ee7bf1201a811694d` consultado somente para contexto de QA/fluxo, sem adoção de nova revisão, cópia, atualização de skills ou locks. Nenhum aprendizado foi gravado no Playbook. Possível melhoria futura para avaliação: tornar as fixtures de produção independentes da capitalização do conteúdo fictício.
