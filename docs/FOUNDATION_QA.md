# Fundação técnica — issue #18

Escopo: sincronizar saída, assets CSS, navegação progressiva e contatos do gerador
existente, sem portar ainda o visual da Ilana. A próxima etapa usará somente a
Home final `eaef856f5a998071115d73a98eb99bf2a2e8bfc8`, sem Heroes alternativos.

## Alterações

- `public/` regenerado, incluindo `assets/retrato.css`, sem alterar hospedagem.
- Teste compara HTML, CSS, robots e headers versionados com a geração.
- Navegação visível sem JS; toggle instalado somente após ativação do script.
- Links do menu fechado ficam fora da navegação por teclado via `hidden`.
- Flutuante é link nativo com o mesmo destino/mensagem dos demais CTAs.
- Sem número, link aponta para contato; JS pode abrir aviso demonstrativo.
- Publicação sem número oculta o flutuante e remove o aviso de demonstração.
- Configuração inválida preserva os arquivos de saída no cenário testado.

## Verificações executadas em 23/10/2026

- `python -B gerar.py`: geração concluída.
- `python -B -m unittest discover -s tests`: 29 testes passaram.
- `git diff --check`: passou.
- Chromium via HTTP local, JS habilitado/desabilitado: 14 cenários nas viewports
  320×740, 390×844, 768×900, 1080×768, 1081×900, 1366×768 e 1440×900.
- Sem overflow horizontal ou erros JS; menu abre/fecha, Escape retorna foco;
  sem JS, navegação disponível e flutuante aponta para `#contato`.
- Com JS, aviso demonstrativo abre/fecha e retorna foco ao acionador.
- Capturas do topo inspecionadas em 390 e 1440 px, com fontes de fallback.

Limites: requisições externas bloqueadas durante o QA, sem abrir contatos reais.
Não é revisão tipográfica final, comparação com Ilana, auditoria WCAG completa,
validação de outros motores, dispositivos físicos ou headers na hospedagem.
Nenhuma publicação ou merge foi executado. Playbook, Ilana, Starter, skills e
locks não foram alterados. Não houve adoção de revisão metodológica nova.
