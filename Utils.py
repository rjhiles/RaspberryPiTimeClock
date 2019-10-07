#! /usr/bin/python3

from DBconn import DBConn
from Database import *
import logging
import MySQLdb
import datetime
from tkinter import Toplevel, Message
import configparser
import os

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Utils.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

if os.path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read("config.ini")

def update_employee_table():
    # Retrieve from remote DB
    try:
        with DBConn('mysql') as conn:
            employees = Employee(is_active=True).select_query('mysql')
        with DBConn('sqlite') as sqlite_conn:
            c = sqlite_conn.cursor()
            c.execute("""DELETE FROM employee""")
            sqlite_conn.commit()
        for employee in employees:
            current_employee = Employee(**employee)
            current_employee.insert('sqlite')
    except MySQLdb.Error as e:
        logger.exception("Caught exception connecting to database\n Error: {}".format(e))


def timed_messagebox(title, message):
    messagebox = Toplevel()
    messagebox.title(title)
    m = Message(messagebox, text=message, padx=100, pady=100)
    m.config(font=('TkDefaultFont', 20))
    m.pack()
    messagebox.after(3000, messagebox.destroy)
