from selenium import webdriver
from selenium.webdriver.common.by import By  # Import the By class to specify the search method
import requests
from bs4 import BeautifulSoup
import sqlite3

def get_content(url):
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
        article_links = soup.select("#content > div.post_body p")
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
driver.get("https://money.163.com/stock/")

# Wait for the page to fully load (you may need to adjust the sleep time)
import time
time.sleep(5)  # Wait for 5 seconds (adjust as needed)

# Extract the content you want using CSS selector
link_elements = driver.find_elements(By.CSS_SELECTOR, "div>div.news_title>h3>a")

doc = {}

for link in link_elements:
    docurl = link.get_attribute("href")
    doctitle = link.text
    doc['url'] = docurl
    doc['title'] = doctitle
    doc['content'] = get_content(docurl)
    doc['time'] = None
    # print(doc)
    cursor.execute('''INSERT INTO news (url, content, title, time)
                  VALUES (?, ?, ?, ?)''', (doc['url'], doc['content'], doc['title'], doc['time']))

conn.commit()
conn.close()

driver.quit()

# Now you can use 'docurl' and 'title' in your code
# body > div > div.ne-area > div.main_area.clearfix > div.c_left > div.hot_list > div > div.newsdata_wrap > ul > li > div > div.data_row.news_article.clearfix.news_first > div > div.news_title > h3 > a
# body > div > div.ne-area > div.main_area.clearfix > div.c_left > div.hot_list > div > div.newsdata_wrap > ul > li > div > div:nth-child(3) > div > div.news_title > h3 > a
# body > div > div.ne-area > div.main_area.clearfix > div.c_left > div.hot_list > div > div.newsdata_wrap > ul > li > div > div:nth-child(7) > div > div.news_title > h3 > a