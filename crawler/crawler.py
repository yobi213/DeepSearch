from utils import Get_Article_Body, ariticle_reply, get_article_df
import datetime
from selenium import webdriver
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DeepSearch'))))
from connector import es_connector


#chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome("chromedriver", options = chrome_options)


#date
today = datetime.datetime.now()
yesterday = today + datetime.timedelta(days=-1)


# 검색 키워드 입력
search_keywords = ['삼성생명','라이나생명','ESG','보험','금융']

# 기간 설정
years = [yesterday.strftime("%Y-%m-%d")[:4]]
months = [datetime.datetime.now().strftime("%Y-%m-%d")[5:7]]
all_days = [yesterday.strftime("%Y-%m-%d")[-2:]]

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
    
# es.createIndex(index='news-naver',settings=settings, mappings=mappings)

for i in range(len(article_url_df)):
    try:
        article_dict = Get_Article_Body(article_url_df['url'][i],driver)
        article_dict['search_keywords'] = article_url_df['search_keyword'][i]
        print(article_dict)
        es.dataInsert(index='news-naver', data=article_dict)
        #reply_df = ariticle_reply()
        #reply_dfs.append(reply_df)
    except:
        continue

