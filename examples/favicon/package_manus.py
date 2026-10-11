#!/usr/bin/env python3
"""Empacota o kit de favicon como Skill importável no Manus → favicon-identity-specialist-manus.zip"""
import zipfile
from pathlib import Path

KIT = Path(__file__).resolve().parent
NAME = "favicon-identity-specialist"
OUT = KIT / f"{NAME}-manus.zip"
INCLUDE = ["SKILL.md", "README.md", "PROMPT-MANUS.md", "favicon_kit.py", "master", "dist", "fixtures"]


def main():
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for entry in INCLUDE:
            path = KIT / entry
            files = sorted(p for p in path.rglob("*") if p.is_file()) if path.is_dir() else [path]
            for f in files:
                rel = f.relative_to(KIT).as_posix()
                if f.name == "README.md":
                    data = f.read_text(encoding="utf-8").replace(
                        "[Favicon Identity Specialist](../../design/design-favicon-identity-specialist.md)",
                        "Favicon Identity Specialist (regras em `SKILL.md`)")
                    zf.writestr(f"{NAME}/{rel}", data)
                else:
                    zf.write(f, f"{NAME}/{rel}")
    print(f"gerado: {OUT.name} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
