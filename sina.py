from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class to specify the search method
import requests
from bs4 import BeautifulSoup
import sqlite3
import random
import string
import json
from crawl_helper import generate_random_number_string
import lxml.html
import lxml.etree
import re
from utils.downloader import Downloader
from utils.disk_cache import DiskCache

no_cache_downloader = Downloader(cache=None)

def get_url_content(url):
    """
    获取新闻内容
    :param url: str, 新闻链接
    :return: str, 新闻内容
    """
    content = ''
    try:
        text = no_cache_downloader(url)
        html = lxml.etree.HTML(text)
        res = html.xpath('//*[@id="artibody" or @id="article"]//p')
        p_str_list = [lxml.etree.tostring(node).decode('utf-8') for node in res]
        p_str = ''.join(p_str_list)
        html_content = lxml.html.fromstring(p_str)
        content = html_content.text_content()
        # 清理未知字符和空白字符
        content = re.sub(r'\u3000', '', content)
        content = re.sub(r'[ \xa0?]+', ' ', content)
        content = re.sub(r'\s*\n\s*', '\n', content)
        content = re.sub(r'\s*(\s)', r'\1', content)
        content = content.strip()
    except Exception as e:
        print('get_news_content(%s) error:' % url, e)
    return content


def get_content(index):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS news
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                   url TEXT,
                   content TEXT,
                   title TEXT,
                   time TEXT)''')


    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    random_number_string = generate_random_number_string()
    url = f'https://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=5&page=1'
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'
    # print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    # print(soup)
    data = json.loads(response.text)
    # print(data)
    news_list = data['result']["data"]
    # print(news_list)
    for news in news_list:
        # print(news)
        docurl = news['url']
        doctitle = news['title']
        doc = {}
        doc['url'] = docurl
        doc['title'] = doctitle
        doc['content'] = get_url_content(docurl)
        doc['time'] = None
        # print(doc)
        cursor.execute('''INSERT INTO news (url, content, title, time)
                  VALUES (?, ?, ?, ?)''', (doc['url'], doc['content'], doc['title'], doc['time']))

    conn.commit()
    conn.close()
    
# get_content('https://finance.eastmoney.com/a/cgnjj_1.html')
# https://money.163.com/special/00259K2L/data_stock_redian.js?callback=data_callback
# https://money.163.com/special/00259K2L/data_stock_redian_02.js?callback=data_callback
# https://money.163.com/special/00259K2L/data_stock_redian_03.js?callback=data_callback


# for i in range(1,5):
#     get_content(i)
get_content(1)
# get_content('https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index=2&page_size=20&req_trace=1694154671821&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20&callback=jQuery183040257121358187997_1694154670958&_=1694154671821')
# get_content('https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index=3&page_size=20&req_trace=1694154737942&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20&callback=jQuery1830477268958035018_1694154737674&_=1694154737942')

# https://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=10&page=1&callback=feedCardJsonpCallback&_=1694328573613

# https://feed.mix.sina.com.cn/api/roll/get?pageid=155&lid=1686&num=10&page=2&callback=feedCardJsonpCallback&_=1694328692203
  