#!/usr/bin/env python3
"""Empacota o kit anti-slop como Skill importável no Manus.

Uso: python3 package_manus.py  →  anti-slop-reviewer-manus.zip
"""
import zipfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
NAME = "anti-slop-reviewer"
OUT = KIT / f"{NAME}-manus.zip"
FILES = ["SKILL.md", "CATALOGO.md", "PROMPT-MANUS.md", "README.md", "slop_scan.py", "patterns.json",
         "fixtures/slop-landing.html"]
EXTRA = {"brand-tokens/rd-station-tokens.css": KIT.parent / "rd-station-design-system" / "tokens.css"}


def main():
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel in FILES:
            data = (KIT / rel).read_text(encoding="utf-8")
            if rel == "README.md":  # dentro do pacote, o agente do repositório vira o SKILL.md
                data = data.replace("[Anti-Slop Reviewer](../../design/design-anti-slop-reviewer.md)",
                                    "Anti-Slop Reviewer (regras em `SKILL.md`)")
                data = data.replace("../rd-station-design-system/tokens.css", "brand-tokens/rd-station-tokens.css")
            zf.writestr(f"{NAME}/{rel}", data)
        for rel, src in EXTRA.items():
            zf.write(src, f"{NAME}/{rel}")
    print(f"gerado: {OUT.name} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
