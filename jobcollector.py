from selenium.webdriver.common.by import By
from time import sleep
from configurations import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import selenium.common.exceptions as sel_exc
from job import Job


class JobCollector:

    def __init__(self, driver):
        self._driver = driver

    def _scroll(self):
        """
        performs a scroll to the bottom of page. if a button press is needed
        ('show more jobs') it is clicked.
        The function checks if the scroll caused the page to load more jobs.
        if additional jobs were not loaded for TIME_BETWEEN_SCROLL_ATTEMPTS it
        will try again.
        if there is no success for LIST_UPDATE_MAX_TIME it will return with 0
        :return: additional length of page after the scroll in pixels
        """
        scroll_attempts_left = SCROLL_ATTEMPTS

        # Wait for first job element to appear
        element_present = ec.presence_of_element_located(
            (By.CLASS_NAME, 'base-search-card__info'))
        WebDriverWait(self._driver, LIST_UPDATE_MAX_TIME).until(
            element_present)

        while True:
            # Get scroll distance
            scroll_dist = self._driver.execute_script(
                "return document.body.scrollHeight")

            # Scroll down to bottom
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            sleep(TIME_BETWEEN_SCROLL_ATTEMPTS)

            # Calculate new scroll height and compare with last scroll height
            new_dist = self._driver.execute_script(
                "return document.body.scrollHeight")

            # If no new results are shown
            if new_dist == scroll_dist:
                if scroll_attempts_left > 0:
                    scroll_attempts_left -= 1
                else:
                    # Scroll finished or timed out
                    return 0

                # Searches for a 'show more' button
                button_els = self._driver.find_elements(By.CLASS_NAME,
                                                        "infinite-scroller__"
                                                        "show-more-button--"
                                                        "visible")

                # If button found
                if button_els:
                    button_els[0].click()
            # New results appeared
            else:
                return new_dist - scroll_dist

    def _collect_jobs_batch(self, start_index):
        """
        collect_jobs scrapes, for every job card, the job title, the company offering the
        job, the job's location and a time note relative to the time of running
        the scraper.
        :param start_index: Scraping starts from the job listing at start_index
        :return: list of job objects and next index to collect
        """

        sleep(WAIT_TIME)

        # Acquire data for each job element
        list_of_jobs = []

        job_listing_idx = start_index
        while True:
            try:
                # Searches for a <div> element with requested index
                title_div = self._driver.\
                    find_element(By.XPATH, f'//div[@data-row='
                                           f'"{str(job_listing_idx)}"]')
            except sel_exc.NoSuchElementException:
                # If not found could be a rare special case <a> element
                try:
                    title_div = self._driver.\
                        find_element(By.XPATH, f'//a[@data-row='
                                               f'"{str(job_listing_idx)}"]')
                except sel_exc.NoSuchElementException:
                    # No element found with the requested index
                    break
            try:
                title = title_div.find_element(By.CLASS_NAME,
                                               'base-search-card__title')
                company = title_div.find_element(By.CLASS_NAME,
                                                 'base-search-card__subtitle')
                location = title_div.find_element(By.CLASS_NAME,
                                                  'job-search-card__location')
                publish_period = title_div.find_element(By.TAG_NAME, 'time')
            except sel_exc.NoSuchElementException:
                # In case encountered some strange job listing skip to next job
                print("Error: skipped job listing")
                job_listing_idx += 1
                continue

            job = Job(title.text, company.text, location.text,
                      publish_period.text)
            list_of_jobs.append(job)

            try:
                # Should work in case title_div is a <div> element
                job_listing = title_div.find_element(By.CLASS_NAME,
                                                     'base-card__full-link')
            except sel_exc.NoSuchElementException:
                # Should work in the rare case title_div is an <a> element
                job_listing = title_div

            # Click on job listing to see more info
            job_listing.click()

            sleep(WAIT_TIME)
            try:
                self._collect_job_extra_info(job_inst=job)
                # list_of_jobs[-1].set_extra_info(
                #     self._collect_job_extra_info())
            except sel_exc.NoSuchElementException:
                # In case encountered some strange job listing skip to next job
                print("Error: partial job collection")
                pass
            except sel_exc.StaleElementReferenceException:
                # If stale element
                print('Error: StaleElementReferenceException: element is '
                      'not attached to the page document')

            print(job)
            job_listing_idx += 1

        return job_listing_idx, list_of_jobs

    def _collect_job_extra_info(self, job_inst):
        """
        collect_job_extra_info collects, per each job for which it is being called,
        the extra information from the right-hand side of the html page
        and updates the new info in the job object.
        assumes the driver had already clicked the job link and page finished loading
        :return:
        """
        page_content = self._driver.find_element(By.CLASS_NAME,
                                                 'base-serp-page__content')
        top_card = page_content.find_element(By.CLASS_NAME,
                                             'top-card-layout__entity-'
                                             'info-container')
        flavor_second = \
            top_card.find_elements(By.CLASS_NAME, 'topcard__flavor-row')[1]
        # There are two topcad__flavor-row tags

        number_of_applicants = flavor_second.\
            find_element(By.CLASS_NAME, 'num-applicants__caption').text

        core_section_tag = self._driver.find_element(
            By.CLASS_NAME, 'core-section-container__content')
        criteria_list_tag = core_section_tag.\
            find_element(By.CLASS_NAME, 'description__job-criteria-list')  # ul

        li_four_elements_list = criteria_list_tag.\
            find_elements(By.TAG_NAME, 'li')

        extra_dict = {}
        for li in li_four_elements_list:
            key = li.find_element(By.CLASS_NAME,
                                  'description__job-criteria'
                                  '-subheader').text.strip()

            value = li.find_element(By.TAG_NAME, 'span').text.strip()
            extra_dict[key] = value

        extra_dict['Applicants String'] = number_of_applicants

        job_inst.set_extra_info(extra_dict)

    def collect_jobs(self):
        """
        Performs general job collection using JobCollector methods
        :return: A list of job entries instances
        """
        all_jobs = []

        # job index on linkedin job list starts from 1
        jobs_idx = 1
        while True:
            jobs_idx, jobs_batch = self._collect_jobs_batch(
                start_index=jobs_idx)
            if len(jobs_batch) == 0:
                break

            all_jobs += jobs_batch
            self._scroll()
            sleep(SCROLL_TIME)
        return all_jobs

