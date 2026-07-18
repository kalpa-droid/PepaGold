#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error
import yaml

# Mapeo de locales a nombres legibles
TARGET_LOCALES = {
    "es-mx": "Español de México",
    "es-es": "Español de España",
    "en-us": "Inglés de Estados Unidos",
    "fr-fr": "Francés",
    "de-de": "Alemán",
    "it-it": "Italiano",
    "pt-br": "Portugués de Brasil",
    "ru-ru": "Ruso",
    "zh-hans": "Chino Simplificado"
}

def translate_post(source_path, model_name="google/gemini-2.5-pro", force=False):
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: La variable de entorno OPENROUTER_API_KEY no está configurada.", file=sys.stderr)
        print("Por favor ejecute: export OPENROUTER_API_KEY='su_clave_aquí'", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(source_path):
        print(f"Error: El archivo de origen '{source_path}' no existe.", file=sys.stderr)
        sys.exit(1)

    # Cargar las reglas de traducción
    rules_path = "translation_rules.md"
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules_content = f.read()
    else:
        rules_content = "Sigue las mejores prácticas para traducción y localización natural."

    # Leer el archivo origen
    with open(source_path, "r", encoding="utf-8") as f:
        source_content = f.read()

    filename = os.path.basename(source_path)

    print(f"Iniciando traducción de: {filename}")
    print(f"Modelo utilizado: {model_name}\n")

    for locale, lang_name in TARGET_LOCALES.items():
        dest_dir = os.path.join("blog", "posts", locale)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.exists(dest_path) and not force:
            print(f"[-] Saltando {locale} (el archivo ya existe). Use --force para sobrescribir.")
            continue

        print(f"[+] Traduciendo al {lang_name} ({locale})...")

        prompt = f"""
Usted es un experto traductor profesional y editor de localización.
Su tarea es traducir y adaptar el siguiente artículo de blog del Español de Argentina (es-ar) al {lang_name} ({locale}).

IMPORTANTE: Debe seguir estrictamente las reglas de traducción y modismos culturales detallados en esta guía:
---
{rules_content}
---

Instrucciones de formato:
1. Traduzca el bloque de frontmatter YAML inicial y el cuerpo en Markdown.
2. Para el frontmatter YAML:
   - Traduzca los campos: `title`, `description`, `region_label`, `local_phenomenon`.
   - Si existen campos como `category_label` o textos en `epigraph`, `summary`, `faq`, tradúzcalos de manera acorde.
   - Modifique el campo `locale` para que sea exactamente: "{locale}"
   - NO altere, modifique ni traduzca los campos técnicos: `slug`, `category`, `concept`, `date`, `media`, `author`, `related`, `show_science_link`. Deben quedar idénticos al original.
3. Para el cuerpo en Markdown:
   - Traduzca todo el texto al {lang_name} de manera fluida y adaptada.
   - Respete y mantenga intactos los bloques interactivos personalizados (ej: `:::tip`, `:::info`, `:::stat`, `:::checklist`, `:::quiz`), traduciendo solo el contenido dentro de ellos. No modifique los nombres de los bloques.
   - Conserve todas las etiquetas HTML, negritas, enlaces y saltos de línea.
4. Devuelva ÚNICAMENTE el artículo en Markdown traducido y con su frontmatter YAML completo. No incluya preámbulos, explicaciones ni notas de traducción. Comience directo con los guiones del frontmatter `---` y termine con el fin del texto.

Artículo origen:
---
{source_content}
---
"""

        # Preparar la llamada a OpenRouter
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://pepagold.blog",
            "X-Title": "PepaGold Blog Translator"
        }

        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }

        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps(data).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                translated_md = res_data["choices"][0]["message"]["content"].strip()
                
                # Quitar envoltorios de bloques de código markdown/yaml sobrantes si los hay
                import re
                translated_md = re.sub(r"^```(yaml|markdown|md)?\s*\n", "", translated_md)
                
                parts = re.split(r"^---\s*$", translated_md, flags=re.M)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    if body.startswith("```"):
                        body = re.sub(r"^```[a-zA-Z]*\s*\n", "", body)
                        translated_md = "---" + parts[1] + "---\n\n" + body
                        
                if translated_md.endswith("```"):
                    translated_md = translated_md[:-3].strip()

                os.makedirs(dest_dir, exist_ok=True)
                with open(dest_path, "w", encoding="utf-8") as out_f:
                    out_f.write(translated_md)
                print(f"[✓] Guardado en: {dest_path}")

        except urllib.error.HTTPError as e:
            print(f"[X] Error HTTP al traducir al {locale}: {e.code} - {e.read().decode('utf-8')}", file=sys.stderr)
        except Exception as e:
            print(f"[X] Error inesperado al traducir al {locale}: {e}", file=sys.stderr)

    print("\nTraducción completada con éxito.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 translate_blog.py <ruta_del_articulo_origen.md> [--model nombre_modelo] [--force]")
        print("Ejemplo: python3 translate_blog.py blog/posts/es-ar/ciencia-barrera-cutanea-microbioma.md")
        sys.exit(1)

    source_file = sys.argv[1]
    
    model = "google/gemini-2.5-pro"
    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model = sys.argv[idx + 1]

    force_flag = "--force" in sys.argv

    translate_post(source_file, model_name=model, force=force_flag)
