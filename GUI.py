#! /usr/bin/python3

from tkinter import *
import logging
import hashlib
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
            # Hash pin
            # .get() employee from dropdown var
            # Retrieve pin from db & compare
            self.pin = ""
            self.pin_var.set(self.pin)
            pass
        else:
            self.pin = self.pin + entry
            self.pin_var.set(self.pin)






LOG_FILENAME = "TimeClock.log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)
root = Tk()
root.title(os.environ["TIMECLOCK_NAME"])
root.geometry("800x480")
app = Controller(root)
root.mainloop()
