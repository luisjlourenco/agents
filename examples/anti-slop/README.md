# Anti-slop: revisão de sites e ferramentas gerados por IA

Kit dos agentes [Anti-Slop Reviewer](../../design/design-anti-slop-reviewer.md) (texto, estrutura e visual) e [Visual Slop Reviewer](../../design/design-visual-slop-reviewer.md) (só visual, com testes de percepção e captura anotada). Eles identificam os sinais visuais, estruturais e de texto que denunciam uma interface feita por Claude, Manus, v0, Lovable e afins, dá uma nota (Slop Score) e gera o prompt de correção.

## Uso rápido

```bash
pip install playwright && playwright install chromium   # uma vez
python3 slop_scan.py https://minha-ferramenta.manus.space \
  --tokens ../rd-station-design-system/tokens.css \
  --screenshot captura.png --out relatorio.md
```

| Opção | Efeito |
|---|---|
| `--tokens arquivo.css` | Cores e fontes do design system deixam de contar como slop |
| `--screenshot arquivo.png` | Captura de página inteira, para a inspeção visual |
| `--out relatorio.md` / `--json relatorio.json` | Grava o relatório |
| `--static` | Não abre navegador: analisa só o HTML (não funciona em SPA/React) |
| `--only visual` | Só sinais visuais (V*) e de layout (E04, E05, E07): modo do Visual Slop Reviewer |
| `--annotate arquivo.png` | Captura com cada sinal visual marcado e rotulado sobre a página |

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `CATALOGO.md` | Todos os sinais (V = visual, E = estrutura, T = texto), com severidade, detecção e troca no RD Kit |
| `slop_scan.py` | Scanner (Python 3; Playwright opcional) |
| `patterns.json` | Listas editáveis: cores Tailwind, fontes genéricas, frases, CTAs, rastros de geradores |
| `PROMPT-MANUS.md` | Bloco de prevenção para colar antes de gerar e modelo de prompt de correção |
| `fixtures/slop-landing.html` | Página com slop proposital, para testar o scanner |
| `SKILL.md` / `SKILL-VISUAL.md` | Instruções das skills para o Manus (revisor geral e revisor visual) |
| `package_manus.py` | Gera os dois `.zip` de skill para o Manus |

## Calibração

| Página | Modo | Slop Score |
|---|---|---|
| `fixtures/slop-landing.html` | renderizado e estático | 100/100 (Template de IA) |
| RD Kit `dist/calculadora-roi-marketing.html` | renderizado | 0/100 (Autoral) |
| RD Kit `dist/potencial-da-base-marketing-continuo.html` | renderizado | 0/100 (Autoral) |
| `fixtures/slop-landing.html` com `--only visual` | renderizado | 100/100, 16 sinais visuais marcados na captura |

## Limites

- O scanner mede o que é mensurável. Imagens geradas por IA (V16), mockups inventados (V18), ritmo de seções (E07), tríades (T04) e tom de voz exigem revisão visual. Esse é o papel do agente.
- As listas de `patterns.json` refletem os defaults observados em ferramentas de geração em 2025–2026. Atualize quando surgir um padrão novo.
