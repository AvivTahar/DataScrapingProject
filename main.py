from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


SCRAPING_URL = 'https://il.linkedin.com/jobs/' \
        'data-scientist-jobs?position=1&pageNum=0'

LIST_UPDATE_MAX_TIME = 5
TIME_BETWEEN_SCROLL_ATTEMPTS = 0.5
SCROLL_ATTEMPTS = LIST_UPDATE_MAX_TIME // TIME_BETWEEN_SCROLL_ATTEMPTS


def scroll(browser_driver):
    """
    performs a scroll to the bottom of page. if a button press is needed('show more jobs')
    it is clicked. the function checks if the scroll caused the page to load more jobs.
    if additional jobs were not loaded for TIME_BETWEEN_SCROLL_ATTEMPTS it will try again.
    if there is no success for LIST_UPDATE_MAX_TIME it will return with 0
    :param browser_driver:
    :return: additional length of page after the scroll in pixels
    """
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
                return 0

            # searches for a 'show more' button
            button_els = browser_driver.find_elements(By.CLASS_NAME, "infinite-scroller__show-more-button--visible")

            # if button found
            if button_els:
                button_els[0].click()
        # new results appeared
        else:
            return new_dist - scroll_dist


def collect_job_extra_info(driver_extra):
    """
    collect_job_extra_info receives a chrome driver object an collects, per
    each job for which it is being called, the extra information from the
    right-hand side of the html page
    :param driver_extra: A chrome driver to have access to html
    :return: A dictionary of extra information
    """
    page_content = driver_extra.find_element(By.CLASS_NAME, 'base-serp-page__content')
    top_card = page_content.find_element(By.CLASS_NAME, 'top-card-layout__entity-info-container')
    flavor_second = top_card.find_elements(By.CLASS_NAME, 'topcard__flavor-row')[1]         # There are two topcad__flavor-row

    number_of_applicants = flavor_second.find_element(By.CLASS_NAME, 'num-applicants__caption').text

    core_section_tag = driver_extra.find_element(
        By.CLASS_NAME, 'core-section-container__content')
    criteria_list_tag = core_section_tag.find_element(By.CLASS_NAME, 'description__job-criteria-list')  # ul
    li_four_elements_list = criteria_list_tag.find_elements(By.TAG_NAME, 'li')

    extra_dict = {}
    for li in li_four_elements_list:
        key = li.find_element(By.CLASS_NAME, 'description__job-criteria-subheader').text.strip()
        value = li.find_element(By.TAG_NAME, 'span').text.strip()
        extra_dict[key] = value

    li_amount = len(li_four_elements_list)
    four_keys = ['Seniority level', 'Employment type', 'Job function', 'Industries']
    if not li_amount == 4:
        for item in four_keys:
            if item not in extra_dict.keys():
                extra_dict[item] = 'No-Data'

    extra_dict['Applicants String'] = number_of_applicants
    return extra_dict


def collect_jobs(driver_collect, start_index):
    """
    collect_jobs takes a selenium driver object of a job platform web page and
    scrapes, for every job card, the job title, the company offering the job,
    the job's location and a time note relative to the time of running the
    scraper.
    :param driver_collect: A Selenium chrome driver object
    :param start_index: Scraping starts from start_index
    :return: The function stores the collected data into a list of dictionaries
    and prints the list. returns number of jobs collected
    """
    jobs_collected = 0

    # Acquire the list that encapsulates all the job entries
    title_divs = driver_collect.find_elements(By.CLASS_NAME,
                                              'base-card')

    # Acquire data for each individual parent tag
    list_of_jobs = []
    for div in title_divs[start_index:-1]:
        title = div.find_element(By.CLASS_NAME, 'base-search-card__title')
        company = div.find_element(By.CLASS_NAME, 'base-search-card__subtitle')
        location = div.find_element(By.CLASS_NAME, 'job-search-card__location')
        publish_period = div.find_element(By.TAG_NAME, 'time')
        list_of_jobs.append({'card_title': f'{title.text}',
                              'company': f'{company.text}',
                              'location': f'{location.text}',
                              'publishment time': f'{publish_period.text}'})

        #wait = WebDriverWait(driver_collect, 10)
        #job_listing = wait.until(lambda d: div.find_element(By.CLASS_NAME, 'base-card__full-link'))
        job_listing = div.find_element(By.CLASS_NAME, 'base-card__full-link')
        # click on job listing to see more info
        job_listing.click()
        sleep(3)

        list_of_jobs[-1].update(collect_job_extra_info(driver_collect))
        jobs_collected += 1
        print(list_of_jobs[-1])

    return jobs_collected


if __name__ == '__main__':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(SCRAPING_URL)

    # Wait until first parsed tag is uploaded
    element_present = ec.presence_of_element_located((By.CLASS_NAME,
                                                      'base-search-card__info'))
    WebDriverWait(driver, LIST_UPDATE_MAX_TIME).until(element_present)
    driver.maximize_window()
    sleep(1)

    jobs_collected = 0
    while True:
        jobs_collected += collect_jobs(driver, jobs_collected)
        if not jobs_collected:
            break
        scroll(driver)
        sleep(3)

    driver.close()
