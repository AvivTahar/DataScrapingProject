from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


TIMEOUT = 3


def scroll(driver):
    pass


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
    # Acquire parent tags
    title_divs = driver_collect.find_elements(By.CLASS_NAME,
                                              'base-search-card__info')
    # Acquire data for each individual parent tag
    list_of_dicts = []
    for div in title_divs:
        title = div.find_element(By.CLASS_NAME, 'base-search-card__title')
        company = div.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
        location = div.find_element(By.CLASS_NAME, 'job-search-card__location')
        divdate = div.find_element(By.TAG_NAME, 'time')

        list_of_dicts.append({'card_title': f'{title.text}',
                              'company': f'{company.text}',
                              'location': f'{location.text}',
                              'date': f'{divdate.text}'})

    # Print each job dictionary
    for dictionary in list_of_dicts:
        print(dictionary)

    driver_collect.close()


if __name__ == '__main__':

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    url = 'https://il.linkedin.com/jobs/' \
          'data-scientist-jobs?position=1&pageNum=0'
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # Wait until first parsed tag is uploaded
    element_present = ec.presence_of_element_located((By.CLASS_NAME,
                                                      'base-search-card__info'))
    WebDriverWait(driver, TIMEOUT).until(element_present)

    collect_jobs(driver)
