#!/usr/bin/env python3
import os
import re
import sys
import glob
import json
import yaml
import markdown
import datetime
from xml.sax.saxutils import escape as xml_escape

SITE_URL = "https://pepagold.blog"
POSTS_DIR = "blog/posts"
SITEMAP_PATH = "sitemap.xml"

LOCALE_FOLDERS = {
    "es-ar": "", "es-mx": "mx", "es-es": "es", "en-us": "us",
    "fr-fr": "fr", "de-de": "de", "it-it": "it", "pt-br": "pt",
    "ru-ru": "ru", "zh-hans": "zh",
}

HREFLANG_MAP = {k: k for k in LOCALE_FOLDERS}

LOCALE_INFO = {
    "es-ar": {"flag": "🇦🇷", "name": "Español (AR)", "code": "AR"},
    "es-mx": {"flag": "🇲🇽", "name": "Español (MX)", "code": "MX"},
    "es-es": {"flag": "🇪🇸", "name": "Español (ES)", "code": "ES"},
    "en-us": {"flag": "🇺🇸", "name": "English", "code": "US"},
    "fr-fr": {"flag": "🇫🇷", "name": "Français", "code": "FR"},
    "de-de": {"flag": "🇩🇪", "name": "Deutsch", "code": "DE"},
    "it-it": {"flag": "🇮🇹", "name": "Italiano", "code": "IT"},
    "pt-br": {"flag": "🇧🇷", "name": "Português", "code": "PT"},
    "ru-ru": {"flag": "🇷🇺", "name": "Русский", "code": "RU"},
    "zh-hans": {"flag": "🇨🇳", "name": "简体中文", "code": "ZH"},
}

CATEGORY_LABELS_DEFAULT = {
    "barrera-cutanea": "🔬 Ciencia de la Piel",
    "sostenibilidad": "🌱 Sostenibilidad y Ecología",
    "rutinas-minimalismo": "🧘‍♀️ Rutinas y Skinimalismo",
    "comparativas-economia": "⚖️ Comparativas y Economía",
    "guias-regionales": "🏜️ Guías Regionales y Clima",
    "cuidado-producto": "🧼 Uso y Cuidado del Producto",
    "testimonios-estilo-vida": "💬 Testimonios y Estilo de Vida",
    "tendencias-skincare": "📈 Tendencias Globales",
}

CATEGORY_LABELS_I18N = {
    "es-ar": CATEGORY_LABELS_DEFAULT,
    "es-mx": CATEGORY_LABELS_DEFAULT,
    "es-es": CATEGORY_LABELS_DEFAULT,
    "en-us": {
        "barrera-cutanea": "🔬 Skin Science",
        "sostenibilidad": "🌱 Sustainability & Ecology",
        "rutinas-minimalismo": "🧘‍♀️ Routines & Skinimalism",
        "comparativas-economia": "⚖️ Comparisons & Savings",
        "guias-regionales": "🏜️ Regional Guides & Climate",
        "cuidado-producto": "🧼 Product Use & Care",
        "testimonios-estilo-vida": "💬 Stories & Lifestyle",
        "tendencias-skincare": "📈 Global Trends",
    },
    "fr-fr": {
        "barrera-cutanea": "🔬 Science de la Peau",
        "sostenibilidad": "🌱 Écologie & Durabilité",
        "rutinas-minimalismo": "🧘‍♀️ Routines & Skinimalisme",
        "comparativas-economia": "⚖️ Comparatifs & Économies",
        "guias-regionales": "🏜️ Guides Régionaux & Climat",
        "cuidado-producto": "🧼 Utilisation & Entretien",
        "testimonios-estilo-vida": "💬 Témoignages & Mode de Vie",
        "tendencias-skincare": "📈 Tendances Globales",
    },
    "de-de": {
        "barrera-cutanea": "🔬 Hautwissenschaft",
        "sostenibilidad": "🌱 Nachhaltigkeit & Ökologie",
        "rutinas-minimalismo": "🧘‍♀️ Routinen & Skinimalismus",
        "comparativas-economia": "⚖️ Vergleiche & Ersparnisse",
        "guias-regionales": "🏜️ Regionale Ratgeber & Klima",
        "cuidado-producto": "🧼 Produktnutzung & Pflege",
        "testimonios-estilo-vida": "💬 Berichte & Lebensstil",
        "tendencias-skincare": "📈 Globale Trends",
    },
    "it-it": {
        "barrera-cutanea": "🔬 Scienza della Pelle",
        "sostenibilidad": "🌱 Sostenibilità ed Ecologia",
        "rutinas-minimalismo": "🧘‍♀️ Routine e Skinimalismo",
        "comparativas-economia": "⚖️ Confronti ed Economia",
        "guias-regionales": "🏜️ Guide Regionali e Clima",
        "cuidado-producto": "🧼 Uso e Cura del Prodotto",
        "testimonios-estilo-vida": "💬 Storie e Stile di Vita",
        "tendencias-skincare": "📈 Tendenze Globali",
    },
    "pt-br": {
        "barrera-cutanea": "🔬 Ciência da Pele",
        "sostenibilidad": "🌱 Sustentabilidade e Ecologia",
        "rutinas-minimalismo": "🧘‍♀️ Rotinas e Skinimalismo",
        "comparativas-economia": "⚖️ Comparativos e Economia",
        "guias-regionales": "🏜️ Guias Regionais e Clima",
        "cuidado-producto": "🧼 Uso e Cuidados com o Produto",
        "testimonios-estilo-vida": "💬 Depoimentos e Estilo de Vida",
        "tendencias-skincare": "📈 Tendências Globales",
    },
    "ru-ru": {
        "barrera-cutanea": "🔬 Наука о коже",
        "sostenibilidad": "🌱 Экология и устойчивость",
        "rutinas-minimalismo": "🧘‍♀️ Уход и скиннимализм",
        "comparativas-economia": "⚖️ Сравнение и экономика",
        "guias-regionales": "🏜️ Региональные гиды и климат",
        "cuidado-producto": "🧼 Использование и уход",
        "testimonios-estilo-vida": "💬 Отзывы и стиль жизни",
        "tendencias-skincare": "📈 Мировые тренды",
    },
    "zh-hans": {
        "barrera-cutanea": "🔬 皮肤科学",
        "sostenibilidad": "🌱 环保与可持续",
        "rutinas-minimalismo": "🧘‍♀️ 极简护肤",
        "comparativas-economia": "⚖️ 对比与护肤经济",
        "guias-regionales": "🏜️ 气候与区域指南",
        "cuidado-producto": "🧼 产品使用与护理",
        "testimonios-estilo-vida": "💬 真实体验与生活",
        "tendencias-skincare": "📈 全球趋势",
    },
}

def get_cat_label(cat_key, locale):
    cats = CATEGORY_LABELS_I18N.get(locale, CATEGORY_LABELS_DEFAULT)
    return cats.get(cat_key, CATEGORY_LABELS_DEFAULT.get(cat_key, cat_key or ""))


