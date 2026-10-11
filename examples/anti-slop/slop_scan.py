#!/usr/bin/env python3
"""slop_scan — detecta os sinais de interface "feita por IA" em sites e ferramentas.

Uso:
    python3 slop_scan.py https://meusite.manus.space
    python3 slop_scan.py pagina.html --tokens ../rd-station-design-system/tokens.css
    python3 slop_scan.py URL --json relatorio.json --screenshot captura.png
    python3 slop_scan.py URL --static        # sem navegador: só analisa o HTML bruto

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
    "V17": "Imagens placeholder ou logos fictícios", "V19": "KPIs com variação padrão", "V20": "Rastro da ferramenta geradora",
    "V21": "Cara de IA na interface", "E01": "Sequência canônica de landing de IA", "E02": "Linha de estatísticas redondas",
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
    backdrop: 0, blobs: 0, gridBg: 0, cards: 0, pills: [], lucide: [], buttons: [], imgs: [], headings: [],
    hoverLift: 0, transitionAll: 0, fadeKeyframes: [], featureGrids: [], scripts: [], classes: '' };
  const add = (o, k) => { if (k) o[k] = (o[k] || 0) + 1; };
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
      const bs = s.backgroundSize;
      if (/repeating|radial-gradient\([^)]*1px|linear-gradient[\s\S]*linear-gradient/.test(bi) && /^\d+px/.test(bs) && parseFloat(bs) <= 80) out.gridBg++;
    }
    const clip = s.backgroundClip + ' ' + (s.webkitBackgroundClip || '');
    if (clip.includes('text') && bi.includes('gradient')) out.gradientText.push(el.innerText.slice(0, 80));
    if (s.backdropFilter && s.backdropFilter.includes('blur')) out.backdrop++;
    const blur = (s.filter || '').match(/blur\(([\d.]+)px/);
    if (blur && parseFloat(blur[1]) >= 40) out.blobs++;
    const rad = parseFloat(s.borderTopLeftRadius);
    if (rad >= 12 && rad <= 28 && s.boxShadow !== 'none' && r.width > 120 && r.height > 80) out.cards++;
    if (rad >= r.height / 2 - 1 && r.height < 40 && r.width < 420 && hasText && (parseFloat(s.borderTopWidth) > 0 || rgb2hex(s.backgroundColor)))
      out.pills.push({ text: el.innerText.trim().slice(0, 60), top: Math.round(r.top + scrollY) });
    if (/^(A|BUTTON)$/.test(el.tagName) && el.innerText.trim())
      out.buttons.push({ text: el.innerText.trim().slice(0, 60), top: Math.round(r.top + scrollY), filled: !!rgb2hex(s.backgroundColor) });
    if (/^H[1-3]$/.test(el.tagName)) out.headings.push({ tag: el.tagName, text: el.innerText.trim().slice(0, 140),
      align: s.textAlign, size: parseFloat(s.fontSize), top: Math.round(r.top + scrollY), font: s.fontFamily });
    if (el.tagName === 'svg' || el.tagName === 'SVG') { const c = el.getAttribute('class') || ''; if (c.includes('lucide')) out.lucide.push(c); }
    const kids = Array.from(el.children).filter(vis);
    if ((s.display.includes('grid') || s.display.includes('flex')) && kids.length >= 3 && kids.length <= 8) {
      const rs = kids.map(k => k.getBoundingClientRect());
      const sameW = rs.every(x => Math.abs(x.width - rs[0].width) < rs[0].width * 0.08);
      const sameH = rs.every(x => Math.abs(x.height - rs[0].height) < rs[0].height * 0.2);
      const rowish = new Set(rs.map(x => Math.round(x.top / 10))).size <= Math.ceil(kids.length / 2);
      const iconTitle = kids.every(k => (k.querySelector('svg, img') || EMOJI_RE.test(k.innerText.slice(0, 4))) && k.innerText.trim().split(/\s+/).length >= 4);
      if (sameW && sameH && rowish && iconTitle && rs[0].width > 140) out.featureGrids.push({ n: kids.length, sample: kids[0].innerText.trim().slice(0, 80) });
    }
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
  out.imgs = Array.from(document.images).map(i => ({ src: i.currentSrc || i.src, alt: i.alt || '' }));
  out.scripts = Array.from(document.scripts).map(s => s.src).filter(Boolean);
  out.classes = Array.from(document.querySelectorAll('[class]')).slice(0, 4000).map(e => e.getAttribute('class')).join(' ').slice(0, 200000);
  out.aos = document.querySelectorAll('[data-aos], [data-animate], .animate-fade-in, .fade-in, .reveal').length;
  return out;
}
""".replace("EMOJI_RE", "/[\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF]/u")


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


def collect_rendered(target, screenshot=None):
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
    ai_grads = [g for g in d["gradients"] if any(h in g.get("bg", "") for h in hues)
                or any(c in g.get("bg", "").lower() for c in ("#6366f1", "#8b5cf6", "#a855f7", "#7c3aed", "#ec4899", "99, 102, 241", "139, 92, 246", "168, 85, 247", "124, 58, 237", "236, 72, 153", "147, 51, 234", "79, 70, 229"))]
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
    kpi = re.findall(r"[+↑▲]\s?\d+[,.]?\d*\s?%\s*(?:vs|em rela|from|desde|do m)", low)
    if len(kpi) >= 2:
        hit("V19", "media", f"{len(kpi)} KPI(s) com variação padrão (\"{kpi[0]}…\")")
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


def report(target, d, findings):
    score = min(100, sum(SEV_POINTS[f["severidade"]] for f in findings))
    verdict = ("Autoral" if score <= 15 else "Traços de IA" if score <= 35 else "Slop evidente" if score <= 60 else "Template de IA")
    order = {"alta": 0, "media": 1, "baixa": 2}
    lines = [f"# Relatório anti-slop", "", f"- **Alvo:** {target}", f"- **Modo:** {d['mode']}",
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
    a = ap.parse_args()

    pat = load_patterns()
    allowed_colors, allowed_fonts = brand_allowlist(a.tokens)
    data = None
    if not a.static:
        try:
            data = collect_rendered(a.target, a.screenshot)
        except ImportError:
            print("Playwright não instalado: usando modo estático (pip install playwright).", file=sys.stderr)
    if data is None:
        data = collect_static(a.target)
    findings = analyze(data, pat, allowed_colors, allowed_fonts)
    score, verdict, md = report(a.target, data, findings)
    print(md)
    if a.out:
        Path(a.out).write_text(md + "\n", encoding="utf-8")
    if a.json:
        Path(a.json).write_text(json.dumps({"alvo": a.target, "score": score, "diagnostico": verdict,
                                            "achados": findings}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
