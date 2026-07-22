#!/usr/bin/env python3
"""
insert_images.py — El "botón de sincronizar imagen", con verificación real
antes de escribir nada y reconstrucción atómica de metadatos.

Qué hace este script:
  1. Busca la carpeta canónica de imágenes del artículo (la del es-ar
     original — es la única fuente de verdad).
  2. Verifica CADA archivo esperado: que exista Y que no esté vacío/roto.
  3. Reconstruye el frontmatter (`cover_image` y `media`) desde cero en los
     10 idiomas usando la lista canónica de es-ar (pisando cualquier basura o
     duplicado previo).
  4. Mapea las imágenes del cuerpo por posición. Si un idioma traducido
     perdió etiquetas de imagen en el cuerpo, advierte exactamente qué idioma
     necesita revisión manual sin inventar posiciones al azar.

Uso:
    python3 insert_images.py PG-001
"""
import os
import re
import sys
import yaml

POSTS_DIR = "blog/posts"
MIN_FILE_SIZE_BYTES = 8_000  # un webp real pesa más que esto


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
    return sorted(files)


def find_source_file(files):
    for path in files:
        if os.path.basename(os.path.dirname(path)) == "es-ar":
            return path
    return None


def verify_images(canonical_dir, expected_basenames):
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


def update_post_images(path, canonical_cover, canonical_media, ref_body_images):
    meta, body, raw = parse_post(path)
    if meta is None:
        return False, "no se pudo parsear"

    modified = False

    # 1. Reconstruir frontmatter cover_image y media desde cero
    if meta.get("cover_image") != canonical_cover:
        meta["cover_image"] = canonical_cover
        modified = True

    if meta.get("media") != canonical_media:
        meta["media"] = canonical_media
        modified = True

    # 2. Verificar y actualizar imágenes en el cuerpo
    cur_body_imgs = re.findall(r'!\[.*?\]\((.*?)\)', body)
    warning = None

    if len(cur_body_imgs) == len(ref_body_images):
        # Mapear imágenes 1 a 1 por posición exacta
        new_body = body
        for idx, (old_img, ref_img) in enumerate(zip(cur_body_imgs, ref_body_images)):
            if old_img != ref_img:
                new_body = new_body.replace(old_img, ref_img)
                modified = True
        body = new_body
    elif len(cur_body_imgs) > 0 and len(cur_body_imgs) != len(ref_body_images):
        warning = f"⚠️ {path}: tiene {len(cur_body_imgs)} imágenes en el cuerpo (se esperaban {len(ref_body_images)} como es-ar)"

    if modified:
        new_yaml = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False, width=1000)
        new_content = f"---\n{new_yaml}---\n{body}"
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True, warning

    return False, warning


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

    source_meta, source_body, _ = parse_post(source_path)
    canonical_cover = source_meta.get("cover_image", "")
    if not canonical_cover:
        print(f"🔴 {source_path} no tiene 'cover_image' definido todavía — generá y asigná las imágenes primero.")
        return 1

    canonical_dir = os.path.dirname(canonical_cover)
    canonical_media = source_meta.get("media") or []
    ref_body_images = re.findall(r'!\[.*?\]\((.*?)\)', source_body)

    expected = []
    if canonical_cover:
        expected.append(os.path.basename(canonical_cover))
    for m in canonical_media:
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
            "correr este mismo comando."
        )
        return 1

    print("🟢 Todas las imágenes están confirmadas en disco. Sincronizando los 10 idiomas...\n")
    warnings = []
    updated_count = 0

    for path in files:
        changed, warn = update_post_images(path, canonical_cover, canonical_media, ref_body_images)
        if warn:
            warnings.append(warn)
        if changed:
            updated_count += 1
            print(f"  ✓ actualizado: {path}")
        else:
            print(f"  = sin cambios: {path}")

    print(f"\n🟢 {article_id}: metadatos e imágenes procesados en los {len(files)} idiomas.")

    if warnings:
        print("\n⚠️ Advertencias de imágenes en cuerpo:")
        for w in warnings:
            print(f"  - {w}")

    print("\nCorré ahora: python3 validate_translations.py  (para la confirmación cruzada final)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
