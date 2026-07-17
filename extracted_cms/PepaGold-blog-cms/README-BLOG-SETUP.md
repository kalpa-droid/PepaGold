# Blog + CMS de PepaGold — guía de instalación

Esto te da: un panel de administrador en `pepagold.blog/admin`, donde pegás
un título y un texto, apretás "Publish", y en ~1 minuto el artículo está
online, en el idioma correcto, sumado al índice del blog y al sitemap. Sin
tocar código, sin servidor propio, sin base de datos, gratis.

## Qué se agregó a tu repo

```
admin/config.yml          ← configuración del panel (categorías, idiomas, campos)
admin/index.html          ← el panel en sí (Sveltia CMS, gratis y open source)
blog/posts/*.md           ← acá se guardan los artículos "en crudo" (ya incluye 1 de ejemplo)
build_blog.py             ← convierte esos .md en páginas HTML + arma el índice + el sitemap
requirements.txt          ← dependencias de Python que usa build_blog.py
.github/workflows/build-blog.yml  ← corre build_blog.py solo, cada vez que se publica algo
```

## Paso 1 — Crear la GitHub OAuth App (una sola vez, 5 minutos)

Esto es lo que le permite al panel de `/admin` identificarte con tu cuenta
de GitHub para poder publicar. No hay contraseñas nuevas que recordar.

1. Andá a **github.com → Settings → Developer settings → OAuth Apps → New OAuth App**.
2. Completá:
   - **Application name**: `PepaGold Blog Admin`
   - **Homepage URL**: `https://pepagold.blog`
   - **Authorization callback URL**: `https://pepagold.blog/admin/`
3. Al crearla, copiá el **Client ID** que te muestra GitHub.
4. Pegalo en `admin/config.yml`, en la línea:
   ```yaml
   app_id: "PEGAR_AQUI_EL_CLIENT_ID_DE_LA_OAUTH_APP"
   ```
   (No hace falta el "Client secret" — Sveltia usa un flujo de autenticación
   moderno, PKCE, que no lo necesita).

## Paso 2 — Subir estos archivos a tu repo

```bash
git add admin/ blog/ build_blog.py requirements.txt .github/
git commit -m "feat: agregar blog con panel de administrador"
git push
```

Vercel va a desplegar esto como cualquier otro cambio — no rompe nada de lo
que ya tenés (tu `compile.py` y la landing principal siguen funcionando
exactamente igual).

## Paso 3 — Publicar tu primer artículo

1. Entrá a `https://pepagold.blog/admin`.
2. Iniciá sesión con GitHub (te va a pedir autorizar la OAuth App del Paso 1).
3. Click en **"Artículos del blog" → "New Artículo"**.
4. Completá título, descripción, elegí el idioma/región y la categoría,
   pegá el texto en el editor.
5. Click en **"Publish"**.

Eso hace un commit directo a `blog/posts/tu-articulo.md` en GitHub. Automáticamente:
- GitHub Actions corre `build_blog.py`.
- Se genera la página del artículo, oculta, en `/blog/tu-slug/`.
- Se regenera `/blog/index.html` con la tarjeta nueva.
- Se agrega la URL al `sitemap.xml`.
- Ese resultado se commitea de vuelta al repo, lo que dispara un nuevo
  deploy de Vercel.

En 1-2 minutos el artículo está online y en el sitemap. Nada de esto lo
hacés a mano.

## Ya incluí un artículo de ejemplo

`blog/posts/viento-zonda-piel.md` — el artículo de "Viento Zonda" que
armamos antes, ya probado y generando bien. Corré `python3 build_blog.py`
localmente si querés verlo antes de subir nada:

```bash
pip install -r requirements.txt
python3 build_blog.py
# abrí blog/viento-zonda-cuidado-piel/index.html en el navegador
```

## Cómo se ve el formato de un artículo nuevo (frontmatter)

Copiá este bloque como base para cada artículo nuevo si alguna vez lo
escribís directo en un archivo `.md` en vez de usar el panel:

```markdown
---
title: "Título del artículo"
description: "Meta description de ~155 caracteres"
date: 2026-07-20
category: sostenibilidad
category_label: "Sostenibilidad"
locale: es-ar
concept: nombre-unico-que-agrupa-los-9-idiomas   # opcional
region_label: "Etiqueta regional visible"         # opcional
slug: url-del-articulo
cover_image: /assets/imagenes/blog/portada.webp
author: PepaGold
faq:
  - q: "¿Pregunta frecuente?"
    a: "Respuesta."
---

Acá va el cuerpo del artículo en Markdown normal.

## Subtítulos con ##

Párrafos, **negritas**, [links](https://...), listas, todo Markdown estándar.
```

## Si en algún momento no confía en GitHub Actions

Alternativa manual: correr `python3 build_blog.py` en tu máquina después
de publicar desde `/admin` (el panel igual hace el commit del `.md`; el
script simplemente no se ejecuta solo). Pero con la Action ya configurada
no deberías necesitar hacer esto nunca.
