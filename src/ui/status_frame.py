#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

class StatusFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        inner_frame = tk.Frame(self)
        inner_frame.pack()

        tk.Label(inner_frame, text="Model:", font=("", 12)).grid(column=0, row=0, sticky=tk.E)
        tk.Label(inner_frame, text="Filtered Episode(s):", font=("", 12)).grid(column=0, row=1, sticky=tk.E)

        self.model_label = tk.Label(inner_frame, text="None", font=("", 12))
        self.episodes_label = tk.Label(inner_frame, text="None", font=("", 12))

        self.model_label.grid(column=1, row=0, sticky=tk.W)
        self.episodes_label.grid(column=1, row=1, sticky=tk.W)

    def change_model_name(self, new_model_name):
        self.model_label.config(text=new_model_name)

    def change_episodes(self, count_all, count_filtered):
        self.episodes_label.config(text=str(round(count_filtered)) + " of " + str(round(count_all)))

    def reset(self):
        self.model_label.config(text="None")
        self.episodes_label.config(text="None")

