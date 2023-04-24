
from selenium import webdriver

# Erstelle eine Instanz des Chrome WebDriver
driver = webdriver.Chrome()  # Du musst den Chrome WebDriver installiert haben

# Navigiere zur Website
driver.get('https://www.pcwelt.de/article/1361235/diese-webseiten-sollte-wirklich-jeder-kennen.html')  # Ersetze 'https://deine-website.de' mit der URL deiner eigenen Website

# Warte bis die Seite geladen ist
driver.implicitly_wait(10)  # Warte max. 10 Sekunden, bis die Seite geladen ist

# Finde das Button-Element mit ID oder Klasse, das den Begriff "accept" enthält
accept_button = None
try:
    accept_button = driver.find_element_by_xpath('//*[@id[contains(@id, "accept")] or contains(@class, "accept")]' )
    # Hier wird nach einem Element gesucht, dessen ID den Begriff "accept" enthält oder dessen Klasse den Begriff "accept" enthält
    # Du kannst das XPath-Muster entsprechend anpassen, um deinen Bedürfnissen gerecht zu werden
except:
    pass

# Klicke auf den Button, falls gefunden
if accept_button is not None:
    accept_button.click()

# Erfasse einen Screenshot
driver.save_screenshot('screenshot.jpg')  # Speichere den Screenshot in einer Datei

# Schließe den WebDriver
driver.quit()
