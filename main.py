from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

SCTAPING_URL = 'https://il.linkedin.com/jobs/' \
      'data-scientist-jobs?position=1&pageNum=0'

LIST_UPDATE_MAX_TIME = 5
TIME_BETWEEN_SCROLL_ATTEMPTS = 0.5
SCROLL_ATTEMPTS = LIST_UPDATE_MAX_TIME // TIME_BETWEEN_SCROLL_ATTEMPTS

def scroll(browser_driver):
    scroll_attempts_left = SCROLL_ATTEMPTS

    # wait for first job element to appear
    element_present = ec.presence_of_element_located((By.CLASS_NAME, 'base-search-card__info'))
    WebDriverWait(browser_driver, LIST_UPDATE_MAX_TIME).until(element_present)

    while True:
        # Get scroll distance
        scroll_dist = browser_driver.execute_script("return document.body.scrollHeight")

        # Scroll down to bottom
        browser_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(TIME_BETWEEN_SCROLL_ATTEMPTS)

        # Calculate new scroll height and compare with last scroll height
        new_dist = browser_driver.execute_script("return document.body.scrollHeight")

        # if no new results are shown
        if new_dist == scroll_dist:
            if scroll_attempts_left > 0:
                scroll_attempts_left -= 1
            else:
                # scroll finished or timed out
                break

            # searches for a 'show more' button
            button_els = browser_driver.find_elements(By.CLASS_NAME, "infinite-scroller__show-more-button--visible")

            # if button found
            if button_els:
                button_els[0].click()
        # new results appeared
        else:
            scroll_attempts_left = SCROLL_ATTEMPTS


def collect_jobs(driver_collect):
    """
    collect_jobs takes a selenium driver object of a job platform web page and
    scrapes, for every job card, the job title, the company offering the job,
    the job's location and a time note relative to the time of running the
    scraper.
    :param driver_collect: A Selenium chrome driver object
    :return: The function stores the collected data into a list of dictionaries
    and prints the list
    """
    # Acquire the list that encapsulates all the job entries
    title_divs = driver_collect.find_elements(By.CLASS_NAME,
                                              'base-search-card__info')

    # Acquire data for each individual parent tag
    list_of_dicts = []
    for div in title_divs:
        title = div.find_element(By.CLASS_NAME, 'base-search-card__title')
        company = div.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
        location = div.find_element(By.CLASS_NAME, 'job-search-card__location')
        publish_period = div.find_element(By.TAG_NAME, 'time')

        list_of_dicts.append({'card_title': f'{title.text}',
                              'company': f'{company.text}',
                              'location': f'{location.text}',
                              'date': f'{publish_period.text}'})
        print(list_of_dicts[-1])
    # Print each job entry
    # for dictionary in list_of_dicts:
    #     print(dictionary)


if __name__ == '__main__':

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SCTAPING_URL)

    # Wait until first parsed tag is uploaded
    element_present = ec.presence_of_element_located((By.CLASS_NAME,
                                                      'base-search-card__info'))
    WebDriverWait(driver, LIST_UPDATE_MAX_TIME).until(element_present)

    scroll(driver)
    collect_jobs(driver)

    driver.close()
