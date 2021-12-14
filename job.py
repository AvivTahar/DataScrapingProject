import logging


class Job:

    def __init__(self, title, company, location, publish_period):
        self.title = title
        self.company = company
        self._location = location
        self._publish_period = publish_period
        self.seniority = None
        self.emp_type = None
        self.job_function = None
        self.industry = None
        self._application_str = None
        logging.debug(f'Job class instantiated with:'
                      f' title = {title},'
                      f' company = {company},'
                      f' location = {location},'
                      f' publish period = {publish_period}.')

    def set_extra_info(self, info):
        keys = info.keys()
        if 'Seniority level' in keys:
            self.seniority = info['Seniority level']
        if 'Employment type' in keys:
            self.emp_type = info['Employment type']
        if 'Job function' in keys:
            self.job_function = info['Job function']
        if 'Industries' in keys:
            self.industry = info['Industries']
        if 'Applicants String' in keys:
            self._application_str = info['Applicants String']
        logging.debug(f'Extra job info set at instance with: '
                      f'Seniority = {self.seniority} '
                      f'Employment type = {self.emp_type} '
                      f'Job Function = {self.job_function} '
                      f'Industries = {self.industry} '
                      f'Application String = {self._application_str}.')

    def get_city(self):
        logging.debug(f'Location Fetch (get_city): {self._location}')
        return self._location.split(',')[0]

    def get_country(self):
        logging.debug(f'Location Fetch (get_country): {self._location}')
        return self._location.split(',')[-1][1:]

    def __str__(self):
        return f'Title: {self.title}, Company: {self.company}, Location: ' \
               f'{self._location}, Publishment Period: {self._publish_period},'\
               f' Seniority Level: {self.seniority}, Employment Type: ' \
               f'{self.emp_type}, Job Function: {self.job_function}, ' \
               f'Industry: {self.industry}, No. of Applicants: ' \
               f'{self._application_str}'
