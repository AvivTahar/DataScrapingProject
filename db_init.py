import pymysql
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='initialize the data base for storing the job entries')
    parser.add_argument('db_user', type=ascii, help='User name of the database server')
    parser.add_argument('db_pass', type=ascii, help='Password for the database user')
    parser.add_argument('db_ip', type=ascii, help='IP address of the MySQL database server')
    args = parser.parse_args()

    # takes arguments without the quotes
    db_user_name = args.db_user[1:-1]
    db_user_pass = args.db_pass[1:-1]
    db_server_ip = args.db_ip[1:-1]

    newDatabaseName = "jobs"  # Name of the database that is to be created

    connection = pymysql.connect(host=db_server_ip, user=db_user_name, password=db_user_pass,
                                 cursorclass=pymysql.cursors.DictCursor)
    print("connected to database")
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE " + newDatabaseName)
        cursor.execute("USE " + newDatabaseName)
        cursor.execute("CREATE TABLE companies(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "company VARCHAR(255), "
                                "UNIQUE(company)"
                                ")")
        cursor.execute("CREATE TABLE countries(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "country VARCHAR(255), "
                                "UNIQUE(country)"
                                ")")
        cursor.execute("CREATE TABLE cities(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "city VARCHAR(255), "
                                "country_id INT, "
                                "FOREIGN KEY(country_id) REFERENCES countries(id), "
                                "CONSTRAINT UC_city UNIQUE(city, country_id)"
                                ")")
        cursor.execute("CREATE TABLE seniority(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "seniority_level VARCHAR(255), "
                                "UNIQUE(seniority_level)"
                                ")")
        cursor.execute("CREATE TABLE employment_type(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "employment_type VARCHAR(255), "
                                "UNIQUE(employment_type)"
                                ")")
        cursor.execute("CREATE TABLE job_function(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                               "job_function VARCHAR(255), "
                               "UNIQUE(job_function)"
                               ")")
        cursor.execute("CREATE TABLE industries(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
                                "industry VARCHAR(255), "
                                "UNIQUE(industry)"
                               ")")
        cursor.execute("CREATE TABLE jobs(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, "
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
    finally:
        connection.close()
