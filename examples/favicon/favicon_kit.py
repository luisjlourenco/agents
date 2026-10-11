#!/usr/bin/env python3
"""favicon_kit — favicon oficial RD Station para sites e ferramentas (Manus, Vite, Next, HTML).

Comandos:
    python3 favicon_kit.py build   [--out dist]
        Gera o pacote completo a partir de master/*.svg (requer Playwright + Pillow).
        O pacote já vem pronto em dist/: só rode build se o ícone mudar.

    python3 favicon_kit.py install index.html --name "Calculadora de ROI" \
        [--url https://calculadora.manus.space] [--description "..."] [--public public/] [--lang pt-BR]
        Corrige o <head>: remove ícones antigos (vite.svg etc.), insere o bloco oficial,
        ajusta título, nome do site, manifest e dados estruturados. Com --public, copia
        os arquivos do pacote para a pasta pública do projeto e grava o manifest.

    python3 favicon_kit.py check index.html [--public public/]
        Audita o <head> e os arquivos contra o checklist de favicon e identidade do site.
"""
import argparse
import base64
import html
import json
import re
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
BRAND = "RD Station"
THEME = "#001927"       # navy de marca: barra do navegador e splash
BACKGROUND = "#00DBFF"  # fundo do ícone
GENERIC_TITLES = {"", "vite + react", "vite + react + ts", "react app", "document", "home", "index", "untitled", "my app", "app"}

# Nome do arquivo final → (svg de origem, tamanho em px)
PNGS = {
    "favicon-96x96.png": ("rd-station-icon.svg", 96),     # Google: múltiplo de 48px
    "apple-touch-icon.png": ("rd-station-icon.svg", 180),  # iOS: opaco, 180x180
    "web-app-manifest-192x192.png": ("rd-station-icon.svg", 192),
    "web-app-manifest-512x512.png": ("rd-station-icon.svg", 512),
    "web-app-manifest-maskable-512x512.png": ("rd-station-icon-maskable.svg", 512),
}
ICO_SIZES = (16, 32, 48)
PACK_FILES = ["favicon.ico", "favicon.svg", *PNGS]

HEAD_START, HEAD_END = "<!-- favicon RD Station: início -->", "<!-- favicon RD Station: fim -->"


# --------------------------------------------------------------------------- build
def render_png(svg_path, size, out_path, page):
    data = base64.b64encode(svg_path.read_bytes()).decode()
    page.set_viewport_size({"width": size, "height": size})
    page.set_content(f'<html><body style="margin:0;background:{BACKGROUND}">'
                     f'<img src="data:image/svg+xml;base64,{data}" width="{size}" height="{size}" style="display:block"></body></html>')
    page.screenshot(path=str(out_path), clip={"x": 0, "y": 0, "width": size, "height": size})


