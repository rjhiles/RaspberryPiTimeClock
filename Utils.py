#! /usr/bin/python3

from DBconn import DBConn
from Database import *


def update_employee_table():
    with DBConn('sqlite') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM employee""")
        conn.commit()
    with DBConn('mysql') as conn:
        employees = Employee(db_type='mysql', is_active=True).select_query()
    with DBConn('sqlite') as sqlite_conn:
        c = sqlite_conn.cursor()
        for employee in employees:
            query = """INSERT INTO employee VALUES {} """.format(employee)
            c.execute(query)
        sqlite_conn.commit()

