import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


class LinkGetter:
    def __init__(self, driver):
        self.driver = driver

    def get_link(self, search_query):
        search_query = search_query.replace(" ", "+")
        self.driver.get('https://www.google.com/search?q=' + search_query + '+linkedin')
        sleep(2)
        search_results = self.driver.find_element(By.XPATH, f'//div[@role="main"]')
        link = search_results.find_element(By.TAG_NAME, 'a')
        link.click()


if __name__ == '__main__':
    # test
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)
    link_getter = LinkGetter(driver)
    link_getter.get_link("full stack jobs in israel")