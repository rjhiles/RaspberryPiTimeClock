# /usr/bin/python3

#import MySQLdb
#import MySQLdb.cursors
import pymysql
import pymysql.cursors
import sqlite3
import os
import configparser


class DBConn:
    """
    Database connection for timeclock with context manager.
    USE:        with DBconn() as conn:
                    conn.query(your_query)
                    conn.commit()
    """

    def __init__(self, db_type):
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
            self.conn = pymysql.Connection(
                host=host,
                user=user,
                passwd=passwd,
                port=3306,
                db=db,
                #cursorclass=MySQLdb.cursors.DictCursor,
		cursorclass=pymysql.cursors.DictCursor)
        elif db_type == 'sqlite':
            self.conn = sqlite3.connect('TimeClock.db')
            self.conn.row_factory = self.dict_factory

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    @staticmethod
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
