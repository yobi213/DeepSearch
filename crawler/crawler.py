from utils import Get_Article_Body, ariticle_reply, get_article_df
import datetime
from selenium.webdriver import Chrome
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DeepSearch'))))
from connector import es_connector


today = datetime.datetime.now()
yesterday = today + datetime.timedelta(days=-1)


# 검색 키워드 입력
search_keywords = ['보험','금융']

# 기간 설정
years = [yesterday.strftime("%Y-%m-%d")[:4]]
months = [datetime.datetime.now().strftime("%Y-%m-%d")[5:7]]
all_days = ['14', yesterday.strftime("%Y-%m-%d")[-2:]]

driver = Chrome()
article_url_df = get_article_df(years, months, all_days, search_keywords, driver)
urls = article_url_df['url']
#기사 내용 수집
article_dicts = []
reply_dfs = []



es = es_connector.ES()

# with open('settings.json','r') as f:
#     settings = json.load(f)
    
# with open('mappings.json','r') as f:
#     mappings = json.load(f)
    
# es.createIndex(index='news',settings=settings, mappings=mappings)


for url in urls:
    article_dict = Get_Article_Body(url,driver)
    print(article_dict)
    es.dataInsert(index='news', data=article_dict)
    print('진행중')
    #reply_df = ariticle_reply()
    #reply_dfs.append(reply_df)

