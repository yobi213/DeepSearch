import os

class es_config:
    hosts = os.getenv('ES_HOSTS')
    auth = os.getenv('ES_AUTH')


class strapi_config:
    hosts = os.getenv('STRAPI_HOSTS')
    collection = 'crawler-keywords'
