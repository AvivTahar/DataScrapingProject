"""Data Scraping project Configuration File"""

DB_NAME = 'jobs'

LIST_UPDATE_MAX_TIME = 5

TIME_BETWEEN_SCROLL_ATTEMPTS = 0.5

SCROLL_ATTEMPTS = LIST_UPDATE_MAX_TIME // TIME_BETWEEN_SCROLL_ATTEMPTS

WAIT_TIME = 2

SCROLL_TIME = 3

GEO_API = 'http://api.positionstack.com/v1/'
