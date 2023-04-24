import requests
from bs4 import BeautifulSoup

# Die Suchanfrage, die Sie durchführen möchten
search_query = "Uhldingen Mühlhofen"

# Die URL-Adresse der Wikipedia-Suchergebnisseite
url = "https://de.wikipedia.org/w/index.php?search=" + search_query.replace(" ", "+")

# Abrufen der Suchergebnisseite mit requests
response = requests.get(url)
print(url)
# Überprüfen des HTTP-Statuscodes
if response.status_code >= 300 and response.status_code < 400:
    print("Weiterleitung erkannt."+response.status_code)
    # Hier können Sie entsprechende Logik für den Fall implementieren, dass Sie weitergeleitet wurden
elif response.status_code == 200:
    # Das HTML-Response mit BeautifulSoup analysieren
    soup = BeautifulSoup(response.content, "html.parser")
    # Finden des ersten Links auf der Seite, der auf einen Wikipedia-Artikel verweist
    search_results = soup.find("ul", {"class": "mw-search-results"})
    if search_results:
        first_result = search_results.find("a")
        if first_result:
            # Extrahieren der URL-Adresse des Wikipedia-Artikels aus dem gefundenen Link
            article_url = "https://de.wikipedia.org" + first_result["href"]
            print(article_url)
        else:
            print("Keine Ergebnisse gefunden.")
    else:
        print("Weitergeleitet - Passender Artikel gefunden.")
        articel_title = soup.find("span", {"class": "mw-page-title-main"})
        if articel_title:
            # Überprüfen, ob title nicht None ist, bevor .replace() darauf angewendet wird  
            print("https://de.wikipedia.org/wiki/" + articel_title.text.replace(" ", "_"))
        else:
            print("Keine Ergebnisse gefunden.")
else:
    print("Fehler beim Abrufen der Suchergebnisseite.")
