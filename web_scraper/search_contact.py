import re
from bs4 import BeautifulSoup
import scrape


def search(url):
    soup = scrape.get_soup(url)
    telefon_regex = re.compile(r'((\+\d{1,2})|0)?[\d\s.-]{10,13}')
    email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
    phonenumbers = []
    emails = []

    for element in soup.find_all():
        if element.text:
            telefon_match = telefon_regex.search(element.text)
            if telefon_match:
                phonenumber = telefon_match.group().strip()
                phonenumber = phonenumber.replace(' ', '').replace('-', '').replace('.', '').replace('/', '').replace('(', '').replace(')', '').replace('O', '0').replace('o', '0').replace('|', '1').replace('l', '1')
                if len(phonenumber) > 7:
                    if phonenumber not in phonenumbers:
                        phonenumbers.append(phonenumber)
    contact_dict = {
        "url": url,
        "phone": phonenumbers,
        "mail": emails
    }
    print("phone:", phonenumbers)
    print("mail:", emails)
    return contact_dict
                    
                        
def find(url): 
     
    phonenumbers = []
    emails = [] 
    # E-Mail-Adressen extrahieren
    soup = scrape.get_soup(url)
    for element in soup.find_all():
        find_phone(element,phonenumbers)
        find_mail(element,emails)
             
            
    contact_dict = {
        "url": url,
        "phone": phonenumbers,
        "mail": emails
    }
    print("phone:", phonenumbers)
    print("mail:", emails)
    return contact_dict

    
def find_mail(element,emails):
    mail_keyword = "mailto|mail|email|e-mail|mail-to"       
    if  element.has_attr('href') and element['href'].startswith('mailto:'):
        if "@" in element.text: 
            emails.append(element.text)   
            
    if element.has_attr('class') and 'mail' in element['class']:
        if "@" in element.text: 
            emails.append(element.text)
    # Control if Email list is empty and try a scraper method
    if len(emails) < 1:
        if element.text and any(kw in (element.text.lower()) for kw in mail_keyword.split("|")):  
            email_regex = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
            match = email_regex.search(element.text)
            if match:
                email = match.group()
                emails.append(email)
            else:
                print("No email found")
            
            

def find_phone(element,phonenumbers):
    phone_keyword = "tel:|phone:|call:|telephone:|tel:|mobil:|mobile:|telefon:|+1|+49|+41|fon:|telephone"   
    phone_regex = re.compile(r'''(
    (\+\d{1,3}[\s.-]*)?     # optional cc 
    (\(?\d{1,3}\)?[\s.-]*)? # optional ac
    (\d{3}[\s.-]*)          # 3 digs
    (\d{2,4}[\s.-]*)        # 2-4 digs
    (\d{0,2})?              # ending
    )''', re.VERBOSE)

    if element.has_attr('href') and element['href'].startswith('callto:') or element.has_attr('href') and element['href'].startswith('tel:'):
            phonenumbers.append(element.text) 
    if element.has_attr('class'):
        if any(kw in (element['class'] or element.text.lower()) for kw in phone_keyword.split("|")): 
            phonenumbers.append(element.text)    
              
        if element.has_attr('class') and element.has_attr('href'):
            if any(kw in (element['class'] or element.text.lower() or element['href'] ) for kw in phone_keyword.split("|")): 
                phonenumbers.append(element.text)   
    if len(phonenumbers) < 1:       
        if element.text and any(kw in (element.text.lower()) for kw in phone_keyword.split("|")): 
            if len(element.text) < 305:     
                phone_match = phone_regex.search(element.text)
                if phone_match:
                    phone_number = phone_match.group(0)
                    phonenumbers.append(phone_number)   
            
    

  