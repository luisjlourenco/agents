#!/usr/bin/env python3
"""Empacota o kit como Skill importável no Manus.

Uso:
    python3 package_manus.py

Regera dist/, monta a pasta rd-station-design-system/ com SKILL.md na raiz
e grava rd-station-design-system-manus.zip ao lado deste script. Falha se
algum arquivo do pacote citar referências externas proibidas.
"""
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
NAME = "rd-station-design-system"
OUT = KIT / f"{NAME}-manus.zip"
INCLUDE = [
    "SKILL.md", "GUIDELINES.md", "README.md",
    "tokens.css", "components.css", "generate.py",
    "brand", "templates", "tools", "dist",
]
FORBIDDEN = ("tangram",)


def files():
    for entry in INCLUDE:
        path = KIT / entry
        if path.is_dir():
            yield from sorted(p for p in path.rglob("*") if p.is_file() and "__pycache__" not in p.parts)
        else:
            yield path


def main():
    subprocess.run([sys.executable, str(KIT / "generate.py")], check=True)
    problems = []
    for path in files():
        text = path.read_text(encoding="utf-8").lower()
        problems += [f"{path.relative_to(KIT)}: cita '{word}'" for word in FORBIDDEN if word in text]
    if problems:
        raise SystemExit("Pacote bloqueado:\n" + "\n".join(problems))

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files():
            zf.write(path, f"{NAME}/{path.relative_to(KIT).as_posix()}")
    print(f"gerado: {OUT.name} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
