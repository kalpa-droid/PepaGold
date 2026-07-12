import os
import re
import json
import subprocess
from bs4 import BeautifulSoup

# Regional configurations mapping to translations.js keys
REGIONS = {
    "es-ar": {
        "folder": "", # Root folder
        "price": 64000,
        "priceOld": 80000,
        "symbol": "$",
        "currency": "ARS",
        "country_code": "AR",
        "flag_label": "🇦🇷 AR"
    },
    "es-mx": {
        "folder": "mx",
        "price": 890,
        "priceOld": 1190,
        "symbol": "$",
        "currency": "MXN",
        "country_code": "MX",
        "flag_label": "🇲🇽 MX"
    },
    "es-es": {
        "folder": "es",
        "price": 44,
        "priceOld": 55,
        "symbol": "€",
        "currency": "EUR",
        "country_code": "ES",
        "flag_label": "🇪🇸 ES"
    },
    "en": {
        "folder": "us",
        "price": 33.20,
        "priceOld": 40.00,
        "symbol": "$",
        "currency": "USD",
        "country_code": "US",
        "flag_label": "🇺🇸 US"
    },
    "fr": {
        "folder": "fr",
        "price": 44,
        "priceOld": 55,
        "symbol": "€",
        "currency": "EUR",
        "country_code": "FR",
        "flag_label": "🇫🇷 FR"
    },
    "de": {
        "folder": "de",
        "price": 44,
        "priceOld": 55,
        "symbol": "€",
        "currency": "EUR",
        "country_code": "DE",
        "flag_label": "🇩🇪 DE"
    },
    "it": {
        "folder": "it",
        "price": 44,
        "priceOld": 55,
        "symbol": "€",
        "currency": "EUR",
        "country_code": "IT",
        "flag_label": "🇮🇹 IT"
    },
    "pt-br": {
        "folder": "pt",
        "price": 240,
        "priceOld": 300,
        "symbol": "R$",
        "currency": "BRL",
        "country_code": "BR",
        "flag_label": "🇧🇷 BR"
    },
    "ru": {
        "folder": "ru",
        "price": 2860,
        "priceOld": 3500,
        "symbol": "₽",
        "currency": "RUB",
        "country_code": "RU",
        "flag_label": "🇷🇺 RU"
    },
    "zh": {
        "folder": "zh",
        "price": 260,
        "priceOld": 320,
        "symbol": "¥",
        "currency": "CNY",
        "country_code": "CN",
        "flag_label": "🇨🇳 CN"
    }
}



