from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from configurations import *


class GoogleSearcher:
    def __init__(self, driver):
        self.driver = driver
        logging.info(f'Initiated GoogleSearcher class')
        logging.debug(f'driver print {self.driver}')

    def open_results(self, search_query):
        search_query = search_query.replace(" ", "+")
        self.driver.get('https://www.google.com/search?q=' + search_query +
                        '+linkedin')
        logging.info('Successfully performed google search')

        sleep(2)
        search_results = self.driver.find_element(By.XPATH,
                                                  f'//div[@role="main"]')
        logging.debug(f'search_results for div tag role main: {search_results}')

        link = search_results.find_element(By.TAG_NAME, 'a')
        logging.debug(f'link for search_result tag a: {link}')

        link.click()
        logging.info('Clicking google search result performed')

        # Wait until first parsed tag is uploaded
        element_present = ec.presence_of_element_located((
            By.CLASS_NAME, 'base-search-card__info'))
        WebDriverWait(self.driver, LIST_UPDATE_MAX_TIME).until(element_present)
        self.driver.maximize_window()
        logging.info('Chrome window has been maximized')
        sleep(WAIT_TIME)

