#! /usr/bin/python3
import datetime
from DBconn import DBConn


class Table:

    primary_key = "id"

    def load(self, record=None):
        if not record:
            result = self.select_query()
            result = result[0]
        else:
            result = record
        for number, key in enumerate(self.__dict__.keys()):
            item = result[number]
            if isinstance(item, str):
                if item.replace(" ", "") == "":
                    assign = "self.{} = None".format(key)
                else:
                    assign = "self.{} = \'\'\'{}\'\'\'".format(key, item)
            elif isinstance(item, datetime.datetime):
                assign = "self.{} = datetime.datetime.strptime(\'{}\', \'%Y-%m-%d %H:%M:%S\')".format(key, item)
            elif isinstance(item, datetime.date):
                assign = "self.{} = datetime.datetime.strptime(\'{}\', \'%Y-%m-%d\')".format(key, item)
            elif isinstance(item, datetime.timedelta):
                assign = "self.{} = datetime.timedelta({})".format(key, item.total_seconds())
            else:
                assign = "self.{} = {}".format(key, item)
            exec(assign)

    def update(self):
        self.commit_to_db(self.update_query_format())

    def insert(self):
        self.commit_to_db(self.insert_query_format())

    def delete(self):
        # TODO: Make this primary key, not id, run through quote check
        self.commit_to_db("""DELETE FROM {} WHERE id = {}""".format(self.table_name, self.id))

    def select_query_format(self, order_by=None, how="ASC"):
        param_dict = self.build_param_dict()
        # print(param_dict)
        if len(param_dict) > 0:
            filters = ""
            for key in param_dict.keys():
                value = param_dict[key]
                if isinstance(value, str) and value.replace(" ", "") == "NULL":
                    q_filter = "{} IS NULL AND ".format(key)
                elif isinstance(value, Between):
                    q_filter = "({} BETWEEN {} AND {}) AND ".format(key, value.start, value.end)
                else:
                    q_filter = "{} = {} AND ".format(key, self.quote_check(value))
                filters = filters + q_filter
            filters = filters[0:len(filters) - 4]
            if order_by:
                filters = "{} ORDER BY {} {}".format(filters, order_by, how)
            query_string = """SELECT * FROM {} WHERE {}""".format(self.table_name, filters)
        else:
            if order_by:
                table_name = "{} ORDER BY {} {}".format(self.table_name, order_by, how)
            else:
                table_name = self.table_name
            query_string = """SELECT * FROM {}""".format(table_name)
        return query_string

    def update_query_format(self):
        param_dict = self.build_param_dict()
        values = ""
        for key in param_dict.keys():
            if key != self.primary_key:
                value = self.quote_check(param_dict[key])
                values += " {} = {},".format(key, value)
        values = values[0:len(values) - 1]
        return "UPDATE {} SET {} WHERE {} = {}".format(self.table_name, values,
                                                       self.primary_key, self.quote_check(param_dict[self.primary_key]))

    def insert_query_format(self):
        """
        Formats an object's dictionary of instance variables and a table name into an SQL query
        :return: Syntactically correct SQL query string
        """
        param_dict = self.build_param_dict()
        fields = ""
        for key in param_dict.keys():
            fields = fields + key + ', '
        fields = fields[0:len(fields) - 2]
        values = ""
        for key in param_dict.keys():
            value = self.quote_check(param_dict[key])
            values = values + value + ", "
        values = values[0:len(values) - 2]

        return """INSERT INTO {} ({}) VALUES ({})""".format(self.table_name, fields, values)

    def select_query(self, order_by=None, how="ASC", limit=None):
        with DBConn() as conn:
            if not order_by:
                query = self.select_query_format()
            else:
                query= self.select_query_format(order_by=order_by, how=how)
            if limit:
                query = "{} LIMIT {}".format(query, limit)
            conn.query(query)
            result = conn.store_result()
            rows = self.aggregate_rows(result)
        return rows

    @staticmethod
    def commit_to_db(query):
        with DBConn() as conn:
            conn.query(query)
            conn.commit()

    def build_param_dict(self):
        param_dict = {}
        for key in self.__dict__.keys():
            if self.__dict__[key] != "" and self.__dict__[key] != None:
                param_dict[key] = self.__dict__[key]
        return param_dict

    @staticmethod
    def quote_check(data):
        if isinstance(data, str):
            if data.replace(" ", "") == "NULL":
                value = "NULL"
            else:
                value = "'{}'".format(data)
        elif isinstance(data, datetime.date):
            value = "'{}'".format(data)
        elif isinstance(data, datetime.datetime):
            value = "'{}'".format(data)
        elif isinstance(data, datetime.timedelta):
            value = "'{}'".format(data)
        else:
            value = "{}".format(data)
        return value

    @staticmethod
    def aggregate_rows(results):
        rows = []
        for i in range(0, results.num_rows()):
            temp = results.fetch_row()
            rows.append(temp[0])
        return rows


class Employee(Table):

    table_name = "employee"

    def __init__(self, id=None, first_name=None, last_name=None, preferred_name=None, pin=None, is_active=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_name = preferred_name
        self.pin = pin
        self.is_active = is_active
        if self.id is not None:
            self.load()


class TimeEntries(Table):

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
        if self.id is not None:
            self.load()


class Between:

    def __init__(self, start, end):
        self.start = Table.quote_check(start)
        self.end = Table.quote_check(end)


def between(start, end):
    r = Between(start, end)
    return r

