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

def aggregate_rows(results):
    rows= []
    for i in range(0, results.num_rows()):
        temp= results.fetch_row()
        rows.append(temp[0])
    return rows

def update_query_format(db_object):
    param_dict = build_param_dict(db_object.__dict__)
    values = ""
    for key in param_dict.keys():
        if key != "id":
            value = quote_check(param_dict[key])
            values += " {} = {},".format(key, value)
    values = values[0:len(values) - 1]
    return "UPDATE {} SET{} WHERE ID = {}".format(db_object.table_name, values, param_dict['id'])

def select_query_format(db_object):
    param_dict = build_param_dict(db_object.__dict__)
    filters = ""
    for key in param_dict.keys():
        value = quote_check(param_dict[key])
        filter = "{} = {} AND ".format(key, value)
        filters = filters + filter
    filters = filters[0:len(filters) - 4]
    return """SELECT * FROM {} WHERE {}""".format(db_object.table_name, filters)

def insert_query_format(db_object):
    """
    Formats an object's dictionary of instance variables and a table name into an SQL query
    :param db_object: Object, database model
    :param table_name: string
    :return: Syntactically correct SQL query string
    """
    param_dict = build_param_dict(db_object.__dict__)
    fields = ""
    for key in param_dict.keys():
        fields = fields + key + ', '
    fields = fields[0:len(fields) - 2]
    values = ""
    for key in param_dict.keys():
        value = quote_check(param_dict[key])
        values = values + value + ", "
    values = values[0:len(values) - 2]
    return """INSERT INTO {} ({}) VALUES ({})""".format(db_object.table_name, fields, values)

def quote_check(data):
    if isinstance(data, str):
        value = "'{}'".format(data)
    elif isinstance(data, datetime.date):
        value = "'{}'".format(data)
    elif isinstance(data, datetime.datetime):
        value = "'{}'".format(data)
    else:
        value = "{}".format(data)
    return value

def build_param_dict(dict):
    param_dict={}
    for key in dict.keys():
        if dict[key] != "" and dict[key] != None:
            param_dict[key] = dict[key]
    return param_dict


def select_query(query_string):
    with DBConn() as conn:
        conn.query(query_string)
        result = conn.store_result()
        rows = aggregate_rows(result)
    return rows

def commit_to_db(query):
    with DBConn() as conn:
        conn.query(query)
        conn.commit()