import pymysql
from job import Job


class DB:
    def __init__(self, db_user_name, db_user_pass, db_server_ip, db_name):
        db_server_ip = db_server_ip[1:-1]
        db_user_name = db_user_name[1:-1]
        db_user_pass = db_user_pass[1:-1]

        self.connection = pymysql.connect(host=db_server_ip, user=db_user_name, password=db_user_pass,
                                          cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection.cursor()
        self.cursor.execute("USE " + db_name)

    def insert(self, job_list):
        try:
            for job_entry in job_list:
                self.cursor.execute(f'INSERT IGNORE INTO companies(company) VALUES ("{job_entry.company}")')
                self.cursor.execute(f'SELECT id FROM companies WHERE company = "{job_entry.company}"')
                company_id = self.cursor.fetchone()["id"]

                self.cursor.execute(f'INSERT IGNORE INTO countries(country) VALUES ("{job_entry.get_country()}")')
                self.cursor.execute(f'SELECT id FROM countries WHERE country = "{job_entry.get_country()}"')
                country_id = self.cursor.fetchone()["id"]

                self.cursor.execute(f'INSERT IGNORE INTO cities(city, country_id) VALUES ("{job_entry.get_city()}", "{country_id}")')
                self.cursor.execute(f'SELECT id FROM cities WHERE city = "{job_entry.get_city()}"')
                city_id = self.cursor.fetchone()["id"]

                self.cursor.execute(f'INSERT IGNORE INTO seniority(seniority_level) VALUES ("{job_entry.seniority}")')
                self.cursor.execute(f'SELECT id FROM seniority WHERE seniority_level = "{job_entry.seniority}"')
                seniority_id = self.cursor.fetchone()["id"]

                self.cursor.execute(f'INSERT IGNORE INTO employment_type(employment_type) VALUES ("{job_entry.emp_type}")')
                self.cursor.execute(f'SELECT id FROM employment_type WHERE employment_type = "{job_entry.emp_type}"')
                emp_type_id = self.cursor.fetchone()["id"]

                self.cursor.execute(
                    f'INSERT IGNORE INTO job_function(job_function) VALUES ("{job_entry.job_function}")')
                self.cursor.execute(f'SELECT id FROM job_function WHERE job_function = "{job_entry.job_function}"')
                job_function_id = self.cursor.fetchone()["id"]

                self.cursor.execute(
                    f'INSERT IGNORE INTO industries(industry) VALUES ("{job_entry.industry}")')
                self.cursor.execute(f'SELECT id FROM industries WHERE industry = "{job_entry.industry}"')
                industry_id = self.cursor.fetchone()["id"]

                self.cursor.execute(
                    f'INSERT IGNORE INTO jobs('
                    f'job_title, company_id, city_id, seniority_id, emp_type_id, job_func_id, industry_id) VALUES '
                    f'("{job_entry.title}", "{company_id}", "{city_id}", "{seniority_id}", "{emp_type_id}", "{job_function_id}", "{industry_id}")')
        except Exception as e:
            print(e)
        finally:
            self.connection.commit()

    def disconnect(self):
        self.connection.close()
