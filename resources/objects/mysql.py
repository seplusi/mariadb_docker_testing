import mysql.connector
import time
from mysql.connector.errors import OperationalError


class mysqlClient(object):
    def __init__(self, host, port, user, passwd, db_name, timeout=60) -> None:
        initial_ts = int(time.time())
        while int(time.time()) < initial_ts + timeout:
            try:
                self.mysql_conn = mysql.connector.connect(host=host, port=port, user=user, password=passwd, database=db_name)
                break
            except OperationalError:
                # If container was just created, there will be errors trying to connect to the container's database
                # It requires time to allow the DB to fully start in the container
                time.sleep(2)
        else:
            assert False, f'Could not connect database'

    def close(self):
        # Close connection to DB
        self.mysql_conn.cursor().close()
        self.mysql_conn.close()
    
    def get_data_from_query(self, query):
        # Gets data from DB based in query
        cursor = self.mysql_conn.cursor()
        cursor.execute(query)

        return cursor.fetchall()

    def insert_data(self, query):
        # Insert data based in query
        cursor = self.mysql_conn.cursor()
        cursor.execute(query)
        self.mysql_conn.commit()
