from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class to specify the search method
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import sqlite3

def get_url_content(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    # Send an HTTP GET request to the URL
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    article_links = soup.select("#ArticleContent > p")
    content = ""
        # Loop through the article links and extract information
    for link in article_links:
        article_title = link.text  # Get the title of the article
        content += article_title
    # print(content)
    return content











conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS news
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT,
                content TEXT,
                title TEXT,
                time TEXT)''')

# Create a new instance of the Chrome driver (you'll need to install ChromeDriver)
driver = webdriver.Chrome()

# Navigate to the URL
driver.get("https://new.qq.com/ch/finance/")

# Wait for the page to fully load (you may need to adjust the sleep time)
import time
time.sleep(5)  # Wait for 5 seconds (adjust as needed)


for i in range(10):  # 例如，模拟滚动或点击5次
    # 在此处执行向下滚动或点击"加载更多"按钮的操作
    # 如果是滚动，你可以使用以下代码：
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    
    # 如果是点击按钮，你可以使用以下代码：
    # load_more_button = driver.find_element(By.ID, 'load-more-button')  # 使用正确的元素定位方法
    # load_more_button.click()
    
    # 等待一段时间以确保新内容加载完成（根据需要调整等待时间）
    time.sleep(2)




# Extract the content you want using CSS selector
link_elements = driver.find_elements(By.CSS_SELECTOR, "div.detail>h3>a")

doc = {}

for link in link_elements:
    docurl = link.get_attribute("href")
    doctitle = link.text
    doc['url'] = docurl
    doc['title'] = doctitle
    if docurl:
        doc['content'] = get_url_content(docurl)
    else:
        doc['content'] = None
    doc['time'] = None
    # print(doc)
    if doc['content'] == None:
        pass
    else:
        cursor.execute('''INSERT INTO news (url, content, title, time)
                  VALUES (?, ?, ?, ?)''', (doc['url'], doc['content'], doc['title'], doc['time']))

conn.commit()
conn.close()

driver.quit()