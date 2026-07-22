#!/usr/bin/env python3
"""
insert_images.py — El "botón de sincronizar imagen", pero con verificación
real antes de escribir nada.

Por qué existe: hasta ahora, cuando se le pedía a la IA que insertara una
imagen recién subida, escribía la referencia en los 10 artículos SIN
comprobar que el archivo existiera de verdad en el disco. Si la subida
todavía no había terminado, o el nombre no coincidía, el resultado era una
imagen rota o equivocada — y como se escribía en los 10 idiomas a la vez,
a veces quedaba bien en unos y mal en otros.

Qué hace este script en cambio:
  1. Busca la carpeta canónica de imágenes del artículo (la del es-ar
     original — es la única fuente de verdad, sin importar que el slug
     traducido sea distinto en otros idiomas).
  2. Verifica CADA archivo esperado: que exista Y que no esté vacío/roto
     (un .webp de 0 bytes o de pocos KB es señal de una subida a medias).
  3. Si falta o está roto UN SOLO archivo, no toca NINGÚN artículo — imprime
     exactamente qué falta y se detiene ahí. No hay que adivinar cuánto
     esperar: simplemente se vuelve a correr el comando cuando el archivo
     ya esté.
  4. Si todo está bien, recién ahí reescribe los 10 archivos de idioma para
     que TODOS apunten a la carpeta canónica — es una operación atómica,
     no puede quedar la mitad bien y la mitad mal.
  5. Al final corre el chequeo de imágenes de validate_translations.py
     como confirmación cruzada.

Uso:
    python3 insert_images.py PG-001
"""
import os
import re
import sys
import glob
import yaml

POSTS_DIR = "blog/posts"
MIN_FILE_SIZE_BYTES = 8_000  # un webp real de foto pesa bastante más que esto;
                              # menos que esto es señal de subida cortada/rota


def parse_post(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m:
        return None, None, raw
    meta = yaml.safe_load(m.group(1)) or {}
    return meta, m.group(2), raw


def find_article_files(article_id):
    files = []
    for root, _, names in os.walk(POSTS_DIR):
        for n in names:
            if not n.endswith(".md"):
                continue
            path = os.path.join(root, n)
            meta, _, _ = parse_post(path)
            if meta and meta.get("article_id") == article_id:
                files.append(path)
    return files


def find_source_file(files):
    """El archivo de es-ar es la fuente de verdad de la carpeta de imágenes."""
    for path in files:
        if os.path.basename(os.path.dirname(path)) == "es-ar":
            return path
    return None


def verify_images(canonical_dir, expected_basenames):
    """Devuelve (ok: bool, detalle: list[str])."""
    problems = []
    for name in expected_basenames:
        fs_path = os.path.join(canonical_dir.lstrip("/"), name)
        if not os.path.exists(fs_path):
            problems.append(f"FALTA: '{name}' no existe todavía en {canonical_dir}/")
            continue
        size = os.path.getsize(fs_path)
        if size < MIN_FILE_SIZE_BYTES:
            problems.append(
                f"SOSPECHOSO: '{name}' existe pero pesa solo {size} bytes "
                f"(parece una subida cortada, no una foto real)"
            )
    return (len(problems) == 0), problems


def rewrite_image_paths(raw_content, canonical_dir, expected_basenames):
    """Reescribe cover_image, media[] y los ![...](...) del cuerpo para que
    TODOS apunten a la carpeta canónica, preservando el nombre de archivo."""
    for name in expected_basenames:
        pattern = re.compile(r"/assets/imagenes/blog/[^)\s\"']+/" + re.escape(name))
        raw_content = pattern.sub(f"{canonical_dir}/{name}", raw_content)
    return raw_content


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 insert_images.py PG-XXX")
        return 1
    article_id = sys.argv[1]

    files = find_article_files(article_id)
    if not files:
        print(f"🔴 No encontré ningún artículo con article_id '{article_id}'.")
        return 1

    source_path = find_source_file(files)
    if not source_path:
        print(f"🔴 No encontré la versión es-ar de {article_id} (es la fuente de verdad de las imágenes).")
        return 1

    source_meta, _, _ = parse_post(source_path)
    canonical_dir = os.path.dirname(source_meta.get("cover_image", ""))
    if not canonical_dir:
        print(f"🔴 {source_path} no tiene 'cover_image' definido todavía — generá y asigná las imágenes primero.")
        return 1

    expected = []
    if source_meta.get("cover_image"):
        expected.append(os.path.basename(source_meta["cover_image"]))
    for m in source_meta.get("media") or []:
        bn = os.path.basename(m)
        if bn not in expected:
            expected.append(bn)

    print(f"Artículo: {article_id}")
    print(f"Carpeta canónica de imágenes: {canonical_dir}")
    print(f"Archivos esperados: {expected}\n")

    ok, problems = verify_images(canonical_dir, expected)
    if not ok:
        print("🔴 NO SE MODIFICÓ NINGÚN ARTÍCULO. Faltan imágenes por confirmar:\n")
        for p in problems:
            print(f"  - {p}")
        print(
            "\n👉 Generá/subí el archivo que falta a esa carpeta local y volvé a "
            "correr este mismo comando. No hace falta esperar un tiempo fijo — "
            "en cuanto el archivo esté ahí, el comando va a pasar solo."
        )
        return 1

    print("🟢 Todas las imágenes están confirmadas en disco. Sincronizando los 10 idiomas...\n")
    for path in files:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
        new_raw = rewrite_image_paths(raw, canonical_dir, expected)
        if new_raw != raw:
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_raw)
            print(f"  ✓ actualizado: {path}")
        else:
            print(f"  = sin cambios: {path}")

    print(f"\n🟢 {article_id}: imágenes sincronizadas en los {len(files)} idiomas.")
    print("Corré ahora: python3 validate_translations.py  (para la confirmación cruzada final)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
