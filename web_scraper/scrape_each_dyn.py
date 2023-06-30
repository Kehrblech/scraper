import json
import re
from summarizer_algorithms import lda, luhn, lsa, lex_rank
excluded_urls = [
    "//upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Disambig-dark.svg/25px-Disambig-dark.svg.png",
    "/static/images/footer/wikimedia-button.png",
    "/w/extensions/ImageMap/resources/desc-20.png?15600",
    "//upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Reddot.svg/5px-Reddot.svg.png",
    "//upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Qsicon_Quelle.svg/24px-Qsicon_Quelle.svg.png",
    "//upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Red_pog.svg/8px-Red_pog.svg.png",
    "//upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Loudspeaker.svg/12px-Loudspeaker.svg.png",
    "//upload.wikimedia.org/wikipedia/commons/thumb/e/ef/RedMountain.svg/12px-RedMountain.svg.png",
    "//upload.wikimedia.org/wikipedia/commons/thumb/f/f4/OOjs_UI_icon_play-ltr-progressive.svg/10px-OOjs_UI_icon_play-ltr-progressive.svg.png"
]


def each(soup):
    artikel_info = {}

    # Überschriften (h1, h2, h3) extrahieren
    ueberschrift = None
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
        if element.name in ['h1', 'h2', 'h3']:
            ueberschrift = element.text.strip()
            ueberschrift = ueberschrift.replace(
                "[Bearbeiten | Quelltext bearbeiten]", "")
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


def each_slide(soup):
    artikel_info = {}

    # Überschriften (h1, h2, h3) extrahieren
    ueberschrift = None
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img']):
        if element.name in ['h1', 'h2', 'h3']:
            ueberschrift = element.text.strip()
            ueberschrift = ueberschrift.replace(
                "[Bearbeiten | Quelltext bearbeiten]", "")
            print("Done")
            artikel_info[ueberschrift] = []
        elif element.name == 'p' and ueberschrift:
            text = element.text.strip()
            # Entfernen der eckigen Klammern
            text = re.sub(r'\[[^\]]*\]', '', text)
            artikel_info[ueberschrift].append({"text": text})
        elif element.name == 'img' and ueberschrift:
            bild_url = element['src']
            if bild_url not in excluded_urls:
                artikel_info[ueberschrift].append({"image": bild_url})
        else:
            # Extrahieren von Text zwischen den Überschriften
            if ueberschrift:
                text = element.text.strip()
                if text:
                    # Entfernen der eckigen Klammern
                    text = re.sub(r'\[[^\]]*\]', '', text)
                    artikel_info[ueberschrift].append({"text": text})

    new_artikel = {}
    new_artikel["slides"] = []

    for topic, data in artikel_info.items():
        topic_data = {}
        topic_data["name"] = topic
        topic_data["images"] = []
        topic_data["text"] = ""

        for item in data:
            if isinstance(item, dict) and "image" in item:
                image_url = item["image"]
                image_data = {"url": image_url}
                topic_data["images"].append(image_data)
            elif isinstance(item, dict) and "text" in item:
                text = item["text"]
                bullet_points = lex_rank.bulletpoints_string(text)
                print(text)
                topic_data["text"] = bullet_points

        new_artikel["slides"].append(topic_data)

    new_json_str = json.dumps(new_artikel)

    with open('website.json', 'w', encoding='utf-8') as file:
        json.dump(new_artikel, file, indent=4, ensure_ascii=False)

    return new_artikel
