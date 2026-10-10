#!/usr/bin/env python3
"""RD Kit — gera ferramentas em massa a partir de manifestos JSON.

Uso:
    python3 generate.py                      # gera todas as ferramentas de tools/
    python3 generate.py tools/minha.json     # gera só as indicadas

Saída: dist/<slug>.html — um arquivo único, sem dependências além da fonte
DM Sans, com tokens, componentes e logos oficiais embutidos.
"""
import html
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
REQUIRED = ("slug", "title", "subtitle", "inputs", "outputs")


def read(rel):
    return (KIT / rel).read_text(encoding="utf-8")


def field_html(field):
    fid = html.escape(field["id"])
    kind = "number" if field.get("type") == "number" else "text"
    required = field.get("required", True)
    star = ' <span class="required" aria-hidden="true">*</span>' if required else ""
    help_text = html.escape(field.get("help", "Campo obrigatório." if required else ""))
    return (
        f'          <div class="form-control">\n'
        f'            <label class="form-label" for="{fid}">{html.escape(field["label"])}{star}</label>\n'
        f'            <input class="input" id="{fid}" name="{fid}" type="{kind}" inputmode="{"decimal" if kind == "number" else "text"}"'
        f' placeholder="{html.escape(field.get("placeholder", ""))}" aria-describedby="{fid}-help"{" required" if required else ""}>\n'
        f'            <span class="form-feedback" id="{fid}-help">{help_text}</span>\n'
        f"          </div>"
    )


def output_html(out):
    oid = html.escape(out["id"])
    return (
        f'              <div class="data-block">\n'
        f'                <span class="data-block__title">{html.escape(out["label"])}</span>\n'
        f'                <span class="data-block__value" id="out-{oid}">—</span>\n'
        f"              </div>"
    )


def title_html(tool):
    title = html.escape(tool["title"])
    hl = tool.get("title_highlight")
    return title.replace(html.escape(hl), f"<em>{html.escape(hl)}</em>", 1) if hl else title


def inline_logo(svg):
    """O contentor .brand já leva aria-label; o SVG vira decorativo para não duplicar ids."""
    svg = re.sub(r"\s*<title[^>]*>.*?</title>", "", svg, flags=re.S)
    svg = re.sub(r'\s(role|aria-labelledby)="[^"]*"', "", svg)
    return svg.replace("<svg", '<svg aria-hidden="true" focusable="false"', 1).strip()


def build(manifest_path, template, css, logos):
    tool = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    missing = [k for k in REQUIRED if k not in tool]
    if missing:
        raise SystemExit(f"{manifest_path}: faltam campos obrigatórios {missing}")

    cta = tool.get("secondary_cta", {"label": "Conheça a RD Station", "url": "https://www.rdstation.com/"})
    script_data = {k: tool[k] for k in ("inputs", "outputs")}
    script_data["insight"] = tool.get("insight", "")

    values = {
        "TITLE": html.escape(tool["title"]),
        "TITLE_HTML": title_html(tool),
        "SUBTITLE": html.escape(tool["subtitle"]),
        "EYEBROW": html.escape(tool.get("eyebrow", "Ferramenta RD Station")),
        "FORM_TITLE": html.escape(tool.get("form_title", "Seus dados")),
        "PRIMARY_CTA_LABEL": html.escape(tool.get("primary_cta", "Ver resultado")),
        "SECONDARY_CTA_LABEL": html.escape(cta["label"]),
        "SECONDARY_CTA_URL": html.escape(cta["url"]),
        "PRIVACY_NOTE": html.escape(tool.get("privacy_note", "")),
        "RESULT_TITLE": html.escape(tool.get("result_title", "Resultado")),
        "FIELDS": "\n".join(field_html(f) for f in tool["inputs"]),
        "OUTPUTS": "\n".join(output_html(o) for o in tool["outputs"]),
        # </ escapado para o JSON nunca fechar a tag <script>
        "TOOL_JSON": json.dumps(script_data, ensure_ascii=False).replace("</", "<\\/"),
        "THEME": html.escape(tool.get("theme", "rd-station")),
        "CSS": css,
        **logos,
    }
    page = template
    for key, value in values.items():
        page = page.replace("{{" + key + "}}", value)
    if "{{" in page:
        raise SystemExit(f"{manifest_path}: placeholder sem valor no template")

    out = KIT / "dist" / f'{tool["slug"]}.html'
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    return out


def main(argv):
    template = read("templates/tool-public.html")
    css = read("tokens.css") + "\n" + read("components.css")
    logos = {
        "LOGO_RD_ON_DARK": inline_logo(read("brand/rd-station-logo-on-dark.svg")),
        "LOGO_TOTVS_ON_DARK": inline_logo(read("brand/totvs-logo-on-dark.svg")),
    }
    manifests = argv or sorted(str(p) for p in (KIT / "tools").glob("*.json"))
    for manifest in manifests:
        print("gerado:", build(manifest, template, css, logos).relative_to(KIT))


if __name__ == "__main__":
    main(sys.argv[1:])
