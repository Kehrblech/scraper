import yaml
import json

with open('web_scraper/yaml_to_json/swagger_flask.yml', 'r', encoding='utf-8') as yaml_file:
    yaml_data = yaml.safe_load(yaml_file)

with open('web_scraper/yaml_to_json/swagger_flask.json', 'w', encoding='utf-8') as json_file:
    json.dump(yaml_data, json_file, indent=4, ensure_ascii=False)
