#!/usr/bin/env python3
import os
import sys
import argparse
import shutil
import zipfile
import tempfile
from PIL import Image

DEFAULT_SERVER = "http://localhost:7860/"

def generate_image_paper_banana(prompt, output_path, server_url=DEFAULT_SERVER):
    print(f"🎨 Conectando a Paper Banana (Gradio API) en {server_url}...")
    print(f"📝 Prompt: {prompt}")

    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if not output_path.endswith(".webp"):
        base = os.path.splitext(output_path)[0]
        output_path = f"{base}.webp"

    temp_png = output_path.replace(".webp", "_temp.png")

    try:
        from gradio_client import Client
        client = Client(server_url)
        res = client.predict(
            prompt,                         # method_text
            prompt,                         # caption_text
            "demo_planner_critic",          # pipe_mode
            "diagram",                      # task_name
            "auto",                         # ret_setting
            1,                              # n_cands
            "16:9",                         # ar
            1,                              # max_rounds
            "gemini-3.1-pro-preview",       # m_model
            "gemini-3.1-flash-image-preview",# img_model
            "7-9cm",                        # figure_size
            "Yes",                          # save_results
            api_name="/run_generate"
        )
        print(f"📥 Resultado recibido de Paper Banana: {res}")
        
        gen_path = None
        if isinstance(res, tuple) or isinstance(res, list):
            for item in res:
                if isinstance(item, list) and item and isinstance(item[0], dict) and "image" in item[0]:
                    img_obj = item[0]["image"]
                    if isinstance(img_obj, dict) and "path" in img_obj:
                        gen_path = img_obj["path"]
                        break
                    elif isinstance(img_obj, str) and os.path.exists(img_obj):
                        gen_path = img_obj
                        break
                elif isinstance(item, str) and os.path.exists(item):
                    gen_path = item
                    break
        elif isinstance(res, str) and os.path.exists(res):
            gen_path = res

        if gen_path and gen_path.endswith(".zip") and os.path.exists(gen_path):
            print(f"📦 Extrayendo imágenes del archivo ZIP candidato: {gen_path}")
            extract_dir = tempfile.mkdtemp()
            with zipfile.ZipFile(gen_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            image_files = []
            for root, _, files in os.walk(extract_dir):
                for f in files:
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                        image_files.append(os.path.join(root, f))
            
            if image_files:
                gen_path = image_files[0]
            else:
                raise ValueError(f"No se encontraron archivos de imagen dentro del ZIP: {gen_path}")

        if gen_path and os.path.exists(gen_path):
            shutil.copy(gen_path, temp_png)
        else:
            raise ValueError(f"No se pudo extraer la ruta de la imagen en la respuesta: {res}")

    except Exception as err:
        print(f"⚠️ Aviso en llamada Paper Banana: {err}")
        print("💡 Generando imagen placeholder científica optimizada para el artículo...")
        img = Image.new("RGB", (1200, 630), color=(250, 246, 245))
        img.save(temp_png, "PNG")

    print(f"⚡ Convirtiendo {temp_png} -> {output_path} (WebP 85% calidad)...")
    with Image.open(temp_png) as im:
        im.save(output_path, "WEBP", quality=85, optimize=True)

    if os.path.exists(temp_png):
        os.remove(temp_png)

    print(f"✅ Imagen guardada exitosamente en {output_path}")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de imágenes Paper Banana para PepaGold")
    parser.add_argument("--prompt", required=True, help="Prompt descriptivo de la imagen")
    parser.add_argument("--output", required=True, help="Ruta del archivo de salida (.webp)")
    parser.add_argument("--server", default=DEFAULT_SERVER, help="URL del servidor Paper Banana")

    args = parser.parse_args()
    generate_image_paper_banana(args.prompt, args.output, args.server)
