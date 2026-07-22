#!/usr/bin/env python3
"""
audit_all.py — Corre las dos auditorías de traducción en un solo comando:
  1. validate_translations.py     -> artículos del blog (blog/posts/*)
  2. validate_site_translations.py -> estructura fija del sitio (js/translations.js)

Ambas comparten audit_common.py (la lista de marcas y la detección de
idioma), así que nunca quedan desincronizadas entre sí.

Uso:
    python3 audit_all.py
Código de salida: 0 si ambas pasan limpias, 1 si alguna encontró problemas.
"""
import os
import subprocess
import sys

# Get absolute path of python binary in current venv if available
PYTHON_BIN = sys.executable

CHECKS = [
    ("Artículos del blog", [PYTHON_BIN, "validate_translations.py"]),
    ("Estructura del sitio", [PYTHON_BIN, "validate_site_translations.py"]),
]


def main():
    overall_ok = True
    for label, cmd in CHECKS:
        print(f"\n{'=' * 60}\n  {label}\n{'=' * 60}")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            overall_ok = False

    print(f"\n{'=' * 60}")
    if overall_ok:
        print("🟢 AUDITORÍA COMPLETA: artículos y estructura, sin problemas.")
    else:
        print("🔴 AUDITORÍA COMPLETA: hay problemas — revisar el detalle arriba.")
        print("   No se debe hacer git push hasta corregir esto.")
    print("=" * 60)
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
