import logging

from selenium import webdriver
from jobcollector import JobCollector
from google_searcher import GoogleSearcher
from configurations import *
import argparse
from db import DB
from coord_fetcher import CoordFetcher
import logging

logging.basicConfig(filename='linkedinDataScrapeLog.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=CONF_LEVEL)

if __name__ == '__main__':
    logging.info('Linkedin Job Scrapper started')

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
    # service = webdriver.Chrome.service.Service('./chromedriver')
    # service.start()
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--incognito')
    options.add_argument("--no-sandbox")
    options.add_argument("enable-automation")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("window-size=1400, 1500")

    # options = options.to_capabilities()
    # driver = webdriver.Remote(service.service_url, options)

    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--incognito")
    # chrome_options.headless = True
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument(
    #     f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--remote-debugging-port=9222")
    # Initiate chrome driver and get website
    driver = webdriver.Chrome(options=options, executable_path='./chromedriver')

    google_searcher = GoogleSearcher(driver)
    google_searcher.open_results(args.search_query)

    logging.info('Google search has been performed. Initiating JobCollector')

    # Collect Jobs
    jc = JobCollector(driver)
    logging.info(f'Job Collector initiated with driver: {driver}'
                 f'Calling JobColletctors collect_jobs method')
    jobs = jc.collect_jobs()
    logging.info('Finished collecting jobs')

    logging.info('Initiating Database activity')
    db = DB(args.db_user, args.db_pass, args.db_ip, DB_NAME)
    logging.debug(f'Database class initiated with: db_user = {args.db_user},'
                  f'db_ip = {args.db_ip}, db_name = {DB_NAME}')

    db.insert(jobs)
    logging.info('Database job insertion performed. Adding coordinates'
                 ' from API')

    db.update_coordinates(CoordFetcher(args.key))
    logging.info('performed DB update with coordinates from external API')

    db.disconnect()
    driver.close()
    logging.debug('Disconnected from Database and closed Chrome Driver')
