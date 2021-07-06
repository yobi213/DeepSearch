import requests
import datetime
import json
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DeepSearch'))))
from connector import es_connector

es = es_connector.ES()
index_name = 'dailynews-naver'
#test index
#index_name = 'test_crawler'
# kst
target_day = datetime.date.today()
# utc
# target_day = datetime.date.today() - datetime.timedelta(days=1)
target_day = target_day.strftime('%Y-%m-%d')
webhook_url = os.getenv('WEBHOOK')

query = '''
{"sort": [
    {
      "토픽": {
        "order": "asc"
      }
    }
  ],
  "query": {
    "match": {
      "작성일시": "%s"
    }
  },
  "_source": ["토픽", "제목", "URL"]
}
''' % (target_day)

res = es.searchFilter(index = index_name, body = query)

webhook_payload = {'text':'Daily News Monitoring', 'blocks':[]}
info_section = {'type':'section', 'text': {'type':'mrkdwn','text':f"{datetime.date.today() + datetime.timedelta(days=1)}"}}
divider_section = {'type':'divider'}
webhook_payload['blocks'].append(info_section)
webhook_payload['blocks'].append(divider_section)

topic = res['hits']['hits'][0]['_source']['토픽']
topic_section = {'type':'section', 'text': {'type':'mrkdwn','text':f"*[{topic} 소식]*"}}
webhook_payload['blocks'].append(topic_section)

j=0
for i in range(len(res['hits']['hits'])):
    j += 1
    temp_topic = res['hits']['hits'][i]['_source']['토픽']
    title = res['hits']['hits'][i]['_source']['제목']
    url = res['hits']['hits'][i]['_source']['URL']
    
    if temp_topic == '삼성생명':
        temp_topic = '업계'
    elif temp_topic == '라이나생명':
        temp_topic = '당사'
            
    if topic != temp_topic:
        topic = temp_topic
        webhook_payload['blocks'].append(divider_section)
        j=1
        topic_section = {'type':'section', 'text': {'type':'mrkdwn','text':f"*[{topic} 소식]*"}}
        webhook_payload['blocks'].append(topic_section)
        
    news_section = {'type':'section', 'text' :{'type':'mrkdwn', 'text': f"{j}. {title} (<{url}|Link>)"}}
    webhook_payload['blocks'].append(news_section)
    
requests.post(url=webhook_url, json=webhook_payload)
