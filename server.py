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

    def retrieve_time_entries(self):
        time_entries = TimeEntries(db_type='sqlite', employee_id=self.data_dict['ID']).select_query()
        msg = pickle.dumps(time_entries)
        print(time_entries)
        self.request.sendall(msg)

    def update_time_entry(self):
        time_entry = self.data_dict['TimeEntry']
        time_entry.db_type = 'sqlite'
        time_entry.update()


def run_server():
    server = socketserver.TCPServer((HOST, PORT), TimeClockServer)
    server.serve_forever()

