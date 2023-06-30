import requests
from bs4 import BeautifulSoup


def wiki_search(search_query):
    

    url = "https://de.wikipedia.org/w/index.php?search=" + search_query.replace(" ", "+")

    response = requests.get(url)
    print(url)
    # Check Status codfe
    if response.status_code >= 300 and response.status_code < 400:
        print("Weiterleitung erkannt."+response.status_code)
    # Redirectement
    elif response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
    # Find first link referenced
        search_results = soup.find("ul", {"class": "mw-search-results"})
        if search_results:
            first_result = search_results.find("a")
            if first_result:
                article_url = "https://de.wikipedia.org" + first_result["href"]
                print(article_url)
                return article_url
            else:
                print("Keine Ergebnisse gefunden.")
                return 0
        else:
            print("Weitergeleitet - Passender Artikel gefunden.")
            articel_title = soup.find("span", {"class": "mw-page-title-main"})
            if articel_title:
                print("https://de.wikipedia.org/wiki/" + articel_title.text.replace(" ", "_"))
                return "https://de.wikipedia.org/wiki/" + articel_title.text.replace(" ", "_")
            else:
                print("Keine Ergebnisse gefunden.")
                return 0 
    else:
        print("Fehler beim Abrufen der Suchergebnisseite.")
        return 1
