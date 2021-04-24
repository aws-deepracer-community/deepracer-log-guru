#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from tkinter import *
from re import fullmatch

# Simple base class for dialogues copied from:
#       https://effbot.org/tkinterbook/tkinter-dialog-windows.htm
#
# Now with added validation methods for text entry
#

class Dialog(Toplevel):

    def __init__(self, parent, title = None):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        # Register our own special validation options for text entry
        self.validate_waypoint_id = (self.register(on_validate_waypoint_id), '%P')
        self.validate_positive_integer = (self.register(on_validate_positive_integer), '%P')
        self.validate_whole_percent = (self.register(on_validate_whole_percent), '%P')
        self.validate_simple_float = (self.register(on_validate_simple_float), '%P')

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx() + 50,
                                  parent.winfo_rooty() + 50))

        self.initial_focus.focus_set()

        self.wait_window(self)


    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = Frame(self)

        w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return True # override

    def apply(self):

        pass # override


    #
    # Implement our own special validation options for text entry
    #

def on_validate_waypoint_id(new_value):
    return len(new_value) <= 3 and fullmatch('\d*', new_value) is not None

def on_validate_positive_integer(new_value):
    return len(new_value) <= 6 and fullmatch('[1-9]\d*', new_value) is not None or new_value == ""

def on_validate_whole_percent(new_value):
    return (len(new_value) <= 2 and fullmatch('\d*', new_value) is not None) or new_value == "100"

def on_validate_simple_float(new_value):
    return fullmatch('[-]{0,1}\d*[.]{0,1}\d*', new_value) is not None