import json
import scrape

url = "https://www.searchmetrics.com/de/glossar/website/"
soup = scrape.get_soup(url)

# Find all Headings
data = []
for heading in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
    heading_text = heading.get_text().strip()
    caption_text = None
    paragraphs = []
    word_count = 0

    # Find following siblings like paragraps 
    siblings = heading.find_next_siblings()
    for sibling in siblings:
        if sibling.name and sibling.name.startswith("h"):
            # end if next sibling start with <h*> // we are at a new heading
            break
        if sibling.name == "figcaption":
            caption_text = sibling.get_text().strip()
        elif sibling.name == "p":
            paragraph_text = sibling.get_text().strip()
            paragraphs.append(paragraph_text)
            # Count words in paragraph and add it up 
            word_count += len(paragraph_text.split())

    # Save data in dict
    heading_data = {
        "heading": heading_text,
        "caption": caption_text,
        "paragraph": paragraphs,
        "number_paragraphs": len(paragraphs),
        "word_total": word_count
    }
    data.append(heading_data)

with open("webseite.json", "w", encoding="utf-8") as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)
print("done")