def build(out):
    from PIL import Image
    from playwright.sync_api import sync_playwright
    out.mkdir(parents=True, exist_ok=True)
    master = KIT / "master"
    shutil.copy(master / "rd-station-icon.svg", out / "favicon.svg")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:
            import glob
            browser = p.chromium.launch(executable_path=sorted(glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome"))[-1])
        page = browser.new_page()
        for name, (svg, size) in PNGS.items():
            render_png(master / svg, size, out / name, page)
        icos = []
        for size in ICO_SIZES:
            tmp = out / f".ico-{size}.png"
            render_png(master / "rd-station-icon.svg", size, tmp, page)
            icos.append(Image.open(tmp).convert("RGBA"))
        browser.close()
    icos[-1].save(out / "favicon.ico", format="ICO", sizes=[(s, s) for s in ICO_SIZES], append_images=icos[:-1])
    for size in ICO_SIZES:
        (out / f".ico-{size}.png").unlink()
    write_manifest(out / "site.webmanifest", BRAND, BRAND)
    (out / "head-snippet.html").write_text(head_block(BRAND, None, None) + "\n", encoding="utf-8")
    print("pacote gerado em", out)
    for f in sorted(out.iterdir()):
        print(f"  {f.name:42} {f.stat().st_size:>7} bytes")


# --------------------------------------------------------------------------- textos e head
def page_title(name):
    name = (name or "").strip()
    if not name or name.lower() == BRAND.lower():
        return BRAND
    return f"{name} | {BRAND}"


def write_manifest(path, name, short_name):
    manifest = {
        "name": page_title(name),
        "short_name": short_name[:12] if short_name else BRAND,
        "icons": [
            {"src": "/web-app-manifest-192x192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/web-app-manifest-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/web-app-manifest-maskable-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
        ],
        "theme_color": THEME,
        "background_color": THEME,
        "display": "standalone",
        "lang": "pt-BR",
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def head_block(name, url, description, existing=""):
    """Bloco oficial. Campos de compartilhamento (og:*) e JSON-LD só entram se a página ainda não os tiver."""
    has = lambda pattern: re.search(pattern, existing, re.I) is not None
    title = page_title(name)
    lines = [
        HEAD_START,
        '<link rel="icon" href="/favicon.ico" sizes="48x48">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="/favicon-96x96.png" type="image/png" sizes="96x96">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '<link rel="manifest" href="/site.webmanifest">',
        f'<meta name="theme-color" content="{THEME}">',
        f'<meta name="application-name" content="{html.escape(BRAND)}">',
        f'<meta name="apple-mobile-web-app-title" content="{html.escape(BRAND)}">',
        f'<meta property="og:site_name" content="{html.escape(BRAND)}">',
    ]
    if not has(r'property=["\']og:title'):
        lines.append(f'<meta property="og:title" content="{html.escape(title)}">')
    if description and not has(r'property=["\']og:description'):
        lines.append(f'<meta property="og:description" content="{html.escape(description)}">')
    if url:
        site = re.match(r"https?://[^/]+", url).group(0)
        if not has(r'property=["\']og:url'):
            lines.append(f'<meta property="og:url" content="{html.escape(url)}">')
        if not has(r'property=["\']og:image'):
            lines.append(f'<meta property="og:image" content="{html.escape(site)}/web-app-manifest-512x512.png">')
        if not has(r'"@type"\s*:\s*"WebSite"'):
            ld = {"@context": "https://schema.org", "@type": "WebSite", "name": BRAND,
                  "alternateName": ["RD"], "url": site + "/"}
            lines.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>")
    lines.append(HEAD_END)
    return "\n".join(lines)


# Só o que é do favicon e da identidade do site é substituído. Campos og:* específicos da página são preservados.
ICON_TAG = re.compile(
    r'[ \t]*<link\b[^>]*\brel=["\'](?:shortcut icon|icon|apple-touch-icon(?:-precomposed)?|mask-icon|manifest)["\'][^>]*>[ \t]*\n?'
    r'|[ \t]*<meta\b[^>]*\bname=["\'](?:theme-color|application-name|apple-mobile-web-app-title|msapplication-[\w-]+)["\'][^>]*>[ \t]*\n?'
    r'|[ \t]*<meta\b[^>]*\bproperty=["\']og:site_name["\'][^>]*>[ \t]*\n?', re.I)


def install(html_path, name, url, description, public, lang="pt-BR"):
    src = Path(html_path).read_text(encoding="utf-8")
    doc = re.sub(r"[ \t]*" + re.escape(HEAD_START) + r"[\s\S]*?" + re.escape(HEAD_END) + r"[ \t]*\n?", "", src)  # idempotente
    removed = [m.group(0).strip() for m in ICON_TAG.finditer(doc)]
    doc = ICON_TAG.sub("", doc)

    # idioma do documento (SEO e leitores de tela)
    lang_match = re.search(r"<html\b[^>]*>", doc, re.I)
    old_lang = None
    if lang_match and lang:
        tag = lang_match.group(0)
        m = re.search(r'\blang=["\']([^"\']*)["\']', tag)
        old_lang = m.group(1) if m else None
        new_tag = re.sub(r'\blang=["\'][^"\']*["\']', f'lang="{lang}"', tag) if m else tag[:-1] + f' lang="{lang}">'
        doc = doc.replace(tag, new_tag, 1)

    new_title = page_title(name)
    title_match = re.search(r"<title>([\s\S]*?)</title>", doc, re.I)
    old_title = title_match.group(1).strip() if title_match else None
    if title_match:
        doc = doc.replace(title_match.group(0), f"<title>{html.escape(new_title)}</title>", 1)
    if description and not re.search(r'<meta\b[^>]*name=["\']description["\']', doc, re.I):
        doc = re.sub(r"(</title>)", r'\1\n    <meta name="description" content="' + html.escape(description).replace("\\", "\\\\") + '">',
                     doc, count=1, flags=re.I)

    block = head_block(name, url, description, existing=doc)
    if not title_match:
        block = f"<title>{html.escape(new_title)}</title>\n" + block
    anchor = (re.search(r'<meta\b[^>]*name=["\']viewport["\'][^>]*>', doc, re.I)
              or re.search(r'<meta\b[^>]*charset[^>]*>', doc, re.I)
              or re.search(r"<head[^>]*>", doc, re.I))
    line_start = doc.rfind("\n", 0, anchor.start()) + 1
    indent = re.match(r"[ \t]*", doc[line_start:]).group(0) or "    "
    block = "\n".join(indent + line for line in block.split("\n"))
    doc = doc[:anchor.end()] + "\n" + block + doc[anchor.end():]
    Path(html_path).write_text(doc, encoding="utf-8")

    print(f"<head> atualizado: {html_path}")
    print(f"  título: {old_title!r} → {new_title!r}")
    if lang and old_lang != lang:
        print(f"  idioma: {old_lang!r} → {lang!r}")
    for tag in removed:
        print("  removido:", tag[:110])
    if public:
        pub = Path(public)
        pub.mkdir(parents=True, exist_ok=True)
        for f in PACK_FILES:
            shutil.copy(KIT / "dist" / f, pub / f)
        write_manifest(pub / "site.webmanifest", name, BRAND)
        for stale in ("vite.svg", "react.svg", "favicon.png", "logo192.png", "logo512.png", "manifest.json"):
            if (pub / stale).exists():
                print(f"  atenção: {pub / stale} parece ícone padrão do gerador. Apague se não for usado.")
        print(f"  {len(PACK_FILES) + 1} arquivos gravados em {pub}/")


# --------------------------------------------------------------------------- check
def check(html_path, public):
    doc = Path(html_path).read_text(encoding="utf-8")
    head = (re.search(r"<head[^>]*>([\s\S]*?)</head>", doc, re.I) or [None, doc])[1]
    links = re.findall(r"<link\b[^>]*>", head, re.I)
    rel = lambda r: [l for l in links if re.search(r'rel=["\'][^"\']*\b' + r + r'\b', l, re.I)]
    title = (re.search(r"<title>([\s\S]*?)</title>", head, re.I) or [None, ""])[1].strip()
    items = [
        ("favicon.ico na raiz (Google, navegadores antigos)", any("/favicon.ico" in l for l in rel("icon"))),
        ("favicon.svg (nítido em qualquer tela)", any(".svg" in l for l in rel("icon"))),
        ("PNG múltiplo de 48px (requisito do Google)", any(re.search(r'sizes=["\'](48|96|144|192)x', l) for l in rel("icon"))),
        ("apple-touch-icon 180x180", any("180" in l for l in rel("apple-touch-icon"))),
        ("web app manifest", bool(rel("manifest"))),
        ("theme-color", bool(re.search(r'name=["\']theme-color', head, re.I))),
        ("sem ícone padrão de gerador (vite.svg, react)", not re.search(r"vite\.svg|react\.svg|logo192", head, re.I)),
        ("um único bloco de ícones (sem duplicatas)", len(rel("icon")) <= 4),
        ("título específico com a marca (\"Ferramenta | RD Station\")", bool(title) and title.lower() not in GENERIC_TITLES and BRAND.lower() in title.lower()),
        ("nome do site (og:site_name / application-name)", bool(re.search(r'og:site_name|application-name', head, re.I))),
        ("dados estruturados WebSite (nome ao lado do favicon no Google; exige --url no install)", bool(re.search(r'"@type"\s*:\s*"WebSite"', doc))),
        ("idioma do documento em pt-BR", bool(re.search(r'<html\b[^>]*lang=["\']pt-BR', doc, re.I))),
    ]
    if public:
        pub = Path(public)
        items.append(("arquivos do pacote presentes na pasta pública", all((pub / f).exists() for f in PACK_FILES + ["site.webmanifest"])))
    ok = sum(v for _, v in items)
    print(f"# Checklist de favicon: {html_path}\n")
    for label, v in items:
        print(f"- [{'x' if v else ' '}] {label}")
    print(f"\n{ok}/{len(items)} itens ok")
    return ok == len(items)


def main():
    ap = argparse.ArgumentParser(description="Favicon oficial RD Station: gerar, instalar e auditar.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build"); b.add_argument("--out", default=str(KIT / "dist"))
    i = sub.add_parser("install"); i.add_argument("html"); i.add_argument("--name", required=True)
    i.add_argument("--url"); i.add_argument("--description"); i.add_argument("--public")
    i.add_argument("--lang", default="pt-BR", help="idioma do <html lang> (padrão pt-BR; use '' para não alterar)")
    c = sub.add_parser("check"); c.add_argument("html"); c.add_argument("--public")
    a = ap.parse_args()
    if a.cmd == "build":
        build(Path(a.out))
    elif a.cmd == "install":
        install(a.html, a.name, a.url, a.description, a.public, a.lang)
    else:
        sys.exit(0 if check(a.html, a.public) else 1)


if __name__ == "__main__":
    main()
