#! /usr/bin/python3

from os import name as osname
from tkinter import *
import logging
import hashlib
from Database import *
from ctypes import cdll, byref, create_string_buffer
import time
import Utils



class Controller:

    master = None
    frame = None

    def __init__(self, gui_root):
        Controller.master = gui_root
        Utils.update_employee_table()
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
        self.user_listbox = Listbox(self.user_list_frame, font=("Calibri", 25))
        self.user_dict = {}
        self.build_user_list()
        self.user_list_frame.grid(row=0, column=1, padx=5, pady=5)
        # Clock
        self.clock_frame = Frame(Controller.frame)
        self.current_time = "{}:{}:{}".format(time.localtime().tm_hour, time.localtime().tm_min,time.localtime().tm_sec)
        self.clock_face = Label(self.clock_frame, text=self.current_time)
        self.clock_face.config(font=('TkDefaultFont', 35))
        self.clock_face.grid(row=0, column=0)
        self.clock_frame.grid(row=0, column=2, padx=5, pady=10, sticky=N)
        self.tick()

    def tick(self):
        self.current_time = "{}:{}:{}".format(time.localtime().tm_hour, time.localtime().tm_min,
                                              time.localtime().tm_sec)
        self.clock_face.configure(text=self.current_time)
        print(self.current_time)
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
                           width= 6,
                           command=lambda x=key: self.keypad_entries(x))
                b.grid(row=y + 3, column=x)
                b.config(font=("Calibri", 20))

    def keypad_entries(self, entry):
        if entry == 'Delete':
            if len(self.pin) > 0:
                self.pin = self.pin[0:len(self.pin) - 1]
                self.pin_var.set(self.pin)

        elif entry == 'Enter':
            employee = Employee(db_type='sqlite', id=self.user_dict[self.user_listbox.get(ACTIVE)])
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
        emp = Employee(db_type='sqlite')
        employees = emp.select_query()
        for employee in employees:
            emp.load(employee)
            emp_name = "{} {}".format(emp.preferred_name, emp.last_name)
            self.user_dict[emp_name] = emp.id
            self.user_listbox.insert(END, emp_name)
        scroll = Scrollbar(self.user_list_frame, width=60)
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
                          command=lambda x: TimeEntries.clock_in(employee.id))
        clock_out = Button(clock_frame,
                           text="Clock Out",
                           height=4,
                           width=25,
                           # TODO: Change this to a local method
                           command=lambda x: TimeEntries.clock_out(employee.id))
        exit = Button(clock_frame, text="Exit", height=4, width=25, command=Authenticate)
        clock_in.grid(row=0, padx=10, pady=5)
        clock_out.grid(row=1, padx=10, pady=5)
        exit.grid(row=2, padx=10,pady=5)

    def clock_in(self):
        # Check last entry
        db = TimeEntries(employee_id=self.employee, entry_date=datetime.date.today(), clock_out="NULL")
        open_entry = db.select_query()
        # if there is not an open entry;
        if len(open_entry) == 0:
            # post time entry
            db.clock_in = datetime.datetime.today()
            db.insert()


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
