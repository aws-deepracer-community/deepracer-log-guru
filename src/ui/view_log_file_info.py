#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from src.log.log import Log
from src.ui.dialog import Dialog


class ViewLogFileInfo(Dialog):

    def __init__(self, parent, log: Log):
        self.log = log

        super().__init__(parent, "Log File Information")

    def body(self, master):
        tk.Label(master, text="Unprocessed Log Text:").grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        tk.Label(master, text=self.log.get_log_file_name()).grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        tk.Label(master, text="Deep Racer Guru Meta:").grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)
        tk.Label(master, text=self.log.get_meta_file_name()).grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)



