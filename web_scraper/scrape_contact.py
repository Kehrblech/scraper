import json
from bs4 import BeautifulSoup
import requests
import scrape
import scrape_each_dyn
import search_contact
from urllib.parse import urljoin, urlparse

def contact_url(soup,org_url):
    if soup.head and soup.head.link and 'href' in soup.head.link.attrs:
        url = soup.head.link['href']
    parsed_url = urlparse(url)

    # extract url without subdomains
    scheme = parsed_url.scheme
    if (scheme != ""):
        domain = parsed_url.netloc.split('.')[-2] + '.' + parsed_url.netloc.split('.')[-1]
        base_url = f"{scheme}://{domain}"

    else:
        scheme = org_url
        base_url = f"{scheme}"
    print("Parsed URL:",scheme)
    print("Base URL:",base_url)
   
    keyword = "impressum|about us|contact|imprint|about"  
    element = soup.find(lambda tag: tag.name == "a" and any(kw in (tag.get("href") or tag.text.lower()) for kw in keyword.split("|")))
    if element:
        print("1")
        if element.get("href"):
            contact_form_url = element.get("href")
            if not contact_form_url.startswith("http"):  # check for https
                print("no http")
                contact_form_url = urljoin(base_url, contact_form_url)  # combine urls
                
            print("contact url found:", contact_form_url)
            return contact_form_url
        else:
            # search for url's
            contact_form_url = None
            if "onclick" in element.attrs:
                onclick_value = element.attrs["onclick"]
                print("url found in onclick:", onclick_value)
                return onclick_value

            elif element.text:
                print("url found in text:", element.text)
                return element.text
    else:
        for link in soup.find_all():
            if link.has_attr('href') and any(kw in (link['href'].lower()) for kw in keyword.split("|")):
                return link['href']
            if link.has_attr('href') and any(kw in (link.text.lower()) for kw in keyword.split("|")):
                return urljoin(base_url, link['href'])
            
        print("No contact information found.")
        
def contact_main(soup,org_url):
    url = contact_url(soup,org_url)
    if(url != None):
        return scrape_each_dyn.each(scrape.get_soup(url,org_url))
    else:
        return "Error no url found"

def contact_find(soup,org_url):
    if(contact_url(soup,org_url) != None):
        return search_contact.find(contact_url(soup,org_url))
    else:
        return "Error no url found"

