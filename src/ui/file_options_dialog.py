#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import tkinter.messagebox as messagebox

from src.ui.dialog import Dialog


class FileOptionsDialog(Dialog):

    def __init__(self, parent):
        self._configManager = parent.get_config_manager()
        self._tk_calculate_new_reward = tk.BooleanVar(value=self._configManager.get_calculate_new_reward())
        self._tk_calculate_alternate_discount_factors = tk.BooleanVar(
            value=self._configManager.get_calculate_alternate_discount_factors())

        super().__init__(parent, "File Processing Options")

    def body(self, master):
        tk.Label(master, text="Select the following options to enable advanced analysis:").grid(
            column=0, row=0, pady=3, sticky="W")

        tk.Checkbutton(master, variable=self._tk_calculate_new_reward,
                       text="Calculate rewards using new reward function").grid(
            column=0, row=1, pady=3, sticky="W")

        tk.Checkbutton(master, variable=self._tk_calculate_alternate_discount_factors,
                       text="Calculate future rewards using alternate discount factors").grid(
            column=0, row=2, pady=3, sticky="W")

        tk.Label(master, text="Beware ... these options will increase the time taken to open a log file",
                 foreground="red").grid(
            column=0, row=3, pady=6, sticky="W")

    def apply(self):
        turned_on_some_analysis = False

        new_value = self._tk_calculate_new_reward.get()
        if new_value != self._configManager.get_calculate_new_reward():
            turned_on_some_analysis = turned_on_some_analysis or new_value
            self._configManager.set_calculate_new_reward(new_value)

        new_value = self._tk_calculate_alternate_discount_factors.get()
        if new_value != self._configManager.get_calculate_alternate_discount_factors():
            turned_on_some_analysis = turned_on_some_analysis or new_value
            self._configManager.set_calculate_alternate_discount_factors(new_value)

        self.parent.refresh_analysis_controls()

        if turned_on_some_analysis:
            messagebox.showinfo(title="Options Reminder", message="You now need to re-open a log file to perform new analysis")
            self.parent.close_file()

    def validate(self):
        return True
