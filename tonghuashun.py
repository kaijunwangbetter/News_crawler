from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class to specify the search method
import requests
from bs4 import BeautifulSoup
import sqlite3
import random
import string
import json
from crawl_helper import generate_random_number_string
import re

def get_url_content(id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    # Send an HTTP GET request to the URL
    response = requests.get(f'http://wapi.hexun.com/detail_master.cc?newsId={id}&version=808', headers=headers)
    # print(response.text)

    if response.text:
        data = json.loads(response.text)
        content_html = data["datas"]["content"]
        soup = BeautifulSoup(content_html, "html.parser")
        text_content = soup.get_text()

        # print(text_content)
        return text_content
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return None






random_number_string = generate_random_number_string()


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
    url = f'https://news.10jqka.com.cn/today_list/index_1.shtml'

    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    article_links = soup.select("body ul span > a")
    # print(article_links)
# body > div.content-1200 > div.module-l.fl > div.list-con > ul > li:nth-child(1) > span > a
    for link in article_links:
        # print(link)
        docurl = link.get("href")
        # print(docurl)
        doctitle = link.get("title")
        doc = {}
        # print(doctitle)
        doc['url'] = docurl
        doc['title'] = doctitle
        doc['content'] = get_url_content(docurl)
        doc['time'] = None
    # print(news_list)
    for news in article_links:
        docurl = news['entityurl']
        doctitle = news['title']
        docid = news['id']
        doc = {}
        doc['url'] = docurl
        doc['title'] = doctitle
        # doc['content'] = get_url_content(docid)
        doc['time'] = news['entitytime']
        # print(doc)
        cursor.execute('''INSERT INTO news (url, content, title, time)
                  VALUES (?, ?, ?, ?)''', (doc['url'], doc['content'], doc['title'], doc['time']))

    conn.commit()
    conn.close()
    
# https://mp.weixin.qq.com/s?__biz=MjM5NzQ5MTkyMA==&chksm=bd471d408a3094566014775d3383bc8d09013e1f295b6c270b74e1e21cb161b32789bcba8b5f&idx=1&mid=2657786111&sn=6b28b5b346ffd4ac9859f53df3197901

# for i in range(1,6):
#     get_content(i)

get_content(1)