from flask import Flask, request, Response, jsonify, render_template
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import scrape
import scrape_wiki_dyn
import scrape_each_dyn
import scrape_contact
import find_url
from summarizer_algorithms import lda, luhn, lsa, lex_rank
from logging_modul import logger

import xmltojson
import json

from flasgger import Swagger

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

app = Flask(__name__) # do not change __name__

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger_flask.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "ScrAPI"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
 
api = Api(app)
CORS(app)
swagger = Swagger(app)

#Returns HTML Content
class Soup(Resource):

    def get(self):
        url  = request.args.get('url')
        clean = request.args.get('clean')
        logger.log_to_file(url)
        if(url != None and clean == None):
            html_response = scrape.get_soup(url)
            return html_response.prettify(),200
        elif(url != None and clean != None):
            html_response = scrape.get_soup(url)
            result=(' '.join(str(html_response.prettify()).strip().replace('\n', '').replace('\r', ' ').split()))
            return (result),200
        else:
            return "add key url and clean", 404

api.add_resource(Soup, "/soup/")

#Returns Tables if found
class Table(Resource):
    
    def get(self):
        url  = request.args.get('url')
        logger.log_to_file(url)
        if(url != None):
            return scrape.all_tables(scrape.get_soup(url)), 200
        else:
            return "/table?url=www.the-website-you-want-to-scrape.com", 404

api.add_resource(Table, "/table/")

#Return Table of Content from Wiki Sites (Currently just German.wikis)
class TOC(Resource):

    def get(self):
        url  = request.args.get('url')
        logger.log_to_file(url)
        if(url != None):
            return scrape.table_of_contents_level_all_with_number(scrape.get_soup(url)), 200
        else:
            return "/toc?url=www.the-website-you-want-to-scrape.com", 404

api.add_resource(TOC, "/toc/")

#Returns Hyperlinks from Websites, you can even Filter
## or if Hyperlinks Contains keywords like "www" or "html" you can send string with "|" as separator 
### like so ".de|.com" Stichwort Google Font Abmahnung ;) 
class Link(Resource):
    
    def get(self):
        url  = request.args.get('url')
        filter  = request.args.get('filter')
        contains = request.args.get('contains')
        logger.log_to_file(url)
        
        if(url != None and filter != None):
            return scrape.hyperlink_filter(scrape.get_soup(url)), 200
        elif(url != None and contains != None):
            return scrape.hyperlink_contains(scrape.get_soup(url),contains), 200
        elif(url != None):
            return scrape.hyperlink(scrape.get_soup(url)), 200
        else:
            return "/link/?url=www.the-website-you-want-to-scrape.com", 404

api.add_resource(Link, "/link/")

#Try to scrape the contact forms of a given link
##returns json structure with url phone and mail address of given web-address
class Contact(Resource):

    def get(self):
        url  = request.args.get('url')
        logger.log_to_file(url)
        try:
            if(url != None):
                return scrape_contact.contact_find(scrape.get_soup(url),url), 200
            else:
                return "Missing URL! Try /contact?url=www.the-website-you-want-to-scrape.com", 404
        except Exception as e:
                return  "Error:" + str(e)
    def post(self):
        # example: 
        #       [
        #        "https://rwu.de",
        #        "https://www.uni-heidelberg.de/de",
        #        "https://www.uni-konstanz.de/"
        #        ]
        
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

api.add_resource(Contact, "/contact/")


#WIKI ONLY
class Image(Resource):

    def get(self):
        url  = request.args.get('url')
        logger.log_to_file(url)
        if(url != None):
            return scrape.image_full_all(scrape.get_soup(url)), 200
        else:
            return "/image?url=www.the-website-you-want-to-scrape.com", 404

api.add_resource(Image, "/image/")

#Returns Text
## Can return Text cleaned from annoying \n etc.
class Text(Resource):

    def get(self):
        url  = request.args.get('url')
        clean  = request.args.get('clean')
        logger.log_to_file(url)
        if(url != None and clean != None):
            text = scrape.get_soup(url).get_text()
            clean_text = text.replace("\n", "").replace("\t", "").replace("\r", "")
            return clean_text, 200
        elif(url != None and clean == None):
            return scrape.get_soup(url).get_text(), 200
        else:
            return "/text?url=www.the-website-you-want-to-scrape.com  use clean key true for removing annoying \\n", 404

api.add_resource(Text, "/text/")

#WIKI ONLY
class Auto(Resource):

    def get(self):
        type = request.args.get('type')
        url = request.args.get('url')

        logger.log_to_file(url)
        if(url != None and type == "all" or type == None):
            return scrape_wiki_dyn.all_info(scrape.get_soup(url)), 200
        elif(url != None and type == "each"):
            return scrape_each_dyn.each(scrape.get_soup(url)), 200
        elif(url != None and type == "slide"):
            return scrape_each_dyn.each_slide(scrape.get_soup(url)), 200

        else:
            return "/auto/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Auto, "/auto/")

