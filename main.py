from selenium import webdriver
from jobcollector import JobCollector
from google_searcher import GoogleSearcher
from configurations import *
import argparse
from db import DB
from coord_fetcher import CoordFetcher

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=
                                     'Linkedin Job Scraping Project')
    parser.add_argument(
        'search_query', type=str,
        help='User search string for a job: Enter job role and location')
    parser.add_argument('db_user', type=ascii, help='User name of the '
                                                    'database server')
    parser.add_argument('db_pass', type=ascii, help='Password for the '
                                                    'database user')
    parser.add_argument('db_ip', type=ascii, help='IP address of the MySQL '
                                                  'database server')
    parser.add_argument('key', type=ascii, help='private key for use in Positionstack API')
    args = parser.parse_args()

    # Set chrome driver options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    # Initiate chrome driver and get website
    driver = webdriver.Chrome(options=chrome_options)

    google_searcher = GoogleSearcher(driver)
    google_searcher.open_results(args.search_query)

    # Collect Jobs
    jc = JobCollector(driver)
    jobs = jc.collect_jobs()

    db = DB(args.db_user, args.db_pass, args.db_ip, DB_NAME)
    db.insert(jobs)
    db.update_coordinates(CoordFetcher(args.key))

    db.disconnect()
    driver.close()
