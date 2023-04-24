import json
import scrape



def all_info(soup):


    # Dict
    artikel_info = {}
    count = 0 
    # get heading
    ueberschrift_h1 = None
    ueberschrift_h2 = None
    ueberschrift_h3 = None
    liste_p = []
    check_first = False
    h1_1 = soup.find('h1')
    filtered_p_elements = []
    for element in soup.find_all(['h1', 'h2', 'h3', 'p', 'img', 'ul' ]):
        
        if element.name == 'h1':
            ueberschrift_h1 = element.text.strip()
            try:
                ueberschrift_h1 = ueberschrift_h1.replace("[Bearbeiten | Quelltext bearbeiten]", "")
            except ValueError:
                pass    
                
            artikel_info[ueberschrift_h1] = {}
            ueberschrift_h2 = None
            ueberschrift_h3 = None
        
        elif element.name == 'h2':
            ueberschrift_h2 = element.text.strip()
            try:
                ueberschrift_h2 = ueberschrift_h2.replace("[Bearbeiten | Quelltext bearbeiten]", "")
            except ValueError:
                pass 
            if ueberschrift_h1:
                artikel_info[ueberschrift_h1][ueberschrift_h2] = {}
            ueberschrift_h3 = None
        elif element.name == 'h3' and ueberschrift_h1 and ueberschrift_h2:
            ueberschrift_h3 = element.text.strip()
            try:
                ueberschrift_h3 = ueberschrift_h3.replace("[Bearbeiten | Quelltext bearbeiten]", "")
            except ValueError:
                pass 
            if ueberschrift_h1 and ueberschrift_h2:
                artikel_info[ueberschrift_h1][ueberschrift_h2][ueberschrift_h3] = []
        elif element.name == 'p' and ueberschrift_h1 and ueberschrift_h2 and ueberschrift_h3:
            text = element.text.strip()
            try:
                artikel_info[ueberschrift_h1][ueberschrift_h2][ueberschrift_h3].append(text)
            except KeyError:
                print("Error:p")
                pass
        elif element.name == 'img' and ueberschrift_h1 and ueberschrift_h2 and ueberschrift_h3:
            bild_url = element['src']
            try:
                artikel_info[ueberschrift_h1][ueberschrift_h2][ueberschrift_h3].append(bild_url)
            except KeyError:
                print("Error:img")
                pass
        elif element.name == 'ul' and ueberschrift_h1 and ueberschrift_h2 and ueberschrift_h3:
            liste = []
            for li in element.find_all('li'):
                liste.append(li.text.strip())
            try:
                artikel_info[ueberschrift_h1][ueberschrift_h2][ueberschrift_h3].append(liste)
            except KeyError:
                print("Error:ul")
                pass
        # elif element.name == 'p'and not any(element.find_parents(attrs={'class': 'geo noexcerpt'})) and not any(element.find_parents(attrs={'id': 'coordinates'})):
        #     next_element = element.find_next_sibling()
        #     if next_element and (next_element.name == 'div' or next_element.name == 'h2'):
        #         filtered_p_elements.append(element.text.strip())
        #         break
        #     elif next_element and (next_element.name == 'p'):
        #         filtered_p_elements.append(element.text.strip())
        #     else:
        #         pass
            
    # Print the text contents of the filtered <p> elements
    for p in filtered_p_elements:
        print(p)
            

    # Inhaltsverzeichnis (toc, vector-toc) extrahieren
    toc_div = soup.find('div', {'id': 'toc'})
    if toc_div:
        inhaltsverzeichnis = []
        for toc_item in toc_div.find_all(['li']):
            toc = toc_item.text.strip()
            inhaltsverzeichnis.append(toc)
        artikel_info["Inhaltsverzeichnis"] = inhaltsverzeichnis

    # Extrahierte Informationen in ein JSON-Objekt schreiben
    with open('wikipedia_artikel.json', 'w', encoding='utf-8') as file:
        json.dump(artikel_info, file, indent=4, ensure_ascii=False)
    return(artikel_info)
    print("Done")
    

