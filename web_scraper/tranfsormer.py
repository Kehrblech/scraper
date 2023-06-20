import yaml
import json

with open('web_scraper/swagger_flask.yml', 'r') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

with open('web_scraper/swagger_flask.json', 'w') as json_file:
    json.dump(yaml_data, json_file, indent=4)