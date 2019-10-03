import os
import sqlite3
from DBconn import DBConn
from Database import Employee


table_queries = [
    # Employee Table
    """CREATE TABLE employee(id INT PRIMARY KEY, first_name TEXT, last_name TEXT, preferred_name TEXT, pin TEXT, is_active NUMERIC)""",
    # Time Entries Table
    """CREATE TABLE time_entries(id INT PRIMARY KEY, employee_id INT, entry_date TEXT, clock_in TEXT, clock_out TEXT, total_time TEXT, error_entry NUMERIC, updated NUMERIC, updated_by INT, update_date TEXT)""",
]


def install():
    with DBConn('sqlite') as conn:
        # Make Tables
        create_tables(conn)
        populate_employee_table(conn)

def create_tables(conn):
    c = conn.cursor()
    for query in table_queries:
        c.execute(query)
    conn.commit()

def populate_employee_table(sqlite_conn):
    with DBConn('sqlite') as conn:
        c = conn.cursor()
        c.execute("""DELETE FROM employee""")
        conn.commit()
    with DBConn('mysql') as conn:
        employees = Employee(db_type='mysql', is_active=True).select_query()
        for employee in employees:
            query = """INSERT INTO employee VALUES {} """.format(employee)
            print(query)
            c = sqlite_conn.cursor()
            c.execute(query)
        sqlite_conn.commit()

if __name__ == "__main__":
    if not os.path.exists('.//TimeClock.db'):
        install()
