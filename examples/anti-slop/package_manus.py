#!/usr/bin/env python3
"""Empacota os revisores anti-slop como Skills importáveis no Manus.

Uso: python3 package_manus.py
  → anti-slop-reviewer-manus.zip     (texto, estrutura e visual)
  → visual-slop-reviewer-manus.zip   (só visual)
"""
import zipfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
COMMON = ["CATALOGO.md", "PROMPT-MANUS.md", "README.md", "slop_scan.py", "patterns.json", "fixtures/slop-landing.html"]
PACKAGES = {
    "anti-slop-reviewer": "SKILL.md",
    "visual-slop-reviewer": "SKILL-VISUAL.md",
}
TOKENS = KIT.parent / "rd-station-design-system" / "tokens.css"


def readme_for_package(text):
    """Dentro do pacote, os agentes do repositório viram o SKILL.md."""
    text = text.replace("[Anti-Slop Reviewer](../../design/design-anti-slop-reviewer.md)", "Anti-Slop Reviewer (regras em `SKILL.md`)")
    text = text.replace("[Visual Slop Reviewer](../../design/design-visual-slop-reviewer.md)", "Visual Slop Reviewer")
    return text.replace("../rd-station-design-system/tokens.css", "brand-tokens/rd-station-tokens.css")


def build(name, skill):
    out = KIT / f"{name}-manus.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(f"{name}/SKILL.md", (KIT / skill).read_text(encoding="utf-8"))
        for rel in COMMON:
            data = (KIT / rel).read_text(encoding="utf-8")
            zf.writestr(f"{name}/{rel}", readme_for_package(data) if rel == "README.md" else data)
        zf.write(TOKENS, f"{name}/brand-tokens/rd-station-tokens.css")
    print(f"gerado: {out.name} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    for name, skill in PACKAGES.items():
        build(name, skill)
