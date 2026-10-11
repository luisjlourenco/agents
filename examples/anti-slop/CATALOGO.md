# Catálogo de slop: os sinais de "feito por IA"

Ferramentas como Claude, Manus, v0, Lovable e Bolt geram interfaces a partir do mesmo repertório: Tailwind, shadcn/ui, Lucide, Inter e a mesma landing page de SaaS. Por isso o resultado é reconhecível em segundos. Este catálogo lista esses sinais (*tells*), cada um com código, severidade, como detectar e a troca correspondente no RD Kit.

**Severidade:**
- **Alta:** uma pessoa reconhece "isso foi feito por IA" sozinha, em menos de 5 segundos. Sempre corrigir.
- **Média:** reforça a sensação de template. Corrigir quando houver mais de um.
- **Baixa:** isolado, é aceitável. Em conjunto, denuncia.

Os códigos com `*` são detectados automaticamente pelo `slop_scan.py`. Os demais exigem inspeção humana ou do agente.

---

## V. Visual

### Cor e superfície

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| V01* | Gradiente roxo → azul, rosa ou ciano (indigo, violet, purple, fuchsia) em hero, header, botão ou banner | Alta | Navy chapado `#001927`/`#002233`. A cor entra pela geometria do KV ou pela digital do Marketing Contínuo, não por gradiente de fundo |
| V02* | Texto em gradiente (`background-clip: text`) na headline | Alta | Peso misto: trecho em ExtraBold branco e trecho em ciano chapado (`title_highlight`) |
| V03* | Paleta Tailwind padrão (`#6366F1`, `#4F46E5`, `#7C3AED`, `#8B5CF6`, `#0F172A`, `#F8FAFC`, `#10B981`…) | Média | Somente os tokens de `tokens.css` |
| V04* | Blobs ou orbs desfocados (blur de 40px ou mais), aurora ou mesh gradient atrás do hero | Alta | Grafismo de borda: geometria triangular, digital ou listras diagonais |
| V05* | Glassmorphism: `backdrop-filter: blur` com fundo translúcido e borda branca de 10–20% | Média | Superfície sólida: branco, navy elevado `#0B2C4A` ou cinza `#EFEFEF` |
| V06 | Dark mode slate ou zinc com acento neon e *glow* | Média | Navy de marca, sem glow. Ciano só como cor de texto ou detalhe |
| V07* | Fundo de grid quadriculado ou de pontos com fade radial | Média | Fundo chapado. A textura, quando houver, é o grafismo da marca |

### Tipografia

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| V08* | Inter, Geist ou system-ui em tudo, sem fonte de marca | Média (alta se a marca define outra) | DM Sans; ou Red Hat Display com Inter Tight no tema Marketing Contínuo |
| V09* | Headline gigante centralizada, `tracking-tight`, com uma palavra em gradiente | Média | Headline alinhada à esquerda, no máximo 16 caracteres por linha, destaque em ciano chapado |
| V10* | Pílula ou badge acima do título ("✨ Novo: …", "Powered by AI") | Alta | Eyebrow em caixa alta, sem moldura nem emoji |

### Forma e componentes

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| V11* | "Cardificação": tudo em `rounded-xl`/`rounded-2xl`, com `shadow-sm` e borda `slate-200` | Média | Hierarquia por tipografia e espaço. Card só onde agrupa dados, com o raio do componente (16px card, 12px input) |
| V12* | Grade de 3, 4 ou 6 cards de feature idênticos, cada um com ícone num quadrado pastel | Alta | Lista com números reais, layout assimétrico ou `.mc-card` com barra de cor e conteúdo concreto |
| V13* | Ícones Lucide genéricos (Sparkles, Zap, Rocket, Shield, CheckCircle) ou emoji fazendo papel de ícone | Média | Material Symbols Rounded peso 600, ou ícone bicolor da marca |
| V14* | Todo card sobe no hover (`translateY`) com sombra; `transition: all 300ms` | Baixa | Hover só em elemento clicável, com a duração do token (100–200ms) |
| V15* | Toda seção entra com *fade-in-up* ao rolar | Baixa | Movimento só para mudança de estado (resultado calculado, toast) |

### Imagem

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| V16 | Imagem gerada por IA: pele plástica, 3D brilhoso, cérebro ou rede neural luminosa, mão de robô, isométrico genérico | Alta | Foto real em fundo neutro claro, recortada reta, ao lado de bloco ciano chapado |
| V17* | Placeholder ou avatar genérico (pravatar, ui-avatars, picsum, Unsplash aleatório) e logos fictícios (Acme, Globex, Initech) | Alta | Clientes reais com autorização, ou remover a seção |
| V18 | Mockup de dashboard inventado no hero, inclinado e com glow | Média | Captura real do produto ou do resultado da ferramenta |

