"""Data Scraping project Configuration File"""

DB_NAME = 'jobs'

SCRAPING_URL = 'https://il.linkedin.com/jobs/' \
               'data-scientist-jobs?position=1&pageNum=0'

LIST_UPDATE_MAX_TIME = 5

TIME_BETWEEN_SCROLL_ATTEMPTS = 0.5

SCROLL_ATTEMPTS = LIST_UPDATE_MAX_TIME // TIME_BETWEEN_SCROLL_ATTEMPTS

WAIT_TIME = 1

SCROLL_TIME = 3
