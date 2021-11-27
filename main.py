from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import selenium.common.exceptions as sel_exc
from jobcollector import JobCollector
from google_searcher import GoogleSearcher
from configurations import *


if __name__ == '__main__':
    # Set chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    # Initiate chrome driver and get website
    driver = webdriver.Chrome(options=chrome_options)
    google_searcher = GoogleSearcher(driver)
    google_searcher.open_results(input('Enter google search: '))

    # Collect Jobs
    jc = JobCollector(driver)
    jobs = jc.collect_jobs()

    driver.close()
