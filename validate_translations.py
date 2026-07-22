#!/usr/bin/env python3
"""
validate_translations.py — Auditoría de pureza de idioma (v2, adaptada a la
estructura real del repo: blog/posts/{locale}/{slug}.md).

Chequea 3 cosas distintas, cada una detecta un tipo de bug diferente:
  1. PUREZA DE IDIOMA: el texto de cada campo/párrafo está en el idioma
     que corresponde al `locale` declarado (detección real, no lista de frases).
  2. CONSISTENCIA ESTRUCTURAL: el archivo vive en la carpeta correcta para
     su `locale` (blog/posts/de-de/x.md con locale: de-de, no al revés).
  3. CONSISTENCIA DE CONCEPTO: todos los archivos que comparten `article_id`
     tienen el mismo valor de `concept` (así lo exige AGENTS.md, y es lo que
     permite enlazar el hreflang entre idiomas).

Uso:
    python3 validate_translations.py
    python3 validate_translations.py --article PG-004   # solo un artículo
"""
import os
import re
import sys
import yaml
from collections import defaultdict
from audit_common import BRAND_WHITELIST, BLOG_EXPECTED_LANG, detect_lang

POSTS_DIR = "blog/posts"

EXPECTED_LANG = BLOG_EXPECTED_LANG


def parse_post(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m:
        return None, None
    return yaml.safe_load(m.group(1)) or {}, m.group(2)


def collect_text_blocks(meta, body_md):
    blocks = []
    for field in ("title", "description", "category_label", "region_label", "local_phenomenon"):
        if meta.get(field):
            blocks.append((f"frontmatter.{field}", str(meta[field])))
    for i, item in enumerate(meta.get("summary") or []):
        blocks.append((f"frontmatter.summary[{i}]", str(item)))
    epigraph = meta.get("epigraph")
    if isinstance(epigraph, dict) and epigraph.get("text"):
        blocks.append(("frontmatter.epigraph.text", epigraph["text"]))
    for i, item in enumerate(meta.get("faq") or []):
        if item.get("q"):
            blocks.append((f"frontmatter.faq[{i}].q", item["q"]))
        if item.get("a"):
            blocks.append((f"frontmatter.faq[{i}].a", item["a"]))
    clean_body = re.sub(r":::\w+.*?:::", "", body_md, flags=re.S)
    for i, p in enumerate([p.strip() for p in clean_body.split("\n\n") if p.strip()]):
        if p.startswith("#") or p.startswith("!["):
            continue
        blocks.append((f"body.paragraph[{i}]", p))
    return blocks


def find_all_posts():
    """os.walk recursivo — misma lógica que usa build_blog.py hoy."""
    posts = []
    for root, _, files in os.walk(POSTS_DIR):
        for fn in files:
            if fn.endswith(".md"):
                posts.append(os.path.join(root, fn))
    return sorted(posts)


def main():
    only_article = None
    if "--article" in sys.argv:
        only_article = sys.argv[sys.argv.index("--article") + 1]

    all_paths = find_all_posts()
    problems = []
    concept_by_article = defaultdict(set)
    slug_by_article = defaultdict(set)
    articles_seen = defaultdict(set)
    image_count_by_article = defaultdict(dict)

    for path in all_paths:
        meta, body_md = parse_post(path)
        if meta is None:
            problems.append(f"[ESTRUCTURA] {path}: no se pudo leer el frontmatter")
            continue

        article_id = meta.get("article_id", "SIN-ID")
        if only_article and article_id != only_article:
            continue

        locale = meta.get("locale")
        folder_locale = os.path.basename(os.path.dirname(path))

        # 1) Consistencia estructural: carpeta vs. campo locale declarado
        if locale != folder_locale:
            problems.append(
                f"[ESTRUCTURA] {path}: está en la carpeta '{folder_locale}' "
                f"pero declara locale: '{locale}' — build_blog.py puede estar "
                f"aplicando el fallback silencioso a es-ar."
            )

        articles_seen[article_id].add(folder_locale)
        if meta.get("concept"):
            concept_by_article[article_id].add(meta["concept"])
        if meta.get("slug"):
            slug_by_article[article_id].add(meta["slug"])

        # 2) Pureza de idioma
        expected = EXPECTED_LANG.get(locale)
        if expected is None:
            problems.append(f"[ESTRUCTURA] {path}: locale '{locale}' no reconocido")
            continue
        for origin, text in collect_text_blocks(meta, body_md):
            detected = detect_lang(text)
            if detected and detected != expected:
                snippet = text[:70].replace("\n", " ")
                problems.append(
                    f"[IDIOMA] {path} [{origin}] — se esperaba '{expected}', "
                    f"se detectó '{detected}': \"{snippet}...\""
                )

        # 4) Colección de imágenes en el cuerpo y metadatos
        body_images = re.findall(r'!\[.*?\]\((.*?)\)', body_md)
        image_count_by_article[article_id][folder_locale] = len(body_images)
        if not meta.get("cover_image"):
            problems.append(f"[IMAGEN PORTADA] {path}: le falta el campo 'cover_image' en el frontmatter")

    # 3) Consistencia de concepto y slugs entre idiomas del mismo article_id
    for article_id, concepts in concept_by_article.items():
        if len(concepts) > 1:
            problems.append(
                f"[CONCEPTO] {article_id}: el campo 'concept' NO es idéntico en "
                f"todos los idiomas — valores encontrados: {concepts}"
            )
    for article_id, slugs in slug_by_article.items():
        if len(slugs) > 1:
            problems.append(
                f"[SLUG] {article_id}: el slug NO es idéntico en todos los idiomas "
                f"(rompe el hreflang entre versiones) — valores encontrados: {slugs}"
            )

    # 4) Consistencia de imágenes entre idiomas (contra es-ar como referencia)
    for article_id, counts in image_count_by_article.items():
        ref_count = counts.get("es-ar", 0)
        for loc, count in counts.items():
            if count != ref_count and loc != "es-ar":
                problems.append(
                    f"[IMÁGENES DESIGUALES] {article_id} [{loc}]: tiene {count} imágenes en el cuerpo "
                    f"mientras que es-ar tiene {ref_count} imágenes."
                )

    print(f"Artículos escaneados: {len(all_paths)}\n")

    # Resumen de cobertura por article_id
    print("Cobertura por artículo:")
    for article_id, locales in sorted(articles_seen.items()):
        missing = sorted(set(EXPECTED_LANG) - locales)
        status = "🟢 completo" if not missing else f"🟡 faltan: {', '.join(missing)}"
        print(f"  {article_id}: {len(locales)}/10 — {status}")
    print()

    if problems:
        print(f"🔴 {len(problems)} problema(s) encontrado(s):\n")
        for p in problems:
            print(f"  - {p}")
        return 1

    print("🟢 Sin problemas de idioma, estructura ni consistencia de concepto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