I18N_STRINGS = {
    "es-ar": {
        "summary_title": "⏱️ En 30 segundos", "toc_title": "En este artículo", "reading_time": "min de lectura",
        "science_title": "Lo que dice la ciencia", "science_desc": "Dermatólogos y estudios sobre barrera cutánea y microbioma que respaldan esta nota →",
        "cta_desc": "<strong>Laska Mini Set</strong> — el set de microfibra que reemplaza discos de algodón, agua micelar y desmaquillante. Solo con agua.",
        "cta_btn": "Conocer el producto &rarr;", "faq_title": "Preguntas frecuentes", "related_title": "Seguí leyendo",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Todos los derechos reservados.", "read_btn": "Leer Artículo",
        "index_desc": "Artículos sobre cuidado de la piel sin químicos, sostenibilidad y skincare consciente.", "index_title": "Blog | PepaGold", "index_all": "Todos", "checklist_hint": "Se guarda solo en este navegador — marcá a tu ritmo."
    },
    "es-mx": {
        "summary_title": "⏱️ En 30 segundos", "toc_title": "En este artículo", "reading_time": "min de lectura",
        "science_title": "Lo que dice la ciencia", "science_desc": "Dermatólogos y estudios sobre barrera cutánea y microbioma que respaldan esta nota →",
        "cta_desc": "<strong>Laska Mini Set</strong> — el set de microfibra que reemplaza pads de algodón, agua micelar y desmaquillantes. Solo con agua.",
        "cta_btn": "Conocer el producto &rarr;", "faq_title": "Preguntas frecuentes", "related_title": "Sigue leyendo",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Todos los derechos reservados.", "read_btn": "Leer Artículo",
        "index_desc": "Artículos sobre cuidado de la piel sin químicos, sostenibilidad y skincare consciente.", "index_title": "Blog | PepaGold", "index_all": "Todos", "checklist_hint": "Se guarda solo en este navegador — marca a tu ritmo."
    },
    "es-es": {
        "summary_title": "⏱️ En 30 segundos", "toc_title": "En este artículo", "reading_time": "min de lectura",
        "science_title": "Lo que dice la ciencia", "science_desc": "Dermatólogos y estudios sobre barrera cutánea y microbioma que respaldan esta nota →",
        "cta_desc": "<strong>Laska Mini Set</strong> — el set de microfibra que reemplaza algodones, agua micelar y desmaquillante. Solo con agua.",
        "cta_btn": "Descubrir producto &rarr;", "faq_title": "Preguntas frecuentes", "related_title": "Sigue leyendo",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Todos los derechos reservados.", "read_btn": "Leer Artículo",
        "index_desc": "Artículos sobre cuidado de la piel sin químicos, sostenibilidad y skincare consciente.", "index_title": "Blog | PepaGold", "index_all": "Todos", "checklist_hint": "Se guarda solo en este navegador — marca a tu ritmo."
    },
    "en-us": {
        "summary_title": "⏱️ In 30 seconds", "toc_title": "In this article", "reading_time": "min read",
        "science_title": "What science says", "science_desc": "Dermatologists and clinical studies on the skin barrier and microbiome supporting this guide &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — the reusable UpPoly microfiber set replacing cotton pads, micellar water, and cleansers. Water only.",
        "cta_btn": "Explore Product &rarr;", "faq_title": "Frequently Asked Questions", "related_title": "Keep reading",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; All rights reserved.", "read_btn": "Read Article",
        "index_desc": "Articles on chemical-free skincare, sustainability, and skinimalism.", "index_title": "Blog | PepaGold", "index_all": "All", "checklist_hint": "Saved locally in your browser — mark at your own pace."
    },
    "fr-fr": {
        "summary_title": "⏱️ En 30 secondes", "toc_title": "Dans cet article", "reading_time": "min de lecture",
        "science_title": "Ce que dit la science", "science_desc": "Dermatologues et études cliniques sur la barrière cutanée et le microbiome soutiennent ce guide &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — le coffret en microfibre réutilisable qui remplace le coton, l'eau micellaire et le démaquillant. Rien qu'avec de l'eau.",
        "cta_btn": "Découvrir le produit &rarr;", "faq_title": "Foire aux questions", "related_title": "Poursuivez votre lecture",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Tous droits réservés.", "read_btn": "Lire l'article",
        "index_desc": "Articles sur les soins de la peau sans produits chimiques et la beauté durable.", "index_title": "Blog | PepaGold", "index_all": "Tous", "checklist_hint": "Enregistré localement dans votre navigateur — cochez à votre rythme."
    },
    "de-de": {
        "summary_title": "⏱️ In 30 Sekunden", "toc_title": "In diesem Artikel", "reading_time": "Min. Lesezeit",
        "science_title": "Was die Wissenschaft sagt", "science_desc": "Dermatologen und Studien zur Hautbarriere und zum Mikrobiom, die diesen Artikel stützen &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — das wiederverwendbare Mikrofaser-Set, das Wattepads, Mizellenwasser und Abschminkmittel ersetzt. Nur mit Wasser.",
        "cta_btn": "Produkt entdecken &rarr;", "faq_title": "Häufig gestellte Fragen", "related_title": "Weiterlesen",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Alle Rechte vorbehalten.", "read_btn": "Artikel lesen",
        "index_desc": "Artikel über chemiefreie Hautpflege, Nachhaltigkeit und Skinimalismus.", "index_title": "Blog | PepaGold", "index_all": "Alle", "checklist_hint": "Lokal im Browser gespeichert — markieren Sie in Ihrem eigenen Tempo."
    },
    "it-it": {
        "summary_title": "⏱️ In 30 secondi", "toc_title": "In questo articolo", "reading_time": "min di lettura",
        "science_title": "Cosa dice la scienza", "science_desc": "Dermatologi e studi sulla barriera cutanea e sul microbioma che supportano questa guida &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — il set di microfibra riutilizzabile che sostituisce dischetti di cotone, acqua micellare e struccanti. Solo con acqua.",
        "cta_btn": "Scopri il prodotto &rarr;", "faq_title": "Domande frequenti", "related_title": "Continua a leggere",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Tutti i diritti riservati.", "read_btn": "Leggi l'articolo",
        "index_desc": "Articoli sulla cura della pelle senza sostanze chimiche e sostenibilità.", "index_title": "Blog | PepaGold", "index_all": "Tutti", "checklist_hint": "Salvato localmente nel tuo browser — segna al tuo ritmo."
    },
    "pt-br": {
        "summary_title": "⏱️ Em 30 segundos", "toc_title": "Neste artigo", "reading_time": "min de leitura",
        "science_title": "O que a ciência diz", "science_desc": "Dermatologistas e estudos sobre a barreira cutânea e o microbioma que apoiam este artigo &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — o conjunto de microfibra reutilizável que substitui algodão, água micelar e demaquilante. Apenas com água.",
        "cta_btn": "Conheça o produto &rarr;", "faq_title": "Perguntas frequentes", "related_title": "Continue lendo",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Todos os direitos reservados.", "read_btn": "Ler Artigo",
        "index_desc": "Artigos sobre cuidados com a pele sem químicos e sustentabilidade.", "index_title": "Blog | PepaGold", "index_all": "Todos", "checklist_hint": "Salvo localmente no seu navegador — marque no seu próprio ritmo."
    },
    "ru-ru": {
        "summary_title": "⏱️ За 30 секунд", "toc_title": "В этой статье", "reading_time": "мин чтение",
        "science_title": "Что говорит наука", "science_desc": "Дерматологи и клинические исследования кожного барьера и микробиома &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — набор из микроволокна UpPoly, заменяющий ватные диски и мицеллярную воду. Только вода.",
        "cta_btn": "Узнать больше о продукте &rarr;", "faq_title": "Часто задаваемые вопросы", "related_title": "Читайте также",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; Все права защищены.", "read_btn": "Читать статью",
        "index_desc": "Статьи об уходе за кожей без химии, экологии и осознанном уходе.", "index_title": "Блог | PepaGold", "index_all": "Все", "checklist_hint": "Сохраняется локально в вашем браузере — отмечайте в своем темпе."
    },
    "zh-hans": {
        "summary_title": "⏱️ 30秒速览", "toc_title": "本文目录", "reading_time": "分钟阅读",
        "science_title": "科学依据", "science_desc": "皮肤学专家与临床研究关于皮肤屏障与微生态的背书 &rarr;",
        "cta_desc": "<strong>Laska Mini Set</strong> — 替代卸妆棉、卸妆水和清洁乳的可重复使用超细纤维套装。只需清水。",
        "cta_btn": "了解产品详情 &rarr;", "faq_title": "常见问题解答", "related_title": "推荐阅读",
        "footer_copy": "&copy; 2025&ndash;2026 PepaGold &middot; 保留所有权利。", "read_btn": "阅读文章",
        "index_desc": "关于无化学护肤、环保与极简护肤的文章。", "index_title": "博客 | PepaGold", "index_all": "全部", "checklist_hint": "保存在您的浏览器中 — 请按自己的节奏标记。"
    }
}

