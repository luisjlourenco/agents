# RD Kit: design system para ferramentas RD Station em escala

Kit para produzir calculadoras, diagnósticos, dashboards e páginas de evento com a mesma identidade visual da RD Station (uma operação TOTVS). É operado pelo agente [RD Station UI Designer](../../design/design-rd-station-ui-designer.md).

**Princípio:** uma ferramenta nova é um manifesto JSON, não um HTML novo. O visual vem do sistema, então a centésima ferramenta sai tão fiel à marca quanto a primeira.

## Uso rápido

```bash
cd examples/rd-station-design-system
python3 generate.py                                   # gera todas as ferramentas de tools/
python3 generate.py tools/calculadora-roi-marketing.json             # tema rd-station
python3 generate.py tools/potencial-da-base-marketing-continuo.json  # tema marketing-continuo
open dist/calculadora-roi-marketing.html
```

Só usa a biblioteca padrão do Python 3. A saída é um arquivo HTML único, com CSS e logos embutidos (só as fontes DM Sans, Red Hat Display e Inter Tight vêm do Google Fonts).

## Camadas

| Camada | Arquivo | O que define |
|---|---|---|
| 1. Tokens Tangram | `tokens.css` | Cores primárias, neutras, funcionais e de suporte; DM Sans; grid de 8px; raios; elevação; z-index; motion |
| 2. Key Visual | `tokens.css` (`--kv-*`) | Navy `#001927`, ciano `#00DBFF`, lime `#C3F628`, gradiente violeta Tangram, hero radial |
| 2b. Endosso TOTVS | `tokens.css` (`--totvs-*`) | Logo e assinatura "uma operação TOTVS". Paleta institucional pendente (ver abaixo) |
| 2c. Tema Marketing Contínuo | `tokens.css` (`[data-theme="marketing-continuo"]`) | Red Hat Display + Inter Tight, navy `#002233`, roxo `#A44DFF`/`#7B2FFF`, ciano `#00DBFF`, lime `#D9FC68`, listras e digital |
| 3. Componentes | `components.css` | Button (região × kind), Input, Card, DataBlock, Tag, Badge, Alert, Message, Toast, Table, Steps, Skeleton |
| 4. Padrões | `components.css` | Shell do produto logado, topbar, hero KV, painel sobreposto, rodapé com endosso TOTVS |
| 5. Marca | `brand/` | Logos oficiais, extraídos do componente Brand do Tangram |
| 6. Produção | `templates/`, `tools/`, `generate.py` | Template com placeholders, manifestos e gerador |

Tokens marcados `[derivado]` em `tokens.css` não constam da tabela pública do Tangram (ex.: curvas de sombra, hover do botão primário). Valide com o time de Design antes de usar fora do kit.

## Logo oficial

| Fundo | Arquivo |
|---|---|
| Claro (branco, cinza) | `brand/rd-station-logo.svg` (navy `#002233`) |
| Navy ou escuro | `brand/rd-station-logo-on-dark.svg` (branco) |
| Navbar do produto logado | `brand/rd-station-logo-cyan.svg` (ciano `#00DBFF`), só no shell Tangram |
| Endosso TOTVS, claro | `brand/totvs-logo.svg` |
| Endosso TOTVS, escuro | `brand/totvs-logo-on-dark.svg` |

- Altura de 32px (mínimo de 20px em endosso), com 16px de respiro.
- Nunca redesenhar, esticar, recolorir fora dessas versões, aplicar efeito ou trocar o RD Station pelo logo TOTVS.
- A TOTVS entra como endosso, com a assinatura "uma operação TOTVS": canto superior direito em capas e slides, rodapé em ferramentas. Sempre menor que o RD Station.

## Temas

| Tema | Quando usar | Manifesto |
|---|---|---|
| `rd-station` (padrão) | Ferramentas institucionais e de produto | sem `theme` |
| `marketing-continuo` | Tudo que comunica a disciplina Marketing Contínuo | `"theme": "marketing-continuo"` |

Regras do tema Marketing Contínuo, extraídas do guia visual oficial:

- O roxo `#A44DFF` fica para superfícies, grafismos e texto de 24px ou mais (4,13:1 com branco). Botões e texto pequeno usam `#7B2FFF` (5,69:1).
- Aberturas de seção levam numeral roxo em itálico black e título ciano em itálico, caixa alta (`.mc-section`).
- Headlines misturam pesos: um trecho extra-bold e outro light em ciano (`title_highlight`, `.mc-headline`).
- Grafismos (digital roxa ou lime, listras diagonais ciano) ficam nas bordas, nunca atrás de texto.
- Componentes extras: `.mc-card` (barra de cor no topo), `.mc-chip` (ponto lime), `.mc-band` (faixa-rótulo) e `.mc-impact` (painel roxo de frase de impacto).

## Pendências de fonte oficial

O ambiente em que este kit foi montado não teve acesso de rede a `marca.totvs.com`, `rdstation.com` nem ao brand system no zeroheight. Por isso:

- **A paleta e a tipografia institucionais da TOTVS ainda não estão no kit.** A TOTVS aparece só como logo de endosso. Antes de peças co-branded, registre os valores oficiais na camada 2b.
- **Os tokens do site e do brand system** vêm do Tangram e do guia Marketing Contínuo. Confira contra o zeroheight e ajuste os itens `[derivado]`.

## Manifesto de ferramenta

| Campo | Obrigatório | Descrição |
|---|---|---|
| `slug` | sim | Nome do arquivo de saída |
| `title` / `title_highlight` | sim / não | H1; o trecho em destaque fica em ciano |
| `subtitle`, `eyebrow` | sim / não | Apoio do hero |
| `inputs[]` | sim | `id`, `label`, `type` (`number`/`text`), `placeholder`, `help`, `required` |
| `outputs[]` | sim | `id`, `label`, `formula` (JS sobre ids de inputs e saídas anteriores), `format` (`currency`, `percent`, `number`) |
| `insight` | não | Frase com `${id}` das saídas, já formatadas |
| `theme` | não | `rd-station` (padrão) ou `marketing-continuo` |
| `primary_cta`, `secondary_cta` | não | Rótulo do submit e link do topo |
| `form_title`, `result_title`, `privacy_note` | não | Textos de apoio |

As fórmulas rodam no navegador. Elas são escritas pelo time (conteúdo confiável) e nunca devem vir de input de visitante.

## Checklist de QA

- [ ] Logo RD Station oficial acima da dobra, na versão certa para o fundo
- [ ] Endosso "uma operação TOTVS"
- [ ] Tema correto para o assunto
- [ ] Nenhum hex fora de `tokens.css`
- [ ] Um único botão primário por tela
- [ ] Contraste AA: ciano puro só sobre navy; em fundo claro, usar `--primary-text`
- [ ] Sem scroll horizontal em 390px; as peças do KV não cobrem texto
- [ ] Foco visível; label, ajuda e erro ligados por `aria-describedby`

## Fontes

- Tangram Design System: https://tangram.rdstation.com.br
- Guia visual "Marketing Contínuo: Tudo sobre a Disciplina de Crescimento" (cores amostradas do PDF oficial)
- A validar: https://marca.totvs.com/identidade-visual/ · https://www.rdstation.com/ · https://zeroheight.com/8b3388065/p/61eb76-brand-system-rd-station
- Repositório Tangram: https://github.com/ResultadosDigitais/tangram
