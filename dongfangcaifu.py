from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class to specify the search method
import requests
from bs4 import BeautifulSoup
import sqlite3
import random
import string
import json
from crawl_helper import generate_random_number_string

def get_url_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")
        # print(soup)
        # Define a CSS selector to locate the news article links on the page
        # Adjust this selector to match the structure of the website you're scraping
        article_links = soup.select("#ContentBody > p")
        # print(article_links)
        content = ""
        # Loop through the article links and extract information
        for link in article_links:
            article_title = link.text  # Get the title of the article
            content += article_title
        return content
    
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return None






def generate_random_number_string(min_length=1, max_length=15):
    length = random.randint(min_length, max_length)
    random_string = ''.join(random.choice(string.digits) for _ in range(length))
    return random_string

# 生成一个随机数字字符串
random_number_string = generate_random_number_string()
# print(random_number_string)


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
    url = f'https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index={index}&page_size=20&req_trace={random_number_string}'
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    # print(response.text)
    # soup = BeautifulSoup(response.text, "html.parser")
    data = json.loads(response.text)
    # print(data)
    news_list = data["data"]['list']
    # print(news_list)
    for news in news_list:
        docurl = news['uniqueUrl']
        doctitle = news['title']
        doc = {}
        doc['url'] = docurl
        doc['title'] = doctitle
        doc['content'] = get_url_content(docurl)
        doc['time'] = news['showTime']
        # print(doc)
        cursor.execute('''INSERT INTO news (url, content, title, time)
                  VALUES (?, ?, ?, ?)''', (doc['url'], doc['content'], doc['title'], doc['time']))

    conn.commit()
    conn.close()
    
# get_content('https://finance.eastmoney.com/a/cgnjj_1.html')
# https://money.163.com/special/00259K2L/data_stock_redian.js?callback=data_callback
# https://money.163.com/special/00259K2L/data_stock_redian_02.js?callback=data_callback
# https://money.163.com/special/00259K2L/data_stock_redian_03.js?callback=data_callback


for i in range(1,5):
    get_content(i)
# get_content('https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index=2&page_size=20&req_trace=1694154671821&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20&callback=jQuery183040257121358187997_1694154670958&_=1694154671821')
# get_content('https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=350&order=1&needInteractData=0&page_index=3&page_size=20&req_trace=1694154737942&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20&callback=jQuery1830477268958035018_1694154737674&_=1694154737942')