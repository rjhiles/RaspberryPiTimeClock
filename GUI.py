#! /usr/bin/python3

from os import name as osname, path
from tkinter import *
from tkinter import messagebox
import logging
import hashlib
from Database import *
from ctypes import cdll, byref, create_string_buffer
import time
import Utils
import configparser
import threading
import Daemon

if path.exists('config.ini'):
    config = configparser.ConfigParser()
    config.read("config.ini")


class Controller:

    master = None
    frame = None

    def __init__(self, gui_root):
        Controller.master = gui_root
        Utils.update_employee_table()
        thread = threading.Thread(target=Daemon.main_loop, daemon=True)
        thread.start()
        Authenticate()


class Authenticate(Controller):

    def __init__(self):
        if Controller.frame:
            Controller.frame.destroy()
        Controller.frame = Frame(Controller.master)
        Controller.frame.grid(row=0, column=0, padx=5, pady=20, sticky=NSEW)
        # Keypad Items
        self.pin = ""
        self.keypad_frame = LabelFrame(Controller.frame, text="Enter Your Pin")
        self.pin_var = StringVar()
        self.pin_entry = Entry(self.keypad_frame, textvariable=self.pin_var, show="*")
        self.make_keypad()
        self.keypad_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        # User Menu Items
        self.user_list_frame = Frame(Controller.frame)
        self.user_listbox = Listbox(self.user_list_frame, font=("Calibri", 20))
        self.user_dict = {}
        self.build_user_list()
        self.user_list_frame.grid(row=0, column=1, padx=5, pady=5)
        # Clock
        self.clock_frame = Frame(Controller.frame)
        self.current_time = "{}:{}:{}".format(time.localtime().tm_hour, time.localtime().tm_min,time.localtime().tm_sec)
        self.clock_face = Label(self.clock_frame, text=self.current_time)
        self.clock_face.config(font=('TkDefaultFont', 30))
        self.clock_face.grid(row=0, column=0)
        self.clock_frame.grid(row=0, column=2, padx=5, pady=10, sticky=N)
        self.tick()

    def double_digit(num):
        result = num
        if len(str(num)) < 2:
            result = '0{}'.format(num)
        return result

    def tick(self):
        self.current_time = "{}:{}:{}".format(double_digit(time.localtime().tm_hour), double_digit(time.localtime().tm_min),
                                              double_digit(time.localtime().tm_sec))
        self.clock_face.configure(text=self.current_time)
        self.clock_face.after(500, self.tick)

    def make_keypad(self):
        self.pin_entry.config(font=("Calibri", 15))
        self.pin_entry.grid(row=0, column=0, pady=10, columnspan=3)
        keys = [
            ['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9'],
            ['Delete', '0', 'Enter'], ]

        for y, row in enumerate(keys, 1):
            for x, key in enumerate(row):
                b = Button(self.keypad_frame,
                           text=key,
                           height=2,
                           width=4,
                           command=lambda z=key: self.keypad_entries(z))
                b.grid(row=y + 3, column=x)
                b.config(font=("Calibri", 20))

    def keypad_entries(self, entry):
        if entry == 'Delete':
            if len(self.pin) > 0:
                self.pin = self.pin[0:len(self.pin) - 1]
                self.pin_var.set(self.pin)

        elif entry == 'Enter':
            employee = Employee(id=self.user_dict[self.user_listbox.get(ACTIVE)])
            employee.load('sqlite')
            pin_hash = hashlib.sha256(self.pin.encode("utf-8")).hexdigest()
            if employee.pin == pin_hash:

                UserMenu(employee)
            self.pin = ""
            self.pin_var.set(self.pin)
            pass
        else:
            self.pin = self.pin + entry
            self.pin_var.set(self.pin)

    def build_user_list(self):
        emp = Employee()
        employees = emp.select_query('sqlite')
        for employee in employees:
            emp.load('sqlite', record=employee)
            emp_name = "{} {}".format(emp.preferred_name, emp.last_name)
            self.user_dict[emp_name] = emp.id
            self.user_listbox.insert(END, emp_name)
        scroll = Scrollbar(self.user_list_frame, width=50)
        scroll.config(command=self.user_listbox.yview())
        self.user_listbox.config(width=0, yscrollcommand=scroll.set)
        self.user_listbox.grid(row=0, column=0)
        scroll.grid(row=0, column=1,sticky=NS)



