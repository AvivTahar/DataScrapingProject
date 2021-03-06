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

    # scroll is not needed in headless driver
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
        sleep(LIST_UPDATE_MAX_TIME)

        logging.debug('base-search-card__info appeared')

        while True:
            logging.debug(
                f'Attempting scroll. Scrolling Attempts Left '
                f'{scroll_attempts_left}')
            # Get scroll distance
            scroll_dist = self._driver.execute_script(
                "return document.body.scrollHeight")
            logging.debug(f'scroll distance at beginning of loop:'
                          f' {scroll_dist}')

            # Scroll down to bottom
            self._driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            logging.debug('Scroll performed')

            # Wait to load page
            sleep(TIME_BETWEEN_SCROLL_ATTEMPTS)
            logging.debug('Page load waiting time passed')

            # Calculate new scroll height and compare with last scroll height
            new_dist = self._driver.execute_script(
                "return document.body.scrollHeight")
            logging.debug(f'new distance after scroll: {new_dist}')

            # If no new results are shown
            if new_dist == scroll_dist:
                if scroll_attempts_left > 0:
                    scroll_attempts_left -= 1
                else:
                    # Scroll finished or timed out
                    logging.debug('Scroll finished or timed out')
                    return 0

                # Searches for a 'Show More Jobs' button
                button_els = self._driver.find_elements(By.CLASS_NAME,
                                                        "infinite-scroller__"
                                                        "show-more-button--"
                                                        "visible")

                # If button found
                if button_els:
                    button_els[0].click()
                    logging.debug('Show More Jobs button found and clicked')
            # New results appeared
            else:
                return new_dist - scroll_dist

    @staticmethod
    def _click_job_card(t_div):
        """click_job_card clicks a sole job card to expose extra info per job"""
        try:
            # Should work in case title_div is a <div> element
            job_listing = t_div.find_element(By.CLASS_NAME,
                                             'base-card__full-link')
        except sel_exc.NoSuchElementException:
            # Should work in the rare case title_div is an <a> element
            job_listing = t_div

        # Click on job listing to see more info
        job_listing.click()

    def _get_title_div(self, job_index):
        """get_title_div uses the scrapper driver to get title div according
        to the website's html structure"""
        try:
            # Searches for a <div> element with requested index
            title_div = self._driver. \
                find_element(By.XPATH, f'//div[@data-row='
                                       f'"{str(job_index)}"]')
            logging.debug('Got title_div using \'data-row\' XPATH tag')

        except sel_exc.NoSuchElementException:
            # If not found could be a rare special case <a> element
            title_div = self._driver. \
                find_element(By.XPATH, f'//a[@data-row='
                                       f'"{str(job_index)}"]')
            logging.info('Got title_div using \'a\' XPATH tag')
        return title_div

    @staticmethod
    def _get_left_info(title_div):
        """_get_left_info gets all the info on the initial card from the
        left hand side of the linkedin page"""

        title = title_div.find_element(By.CLASS_NAME,
                                       'base-search-card__title')
        company = title_div.find_element(By.CLASS_NAME,
                                         'base-search-card__subtitle')
        location = title_div.find_element(By.CLASS_NAME,
                                          'job-search-card__location')
        publish_period = title_div.find_element(By.TAG_NAME, 'time')

        logging.debug(f'Left info fetch: '
                      f'{title, company, location, publish_period}')
        return title, company, location, publish_period

    def _collect_jobs_batch(self, start_index):
        """
        collect_jobs scrapes, for every job card, the job title, the company
        offering the job, the job's location and a time note relative to the
        time of running the scraper.
        :param start_index: Scraping starts from the job listing at start_index
        :return: list of job objects and next index to collect
        """

        sleep(WAIT_TIME)

        # Acquire data for each job element
        list_of_jobs = []

        job_listing_idx = start_index
        logging.debug(f'Performing job batch collection with job_listing_idx ='
                      f' {start_index}')

        while True:

            try:
                title_div = self._get_title_div(job_listing_idx)
            except sel_exc.NoSuchElementException:
                logging.info('Did not find title_div html tag. Exiting job'
                             ' batch collection loop')
                break

            try:
                title, company, location, publish_period = \
                    self._get_left_info(title_div)
            except sel_exc.NoSuchElementException:
                # In case encountered some strange job listing skip to next job
                logging.error("Error: Did not find left card data on title_div"
                              " tag. Skipping job listing - moving to next idx")
                job_listing_idx += 1
                continue

            job = Job(title.text, company.text, location.text,
                      publish_period.text)
            list_of_jobs.append(job)
            logging.info('Successful initiation of Job class instance')
            logging.debug(f'Job Card: {job.__str__()}')

            # Click a job card to show scrapper extra job info
            self._click_job_card(title_div)
            logging.info('Clicked on left side job card')

            sleep(WAIT_TIME)
            try:
                self._collect_job_extra_info(job_inst=job)
            except sel_exc.NoSuchElementException:
                # In case encountered some strange job listing skip to next job
                logging.error("Error: partial job collection")
            except sel_exc.StaleElementReferenceException:
                # If stale element
                logging.error('Error: StaleElementReferenceException: element is '
                      'not attached to the page document')

            print(job)
            job_listing_idx += 1

        return job_listing_idx, list_of_jobs

    def _collect_job_extra_info(self, job_inst):
        """
        collect_job_extra_info collects, per each job for which it is being
        called, the extra information from the right-hand side of the html page
        and updates the new info in the job object.
        assumes the driver had already clicked the job link and page loaded
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

        number_of_applicants = flavor_second. \
            find_element(By.CLASS_NAME, 'num-applicants__caption').text

        core_section_tag = self._driver.find_element(
            By.CLASS_NAME, 'core-section-container__content')
        criteria_list_tag = core_section_tag. \
            find_element(By.CLASS_NAME, 'description__job-criteria-list')  # ul

        li_four_elements_list = criteria_list_tag. \
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

        # Job index on linkedin job list starts from 1
        jobs_idx = 1
        logging.info('Beginning of main colect_job method\'s job-batch '
                     'collecting loop')
        while True:
            jobs_idx, jobs_batch = self._collect_jobs_batch(
                start_index=jobs_idx)
            logging.debug(f'Collected job batch with index: {jobs_idx} and'
                          f'jobs_batch: {jobs_batch}')
            if len(jobs_batch) == 0:
                logging.debug('jobs_batch equals 0, exiting job-batch '
                              'collecting loop')
                break

            all_jobs += jobs_batch

            # scroll is not needed in headless driver
            # self._scroll()
            # logging.info('Page scroll')
            sleep(SCROLL_TIME)
        return all_jobs
