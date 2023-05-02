import json

def each(soup):
    artikel_info = {}

    # Überschriften (h1, h2, h3) extrahieren
    ueberschrift = None
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
        if element.name in ['h1', 'h2', 'h3']:
            ueberschrift = element.text.strip()
            ueberschrift = ueberschrift.replace("[Bearbeiten | Quelltext bearbeiten]", "")
            print("Done")
            artikel_info[ueberschrift] = []
        elif element.name == 'p' and ueberschrift:
            text = element.text.strip()
            artikel_info[ueberschrift].append(text)
        elif element.name == 'img' and ueberschrift:
            bild_url = element['src']
            artikel_info[ueberschrift].append(bild_url)
        else:
        # Extrahieren von Text zwischen den Überschriften
            if ueberschrift:
                text = element.text.strip()
                if text:
                    artikel_info[ueberschrift].append(text)

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
    return (artikel_info)
    