#searches for a Keyword on the website
# returns Text in which keyword was found
# you even can display metrics 
class Keyword(Resource):

    def get(self):
        url = request.args.get('url')
        keyword = request.args.get('keyword')
        metrics = request.args.get('metrics')
        logger.log_to_file(url)
        if(url != None and keyword != None and metrics == None):
            return scrape.find_text(scrape.get_soup(url),keyword), 200
        elif(url != None and keyword != None and metrics != 'false'):
            return scrape.find_text_metrics(scrape.get_soup(url),keyword), 200
        elif(url != None and keyword != None and metrics == 'false'):
            return scrape.find_text(scrape.get_soup(url),keyword), 200
        else:
            return "/keyword?url=www.the-website-you-want-to-scrape.com&keyword=Studium&metrics=true", 404

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

api.add_resource(Keyword, "/keyword/")


#  elif(url != None and item != None and element == "class"):
#             return scrape.find_class(scrape.get_soup(url),item), 200
#         elif(url != None and item != None and element == "id"):
#             return scrape.find_id(scrape.get_soup(url),item), 200
#         elif(url != None and item != None and element !=None):
#             return scrape.find_element(scrape.get_soup(url),item,element), 200


# EXPERIMENTAL
class Summarizer(Resource):

    def get(self):
        type  = request.args.get('type')
        text  = request.args.get('text')
        num = request.args.get('num')

        print(text,type,num)
        if(text != None): 
            return lex_rank.bulletpoints_number(text,num) , 200
        else:
            return "/summarizer/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Summarizer, "/summarizer/")

#WIKI ONLY
class FindURL(Resource):

    def get(self):
        text  = request.args.get('text')

        print(text)
        if(text != None): 
            return find_url.wiki_search(text) , 200
        else:
            return "/findurl/ is a service for scrape and search php index", 404

api.add_resource(FindURL, "/findurl/")

class Analysis(Resource):
    #luhn.luhn_summarizer(scrape.concatenate_texts(scrape.analyse_keywords(scrape.get_soup(url),keyword)),3), 200
    def get(self):
        url  = request.args.get('url')
        algorithm  = request.args.get('algorithm')
        results  = request.args.get('results')
        logger.log_to_file(url)
        if(url != None and algorithm== "lda" and results  == None):
            return lda.topic_ranking((scrape.all_text(scrape.get_soup(url))),3), 200
        elif(url != None and algorithm== "lda" and results  != None):
            return lda.topic_ranking((scrape.all_text(scrape.get_soup(url))),results), 200
        elif(url != None and algorithm== "luhn" and results  == None):
            return luhn.luhn_summarizer((scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and algorithm== "luhn" and results  != None):
            return luhn.luhn_summarizer_number((scrape.all_text(scrape.get_soup(url))),results), 200
        elif(url != None and algorithm== "lsa" and results  == None):
            return lsa.lsa_summarzier((scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and algorithm== "lsa" and results  != None):
            return lsa.lsa_summarzier_number((scrape.all_text(scrape.get_soup(url))),results), 200
        elif(url != None and algorithm== "lex" and results  == None):
            return lex_rank.bulletpoints((scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and algorithm== "lex" and results  != None):
            return lex_rank.bulletpoints_number((scrape.all_text(scrape.get_soup(url))),results), 200
        else:
            return "/analysis/analysis_type/www.the-website-you-want-to-scrape.com  or /analysis/analysis_type/www.the-website-you-want-to-scrape.com?num_results=5", 404

    def post(self):
        data = request.get_json()
        if data is None:
            return "Wrong Input. Need a JSON format!", 400
        algorithm = data.get("algorithm")
        urls = data.get("urls")

        results = []
        tmp_result = []
        for url in urls:
            try:
                if algorithm == "lda":
                    tmp_result=lda.topic_ranking((scrape.all_text(scrape.get_soup(url))),3)
                elif algorithm == "luhn":
                    tmp_result=luhn.luhn_summarizer((scrape.all_text(scrape.get_soup(url))))
                elif algorithm == "lsa":
                    tmp_result=lsa.lsa_summarzier((scrape.all_text(scrape.get_soup(url))))
                elif algorithm == "lex":
                    tmp_result=lex_rank.bulletpoints((scrape.all_text(scrape.get_soup(url))))
                else:
                    return "Wrong Json Input, Maybe Wrong algorithm?", 404
                result = {
                    "url": url,
                    "topics": tmp_result,
                    }
                results.append(result)
            except Exception as e:
                results.append({"url": url, "error": str(e)})

        return results, 200

api.add_resource(Analysis, "/analysis/")



if __name__ == '__main__':
    app.run(debug=True)
