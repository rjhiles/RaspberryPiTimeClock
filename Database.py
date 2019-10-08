#! /usr/bin/python3
import datetime
from DBconn import DBConn


class Table:

    primary_key = "id"
    # db_type = "mysql"

    def load(self, db_type, record=None):
        if not record:
            result = self.select_query(db_type)
            record = result[0]
        for key in record.keys():
            self.__setattr__(key, record[key])
        # for number, key in enumerate(self.__dict__.keys()):
        #     item = result[number]
        #     if isinstance(item, str):
        #         if item.replace(" ", "") == "":
        #             assign = "self.{} = None".format(key)
        #         else:
        #             assign = "self.{} = \'\'\'{}\'\'\'".format(key, item)
        #     elif isinstance(item, datetime.datetime):
        #         assign = "self.{} = datetime.datetime.strptime(\'{}\', \'%Y-%m-%d %H:%M:%S\')".format(key, item)
        #     elif isinstance(item, datetime.date):
        #         assign = "self.{} = datetime.datetime.strptime(\'{}\', \'%Y-%m-%d\').date()".format(key, item)
        #     elif isinstance(item, datetime.timedelta):
        #         assign = "self.{} = datetime.timedelta({})".format(key, item.total_seconds())
        #     else:
        #         assign = "self.{} = {}".format(key, item)
        #     exec(assign)

    def update(self, db_type):
        self.commit_to_db(db_type, self.update_query_format())

    def insert(self, db_type):
        self.commit_to_db(db_type, self.insert_query_format())

    def delete(self, db_type):
        # TODO: Make this primary key, not id, run through quote check
        self.commit_to_db(db_type, """DELETE FROM {} WHERE id = {}""".format(self.table_name, self.id))

    def select_query(self, db_type, order_by=None, how="ASC", limit=None):
        with DBConn(db_type) as conn:
            if not order_by:
                query = self.select_query_format()
            else:
                query = self.select_query_format(order_by=order_by, how=how)
            if limit:
                query = "{} LIMIT {}".format(query, limit)
            c = conn.cursor()
            c.execute(query)
            rows = c.fetchall()
            return rows

    @staticmethod
    def commit_to_db(db_type, query):
        with DBConn(db_type) as conn:
            c = conn.cursor()
            c.execute(query)
            conn.commit()

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

    def build_param_dict(self):
        param_dict = {}
        for key in self.__dict__.keys():
            if self.__dict__[key] != "" and self.__dict__[key]:
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


class Employee(Table):

    table_name = "employee"

    def __init__(self, id=None, first_name=None, last_name=None, preferred_name=None, pin=None, is_active=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.preferred_name = preferred_name
        self.pin = pin
        self.is_active = is_active


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
                 updated=None,
                 updated_by=None,
                 update_date=None):
        self.id = id
        self.employee_id = employee_id
        self.entry_date = entry_date
        self.clock_in = clock_in
        self.clock_out = clock_out
        self.total_time = total_time
        self.error_entry = error_entry
        self.updated = updated
        self.updated_by = updated_by
        self.update_date = update_date

    def compute_total_time(self):
        if self.clock_out and self.clock_in:
            self.total_time = self.clock_out - self.clock_in

    def to_datetime(self):
        if self.entry_date:
            self.entry_date = datetime.datetime.strptime(self.entry_date, '%Y-%m-%d').date()
        if self.update_date:
            self.update_date = datetime.datetime.strptime(self.update_date, '%Y-%m-%d').date()
        if self.clock_in:
            self.clock_in = datetime.datetime.strptime(self.clock_in.split(".")[0], '%Y-%m-%d %H:%M:%S')
        if self.clock_out:
            self.clock_out = datetime.datetime.strptime(self.clock_out.split(".")[0], '%Y-%m-%d %H:%M:%S')

    def to_string(self):
        if self.entry_date:
            self.entry_date = self.entry_date.__str__()
        if self.clock_in:
            self.clock_in = self.clock_in.__str__().split(".")[0]
        if self.clock_out:
            self.clock_out = self.clock_out.__str__().split(".")[0]
        if self.update_date:
            self.update_date = self.update_date.__str__()


class Notify(Table):

    table_name = "notify"

    def __init__(self, id=None, employee_id=None, missed_entry_date=None):
        self.id = id
        self.employee_id = employee_id
        self.missed_entry_date = missed_entry_date

    def to_datetime(self):
        if self.missed_entry_date:
            self.missed_entry_date = datetime.datetime.strptime(self.missed_entry_date, '%Y-%m-%d').date()

    def to_string(self):
        if self.missed_entry_date:
            self.missed_entry_date = self.missed_entry_date.__str__()


class Between:

    def __init__(self, start, end):
        self.start = Table.quote_check(start)
        self.end = Table.quote_check(end)


def between(start, end):
    r = Between(start, end)
    return r

