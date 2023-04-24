from flask import Flask, jsonify
from flask_restful import Api, Resource
import scrape
import scrape_wiki_dyn


app = Flask(__name__)
api = Api(app)

class Table(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.table_of_contents_level_all_with_number(scrape.get_soup(url)), 200
        else:
            return "Type in a url", 404

api.add_resource(Table, "/table/<path:url>")

class Text(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape.titles_with_text(scrape.get_soup(url)), 200
        else:
            return "Type in a url", 404

api.add_resource(Text, "/text/<path:url>")

class Auto(Resource):

    def get(self, url=None):
        print(url)
        if(url != None):
            return scrape_wiki_dyn.all_info(scrape.get_soup(url)), 200
        else:
            return "Type in a url", 404

api.add_resource(Auto, "/auto/<path:url>")

if __name__ == '__main__':
    app.run(debug=True)
