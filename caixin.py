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
    url = f'https://gateway.caixin.com/api/extapi/homeInterface.jsp?channel=125&start=0&count=2&picdim=_145_97'
    #listArticle > div:nth-child(1) > h4 > a
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    # print(response.text)
    data = json.loads(response.text)
    content = data["datas"][1]['summ']
    print(content)
    if json_data_match:
        json_data_str = json_data_match.group(1)
        json_data = json.loads(json_data_str)
        data = json_data.get("result")
    else:
        print("无法提取JSON数据")

    news_list = data
    # print(news_list)
    for news in news_list:
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
    


# for i in range(1,6):
#     get_content(i)

get_content(1)
# get_url_content(1)




# https://opentool.hexun.com/MongodbNewsService/getNewsListByJson.jsp?id=189223574&s=20&cp=1&callback=ptemplate_jsonp_007220895193096655
# https://opentool.hexun.com/MongodbNewsService/getNewsListByJson.jsp?id=189223574&s=20&cp=2&callback=ptemplate_jsonp_005797325500028894