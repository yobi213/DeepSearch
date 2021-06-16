import requests
import pandas as pd
import numpy as np
import time
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from tqdm import tqdm_notebook
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip
import math
import re
import collections as co

# 기사 본문
def Get_Article_Body(url): 
    driver.get(url)
    time.sleep(1) 
    title = driver.find_element_by_css_selector('div.article_info h3').text
    write_time = driver.find_element_by_css_selector('span.t11').text[:10].replace('.', '-')
    press_name = driver.find_element_by_css_selector('div.press_logo img').get_attribute('title')
    body = driver.find_elements_by_xpath("//div[@id='articleBodyContents']") 
    text = "" 
    try:
        Nreply = driver.find_element_by_xpath("//span[@class='u_cbox_count']") 
    except:
        Nreply = driver.find_element_by_xpath('//*[@id="cbox_module"]/div/h5/em')
    Nreply = Nreply.text 
    Nreply = int(Nreply.replace(',','')) 
    for b in body: 
        text = text.join(b.text) 
    # re-enter 
    if text.strip(url) == '':
        driver.refresh() 
        time.sleep(1) 
        driver.get(url) 
        body = driver.find_elements_by_xpath("//div[@id='articleBody']") 
        text = "" 

        for b in body: 
            text = text.join(b.text) 
    tmp_article = { 'url':url, 'title':title,'body':text ,'Nreply':Nreply,'write_time':write_time,
                   'press_name':press_name} 
    return tmp_article

# 댓글
def ariticle_reply(): 
    time.sleep(1)
    noreply = False
    no_reply = pd.DataFrame({'replyID':[None], 
                             'reply':[None], 
                             'time':[None], 
                             're_reply':[None], 
                             'like':[None], 
                             'dislike':[None], 
                             'url':[None] }) 
    try: 
        # Click more reply
        driver.find_elements_by_xpath("//span[@class='u_cbox_in_view_comment']")[0].click() 
    except: 
        noreply = True 
        
    if noreply: 
        tmp_reply = no_reply 
    else: 
        driver.refresh() 
        time.sleep(2) 
        # 총 댓글 갯수 확인 
        Nreply = driver.find_element_by_xpath("//span[@class='u_cbox_count']") 
        Nreply = Nreply.text 
        Nreply = int(Nreply.replace(',','')) 
        
        if Nreply > 20: 
            NreplyLoop = (Nreply//20) if Nreply%20 > 0 else (Nreply//20)-1 
            for i in range(NreplyLoop): 
                driver.find_elements_by_xpath("//span[@class='u_cbox_page_more']")[0].click() 
                time.sleep(1) 
                # 댓글 수집 
        reply = driver.find_elements_by_xpath('//div[@class="u_cbox_comment_box"]') 
        if len(reply) > 0: # 댓글이 적어도 하나라도 있는 경우: 클린봇 X, 삭제 X 
            tmp_reply = co.deque([]) 
            for r in reply: 
                tmp_list = r.text.split('\n') 
                if len(tmp_list) == 11:
                    tmp_reply.append(tmp_list)
            tmp_reply = pd.DataFrame(tmp_reply) 
            if len(tmp_reply) == 0: # 댓글 하나만 있는데 삭제되었을 때 
                tmp_reply = no_reply 
            else: 
                tmp_reply = tmp_reply[[0,3,4,5,8,10]].rename(columns={ 
                    0:'replyID', 
                    3:'reply', 
                    4:'time', 
                    5:'re_reply', 
                    8:'like', 
                    10:'dislike' }) 
                tmp_reply['url'] = url
                
        
        else:
            
            tmp_reply = no_reply

    return tmp_reply
# 기사 URL DF
def get_article_df(years, months, all_days, search_keywords):

    # 해당 일자 기사 목록dml 빈 리스트
    article_urls = []
    for search_keyword in search_keywords:
        for year in years:
            for month in months:
                for day in all_days:
                    ## 페이지 이동
                    base_url = 'https://search.naver.com/search.naver?where=news&sm=tab_pge&query={0}&sort=1&photo=0&field=0&pd=3&ds={1}.{2}.{3}&de={1}.{2}.{3}&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so:dd,p:from20210613to20210615,a:all&start=1'
                    search_url = base_url.format(search_keyword,year, month , day)
                    driver.get(search_url)
                    time.sleep(1)
                    btn_html = driver.page_source
                    btn_soup = BeautifulSoup(btn_html, 'html.parser')
                    btns = btn_soup.select('div.sc_page_inner a.btn')
                    for i in range(len(btns)):
                        
                        driver.get(search_url+str(i))

                        # 페이지 소스 가져오기
                        page_html = driver.page_source
                        page_soup = BeautifulSoup(page_html, 'html.parser')
                        links = page_soup.select('ul.list_news a')
                        # 하이퍼링크 가져오기
                        for link in links:
                            link = link['href']
                            news_dict = {'YEAR':year, 'MONTH':month, 'DAY':day, 'url':link, 'search_keyword':search_keyword}
                            article_urls.append(news_dict)

    article_url_df = pd.DataFrame(article_urls).drop_duplicates(subset='url').reset_index(drop=True)
    article_url_df = article_url_df[article_url_df['url'].str.contains('https://news.naver.com/main/')].reset_index(drop=True)
    #뉴스 기사 주소 추출 완료
    return article_url_df


today = datetime.datetime.now()
yesterday = today + datetime.timedelta(days=-1)


# 검색 키워드 입력
search_keywords = ['라이나생명']

# 기간 설정
years = [yesterday.strftime("%Y-%m-%d")[:4]]
months = [datetime.datetime.now().strftime("%Y-%m-%d")[5:7]]
all_days = ['14', yesterday.strftime("%Y-%m-%d")[-2:]]


driver = Chrome()
article_url_df = get_article_df(years, months, all_days, search_keywords)
urls = article_url_df['url']
#기사 내용 수집
article_dicts = []
reply_dfs = []

for url in urls:
    article_dict = Get_Article_Body(url)
    reply_df = ariticle_reply()
    article_dicts.append(article_dict)
    reply_dfs.append(reply_df)
    
    
article_df = pd.DataFrame(article_dicts)
article_df = pd.merge(article_df, article_url_df[['url', 'search_keyword']], on='url', how='left')
reply_df = pd.concat(reply_dfs).reset_index(drop=True)
reply_df = reply_df[reply_df['replyID'].notnull()].reset_index(drop=True)




import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname('DeepSearch'))))
from connector import es_connector

data = article_df.to_dict()

for d in data:
    es.dataInsert(index='test3',body=d)
    