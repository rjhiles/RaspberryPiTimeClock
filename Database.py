#! /usr/bin/python3

from DBconn import DBConn

class Employee:

    table_name = "employee"

    def __init__(self, id=None, first_name=None, last_name=None, preferred_name=None, pin=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_name = preferred_name
        self.pin = pin

    def load(self):
        query = """SELECT * FROM employee WHERE id = {}""".format(self.id)
        result = select_query(query)
        self.id, self.first_name, self.last_name, self.preferred_name, self.pin = result[0]

    def update(self):
        query = """UPDATE employee SET first_name='{}', last_name='{}', preferred_name='{}', pin='{}' WHERE id ={}"""
        update_query(query.format(self.first_name, self.last_name, self.preferred_name, self.pin, self.id))

    @staticmethod
    def fetch_names_and_ids():
        """
        Returns a dictionary with ids and names, formats name as preferred first name and last name
        :return: dict: keys are id, values are names formatted for display
        """
        result = select_query("""SELECT id, preferred_name, last_name FROM employee""")
        employee_dict = {}
        for i in range(0, len(result)):
            row = result[i]
            key = row[0]
            value = row[1] + " " + row[2]
            employee_dict[key] = value
        return employee_dict

    @staticmethod
    def fetch_ids_and_names():
        """
        Retrieves employee names and ids, formats name as preferred first name and last name
        :return: dict: keys are names formatted for display, values are ids
        """
        result = select_query("""SELECT id, preferred_name, last_name FROM employee""")
        employee_dict = {}
        for i in range(0, len(result)):
            row = result[i]
            key = row[1] + " " + row[2]
            value = row[0]
            employee_dict[key] = value
        return employee_dict


def select_query(query_string):
    with DBConn() as conn:
        conn.query(query_string)
        result = conn.store_result()
        rows = aggregate_rows(result)
    return rows

def update_query(query_string):
    with DBConn() as conn:
        conn.query(query_string)
        conn.commit()

def aggregate_rows(results):
    rows= []
    for i in range(0, results.num_rows()):
        temp= results.fetch_row()
        rows.append(temp[0])
    return rows