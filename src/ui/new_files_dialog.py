#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import tkinter.messagebox

from src.ui.dialog import Dialog
from src.log.log_utils import import_new_logs, get_possible_new_model_log_files
from src.ui.please_wait import PleaseWait

class NewFilesDialog(Dialog):

    def __init__(self, parent, please_wait :PleaseWait):
        self.new_log_files = get_possible_new_model_log_files(parent.get_log_directory())
        self.please_wait = please_wait

        super().__init__(parent, "Import New Log Files")

    def body(self, master):

        if self.new_log_files:
            tk.Label(master, text="The following new log files were found:").pack(anchor=tk.W, pady=10)

            for f in self.new_log_files:
                tk.Label(master, text="        " + f).pack(anchor=tk.W, pady=2)

            tk.Label(master, text="Click OK to import them now").pack(anchor=tk.W, pady=10)
        else:
            tk.Label(master, text="No new log files were found").pack()

    def apply(self):
        import_new_logs(self.new_log_files, self.please_wait, self.parent.get_log_directory())
        self.please_wait.stop(0.2)
        tk.messagebox.showinfo("Fetch File", "Import succeeded")
