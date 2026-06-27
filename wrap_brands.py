import sys
from bs4 import BeautifulSoup, NavigableString

brands = [
    "Laska Mini",
    "PepaGold",
    "UpPoly",
    "CARE 4",
    "CARE 15",
    "CARE 6",
    "Greenway Global",
    "Greenway"
]

def wrap_brands_in_text(text):
    # This is a bit tricky with raw string replacement, as we want to return a list of elements
    # But since BeautifulSoup allows replacing a NavigableString with a new BeautifulSoup fragment
    # we can construct HTML and parse it back.
    html_text = str(text)
    modified = False
    
    # Sort brands by length descending so "Greenway Global" matches before "Greenway"
    for brand in sorted(brands, key=len, reverse=True):
        if brand in html_text:
            # Simple replacement. Not robust if brand is inside an existing tag, but we are working on text nodes.
            replacement = f'<span class="notranslate" translate="no">{brand}</span>'
            html_text = html_text.replace(brand, replacement)
            modified = True
            
    if modified:
        return html_text
    return None

def process_html(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        html = f.read()

    # Pre-cleaning: Remove any already wrapped brands to prevent double wrapping
    for brand in brands:
        html = html.replace(f'<span class="notranslate" translate="no">{brand}</span>', brand)
        html = html.replace(f'<span class=\'notranslate\' translate=\'no\'>{brand}</span>', brand)

    soup = BeautifulSoup(html, 'html.parser')

    # Find all text nodes
    for text_node in soup.find_all(string=True):
        # Skip if parent is a script, style or the notranslate span itself
        parent = text_node.parent
        if parent.name in ['script', 'style']:
            continue
        if parent.name == 'span' and 'notranslate' in parent.get('class', []):
            continue
            
        new_html = wrap_brands_in_text(text_node)
        if new_html:
            # Parse the new HTML snippet and replace the text node
            new_nodes = BeautifulSoup(new_html, 'html.parser')
            text_node.replace_with(new_nodes)

    # Clean up some formatting issues BS4 introduces occasionally, but BS4 generally writes well.
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(str(soup))
        
    print(f"Processed {filename} successfully.")

if __name__ == '__main__':
    process_html('index.html')
