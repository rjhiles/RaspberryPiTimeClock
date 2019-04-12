# /usr/bin/python3

import MySQLdb
import os

class DBConn():
    """
    Databse connection for timeclock with context manager.
    USE:        with DBconn() as conn:
                    conn.query(your_query)
                    conn.commit()
    """

    def __init__(self):
        self.conn = MySQLdb.Connection(
            host=os.environ['TIMECLOCK_DB_HOST'],
            user=os.environ['TIMECLOCK_DB_USER'],
            passwd=os.environ['TIMECLOCK_DB_PWD'],
            port=3306,
            db=os.environ['TIMECLOCK_DB_NAME'])



    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
