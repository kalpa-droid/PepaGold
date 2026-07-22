#!/usr/bin/env python3
"""
validate_site_translations.py — Auditoría de js/translations.js
(la estructura fija del sitio: botones, headlines, textos de venta).

Es un chequeo distinto al de los artículos, porque acá el bug típico no es
"quedó en español" sino "falta una clave y el sitio muestra un hueco vacío"
o "se perdió el {price} y el precio nunca aparece".

Chequea, contra es-ar como referencia:
  1. PARIDAD DE CLAVES: mismas 244 claves en los 10 idiomas — ni de más ni de menos.
  2. PLACEHOLDERS: cada clave con {price}, <br>, <strong>, etc. conserva los
     mismos placeholders en cada idioma (si no, la interpolación falla en runtime).
  3. MARCAS INTACTAS: si el valor en es-ar contiene una marca de BRAND_WHITELIST,
     el mismo valor en cada idioma debe seguir conteniéndola tal cual.
  4. PUREZA DE IDIOMA: el texto está en el idioma que corresponde a esa clave.

Uso:
    python3 validate_site_translations.py
"""
import re
import sys
import json
import subprocess
from audit_common import BRAND_WHITELIST, SITE_EXPECTED_LANG, detect_lang

REFERENCE_LOCALE = "es-ar"
TAG_NAME_RE = re.compile(r"<\s*/?\s*([a-zA-Z]+)")
TOKEN_RE = re.compile(r"\{[a-zA-Z_]+\}")


def structural_signature(text):
    """Cuenta ocurrencias de cada tag (br, strong, span...) y cada {token},
    ignorando clases/atributos que varían legítimamente entre idiomas."""
    tags = re.findall(TAG_NAME_RE, text)
    tokens = re.findall(TOKEN_RE, text)
    tag_counts = {t: tags.count(t) for t in set(tags)}
    token_counts = {t: tokens.count(t) for t in set(tokens)}
    return tag_counts, token_counts


def load_translations():
    res = subprocess.run(
        ["node", "-e",
         "global.window = {}; require('./js/translations.js'); "
         "console.log(JSON.stringify(global.window.siteTranslations));"],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        print(f"No se pudo leer js/translations.js con Node:\n{res.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(res.stdout)


def main():
    data = load_translations()
    if REFERENCE_LOCALE not in data:
        print(f"No se encontró el locale de referencia '{REFERENCE_LOCALE}'", file=sys.stderr)
        sys.exit(1)

    ref_keys = set(data[REFERENCE_LOCALE].keys())
    problems = []

    for locale, entries in data.items():
        expected_lang = SITE_EXPECTED_LANG.get(locale)
        if expected_lang is None:
            problems.append(f"[ESTRUCTURA] locale '{locale}' no está mapeado en SITE_EXPECTED_LANG")
            continue

        # 1) Paridad de claves
        these_keys = set(entries.keys())
        missing = ref_keys - these_keys
        extra = these_keys - ref_keys
        if missing:
            problems.append(f"[CLAVES FALTANTES] {locale}: {sorted(missing)}")
        if extra:
            problems.append(f"[CLAVES DE MÁS] {locale}: {sorted(extra)} (huérfanas, no existen en {REFERENCE_LOCALE})")

        for key in these_keys & ref_keys:
            ref_val = str(data[REFERENCE_LOCALE][key])
            val = str(entries[key])

            # 2) Placeholders preservados (por tipo y cantidad, no string exacto)
            ref_tags, ref_tokens = structural_signature(ref_val)
            val_tags, val_tokens = structural_signature(val)
            if (ref_tags != val_tags or ref_tokens != val_tokens) and locale != REFERENCE_LOCALE:
                problems.append(
                    f"[PLACEHOLDER] {locale}.{key}: tags {ref_tags}->{val_tags}, "
                    f"tokens {ref_tokens}->{val_tokens}"
                )

            # 3) Marcas intactas (si la referencia la tiene, la traducción también debe tenerla)
            for brand in BRAND_WHITELIST:
                if brand in ref_val and brand not in val:
                    problems.append(f"[MARCA PERDIDA] {locale}.{key}: falta '{brand}' (presente en {REFERENCE_LOCALE})")

            # 4) Pureza de idioma
            if locale != REFERENCE_LOCALE:
                detected = detect_lang(val)
                if detected and detected != expected_lang:
                    snippet = val[:70].replace("\n", " ")
                    problems.append(
                        f"[IDIOMA] {locale}.{key} — se esperaba '{expected_lang}', "
                        f"se detectó '{detected}': \"{snippet}...\""
                    )

    print(f"Locales auditados: {list(data.keys())}")
    print(f"Claves de referencia ({REFERENCE_LOCALE}): {len(ref_keys)}\n")

    if problems:
        print(f"🔴 {len(problems)} problema(s) encontrado(s):\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("🟢 Estructura del sitio: sin claves faltantes, placeholders rotos, marcas perdidas ni mezcla de idioma.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