class UserMenu(Controller):

    def __init__(self, employee):
        self.employee = employee
        Controller.frame.destroy()
        Controller.frame = Frame(Controller.master)
        Controller.frame.grid()
        clock_frame = Frame(Controller.frame)
        clock_frame.grid(row=0, column=0)
        clock_in = Button(clock_frame,
                          text="Clock In",
                          height=4,
                          width=25,
                          # TODO: Change this to a local method
                          command=self.clock_in)
        clock_out = Button(clock_frame,
                           text="Clock Out",
                           height=4,
                           width=25,
                           # TODO: Change this to a local method
                           command=self.clock_out)
        exit = Button(clock_frame, text="Exit", height=4, width=25, command=Authenticate)
        clock_in.config(font=('TkDefaultFont', 15))
        clock_out.config(font=('TkDefaultFont', 15))
        exit.config(font=('TkDefaultFont', 15))
        clock_in.grid(row=0, padx=10, pady=5)
        clock_out.grid(row=1, padx=10, pady=5)
        exit.grid(row=2, padx=10,pady=5)
        self.check_user_notifications()

    def clock_in(self):
        # Check last entry
        entry_search = TimeEntries(employee_id=self.employee.id,
                                   entry_date=datetime.date.today(),
                                   clock_out='NULL',
                                   error_entry='NULL')
        entry_search.to_string()
        last_entry = entry_search.select_query('sqlite')
        if last_entry:
            entry = TimeEntries()
            entry.load('sqlite', record=last_entry[0])
            entry.error_entry = 1
            entry.update('sqlite')
            messagebox.showerror(title="ERROR", message=config['MESSAGES']['CLOCK_IN_AFTER_MISSED_CLOCK_OUT'])
            # TODO: Send alert email

        new_entry = TimeEntries(employee_id=self.employee.id,
                                entry_date=datetime.date.today(),
                                clock_in=datetime.datetime.today())
        new_entry.to_string()
        new_entry.insert('sqlite')
        Utils.timed_messagebox("Success", "You are clocked in!")
        Authenticate()

    def clock_out(self):
        # Check to see if there is an open time entry for this employee
        entry_search = TimeEntries(employee_id=self.employee.id,
                                   entry_date=datetime.date.today(),
                                   clock_out="NULL",
                                   error_entry="NULL")
        entry_search.to_string()
        last_entry = entry_search.select_query('sqlite')
        if len(last_entry) > 1:
            # The employee missed a previous clock out and hasn't been corrected this is caught by clock_in error check
            # Find the most recent time entry
            entry = TimeEntries()
            most_recent_open_entry = TimeEntries()
            most_recent_open_entry.load('sqlite', record=last_entry[0])
            most_recent_open_entry.to_datetime()
            for i in range(1, len(last_entry)):
                entry.load('sqlite', record=last_entry[i])
                entry.to_datetime()
                if entry.clock_in > most_recent_open_entry.clock_in:
                    most_recent_open_entry.to_string()
                    most_recent_open_entry.error_entry = 1
                    most_recent_open_entry.update('sqlite')
                    most_recent_open_entry.load(record=last_entry[i])
                    most_recent_open_entry.to_datetime()
            most_recent_open_entry.clock_out = datetime.datetime.today()
            most_recent_open_entry.to_string()
            most_recent_open_entry.update('sqlite')

        elif len(last_entry) == 1:
            # All is as expected add clock out entry
            entry = TimeEntries(id=last_entry[0]['id'])
            entry.to_datetime()
            entry.clock_out = datetime.datetime.today()
            entry.to_string()
            entry.update('sqlite')
        elif len(last_entry) == 0:
            # They missed a clock in
            messagebox.showerror(title='Erorr', message=config['MESSAGES']['MISSED_CLOCK_IN'])
            entry = TimeEntries(employee_id=self.employee.id,
                                entry_date=datetime.date.today(),
                                clock_out=datetime.datetime.today(),
                                error_entry=1,
                                )
            entry.to_string()
            entry.insert('sqlite')
        Utils.timed_messagebox('Success', 'You have successfully clocked out!')
        Authenticate()

    def check_user_notifications(self):
        notification = Notify(employee_id=self.employee.id).select_query('sqlite')
        if notification:
            messagebox.showerror(title="ERROR", message=config['MESSAGES']['MISSED_CLOCK_OUT_PREVIOUS_DAY'])
            notification_entry = Notify()
            notification_entry.load('sqlite', record=notification[0])
            notification_entry.delete('sqlite')


# change process name from just python to TimeClock so we can use a bash script to make sure it is still alive
if osname == "posix":
    procname = "TimeClock"
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(procname) +1)
    buff.value = procname.encode('utf-8')
    libc.prctl(15, byref(buff), 0, 0, 0)

LOG_FILENAME = "TimeClock.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
root = Tk()
root.title("Time Clock")
root.geometry("800x480")
app = Controller(root)
root.mainloop()
