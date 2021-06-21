from .config import es_config, strapi_config
import requests
import json


class Strapi:
    def __init__(self):
        self.hosts = strapi_config.hosts
    
    def get_db(self,collection: str = strapi_config.collection):
        response = requests.get(self.hosts + collection,
                      headers={
                        'Content-Type': 'application/json'
                      })
        data = json.loads(response.text)
        return data 