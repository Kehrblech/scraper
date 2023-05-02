import re
from bs4 import BeautifulSoup
import scrape

def search(url):
    soup = scrape.get_soup(url)
    # Suchen nach Telefonnummern, E-Mail-Adressen und Adressen
    telefon_regex = re.compile(r'((\+\d{1,2})|0)?[\d\s.-]{10,13}')
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    telefonnummern = []
    emails = []

    for element in soup.find_all():
        # Telefonnummern extrahieren
        if element.text:
            telefon_match = telefon_regex.search(element.text)
            if telefon_match:
                telefonnummer = telefon_match.group().strip()
                # Telefonnummer im gewünschten Format formatieren
                telefonnummer = telefonnummer.replace(' ', '').replace('-', '').replace('.', '').replace('/', '').replace('(', '').replace(')', '').replace('O', '0').replace('o', '0').replace('|', '1').replace('l', '1')
                if len(telefonnummer) > 5:
                    if telefonnummer not in telefonnummern:
                        telefonnummern.append(telefonnummer)
                    
                        
       
        # E-Mail-Adressen extrahieren
        if element.has_attr('href'):
            email_match = email_regex.search(element['href'])
            if email_match:
                emails.append(email_match.group())

    # Ergebnisse ausgeben
    contact_dict = {
        "url": url,
        "phone": telefonnummern,
        "mail": emails
    }
    print("phone:", telefonnummern)
    print("mail:", emails)
    return contact_dict