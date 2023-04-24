
from selenium import webdriver

driver = webdriver.Chrome()  

driver.get('https://www.pcwelt.de/article/1361235/diese-webseiten-sollte-wirklich-jeder-kennen.html') 

driver.implicitly_wait(10)

# find button
accept_button = None
try:
    accept_button = driver.find_element_by_xpath('//*[@id[contains(@id, "accept")] or contains(@class, "accept")]' )
  
except:
    pass

# click
if accept_button is not None:
    accept_button.click()


driver.save_screenshot('screenshot.jpg')  # Speichere den Screenshot in einer Datei

driver.quit()
