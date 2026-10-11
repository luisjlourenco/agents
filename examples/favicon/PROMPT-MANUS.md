# Prompt de favicon para o Manus

Use quando não for possível rodar o `favicon_kit.py`. Anexe ao Manus os arquivos de `dist/` (ou o `.zip` da skill) e cole o texto abaixo, trocando os campos entre colchetes.

```text
Troque o favicon e a identidade do site pelo ícone oficial RD Station. Não altere conteúdo, layout, textos da página nem lógica.

1. Copie para a pasta pública do projeto (no Vite e no Create React App: public/; em HTML estático: a raiz do site) estes arquivos anexados, sem renomear:
   favicon.ico, favicon.svg, favicon-96x96.png, apple-touch-icon.png,
   web-app-manifest-192x192.png, web-app-manifest-512x512.png,
   web-app-manifest-maskable-512x512.png, site.webmanifest

2. Apague os ícones padrão do gerador (por exemplo public/vite.svg, src/assets/react.svg se não for usado, logo192.png, logo512.png) e remova do <head> todas as tags <link rel="icon">, <link rel="apple-touch-icon">, <link rel="manifest"> e <meta name="theme-color"> antigas.

3. No <head> do index.html, logo depois de <meta name="viewport">, insira:
   <link rel="icon" href="/favicon.ico" sizes="48x48">
   <link rel="icon" href="/favicon.svg" type="image/svg+xml">
   <link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">
   <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">
   <link rel="manifest" href="/site.webmanifest">
   <meta name="theme-color" content="#001927">
   <meta name="application-name" content="RD Station">
   <meta name="apple-mobile-web-app-title" content="RD Station">
   <meta property="og:site_name" content="RD Station">
   <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"RD Station","alternateName":["RD"],"url":"[https://SEU-DOMINIO.manus.space/]"}</script>

4. Ajuste os textos:
   - <html lang="pt-BR">
   - <title>[Nome da ferramenta] | RD Station</title>
   - <meta name="description" content="[uma frase em português sobre o que a ferramenta faz]"> (se não existir)
   - Em site.webmanifest, "name": "[Nome da ferramenta] | RD Station".
   - Se a página ainda não tiver og:title, og:url e og:image, adicione og:title igual ao <title>, og:url com o endereço publicado e og:image apontando para /web-app-manifest-512x512.png. Não substitua os que já existirem.

5. Se o projeto for Next.js: coloque os arquivos em public/, apague app/favicon.ico e app/icon.* padrão e declare os mesmos ícones, o manifest e o título em metadata, no app/layout.tsx.

6. Publique e confirme que https://[SEU-DOMINIO]/favicon.ico e https://[SEU-DOMINIO]/site.webmanifest abrem, e que a aba mostra o ícone ciano com o símbolo navy.
```
