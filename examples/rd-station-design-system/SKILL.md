---
name: rd-station-design-system
description: Design system completo da RD Station (uma operação TOTVS) para criar ferramentas, calculadoras, diagnósticos, dashboards, landing pages, páginas de evento e qualquer interface em massa com o mesmo estilo visual. Contém o guia visual integral (cores, tipografia, espaçamento, formas, elevação, movimento, ícones, componentes, layouts), os temas RD Station e Marketing Contínuo, tokens CSS, componentes prontos, os logos oficiais em SVG e um gerador de ferramentas por manifesto JSON. Use sempre que for produzir algo visual com a identidade da RD Station.
---

# RD Station Design System

Você é o designer de UI responsável por produzir peças digitais da RD Station em escala. A centésima ferramenta precisa sair tão fiel à marca quanto a primeira, porque todas nascem do mesmo sistema. Este pacote é autossuficiente: tudo o que você precisa está nesta pasta.

## Antes de qualquer entrega

1. **Leia `GUIDELINES.md`**. Ele é a fonte única de verdade para cores, tipografia, espaçamento, formas, elevação, movimento, ícones, componentes, layouts, logos e acessibilidade.
2. Escolha o **tema**: `rd-station` (padrão) ou `marketing-continuo` (só em peças sobre a disciplina Marketing Contínuo).
3. Use **apenas** valores de `tokens.css` e classes de `components.css`. Nunca invente um hex, uma fonte ou um espaçamento.

## Mapa do pacote

| Arquivo | Conteúdo |
|---|---|
| `GUIDELINES.md` | Guia visual completo (leitura obrigatória) |
| `tokens.css` | Todas as variáveis de design, temas e a importação das fontes |
| `components.css` | Componentes e padrões prontos em CSS puro |
| `brand/` | Logos oficiais em SVG: RD Station, os produtos RD Station e TOTVS, em versões clara e escura |
| `templates/tool-public.html` | Template de ferramenta pública com placeholders `{{...}}` |
| `tools/*.json` | Manifestos de exemplo, um por ferramenta |
| `generate.py` | Gera `dist/<slug>.html` a partir dos manifestos (Python 3, só biblioteca padrão) |
| `dist/` | Ferramentas de exemplo já geradas, como referência visual |
| `README.md` | Como operar o kit, campos do manifesto e pendências |

## Fluxo de produção

### Ferramenta (calculadora, diagnóstico, simulador)
1. Copie um manifesto de `tools/` e ajuste `slug`, `theme`, textos, `inputs`, `outputs` (com `formula`) e `insight`.
2. Rode `python3 generate.py tools/<slug>.json`.
3. Entregue `dist/<slug>.html`: um arquivo único, com CSS e logos embutidos.
4. Confira o checklist de QA em 1280px e em 390px.

Se não puder rodar Python, monte o HTML à mão a partir de `templates/tool-public.html`. Cole `tokens.css` e `components.css` dentro do `<style>`, substitua os `{{...}}` e cole os SVGs de `brand/` nos lugares do logo.

### Outras peças (dashboard, landing page, protótipo, página de evento)
- Componha com `tokens.css`, `components.css` e os layouts da seção 11 de `GUIDELINES.md`.
- Produto logado: shell com navbar e sidebar de 64px em navy e conteúdo branco com o canto superior esquerdo arredondado em 20px.
- Página pública: topbar navy, hero KV, painel branco sobreposto e rodapé com endosso.

### Peças não-HTML (slides, imagens, PDFs)
Aplique os mesmos valores: paleta, fontes, escala tipográfica, raios, grafismos e regras de logo de `GUIDELINES.md`.

## Regras inegociáveis

**Logo**
- O logo RD Station oficial (de `brand/`) está sempre presente, acima da dobra, com 32px de altura e 16px de respiro.
- Em fundo claro, use a versão navy. Em fundo escuro, use a versão branca. A versão ciano é só para a navbar do produto logado.
- Nunca redesenhe, estique, recolora ou aplique efeito no logo, e nunca troque o RD Station pelo logo TOTVS.
- Endosso: **"uma operação TOTVS"**, sempre menor que o RD Station. Em capas, fica no canto superior direito; em ferramentas, no rodapé.

**Cor**
- O ciano `#00DBFF` é a cor-assinatura. Sobre fundo claro, texto e ícone usam `#0077B2`, porque o ciano puro reprova o contraste.
- O botão primário fica em navy com texto ciano. Use **um único primário por tela**.
- O lime `#C3F628` é exclusivo do CTA de campanha ou KV, com texto navy.
- As cores funcionais (perigo, sucesso, atenção, destaque) nunca são decorativas. As cores de suporte servem só para gráficos.
- No tema Marketing Contínuo, o roxo `#A44DFF` só aparece em superfícies, grafismos e texto de 24px ou mais. Botões usam `#7B2FFF`.

**Tipografia**
- Tema padrão: DM Sans.
- Tema Marketing Contínuo: Red Hat Display nos títulos e Inter Tight no corpo.
- Use só a escala de `GUIDELINES.md` (12, 14, 16, 20, 28 e 36px, mais o display dos heros).

**Composição**
- Grid de 8px, 12 colunas e breakpoints em 480, 768, 1024 e 1280px.
- Grafismos (geometria, digital, listras) ficam nos cantos e bordas, nunca atrás de texto.
- Button executa uma ação; Link navega. Rótulos de botão vão no infinitivo, com 2 a 3 palavras.

**Acessibilidade**
- Contraste AA, foco visível e labels ligados aos campos.
- Nada de rolagem horizontal em 390px. Respeite `prefers-reduced-motion`.

## Checklist de QA (rode em toda entrega)

- [ ] O logo RD Station oficial aparece acima da dobra, na versão certa para o fundo.
- [ ] O endosso "uma operação TOTVS" é menor que o logo RD Station.
- [ ] O tema está certo para o assunto.
- [ ] Nenhum hex fora de `tokens.css`. Só as fontes do tema.
- [ ] Um único botão primário por tela.
- [ ] Contraste AA (ciano puro só sobre navy).
- [ ] Sem rolagem horizontal em 390px, e os grafismos não cobrem texto.
- [ ] Foco visível; ajuda e erro ligados aos campos por `aria-describedby`.

## Limites deste pacote

- A paleta e a tipografia institucionais da **TOTVS** não estão incluídas. A TOTVS aparece só como logo de endosso. Não aproxime esses valores: peça os oficiais antes de criar peças co-branded.
- Tokens marcados `[derivado]` em `tokens.css` (curvas de sombra e o hover do botão primário, por exemplo) devem ser validados pelo time de Design antes de usos fora deste kit.
