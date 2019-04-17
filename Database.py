#! /usr/bin/python3
import datetime
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


class TimeEntries:

    table_name = "time_entries"

    def __init__(self,
                 id=None,
                 employee_id=None,
                 entry_date=None,
                 clock_in=None,
                 clock_out=None,
                 total_time=None,
                 error_entry=None,
                 updated=None):
        self.id = id
        self.employee_id    = employee_id
        self.entry_date     = entry_date
        self.clock_in       = clock_in
        self.clock_out      = clock_out
        self.total_time     = total_time
        self.error_entry    = error_entry
        self.updated        = updated

    def clock_in(self):
        # TODO: Check last action
        pass

def select_query_format(db_object, select_all=False):
    temp_param_dict = db_object.__dict__
    param_dict = {}
    for key in temp_param_dict.keys():
        if temp_param_dict[key] != "" and temp_param_dict[key] != None:
            param_dict[key] = temp_param_dict[key]
    filters = ""
    for key in param_dict.keys():
        if isinstance(param_dict[key], str):
            value = " = '{}'".format(param_dict[key])
        elif isinstance(param_dict[key], datetime.date):
            value = "='{}'".format(param_dict[key])
        elif isinstance(param_dict[key], datetime.datetime):
            value = "='{}'".format(param_dict[key])
        else:
            value = " = {}".format(param_dict[key])
        filters = filters + key + value + " AND "
    filters = filters[0:len(filters) - 4]
    return """SELECT * FROM {} WHERE {}""".format(db_object.table_name, filters)

def insert_query_format(db_object):
    """
    Formats an object's dictionary of instance variables and a table name into an SQL query
    :param db_object: Object, database model
    :param table_name: string
    :return: Syntactically correct SQL query string
    """
    temp_param_dict = db_object.__dict__
    print(temp_param_dict)
    param_dict = {}
    for key in temp_param_dict.keys():
        if temp_param_dict[key] != "" and temp_param_dict[key] != None:
            param_dict[key] = temp_param_dict[key]
    print(param_dict)
    fields = ""
    for key in param_dict.keys():
        fields = fields + key + ', '
    fields = fields[0:len(fields) - 2]
    values = ""
    for key in param_dict.keys():
        if isinstance(param_dict[key], str):
            value = "'{}'".format(param_dict[key])
        elif isinstance(param_dict[key], datetime.date):
            value = "'{}'".format(param_dict[key])
        elif isinstance(param_dict[key], datetime.datetime):
            value = "'{}'".format(param_dict[key])
        else:
            value = "{}".format(param_dict[key])
        values = values + value + ", "
    values = values[0:len(values) - 2]
    return """INSERT INTO {} ({}) VALUES ({})""".format(db_object.table_name, fields, values)

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