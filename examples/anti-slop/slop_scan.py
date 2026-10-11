#!/usr/bin/env python3
"""slop_scan — detecta os sinais de interface "feita por IA" em sites e ferramentas.

Uso:
    python3 slop_scan.py https://meusite.manus.space
    python3 slop_scan.py pagina.html --tokens ../rd-station-design-system/tokens.css
    python3 slop_scan.py URL --json relatorio.json --screenshot captura.png
    python3 slop_scan.py URL --static        # sem navegador: só analisa o HTML bruto
    python3 slop_scan.py URL --only visual --annotate anotado.png   # revisor visual

Modo renderizado (padrão) usa Playwright e mede o que o visitante vê: cores
computadas, fontes, gradientes, blur, grids de cards, hover, textos. Sites em
React/SPA (o padrão do Manus, Lovable e v0) só são analisáveis neste modo.
Se o Playwright não estiver instalado, cai automaticamente no modo estático.

Os códigos dos achados (V01, E03, T08…) são os do CATALOGO.md.
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEV_POINTS = {"alta": 10, "media": 5, "baixa": 2}
SEV_LABEL = {"alta": "Alta", "media": "Média", "baixa": "Baixa"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u2604\u2607-\u27BF\u2B50\u2705\u274C\u2728]")  # sem ★ ☆

TITLES = {
    "V01": "Gradiente roxo/azul/rosa de IA", "V02": "Texto em gradiente", "V03": "Paleta Tailwind padrão",
    "V04": "Blobs desfocados atrás do conteúdo", "V05": "Glassmorphism", "V07": "Fundo de grid ou pontos",
    "V08": "Fonte genérica (Inter/system)", "V09": "Headline centralizada gigante", "V10": "Pílula acima do título",
    "V11": "Cardificação", "V12": "Grade de cards de feature idênticos", "V13": "Ícones genéricos (Lucide/emoji)",
    "V14": "Hover que levanta tudo / transition: all", "V15": "Animação de entrada em toda seção",
    "V17": "Imagens placeholder ou logos fictícios", "V19": "Dashboard e gráfico padrão", "V20": "Rastro da ferramenta geradora",
    "V21": "Cara de IA na interface", "V22": "Lista com ícone em cada item", "V23": "Emoji como marcador",
    "V24": "Passos em círculos numerados", "V25": "Excesso de tags e badges", "V26": "Card dentro de card",
    "V27": "Bento grid", "V28": "Caixas de destaque com borda lateral", "V29": "Cards de estatística", "V30": "Linha do tempo com bolinhas", "E01": "Sequência canônica de landing de IA", "E02": "Linha de estatísticas redondas",
    "E03": "Depoimentos genéricos 5 estrelas", "E04": "Hero com primário + 'Saiba mais'", "E06": "Rodapé genérico",
    "T01": "Verbos de hype", "T02": "Promessa vazia", "T03": "'Não é apenas X, é Y'", "T05": "Excesso de travessões",
    "T06": "Emoji em títulos e marcadores", "T07": "Title Case em português", "T08": "CTA genérico",
    "T09": "Abertura/fechamento de IA", "T10": "Inglês residual", "T11": "Números redondos sem fonte", "T12": "Palavras-muleta",
}

COLLECT_JS = r"""
() => {
  const vis = el => { const r = el.getBoundingClientRect(); const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0.05; };
  const all = Array.from(document.querySelectorAll('body *')).slice(0, 6000);
  const out = { title: document.title, favicon: (document.querySelector('link[rel*=icon]') || {}).href || '',
    text: document.body ? document.body.innerText : '', fonts: {}, colors: {}, gradients: [], gradientText: [],
    backdrop: 0, blobs: 0, svgColors: {}, gridBg: 0, cards: 0, pills: [], lucide: [], buttons: [], imgs: [], headings: [],
    hoverLift: 0, transitionAll: 0, fadeKeyframes: [], featureGrids: [], scripts: [], classes: '' };
  const add = (o, k) => { if (k) o[k] = (o[k] || 0) + 1; };
  const box = r => ({ x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY), w: Math.round(r.width), h: Math.round(r.height) });
  out.marks = [];
  const rgb2hex = c => { const m = c && c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);
    if (!m || (m[4] !== undefined && parseFloat(m[4]) < 0.15)) return null;
    return '#' + [m[1], m[2], m[3]].map(x => (+x).toString(16).padStart(2, '0')).join(''); };
  for (const el of all) {
    if (!vis(el)) continue;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    const hasText = Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 1);
    if (hasText) { add(out.fonts, s.fontFamily.split(',')[0].replace(/["']/g, '').trim().toLowerCase()); add(out.colors, rgb2hex(s.color)); }
    add(out.colors, rgb2hex(s.backgroundColor));
    if (parseFloat(s.borderTopWidth) > 0) add(out.colors, rgb2hex(s.borderTopColor));
    const bi = s.backgroundImage;
    if (bi && bi.includes('gradient')) {
      out.gradients.push({ tag: el.tagName, w: Math.round(r.width), h: Math.round(r.height), bg: bi.slice(0, 300) });
      if (r.width * r.height > 4000) out.marks.push({ kind: 'gradient', bg: bi.slice(0, 300), ...box(r) });
      const bs = s.backgroundSize;
      if (/repeating|radial-gradient\([^)]*1px|linear-gradient[\s\S]*linear-gradient/.test(bi) && /^\d+px/.test(bs) && parseFloat(bs) <= 80) out.gridBg++;
    }
    const clip = s.backgroundClip + ' ' + (s.webkitBackgroundClip || '');
    if (clip.includes('text') && bi.includes('gradient')) { out.gradientText.push(el.innerText.slice(0, 80)); out.marks.push({ kind: 'gradientText', ...box(r) }); }
    if (s.backdropFilter && s.backdropFilter.includes('blur')) { out.backdrop++; out.marks.push({ kind: 'backdrop', ...box(r) }); }
    const blur = (s.filter || '').match(/blur\(([\d.]+)px/);
    if (blur && parseFloat(blur[1]) >= 40) { out.blobs++; out.marks.push({ kind: 'blob', ...box(r) }); }
    const rad = parseFloat(s.borderTopLeftRadius);
    if (rad >= 12 && rad <= 28 && s.boxShadow !== 'none' && r.width > 120 && r.height > 80) out.cards++;
    if (rad >= r.height / 2 - 1 && r.height < 40 && r.width < 420 && hasText && (parseFloat(s.borderTopWidth) > 0 || rgb2hex(s.backgroundColor)))
      { out.pills.push({ text: el.innerText.trim().slice(0, 60), top: Math.round(r.top + scrollY) }); out.marks.push({ kind: 'pill', text: el.innerText.trim().slice(0, 60), ...box(r) }); }
    if (/^(A|BUTTON)$/.test(el.tagName) && el.innerText.trim())
      out.buttons.push({ text: el.innerText.trim().slice(0, 60), top: Math.round(r.top + scrollY), filled: !!rgb2hex(s.backgroundColor) });
    if (/^H[1-3]$/.test(el.tagName)) out.headings.push({ tag: el.tagName, text: el.innerText.trim().slice(0, 140),
      align: s.textAlign, size: parseFloat(s.fontSize), top: Math.round(r.top + scrollY), font: s.fontFamily });
    if (el instanceof SVGElement && /^(path|rect|circle|line|polyline|polygon)$/i.test(el.tagName)) {
      add(out.svgColors, rgb2hex(s.fill)); add(out.svgColors, rgb2hex(s.stroke)); }
    if (el.tagName === 'svg' || el.tagName === 'SVG') { const c = el.getAttribute('class') || ''; if (c.includes('lucide')) { out.lucide.push(c); out.marks.push({ kind: 'lucide', cls: c, ...box(r) }); } }
    const kids = Array.from(el.children).filter(vis);
    if ((s.display.includes('grid') || s.display.includes('flex')) && kids.length >= 3 && kids.length <= 8) {
      const rs = kids.map(k => k.getBoundingClientRect());
      const sameW = rs.every(x => Math.abs(x.width - rs[0].width) < rs[0].width * 0.08);
      const sameH = rs.every(x => Math.abs(x.height - rs[0].height) < rs[0].height * 0.2);
      const rowish = new Set(rs.map(x => Math.round(x.top / 10))).size <= Math.ceil(kids.length / 2);
      const iconTitle = kids.every(k => (k.querySelector('svg, img') || EMOJI_RE.test(k.innerText.slice(0, 4))) && k.innerText.trim().split(/\s+/).length >= 4);
      if (sameW && sameH && rowish && iconTitle && rs[0].width > 140) { out.featureGrids.push({ n: kids.length, sample: kids[0].innerText.trim().slice(0, 80) }); out.marks.push({ kind: 'featureGrid', ...box(r) }); }
    }
  }
  // ---- Marcadores e contêineres (V22–V30): segunda passada sobre os elementos visíveis ----
  const visEls = all.filter(vis);
  const txt = e => (e && typeof e.innerText === 'string' ? e.innerText : (e && e.textContent) || '');
  const opaque = s => !!rgb2hex(s.backgroundColor);
  const sat = c => { const m = c && c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/); if (!m) return 0; const v = [+m[1], +m[2], +m[3]]; return Math.max(...v) - Math.min(...v); };
  const directText = el => Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
  const isCard = el => { const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return parseFloat(s.borderTopLeftRadius) >= 8 && (parseFloat(s.borderTopWidth) > 0 || s.boxShadow !== 'none') && opaque(s) && r.width > 80 && r.height > 48; };
  const cards = new Set(visEls.filter(isCard));
  Object.assign(out, { checkLists: [], emojiMarkers: [], numCircles: [], tags: [], nested: [], bento: [], callouts: [], statCards: [], dots: [] });
  const CHECK = /^[✓✔✅☑•●▸→➜]/;
  const EMO = /^[\u{1F300}-\u{1FAFF}\u2600-\u2604\u2607-\u2712\u2715-\u27BF\u2B50]/u;  // ✓ ✔ ficam com o V22
  for (const el of visEls) {
    const s = getComputedStyle(el), r = el.getBoundingClientRect(), dt = directText(el);
    // V22: lista em que cada item começa com ícone pequeno ou caractere de check
    const kids = Array.from(el.children).filter(vis);
    if (kids.length >= 3 && !cards.has(el)) {
      const marked = kids.filter(k => { const kr = k.getBoundingClientRect(); if (kr.height > 72) return false;
        const first = k.firstElementChild; const fr = first && first.getBoundingClientRect();
        const iconFirst = first && /^(svg|img|i)$/i.test(first.tagName) && fr.width <= 28 && fr.height <= 28;
        const iconWrap = first && fr.width <= 36 && fr.height <= 36 && first.querySelector('svg') && !txt(first).trim();
        return iconFirst || iconWrap || CHECK.test(txt(k).trim()); });
      if (marked.length >= 3 && marked.length >= kids.length * 0.6) out.checkLists.push({ n: marked.length, sample: txt(marked[0]).trim().slice(0, 60), ...box(r) });
    }
    // V23: emoji como marcador no início de item, título ou parágrafo
    if (/^(LI|H3|H4|H5|P|DT|SPAN|DIV)$/.test(el.tagName) && EMO.test(dt || '') ) out.emojiMarkers.push({ text: dt.slice(0, 50), ...box(r) });
    // V24: círculo com número de etapa
    if (/^\d{1,2}$/.test(txt(el).trim()) && el.children.length <= 1 && r.width >= 24 && r.width <= 72 && Math.abs(r.width - r.height) < 4
        && parseFloat(s.borderTopLeftRadius) >= r.width / 2 - 1 && (opaque(s) || parseFloat(s.borderTopWidth) > 0))
      out.numCircles.push({ n: +txt(el).trim(), ...box(r) });
    // V25: tags e badges em pílula (fora de botões e links)
    if (dt && !/^(A|BUTTON|INPUT|LABEL)$/.test(el.tagName) && r.height >= 16 && r.height <= 34 && r.width < 260
        && parseFloat(s.borderTopLeftRadius) >= r.height / 2 - 1 && dt.split(/\s+/).length <= 4 && (opaque(s) || parseFloat(s.borderTopWidth) > 0))
      out.tags.push({ text: dt.slice(0, 40), ...box(r) });
    // V28: caixa de destaque com borda colorida só à esquerda
    if (parseFloat(s.borderLeftWidth) >= 3 && parseFloat(s.borderTopWidth) === 0 && parseFloat(s.borderRightWidth) === 0 && sat(s.borderLeftColor) > 60 && r.height > 32)
      out.callouts.push({ ...box(r) });
    // V30: bolinhas de linha do tempo
    if (!el.children.length && !txt(el).trim() && r.width >= 6 && r.width <= 20 && Math.abs(r.width - r.height) < 2
        && parseFloat(s.borderTopLeftRadius) >= r.width / 2 - 1 && (opaque(s) || parseFloat(s.borderTopWidth) > 0))
      out.dots.push({ ...box(r) });
    // V27: bento grid (grid de cards com tamanhos diferentes)
    if (s.display.includes('grid') && kids.length >= 4 && kids.every(k => cards.has(k))) {
      const rs = kids.map(k => k.getBoundingClientRect());
      const ws = new Set(rs.map(x => Math.round(x.width / 40))), hs = new Set(rs.map(x => Math.round(x.height / 40)));
      if (ws.size >= 2 || hs.size >= 2) out.bento.push({ n: kids.length, ...box(r) });
    }
  }
  for (const c of cards) {
    // V26: card dentro de card
    let p = c.parentElement;
    while (p && p !== document.body) { if (cards.has(p)) { out.nested.push({ ...box(c.getBoundingClientRect()) }); break; } p = p.parentElement; }
    // V29: card de estatística (número grande sozinho no card)
    const big = Array.from(c.querySelectorAll('*')).find(e => parseFloat(getComputedStyle(e).fontSize) >= 28 && /^[\d.,+%kKmMxX\s/$R]{1,9}$/.test(txt(e).trim()) && /\d/.test(txt(e)));
    if (big && txt(c).trim().split(/\s+/).length <= 8) out.statCards.push({ value: txt(big).trim(), ...box(c.getBoundingClientRect()) });
  }
  for (const sh of Array.from(document.styleSheets)) {
    let rules; try { rules = sh.cssRules; } catch (e) { continue; }
    for (const rule of Array.from(rules || [])) {
      const t = rule.cssText || '';
      if (/:hover[^{]*\{[^}]*translate(Y|3d)?\(\s*-/.test(t) || /:hover[^{]*\{[^}]*--tw-translate-y:\s*-/.test(t)) out.hoverLift++;
      if (/transition(-property)?:\s*all/.test(t) || /transition:\s*[\d.]+m?s(\s+[\w-]+(\([^)]*\))?)?\s*[;}]/.test(t)) out.transitionAll++;
      if (rule.type === 7 && /fade|slide|up|reveal|appear/i.test(rule.name)) out.fadeKeyframes.push(rule.name);
    }
  }
  out.imgs = Array.from(document.images).map(i => { const r = (i.getBoundingClientRect().width ? i : (i.parentElement || i)).getBoundingClientRect();
    return { src: i.currentSrc || i.src, alt: i.alt || '', ...box(r) }; });
  out.scripts = Array.from(document.scripts).map(s => s.src).filter(Boolean);
  out.classes = Array.from(document.querySelectorAll('[class]')).slice(0, 4000).map(e => e.getAttribute('class')).join(' ').slice(0, 200000);
  out.aos = document.querySelectorAll('[data-aos], [data-animate], .animate-fade-in, .fade-in, .reveal').length;
  return out;
}
""".replace("EMOJI_RE", "/[\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF]/u")


OVERLAY_JS = r"""
(marks) => {
  const root = document.createElement('div');
  root.style.cssText = 'position:absolute;left:0;top:0;width:0;height:0;z-index:2147483647;pointer-events:none';
  for (const m of marks) {
    const b = document.createElement('div');
    b.style.cssText = `position:absolute;left:${Math.max(0, m.x)}px;top:${Math.max(24, m.y)}px;width:${Math.max(m.w, 18)}px;height:${Math.max(m.h, 18)}px;` +
      'outline:3px solid #E60F57;outline-offset:2px;background:rgba(230,15,87,.07);box-sizing:border-box';
    const t = document.createElement('span');
    t.textContent = m.w < 140 ? m.label.split(' ')[0] : m.label;  // caixa pequena: só o código
    t.style.cssText = (m.w > 600 ? 'right:-3px;' : 'left:-3px;') + 'position:absolute;top:-24px;background:#E60F57;color:#fff;font:700 12px/16px system-ui,sans-serif;padding:3px 6px;border-radius:4px;white-space:nowrap';
    b.appendChild(t); root.appendChild(b);
  }
  document.documentElement.appendChild(root);
}
"""

# Escopo do revisor visual: todos os sinais V e os de layout da estrutura.
VISUAL_CODES = lambda code: code.startswith("V") or code in ("E04", "E05", "E07")
AI_GRADIENT_RGB = ("99, 102, 241", "139, 92, 246", "168, 85, 247", "124, 58, 237", "236, 72, 153", "147, 51, 234", "79, 70, 229")
AI_GRADIENT_HEX = ("#6366f1", "#8b5cf6", "#a855f7", "#7c3aed", "#ec4899")


def is_ai_gradient(bg, hues):
    bg = bg.lower()
    return any(h in bg for h in hues) or any(c in bg for c in AI_GRADIENT_HEX + AI_GRADIENT_RGB)


def visual_marks(data, findings, pat):
    """Converte os achados visuais em caixas para a captura anotada."""
    codes = {f["code"] for f in findings}
    hues = pat["ai_gradient_hues"]
    rules = {
        "V01": lambda m: m["kind"] == "gradient" and is_ai_gradient(m.get("bg", ""), hues),
        "V02": lambda m: m["kind"] == "gradientText",
        "V04": lambda m: m["kind"] == "blob",
        "V05": lambda m: m["kind"] == "backdrop",
        "V10": lambda m: m["kind"] == "pill" and any(m.get("text", "") in f["evidencia"] for f in findings if f["code"] == "V10"),
        "V12": lambda m: m["kind"] == "featureGrid",
        "V13": lambda m: m["kind"] == "lucide" and any(f"lucide-{n}" in m.get("cls", "") for n in pat["lucide_generic_icons"]),
    }
    marks = []
    for code, match in rules.items():
        if code in codes:
            marks += [dict(m, label=f"{code} {TITLES[code]}") for m in data.get("marks", []) if match(m)][:6]
    extra = {"V22": "checkLists", "V23": "emojiMarkers", "V24": "numCircles", "V25": "tags", "V26": "nested",
             "V27": "bento", "V28": "callouts", "V29": "statCards", "V30": "dots"}
    for code, key in extra.items():
        if code in codes:
            marks += [dict(m, label=f"{code} {TITLES[code]}") for m in data.get(key, [])][:8]
    if "V17" in codes:
        marks += [dict(i, label=f"V17 {TITLES['V17']}") for i in data.get("imgs", [])
                  if any(h in i["src"] for h in pat["placeholder_image_hosts"])][:6]
    return marks


def load_patterns():
    return json.loads((HERE / "patterns.json").read_text(encoding="utf-8"))


def brand_allowlist(tokens_path):
    if not tokens_path:
        return set(), set()
    css = Path(tokens_path).read_text(encoding="utf-8")
    colors = {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", css)}
    fonts = {f.strip().strip('"\'').lower() for decl in re.findall(r"--font-[\w-]+:\s*([^;]+);", css) for f in decl.split(",")}
    fonts |= {f.replace("+", " ").lower() for f in re.findall(r"family=([A-Za-z+]+)", css)}
    return colors, fonts


def find_chromium():
    for pattern in ("/opt/pw-browsers/chromium-*/chrome-linux/chrome", "/opt/pw-browsers/chromium"):
        hits = sorted(glob.glob(pattern))
        if hits and os.path.isfile(hits[-1]):
            return hits[-1]
    return None


def collect_rendered(target, screenshot=None, annotate=None, post=None):
    from playwright.sync_api import sync_playwright
    url = target if re.match(r"https?://", target) else Path(target).resolve().as_uri()
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            browser = p.chromium.launch(executable_path=find_chromium())
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        height = page.evaluate("document.body.scrollHeight")
        for y in range(0, height, 700):  # dispara animações de scroll e lazy-load
            page.evaluate(f"window.scrollTo(0, {y})")
            page.wait_for_timeout(60)
        page.evaluate("window.scrollTo(0, 0)")
        data = page.evaluate(COLLECT_JS)
        if screenshot:
            page.screenshot(path=screenshot, full_page=True)
        if annotate and post:
            page.evaluate(OVERLAY_JS, post(data))
            page.screenshot(path=annotate, full_page=True)
        mobile = browser.new_page(viewport={"width": 390, "height": 844})
        mobile.goto(url, wait_until="networkidle", timeout=60000)
        data["mobile_overflow"] = mobile.evaluate("document.documentElement.scrollWidth") > 392
        browser.close()
    data["mode"] = "renderizado"
    return data


def collect_static(target):
    if re.match(r"https?://", target):
        req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0 slop_scan"})
        html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    else:
        html = Path(target).read_text(encoding="utf-8")
    text = re.sub(r"<(script|style)[\s\S]*?</\1>", " ", html, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    classes = " ".join(re.findall(r'class(?:Name)?="([^"]*)"', html))
    headings = [{"tag": t.upper(), "text": re.sub(r"<[^>]+>", "", h).strip(), "align": "", "size": 0, "top": 0, "font": ""}
                for t, h in re.findall(r"<(h[1-3])[^>]*>([\s\S]*?)</\1>", html, flags=re.I)]
    buttons = [{"text": re.sub(r"<[^>]+>", "", b).strip(), "top": 0, "filled": True}
               for b in re.findall(r"<(?:a|button)[^>]*>([\s\S]*?)</(?:a|button)>", html, flags=re.I)]
    title = (re.search(r"<title>([\s\S]*?)</title>", html, flags=re.I) or [None, ""])[1]
    fonts = Counter(f.lower() for f in re.findall(r"font-family:\s*['\"]?([A-Za-z0-9 ]+)", html))
    fonts.update(f.replace("+", " ").lower() for f in re.findall(r"family=([A-Za-z+]+)", html))
    return {
        "mode": "estático", "title": title, "favicon": "", "text": text, "fonts": dict(fonts),
        "colors": dict(Counter(c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", html))),
        "gradients": [{"bg": g} for g in re.findall(r"(?:linear|radial)-gradient\([^;\"]+", html)],
        "gradientText": ["(classe)"] * len(re.findall(r"bg-clip-text|background-clip:\s*text", html)),
        "backdrop": len(re.findall(r"backdrop-blur|backdrop-filter", html)),
        "blobs": len(re.findall(r"blur-(?:2xl|3xl)|filter:\s*blur\((?:[4-9]\d|\d{3})px", html)),
        "gridBg": len(re.findall(r"bg-grid|bg-dot|background-size:\s*\d{1,2}px\s+\d{1,2}px", html)),
        "cards": len(re.findall(r"rounded-(?:xl|2xl|3xl)[^\"]*shadow|shadow[^\"]*rounded-(?:xl|2xl|3xl)", classes)),
        "pills": [], "lucide": re.findall(r"lucide[-\w]*", html), "buttons": buttons,
        "imgs": [{"src": s, "alt": ""} for s in re.findall(r"<img[^>]+src=\"([^\"]+)", html)], "headings": headings,
        "hoverLift": len(re.findall(r"hover:-translate-y|:hover[^{]*\{[^}]*translateY\(-", html)),
        "transitionAll": len(re.findall(r"transition-all|transition:\s*all", html)),
        "fadeKeyframes": re.findall(r"@keyframes\s+([\w-]*(?:fade|slide|up|reveal)[\w-]*)", html, flags=re.I),
        "featureGrids": [], "scripts": re.findall(r"<script[^>]+src=\"([^\"]+)", html), "classes": classes,
        "aos": len(re.findall(r"data-aos|animate-fade|fade-in", html)), "mobile_overflow": None,
    }


def analyze(d, pat, allowed_colors, allowed_fonts):
    F = []
    def hit(code, sev, evidence):
        F.append({"code": code, "titulo": TITLES.get(code, code), "severidade": sev, "evidencia": evidence})

    text = d.get("text", "")
    low = text.lower()
    classes = d.get("classes", "").lower()
    words = max(1, len(re.findall(r"\w+", text)))
    hues = pat["ai_gradient_hues"]
    tw = pat["tailwind_default_colors"]

    # --- Visual: cor ---
    ai_grads = [g for g in d["gradients"] if is_ai_gradient(g.get("bg", ""), hues)]
    ai_grads += [{"bg": c} for c in re.findall(r"from-(?:indigo|violet|purple|fuchsia|pink|blue)-\d+", classes)]
    if ai_grads:
        hit("V01", "alta", f"{len(ai_grads)} gradiente(s) na família roxo/azul/rosa. Ex.: {ai_grads[0].get('bg', '')[:110]}")
    if d["gradientText"]:
        hit("V02", "alta", f"{len(d['gradientText'])} texto(s) em gradiente: \"{d['gradientText'][0]}\"")
    tw_used = {c: n for c, n in d["colors"].items() if c in tw and c not in allowed_colors}
    if len(tw_used) >= 3:
        top = sorted(tw_used.items(), key=lambda x: -x[1])[:6]
        hit("V03", "media", "Cores padrão do Tailwind em uso: " + ", ".join(f"{c} ({tw[c]})" for c, _ in top))
    if d["blobs"]:
        hit("V04", "alta", f"{d['blobs']} elemento(s) com blur de 40px ou mais (blobs/orbs)")
    if d["backdrop"]:
        hit("V05", "media", f"{d['backdrop']} elemento(s) com backdrop-filter: blur")
    if d["gridBg"] or re.search(r"bg-grid|bg-dot", classes):
        hit("V07", "media", "Fundo com padrão de grid ou pontos")

    # --- Visual: tipografia ---
    fonts = Counter(d["fonts"])
    if fonts:
        main, _ = fonts.most_common(1)[0]
        brand_font = any(f in allowed_fonts for f in fonts)
        if main in pat["generic_fonts"] and not brand_font:
            hit("V08", "media", f"Fonte predominante: {main} ({', '.join(list(fonts)[:4])})")
    h1s = [h for h in d["headings"] if h["tag"] == "H1"]
    if h1s and h1s[0]["align"] == "center" and h1s[0]["size"] >= 44:
        hit("V09", "media", f"H1 centralizado de {int(h1s[0]['size'])}px: \"{h1s[0]['text'][:70]}\"")
    if h1s:
        h1top = h1s[0]["top"]
        pills = [p for p in d["pills"] if 0 < h1top - p["top"] < 160]
        if pills:
            hit("V10", "alta", f"Pílula acima do H1: \"{pills[0]['text']}\"")
    elif re.search(r"rounded-full[^\"]*(?:px-3|px-4)[^\"]*text-(?:xs|sm)", classes) and EMOJI.search(text[:400]):
        hit("V10", "alta", "Badge arredondado com emoji no topo da página")

    # --- Visual: forma ---
    if d["cards"] >= 6:
        hit("V11", "media", f"{d['cards']} cartões com raio de 12–28px e sombra")
    if d["featureGrids"]:
        g = d["featureGrids"][0]
        hit("V12", "alta", f"{len(d['featureGrids'])} grade(s) de {g['n']} cards idênticos com ícone. Ex.: \"{g['sample']}\"")
    luc = [c for c in d["lucide"] if any(f"lucide-{n}" in c for n in pat["lucide_generic_icons"])]
    icon_emoji = [h["text"] for h in d["headings"] if EMOJI.search(h["text"])]
    if len(luc) >= 3 or len(d["lucide"]) >= 8:
        hit("V13", "media", f"{len(d['lucide'])} ícones Lucide (genéricos: {len(luc)})")
    if d["hoverLift"] or "hover:-translate-y" in classes or d["transitionAll"] >= 3:
        hit("V14", "baixa", f"Hover que levanta: {d['hoverLift']} regra(s); transition all: {d['transitionAll']}")
    if d["aos"] >= 3 or len(set(d["fadeKeyframes"])) >= 1 and d["aos"]:
        hit("V15", "baixa", f"{d['aos']} bloco(s) com animação de entrada ({', '.join(set(d['fadeKeyframes']))[:60]})")

    # --- Visual: imagem e rastros ---
    ph = [i["src"] for i in d["imgs"] if any(h in i["src"] for h in pat["placeholder_image_hosts"])]
    fake = [l for l in pat["fake_logos"] if re.search(r"\b" + re.escape(l) + r"\b", low)]
    if ph or fake:
        hit("V17", "alta", "; ".join(filter(None, [f"{len(ph)} imagem(ns) placeholder ({ph[0][:60]})" if ph else "",
                                                   f"logos fictícios: {', '.join(fake)}" if fake else ""])))
    chart = sorted({c for c in d.get("svgColors", {}) if c in pat["chart_default_colors"]} - allowed_colors)
    kpi = re.findall(r"[+↑▲]\s?\d+[,.]?\d*\s?%\s*(?:vs|em rela|from|desde|do m)", low)
    v19 = []
    if chart:
        v19.append("cores padrão de biblioteca de gráfico: " + ", ".join(f"{c} ({pat['chart_default_colors'][c]})" for c in chart))
    if len(kpi) >= 2:
        v19.append(f"{len(kpi)} KPI(s) com variação padrão (\"{kpi[0]}…\")")
    if v19:
        msg = "; ".join(v19)
        hit("V19", "media", msg[0].upper() + msg[1:])
    trace_src = " ".join([low, d.get("title", "").lower(), " ".join(d["scripts"]).lower()])
    traces = [t for t in pat["generator_traces"] if t in trace_src]
    if d.get("title", "").strip().lower() in ("vite + react + ts", "vite + react", "react app", "document", ""):
        traces.append(f"título da aba: \"{d.get('title', '')}\"")
    if any("cdn.tailwindcss.com" in s for s in d["scripts"]):
        traces.append("Tailwind via CDN (padrão de protótipo)")
    if traces:
        hit("V20", "alta", "Rastros: " + "; ".join(traces[:5]))
    ai_ui = [l for l in pat["ai_ui_labels"] if l in " ".join(b["text"].lower() for b in d["buttons"]) or (l != "✨" and l in low)]
    if ai_ui:
        hit("V21", "media", "Rótulos de IA na interface: " + ", ".join(ai_ui))

    # --- Visual: marcadores e contêineres (só modo renderizado) ---
    cl = d.get("checkLists", [])
    if len(cl) >= 2 or sum(c["n"] for c in cl) >= 6:
        hit("V22", "media", f"{len(cl)} lista(s) com ícone em cada item ({sum(c['n'] for c in cl)} itens). Ex.: \"{cl[0]['sample']}\"")
    em = d.get("emojiMarkers", [])
    if len(em) >= 3:
        hit("V23", "media", f"{len(em)} item(ns) começando com emoji. Ex.: \"{em[0]['text']}\"")
    nums = sorted({c["n"] for c in d.get("numCircles", [])})
    if len(nums) >= 3 and nums[:3] == [1, 2, 3]:
        hit("V24", "media", f"{len(d['numCircles'])} círculo(s) numerados ({', '.join(map(str, nums[:6]))})")
    tags = d.get("tags", [])
    if len(tags) >= 8:
        hit("V25", "media", f"{len(tags)} tags/badges em pílula. Ex.: " + ", ".join(dict.fromkeys(t["text"] for t in tags[:5])))
    if len(d.get("nested", [])) >= 2:
        hit("V26", "media", f"{len(d['nested'])} card(s) dentro de outro card")
    if d.get("bento"):
        hit("V27", "media", f"{len(d['bento'])} grade(s) bento com {d['bento'][0]['n']} cards de tamanhos variados")
    if len(d.get("callouts", [])) >= 3:
        hit("V28", "baixa", f"{len(d['callouts'])} caixas com borda colorida só à esquerda")
    if len(d.get("statCards", [])) >= 3:
        hit("V29", "baixa", f"{len(d['statCards'])} cards de estatística: " + ", ".join(c["value"] for c in d["statCards"][:5]))
    dots = d.get("dots", [])
    cols = Counter(round(x["x"] / 6) for x in dots)
    if cols and cols.most_common(1)[0][1] >= 3:
        hit("V30", "baixa", f"{cols.most_common(1)[0][1]} bolinhas alinhadas verticalmente (linha do tempo)")

    # --- Estrutura ---
    blocks = {
        "logos": bool(re.search(r"confiam em nós|trusted by|empresas que confiam|usado por|nossos clientes", low)),
        "features": bool(d["featureGrids"]) or bool(re.search(r"recursos|funcionalidades|features", low)),
        "como_funciona": bool(re.search(r"como funciona|how it works|em 3 passos|três passos|3 simple steps", low)),
        "depoimentos": bool(re.search(r"depoimento|o que dizem|testimonial|what our customers", low)) or "★★★★★" in text,
        "precos": bool(re.search(r"mais popular|most popular|/m[êe]s\b|/mo\b|per month|planos e pre", low)),
        "faq": bool(re.search(r"perguntas frequentes|\bfaq\b|frequently asked", low)),
        "cta_final": bool(re.search(r"pronto para|ready to|comece hoje|start today", low)),
    }
    present = [k for k, v in blocks.items() if v]
    if len(present) >= 5:
        hit("E01", "alta", "Blocos de template presentes: " + ", ".join(present))
    elif len(present) >= 3:
        hit("E01", "media", "Blocos de template presentes: " + ", ".join(present))
    stats = re.findall(r"\b\d+[kKmM]\+|\b\d+\s?mil\+|99[,.]9\s?%|\b24/7\b|\b\d{2,3}\+\s", text)
    if len(stats) >= 2:
        hit("E02", "media", "Estatísticas redondas: " + ", ".join(dict.fromkeys(s.strip() for s in stats))[:120])
    stars = text.count("★") + len(re.findall(r"lucide-star\b", " ".join(d["lucide"])))
    if stars >= 5 and blocks["depoimentos"]:
        hit("E03", "alta", f"{stars} estrelas em depoimentos")
    if h1s:
        near = [b for b in d["buttons"] if 0 < b["top"] - h1s[0]["top"] < 420]
        if len(near) >= 2 and any(b["text"].lower() in pat["generic_ctas"] for b in near):
            hit("E04", "baixa", "Botões no hero: " + " | ".join(b["text"] for b in near[:3]))
    m = re.search(r"©\s?(20\d\d)", text)
    if m and int(m.group(1)) < 2026 or re.search(r"todos os direitos reservados|all rights reserved", low) and not re.search(r"rd station", low):
        hit("E06", "media", f"Rodapé genérico ({m.group(0) if m else 'todos os direitos reservados'})")

    # --- Texto ---
    for code, sev in (("T01", "media"), ("T02", "media"), ("T03", "media"), ("T09", "media"), ("T10", "baixa"), ("T12", "baixa")):
        found = [p for p in pat["phrases"][code] if re.search(r"(?<!\w)" + re.escape(p), low)]
        if found:
            hit(code, sev, ", ".join(f"\"{p}\"" for p in found[:6]))
    dashes = len(re.findall(r"\w[ \t,]*—[ \t]*\w", text))  # só travessão entre palavras (prosa)
    if dashes / words * 1000 > 3 and dashes >= 3:
        hit("T05", "baixa", f"{dashes} travessões em {words} palavras")
    emoji_spots = icon_emoji + [b["text"] for b in d["buttons"] if EMOJI.search(b["text"])]
    if emoji_spots or len(EMOJI.findall(text)) >= 4:
        hit("T06", "media", f"{len(EMOJI.findall(text))} emoji(s). Ex.: \"{(emoji_spots or [EMOJI.findall(text)[0]])[0][:60]}\"")
    stop = set(pat["title_case_stopwords_pt"])
    tc = []
    for h in d["headings"]:
        ws = [w for w in re.findall(r"[A-Za-zÀ-ÿ]+", h["text"]) if w.lower() not in stop]
        if len(ws) >= 3 and all(w[0].isupper() for w in ws) and not h["text"].isupper():
            tc.append(h["text"][:50])
    if tc:
        hit("T07", "media", f"{len(tc)} título(s) em Title Case: \"{tc[0]}\"")
    gen = [b["text"] for b in d["buttons"] if b["text"].strip().lower().rstrip(" →>") in pat["generic_ctas"]]
    if gen:
        hit("T08", "media", "CTAs genéricos: " + ", ".join(dict.fromkeys(gen)))
    nums = re.findall(r"\b\d{1,2}x\b|\b[1-9]\d{2,}\s?%|\b(?:10|5|3)\s?vezes mais", low)
    if nums:
        hit("T11", "alta", "Números de impacto sem fonte: " + ", ".join(dict.fromkeys(nums)))

    return F


def report(target, d, findings, title="Relatório anti-slop"):
    score = min(100, sum(SEV_POINTS[f["severidade"]] for f in findings))
    verdict = ("Autoral" if score <= 15 else "Traços de IA" if score <= 35 else "Slop evidente" if score <= 60 else "Template de IA")
    order = {"alta": 0, "media": 1, "baixa": 2}
    lines = [f"# {title}", "", f"- **Alvo:** {target}", f"- **Modo:** {d['mode']}",
             f"- **Slop Score:** **{score}/100**, {verdict}",
             f"- **Achados:** {sum(f['severidade']=='alta' for f in findings)} alta · "
             f"{sum(f['severidade']=='media' for f in findings)} média · {sum(f['severidade']=='baixa' for f in findings)} baixa", ""]
    if findings:
        lines += ["| Código | Sinal | Sev. | Evidência |", "|---|---|---|---|"]
        for f in sorted(findings, key=lambda f: (order[f["severidade"]], f["code"])):
            ev = f["evidencia"].replace("|", "/").replace("\n", " ")
            lines.append(f"| {f['code']} | {f['titulo']} | {SEV_LABEL[f['severidade']]} | {ev} |")
    else:
        lines.append("Nenhum sinal automático encontrado.")
    if d.get("mobile_overflow"):
        lines += ["", "**Atenção (fora do score):** a página tem rolagem horizontal em 390px."]
    lines += ["", "Trocas recomendadas: consulte cada código no CATALOGO.md.",
              "O scanner cobre os sinais mensuráveis. Imagens geradas por IA (V16), mockups inventados (V18), "
              "ritmo de seções (E07) e tríades (T04) pedem revisão visual."]
    return score, verdict, "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Detecta sinais de interface feita por IA.")
    ap.add_argument("target", help="URL ou arquivo HTML")
    ap.add_argument("--tokens", help="tokens.css da marca: cores e fontes dele deixam de contar como slop")
    ap.add_argument("--static", action="store_true", help="não abre navegador; analisa só o HTML")
    ap.add_argument("--json", help="grava os achados em JSON")
    ap.add_argument("--screenshot", help="grava captura de página inteira (modo renderizado)")
    ap.add_argument("--out", help="grava o relatório em Markdown")
    ap.add_argument("--only", choices=["visual"], help="restringe aos sinais visuais (V*) e de layout (E04, E05, E07)")
    ap.add_argument("--annotate", help="grava captura com cada sinal visual marcado e rotulado (modo renderizado)")
    a = ap.parse_args()

    pat = load_patterns()
    allowed_colors, allowed_fonts = brand_allowlist(a.tokens)
    data = None
    if not a.static:
        try:
            post = lambda d: visual_marks(d, analyze(d, pat, allowed_colors, allowed_fonts), pat)
            data = collect_rendered(a.target, a.screenshot, a.annotate, post)
        except ImportError:
            print("Playwright não instalado: usando modo estático (pip install playwright).", file=sys.stderr)
    if data is None:
        data = collect_static(a.target)
    findings = analyze(data, pat, allowed_colors, allowed_fonts)
    title = "Relatório anti-slop"
    if a.only == "visual":
        findings = [f for f in findings if VISUAL_CODES(f["code"])]
        title = "Relatório de slop visual"
    if a.annotate and data["mode"] != "renderizado":
        print("--annotate exige o modo renderizado (Playwright).", file=sys.stderr)
    score, verdict, md = report(a.target, data, findings, title)
    print(md)
    if a.out:
        Path(a.out).write_text(md + "\n", encoding="utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps({"alvo": a.target, "score": score, "diagnostico": verdict,
                                            "achados": findings}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
