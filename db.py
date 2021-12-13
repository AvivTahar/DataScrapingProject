import pymysql
from configurations import *


class DB:
    def __init__(self, db_user_name, db_user_pass, db_server_ip, db_name):
        db_server_ip = db_server_ip[1:-1]
        db_user_name = db_user_name[1:-1]
        db_user_pass = db_user_pass[1:-1]

        self.connection = pymysql.connect(host=db_server_ip,
                                          user=db_user_name,
                                          password=db_user_pass,
                                          cursorclass=
                                          pymysql.cursors.DictCursor)

        self.cursor = self.connection.cursor()

        self.cursor.execute("show databases")
        dbses = self.cursor.fetchall()

        # Create Database if not exist
        db_exist = False
        for db in dbses:
            if db['Database'] == DB_NAME:
                db_exist = True
                break
        if not db_exist:
            self._create_db()

        self.cursor.execute("USE " + db_name)

    def _create_db(self):
        """_create_db creates a database for the web scraper"""
        newDatabaseName = DB_NAME  # Name of the database that is to be created
        try:
            self.cursor.execute("CREATE DATABASE " + newDatabaseName)
            self.cursor.execute("USE " + newDatabaseName)
            self.cursor.execute(
                "CREATE TABLE companies(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "company VARCHAR(255), "
                "UNIQUE(company)"
                ")")
            self.cursor.execute(
                "CREATE TABLE countries(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "country VARCHAR(255), "
                "UNIQUE(country)"
                ")")
            self.cursor.execute(
                "CREATE TABLE cities(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "city VARCHAR(255), "
                "country_id INT, "
                "FOREIGN KEY(country_id) REFERENCES countries(id), "
                "CONSTRAINT UC_city UNIQUE(city, country_id)"
                ")")
            self.cursor.execute(
                "CREATE TABLE seniority(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "seniority_level VARCHAR(255), "
                "UNIQUE(seniority_level)"
                ")")
            self.cursor.execute(
                "CREATE TABLE employment_type(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "employment_type VARCHAR(255), "
                "UNIQUE(employment_type)"
                ")")
            self.cursor.execute(
                "CREATE TABLE job_function(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "job_function VARCHAR(255), "
                "UNIQUE(job_function)"
                ")")
            self.cursor.execute(
                "CREATE TABLE industries(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "industry VARCHAR(255), "
                "UNIQUE(industry)"
                ")")
            self.cursor.execute(
                "CREATE TABLE jobs(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                "job_title VARCHAR(255), "
                "company_id INT,"
                "city_id INT, "
                "seniority_id INT, "
                "emp_type_id INT, "
                "job_func_id INT, "
                "industry_id INT, "
                "FOREIGN KEY(company_id) REFERENCES companies(id), "
                "FOREIGN KEY(city_id) REFERENCES cities(id), "
                "FOREIGN KEY(seniority_id) REFERENCES seniority(id), "
                "FOREIGN KEY(emp_type_id) REFERENCES employment_type(id), "
                "FOREIGN KEY(job_func_id) REFERENCES job_function(id), "
                "FOREIGN KEY(industry_id) REFERENCES industries(id), "
                "CONSTRAINT UC_job UNIQUE(job_title, company_id, city_id, seniority_id)"
                ")")
            print("database created")
        except Exception as e:
            print("Exception:{}".format(e))

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
