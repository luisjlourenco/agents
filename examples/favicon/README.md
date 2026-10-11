# Favicon oficial RD Station

Kit do agente [Favicon Identity Specialist](../../design/design-favicon-identity-specialist.md): troca o favicon de sites e ferramentas criados no Manus (ou em Vite, Next.js e HTML puro) pelo ícone oficial RD Station e ajusta os textos de identidade para busca, abas, favoritos e celular.

## O ícone

Símbolo RD Station navy `#002233` centralizado em quadrado ciano `#00DBFF`, ocupando cerca de 63% da altura. O vetor-mestre (`master/rd-station-icon.svg`) foi reconstruído a partir do traçado oficial do logo e conferido contra o ícone de referência (diferença média de 3 em 255 por pixel, só no serrilhado das bordas).

| Arquivo-mestre | Uso |
|---|---|
| `master/rd-station-icon.svg` | Ícone padrão (origem de todos os tamanhos) |
| `master/rd-station-icon-maskable.svg` | Android adaptável: símbolo a 55% da altura, dentro da zona segura |
| `master/rd-station-symbol.svg` | Só o símbolo, sem fundo (uso interno, não é favicon) |

## Uso

```bash
# pacote já gerado em dist/; rode build só se o ícone mudar (requer Playwright + Pillow)
python3 favicon_kit.py build

# instalar num projeto (Vite/Manus: index.html na raiz e pasta public/)
python3 favicon_kit.py install projeto/index.html --name "Calculadora de ROI" \
  --url "https://calculadora-roi.manus.space/" \
  --description "Calcule o ROI, o CAC e a meta de leads do seu marketing." \
  --public projeto/public

# auditar
python3 favicon_kit.py check projeto/index.html --public projeto/public
```

Sem terminal no Manus: use `PROMPT-MANUS.md`.

## O que o `install` faz

| Ação | Por quê |
|---|---|
| Remove `<link rel="icon">`, apple-touch, manifest e theme-color antigos | Evita ícone duplicado e o `vite.svg` padrão |
| Insere o bloco oficial entre `<!-- favicon RD Station: início/fim -->` | Reaplicar não duplica nada (idempotente) |
| Título → `Nome | RD Station` | Marca no título da aba e no resultado de busca |
| `<html lang="pt-BR">` | Geradores deixam `en`, o que atrapalha a busca em português |
| `application-name`, `apple-mobile-web-app-title`, `og:site_name` = RD Station | Nome certo em atalhos, favoritos e compartilhamento |
| `WebSite` JSON-LD com `name` e `alternateName` | Nome do site exibido ao lado do favicon no Google |
| `og:title`, `og:description`, `og:url`, `og:image` só se ausentes | Nunca sobrescreve a imagem de compartilhamento da página |
| Copia o pacote e grava `site.webmanifest` com o nome da ferramenta | Ícone e nome corretos ao instalar como app |

## Validação

- Fixture `fixtures/manus-vite/` (projeto Vite como o Manus gera): `check` passou de 2/12 para 13/13 após o `install`. Aplicar duas vezes produz o mesmo arquivo.
- Servido como build, os 8 arquivos responderam HTTP 200 com o tipo MIME correto (`image/vnd.microsoft.icon`, `image/svg+xml`, `image/png`, `application/manifest+json`).
- O `slop_scan.py` do kit anti-slop aponta favicon ausente ou padrão de gerador como rastro de IA (V20). As ferramentas do RD Kit já saem com o ícone embutido.

## SEO sem mito

- Favicon não é fator de ranqueamento. Ele melhora reconhecimento e clique na busca e nas abas.
- Para o Google exibir: ícone quadrado, múltiplo de 48px, URL estável e rastreável, página inicial indexável.
- O Google pode levar semanas para atualizar. Peça a reindexação da página inicial no Search Console.
- Mantenha os caminhos fixos. Só acrescente `?v=2` quando o ícone mudar de fato.
