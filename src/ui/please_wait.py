from tkinter import *


class PleaseWaitDialog(Toplevel):

    def __init__(self, parent):

        Toplevel.__init__(self, parent)
        self.transient(parent)

        self.title("Please wait")

        self.parent = parent

        Label(self, text="PLEASE WAIT >>>", height=3).pack()

        self.grab_set()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

        # self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
        #                           parent.winfo_rooty()+50))

        self.update()

