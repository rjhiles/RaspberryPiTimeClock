import os
from DBconn import DBConn
from Utils import update_employee_table



table_queries = [
    # Employee Table
    """CREATE TABLE employee(id INT PRIMARY KEY, first_name TEXT, last_name TEXT, preferred_name TEXT, pin TEXT, is_active NUMERIC)""",
    # Time Entries Table
    """CREATE TABLE time_entries(id INT PRIMARY KEY, employee_id INT, entry_date TEXT, clock_in TEXT, clock_out TEXT, total_time TEXT, error_entry NUMERIC, updated NUMERIC, updated_by INT, update_date TEXT)""",
]


def install():
    create_tables()
    update_employee_table()

def create_tables():
    with DBConn('sqlite') as conn:
        c = conn.cursor()
        for query in table_queries:
            c.execute(query)
        conn.commit()

# TODO: add function for creating .ini file
def make_ini_file():
    pass
    # TODO: check if ini file exists:
        # TODO: create file collect entries

if __name__ == "__main__":
    if not os.path.exists('.//TimeClock.db'):
        install()
