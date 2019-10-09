#! /usr/bin/python3

from DBconn import DBConn
import pandas as pd
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
    except MySQLdb.OperationalError as e:
        logger.exception("Caught exception connecting to database\n Error: {}".format(e))
        raise


def timed_messagebox(title, message):
    messagebox = Toplevel()
    messagebox.title(title)
    m = Message(messagebox, text=message, padx=100, pady=100)
    m.config(font=('TkDefaultFont', 20))
    m.pack()
    messagebox.after(3000, messagebox.destroy)

def calculate_hours_for_the_week(employee_id):
    # Get mysql total time
    time_entries = TimeEntries(employee_id=employee_id)
    current_date = datetime.date.today().weekday()
    if current_date == 0:
        date_param = datetime.date.today()
    else:
        date_param = between(datetime.date.today() + datetime.timedelta(days=-current_date), datetime.date.today())
    time_entries.entry_date = date_param
    try:
        entries = time_entries.select_query('mysql')
    except MySQLdb.OperationalError as e:
        timed_messagebox("ERROR!", "Error while connceting to database, please try again later.")
        logging.exception("Caught exception while connceting to database")
        raise e
    df = pd.DataFrame.from_records(entries)
    mysql_total_time = df['total_time'].sum().total_seconds()
    mysql_total_hours, mysql_total_minutes = calculate_hours_and_minutes(mysql_total_time)
    # Get sqlite total time
    time_entries = TimeEntries(employee_id=employee_id).select_query('sqlite')
    for entry in time_entries:
        time_entry = TimeEntries()
        time_entry.load('sqlite', record=entry)
        time_entry.to_datetime()
        if time_entry.clock_in and not time_entry.clock_out:
            clock_in = time_entry.clock_in
            clock_out = datetime.date.today()
        elif time_entry.clock_in and time_entry.clock_out:
            clock_in = time_entry.clock_in
            clock_out = time_entry.clock_out
        else:
            timed_messagebox("Error", "There was an error in your clock entries, your total hour count may be off.")
        sqlite_total_time = (clock_out - clock_in).total_seconds()
        sqlite_total_hours, sqlite_total_minutes = calculate_hours_and_minutes(sqlite_total_time)
        mysql_total_hours += sqlite_total_hours
        mysql_total_minutes += sqlite_total_minutes
    return mysql_total_hours, mysql_total_minutes

def calculate_hours_and_minutes(total_seconds):
    hours = int(total_seconds / 60 // 60)
    minutes = int(round(60*((total_seconds / 60 / 60) - hours), 0))
    return hours, minutes
