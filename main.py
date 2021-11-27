from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import selenium.common.exceptions as sel_exc
from jobcollector import JobCollector
from google_searcher import GoogleSearcher
from configurations import *
import argparse


if __name__ == '__main__':
    # Set chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    # Initiate chrome driver and get website
    driver = webdriver.Chrome(options=chrome_options)

    parser = argparse.ArgumentParser(description=
                                     'Linkedin Job Scraping Project')
    parser.add_argument(
        'search_query', type=str,
        help='User search string for a job: Enter job role and location')
    args = parser.parse_args()

    google_searcher = GoogleSearcher(driver)
    google_searcher.open_results(args.search_query)

    # Collect Jobs
    jc = JobCollector(driver)
    jobs = jc.collect_jobs()

    driver.close()
