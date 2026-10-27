# Portabilidade da Home final

## Base e governança

Consumidor: `scheffergiro/template-landing-psicologia`. `main` remota confirmada em
`d0616d20ba7cd875ecf6169a2acc4a4838dd5465`, merge da PR #19. Checkout inicial limpo.
O proxy de rede do shell exigiu acesso de rede habilitado; antes disso, a base foi
lida pelo conector GitHub e materializada com árvore idêntica
`20986d8b57d0cbbca143a3b6538550387ea1bab4` e objeto de commit assinado idêntico.
O fetch posterior confirmou o mesmo SHA e recuperou o histórico completo.

Referência: `scheffergiro/demo-ilana-naves`, HEAD limpo em
`eaef856f5a998071115d73a98eb99bf2a2e8bfc8`. Lidas as fontes reais `src/home.html`,
`src/styles.css`, `src/motion.js`, `scripts/home.py`, `scripts/contact.py`, os
relatórios de Hero/encaixe e as descrições das PRs #10 e #11. O ajuste final da
foto desktop, incluindo o limite `470.96px` e o fator responsivo `.80185`, está
preservado. Não se usou o protótipo de exploração como renderer.

A direção fixa é requisito deste template (decisão do consumidor); conteúdo
clínico, contatos e permissões de atendimento continuam específicos de cada
profissional. As skills locais Scheffer Sites e CodeMakers foram consultadas na
revisão já empacotada, sem sincronização, atualização ou adoção de novo lock.
Playbook, Starter e o conteúdo versionado da Ilana não foram modificados.

## Componentes e arquivos

| Fonte de referência | Destino e adaptação |
| --- | --- |
| `src/home.html` | `src/home.html`: mesmo Hero, cabeçalho, skip link e rodapé; identidades, textos e menus configuráveis |
| `src/styles.css` | `src/styles.css`: cascata consolidada e breakpoints preservados; `.aflorar` vira `.recurso`; apêndice limitado a estados reutilizáveis |
| `src/motion.js` | `src/motion.js`: bytes preservados, mesma abertura/revelações e cancelamentos |
| Script inline de navegação | `src/navigation.js`: extraído sem alteração de comportamento |
| `scripts/home.py → values` | `scripts/home.py`: mesma montagem das seções e grades; retirados dados da cliente, quantidades fixas e obrigatoriedade de seções |
| `scripts/contact.py` | `scripts/contact.py`: mesmos SVGs; URL/mensagem únicas; destino/rótulos configuráveis; sem contato, seta genérica e seção informativa |
| Fontes locais e OFL | `src/assets/fonts/`, copiadas pelo build com suas licenças |
| Fundação do template | `gerar.py` integra a Home e mantém `seo.py`; `gerar_retrato.py` delega ao gerador único |
| Dados e exemplos | `cliente.json`, `examples/clara.json`, `examples/alexandre.json`, `examples/geometria.json` |
| Segurança/configuração | `scripts/config.py`: validação v2, URLs, tokens e assets; manifesto de saída sem travessia, symlinks ou hard links |
| Artefatos | `public/index.html`, CSS/JS, fontes/licenças, SEO e `.generated-files.json`; remoção do CSS Retrato obsoleto |
| Regressões e prova | `tests/`, `scripts/prepare_visual_qa.py`, `scripts/qa_browser.py`, `docs/VISUAL_QA.md` e `docs/visual/` |

A foto pessoal, CRP, contatos, textos específicos, abordagem da Ilana e conteúdo
do e-book não integram os dados nem os assets do template. `exterior` e `recurso`
ficam ausentes por padrão. Métricas e depoimentos continuam opcionais, agora com
listas sem quantidade fixa; depoimentos exigem autorização e fonte explícitas.

## Ajustes restritos à reutilização

- Reserva de retrato na proporção 682/863, sem imagem inventada de profissional.
- Nomes acima de 30 caracteres têm escala menor; spans mantêm quebras editoriais
  configuráveis e admitem reflow. Não se introduz outra composição de Hero.
- Navegação e rodapé derivados das seções existentes; FAQ não deixa âncora órfã.
- Sem recurso editorial antes do FAQ, recupera-se o padding normal; com recurso,
  mantém-se o espaçamento curto e a divisória da referência.
- Sem contatos, flutuante e ações externas ficam ausentes; botões iniciais levam
  às informações de contato, e a seção não contém um botão de autorreferência.
- Faixa de destaques admite lista variável; listas vazias não geram a seção.

## Permissões e recursos

A reutilização do código visual é o objeto da autorização expressa deste pedido.
Não foi atribuída uma licença externa ao código sem evidência. Os SVGs foram
conferidos no `scripts/contact.py` e na decisão de origem 003 da referência; ela
registra autorização do solicitante e ausência de biblioteca externa identificada.
Isso não equivale a uma avaliação jurídica de marcas.

Playfair Display e DM Sans têm licença **SIL Open Font License 1.1**, lida e
incluída integralmente. Arquivos originais sem modificação, conversão ou subset.
Origem documentada na referência: repositório público `google/fonts`, diretórios
`ofl/playfairdisplay` e `ofl/dmsans`. Git blobs verificados:

| Arquivo | Blob SHA-1 |
| --- | --- |
| `PlayfairDisplay.ttf` | `7a09eb71f10622fd083134ac9ed46f59b21bee18` |
| `DMSans.ttf` | `c672f98060af9b2c85fca704ebd5ad9a8717c1df` |
| `PlayfairDisplay-OFL.txt` | `13153890847ba9bde8a852596d1515261156e474` |
| `DMSans-OFL.txt` | `4430b85ac62998e2edb914360f9ebdfe43f4deaa` |

`src/assets/reserva.png` é um desenho geométrico sintético produzido nesta tarefa
para verificar enquadramento, sem fotografia ou identidade de uma pessoa. Apenas
`examples/geometria.json` o ativa. O build copia somente assets declarados e as
quatro fontes/licenças conhecidas. Não redistribui skills externas.
