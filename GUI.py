#! /usr/bin/python3

from tkinter import *
import logging
import hashlib
import Database
import os

class Controller:

    master = None
    frame = None

    def __init__(self, gui_root):
        Controller.master = gui_root
        Authenticate()



class Authenticate(Controller):

    def __init__(self):
        Controller.frame = LabelFrame(Controller.master, text="Enter Your Pin")
        Controller.frame.grid(row=0, column=0, padx=5, pady=20, sticky=NSEW)
        # Keypad Items
        self.pin = ""
        self.keypad_frame = Frame(Controller.frame)
        self.pin_var = StringVar()
        self.pin_entry = Entry(self.keypad_frame, textvariable=self.pin_var, show="*")
        self.make_keypad()
        self.keypad_frame.grid(row=0, column=0, padx=5, pady=5, sticky=NSEW)
        # User Menu Items
        self.user_list_frame = Frame(Controller.frame)
        self.employee_var = StringVar()
        self.user_listbox = Listbox(self.user_list_frame)
        self.build_user_list()


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
            employee = Database.Employee.load(self.employee_var.get())
            pin_hash = hashlib.sha256(self.pin.encode("utf-8")).hexdigest()
            if employee.pin == pin_hash:
                UserMenu()
            self.pin = ""
            self.pin_var.set(self.pin)
            pass
        else:
            self.pin = self.pin + entry
            self.pin_var.set(self.pin)

    def build_user_list(self):
        user_dict = Database.Employee.fetch_names_and_ids()
        for employee in user_dict.values():
            self.user_listbox.insert(END, employee)
        self.user_listbox.grid()

class UserMenu:

    def __init__(self):
        Controller.frame.destroy()
        Controller.frame = Frame(Controller.master)
        label = Label(Controller.frame, text="Test")
        Controller.frame.grid()
        label.grid()


LOG_FILENAME = "TimeClock.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
root = Tk()
root.title("Time Clock")
root.geometry("800x480")
app = Controller(root)
root.mainloop()
