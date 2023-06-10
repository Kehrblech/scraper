import requests
from bs4 import BeautifulSoup


url = 'https://www.immobilienscout24.de/Suche/radius/haus-kaufen?centerofsearchaddress=Uhldingen-M%C3%BChlhofen;88690;;;;&geocoordinates=47.73202;9.24692;5.0&enteredFrom=result_list'

# Create a header file so we can trick the website to think we are a genuin browser 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
}

# include the header with our get request
response = requests.get(url, headers=headers)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
else:
    print('Error', response.status_code)