MONTHS_I18N = {
    "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"],
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"],
    "it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembri", "dicembre"],
    "pt": ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"],
    "ru": ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"],
    "zh": ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"],
}

def format_localized_date(date_str, locale):
    if not date_str: return ""
    try:
        dt = datetime.datetime.strptime(str(date_str).split()[0], "%Y-%m-%d")
        lang = locale.split("-")[0]
        months = MONTHS_I18N.get(lang, MONTHS_I18N["es"])
        month_name = months[dt.month - 1]
        if lang == "en": return f"{month_name} {dt.day}, {dt.year}"
        elif lang == "zh": return f"{dt.year}年{dt.month}月{dt.day}日"
        elif lang == "de": return f"{dt.day}. {month_name} {dt.year}"
        elif lang == "ru": return f"{dt.day} {month_name} {dt.year} г."
        else: return f"{dt.day} de {month_name} de {dt.year}"
    except Exception:
        return str(date_str)

# =========================================================================
# BLOQUES INTERACTIVOS (Tip, Stat, Checklist, Quiz)
# =========================================================================

BLOCK_RE = re.compile(r"^:::(tip|info|stat|checklist|quiz|funfact)(?:[ \t]+([^\n]*))?\n(.*?)\n:::[ \t]*$", re.M | re.S)
_inline_md = markdown.Markdown(extensions=["extra"])

def _inline(text):
    _inline_md.reset()
    html = _inline_md.convert(text.strip())
    if html.startswith("<p>") and html.endswith("</p>") and html.count("<p>") == 1:
        html = html[3:-4]
    return html

def render_tip_or_info(kind, title, content):
    icon = "💡" if kind == "tip" else "ℹ️"
    label = title or ("Tip" if kind == "tip" else "Para tener en cuenta")
    body = markdown.markdown(content.strip(), extensions=["extra", "sane_lists"])
    return (
        f'<div class="callout callout-{kind}">'
        f'<p class="callout-title">{icon} {label}</p>'
        f'<div class="callout-body">{body}</div></div>'
    )

def render_funfact(title, content):
    label = title or "Dato Curioso"
    body = markdown.markdown(content.strip(), extensions=["extra", "sane_lists"])
    return (
        f'<div class="callout callout-funfact">'
        f'<p class="callout-title">🤯 {label}</p>'
        f'<div class="callout-body">{body}</div></div>'
    )

def render_stat(content):
    lines = [l for l in content.strip().split("\n") if l.strip()]
    if not lines: return ""
    first_line = lines[0]

    match = re.match(r"^\*\*(.*?)\*\*\s*(.*)$", first_line)
    if match:
        number = match.group(1)
        caption = (match.group(2) + " " + " ".join(lines[1:])).strip()
    elif len(lines) > 1:
        number = first_line
        caption = " ".join(lines[1:])
    else:
        number = ""
        caption = first_line

    num_html = f'<p class="stat-number">{_inline(number)}</p>' if number else ""
    cap_html = f'<p class="stat-caption">{_inline(caption)}</p>' if caption else ""

    return f'<div class="callout stat-box">{num_html}{cap_html}</div>'

def render_checklist(title, content, block_id, locale="es-ar"):
    items = [l[2:].strip() for l in content.strip().split("\n") if l.strip().startswith("- ")]
    lis = "".join(
        f'<li><label><input type="checkbox" class="cl-item" data-key="{block_id}-{i}"> '
        f'<span>{_inline(item)}</span></label></li>'
        for i, item in enumerate(items)
    )
    label = title or "Probalo en casa"
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    hint = i18n.get("checklist_hint", "Se guarda solo en este navegador — marcá a tu ritmo.")
    return (
        f'<div class="callout checklist-box">'
        f'<p class="callout-title">✅ {label}</p>'
        f'<ul class="checklist">{lis}</ul>'
        f'<p class="checklist-hint">{hint}</p>'
        f'</div>'
    )

def render_quiz(title, content, block_id):
    questions = [q for q in re.split(r"\n\s*\n", content.strip()) if q.strip()]
    out = [f'<div class="callout quiz-box"><p class="callout-title">🧠 {title or "Ponete a prueba"}</p>']
    for qi, block in enumerate(questions):
        lines = [l.strip() for l in block.strip().split("\n") if l.strip()]
        if not lines or not lines[0].startswith("Q:"):
            continue
        question_text = lines[0][2:].strip()
        options = []
        for opt_line in lines[1:]:
            if not opt_line.startswith("- "):
                continue
            correct = "*correct*" in opt_line
            text = opt_line[2:].replace("*correct*", "").strip()
            options.append((text, correct))
        out.append(f'<div class="quiz-question"><p class="quiz-q">{_inline(question_text)}</p><div class="quiz-options">')
        for oi, (text, correct) in enumerate(options):
            out.append(
                f'<button type="button" class="quiz-option" data-correct="{1 if correct else 0}" '
                f'onclick="pgQuiz(this,{1 if correct else 0})">{_inline(text)}</button>'
            )
        out.append('</div></div>')
    out.append('</div>')
    return "".join(out)

def preprocess_custom_blocks(md_text, slug, locale="es-ar"):
    counter = {"n": 0}
    def repl(m):
        kind, title, content = m.group(1), (m.group(2) or "").strip(), m.group(3)
        counter["n"] += 1
        bid = f"{slug}-{counter['n']}"
        if kind in ("tip", "info"): return render_tip_or_info(kind, title, content)
        if kind == "funfact": return render_funfact(title, content)
        if kind == "stat": return render_stat(content)
        if kind == "checklist": return render_checklist(title, content, bid, locale=locale)
        if kind == "quiz": return render_quiz(title, content, bid)
        return ""
    return BLOCK_RE.sub(repl, md_text)

def render_media(media_list):
    if not media_list:
        return (
            '<div class="media-placeholder-fallback" style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: linear-gradient(135deg, #FAF6F5, #FDF7F7); min-height: 250px; border-radius: 8px;">'
            '<img src="/assets/imagenes/icono.svg" style="width: 56px; height: 56px; opacity: 0.65; transform: none;" alt="PepaGold Logo">'
            '</div>'
        )
    html = '<div class="media-gallery" style="display: flex; gap: 10px; width: 100%; height: 100%;">'
    for item in media_list:
        src = item if isinstance(item, str) else item.get('file', '')
        if src.lower().endswith(('.mp4', '.webm')):
            html += f'<video src="{src}" autoplay muted loop playsinline style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;"></video>'
        else:
            html += f'<img src="{src}" style="flex: 1; width: 100%; object-fit: cover; border-radius: 8px;" alt="Blog Media">'
    html += '</div>'
    return html

def get_cover_image(meta):
    if meta.get("cover_image"):
        return meta["cover_image"]
    media = meta.get("media", [])
    if not media:
        return ""
    for item in media:
        src = item if isinstance(item, str) else item.get('file', '')
        if any(k in src.lower() for k in ['portada', 'gemini_generated_image', 'cover', 'hero']):
            return src
    for item in media:
        src = item if isinstance(item, str) else item.get('file', '')
        if 'cuerpo' not in src.lower():
            return src
    first = media[0]
    return first if isinstance(first, str) else first.get('file', '')

# =========================================================================
# PLANTILLAS HTML
# =========================================================================

