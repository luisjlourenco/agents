# Guia visual RD Station

Referência completa e autossuficiente da identidade visual da RD Station (uma operação TOTVS) para interfaces, ferramentas, páginas e materiais digitais. Todo valor citado aqui existe como token em `tokens.css`. Os componentes descritos estão implementados em `components.css`.

**Regra zero:** nunca use um valor solto (hex, px, fonte) que não esteja neste guia. Se faltar algo, crie o token primeiro e documente aqui.

---

## Sumário

1. [Marca e logos](#1-marca-e-logos)
2. [Cores](#2-cores)
3. [Tipografia](#3-tipografia)
4. [Espaçamento e grid](#4-espaçamento-e-grid)
5. [Formas e arredondamentos](#5-formas-e-arredondamentos)
6. [Elevação e sobreposição](#6-elevação-e-sobreposição)
7. [Movimento](#7-movimento)
8. [Ícones](#8-ícones)
9. [Key Visual (KV)](#9-key-visual-kv)
10. [Tema Marketing Contínuo](#10-tema-marketing-contínuo)
11. [Layouts](#11-layouts)
12. [Componentes](#12-componentes)
13. [Qual componente usar](#13-qual-componente-usar)
14. [Texto de interface](#14-texto-de-interface)
15. [Acessibilidade](#15-acessibilidade)
16. [Checklist de QA de marca](#16-checklist-de-qa-de-marca)

---

## 1. Marca e logos

### 1.1 Arquivos oficiais (`brand/`)

| Marca | Fundo claro | Fundo escuro |
|---|---|---|
| RD Station (marca principal) | `rd-station-logo.svg` (navy `#002233`) | `rd-station-logo-on-dark.svg` (branco) |
| RD Station, navbar do produto logado | — | `rd-station-logo-cyan.svg` (ciano `#00DBFF`) |
| RD Station Marketing | `rd-station-marketing-logo.svg` | `rd-station-marketing-logo-on-dark.svg` |
| RD Station Marketing for Ecommerce | `rd-station-marketing-ecommerce-logo.svg` | `rd-station-marketing-ecommerce-logo-on-dark.svg` |
| RD Station CRM | `rd-station-crm-logo.svg` | `rd-station-crm-logo-on-dark.svg` |
| RD Station Conversas | `rd-station-conversas-logo.svg` | `rd-station-conversas-logo-on-dark.svg` |
| RD Station Mentor IA | `rd-station-mentor-ia-logo.svg` | `rd-station-mentor-ia-logo-on-dark.svg` |
| RD Station Billing | `rd-station-billing-logo.svg` | `rd-station-billing-logo-on-dark.svg` |
| RD Station App Store | `rd-station-app-store-logo.svg` | `rd-station-app-store-logo-on-dark.svg` |
| TOTVS (endosso) | `totvs-logo.svg` | `totvs-logo-on-dark.svg` |

### 1.2 Regras de uso

- **O logo RD Station está sempre presente**, acima da dobra.
- Altura padrão de **32px**. Use no mínimo 20px em endossos e rodapés. A largura acompanha a proporção do SVG: nunca defina largura e altura fixas ao mesmo tempo.
- Deixe **16px de respiro** livre em todos os lados.
- Em fundo claro (branco ou cinza), use a versão navy. Em fundo navy ou escuro, use a versão branca.
- A versão ciano é exclusiva da navbar do produto logado. Não use em peças de marketing.
- Use logos de produto apenas em peças daquele produto. Nas demais, o logo é o RD Station.
- **Proibido:**
  - redesenhar, esticar, rotacionar, recortar ou rasterizar em baixa resolução;
  - recolorir fora das versões acima;
  - aplicar sombra, contorno, gradiente ou brilho;
  - pôr o logo sobre foto sem uma película navy por baixo;
  - usar o logo TOTVS no lugar do RD Station.
- **Acessibilidade:** o contentor do logo leva `aria-label="RD Station"` (ou o nome do produto). Se o SVG estiver dentro de um link ou contentor rotulado, marque-o como decorativo (`aria-hidden="true"`).

### 1.3 Endosso TOTVS

- Assinatura: **"uma operação TOTVS"**, com o texto "uma operação" seguido do logo TOTVS.
- **Posição:**
  - em capas, slides e banners: no canto superior direito, com o RD Station no canto superior esquerdo ou inferior direito;
  - em ferramentas e páginas: no rodapé.
- O endosso é sempre menor que o logo RD Station e nunca disputa a mesma hierarquia.
- A paleta e a tipografia institucionais da TOTVS **não** fazem parte deste guia. A TOTVS aparece apenas como endosso.

---

## 2. Cores

Contraste mínimo (WCAG AA): **4,5:1** para texto normal e **3:1** para texto grande (24px ou mais, ou 18,66px ou mais em negrito).

### 2.1 Primárias

Predominam nos elementos de destaque.

| Token | Hex | Uso |
|---|---|---|
| `--primary-border` | `#00DBFF` | Bordas com destaque primário |
| `--primary-border-hover` | `#0088CC` | Borda em hover e foco de input |
| `--primary-icon` | `#0077B2` | Ícones primários sobre fundo claro |
| `--primary-icon-hover` | `#005580` | Ícones primários em hover |
| `--primary-icon-on-color` | `#00DBFF` | Ícones sobre fundo escuro |
| `--primary-icon-on-color-hover` | `#66E9FF` | Ícones on-dark em hover |
| `--primary-surface-high-emphasis` | `#00DBFF` | Fundo de maior destaque (card ativo, barra de progresso) |
| `--primary-surface-low-emphasis` | `#B2F4FF` | Fundo suave (botão secundário, mensagem informativa) |
| `--primary-surface-hover` | `#66EBFF` | Fundo primário em hover |
| `--primary-text` | `#0077B2` | Texto e link primário sobre fundo claro |
| `--primary-text-hover` | `#005580` | Texto primário em hover |
| `--primary-text-on-color` | `#00DBFF` | Texto sobre fundo escuro |
| `--primary-text-on-color-hover` | `#66E9FF` | Texto on-dark em hover |

> O ciano puro `#00DBFF` sobre branco tem só 1,6:1 de contraste. Em fundo claro, texto e ícone usam `#0077B2`.

### 2.2 Neutras

Para textos, bordas, fundos e divisores.

| Token | Hex | Uso |
|---|---|---|
| `--neutral-border` | `#D6DBDE` | Bordas padrão de cards e divisores |
| `--neutral-border-interactive` | `#B2BCC1` | Borda de input, select e checkbox |
| `--neutral-border-interactive-hover` | `#8C9BA3` | Borda interativa em hover |
| `--neutral-border-interactive-disabled` | `#E5E8EA` | Borda desabilitada |
| `--neutral-icon-high-emphasis` | `#002233` | Ícone de máximo destaque |
| `--neutral-icon-low-emphasis` | `#596B7A` | Ícone secundário |
| `--neutral-icon-disabled` | `#8C98A3` | Ícone desabilitado |
| `--neutral-icon-inverse` | `#FFFFFF` | Ícone sobre fundo escuro |
| `--neutral-surface` | `#FFFFFF` | Fundo padrão de cards, modais e inputs |
| `--neutral-surface-high-emphasis` | `#E5E8EA` | Superfície de maior contraste |
| `--neutral-surface-low-emphasis` | `#ECEEEF` | Superfície suave (linha zebrada, sidebar) |
| `--neutral-surface-hover` | `#DADEE0` | Fundo em hover |
| `--neutral-surface-disabled` | `#EDEFF1` | Fundo desabilitado |
| `--neutral-surface-inverse` | `#002233` | Fundo escuro (tooltip, barra de ações em massa) |
| `--neutral-text-high-emphasis` | `#002233` | Texto principal |
| `--neutral-text-low-emphasis` | `#405466` | Texto secundário, descrição, placeholder |
| `--neutral-text-disabled` | `#7F8D99` | Texto desabilitado |
| `--neutral-text-inverse` | `#FFFFFF` | Texto sobre fundo escuro |

### 2.3 Funcionais

Comunicam estado e significado. **Nunca use de forma decorativa.**

**Perigo (vermelho).** Para exclusão, desconexão e perda irreversível.

| Token | Hex |
|---|---|
| `--danger-border` / `--danger-icon` / `--danger-text` | `#C20046` |
| `--danger-surface-high-emphasis` | `#E60F57` |
| `--danger-surface-low-emphasis` | `#FFD6E4` |
| `--danger-surface-hover` | `#F53D74` |
| `--danger-text-on-color` | `#F53D74` |

**Sucesso (verde).** Para ação concluída e validação OK.

| Token | Hex |
|---|---|
| `--success-border` | `#0AAF54` |
| `--success-icon` / `--success-text` | `#087A3A` |
| `--success-surface-high-emphasis` | `#0ED869` |
| `--success-surface-low-emphasis` | `#D6FAE8` |
| `--success-surface-hover` | `#29DE82` |

**Atenção (amarelo).** Para situações não críticas e reversíveis.

| Token | Hex |
|---|---|
| `--warning-border` | `#D4920A` |
| `--warning-icon` / `--warning-text` | `#A06800` |
| `--warning-surface-high-emphasis` | `#FFBD28` |
| `--warning-surface-low-emphasis` | `#FFF3D0` |
| `--warning-surface-hover` | `#FFC73E` |

**Destaque (roxo).** Para ajuda, suporte e novidades. Também pode ser fundo de avatar.

| Token | Hex |
|---|---|
| `--highlight-border` / `--highlight-icon` / `--highlight-text` | `#6E00C5` |
| `--highlight-surface-high-emphasis` | `#8800F7` |
| `--highlight-surface-low-emphasis` | `#EDD6FF` |
| `--highlight-surface-hover` | `#9E38FF` |
| `--highlight-text-on-color` | `#B570FF` |

### 2.4 Suporte (apenas gráficos e data viz)

Use somente em gráficos, legendas e visualização de dados, nunca em interface.

| Família | Forte | Suave | Brisa |
|---|---|---|---|
| Mint | `#00F2C9` | `#81F0D8` | `#CCFCF1` |
| Magenta / Pink | `#ED0093` | `#FA86C5` | `#FDD6EA` |
| Orange | `#FF8900` | `#FFC676` | `#FFE8C2` |
| Lime | `#C3F628` (deep `#9FCA1D`) | `#E6FC88` | `#F6FED0` |

Ordem recomendada de séries: ciano `#00DBFF`, mint, magenta, orange, lime, roxo `#8800F7`.

### 2.5 Nomenclatura

| Sufixo | Significado |
|---|---|
| `surface` | Preenchimento de elementos (não vale para texto, ícone ou borda) |
| `high-emphasis` / `low-emphasis` | Tom de maior ou menor destaque dentro da paleta |
| `on-color` / `inverse` | Para usar sobre fundos escuros ou coloridos |
| `interactive` | Bordas de elementos interativos |
| `hover` / `disabled` | Estados |

### 2.6 Regiões

Toda tela é composta por três tipos de região, e os componentes se adaptam a cada uma:

| Região | Fundo | Uso |
|---|---|---|
| **Default** | Branco `#FFFFFF` | Conteúdo, formulários, tabelas |
| **Contrast** | Navy `#001927` / `#002233` | Navbar, heros, faixas de impacto, barras de ação |
| **Highlight** | Roxo `#8800F7` ou cor de campanha | Faixas de campanha e chamadas especiais |

---

## 3. Tipografia

### 3.1 Famílias

| Tema | Títulos | Corpo |
|---|---|---|
| RD Station (padrão) | **DM Sans** (Regular 400, Bold 700, ExtraBold 800) | DM Sans |
| Marketing Contínuo | **Red Hat Display** (300 a 900, com itálico) | **Inter Tight** (400, 500, 700) |

Fallback: `system-ui, -apple-system, "Segoe UI", sans-serif`. Carregamento: Google Fonts (já incluído em `tokens.css`).

### 3.2 Escala

Os tokens não estão presos a `h1`, `h2` ou `p`. Escolha pelo papel do texto.

| Token | Tamanho / linha | Letter-spacing | Uso |
|---|---|---|---|
| `--text-xxl-*` | 36 / 46px | -0.02em | Big numbers, KPIs, métricas principais |
| `--text-xl-*` | 28 / 36px | -0.01em | Título de página |
| `--text-lg-*` | 20 / 30px | -0.01em | Subtítulo, título de bloco, modal, sidebar |
| `--text-md-*` | 16 / 24px | -0.01em | **Padrão de interface:** texto, label, input, botão, link |
| `--text-sm-*` | 14 / 20px | -0.01em | Texto de apoio, validação, componentes compactos |
| `--text-xs-*` | 12 / 16px | 0 | Cabeçalho de tabela, eixo de gráfico, legenda, rodapé |

Cada tamanho tem três pesos: `-regular` (400), `-bold` (700) e `-extrabold` (800). Exemplo: `font: var(--text-md-bold);`.

**Display (heros e capas):** headline em `clamp(32px, 5vw, 56px)`, peso 800, linha 1,1, letter-spacing -0.02em, até 16 caracteres por linha.

### 3.3 Regras

- Entre um título e o conteúdo abaixo, deixe no mínimo 16px.
- Rótulos de seção (eyebrow) vão em caixa alta: 12 a 14px bold, ciano em fundo escuro ou `#0077B2` em fundo claro.
- Números em tabelas usam `font-variant-numeric: tabular-nums` e ficam alinhados à direita.
- No corpo de texto, limite a linha a 52–65 caracteres.

---

## 4. Espaçamento e grid

### 4.1 Escala (grid de 8px)

| Token | Valor | Uso típico |
|---|---|---|
| `--size-spacing-01` | 4px | Gaps mínimos |
| `--size-spacing-02` | 8px | Ícone e texto, padding de badge |
| `--size-spacing-03` | 12px | Padding de input, gap compacto |
| `--size-spacing-04` | 16px | Padding padrão de card e modal; mínimo entre título e conteúdo |
| `--size-spacing-05` | 24px | Seções dentro de um componente, grupos de campos |
| `--size-spacing-06` | 32px | Entre seções da página e entre cards |
| `--size-spacing-07` | 40px | Blocos maiores |
| `--size-spacing-08` | 48px | Margem de seção |
| `--size-spacing-09` | 56px | Seções grandes |
| `--size-spacing-10` | 64px | Separações estruturais |
| `--size-spacing-11` | 96px | Heros |
| `--size-spacing-12` | 160px | Seções de landing page |

De 8 a 24px, os valores servem a componentes. Acima de 24px, servem a composições e telas. Os valores são mínimos: nunca use menos que o indicado para o contexto.

### 4.2 Grid

- 12 colunas.
- Gutter de 16px no mobile e de 24px a partir do tablet.
- Container com no máximo 1280px no desktop e 1440px em telas grandes, e padding lateral de 16px no mobile e de 32px a partir do tablet.
- Breakpoints (min-width): **480px** mobile, **768px** tablet, **1024px** desktop, **1280px** desktop grande.
- Abaixo de 768px, layouts de duas ou três colunas viram uma coluna.

---

## 5. Formas e arredondamentos

| Token | Valor | Uso |
|---|---|---|
| `--border-radius-xs` | 4px | Tags, chips compactos, checkbox |
| `--border-radius-sm` | 8px | Botão compacto, itens de navegação |
| `--border-radius-md` | 12px | Botão padrão, input, dropdown, card médio |
| `--border-radius-lg` | 16px | Card, painel, imagem arredondada |
| `--border-radius-xl` | 24px | Modal, painel de ferramenta, drawer |
| `--border-radius-xxl` | 32px | Destaques máximos |
| `--border-radius-pill` | 999px | Avatar, chip pill, switch, barra de progresso |
| `--border-radius-circle` | 50% | Formas elípticas |

O conteúdo principal do produto logado tem o canto superior esquerdo com 20px de raio.

---

## 6. Elevação e sobreposição

| Nível | Token | Uso |
|---|---|---|
| 1 | sem sombra | Texto, botão, formulário, imagem |
| 2 | `--shadow-xs` | Navbar, card elevado |
| 3 | `--shadow-sm` | Dropdown, popover, date picker, hover de card clicável |
| 4 | `--shadow-md` | Toast |
| 5 | `--shadow-lg` | Drawer sobre fundo claro, painel de ferramenta sobre o hero |
| 6 | `--shadow-xl` | Modal, dialog e drawer sobre overlay |

As sombras usam o navy `rgba(0, 34, 51, …)`, nunca preto puro. O overlay de modal é `rgba(0, 34, 51, 0.5)`.

| Z-index | Valor | Uso |
|---|---|---|
| `--zindex-0` | 1 | Elemento selecionado |
| `--zindex-1` | 1000 | Dropdown, popover |
| `--zindex-2` | 1010 | Tooltip, navbar fixa |
| `--zindex-3` | 1020 | Overlay |
| `--zindex-4` | 1030 | Modal, dialog, drawer |
| `--zindex-6` | 1050 | Toast (acima de tudo) |

---

## 7. Movimento

O movimento sempre tem propósito: indicar uma mudança de estado, revelar conteúdo ou dar ênfase. Ele nunca faz a pessoa esperar.

| Duração | Valor | Uso |
|---|---|---|
| `--motion-duration-extra-fast` | 100ms | Botões, toggles, checkbox, inputs |
| `--motion-duration-fast` | 200ms | Microinterações, dropdown, select |
| `--motion-duration-normal` | 300ms | Expansões médias, toast, accordion |

| Curva | Valor | Uso |
|---|---|---|
| `--motion-timing-function-ease-out` | `cubic-bezier(0.215, 0.61, 0.355, 1)` | **Entrar:** abrir modal, mostrar alerta |
| `--motion-timing-function-ease-in` | `cubic-bezier(0.55, 0.055, 0.675, 0.19)` | **Sair:** fechar, esconder |
| `--motion-timing-function-ease-in-out` | `cubic-bezier(0.645, 0.045, 0.355, 1)` | Elementos visíveis o tempo todo |

O que entra pela esquerda sai pela esquerda. Elementos menores se movem mais rápido. Sempre respeite `prefers-reduced-motion`.

---

## 8. Ícones

| Propriedade | Valor |
|---|---|
| Biblioteca | Material Symbols (Google) |
| Estilo | **Rounded** |
| Fill | Preenchido (fill 1) |
| Peso | **600** |
| Tamanhos | 24px (padrão), 20px (compacto), 16px (inline em texto pequeno) |

- Ícones da navegação do produto são bicolores: contorno branco com detalhe ciano `#00DBFF` sobre navy.
- Um botão só com ícone precisa de `aria-label`.
- Nunca misture estilos de ícone na mesma interface.

---

## 9. Key Visual (KV)

É a linguagem de site, campanhas, eventos e ferramentas públicas.

| Token | Hex | Papel |
|---|---|---|
| `--kv-navy-900` | `#001927` | Fundo de marca: topbar, hero, rodapé, slides de impacto |
| `--kv-navy-800` | `#002233` | Superfície inversa, texto de máxima ênfase |
| `--kv-navy-700` | `#0A3A52` | Cards sobre navy |
| `--kv-cyan` | `#00DBFF` | Cor-assinatura: destaque de headline, acentos, CTAs on-dark |
| `--kv-cyan-soft` | `#66E9FF` | Hover on-dark |
| `--kv-lime` | `#C3F628` | CTA de campanha (com texto navy) |
| `--kv-violet-start` → `--kv-violet-end` | `#7B4AFF` → `#3C10B1` | Gradiente de ilustração e geometria |

**Composição do KV:**
- **Hero:** gradiente radial navy (`--kv-gradient-hero`), com eyebrow ciano em caixa alta, headline branca de peso 800 e um trecho de destaque em ciano, mais um subtítulo branco com 78% de opacidade.
- **Geometria:** peças triangulares e losangos em ciano e no gradiente violeta, sempre ancoradas nos cantos e nunca atrás de texto.
- **CTA de destaque on-dark:** fundo lime `#C3F628` com texto navy, 48px de altura e raio de 12px. Use um por tela.
- **Fotografia:** pessoas reais em fundo neutro claro, enquadradas em retângulos retos ao lado de blocos chapados de ciano.

---

## 10. Tema Marketing Contínuo

É a linguagem do guia visual da disciplina Marketing Contínuo. Ative com `<html data-theme="marketing-continuo">` ou com `"theme": "marketing-continuo"` no manifesto. Use apenas em peças sobre a disciplina e nunca misture com o tema padrão na mesma peça.

### 10.1 Paleta

| Token | Hex | Papel |
|---|---|---|
| `--mc-navy` | `#002233` | Fundo dominante |
| `--mc-navy-raised` | `#0B2C4A` | Cards e painéis sobre navy |
| `--mc-navy-line` | `#023548` | Divisórias e listras escuras |
| `--mc-purple` | `#A44DFF` | Slide de impacto, numerais de seção, grafismos |
| `--mc-purple-deep` | `#7B2FFF` | Botões e faixas com texto pequeno |
| `--mc-purple-text` | `#B57BFF` | Texto roxo pequeno sobre navy |
| `--mc-cyan` | `#00DBFF` | Headlines on-dark, faixas, destaques |
| `--mc-cyan-deep` | `#00C9EB` | Listras diagonais e anéis |
| `--mc-lime` | `#D9FC68` | Grafismo de digital, marcador de chip |
| `--mc-gray` | `#EFEFEF` | Fundo claro dos slides de conceito |
| `--mc-gray-2` | `#DDDDDD` | Painel claro em split-screen |

**Contraste:**
- `#A44DFF` com branco dá 4,13:1. Use **só em superfícies, grafismos e texto de 24px ou mais**.
- Botões e texto pequeno usam `#7B2FFF`, que com branco dá 5,69:1.
- Para texto roxo pequeno sobre navy, use `#B57BFF` (5,67:1).
- Sobre cinza `#EFEFEF`, o texto pequeno primário usa `#005580`, porque `#0077B2` dá apenas 4,27:1.

### 10.2 Tipografia do tema

- **Títulos:** Red Hat Display. Combine pesos na mesma frase: um trecho em ExtraBold 800 e outro em Light 300 ciano.
- **Abertura de seção**, no padrão "01 · O MOMENTO E O PROBLEMA":
  - numeral roxo `#A44DFF` em Black Italic, de 40 a 64px;
  - título ciano em Black Italic, caixa alta, de 20 a 32px.
- **Eyebrow:** ExtraBold Italic de 14px, caixa alta, em ciano. Exemplo: "É CONTÍNUO PORQUE".
- **Corpo:** Inter Tight de 14 a 16px, em branco a 78% sobre navy ou em navy sobre cinza.
- **Citações:** de 24 a 32px, entre aspas, com o nome do autor em ciano e o cargo em texto secundário.

### 10.3 Grafismos

| Grafismo | Como usar |
|---|---|
| **Digital** (anéis concêntricos) | Em roxo sobre navy ou em lime sobre roxo. Fica nos cantos inferiores ou na lateral, cortado pela borda |
| **Listras diagonais** | Em ciano `#00C9EB`, inclinadas a 115°. Formam faixas no topo ou na base, e bordas de capa |
| **Anel de texto** | "MARKETING CONTÍNUO" em loop, contornando uma imagem ou um selo |
| **Espiral de três anéis** | Representa o sistema (Contexto profundo, Comportamento previsível, Crescimento em espiral) em torno de "Informação conectada" |
| **Blocos ciano chapados** | Retângulos retos ao lado de fotos de pessoas, em layout de revista |

### 10.4 Composições recorrentes

- **Capa:** navy com bordas de listras diagonais. Logo RD Station no topo à esquerda e "uma operação TOTVS" no topo à direita. Título em Bold 56px ou mais, com um sublinhado ciano curto.
- **Slide de impacto:** fundo roxo `#A44DFF` com uma frase grande, mesclando bold e light. A digital lime aparece na lateral.
- **Split-screen "Antes × Agora":** painel cinza claro à esquerda (antes) e navy à direita (agora).
- **Cards de conteúdo:** navy elevado `#0B2C4A`, com uma barra de 4px no topo em ciano ou roxo e título bold de 16px.
- **Chips de canais:** pílulas brancas com um ponto lime e texto navy.
- **Faixas-rótulo:** barra ciano com texto navy (por exemplo, "Vendas") ou barra roxa profunda com texto branco (por exemplo, "Marketing").
- **Botão primário:** roxo profundo `#7B2FFF`, texto branco em caixa alta. Exemplo: "CLIQUE PARA ACESSAR".

Classes prontas: `.mc-section`, `.mc-headline`, `.mc-eyebrow`, `.mc-card`, `.mc-chip`, `.mc-band` e `.mc-impact`.

---

## 11. Layouts

### 11.1 Produto logado (shell)

```
┌──────────────────────────── navbar 64px (navy #001927) ───────────────────────────┐
│ logo ciano · seletor de produto            ícones · divisor · avatar + nome ▾     │
├────┬──────────────────────────────────────────────────────────────────────────────┤
│ 64 │  conteúdo branco, canto superior esquerdo com raio de 20px,                  │
│ px │  padding lateral de 24px, rolagem interna                                    │
│side│                                                                              │
│bar │                                                                              │
└────┴──────────────────────────────────────────────────────────────────────────────┘
```
- A navbar e a sidebar ficam em navy `#001927`, e os ícones de 24px são brancos com detalhe ciano.
- O item ativo ou em hover da sidebar ganha um fundo `rgba(255,255,255,.08)` com raio de 8px.
- O conteúdo começa com o cabeçalho da página: título de 28px ExtraBold, 40px de padding no topo e as ações à direita.

### 11.2 Ferramenta pública (site, lead-gen, evento)

1. **Topbar** navy com o logo RD Station branco à esquerda e um CTA secundário à direita.
2. **Hero KV** com eyebrow, headline com destaque, subtítulo e geometria no canto.
3. **Painel branco** sobreposto ao hero (64px para cima), com raio de 24px, sombra de nível 5 e padding de 32px (24px e 16px no mobile).
4. **Conteúdo** em duas colunas (formulário à esquerda, resultado à direita), que viram uma no mobile.
5. **Rodapé** navy com o logo RD Station e "uma operação TOTVS".

---

## 12. Componentes

### Button

| Tipo | Default (fundo claro) | Quando usar |
|---|---|---|
| **Primário** | Fundo navy `#002233` e texto ciano `#00DBFF`. Hover em `#0A3A52` com texto `#66E9FF` | Ação principal. **Só um por tela** |
| **Secundário** | Fundo `#B2F4FF` e texto `#0077B2`. Hover em `#66EBFF` | Ação de importância média, perto da primária |
| **Terciário** | Transparente com texto `#0077B2`. Hover em `#B2F4FF` | Cancelar, voltar, fechar |
| **Danger** | Fundo `#E60F57` e texto branco | Ação destrutiva, sempre com "Cancelar" ao lado |
| **Neutro** | Transparente com texto `#405466` | Ação de baixa ênfase |

- **Tamanho padrão:** 40px de altura, padding lateral de 16px, raio de 12px, texto de 16px Bold e ícone de 24px.
- **Tamanho compacto** (`sm`, ou qualquer botão em região escura): 32px de altura, padding de 12px, raio de 8px, texto de 14px Bold e ícone de 20px.
- **Em região escura (Contrast):** transparente com texto ciano. No hover, ganha um fundo ciano translúcido.
- **Em região Highlight:** o primário fica com fundo lime `#C3F628` e texto navy.
- **Desabilitado:** fundo `#EDEFF1` e texto `#7F8D99`.
- **Rótulo:** verbo no infinitivo, com 2 a 3 palavras ("Salvar contato", "Criar campanha"). Nunca quebre em duas linhas.
- **Carregando:** um spinner no lugar do ícone, com o botão desabilitado e `aria-busy="true"`.

### Link
Usado para navegar, nunca para executar uma ação. Texto bold em `#0077B2`, com hover em `#005580` sublinhado. Em fundo escuro, fica em ciano `#00DBFF`.

### Input, Select e TextArea
- 40px de altura, raio de 12px, padding de 12px, borda `#B2BCC1`, com hover em `#8C9BA3`.
- **Foco:** borda `#0088CC` com um anel `0 0 0 3px #B2F4FF`.
- **Erro:** borda `#C20046` e mensagem em `#C20046`.
- **Sucesso:** borda `#0AAF54`.
- **Desabilitado:** fundo `#EDEFF1`.
- **Label:** 16px Bold, com asterisco vermelho quando o campo é obrigatório.
- **Ajuda:** 14px Regular em `#405466`, logo abaixo do campo.
- O placeholder só aparece quando ajuda de verdade e nunca substitui o label.

### Checkbox, Radio e Switch
- **Checkbox e radio:** 18px (ou 24px no tamanho grande), borda `#B2BCC1`. Marcados, ficam em ciano. O gap até o label é de 12px.
- **Switch:** trilho em pílula de 48×24px. Aplica a mudança na hora, sem precisar enviar um formulário.

### Card
- Fundo branco, borda `#D6DBDE` de 1px, raio de 16px e padding de 24px (16px no modo compacto).
- **Clicável:** ganha sombra de nível 3 no hover.
- **Ativo:** fundo ciano `#00DBFF` e borda transparente.

### DataBlock (KPI)
Título de 14px Bold em caixa alta e cor `#405466`. Valor de 36px Bold ou ExtraBold. Texto auxiliar de 14px, em verde quando o valor sobe e em vermelho quando desce.

### Tag
- 24px de altura, raio de 4px, texto de 12px Bold.
- **Variações:** neutra `#ECEEEF`, primária `#B2F4FF`, sucesso `#D6FAE8`, atenção `#FFF3D0`, perigo `#FFD6E4` e destaque `#EDD6FF`. O texto usa o tom forte de cada uma.

### Badge
Ponto de 12px ou contador de 16px de altura, raio de 8px e texto de 12px ExtraBold. A versão de perigo usa `#E60F57` com texto branco; a de sucesso, `#0ED869` com texto navy.

### Avatar
- **Pessoa:** sempre circular, em 32, 40, 80 ou 120px.
- **Marca:** raio proporcional ao tamanho.
- **Iniciais:** primeira letra do primeiro nome e do último sobrenome ("Bruno Ghisi" vira BG).

### Alert
Crítico, fixo no topo e acima da navbar. **Não pode ser fechado.** O perigo usa `#E60F57` com texto branco; a atenção, `#FFBD28` com texto navy. Texto de 14px Bold.

### Message
Mensagem inline, com raio de 12px e padding de 16px. As variantes usam os fundos suaves: primária, sucesso, atenção, perigo e ajuda (`#EDD6FF`).

### Toast
- Temporário e não crítico.
- Posição: canto superior direito, a 32px das bordas, com 300px de largura e sombra de nível 4.
- Fica acima de tudo, inclusive do modal.
- Cores por intenção:
  - vermelho: crítico;
  - amarelo: atenção;
  - verde: sucesso;
  - roxo: ajuda;
  - ciano: novidade.

### Modal e Dialog
- **Modal:** cartão de cerca de 600px, raio de 24px e sombra de nível 6 sobre overlay navy a 50%. O cabeçalho e as ações ficam sempre visíveis. Tem sempre uma opção "Cancelar".
- **Dialog:** só para confirmar. Em ações destrutivas, usa um botão danger e um checkbox de confirmação.

### Drawer
Painel lateral com 100% da altura, nas larguras de 300px, 400px (padrão) ou 600px. À direita, mostra detalhes ou configurações; à esquerda, ferramentas.

### Dropdown, Popover e Tooltip
- **Dropdown:** de 160 a 620px de largura, raio de 12px, sombra de nível 3 e no máximo 360px de altura.
- **Popover:** conteúdo rico, de 280 a 620px de largura.
- **Tooltip:** só texto, até 250px, fundo `#002233` com texto branco de 14px. Nunca coloque informação crítica em tooltip.

### Table
- **Cabeçalho:** 12px Bold em caixa alta, cor `#405466`.
- **Linhas:** zebradas em `#ECEEEF`, com divisória `#D6DBDE`.
- **Valores:** números alinhados à direita; célula vazia mostra "-"; valor zero mostra "0".
- A paginação fica no rodapé, com tamanhos de página de 10, 20, 50 ou 100.

### Tabs, Steps e Pagination
- **Tabs:** 48px de altura, com uma linha inferior de 2px em `#D6DBDE`. A aba ativa fica em ciano.
- **Steps:** barras de 4px em pílula. A etapa atual e as concluídas ficam em ciano; no tema Marketing Contínuo, em roxo.
- **Pagination:** setas de anterior e próximo e números de página. Acima de 7 páginas, usa reticências.

### Skeleton, Spinner e ProgressBar
- **Skeleton:** gradiente animado de `#ECEEEF` para `#E5E8EA`. Use em listas e cards.
- **Spinner:** 24, 32 ou 48px, só para ações pontuais.
- **ProgressBar:** trilho de 8px em `#E5E8EA` com preenchimento ciano.

### EmptyState
Ilustração, título de 20px Bold, descrição e uma ação para criar o primeiro item, tudo centralizado e com padding de 32px.

### BulkActions
Barra navy com "N selecionados", a ação "Limpar seleção" e os botões de ação em massa. Abaixo dela, pode haver uma barra cinza para selecionar todos os itens.

---

## 13. Qual componente usar

```
Notificar
├─ Crítico, sistema instável ou risco de perda de dados → Alert (fixo, não fechável)
├─ Confirmar ação simples → Dialog
├─ Confirmar ação irreversível → Dialog com botão danger e checkbox
├─ Aviso temporário → Toast
└─ Mensagem dentro de formulário → Message

Coletar dado
├─ Texto de uma linha → Input; várias linhas → TextArea
├─ 2 a 3 opções, uma escolha → Radio; várias escolhas → Checkbox
├─ Muitas opções → Select; lista longa com busca → Autocomplete
├─ Data → DatePicker; período → DateRangePicker
├─ Valor em escala → Slider
├─ Ligar ou desligar sem enviar formulário → Switch
└─ Arquivo → Dropfile

Sobrepor
├─ Só confirmar → Dialog
├─ Formulário ou fluxo → Modal
├─ Detalhes ou configurações laterais → Drawer
└─ Contexto de um elemento: só texto → Tooltip; conteúdo rico → Popover

Clicável
├─ Executa uma ação → Button (primário, secundário, terciário ou danger)
└─ Navega → Link

Carregando
├─ Lista ou cards → Skeleton
└─ Ação pontual → Spinner
```

---

## 14. Texto de interface

- Escreva em português do Brasil, com frases curtas e direto ao ponto.
- **Botões:** verbo no infinitivo. Ações duplas seguem o padrão "Salvar e sair". Para desfazer, use só o verbo ("Cancelar", "Excluir").
- **Títulos de modal:** prefira um verbo que descreva o resultado ("Criar campanha").
- **Ajudas:** use verbo e mostre um exemplo ("Use no mínimo 8 letras e números").
- **Erros:** diga o que aconteceu e como resolver, sem culpar a pessoa.
- **Headlines de KV:** fale de benefício, com no máximo 2 linhas no desktop. O trecho de destaque em ciano é o resultado prometido.

---

## 15. Acessibilidade

- Contraste AA em todos os textos. Consulte as combinações aprovadas nas seções 2 e 10.1.
- Foco visível em todo elemento interativo: contorno de 4px em `#0077B2` com 2px de afastamento.
- Áreas de toque com no mínimo 40px (o ideal é 44px).
- Todo label fica ligado ao seu campo. Ajuda e erro se conectam por `aria-describedby`, e campos inválidos levam `aria-invalid`.
- Resultados dinâmicos usam `aria-live="polite"`. Alertas críticos usam `role="alert"`.
- O layout funciona em 390px sem rolagem horizontal e suporta zoom de texto de até 200%.
- Respeite `prefers-reduced-motion`.

---

## 16. Checklist de QA de marca

- [ ] O logo RD Station oficial aparece acima da dobra, na versão certa para o fundo, com altura de pelo menos 32px.
- [ ] O endosso "uma operação TOTVS" é menor que o logo RD Station.
- [ ] O tema está certo para o assunto (Marketing Contínuo só em peças da disciplina).
- [ ] Nenhum hex fora de `tokens.css`.
- [ ] Só as fontes do tema: DM Sans, ou Red Hat Display com Inter Tight.
- [ ] Um único botão primário por tela.
- [ ] Ciano puro só sobre navy. O roxo `#A44DFF` só em texto de 24px ou mais.
- [ ] Cores funcionais e de suporte usadas apenas para o seu fim.
- [ ] Sem rolagem horizontal em 390px, e os grafismos não cobrem texto.
- [ ] Foco visível, labels ligados aos campos e `aria-describedby` em ajuda e erro.
- [ ] Botões com verbo no infinitivo e de 2 a 3 palavras.
