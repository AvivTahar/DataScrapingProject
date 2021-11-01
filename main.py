from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

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


def collect_jobs(driver):
    pass


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
url = 'https://il.linkedin.com/jobs/data-scientist-jobs?position=1&pageNum=0'
driver = webdriver.Chrome(options=chrome_options)

driver.get(url)

scroll(driver)
