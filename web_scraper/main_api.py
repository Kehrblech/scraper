from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
import scrape
import scrape_wiki_dyn
import scrape_contact
from ..summerizer import topic_models 

# #Table
# #toc
# #links
# #contact
# #headings
# #Image
# #Text 
# #Auto 
# #Presentation

### Wörter mit übergeben und danach liste von URLs auf filtern 
### Listen entgegen nehmen von urls 

app = Flask(__name__)

api = Api(app)
CORS(app)


class Soup(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.get_soup(url), 200
        else:
            return "Type in a url", 404

api.add_resource(Soup, "/soup/<path:url>")

class Table(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.all_tables(scrape.get_soup(url)), 200
        else:
            return "/table/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Table, "/table/<path:url>")

class TOC(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.table_of_contents_level_all_with_number(scrape.get_soup(url)), 200
        else:
            return "/toc/www.the-website-you-want-to-scrape.com", 404

api.add_resource(TOC, "/toc/<path:url>")

class Link(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.table_of_contents_level_all_with_number(scrape.get_soup(url)), 200
        else:
            return "/link/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Link, "/link/<path:url>")
#Try to scrape the contact forms of a given link
##-argument-
###none=(gives back all data)
###find=(trys to find phone and e-mail)
###text=(gives back text)
###url=(gives back url)
class Contact(Resource):

    def get(self,argument=None, url=None):
        try:
            if(url != None):
                if(argument != None):
                    if(argument == "find"):
                        return scrape_contact.contact_find(scrape.get_soup(url),url), 200
                    elif(argument == "text"):
                        return scrape_contact.contact_main(scrape.get_soup(url),url), 200
                    elif(argument == "url"):
                        return scrape_contact.contact_url(scrape.get_soup(url),url), 200
                    else:
                        return "Argument invalid try /contact/find/www.the-website-you-want-to-scrape.com. Use following arguments find | text | url", 404
                return scrape_contact.contact_main(scrape.get_soup(url),url), 200
            else:
                return "Missing URL! Try /contact/www.the-website-you-want-to-scrape.com", 404
        except Exception as e:
                return  "Error:" + str(e)
    def post(self):
        data = request.get_json()
        if data is None or not isinstance(data, list):
            return "Wrong Input! need a JSON format!", 400

        results = []
        for url in data:
            try:
                result = {
                    "url": url,
                    "contact": scrape_contact.contact_find(scrape.get_soup(url), url)
                }
                results.append(result)
            except Exception as e:
                results.append({"url": url, "error": str(e)})

        return results, 200

api.add_resource(Contact,"/contact/", "/contact/<path:url>", "/contact/<string:argument>/<path:url>")

class Heading(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.heading_h2_with_text_name_image_auto(scrape.get_soup(url)), 200
        else:
            return "/heading/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Heading, "/heading/<path:url>")

class Image(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.image_full_all(scrape.get_soup(url)), 200
        else:
            return "/image/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Image, "/image/<path:url>")

class Text(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.titles_with_text(scrape.get_soup(url)), 200
        else:
            return "/text/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Text, "/text/<path:url>")

class Auto(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape_wiki_dyn.all_info(scrape.get_soup(url)), 200
        else:
            return "/auto/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Auto, "/auto/<path:url>")

class Finds(Resource):

    def get(self, url=None, item=None, element=None):
        print(url)
        if(url != None and item != None and element == None):
            return scrape.find_text(scrape.get_soup(url),item), 200
        if(url != None and item != None and element == "metrics"):
            return scrape.find_text_metrics(scrape.get_soup(url),item), 200
        elif(url != None and item != None and element == "class"):
            return scrape.find_class(scrape.get_soup(url),item), 200
        elif(url != None and item != None and element == "id"):
            return scrape.find_id(scrape.get_soup(url),item), 200
        elif(url != None and item != None and element !=None):
            return scrape.find_element(scrape.get_soup(url),item,element), 200
        else:
            return "/find/the-item-you-want-to-scrape/www.the-website-you-want-to-scrape.com", 404

    def post(self):
        data = request.get_json()
        if data is None:
            return "Wrong Input. Need a JSON format!", 400
        keyword = data.get("keyword")
        urls = data.get("urls")

        results = []
        tmp_result = []
        for url in urls:
            try:
                tmp_result=scrape.find_text_metrics(scrape.get_soup(url), keyword)
                result = {
                    "url": url,
                    "metrics": tmp_result[0],
                    "data":tmp_result[1:]
                }
                results.append(result)
            except Exception as e:
                results.append({"url": url, "error": str(e)})

        return results, 200

api.add_resource(Finds, "/find","/find/","/find/<string:item>/<path:url>","/find/<string:item>/<string:element>/<path:url>")

class Analysis(Resource):

    def get(self, url=None, keyword=None):
        print(url)
        if(url != None and keyword != None):
            return topic_models.topics(scrape.concatenate_texts(scrape.analyse_keywords(scrape.get_soup(url),keyword)),3), 200
        
        else:
            return "/analysis/the-item-you-want-to-scrape/www.the-website-you-want-to-scrape.com", 404

    def post(self):
        data = request.get_json()
        if data is None:
            return "Wrong Input. Need a JSON format!", 400
        keyword = data.get("keyword")
        urls = data.get("urls")

        results = []
        tmp_result = []
        for url in urls:
            try:
                tmp_result=scrape.analyse_keywords(scrape.get_soup(url), keyword)
                result = {
                    "url": url,
                    "metrics": tmp_result[0],
                    "data":tmp_result[1:]
                }
                results.append(result)
            except Exception as e:
                results.append({"url": url, "error": str(e)})

        return results, 200

api.add_resource(Analysis, "/analysis","/analysis/","/analysis/<string:keyword>/<path:url>")



if __name__ == '__main__':
    app.run(debug=True)
