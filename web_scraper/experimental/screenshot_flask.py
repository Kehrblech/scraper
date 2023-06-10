from selenium import webdriver
from PIL import Image
import io
from flask import Flask, Response, stream_with_context

app = Flask(__name__)

@app.route('/get_screenshot', methods=['GET'])
def get_screenshot():
    driver = webdriver.Chrome() 

    driver.get('https://www.pcwelt.de/article/1361235/diese-webseiten-sollte-wirklich-jeder-kennen.html')  

    driver.implicitly_wait(10)  

    accept_button = None
    try:
        accept_button = driver.find_element_by_xpath('//*[@id[contains(@id, "accept") or contains(@class, "accept")]]' )

        print("found button")
    except:
        pass


    if accept_button is not None:
        accept_button.click()


    screenshot = driver.get_screenshot_as_png()  
    image = Image.open(io.BytesIO(screenshot))  
    print(image,"image")

 
    driver.quit()

    # Image as stream 
    response = Response(stream_with_context(image.stream), content_type='image/png')

    # set response header
    response.headers['Content-Disposition'] = 'attachment; filename=screenshot.png'

    if hasattr(image, 'stream'):
        response = Response(stream_with_context(image.stream), content_type='image/png')
        return response
    else:
        return 'Error: No stream of the image', 500

if __name__ == '__main__':
    app.run(debug=True)
