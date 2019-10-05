#! /usr/bin/python3

from DBconn import DBConn
from Database import *
import logging
import MySQLdb
import datetime
from tkinter import messagebox
import configparser


logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Utils.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if path.exists('config.ini'):
    print('yes')
    config = configparser.ConfigParser()
    config.read("config.ini")
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

## Clock Functions

def clock_in(employee_id):
    # Check last entry
    last_entry = TimeEntries(db_type='sqlite',
                             employee_id=employee_id,
                             entry_date=datetime.date.today().__str__(),
                             clock_out='NULL').select_query()
    if last_entry:
        # Notify user pof error
        messagebox.showerror(title="ERROR", message=config['MESSAGES']['CLOCK_IN_AFTER_MISSED_CLOCK_OUT'])
        # Send alert email
        pass
    new_entry = TimeEntries(db_type='sqlite',
                            employee_id=employee_id,
                            entry_date=datetime.date.today().__str__(),
                            clock_in=datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    new_entry.insert()
