import json
from bs4 import BeautifulSoup
import requests

url = "https://de.wikipedia.org/wiki/Rom"

response = requests.get(url)
html_code = response.text

soup = BeautifulSoup(html_code, 'html.parser')

artikel_info = {}
count = 0 
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

toc_div = soup.find('div', {'id': 'toc'})
if toc_div:
    inhaltsverzeichnis = []
    for toc_item in toc_div.find_all(['li']):
        toc = toc_item.text.strip()
        inhaltsverzeichnis.append(toc)
    artikel_info["Inhaltsverzeichnis"] = inhaltsverzeichnis

neues_json = {}
aktuelles_leeres_objekt = None
for key, value in artikel_info.items():
    if value == []:
        aktuelles_leeres_objekt = key
        neues_json[aktuelles_leeres_objekt] = []
    elif aktuelles_leeres_objekt:
        neues_json[aktuelles_leeres_objekt].append({key: value})

output_json = json.dumps(neues_json, indent=4, ensure_ascii=False)

with open('website.json', 'w', encoding='utf-8') as file:
    file.write(output_json)

print("Done")
