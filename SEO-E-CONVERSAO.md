# Padrão de SEO e conversão para as próximas entregas

## O que esta base já faz

- HTML completo no servidor, legível mesmo sem executar JavaScript.
- Um H1; H1, título da aba, descrição e chamada principal configuráveis por cliente.
- Título e descrição exclusivos: SEO_TITULO e SEO_DESCRICAO.
- URL canonical absoluta no domínio final (URL_SITE), no modo publicado.
- robots.txt e sitemap.xml coerentes com o modo da página.
- Prévia comercial com noindex no HTML e no cabeçalho HTTP. Não bloqueamos rastreamento no robots.txt, pois o Google precisa ler o noindex.
- Open Graph para apresentação dos links compartilhados. É apresentação social, não uma garantia de ranking.
- JSON-LD Person, WebSite e WebPage no modo publicado, derivado do conteúdo real.
- Foto principal com dimensões, alt editável, prioridade alta e espaço reservado para evitar deslocamento de layout.
- Fontes carregadas por stylesheet e preconnect em vez de @import, mantendo display=swap.
- Sem bibliotecas de ícones, framework ou rastreadores adicionados.

## Configuração de cada cliente

Preencher em cliente.json:

- MODO: demo por padrão. Usar publicado somente após aprovação e revisão do conteúdo.
- URL_SITE: origem HTTPS definitiva, por exemplo https://dominio-da-cliente.com/. Não incluir caminho, parâmetros nem fragmento.
- SEO_TITULO: nome + serviço e/ou região/modalidade realmente atendida. Escrever de forma clara, sem repetir palavras para tentar manipular resultados.
- SEO_DESCRICAO: resumo próprio da profissional, público, modalidade/localidade e convite útil. O Google pode gerar outro trecho; não há limite de caracteres que garanta a exibição integral.
- HERO_TITULO e HERO_DESTAQUE: explicar o atendimento logo no começo, preservando o tom acolhedor. Não depender apenas de uma frase abstrata.
- CTA_PRINCIPAL: ação clara, como “Consultar disponibilidade”.
- IMAGEM_SOCIAL e IMAGEM_SOCIAL_ALT: opcionais; URL HTTPS de imagem autorizada e texto alternativo. A foto de compartilhamento precisa estar acessível publicamente.
- BIO_1/BIO_2, formação, abordagem, público e contatos: confirmados com a profissional.

Execute python3 gerar.py e versione os arquivos gerados de public/. A Cloudflare está configurada para servir essa pasta com exit 0; ela não executa o gerador automaticamente. Mudar somente o JSON sem gerar novamente não altera o site. O assistente pode executar essa etapa em cada edição.

O gerador rejeita o modo publicado sem domínio/título/descrição e com os marcadores provisórios mais comuns. Essa validação é limitada e não substitui a revisão humana: campos vazios, dados incorretos ou placeholders diferentes ainda precisam ser identificados na revisão.

No modo publicado, os avisos de demo são retirados. O botão WhatsApp é escondido se o número ainda estiver vazio. Sem foto, permanece a composição com iniciais, sem anúncio de foto pendente. Para atendimento exclusivamente online, deixar os três campos ENDERECO_* vazios remove o bloco de endereço.

## O que depende de trabalho específico para cada cliente

1. Entender o serviço, público e localidades reais; escolher os termos a partir da intenção de busca.
2. Criar conteúdo útil e original. Não publicar cópias que só trocam nome/cidade ou páginas artificiais para bairros onde não há atendimento.
3. Mostrar identidade, formação e registro confirmados. Textos de saúde precisam de revisão da profissional; evitar promessas de cura e resultados garantidos.
4. Se existir consultório elegível, organizar o Perfil da Empresa no Google com nome, endereço, telefone, horários e URL consistentes. Não criar endereço fictício para profissionais exclusivamente online.
5. Acrescentar LocalBusiness somente quando houver informações reais, visíveis e suficientes sobre o estabelecimento. O template não inventa endereço, horários, notas ou avaliações e não promete estrelas/FAQ nos resultados.
6. Quando houver vários serviços com conteúdo suficiente, avaliar páginas próprias. Uma landing page não cobre automaticamente todas as pesquisas de uma especialidade.

## Publicação e migração

### Publicação inicial

