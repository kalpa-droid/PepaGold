#!/usr/bin/env python3
"""
audit_common.py — Lo que comparten los dos auditores (artículos y estructura).

Si mañana agregás una marca, producto o categoría nueva, se agrega ACÁ UNA SOLA VEZ
y automáticamente protege tanto los artículos del blog como la estructura del sitio.
"""
import re
from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0

# Nombres propios y términos científicos que NUNCA deben traducirse.
BRAND_WHITELIST = [
    "PepaGold", "Laska Mini Set", "Laska Mini", "Laska", "Green Fiber",
    "Greenway", "Greenway Global", "UpPoly", "OEKO-TEX", "PETA",
    "CARE SET", "CARE 4", "CARE 6", "CARE 15", "TEWL",
    "Staphylococcus epidermidis", "Staphylococcus", "epidermidis", "S. epidermidis",
    "Poloxamer 184", "Poloxamer", "PEG", "Filaggrin",
]

MIN_CHARS = 45  # frases más cortas que esto no son confiables para detectar idioma

BLOG_TO_SITE_LOCALE = {
    "es-ar": "es-ar", "es-mx": "es-mx", "es-es": "es-es",
    "en-us": "en", "fr-fr": "fr", "de-de": "de",
    "it-it": "it", "pt-br": "pt-br", "ru-ru": "ru", "zh-hans": "zh",
}

SITE_EXPECTED_LANG = {
    "es-ar": "es", "es-mx": "es", "es-es": "es",
    "en": "en", "fr": "fr", "de": "de",
    "it": "it", "pt-br": "pt", "ru": "ru", "zh": "zh-cn",
}

BLOG_EXPECTED_LANG = {
    "es-ar": "es", "es-mx": "es", "es-es": "es",
    "en-us": "en", "fr-fr": "fr", "de-de": "de",
    "it-it": "it", "pt-br": "pt", "ru-ru": "ru", "zh-hans": "zh-cn",
}

# MATRIZ UNIVERSAL DE CATEGORÍAS TRADUCIDAS (10 LOCALES)
CATEGORY_TRANSLATION_MAP = {
    "barrera-cutanea": {
        "es-ar": "🔬 Ciencia de la Piel",
        "es-mx": "🔬 Ciencia de la Piel",
        "es-es": "🔬 Ciencia de la Piel",
        "en-us": "🔬 Skin Science",
        "fr-fr": "🔬 Science de la Peau",
        "de-de": "🔬 Hautwissenschaft",
        "it-it": "🔬 Scienza della Pelle",
        "pt-br": "🔬 Ciência da Pele",
        "ru-ru": "🔬 Наука о коже",
        "zh-hans": "🔬 皮肤科学"
    },
    "rutinas-minimalismo": {
        "es-ar": "🧘‍♀️ Rutinas y Skinimalismo",
        "es-mx": "🧘‍♀️ Rutinas y Skinimalismo",
        "es-es": "🧘‍♀️ Rutinas y Skinimalismo",
        "en-us": "🧘‍♀️ Routines & Skinimalism",
        "fr-fr": "🧘‍♀️ Routines & Skinimalisme",
        "de-de": "🧘‍♀️ Routinen & Skinimalismus",
        "it-it": "🧘‍♀️ Routine & Skinimalismo",
        "pt-br": "🧘‍♀️ Rotinas e Skinimalismo",
        "ru-ru": "🧘‍♀️ Уход и скиннимализм",
        "zh-hans": "🧘‍♀️ 护肤流程与极简主义"
    },
    "ingredientes-dermatologia": {
        "es-ar": "🧪 Ingredientes y Ciencia",
        "es-mx": "🧪 Ingredientes y Ciencia",
        "es-es": "🧪 Ingredientes y Ciencia",
        "en-us": "🧪 Ingredients & Science",
        "fr-fr": "🧪 Ingrédients & Science",
        "de-de": "🧪 Inhaltsstoffe & Wissenschaft",
        "it-it": "🧪 Ingredienti e Scienza",
        "pt-br": "🧪 Ingredientes e Ciência",
        "ru-ru": "🧪 Ингредиенты и наука",
        "zh-hans": "🧪 成分与科学"
    },
    "salud-sensibilidad": {
        "es-ar": "🌿 Piel Sensible y Salud",
        "es-mx": "🌿 Piel Sensible y Salud",
        "es-es": "🌿 Piel Sensible y Salud",
        "en-us": "🌿 Sensitive Skin & Health",
        "fr-fr": "🌿 Peau Sensible & Santé",
        "de-de": "🌿 Empfindliche Haut & Gesundheit",
        "it-it": "🌿 Pelle Sensibile e Salute",
        "pt-br": "🌿 Pele Sensível e Saúde",
        "ru-ru": "🌿 Чувствительная кожа и здоровье",
        "zh-hans": "🌿 敏感肌与健康"
    },
    "exposoma-ambiente": {
        "es-ar": "🛡️ Exposoma y Ambiente",
        "es-mx": "🛡️ Exposoma y Ambiente",
        "es-es": "🛡️ Exposoma y Ambiente",
        "en-us": "🛡️ Exposome & Environment",
        "fr-fr": "🛡️ Exposome & Environnement",
        "de-de": "🛡️ Exposom & Umwelt",
        "it-it": "🛡️ Esposoma e Ambiente",
        "pt-br": "🛡️ Exposoma e Ambiente",
        "ru-ru": "🛡️ Экспозом и окружающая среда",
        "zh-hans": "🛡️ 暴露组与环境"
    }
}

HTML_TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_TOKEN_RE = re.compile(r"\{[a-zA-Z_]+\}")
CJK_CHAR_RE = re.compile(r"[\u4e00-\u9fff]")


def strip_brands(text):
    for b in BRAND_WHITELIST:
        text = text.replace(b, "")
    return text


def strip_for_detection(text):
    """Saca HTML y placeholders antes de detectar idioma."""
    text = HTML_TAG_RE.sub(" ", text or "")
    text = PLACEHOLDER_TOKEN_RE.sub(" ", text)
    return strip_brands(text)


def detect_lang(text):
    """Devuelve el código de idioma detectado, o None si el texto es
    demasiado corto para confiar en la detección."""
    text = strip_for_detection(text).strip()
    if len(text) < MIN_CHARS:
        return None
    
    cjk_count = len(CJK_CHAR_RE.findall(text))
    if cjk_count >= 10:
        return "zh-cn"

    try:
        return detect(text)
    except LangDetectException:
        return None
