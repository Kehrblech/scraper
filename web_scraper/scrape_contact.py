import json
from bs4 import BeautifulSoup
import requests
import scrape
import scrape_each_dyn
import search_contact
from urllib.parse import urljoin, urlparse

# URL des Wikipedia-Artikels
url = "https://holzhandel-deutschland.de/"

# Verbindung herstellen und HTML-Code abrufen

response = requests.get(url)
html_code = response.text

# HTML mit BeautifulSoup analysieren
soup = BeautifulSoup(html_code, 'html.parser')

def contact_url(soup):
    if soup.head and soup.head.link and 'href' in soup.head.link.attrs:
        url = soup.head.link['href']
    parsed_url = urlparse(url)

    # Extract the scheme and domain from the parsed URL
    scheme = parsed_url.scheme
    domain = parsed_url.netloc.split('.')[-2] + '.' + parsed_url.netloc.split('.')[-1]
    base_url = f"{scheme}://{domain}"
    print("Base_URL:",base_url)
    # if soup.head and soup.head.link and 'href' in soup.head.link.attrs:
    #     url = soup.head.link['href']
    # parsed_url = urlparse(url)
    # print(parsed_url)

    # # Extrahieren Sie das Schema und die Netzwerklokation aus der analysierten URL
    # scheme = parsed_url.scheme
    # netloc = parsed_url.netloc

    # # Kombinieren Sie das Schema und die Netzwerklokation, um die Standard-Domain zu erhalten
    # base_url = f"{scheme}://{netloc}"

    # print("Standard-Domain:", base_url)
   
    keyword = "impressum|about us|contact|imprint"  
    element = soup.find(lambda tag: tag.name == "a" and any(kw in (tag.get("href") or tag.text.lower()) for kw in keyword.split("|")))
    if element:
        if element.get("href"):
            contact_form_url = element.get("href")
            if not contact_form_url.startswith("http"):  # Überprüfen, ob die URL kein Protokoll enthält
                print("no http")
                contact_form_url = urljoin(base_url, contact_form_url)  # Kombinieren der URLs
                
            print("Kontaktformular-URL gefunden:", contact_form_url)
            return contact_form_url
        else:
            # Suchen nach URLs in anderen Attributen oder im Textinhalt des Elements
            contact_form_url = None
            if "onclick" in element.attrs:
                onclick_value = element.attrs["onclick"]
                # Hier können Sie z.B. reguläre Ausdrücke verwenden, um die URL aus dem onclick-Wert zu extrahieren
                # Beispiel: contact_form_url = re.search(r"'(.*?)'", onclick_value).group(1)
                print("URL im onclick-Attribut gefunden:", onclick_value)
                return onclick_value

            elif element.text:
                # Hier können Sie z.B. reguläre Ausdrücke verwenden, um die URL aus dem Textinhalt des Elements zu extrahieren
                print("URL im Textinhalt gefunden:", element.text)
                return element.text
    else:
        print("Kein Kontaktformular gefunden.")
        
def contact_main(soup):
    url = contact_url(soup)
    if(url != None):
        return scrape_each_dyn.each(scrape.get_soup(url))
    else:
        return "Error no url found"

def contact_find(soup):
    if(contact_url(soup) != None):
        return search_contact.search(contact_url(soup))
    else:
        return "Error no url found"