### Dados e ferramenta

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| V19* | Todo KPI com "+12,5% vs. mês passado" e seta verde; gráfico com as cores padrão da biblioteca (Recharts `#8884d8`/`#82ca9d`, Chart.js `#36A2EB`/`#FF6384`) ou área com gradiente padrão | Média | DataBlock com dado real; variação só quando existe base comparável; paleta de suporte |
| V20* | Selo ou rastro da ferramenta geradora: "Made with …", "Built with …", título de aba "Vite + React" ou "React App", favicon padrão, domínio de preview | Alta | Título, favicon e domínio próprios; remover o selo |
| V21* | "Cara de IA" na ferramenta: botão com ✨, "Gerar com IA", "Analisando com IA…" sem necessidade | Média | Rótulo pelo resultado ("Calcular meu ROI"); IA só aparece quando for o diferencial |

---

## E. Estrutura

| Código | Sinal | Sev. | Troca no RD Kit |
|---|---|---|---|
| E01* | Sequência canônica de landing: hero centralizado → logos → 3 features → "como funciona" em 3 passos numerados em círculos → depoimentos → 3 planos com o do meio "Mais popular" → FAQ → banner CTA em gradiente → rodapé de 4 colunas | Alta (5 blocos ou mais) | Comece pelo que a pessoa veio fazer (a ferramenta acima da dobra) e só mantenha as seções que têm conteúdo próprio |
| E02* | Linha de estatísticas redondas ("10k+ usuários", "99,9% uptime", "24/7") | Média | Um número verificável, com fonte, ou nenhum |
| E03* | Depoimentos com 5 estrelas, nome e cargo inventados | Alta | Citação real com nome, empresa e foto autorizada |
| E04* | Hero com dois botões: primário e "Saiba mais" fantasma | Baixa | Um único primário. O secundário, se houver, é um link de navegação |
| E05 | Coluna única centralizada `max-w-4xl` do começo ao fim | Baixa | Grid de 12 colunas, com assimetria intencional |
| E06* | Rodapé com "© 2024 … Todos os direitos reservados", ano errado ou links `#` | Média | Rodapé RD Station com o endosso "uma operação TOTVS" e links reais |
| E07 | Todas as seções com o mesmo ritmo: eyebrow, H2 e parágrafo centralizados, `py-24` | Baixa | Ritmo variado conforme o conteúdo, com títulos alinhados à esquerda |

---

## T. Texto

| Código | Sinal | Sev. | Troca |
|---|---|---|---|
| T01* | Verbos de hype: transforme, potencialize, alavanque, desbloqueie, revolucione, eleve, impulsione | Média | Verbo do resultado concreto: "calcule", "descubra quanto", "compare" |
| T02* | Promessa vazia: "solução completa", "tudo em um só lugar", "experiência única", "simples e rápido", "sem complicação" | Média | O que a ferramenta entrega, em números ou em uma tarefa |
| T03* | Estrutura "não é apenas X, é Y" / "mais do que X" | Média | Afirme Y diretamente |
| T04 | Tríades automáticas (três adjetivos ou benefícios), repetidas no texto | Baixa | Um benefício, bem provado |
| T05* | Travessões em excesso (mais de 3 por mil palavras) e dois-pontos dramáticos | Baixa | Ponto final ou vírgula |
| T06* | Emoji como marcador ou dentro de títulos (🚀 ✨ 💡 ✅) | Média | Sem emoji em interface institucional |
| T07* | Title Case em português ("Como Funciona", "Nossos Recursos") | Média | Só a primeira letra maiúscula ("Como funciona") |
| T08* | CTA genérico: "Saiba mais", "Comece agora", "Clique aqui", "Get started" | Média | Verbo no infinitivo com o objeto ("Calcular meu ROI", "Ver meu potencial") |
| T09* | Aberturas e fechamentos de IA: "No cenário atual", "Em um mundo cada vez mais", "Mais do que nunca", "Pronto para transformar…?", "Em suma" | Média | Comece pelo fato e termine pela ação |
| T10* | Inglês residual em interface em português ("Get started", "Powered by AI", "insights acionáveis") | Baixa | Português do Brasil |
| T11* | Números redondos sem fonte ("10x", "300%", "99,9%", "+10 mil") | Alta | Dado com fonte, ou cálculo da própria ferramenta |
| T12* | Palavras-muleta: robusto, inovador, de ponta, perfeitamente, sem esforço, jornada, ecossistema | Baixa | Palavra específica do domínio |

---

## Slop Score

Pontos por achado: alta = 10, média = 5, baixa = 2. O total é limitado a 100.

| Score | Diagnóstico | Ação |
|---|---|---|
| 0–15 | **Autoral.** Parece feito para a marca | Publicar |
| 16–35 | **Traços de IA.** Alguns sinais isolados | Corrigir os de severidade alta |
| 36–60 | **Slop evidente.** Leitor atento percebe | Refazer as seções sinalizadas |
| 61–100 | **Template de IA.** Reconhecível à primeira vista | Regerar com o prompt anti-slop e o RD Kit |

Uma ressalva: os achados de cor e tipografia (V01, V03, V08) somam pontos mesmo quando a cor ou fonte é da própria marca. Ao rodar com `--tokens tokens.css`, os valores do RD Kit entram como permitidos.