COMPLIANCE_DATA = {
    "es-ar": {
        "title": "Defensa del Consumidor",
        "link_text": "Ventanilla Federal de Defensa del Consumidor",
        "link_url": "https://www.argentina.gob.ar/produccion/defensadelconsumidor",
        "badge_html": '<img src="https://www.afip.gob.ar/images/f960/DATAWEB.jpg" alt="Data Fiscal" id="complianceImg" style="max-height:60px; opacity:0.9;">'
    },
    "es-mx": {
        "title": "Defensa del Consumidor",
        "link_text": "Procuraduría Federal del Consumidor (PROFECO)",
        "link_url": "https://www.gob.mx/profeco",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">CONFIANZA VERIFICADA</span></div>'
    },
    "es-es": {
        "title": "Defensa del Consumidor",
        "link_text": "Resolución de litigios en línea (Unión Europea)",
        "link_url": "https://ec.europa.eu/consumers/odr/",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">CUMPLIMIENTO UE</span></div>'
    },
    "en": {
        "title": "Consumer Protection",
        "link_text": "FTC Consumer Protection Guidelines",
        "link_url": "https://www.ftc.gov/consumer-protection",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">VERIFIED SECURE</span></div>'
    },
    "fr": {
        "title": "Protection du Consommateur",
        "link_text": "Règlement en ligne des litiges de l'UE (RLL)",
        "link_url": "https://ec.europa.eu/consumers/odr/",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">SÉCURITÉ VÉRIFIÉE</span></div>'
    },
    "de": {
        "title": "Verbraucherschutz",
        "link_text": "Online-Streitbeilegung-Plattform der EU (OS)",
        "link_url": "https://ec.europa.eu/consumers/odr/",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">SICHERHEIT GEPRÜFT</span></div>'
    },
    "it": {
        "title": "Tutela dei Consumatori",
        "link_text": "Risoluzione delle controversie online dell'UE",
        "link_url": "https://ec.europa.eu/consumers/odr/",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">SICUREZZA VERIFICATA</span></div>'
    },
    "pt-br": {
        "title": "Defesa do Consumidor",
        "link_text": "Resolução de Litígios em Linha (União Europeia)",
        "link_url": "https://ec.europa.eu/consumers/odr/",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">CONFIANÇA VERIFICADA</span></div>'
    },
    "ru": {
        "title": "Права потребителей",
        "link_text": "Роспотребнадзор — защита прав потребителей",
        "link_url": "https://www.rospotrebnadzor.ru",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">ПРОВЕРЕНО И БЕЗОПАСНО</span></div>'
    },
    "zh": {
        "title": "消费者权益保护",
        "link_text": "中华人民共和国工业和信息化部 (MIIT)",
        "link_url": "https://beian.miit.gov.cn",
        "badge_html": '<div class="compliance-badge-trust" style="display: inline-flex; align-items: center; gap: 8px; padding: 8px 12px; border-radius: 8px; background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); margin-top: 10px;"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><path d="M9 11l2 2 4-4"></path></svg><span style="font-family:var(--font-sans); font-size:0.75rem; font-weight:var(--weight-semibold); color:rgba(255,255,255,0.85); letter-spacing:0.5px; text-transform:uppercase;">官方合规认证</span></div>'
    }
}

HOSTNAMES = {
    "AR": "greenwayglobal.ar",
    "MX": "greenwayglobal.mx",
    "US": "greenwayglobal.com",
    "RU": "greenwayglobal.com",
    "CN": "greenwayglobal.com",
    "ES": "new.mygreenway.eu",
    "FR": "new.mygreenway.eu",
    "DE": "new.mygreenway.eu",
    "IT": "new.mygreenway.eu",
    "BR": "new.mygreenway.eu"
}

TITLE_PATTERNS = {
    "es-ar": "Laska Mini Set | Limpieza facial sin químicos — Greenway",
    "es-mx": "Laska Mini Set | Limpieza facial sin químicos — Greenway",
    "es-es": "Laska Mini Set | Limpieza facial sin químicos — Greenway",
    "en": "Laska Mini Set | Chemical-free facial cleansing — Greenway",
    "fr": "Laska Mini Set | Nettoyage du visage sans produits chimiques — Greenway",
    "de": "Laska Mini Set | Chemiefreie Gesichtsreinigung — Greenway",
    "it": "Laska Mini Set | Pulizia del viso senza sostanze chimiche — Greenway",
    "pt-br": "Laska Mini Set | Limpeza facial sem químicos — Greenway",
    "ru": "Laska Mini Set | Очищение лица без химии — Greenway",
    "zh": "Laska Mini Set | 物理性无化学洁面套装 — Greenway"
}

DESC_PATTERNS = {
    "es-ar": "Set reutilizable de microfibra UpPoly para limpiar rostro, cuello y escote solo con agua. Sin químicos. Dura hasta 2 años.",
    "es-mx": "Set reutilizable de microfibra UpPoly para limpiar rostro, cuello y escote solo con agua. Sin químicos. Dura hasta 2 años.",
    "es-es": "Set de microfibra reutilizable UpPoly para limpieza facial. Desmaquíllate solo con agua. Sin químicos. Dura hasta 2 años.",
    "en": "Reusable UpPoly microfiber set to cleanse face, neck, and décolleté with water only. Chemical-free. Lasts up to 2 years.",
    "fr": "Coffret réutilisable en microfibres UpPoly pour nettoyer visage, cou et décolleté avec de l'eau seulement. Sans chimie. Dure jusqu'à 2 ans.",
    "de": "Wiederverwendbares UpPoly-Mikrofaserset zur Reinigung von Gesicht, Hals und Dekolleté nur mit Wasser. Ohne Chemie. Hält bis zu 2 Jahre.",
    "it": "Set riutilizzabile in microfibra UpPoly per la pulizia di viso, collo e décolleté solo con acqua. Senza sostanze chimiche. Dura fino a 2 anni.",
    "pt-br": "Kit reutilizável de microfibra UpPoly para limpar rosto, pescoço e colo apenas com água. Sem químicos. Dura até 2 anos.",
    "ru": "Многоразовый набор из микроволокна UpPoly для очищения лица, шеи и декольте только водой. Без химии. Служит до 2 лет.",
    "zh": "采用 UpPoly 超细纤维的环保卸妆洁面套装，只需温水，零化学添加。可重复清洗使用长达2年。"
}

