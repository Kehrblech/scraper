from flask import Flask, jsonify
from flask_restful import Api, Resource
import scrape
import scrape_wiki_dyn
import scrape_contact

# #soup
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
        print("contact"+url)
        if(url != None):
            if(argument != None):
                if(argument == "find"):
                    return scrape_contact.contact_find(scrape.get_soup(url)), 200
                elif(argument == "text"):
                    return scrape_contact.contact_main(scrape.get_soup(url)), 200
                elif(argument == "url"):
                    return scrape_contact.contact_url(scrape.get_soup(url)), 200
                else:
                    return "Argument invalid try /contact/find/www.the-website-you-want-to-scrape.com \n Use following arguments find | text | url", 404
            return scrape_contact.contact_main(scrape.get_soup(url)), 200
        else:
            return "Missing URL\nTry /contact/www.the-website-you-want-to-scrape.com", 404

api.add_resource(Contact, "/contact/<path:url>", "/contact/<string:argument>/<path:url>")

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

if __name__ == '__main__':
    app.run(debug=True)
