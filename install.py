import os
from DBconn import DBConn
from Utils import update_employee_table



table_queries = [
    # Employee Table
    """CREATE TABLE employee(id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, preferred_name TEXT, pin TEXT, is_active NUMERIC)""",
    # Time Entries Table
    """CREATE TABLE time_entries(id INTEGER PRIMARY KEY, employee_id INT, entry_date TEXT, clock_in TEXT, clock_out TEXT, total_time TEXT, error_entry NUMERIC, updated NUMERIC, updated_by INT, update_date TEXT)""",
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
        """Entries:
            Do you want to set an email address to be notified when a clock error occurs
            If Yes:
                Notify email for employee clock entry errors   
            Missed clock out error message - "What message do you want to display to users when attempt to clock in and they forgot to clock out"
            Missed clock out after employee left 
            Missed Clock in when employee is clocking out for lunch or for the day
                
        """

if __name__ == "__main__":
    if not os.path.exists('.//TimeClock.db'):
        install()
