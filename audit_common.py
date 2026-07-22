#!/usr/bin/env python3
"""
audit_common.py — Lo que comparten los dos auditores (artículos y estructura).

Si mañana agregás una marca o producto nuevo, se agrega ACÁ UNA SOLA VEZ y
automáticamente protege tanto los artículos del blog como la estructura del
sitio. Nunca dupliques esta lista en otro archivo.
"""
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

import re

HTML_TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_TOKEN_RE = re.compile(r"\{[a-zA-Z_]+\}")


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
    try:
        return detect(text)
    except LangDetectException:
        return None
