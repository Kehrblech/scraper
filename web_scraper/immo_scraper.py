import requests
from bs4 import BeautifulSoup

url = "https://www.immobilienscout24.de/Suche/radius/haus-kaufen?centerofsearchaddress=Uhldingen-M%C3%BChlhofen;88690;;;;&geocoordinates=47.73202;9.24692;5.0&enteredFrom=result_list"

response = requests.get(url)
html_code = response.text

soup = BeautifulSoup(html_code, 'html.parser')

print(soup)

result_div = soup.find('div', class_='result-list-entry__data')
if result_div:

    title = result_div.find('h4').get_text(strip=True)
    address = result_div.find('div', class_='result-list-entry__address').get_text(strip=True)
    kaufpreis = result_div.find('dd', class_='font-highlight', text='Kaufpreis').find_previous('dd').get_text(strip=True)
    wohnflaeche = result_div.find('dd', class_='font-highlight', text='Wohnfläche').find_previous('dd').get_text(strip=True)
    zimmer = result_div.find('dd', class_='font-highlight', text='Zi.').find_previous('dd').get_text(strip=True)
    grundstueck = result_div.find('dd', class_='font-highlight', text='Grundstück').find_previous('dd').get_text(strip=True)


    print('Title:', title)
    print('Address:', address)
    print('Kaufpreis:', kaufpreis)
    print('Wohnfläche:', wohnflaeche)
    print('Zimmer:', zimmer)
    print('Grundstück:', grundstueck)