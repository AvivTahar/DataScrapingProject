from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
url = 'https://il.linkedin.com/jobs/data-scientist-jobs?position=1&pageNum=0'
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

# titles_list = []
# for t in range(len(titles)):
#     titles_list.append(titles[t].text)

# print(titles_list)

#
headline_list = []


TIME_BETWEEN_SCROLLS = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    sleep(TIME_BETWEEN_SCROLLS)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Press the button as you can
    driver.find_element_by_class_name("").click()

titles = driver.find_elements(By.TAG_NAME, 'h3')
                              #//h3[@class="base-search-card_title"]')
print(len(titles))

#soup = BeautifulSoup(source, 'lxml')
# for div in soup.find_all('div', class_='base-search-card__info'):
#     headline = div.h3.text
#     headline_list.append(headline.strip())
#
# print(headline_list)
# print(len(headline_list))
