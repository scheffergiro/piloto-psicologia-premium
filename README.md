# Template Premium de Psicologia 2.0

Home estática reutilizável, portada diretamente da composição final aprovada da
Ilana (`eaef856f5a998071115d73a98eb99bf2a2e8bfc8`, PRs #10 e #11).
A configuração padrão usa **Clara Beatriz Ramos, personagem fictícia**, sem foto,
credenciais ou contatos reais. Não recebe solicitações de atendimento.

```bash
python3 -B gerar.py
python3 -m http.server 8000 --directory public
python3 -B -m unittest discover -s tests -v
```

Abra `http://localhost:8000`. O gerador não publica o site. A saída versionada
`public/` continua sendo o diretório entregue à hospedagem Cloudflare existente.

A personalização diária é feita no JSON. Não edite o HTML/CSS de saída.
`gerar.py` é a única implementação oficial; `gerar_retrato.py` mantém apenas uma
função de compatibilidade que delega ao mesmo gerador. `templates/`, `template.html`
e `prototypes/` são estudos históricos fora do build; não são direções alternativas
oficiais nem devem ser usados para gerar novos leads.

- [Campos, exemplos e migração para v2](docs/CONFIGURACAO.md)
- [Origem dos componentes, arquivos e licenças](docs/PORTABILIDADE.md)
- [QA, capturas e comparação com referência sintética](docs/VISUAL_QA.md)

Dois perfis inteiramente fictícios:

```bash
python3 -B gerar.py --config examples/clara.json --output preview/clara
python3 -B gerar.py --config examples/alexandre.json --output preview/alexandre
python3 -B gerar.py --config examples/geometria.json --output preview/geometria
```

O terceiro exemplo ativa seções opcionais e uma **reserva geométrica de retrato**
para comparar proporções; não é fotografia de uma pessoa. O padrão não ativa
atendimento no exterior, recurso editorial, métricas ou depoimentos.

`MODO=demo` mantém `noindex,nofollow`, headers de preview e ausência de canonical,
sitemap e JSON-LD profissional. `MODO=publicado` exige conteúdo revisado, metadados
e domínio definitivo; rejeita placeholders e perfis fictícios. Nenhum comando
efetua deploy, envio de mensagens, merge ou adoção de skills/locks.

Após alterar fontes ou configuração, execute `python3 -B gerar.py` antes da suíte.
O teste de sincronização compara **todo o conjunto e os bytes** de `public/` com
uma geração nova, incluindo fontes, licenças, scripts, CSS e manifesto de assets.
