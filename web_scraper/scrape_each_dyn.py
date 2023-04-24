import json
import scrape

# URL des Wikipedia-Artikels
url = "https://www.searchmetrics.com/de/glossar/website/"
soup = scrape.get_soup(url)
# Dictionary für die gespeicherten Informationen
artikel_info = {}

# Überschriften (h1, h2, h3) extrahieren
ueberschrift = None
for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
    if element.name in ['h1', 'h2', 'h3']:
        ueberschrift = element.text.strip()
        ueberschrift = ueberschrift.replace("[Bearbeiten | Quelltext bearbeiten]", "")
        artikel_info[ueberschrift] = []
    elif element.name == 'p' and ueberschrift:
        text = element.text.strip()
        artikel_info[ueberschrift].append(text)
    elif element.name == 'img' and ueberschrift:
        bild_url = element['src']
        artikel_info[ueberschrift].append(bild_url)

# Inhaltsverzeichnis (toc, vector-toc) extrahieren
toc_div = soup.find('div', {'id': 'toc'})
if toc_div:
    inhaltsverzeichnis = []
    for toc_item in toc_div.find_all(['li']):
        toc = toc_item.text.strip()
        inhaltsverzeichnis.append(toc)
    artikel_info["Inhaltsverzeichnis"] = inhaltsverzeichnis
    


# Extrahierte Informationen in ein JSON-Objekt schreiben
with open('website.json', 'w', encoding='utf-8') as file:
    json.dump(artikel_info, file, indent=4, ensure_ascii=False)

print("Done")
