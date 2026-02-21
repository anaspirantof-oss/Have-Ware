import mysql.connector as msql
import sys

class data_class:
    def __init__(self, db_config):
        try:
            self.connection = msql.connect(
                host=db_config['host'],
                user=db_config['user'],
                password=db_config['password'],
                database="haveware_db"
            )
            self.cursor = self.connection.cursor(dictionary=True)
        except msql.Error as err:
            print(f"\n[!] Connection Error: {err}")
            sys.exit()

    def execute_read(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def execute_write(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return self.cursor.lastrowid
        except msql.Error as err: 
            self.connection.rollback()
            print(f"Transaction Error: {err}")
            return None

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

