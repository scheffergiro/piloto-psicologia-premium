> Arquivo histórico, fora do build v2. A única Home oficial usa `src/`,
> `cliente.json` v2 e `gerar.py`. Consulte o README da raiz.

# Modelo e direção visual ativos

Esta árvore contém os componentes e a direção padrão **Retrato em Contraponto**.
`gerar.py` combina esses arquivos com `cliente.json` e gera o site em `public/`.

## Limites desta fase

- `base.html` registra o shell e os pontos de montagem da página.
- `components/` receberá apenas fragmentos com contrato semântico, funcional ou
  comportamental compartilhado, e não micro-partials de apresentação.
- `directions/retrato/` implementa Retrato em Contraponto. `directions/caderno/`
  permanece reservada, sem implementação.
- `assets/` reserva assets compartilhados. CSS e JavaScript ficam junto aos
  componentes/direção que os utilizam.
- `prototypes/` é material de estudo e não é uma entrada desta arquitetura.

## Namespaces

Dados confirmados do cliente continuam usando `{{CAMPO}}`. Pontos internos de
montagem usam exclusivamente `[[SLOT:NOME_DO_SLOT]]`. O montador futuro deverá
resolver slots internos antes de substituir e escapar os dados do cliente, em
passagens distintas. Um valor de cliente nunca deve ser reinterpretado como slot.

O contrato de campos e critérios de nulabilidade está em `contracts.json`.
`cliente.json` é a fonte de conteúdo e cores; use informações confirmadas e não
transforme dados demonstrativos em fatos.

## Preview de Retrato

Execute `python3 gerar_retrato.py`. A montagem explícita combina `base.html`, os
componentes compartilhados e o corpo próprio da direção em
`preview/retrato/index.html`, copiando `retrato.css`. O diretório
`preview/` não faz parte da publicação da Cloudflare (`public/`) e a saída é
sempre marcada `noindex`, inclusive ao validar o estado publicado.

Para visualizar, execute `python3 -m http.server 8000` na raiz e abra
`http://localhost:8000/preview/retrato/`.

## Segunda fotografia de Retrato

`FOTO_ABORDAGEM` aceita um caminho seguro relativo a `templates/` e o gerador
copia o arquivo para o mesmo caminho em `preview/retrato/`. O texto alternativo
é configurado em `FOTO_ABORDAGEM_ALT`; deixe-o vazio somente quando a imagem for
decorativa. Sem o arquivo, a seção preserva a composição gráfica genérica.
