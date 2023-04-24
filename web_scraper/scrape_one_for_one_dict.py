import json
import scrape

url = "https://www.searchmetrics.com/de/glossar/website/"
soup = scrape.get_soup(url)

# find headings
headings = []
for heading in soup.find_all(['h1', 'h2', 'h3']):
    heading_text = heading.text.strip()
    headings.append(heading_text)

# table of content (toc, vector-toc) extract NEED TO add vector toc for 
inhaltsverzeichnis = []
toc_div = soup.find('div', {'id': 'toc'})
if toc_div:
    for toc_item in toc_div.find_all(['li']):
        toc = toc_item.text.strip()
        inhaltsverzeichnis.append(toc)
# <p>
texte = []
for paragraph in soup.find_all('p'):
    text = paragraph.text.strip()
    texte.append(text)

# <img>
bilder = []
for image in soup.find_all('img'):
    bild_url = image['src']
    bilder.append(bild_url)

# dict
data = {
    'heading': heading_text,
    'table_of_content': inhaltsverzeichnis,
    'text': texte,
    'image': bilder
}

with open('website.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Done")
