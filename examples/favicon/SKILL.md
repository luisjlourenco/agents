---
name: favicon-identity-specialist
description: Troca o favicon de sites e ferramentas criados no Manus (Vite/React, Next.js, Create React App ou HTML) pelo ícone oficial RD Station (símbolo navy sobre fundo ciano), instala o pacote completo (ico, svg, png 96, apple-touch 180, manifest 192/512/maskable), remove ícones padrão do gerador e ajusta título "Nome | RD Station", idioma pt-BR, nome do site, manifest e dados estruturados WebSite para busca, abas, favoritos e celular. Use sempre que um site ou ferramenta for publicado ou estiver com favicon padrão.
---

# Favicon Identity Specialist

Todo site ou ferramenta publicado sai com o **ícone oficial RD Station**: símbolo navy `#002233` sobre quadrado ciano `#00DBFF`. O pacote pronto está em `dist/`. Não gere variações.

## Fluxo

1. **Diagnóstico:** `python3 favicon_kit.py check <index.html> --public <pasta pública>`.
2. **Instalação:**
   ```bash
   python3 favicon_kit.py install <index.html> --name "<Nome da ferramenta>" \
     --url "https://<dominio>/" --description "<uma frase em português>" --public <pasta pública>
   ```
   Pasta pública: `public/` em Vite, Create React App e Next.js; a raiz do site em HTML estático. Em Next.js, traduza o bloco para `metadata` em `app/layout.tsx` e apague `app/favicon.ico` e `app/icon.*`.
   Sem Python, siga `PROMPT-MANUS.md`.
3. **Limpeza:** apague `vite.svg`, `react.svg`, `logo192.png`, `logo512.png` e manifests antigos, se não forem usados.
4. **Verificação:** `check` com todos os itens marcados. Depois do deploy, abra `/favicon.ico` e `/site.webmanifest` no domínio publicado.
5. **Busca:** peça a reindexação da página inicial no Google Search Console.

## Regras

- Sempre o ícone de `dist/`. Proibido recolorir, usar fundo transparente, adicionar texto, borda ou sombra, ou arredondar cantos no arquivo.
- Nomes de arquivo padrão da web (`favicon.ico`, `apple-touch-icon.png`, `site.webmanifest`). Navegadores e o Google procuram esses caminhos.
- Título `Nome | RD Station`, `<html lang="pt-BR">`, nome do site "RD Station".
- Nunca sobrescreva `og:image`, `og:title` ou descrição que a página já tenha.
- Favicon não é fator de ranqueamento: o ganho é reconhecimento e clique. URL estável, sem trocar a cada deploy.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `dist/` | Pacote pronto: `favicon.ico` (16/32/48), `favicon.svg`, `favicon-96x96.png`, `apple-touch-icon.png`, manifest 192/512/maskable, `site.webmanifest`, `head-snippet.html` |
| `master/` | Vetores-mestre do ícone |
| `favicon_kit.py` | `build`, `install` e `check` |
| `PROMPT-MANUS.md` | Instruções para colar no Manus sem terminal |
| `README.md` | Detalhes, validação e SEO |
