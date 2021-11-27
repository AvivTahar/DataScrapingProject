

class Jobs:

    def __init__(self, title, company, location, publish_period):
        self._title = title
        self._company = company
        self._location = location
        self._publish_period = publish_period
        self._seniority = None
        self._emp_type = None
        self._job_function = None
        self._industry = None
        self._application_str = None

    def set_extra_info(self, info):
        keys = info.keys()
        if 'Seniority level' in keys:
            self._seniority = info['Seniority level']
        if 'Employment type' in keys:
            self._emp_type = info['Employment type']
        if 'Job function' in keys:
            self._job_function = info['Job function']
        if 'Industries' in keys:
            self._industry = info['Industries']
        if 'Applicants String' in keys:
            self._application_str = info['Applicants String']

    def __str__(self):
        return f'Title: {self._title}, Company: {self._company}, Location: ' \
               f'{self._location}, Publishment Period: {self._publish_period},'\
               f' Seniority Level: {self._seniority}, Employment Type: ' \
               f'{self._emp_type}, Job Function: {self._job_function}, ' \
               f'Industry: {self._industry}, No. of Applicants: ' \
               f'{self._application_str}'
