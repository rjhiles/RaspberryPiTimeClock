# /usr/bin/python3

import MySQLdb
import sqlite3
import os
import configparser


class DBConn:
    """
    Databse connection for timeclock with context manager.
    USE:        with DBconn() as conn:
                    conn.query(your_query)
                    conn.commit()
    """

    def __init__(self, db_type='mysql'):
        if db_type == 'mysql':
            if os.path.exists('config.ini'):
                config = configparser.ConfigParser()
                config.read('config.ini')
                if config['SETUP']['LOCAL_CREDENTIALS'] == 'True':
                    host = config['CREDENTIALS']['HOST']
                    user = config['CREDENTIALS']['USER']
                    passwd = config['CREDENTIALS']['PASS']
                    db = config['CREDENTIALS']['DB']
                else:
                    host = os.environ['TIMECLOCK_DB_HOST']
                    user = os.environ['TIMECLOCK_DB_USER']
                    passwd = os.environ['TIMECLOCK_DB_PWD']
                    db = os.environ['TIMECLOCK_DB_NAME']
            else:
                host = os.environ['TIMECLOCK_DB_HOST']
                user = os.environ['TIMECLOCK_DB_USER']
                passwd = os.environ['TIMECLOCK_DB_PWD']
                db = os.environ['TIMECLOCK_DB_NAME']
            self.conn = MySQLdb.Connection(
                host=host,
                user=user,
                passwd=passwd,
                port=3306,
                db=db)
        elif db_type == 'sqlite':
            self.conn = sqlite3.connect('TimeClock.db')

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