def format_price(amount, currency, symbol):
    if currency in ["ARS", "MXN"]:
        return f"{symbol}{int(amount):,}".replace(",", ".")
    elif currency == "EUR":
        return f"{int(amount)} {symbol}"
    elif currency == "USD":
        return f"{symbol}{amount:.2f}"
    elif currency == "RUB":
        return f"{int(amount):,} {symbol}".replace(",", " ")
    elif currency == "BRL":
        return f"{symbol} {int(amount)}"
    elif currency == "CNY":
        return f"{symbol}{int(amount)}"
    else:
        return f"{symbol}{amount} {currency}"

def adjust_paths(soup):
    def fix_path(path):
        if not path:
            return path
        # Do not modify external URLs, absolute paths from drive root, or anchors
        if path.startswith(('http://', 'https://', '//', '#', 'mailto:', 'tel:')):
            return path
        if path.startswith('/'):
            return path
        return '../' + path

    for tag in soup.find_all(attrs={"src": True}):
        tag["src"] = fix_path(tag["src"])
    for tag in soup.find_all(attrs={"href": True}):
        tag["href"] = fix_path(tag["href"])
    for tag in soup.find_all(attrs={"poster": True}):
        tag["poster"] = fix_path(tag["poster"])
    for tag in soup.find_all("source"):
        if tag.has_attr("src"):
            tag["src"] = fix_path(tag["src"])
        if tag.has_attr("srcset"):
            tag["srcset"] = fix_path(tag["srcset"])

