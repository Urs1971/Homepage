import json
import os
import urllib.request
from urllib.parse import urlparse

# Ordner erstellen
os.makedirs('bilder', exist_ok=True)

def bild_herunterladen(url):
    """Lädt ein Bild herunter und gibt den lokalen Pfad zurück."""
    dateiname = os.path.basename(urlparse(url).path)
    lokaler_pfad = f'bilder/{dateiname}'

    if os.path.exists(lokaler_pfad):
        print(f'  Bereits vorhanden: {dateiname}')
        return lokaler_pfad

    try:
        print(f'  Lade herunter: {dateiname}')
        urllib.request.urlretrieve(url, lokaler_pfad)
        return lokaler_pfad
    except Exception as e:
        print(f'  FEHLER bei {dateiname}: {e}')
        return url  # Original-URL beibehalten bei Fehler

# === blog.json verarbeiten ===
print('\n--- Blog-Bilder ---')
with open('blog.json', 'r', encoding='utf-8') as f:
    blog = json.load(f)

for post in blog:
    post['bilder'] = [bild_herunterladen(b) for b in post['bilder']]

with open('blog.json', 'w', encoding='utf-8') as f:
    json.dump(blog, f, ensure_ascii=False, indent=2)

print('blog.json aktualisiert.')

# === awurf.json verarbeiten ===
print('\n--- A-Wurf Bilder ---')
with open('awurf.json', 'r', encoding='utf-8') as f:
    awurf = json.load(f)

for woche in awurf:
    for welpe in woche['welpen']:
        welpe['bild'] = bild_herunterladen(welpe['bild'])
    woche['gruppenbilder'] = [bild_herunterladen(b) for b in woche['gruppenbilder']]

with open('awurf.json', 'w', encoding='utf-8') as f:
    json.dump(awurf, f, ensure_ascii=False, indent=2)

print('awurf.json aktualisiert.')

# === Alle URLs in index.html ersetzen ===
print('\n--- index.html Bilder ---')
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Alle ofdreamfarry.ch Bild-URLs finden
urls = re.findall(r'https://ofdreamfarry\.ch/wp-content/uploads/[^\s\'"()]+', html)
urls = list(set(urls))  # Duplikate entfernen

for url in urls:
    lokaler_pfad = bild_herunterladen(url)
    dateiname = os.path.basename(lokaler_pfad)
    html = html.replace(url, f'bilder/{dateiname}')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('index.html aktualisiert.')

# === style.css anpassen ===
print('\n--- style.css Bilder ---')
with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

urls_css = re.findall(r'https://ofdreamfarry\.ch/wp-content/uploads/[^\s\'"()]+', css)
urls_css = list(set(urls_css))

for url in urls_css:
    lokaler_pfad = bild_herunterladen(url)
    dateiname = os.path.basename(lokaler_pfad)
    css = css.replace(url, f'bilder/{dateiname}')

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print('style.css aktualisiert.')
print('\nFertig! Alle Bilder sind im Ordner "bilder/" gespeichert.')
