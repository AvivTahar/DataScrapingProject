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

    def get_city(self):
        return self._location.split(',')[0]

    def get_country(self):
        return self._location.split(',')[-1][1:]

    def __str__(self):
        return f'Title: {self.title}, Company: {self.company}, Location: ' \
               f'{self._location}, Publishment Period: {self._publish_period},'\
               f' Seniority Level: {self.seniority}, Employment Type: ' \
               f'{self.emp_type}, Job Function: {self.job_function}, ' \
               f'Industry: {self.industry}, No. of Applicants: ' \
               f'{self._application_str}'
