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


class Soup(Resource):

    def get(self):
        url  = request.args.get('url')
        if(url != None):
            return scrape.get_soup(url), 200
        else:
            return "Type in a url", 404

api.add_resource(Soup, "/soup/")

class Table(Resource):
    
    def get(self):
        url  = request.args.get('url')
        # """
        # Get all tables from a website
        # ---
        # tags:
        #   - Scrape Table content
        # summary: Parse a URL, get the Table content from a Website 
        # description: When passing a WebUrl address, the Table content can be retrieved. 
        # parameters:
        #   - name: url
        #     in: path
        #     required: true
        #     schema:
        #       type: string
        # responses:
        #   200:
        #     description: OK
        # """
        print(url)
        if(url != None):
            return scrape.all_tables(scrape.get_soup(url)), 200
        else:
            return "/table/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Table, "/table/")

class TOC(Resource):

    def get(self, url=None):
        # """
        # Get table of contents from a wiki site
        # ---
        # tags:
        #   - Scrape Table of Content from a Wiki site
        # summary: Parse a Wiki URL, get the Table of Content from a Wiki site. 
        # description: When passing a WebUrl address, that belongs to a Wiki site, the Table of Content can be retrieved. 
        # parameters:
        #   - name: url
        #     in: path
        #     required: true
        #     schema:
        #       type: string
        # responses:
        #   200:
        #     description: OK
        # """
        print(url)
        if(url != None):
            return scrape.table_of_contents_level_all_with_number(scrape.get_soup(url)), 200
        else:
            return "/toc/www.the-website-you-want-to-scrape.com", 404

api.add_resource(TOC, "/toc/<path:url>")

class Link(Resource):
    
    def get(self):
        url  = request.args.get('url')
        # """
        # Get all hyperlinks from a website
        # ---
        # tags:
        #   - Scrape Hyperlinks 
        # summary: Parse a URL, get get all hyperlinks from a Website
        # description: When passing a WebUrl address, all the hyperlinks are stored in a json file. 
        # parameters:
        #   - name: url
        #     in: path
        #     required: true
        #     schema:
        #       type: string
        # responses:
        #   200:
        #     description: OK
        # """
        print(url)
        if(url != None):
            return scrape.hyperlink(scrape.get_soup(url)), 200
        else:
            return "/link/?url=www.the-website-you-want-to-scrape.com", 404

api.add_resource(Link, "/link/")
#Try to scrape the contact forms of a given link
##-argument-
###none=(gives back all data)
###find=(trys to find phone and e-mail)
###text=(gives back text)
###url=(gives back url)
class Contact(Resource):

    def get(self,argument=None, url=None):
        # """
        # Get contact information from a website
        # ---
        # tags:
        #   - Scrape contact information
        # summary: Parse a URL, retrieve all Contact data from a Website
        # description: When passing a WebUrl address, the script trys to find all contanct information. There are diffrent Methods to Choose from. 
        # parameters:
        #   - in: path
        #     name: argument
        #     required: true
        #     schema:
        #       type: string
        #       enum: [find, text, url]
        #       example: find
        #   - in: path
        #     name: url
        #     required: true
        #     schema:
        #       type: string
        # responses:
        #   200:
        #     description: OK
        # """
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
        # """
        # Get contact information from multiple websites
        # ---
        # tags:
        #   - Scrape contact information
        # summary: Parse multiple URLs, retrieve contact data from each website
        # description: Pass a list of URLs in JSON format to scrape contact information from multiple websites.
        # requestBody:
        #     required: true
        #     content:
        #         application/json:
        #             schema:
        #                 type: object
        #                 properties:
        #                     keyword:
        #                         type: string
        #                         example: Bachelor
        #                     urls:
        #                         type: array
        #                         items:
        #                             type: string
        #                 example: 
        #                     keyword: Bachelor
        #                     urls: 
        #                         - "https://rwu.de"
        #                         - "https://www.uni-konstanz.de/"
        # responses:
        #   200:
        #     description: OK
        # """
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

api.add_resource(Contact, "/contact/", "/contact/<string:argument>/<path:url>")

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

    def get(self):
        type = request.args.get('type')
        url = request.args.get('url')

        print(url)
        if(url != None and type == "all" or type == None):
            return scrape_wiki_dyn.all_info(scrape.get_soup(url)), 200
        elif(url != None and type == "each"):
            return scrape_each_dyn.each(scrape.get_soup(url)), 200
        elif(url != None and type == "slide"):
            return scrape_each_dyn.each_slide(scrape.get_soup(url)), 200

        else:
            return "/auto/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Auto, "/auto/")

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
    def get(self, url=None,  analysis_type=None):
        
        num_results  = request.args.get('num_results')
        print(url)
        if(url != None and analysis_type== "ranking" and num_results  == None):
            return lda.topic_ranking(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url))),3), 200
        elif(url != None and analysis_type== "ranking" and num_results  != None):
            return lda.topic_ranking(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url))),num_results), 200
        elif(url != None and analysis_type== "luhn" and num_results  == None):
            return luhn.luhn_summarizer(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and analysis_type== "luhn" and num_results  != None):
            return luhn.luhn_summarizer_number(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url))),num_results), 200
        elif(url != None and analysis_type== "lsa" and num_results  == None):
            return lsa.lsa_summarzier(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and analysis_type== "lsa" and num_results  != None):
            return lsa.lsa_summarzier_number(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url))),num_results), 200
        elif(url != None and analysis_type== "lex" and num_results  == None):
            return lex_rank.bulletpoints(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url)))), 200
        elif(url != None and analysis_type== "lex" and num_results  != None):
            return lex_rank.bulletpoints_number(scrape.convert_output_to_string(scrape.all_text(scrape.get_soup(url))),num_results), 200
        else:
            return "/analysis/analysis_type/www.the-website-you-want-to-scrape.com  or /analysis/analysis_type/www.the-website-you-want-to-scrape.com?num_results=5", 404

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

api.add_resource(Analysis, "/analysis","/analysis/","/analysis/<string:analysis_type>/<path:url>")



if __name__ == '__main__':
    app.run(debug=True)
