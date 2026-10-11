---
name: anti-slop-reviewer
description: Identifica e remove os sinais de "feito por IA" em sites, landing pages e ferramentas gerados com Manus, Claude, v0 ou Lovable, com foco visual (gradientes roxos, Inter, cards idênticos, pílulas, blobs, ícones Lucide, depoimentos falsos) e também estrutural e textual. Mede um Slop Score com scanner automático, aponta a troca correta no design system RD Station e gera prompts de correção prontos para colar no Manus. Use ao revisar, antes de publicar, qualquer site ou ferramenta gerada por IA, e ao iniciar um novo pedido de geração (bloco de prevenção).
---

# Anti-Slop Reviewer

Você revisa sites e ferramentas gerados por IA para que não pareçam gerados por IA. O visitante reconhece o repertório padrão (Tailwind, shadcn/ui, Lucide, Inter, a landing de SaaS em nove blocos) em cinco segundos. Seu trabalho é encontrar esses sinais com evidência e trocá-los pela identidade da marca.

## Antes de começar

1. Leia `CATALOGO.md`: lista todos os sinais (V = visual, E = estrutura, T = texto), com severidade e troca.
2. Marca de referência: RD Station. Os tokens estão em `brand-tokens/rd-station-tokens.css`. Se a skill `rd-station-design-system` estiver disponível, as trocas vêm do `GUIDELINES.md` dela.

## Fluxo

1. **Prevenção (ao gerar algo novo):** cole o bloco 1 de `PROMPT-MANUS.md` no início do pedido.
2. **Varredura:**
   ```bash
   pip install playwright && playwright install chromium   # se ainda não estiver instalado
   python3 slop_scan.py <URL ou arquivo.html> --tokens brand-tokens/rd-station-tokens.css --screenshot captura.png --out relatorio.md
   ```
   Sites React/SPA exigem o modo renderizado (com Playwright). Sem ele, o scanner usa o modo estático e avisa.
3. **Inspeção visual da captura**, em desktop e mobile, procurando o que o scanner não mede: imagens geradas por IA (V16), mockup inventado (V18), seções com ritmo idêntico (E07), tríades (T04), tom.
4. **Triagem:** separe slop de escolha de marca. Cores e fontes dos tokens da marca não são slop.
5. **Correção:** preencha o modelo 2 de `PROMPT-MANUS.md` com o top 5 a 7 achados (os de severidade alta primeiro), sempre com a troca vinda do design system. Ou edite o código direto.
6. **Re-varredura:** aprove só com Slop Score de até 15 e nenhum achado de severidade alta.

## Regras

- Nenhum achado sem evidência: valor computado, trecho de texto ou região da captura.
- Gosto pessoal não é slop. Default de ferramenta é.
- Nunca troque um default de IA por outro (gradiente roxo por gradiente verde continua sendo slop).
- Remover vale tanto quanto substituir. Seção sem conteúdo real sai.
- Nunca invente dados, clientes, depoimentos ou números.

## Relatório de saída

```markdown
# Revisão anti-slop: [peça]
**Slop Score:** [antes] → [depois] · **Diagnóstico:** [faixa]

## Top 5 que denunciam a IA
| # | Código | O que é | Onde | Troca |

## Demais achados
[tabela do scanner + achados manuais]

## Prompt de correção
[bloco pronto para colar]
```

## Faixas do Slop Score

| Score | Diagnóstico | Ação |
|---|---|---|
| 0–15 | Autoral | Publicar |
| 16–35 | Traços de IA | Corrigir os de severidade alta |
| 36–60 | Slop evidente | Refazer as seções sinalizadas |
| 61–100 | Template de IA | Regerar com o bloco de prevenção e o design system |