BRAND_HEAD = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | PepaGold Blog</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
<link rel="manifest" href="/manifest.json" />
<meta property="og:type" content="article">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{cover_image_abs}">
<meta property="og:url" content="{canonical}">
{hreflang_tags}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --color-primary: #D48C90; --color-primary-hover: #C97A7E; --color-accent: #E29578;
    --color-dark: #2A2523; --color-dark-muted: #5A524E; --border-color: rgba(212,140,144,0.2);
    --bg-primary: #FFFFFF; --bg-secondary: #FAF6F5; --bg-accent-light:#FDF7F7;
    --shadow-md: 0 8px 25px rgba(42, 37, 35, 0.05);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html {{ scroll-behavior: smooth; }}
  body {{ font-family:'Poppins',sans-serif; color:var(--color-dark); background:var(--bg-primary); line-height:1.6; -webkit-font-smoothing:antialiased; }}
  img {{ max-width:100%; height:auto; display:block; }}
  a {{ color:var(--color-primary-hover); text-decoration: none; }}
  
  /* Lang selector and Floating Buttons */
  .floating-droplet {{ position: fixed; top: 65px; left: 20px; width: 56px; height: 56px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.3); border-radius: 0 50% 50% 50%; transform: rotate(45deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(42, 37, 35, 0.08); z-index: 1000; transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.3s ease; cursor: pointer; text-decoration: none; }}
  .floating-droplet:hover {{ transform: rotate(45deg) scale(1.08); box-shadow: 0 12px 30px rgba(212, 140, 144, 0.25); border-color: var(--color-primary); }}
  .floating-droplet img {{ width: 28px; height: 28px; transform: rotate(-45deg); transition: transform 0.3s ease; }}
  .lang-selector-container {{ position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: 'Poppins', sans-serif; }}
  .lang-selector-btn {{ display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }}
  .lang-selector-btn:hover {{ border-color: var(--color-primary); box-shadow: 0 6px 16px rgba(212, 140, 144, 0.15); transform: translateY(-1px); }}
  .lang-selector-btn .arrow-icon {{ font-size: 9px; color: var(--color-primary); transition: transform 0.3s ease; }}
  .lang-selector-container.is-active .lang-selector-btn .arrow-icon {{ transform: rotate(180deg); }}
  .lang-dropdown-menu {{ position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); max-height: 320px; overflow-y: auto; }}
  .lang-selector-container.is-active .lang-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
  .lang-option {{ padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; transition: all 0.2s ease; }}
  .lang-option:hover {{ background: rgba(212, 140, 144, 0.08); color: var(--color-primary-hover); }}
  .lang-option.is-selected {{ background: rgba(212, 140, 144, 0.12); color: var(--color-primary); font-weight: 600; }}
  .blog-nav-btn-floating {{ right: 130px; top: 65px; }}

  /* Scrollbar personalizado para el menú de idiomas */
  .lang-dropdown-menu::-webkit-scrollbar {{ width: 4px; }}
  .lang-dropdown-menu::-webkit-scrollbar-track {{ background: transparent; }}
  .lang-dropdown-menu::-webkit-scrollbar-thumb {{ background: rgba(212, 140, 144, 0.3); border-radius: 10px; }}
  .lang-dropdown-menu::-webkit-scrollbar-thumb:hover {{ background: var(--color-primary); }}
  
  @media (max-width: 600px) {{
    .floating-droplet {{ top: 65px; left: 12px; width: 46px; height: 46px; }}
    .floating-droplet img {{ width: 22px; height: 22px; }}
    .lang-selector-container {{ top: 65px; right: 12px; }}
    .lang-selector-btn {{ padding: 5px 11px; font-size: 12px; }}
    .blog-nav-btn-floating {{ right: 110px !important; }}
  }}

  /* Maquetación del artículo */
  .wrap {{ max-width: 800px; margin: 0 auto; padding: 40px 24px; box-sizing: border-box; }}
  .eyebrow {{ font-size: 0.85rem; font-weight: 600; color: var(--color-accent); text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }}
  .article-title {{ font-family: Georgia, serif; font-size: clamp(2rem, 4vw, 2.8rem); color: var(--color-dark); margin-bottom: 12px; font-weight: 400; line-height: 1.2; }}
  .meta-row {{ display: flex; gap: 10px; font-size: 0.88rem; color: var(--color-dark-muted); margin-bottom: 30px; flex-wrap: wrap; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 15px; }}
  .region-tag {{ display: inline-block; font-size: 0.75rem; font-weight: 600; background: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 999px; padding: 3px 12px; color: var(--color-primary-hover); margin-bottom: 12px; }}
  
  /* Bloques Interactivos y Secciones */
  .epigraph {{ font-family:Georgia,serif; font-style:italic; font-size:1.15rem; color:var(--color-dark-muted); border-left:3px solid var(--color-primary); padding:6px 20px; margin:24px 0; }}
  .epigraph cite {{ display:block; font-style:normal; font-size:0.85rem; margin-top:8px; color:var(--color-accent); }}
  .summary-box {{ background:var(--bg-secondary); border:1px solid var(--border-color); border-radius:14px; padding:22px 24px; margin:24px 0 32px; }}
  .summary-box p.callout-title {{ margin-bottom:10px; font-weight:600; color:var(--color-dark); }}
  .summary-box ul {{ margin-left:20px; color:var(--color-dark-muted); }}
  .summary-box li {{ margin-bottom:6px; }}
  
  .hero-image-placeholder {{ width: 100%; aspect-ratio: 16 / 9; max-height: 440px; background: var(--bg-secondary); border-radius: 18px; margin-bottom: 32px; display: flex; align-items: center; justify-content: center; overflow: hidden; box-shadow: var(--shadow-md); border: 1px solid var(--border-color); }}
  .hero-image-placeholder img {{ width: 100%; height: 100%; object-fit: cover; }}
  
  .toc {{ background:var(--bg-accent-light); border:1px solid var(--border-color); border-radius:14px; padding:18px 22px; margin:0 0 32px; font-size:0.92rem; }}
  .toc::before {{ content: attr(data-title); display:block; font-weight:600; margin-bottom:8px; color:var(--color-dark); }}
  .toc ul {{ list-style:none; }}
  .toc a {{ text-decoration:none; color:var(--color-dark-muted); }}
  .toc a:hover {{ color:var(--color-primary-hover); }}
  .toc li {{ margin-bottom:6px; }}
  
  .article-body h2 {{ font-family:Georgia,serif; font-weight:400; font-size:1.8rem; margin:40px 0 14px; color:var(--color-dark); scroll-margin-top:20px; }}
  .article-body h3 {{ font-family:Georgia,serif; font-size:1.3rem; margin:28px 0 10px; color:var(--color-dark); scroll-margin-top:20px; }}
  .article-body p {{ margin-bottom:18px; color:var(--color-dark-muted); font-size:1.05rem; }}
  .article-body ul, .article-body ol {{ margin:0 0 18px 22px; color:var(--color-dark-muted); }}
  .article-body li {{ margin-bottom:8px; }}
  .article-body img {{ width:100%; border-radius:14px; margin:28px 0; box-shadow:var(--shadow-sm); border:1px solid var(--border-color); object-fit:cover; }}
  
  .callout {{ border-radius:14px; padding:20px 22px; margin:28px 0; }}
  .callout-title {{ font-weight:600; margin-bottom:8px; color:var(--color-dark); }}
  .callout-body p {{ margin-bottom:8px; color:var(--color-dark-muted); }}
  .callout-tip {{ background:var(--bg-accent-light); border:1px solid var(--border-color); }}
  .callout-info {{ background:var(--bg-secondary); border-left:4px solid var(--color-accent); }}
  .callout-funfact {{ background:#FFF9E6; border:1px solid #FFE082; border-left:4px solid #FFB300; }}
  
  .stat-box {{ text-align:center; background:var(--bg-accent-light); border:1px solid var(--border-color); border-left:5px solid var(--color-accent); padding:26px 24px; border-radius:14px; margin:28px 0; box-shadow: var(--shadow-md); }}
  .stat-number {{ font-family:Georgia,serif; font-size:2.6rem; font-weight:700; color:var(--color-dark); margin-bottom:8px; line-height:1.1; }}
  .stat-caption {{ font-size:1.05rem; font-weight:500; color:var(--color-dark); line-height:1.6; opacity:1; }}
  
  .checklist-box {{ background:var(--bg-secondary); border:1px solid var(--border-color); }}
  .checklist {{ list-style:none; margin-top:10px; }}
  .checklist li {{ margin-bottom:10px; }}
  .checklist label {{ display:flex; gap:10px; align-items:flex-start; cursor:pointer; color:var(--color-dark-muted); }}
  .checklist input[type=checkbox] {{ margin-top:4px; accent-color:var(--color-primary); width:18px; height:18px; flex-shrink:0; }}
  .checklist-hint {{ font-size:0.78rem; color:rgba(42,37,35,0.5); margin-top:6px; }}
  
  .quiz-box {{ background:var(--bg-accent-light); border:1px solid var(--border-color); }}
  .quiz-question {{ margin-top:16px; }}
  .quiz-q {{ font-weight:600; margin-bottom:10px; color:var(--color-dark); }}
  .quiz-options {{ display:flex; flex-direction:column; gap:8px; }}
  .quiz-option {{ text-align:left; padding:10px 14px; border-radius:10px; border:1px solid var(--border-color); background:#fff; cursor:pointer; font-family:'Poppins',sans-serif; font-size:0.95rem; color:var(--color-dark); }}
  .quiz-option:hover:not(:disabled) {{ border-color:var(--color-primary); }}
  .quiz-option.correct {{ background:#E7F5EA; border-color:#4CAF50; }}
  .quiz-option.incorrect {{ background:#FBEAEA; border-color:#E57373; }}
  .quiz-option:disabled {{ cursor:default; }}
  
  .science-link {{ display:flex; gap:16px; align-items:center; background:var(--bg-secondary); border-radius:14px; padding:20px 22px; margin:32px 0; text-decoration:none; }}
  .science-link .sci-icon {{ font-size:1.6rem; }}
  .science-link .sci-text p:first-child {{ font-weight:600; color:var(--color-dark); margin-bottom:2px; }}
  .science-link .sci-text p:last-child {{ font-size:0.88rem; color:var(--color-dark-muted); }}
  
  .product-cta {{ margin:40px 0; padding:28px; border-radius:16px; background:var(--bg-secondary); border:1px solid var(--border-color); text-align:center; }}
  .product-cta p {{ margin-bottom:16px; color:var(--color-dark); }}
  .product-cta a.btn {{ display:inline-block; background:var(--color-primary); color:#fff; text-decoration:none; padding:14px 30px; border-radius:999px; font-weight:600; font-size:0.95rem; }}
  .product-cta a.btn:hover {{ background:var(--color-primary-hover); }}
  
  .related-section {{ margin-top:50px; }}
  .related-section h2 {{ font-family:Georgia,serif; font-weight:400; font-size:1.5rem; margin-bottom:16px; }}
  .related-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:18px; }}
  .related-card {{ border:1px solid var(--border-color); border-radius:14px; overflow:hidden; text-decoration:none; color:inherit; }}
  .related-card .card-video {{ aspect-ratio:16/10; object-fit:cover; display:flex; }}
  .related-card .rc-body {{ padding:14px; }}
  .related-card h3 {{ font-family:Georgia,serif; font-weight:400; font-size:1rem; color:var(--color-dark); }}
  
  .faq-section {{ margin-top:50px; }}
  .faq-section h2 {{ font-family:Georgia,serif; font-weight:400; font-size:1.5rem; margin-bottom:16px; }}
  .faq-item {{ border-bottom:1px solid var(--border-color); padding:16px 0; }}
  .faq-item summary {{ cursor:pointer; font-weight:600; color:var(--color-dark); }}
  .faq-item p {{ margin-top:10px; color:var(--color-dark-muted); }}
  
  footer.site-footer {{ background:var(--color-dark); color:rgba(255,255,255,0.7); text-align:center; padding:40px 24px; font-size:0.85rem; margin-top:60px; }}
  footer.site-footer a {{ color:#fff; }}
</style>
{article_schema}
</head>
"""

ARTICLE_TEMPLATE = BRAND_HEAD + """<body>
<!-- Gota de agua del logo flotante -->
<div class="floating-droplet" onclick="window.location.href='{home_url}'" title="PepaGold - Volver al inicio">
  <img alt="PepaGold Icon" src="/assets/imagenes/icono.svg"/>
</div>
<!-- Botón al Blog flotante -->
<a class="lang-selector-btn blog-nav-btn-floating" href="{blog_index_url}" style="position: fixed; top: 65px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">{active_flag}</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>
<!-- Selector de idiomas flotante -->
<div class="lang-selector-container">
  <button aria-expanded="false" aria-haspopup="listbox" class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">{lang_upper}</span>
    <span class="arrow-icon" style="font-size: 9px; color: var(--color-primary);">▼</span>
  </button>
  <ul class="lang-dropdown-menu" id="langDropdownMenu" role="listbox">
    {lang_dropdown_html}
  </ul>
</div>

<div class="wrap" style="padding-top: 130px;">
  {region_tag_html}
  <p class="eyebrow">{category_label}</p>
  <h1 class="article-title">{title}</h1>
  <div class="meta-row"><span>{date_display}</span><span>&middot;</span><span>{reading_time}</span><span>&middot;</span><span>{author}</span></div>
  
  {media_html}
  
  {epigraph_html}
  {summary_html}
  
  {toc_html}
  
  <div class="article-body">
    {body_html}
  </div>
  
  {science_link_html}
  
  {product_cta_html}
  
  {faq_html}
  {related_html}
</div>
<footer class="site-footer">
  <p>{footer_copy}</p>
</footer>
<script>
  // Menu desplegable
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {{
    btn.addEventListener('click', (e) => {{ e.stopPropagation(); container.classList.toggle('is-active'); }});
    document.addEventListener('click', () => {{ container.classList.remove('is-active'); }});
  }}
  
  // Checklist localstorage
  document.querySelectorAll('.cl-item').forEach(function(cb){{
    var k = 'pepagold_check_' + cb.dataset.key;
    cb.checked = localStorage.getItem(k) === '1';
    cb.addEventListener('change', function(){{ localStorage.setItem(k, cb.checked ? '1' : '0'); }});
  }});
  
  // Quiz
  function pgQuiz(btn, correct) {{
    var box = btn.closest('.quiz-question');
    box.querySelectorAll('.quiz-option').forEach(function(b){{ b.disabled = true; }});
    if (correct) {{ btn.classList.add('correct'); }}
    else {{
      btn.classList.add('incorrect');
      box.querySelectorAll('.quiz-option[data-correct="1"]').forEach(function(b){{ b.classList.add('correct'); }});
    }}
  }}

  // Service Worker PWA
  if ('serviceWorker' in navigator) {{
    window.addEventListener('load', function() {{
      navigator.serviceWorker.register('/sw.js').catch(function(){{}});
    }});
  }}
</script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang_attr}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog | PepaGold</title>
<meta name="description" content="Artículos sobre cuidado de la piel sin químicos, sostenibilidad y skincare consciente.">
<link rel="canonical" href="{canonical}">
<link rel="icon" type="image/svg+xml" href="/assets/imagenes/icono.svg" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root {{
    --font-serif: Georgia, "Times New Roman", serif;
    --font-sans: 'Poppins', sans-serif;
    --color-primary: #D48C90; --color-primary-hover: #C97A7E; --color-accent: #E29578;
    --color-dark: #2A2523; --color-dark-muted: #5A524E; --border-color: rgba(212, 140, 144, 0.2);
    --bg-primary: #FFFFFF; --bg-secondary: #FAF6F5;
    --shadow-sm: 0 4px 15px rgba(42, 37, 35, 0.05); --shadow-lg: 0 15px 35px rgba(212, 140, 144, 0.15);
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: var(--font-sans); color: var(--color-dark-muted); background: var(--bg-primary); line-height: 1.8; }}
  h1, h2, h3 {{ font-family: var(--font-serif); color: var(--color-dark); line-height: 1.2; margin-bottom: 20px; }}
  a {{ text-decoration: none; }}

  .site-header {{ padding: 20px 24px; border-bottom: 1px solid var(--border-color); display:flex; align-items:center; justify-content:space-between; }}
  .site-header a.logo {{ font-family: Georgia, serif; font-size:1.3rem; color:var(--color-dark); text-decoration:none; font-weight:600; }}
  .site-header nav a {{ margin-left:20px; font-size:0.9rem; color:var(--color-dark-muted); }}

  .blog-header {{ text-align: center; padding: 80px 20px 40px; background: var(--bg-secondary); }}
  .blog-header h1 {{ font-size: 2.8rem; margin-bottom: 10px; }}
  .blog-header p {{ font-size: 1.1rem; max-width: 600px; margin: 0 auto; color: var(--color-dark-muted); }}

  .chips {{ display:flex; gap:10px; flex-wrap:wrap; justify-content: center; margin: -20px auto 40px; max-width: 1000px; padding: 0 20px; }}
  .chips a {{ font-size:0.82rem; padding:7px 16px; border-radius:999px; border:1px solid var(--border-color); color:var(--color-dark-muted); background: var(--bg-primary); transition: all 0.2s; }}
  .chips a.active {{ background: var(--color-primary); color:#fff; border-color: var(--color-primary); }}

  .pain-agitation-section {{ background: var(--bg-primary); padding: 40px 20px 70px; text-align: center; overflow: hidden; }}
  .interactive-pain {{ max-width: 1000px; margin: 0 auto; display: flex; flex-direction: column; gap: 80px; }}
  .pain-card-v2 {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 50px; align-items: center; text-align: left; }}
  .pain-card-v2:nth-child(even) {{ direction: rtl; }}
  .pain-card-v2:nth-child(even) > * {{ direction: ltr; }}

  .card-video {{ width: 100%; max-width: 440px; margin: 0 auto; aspect-ratio: 16 / 9; border-radius: 16px; box-shadow: var(--shadow-sm); overflow: hidden; display: flex; align-items: center; justify-content: center; transition: transform 0.4s ease; border: 1px solid var(--border-color); }}
  .card-video img {{ width: 100%; height: 100%; object-fit: cover; }}
  .card-video:hover {{ box-shadow: var(--shadow-lg); transform: translateY(-5px); }}

  .text-content {{ display: flex; flex-direction: column; gap: 12px; }}
  .accent-subtitle {{ color: var(--color-accent); font-weight: 600; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1.5px; }}
  .problem-title {{ font-family: var(--font-serif); font-size: 2.2rem; margin: 0; }}
  .problem-description {{ font-size: 1.1rem; color: var(--color-dark-muted); margin: 0; }}

  .read-btn {{ display: inline-flex; align-items: center; gap: 8px; margin-top: 15px; font-weight: 600; color: var(--color-primary); transition: all 0.3s ease; align-self: flex-start; }}
  .read-btn::after {{ content: '→'; }}
  
  /* Lang selector and Floating Buttons */
  .floating-droplet {{ position: fixed; top: 65px; left: 20px; width: 56px; height: 56px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.3); border-radius: 0 50% 50% 50%; transform: rotate(45deg); display: flex; align-items: center; justify-content: center; box-shadow: 0 8px 25px rgba(42, 37, 35, 0.08); z-index: 1000; transition: transform 0.3s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.3s ease; cursor: pointer; text-decoration: none; }}
  .floating-droplet:hover {{ transform: rotate(45deg) scale(1.08); box-shadow: 0 12px 30px rgba(212, 140, 144, 0.25); border-color: var(--color-primary); }}
  .floating-droplet img {{ width: 28px; height: 28px; transform: rotate(-45deg); transition: transform 0.3s ease; }}
  .lang-selector-container {{ position: fixed; top: 65px; right: 20px; z-index: 1000; font-family: 'Poppins', sans-serif; }}
  .lang-selector-btn {{ display: flex; align-items: center; gap: 8px; padding: 6px 14px; border-radius: 30px; background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(212, 140, 144, 0.25); color: var(--color-dark); font-size: 14px; font-weight: 500; cursor: pointer; box-shadow: 0 4px 12px rgba(42, 37, 35, 0.04); transition: all 0.3s ease; text-decoration: none; }}
  .lang-selector-btn:hover {{ border-color: var(--color-primary); box-shadow: 0 6px 16px rgba(212, 140, 144, 0.15); transform: translateY(-1px); }}
  .lang-selector-btn .arrow-icon {{ font-size: 9px; color: var(--color-primary); transition: transform 0.3s ease; }}
  .lang-selector-container.is-active .lang-selector-btn .arrow-icon {{ transform: rotate(180deg); }}
  .lang-dropdown-menu {{ position: absolute; top: calc(100% + 8px); right: 0; min-width: 170px; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border: 1px solid rgba(212, 140, 144, 0.2); border-radius: 12px; padding: 8px 0; margin: 0; list-style: none; box-shadow: 0 10px 30px rgba(42, 37, 35, 0.08); opacity: 0; visibility: hidden; transform: translateY(-8px); transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1); max-height: 320px; overflow-y: auto; }}
  .lang-selector-container.is-active .lang-dropdown-menu {{ opacity: 1; visibility: visible; transform: translateY(0); }}
  .lang-option {{ padding: 10px 18px; font-size: 14px; color: var(--color-dark); cursor: pointer; display: flex; align-items: center; gap: 10px; text-decoration: none; transition: all 0.2s ease; }}
  .lang-option:hover {{ background: rgba(212, 140, 144, 0.08); color: var(--color-primary-hover); }}
  .lang-option.is-selected {{ background: rgba(212, 140, 144, 0.12); color: var(--color-primary); font-weight: 600; }}
  .blog-nav-btn-floating {{ right: 130px; top: 65px; }}

  /* Scrollbar personalizado para el menú de idiomas */
  .lang-dropdown-menu::-webkit-scrollbar {{ width: 4px; }}
  .lang-dropdown-menu::-webkit-scrollbar-track {{ background: transparent; }}
  .lang-dropdown-menu::-webkit-scrollbar-thumb {{ background: rgba(212, 140, 144, 0.3); border-radius: 10px; }}
  .lang-dropdown-menu::-webkit-scrollbar-thumb:hover {{ background: var(--color-primary); }}

  @media (max-width: 600px) {{
    .floating-droplet {{ top: 65px; left: 12px; width: 46px; height: 46px; }}
    .floating-droplet img {{ width: 22px; height: 22px; }}
    .lang-selector-container {{ top: 65px; right: 12px; }}
    .lang-selector-btn {{ padding: 5px 11px; font-size: 12px; }}
    .blog-nav-btn-floating {{ right: 110px !important; }}
  }}
  
  footer.site-footer {{ background: var(--color-dark); color: rgba(255,255,255,0.7); text-align:center; padding: 40px 24px; font-size:0.85rem; }}
  
  @media (max-width: 768px) {{
    .pain-card-v2 {{ grid-template-columns: 1fr; gap: 30px; }}
    .pain-card-v2:nth-child(even) {{ direction: ltr; }}
  }}
</style>
</head>
<body>
<!-- Gota de agua del logo flotante -->
<div class="floating-droplet" onclick="window.location.href='{home_url}'" title="PepaGold - Volver al inicio">
  <img alt="PepaGold Icon" src="/assets/imagenes/icono.svg"/>
</div>
<!-- Botón al Blog flotante -->
<a class="lang-selector-btn blog-nav-btn-floating" href="{blog_index_url}" style="position: fixed; top: 65px; z-index: 1000; text-decoration: none;" title="PepaGold Blog">
  <span class="active-flag">{active_flag}</span>
  <span class="blog-btn-text" style="font-weight: 500;">Blog</span>
</a>
<!-- Selector de idiomas flotante -->
<div class="lang-selector-container">
  <button aria-expanded="false" aria-haspopup="listbox" class="lang-selector-btn" id="langSelectorBtn">
    <span class="active-flag">🌐</span>
    <span class="active-lang-code">{lang_upper}</span>
    <span class="arrow-icon" style="font-size: 9px; color: var(--color-primary);">▼</span>
  </button>
  <ul class="lang-dropdown-menu" id="langDropdownMenu" role="listbox">
    {lang_dropdown_html}
  </ul>
</div>

<div style="padding-top: 130px; margin-bottom: 20px;"></div>

<div class="chips">{chips_html}</div>
<section class="pain-agitation-section">
  <div class="interactive-pain">
    {cards_html}
  </div>
</section>
<footer class="site-footer">
  <p>{footer_copy}</p>
</footer>
<script>
  const container = document.querySelector('.lang-selector-container');
  const btn = document.getElementById('langSelectorBtn');
  if (btn) {{
    btn.addEventListener('click', (e) => {{ e.stopPropagation(); container.classList.toggle('is-active'); }});
    document.addEventListener('click', () => {{ container.classList.remove('is-active'); }});
  }}
</script>
</body>
</html>
"""

# =========================================================================
# FUNCIONES DE RENDERIZADO
# =========================================================================

def parse_post(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw, re.S)
    if not m: raise ValueError(f"{path}: falta el bloque frontmatter '---'")
    meta = yaml.safe_load(m.group(1)) or {}
    body_md = m.group(2)
    meta["_source"] = path
    return meta, body_md

def build_article_schema(meta, canonical, cover_abs):
    faq = meta.get("faq") or []
    locale = meta.get("locale", "es-ar")
    blocks = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": meta.get("title", ""), "description": meta.get("description", ""),
        "inLanguage": locale,
        "image": [cover_abs] if cover_abs else [], "datePublished": str(meta.get("date", "")),
        "author": {"@type": "Organization", "name": meta.get("author", "PepaGold")},
        "publisher": {"@type": "Organization", "name": "PepaGold", "logo": {"@type": "ImageObject", "url": f"{SITE_URL}/assets/imagenes/icono.svg"}},
        "mainEntityOfPage": canonical,
    }]
    if faq:
        blocks.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "inLanguage": locale,
            "mainEntity": [
                {"@type": "Question", "name": item["q"],
                 "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
                for item in faq
            ],
        })
    return "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False)}</script>' for b in blocks)

def render_epigraph(meta):
    ep = meta.get("epigraph")
    if not ep: return ""
    text = ep.get("text", "") if isinstance(ep, dict) else str(ep)
    author = ep.get("author", "") if isinstance(ep, dict) else ""
    cite = f"<cite>— {author}</cite>" if author else ""
    return f'<blockquote class="epigraph">“{text}”{cite}</blockquote>'

def render_summary(meta):
    items = meta.get("summary")
    if not items: return ""
    locale = meta.get("locale", "es-ar")
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    lis = "".join(f"<li>{_inline(i.get('punto', str(i)) if isinstance(i, dict) else str(i))}</li>" for i in items)
    return f'<div class="summary-box"><p class="callout-title">{i18n["summary_title"]}</p><ul>{lis}</ul></div>'

def render_faq(meta):
    faq = meta.get("faq") or []
    if not faq: return ""
    locale = meta.get("locale", "es-ar")
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    items = "".join(f'<details class="faq-item"><summary>{item["q"]}</summary><p>{item["a"]}</p></details>' for item in faq)
    return f'<div class="faq-section"><h2>{i18n["faq_title"]}</h2>{items}</div>'

def render_science_link(meta, home_url):
    if meta.get("show_science_link") is False: return ""
    locale = meta.get("locale", "es-ar")
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    return (
        f'<a class="science-link" href="{home_url}#ciencia">'
        '<span class="sci-icon">🔬</span>'
        f'<span class="sci-text"><p>{i18n["science_title"]}</p>'
        f'<p>{i18n["science_desc"]}</p>'
        '</span></a>'
    )

def render_related(meta, lookup):
    slugs = meta.get("related") or []
    if not slugs: return ""
    locale = meta.get("locale", "es-ar")
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    cards = []
    for s_item in slugs:
        s = s_item.get('slug', s_item) if isinstance(s_item, dict) else s_item
        key = (locale, s)
        other = lookup.get(key)
        if not other: continue
        folder = LOCALE_FOLDERS[locale]
        base = f"{folder}/" if folder else ""
        url = f"/{base}blog/{s}/"
        other_media = other.get("media", [])
        if not other_media and other.get("cover_image"):
            other_media = [other.get("cover_image")]
        media_html = render_media(other_media)
        cards.append(f'<a class="related-card" href="{url}"><div class="card-video">{media_html}</div><div class="rc-body"><h3>{other.get("title", "")}</h3></div></a>')
    
    if not cards: return ""
    return f'<div class="related-section"><h2>{i18n["related_title"]}</h2><div class="related-grid">{"".join(cards)}</div></div>'

def render_article(meta, body_md, hreflang_tags, lookup):
    locale = meta["locale"]
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    folder = LOCALE_FOLDERS[locale]
    slug = meta["slug"]
    base = f"{folder}/" if folder else ""
    canonical = f"{SITE_URL}/{base}blog/{slug}/"
    home_url = f"/{base}" if folder else "/"
    blog_index_url = f"/{base}blog/"
    
    cover_src = get_cover_image(meta)
    cover_abs = f"{SITE_URL}{cover_src}" if cover_src else f"{SITE_URL}/assets/imagenes/icono.svg"
    if cover_src:
        media_gallery = render_media([cover_src])
        media_html = f'<div class="hero-image-placeholder">{media_gallery}</div>'
    else:
        media_html = ""
    
    region_tag_html = f'<span class="region-tag">{meta["region_label"]}</span><br>' if meta.get("region_label") else ""

    processed_md = preprocess_custom_blocks(body_md, slug, locale=locale)
    md_engine = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    body_html = md_engine.convert(processed_md)
    toc_raw = md_engine.toc
    
    # Inject localized TOC header
    toc_raw_localized = re.sub(r'class="toc"', f'class="toc" data-title="{i18n["toc_title"]}"', toc_raw)
    toc_html = toc_raw_localized if toc_raw.count("<li>") >= 2 else ""

    word_count = len(re.sub(r"<[^>]+>", " ", body_html).split())
    reading_time_num = max(1, round(word_count / 200))
    reading_time_str = f"{reading_time_num} {i18n['reading_time']}"
    date_display = format_localized_date(meta.get("date", ""), locale)

    category_label = meta.get("category_label") or get_cat_label(meta.get("category"), locale)
    schema = build_article_schema(meta, canonical, cover_abs)

    active_flag = LOCALE_INFO[locale]["flag"]
    dropdown_lis = []
    concept = meta.get("concept")
    for loc, info in LOCALE_INFO.items():
        fld = LOCALE_FOLDERS[loc]
        bs = f"{fld}/" if fld else ""
        is_sel = " is-selected" if loc == locale else ""
        
        translated_post = None
        if concept and concept in lookup:
            for p in lookup[concept]:
                if p["locale"] == loc:
                    translated_post = p
                    break
        
        if translated_post:
            url = f"/{bs}blog/{translated_post['slug']}/"
        else:
            url = f"/{bs}blog/"
        
        dropdown_lis.append(f'<li class="lang-option{is_sel}" onclick="window.location.href=\'{url}\'" role="option">{info["flag"]} {info["name"]}</li>')
    lang_dropdown_html = "\n".join(dropdown_lis)

    # Inject CTA I18N
    product_cta_html = f'''
  <div class="product-cta">
    <p>{i18n["cta_desc"]}</p>
    <a class="btn" href="{home_url}">{i18n["cta_btn"]}</a>
  </div>
    '''

    html = ARTICLE_TEMPLATE.format(
        lang_attr=locale.split("-")[0], lang_upper=locale.split("-")[0].upper(),
        title=meta.get("title", ""), description=meta.get("description", ""),
        canonical=canonical, cover_image_abs=cover_abs, hreflang_tags=hreflang_tags, article_schema=schema,
        home_url=home_url, blog_index_url=blog_index_url, region_tag_html=region_tag_html,
        category_label=category_label, date_display=date_display, reading_time=reading_time_str,
        author=meta.get("author", "PepaGold"), epigraph_html=render_epigraph(meta), summary_html=render_summary(meta),
        media_html=media_html, toc_html=toc_html, body_html=body_html, science_link_html=render_science_link(meta, home_url),
        product_cta_html=product_cta_html, footer_copy=i18n["footer_copy"],
        faq_html=render_faq(meta), related_html=render_related(meta, lookup),
        active_flag=active_flag, lang_dropdown_html=lang_dropdown_html,
    )
    out_dir = os.path.join(folder, "blog", slug) if folder else os.path.join("blog", slug)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical

def build_hreflang_tags(concept, posts_by_concept):
    if not concept or concept not in posts_by_concept: return ""
    tags = []
    for p in posts_by_concept[concept]:
        loc = p["locale"]
        folder = LOCALE_FOLDERS[loc]
        base = f"{folder}/" if folder else ""
        url = f"{SITE_URL}/{base}blog/{p['slug']}/"
        tags.append(f'<link rel="alternate" hreflang="{HREFLANG_MAP[loc]}" href="{url}" />')
    return "\n".join(tags)

def render_index(locale, posts):
    folder = LOCALE_FOLDERS[locale]
    base = f"{folder}/" if folder else ""
    home_url = f"/{base}" if folder else "/"
    blog_index_url = f"/{base}blog/"
    canonical = f"{SITE_URL}/{base}blog/"
    i18n = I18N_STRINGS.get(locale, I18N_STRINGS["es-ar"])
    posts_sorted = sorted(posts, key=lambda p: str(p.get("date", "")), reverse=True)
    
    cats_present = sorted({p.get("category") for p in posts_sorted if p.get("category")})
    all_label = i18n.get("index_all", "Todos")
    chips = [f'<a href="#" class="active">{all_label}</a>']
    for c in cats_present:
        chips.append(f'<a href="#{c}">{get_cat_label(c, locale)}</a>')
        
    cards = []
    for p in posts_sorted:
        url = f"/{base}blog/{p['slug']}/"
        cover_src = get_cover_image(p)
        media_html = render_media([cover_src]) if cover_src else ""
        cat_label = get_cat_label(p.get("category"), locale)
        
        card = f"""
    <div class="pain-card-v2" data-cat="{p.get("category","")}">
        <div class="card-video">{media_html}</div>
        <div class="text-content">
            <span class="accent-subtitle">{cat_label}</span>
            <h3 class="problem-title">{p.get('title', 'Sin Título')}</h3>
            <p class="problem-description">{p.get('description', '')}</p>
            <a href="{url}" class="read-btn">{i18n["read_btn"]}</a>
        </div>
    </div>
"""
        cards.append(card)
        
    active_flag = LOCALE_INFO[locale]["flag"]
    dropdown_lis = []
    for loc, info in LOCALE_INFO.items():
        fld = LOCALE_FOLDERS[loc]
        bs = f"{fld}/" if fld else ""
        url = f"/{bs}blog/"
        is_sel = " is-selected" if loc == locale else ""
        dropdown_lis.append(f'<li class="lang-option{is_sel}" onclick="window.location.href=\'{url}\'" role="option">{info["flag"]} {info["name"]}</li>')
    lang_dropdown_html = "\n".join(dropdown_lis)

    html = INDEX_TEMPLATE.format(
        lang_attr=locale.split("-")[0], lang_upper=locale.split("-")[0].upper(),
        canonical=canonical, home_url=home_url, chips_html="".join(chips), cards_html="".join(cards),
        active_flag=active_flag, lang_dropdown_html=lang_dropdown_html, blog_index_url=blog_index_url,
        index_title=i18n.get("index_title", "Blog | PepaGold"),
        index_desc=i18n["index_desc"], footer_copy=i18n["footer_copy"]
    )
    out_dir = os.path.join(folder, "blog") if folder else "blog"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return canonical

def update_sitemap(new_urls):
    if not os.path.exists(SITEMAP_PATH): return
    with open(SITEMAP_PATH, encoding="utf-8") as f:
        content = f.read()
    today = datetime.date.today().isoformat()
    added = 0
    for url in new_urls:
        if f"<loc>{xml_escape(url)}</loc>" in content: continue
        block = f'\n  <url>\n    <loc>{xml_escape(url)}</loc>\n    <lastmod>{today}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n'
        content = content.replace("</urlset>", block + "</urlset>")
        added += 1
    with open(SITEMAP_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"sitemap.xml actualizado: {added} URL(s) nueva(s).")

def main():
    md_files = []
    for root, _, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    md_files = sorted(md_files)
    
    if not md_files:
        print("No hay posts en blog/posts/. Nada que generar.")
        return

    all_meta = []
    for path in md_files:
        meta, body_md = parse_post(path)
        if "locale" not in meta: meta["locale"] = "es-ar"
        if meta["locale"] not in LOCALE_FOLDERS: meta["locale"] = "es-ar"
        if "slug" not in meta: meta["slug"] = os.path.basename(path).replace(".md", "")
        all_meta.append((meta, body_md))

    posts_by_concept = {}
    lookup = {}
    for meta, _ in all_meta:
        c = meta.get("concept")
        if c: posts_by_concept.setdefault(c, []).append(meta)
        lookup[(meta["locale"], meta["slug"])] = meta

    new_urls = []
    posts_by_locale = {}
    for meta, body_md in all_meta:
        hreflang_tags = build_hreflang_tags(meta.get("concept"), posts_by_concept)
        canonical = render_article(meta, body_md, hreflang_tags, lookup)
        new_urls.append(canonical)
        posts_by_locale.setdefault(meta["locale"], []).append(meta)

    for locale, posts in posts_by_locale.items():
        index_url = render_index(locale, posts)
        new_urls.append(index_url)

    # Bundled posts.json for CMS fallback & concept lookup
    json_posts = []
    concept_map = {}

    for meta, body_md in all_meta:
        loc = meta.get("locale", "es-ar")
        concept = meta.get("concept", meta["slug"])
        folder = LOCALE_FOLDERS.get(loc, "")
        web_url = f"/{folder}/blog/{meta['slug']}" if folder else f"/blog/{meta['slug']}"

        concept_map.setdefault(concept, {})[loc] = {
            "slug": meta["slug"],
            "title": meta["title"],
            "web_url": web_url,
            "phenomenon": meta.get("local_phenomenon", "Fenómeno Genérico"),
            "region_label": meta.get("region_label", loc)
        }

        if loc == "es-ar":
            json_posts.append({"meta": meta, "body": body_md, "path": f"blog/posts/es-ar/{meta['slug']}.md"})

    admin_bundle = {
        "posts": json_posts,
        "concept_map": concept_map
    }
    os.makedirs("admin", exist_ok=True)
    with open("admin/posts.json", "w", encoding="utf-8") as f:
        json.dump(admin_bundle, f, ensure_ascii=False, indent=2)

    update_sitemap(new_urls)
    print(f"Listo: {len(all_meta)} artículo(s) generado(s) en {len(posts_by_locale)} idioma(s). Admin posts.json actualizado.")

if __name__ == "__main__":
    main()
