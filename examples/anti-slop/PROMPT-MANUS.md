# Prompts anti-slop para o Manus

Dois blocos. O primeiro **previne**: cole no início de qualquer pedido de site ou ferramenta. O segundo **corrige**: preencha com os achados do `slop_scan.py` e envie numa sessão já existente.

---

## 1. Bloco de prevenção (colar antes de gerar)

```text
RESTRIÇÕES VISUAIS E DE TEXTO (obrigatórias)

Identidade: siga o design system RD Station anexado (tokens.css, components.css, GUIDELINES.md e os logos de brand/). Use apenas as cores, fontes, raios e espaçamentos dos tokens. Logo oficial RD Station acima da dobra; endosso "uma operação TOTVS" no rodapé.

Proibido:
- Gradientes de fundo roxo, azul, rosa ou ciano; texto em gradiente; blobs ou orbs desfocados; glassmorphism; fundo de grid ou pontos.
- Paleta padrão do Tailwind (indigo, violet, purple, slate, zinc) e a fonte Inter. Use DM Sans (ou Red Hat Display + Inter Tight no tema Marketing Contínuo).
- Pílula ou badge acima do título ("✨ Novo…"). Headline gigante centralizada.
- Grade de 3 ou 4 cards de feature idênticos com ícone em quadrado colorido. Ícones Lucide genéricos (Sparkles, Zap, Rocket, Shield). Emoji como ícone ou em títulos.
- Hover que levanta todos os cards; animação de entrada em todas as seções.
- Listas com ícone de check em cada item, emoji como marcador, passos em círculos numerados, tags e badges espalhados, card dentro de card, bento grid, caixas com borda colorida à esquerda, cards de estatística e linha do tempo com bolinhas. Prefira texto corrido, listas simples e um único nível de contêiner.
- Imagens geradas por IA, avatares placeholder, logos fictícios, mockup de dashboard inventado.
- Sequência padrão de landing (logos, features, como funciona em 3 passos, depoimentos, 3 planos, FAQ, banner final). Inclua só as seções com conteúdo real que eu fornecer.
- Estatísticas redondas ("10k+", "99,9%", "24/7"), depoimentos de 5 estrelas e qualquer número sem fonte.
- Selo "Made with Manus", título de aba genérico e favicon padrão.

Texto:
- Português do Brasil, frases curtas e concretas. Sem "transforme", "potencialize", "alavanque", "solução completa", "tudo em um só lugar", "não é apenas X, é Y", "no cenário atual", "pronto para…?".
- Títulos com só a primeira letra maiúscula. Botões com verbo no infinitivo e objeto ("Calcular meu ROI"), nunca "Saiba mais" ou "Comece agora". Um único botão primário por tela.
- Sem travessões em excesso e sem emoji.

Comece pela tarefa principal da página (a ferramenta acima da dobra) e use alinhamento à esquerda.
```

---

## 2. Modelo de prompt de correção

Preencha com os achados do relatório (o código e a evidência vêm direto do `slop_scan.py`). Mantenha o pedido cirúrgico: diga o que **não** mudar.

```text
Corrija apenas os pontos abaixo. Não altere a estrutura de dados, os cálculos, os textos que não estão listados nem as seções que não estão citadas.

1. [V01] O hero usa gradiente indigo → pink (linear-gradient(135deg, #4f46e5, #7c3aed, #ec4899)).
   → Troque por fundo navy chapado #001927. Adicione a geometria triangular do KV no canto superior direito, sem cobrir texto.
2. [V10] Há uma pílula "✨ Novo: IA integrada" acima do H1.
   → Substitua por eyebrow em caixa alta, 14px bold, cor #00DBFF, sem borda, fundo ou emoji.
3. [V12] A seção de recursos é uma grade de 3 cards idênticos com ícone.
   → Transforme em lista vertical com os 3 resultados que a ferramenta calcula, cada um com o valor de exemplo.
4. [E03] Os depoimentos com 5 estrelas são inventados.
   → Remova a seção inteira.
5. [T08] Os botões do hero são "Comece agora" e "Saiba mais".
   → Deixe um único botão primário "Calcular meu ROI" (fundo #002233, texto #00DBFF). Remova o segundo.

Depois de corrigir, confirme que o título da aba é "[Nome da ferramenta] | RD Station" e que o rodapé tem o logo RD Station e "uma operação TOTVS".
```

**Dicas:**
- Corrija no máximo de 5 a 7 itens por rodada. Prompts longos fazem o gerador reescrever o que estava bom.
- Ataque primeiro os de severidade alta. Muitas vezes eles arrastam os de severidade média junto (tirar o gradiente costuma resolver V01, V02 e V04 de uma vez).
- Depois de cada rodada, rode o scanner de novo e compare os Slop Scores.