def main():
    # 1. Load translations JSON via node
    cmd = ["node", "-e", "global.window = {}; require('./js/translations.js'); console.log(JSON.stringify(global.window.siteTranslations));"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if res.returncode != 0:
        print("Error compiling translations JS:", res.stderr)
        return
    site_translations = json.loads(res.stdout)

    # 2. Read base template
    with open('template.html', 'r', encoding='utf-8') as f:
        template_content = f.read()

    # 3. Process each region
    for lang, config in REGIONS.items():
        print(f"Compiling regional version: {lang} ({config['country_code']})")
        
        soup = BeautifulSoup(template_content, 'html.parser')
        
        # Get translation dictionary
        dict_trans = site_translations.get(lang, site_translations.get("en"))
        
        # Format prices
        formatted_price = format_price(config["price"], config["currency"], config["symbol"])
        formatted_price_old = format_price(config["priceOld"], config["currency"], config["symbol"])
        
        # Set translated title and meta tags
        soup.title.string = TITLE_PATTERNS.get(lang, TITLE_PATTERNS["en"])
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            meta_desc["content"] = DESC_PATTERNS.get(lang, DESC_PATTERNS["en"])
        
        # Update html lang attribute
        soup.html["lang"] = lang.split("-")[0]
        
        # Update elements with data-i18n attributes
        elements = soup.find_all(attrs={"data-i18n": True})
        for el in elements:
            key = el["data-i18n"]
            if key in dict_trans:
                translated_text = dict_trans[key]
                
                # Replace template variables
                if "{price}" in translated_text:
                    translated_text = translated_text.replace("{price}", formatted_price)
                if "{country}" in translated_text:
                    # Lookup translated country name
                    c_key = f"country_{config['country_code']}"
                    c_name = dict_trans.get(c_key, config["country_code"])
                    translated_text = translated_text.replace("{country}", c_name)
                if "{currency}" in translated_text:
                    translated_text = translated_text.replace("{currency}", config["currency"])
                
                el.clear()
                parsed_frag = BeautifulSoup(translated_text, 'html.parser')
                el.append(parsed_frag)

        # Update buy links hostname
        target_host = HOSTNAMES.get(config["country_code"], "greenwayglobal.com")
        for link in soup.find_all("a", href=True):
            if "greenway" in link["href"]:
                try:
                    from urllib.parse import urlparse, urlunparse
                    u = urlparse(link["href"])
                    u = u._replace(netloc=target_host)
                    link["href"] = urlunparse(u)
                except Exception:
                    pass

        # Update local compliance block dynamically
        comp_data = COMPLIANCE_DATA.get(lang, COMPLIANCE_DATA["en"])
        title_el = soup.find(id="complianceTitle")
        link_el = soup.find(id="complianceLink")
        img_link_el = soup.find(id="complianceImgLink")
        
        if title_el and link_el and img_link_el:
            title_el.string = comp_data["title"]
            link_el.string = comp_data["link_text"]
            link_el["href"] = comp_data["link_url"]
            img_link_el["href"] = comp_data["link_url"]
            
            # Clear current badge content and append the custom HTML/SVG badge
            img_link_el.clear()
            parsed_badge = BeautifulSoup(comp_data["badge_html"], 'html.parser')
            img_link_el.append(parsed_badge)

        # Update visual active flag and code in switcher
        flag_el = soup.find(class_="active-flag")
        code_el = soup.find(class_="active-lang-code")
        if flag_el and code_el:
            parts = config["flag_label"].split(" ")
            flag_el.string = parts[0]
            code_el.string = parts[1]

        # Update dropdown menu option class to reflect selection
        options = soup.find_all(class_="lang-option")
        for opt in options:
            # Matches strings like changeLang('es-mx', '/mx/')
            if f"'{lang}'" in opt.get("onclick", ""):
                opt["class"] = opt.get("class", []) + ["is-selected"]
            else:
                classes = opt.get("class", [])
                if "is-selected" in classes:
                    classes.remove("is-selected")
                    opt["class"] = classes



        # Prepend ../ to relative assets paths if we are inside a subdirectory
        if config["folder"]:
            adjust_paths(soup)

        # Generate HTML string
        html_out = str(soup)

        # Update prices in the ticket animation script using simple regex replacements
        keys_to_replace = [
            "p1_sol", "p1_sol_reus", 
            "prod_micellar", "prod_balm", "prod_oil", "prod_biphasic", 
            "prod_milk", "prod_gel", "prod_wipes", "prod_pads", "prod_reusable",
            "rit_step1_title", "rit_step1_desc",
            "rit_step2_title", "rit_step2_desc",
            "rit_step3_title", "rit_step3_desc"
        ]
        for key in keys_to_replace:
            if key in dict_trans:
                val = dict_trans[key].replace('"', '\\"')
                pattern = rf'/\*{key}\*/".*?"/\*/{key}\*/'
                replacement = f'/*{key}*/"{val}"/*{key}*/'
                html_out = re.sub(pattern, replacement, html_out)

        # Update JSON-LD schema price
        html_out = html_out.replace('"price": "64000"', f'"price": "{int(config["price"])}"')
        html_out = html_out.replace('"priceCurrency": "ARS"', f'"priceCurrency": "{config["currency"]}"')

        # Clean static values in HTML card prices if any
        # (Template defaults to ARS price classes)
        if config["currency"] != "ARS":
            html_out = html_out.replace('$80.000 ARS', formatted_price_old)
            html_out = html_out.replace('$64.000 ARS', formatted_price)

        # Write output file
        if config["folder"]:
            os.makedirs(config["folder"], exist_ok=True)
            output_path = os.path.join(config["folder"], "index.html")
        else:
            output_path = "index.html"

        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(html_out)
        print(f"Generated successfully: {output_path}")

if __name__ == "__main__":
    main()
