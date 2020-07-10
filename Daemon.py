#! /usr/bin/python3

from Database import *
import logging
from time import sleep
import datetime


def transport_completed_entries():
    time_entries = TimeEntries().select_query('sqlite')
    entry = TimeEntries()
    for record in time_entries:
        entry.load('sqlite', record=record)
        entry_date = datetime.datetime.strptime(entry.entry_date, '%Y-%m-%d').date()
        if (entry.clock_in and entry.clock_out) or entry.error_entry or entry_date != datetime.date.today():
            mysql_entry = TimeEntries()
            mysql_entry.load('mysql', record=record)
            mysql_entry.to_datetime()
            if entry_date != datetime.date.today():
                mysql_entry.error_entry = 1
                set_employee_notification(mysql_entry.employee_id, mysql_entry.entry_date)
            mysql_entry.id = None
            if mysql_entry.clock_in and mysql_entry.clock_out:
                mysql_entry.compute_total_time()
            try:
                mysql_entry.insert('mysql')
            except Exception as e:
                logging.exception("=================================\nError transporting entries.  Error  {}".format(e))
                continue
            else:
                entry.delete('sqlite')


def set_employee_notification(employee_id, missed_entry_date):
    notification = Notify(employee_id=employee_id, missed_entry_date=missed_entry_date)
    notification.to_string()
    notification.insert('sqlite')

def main_loop():
    while True:
        transport_completed_entries()
        sleep(60)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Utils.log')
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(funcName)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


