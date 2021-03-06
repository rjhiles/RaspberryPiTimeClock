#! /usr/bin/python3

import socketserver
import pickle
from Database import TimeEntries

HOST, PORT = "192.168.0.20", 9999


class TimeClockServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        self.data_dict = pickle.loads(self.data)
        if self.data_dict['Action'] == 'RETRIEVE':
            self.retrieve_time_entries()
        elif self.data_dict['Action'] == 'UPDATE':
            self.update_time_entry()
        elif self.data_dict['Action'] == 'NEW':
            self.add_time_entry()
        elif self.data_dict['Action'] == 'ALL RECORDS':
            self.all_records()

    def retrieve_time_entries(self):
        time_entries = TimeEntries(employee_id=self.data_dict['ID']).select_query(db_type='sqlite')
        msg = pickle.dumps(time_entries)
        self.request.sendall(msg)

    def update_time_entry(self):
        time_entry = self.data_dict['TimeEntry']
        time_entry.db_type = 'sqlite'
        time_entry.update()

    def add_time_entry(self):
        time_entry = self.data_dict['TimeEntry']
        time_entry.db_type = 'sqlite'
        time_entry.insert()

    def all_records(self):
        time_entries = TimeEntries().select_query('sqlite')
        msg = pickle.dumps(time_entries)
        self.request.sendall(msg)


def run_server():
    with socketserver.TCPServer((HOST, PORT), TimeClockServer) as server:
        server.allow_reuse_address = True
        server.serve_forever()
