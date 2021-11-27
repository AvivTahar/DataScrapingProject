from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from configurations import *


class GoogleSearcher:
    def __init__(self, driver):
        self.driver = driver

    def open_results(self, search_query):
        search_query = search_query.replace(" ", "+")
        self.driver.get('https://www.google.com/search?q=' + search_query +
                        '+linkedin')
        sleep(2)
        search_results = self.driver.find_element(By.XPATH,
                                                  f'//div[@role="main"]')
        link = search_results.find_element(By.TAG_NAME, 'a')
        link.click()

        # Wait until first parsed tag is uploaded
        element_present = ec.presence_of_element_located((
            By.CLASS_NAME, 'base-search-card__info'))
        WebDriverWait(self.driver, LIST_UPDATE_MAX_TIME).until(element_present)
        self.driver.maximize_window()
        sleep(WAIT_TIME)


if __name__ == '__main__':
    # test
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)
    link_getter = GoogleSearcher(driver)
    link_getter.open_results("full stack jobs in israel")