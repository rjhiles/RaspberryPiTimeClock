#! /usr/bin/python3

from DBconn import DBConn
from Database import *
import logging
import MySQLdb
import datetime


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Utils.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def update_employee_table():
    # Retrieve from remote DB
    try:
        with DBConn('mysql') as conn:
            employees = Employee(db_type='mysql', is_active=True).select_query()
        with DBConn('sqlite') as sqlite_conn:
            c = sqlite_conn.cursor()
            c.execute("""DELETE FROM employee""")
            sqlite_conn.commit()
            for employee in employees:
                query = """INSERT INTO employee VALUES {} """.format(employee)
                c.execute(query)
            sqlite_conn.commit()
    except MySQLdb.Error as e:
        logger.exception("Caught exception connecting to database\n Error: {}".format(e))
