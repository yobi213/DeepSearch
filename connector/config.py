import os

class es_config:
#     hosts = 'https://search-deepsearch-bztxmrzp24xb4ms6tddde7vypm.ap-northeast-2.es.amazonaws.com'
#     auth = ('deepsearch', 'Lina123$')
    hosts = os.getenv('ES_HOSTS')
    auth = os.getenv('ES_AUTH')


class strapi_config:
    #hosts = 'http://13.124.235.216:1337/'
    hosts = os.getenv('STRAPI_HOSTS')
    collection = 'crawler-keywords'
