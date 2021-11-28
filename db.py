import pymysql
import jobs

class DB:
    def __init__(self, db_user_name, db_user_pass, db_server_ip, db_name):
        db_server_ip = db_server_ip[1:-1]
        db_user_name = db_user_name[1:-1]
        db_user_pass = db_user_pass[1:-1]

        self.connection = pymysql.connect(host=db_server_ip, user=db_user_name, password=db_user_pass,
                                          cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection.cursor()
        self.cursor.execute("USE " + db_name)

    def insert(self, jobs):
        pass