- Aprovar conteúdo e imagens e confirmar os links de contato.
- Definir uma versão oficial de domínio (com ou sem www) e redirecionar as alternativas quando aplicável.
- Configurar MODO=publicado e o domínio correto, gerar e revisar HTML, canonical, sitemap e cabeçalhos reais.
- O _headers gerado mantém os endereços pages.dev fora da indexação quando o domínio definitivo é próprio. Se pages.dev for explicitamente o domínio final, somente os endereços de preview por versão/branch permanecem bloqueados.
- O sitemap tem somente a página real, sem âncoras #sobre e #contato tratadas como páginas distintas.
- Verificar e testar o site em celular e computador, teclado, formulário se houver, WhatsApp e Instagram. Medir performance com PageSpeed Insights e corrigir problemas encontrados.

### Migração de domínio ou substituição de site

1. Confirme os domínios de origem e destino, os acessos administrativos e quais propriedades do Search Console estão verificadas.
2. Faça um inventário de URLs antigas a partir de sitemaps, páginas relevantes, tráfego e links externos. Mapeie cada URL para o conteúdo equivalente no site novo.
3. Não envie em massa URLs sem relação para a página inicial. Para conteúdo removido sem substituto adequado, avalie respostas 404 ou 410. Um redirecionamento para a homepage pode ser uma decisão específica, não um padrão.
4. Configure redirecionamentos permanentes do lado do servidor (301 ou 308) diretamente ao destino final. Evite cadeias.
5. Teste a resposta HTTP, não apenas a aparência em uma aba anônima. Confira status, cabeçalho Location, destino final e número de saltos para:
   - HTTP e HTTPS;
   - domínio com e sem www;
   - homepage;
   - caminhos antigos relevantes, inclusive os que aparecem em sitemap ou recebem links.
6. Verifique no Search Console as propriedades e variantes antigas e novas necessárias. Em mudança de domínio, use a ferramenta Alteração de endereço no site antigo quando aplicável e siga os requisitos atuais da ferramenta. Ela complementa os redirecionamentos e não garante indexação nem prazo.
7. Envie o sitemap do site novo e monitore indexação e tráfego nos domínios antigo e novo. Atualize links próprios, perfis, campanhas e, quando viável, links externos importantes.
8. Planeje a duração antes de cancelar serviços. O Google recomenda manter os redirecionamentos por pelo menos 180 dias; a documentação geral de migração recomenda um ano ou mais. Manter o domínio antigo registrado também reduz o risco de outra pessoa adquiri-lo.
9. Confirme com a cliente o que ocorre se hospedagem, DNS ou domínio antigo expirarem. O redirecionamento depende de o domínio continuar registrado e de um serviço continuar recebendo e encaminhando as requisições. Se a cliente decidir não renovar, registre a data e o impacto da interrupção.

Uma regra de hospedagem pode interagir com recursos de SSL ou com outra regra de redirecionamento. Se o Search Console reprovar uma validação, compare as respostas HTTP e HTTPS e investigue a configuração real do provedor. Não desligue SSL como passo padrão; qualquer ajuste precisa preservar TLS válido e ser testado em todos os protocolos.

## Conversão e acompanhamento

SEO atrai visitantes; conversão depende de clareza, confiança e facilidade de contato.

Priorizar: serviço/modalidade/localidade claros no primeiro bloco, CTA compreensível, boa leitura mobile, contato fácil, carregamento leve e informações profissionais verificadas.

Após publicar, acompanhar:
- Search Console: impressões, cliques, consultas e taxa de cliques orgânicos.
- Métricas do site, quando configuradas: visitas e cliques de contato.
- Processo comercial da profissional: contatos recebidos e agendamentos.

Cliques no WhatsApp não equivalem a mensagens enviadas nem a consultas marcadas. Não enviar nomes, mensagens, sintomas ou outras informações sensíveis de pacientes para ferramentas de analytics. Definir a medição e eventuais necessidades de consentimento conforme a implementação escolhida; nenhum rastreador foi instalado por este template.

## Limites da entrega

Base técnica não garante indexação, primeiro lugar, rich results, prazo de posicionamento ou aumento de pacientes. Não existe “nota de SEO” que comprove resultados comerciais. Performance e acessibilidade precisam de teste no site final e os resultados orgânicos precisam de acompanhamento.

## Referências oficiais

- https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=pt-br
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- https://developers.google.com/search/docs/appearance/structured-data/sd-policies
- https://developers.google.com/search/docs/appearance/structured-data/local-business
- https://support.google.com/business/answer/7091?hl=pt-BR
- https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes?hl=pt-br
- https://support.google.com/webmasters/answer/9370220?hl=pt-br
