---
name: scheffer-sites
description: Método Scheffer Sites para planejar, criar, revisar, testar e publicar sites com foco em estratégia, UX/UI, copy, SEO, acessibilidade, QA e deploy seguro.
---

# Scheffer Sites Skill

Use esta skill para trabalho em sites produzidos pela Scheffer Sites ou quando o usuário solicitar aplicação do Método Scheffer Sites.

## Objetivo

Aplicar um processo crítico e reutilizável sem copiar mecanicamente decisões de projetos anteriores.

## Workflow

### 1. Entender o contexto
Identifique:

- objetivo do site;
- público;
- oferta;
- ação principal;
- ativos;
- restrições;
- dados confirmados;
- hipóteses;
- estado de publicação.

### 2. Classificar regras
Toda regra importante deve ser entendida como uma destas categorias:

- UNIVERSAL
- SCHEFFER SITES
- NICHO
- CLIENTE
- EXPERIMENTO

Nunca promover automaticamente uma decisão CLIENTE para UNIVERSAL.

### 3. Consultar referências
A skill deve funcionar de forma portátil em repositórios de clientes e templates.

Para trabalho normal, consulte primeiro as referências empacotadas com a própria skill:

- `references/core.md` para princípios operacionais e perguntas de revisão;
- `references/checklists.md` para pré-merge, pré-publicação e retrospectiva.

Quando o repositório central do Playbook também estiver realmente disponível no ambiente, use `docs/playbook/` para aprofundar contexto, decisões históricas e justificativas. Priorize os documentos pertinentes à tarefa, como estratégia, arquitetura da informação, UX/UI, copy, SEO, acessibilidade, performance, deploy, nichos regulados e QA.

Consulte `docs/playbook/decisions/` apenas quando esses arquivos estiverem presentes. Não assuma acesso ao Playbook central a partir de um repositório de cliente.

### 4. Antes de editar
Declare internamente:

- problema real;
- arquivos que precisam mudar;
- elementos que devem permanecer intactos;
- validação esperada.

Evite refatorações não solicitadas.

### 5. Durante a implementação

- não invente informações;
- preserve design aprovado;
- mantenha semântica HTML;
- trate mobile como experiência própria;
- proteja acessibilidade;
- mantenha preview e produção separados;
- mantenha assets-fonte e gerados com origem clara;
- prefira configuração explícita a edição manual de ambiente.


#### Templates reutilizáveis

Ao transformar um site aprovado em template, reaproveite a arquitetura da informação, os padrões de interação e os pontos de CTA como ponto de partida. Separe essa estrutura da identidade e das afirmações do cliente original.

- Configure textos, contatos e tokens visuais por projeto; não reutilize nome, fotos, credenciais ou serviços de outro cliente.
- Deixe métricas, depoimentos e serviços que dependam de elegibilidade ocultos por padrão. Exija informação confirmada e autorização quando aplicável.
- Valide campos opcionais e teste os estados sem conteúdo e com conteúdo configurado, além de verificar que não restaram dados do projeto de referência.
- Trate o template como estrutura inicial, ajustando jornada e direção visual ao próximo profissional. Não transforme decisões de um cliente em padrão do nicho.

### 6. SEO e publicação
Nunca use preview técnico como canonical por conveniência.

Antes de publicação definitiva, valide:

- domínio;
- canonical;
- indexação;
- sitemap;
- robots;
- headers;
- metadados;
- dados estruturados;
- links;
- assets.

### 7. Nichos regulados
Não trate memória como norma atual.

Pesquise fontes oficiais e atuais quando a tarefa depender de regras profissionais, legais ou de plataforma.

Não declare aprovação ou conformidade total sem base suficiente.

### 8. QA
Execute testes proporcionais ao risco.

Decisões de produto verificáveis e propensas a regressão devem receber teste quando possível.

Após mudança visual relevante, valide em navegador real quando disponível.

### 9. Encerramento
Relate:

- o que mudou;
- por que mudou;
- o que foi preservado;
- testes executados;
- limitações;
- pendências;
- novo aprendizado que deveria entrar no Playbook.

## Regra de ouro

Preserve o raciocínio, não apenas a solução anterior.
