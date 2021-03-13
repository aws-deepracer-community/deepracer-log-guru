#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from typing import Callable

import src.utils.abstract_method as abstract_method


class Control:

    def __init__(self, guru_parent_redraw: Callable, control_frame: tk.Frame, title: str):
        self._guru_parent_redraw = guru_parent_redraw
        self._control_frame = control_frame
        self._title = title
        self._row = None
        self._label_frame = None

    def add_to_control_frame(self):
        self._label_frame = tk.LabelFrame(self._control_frame, text=self._title)
        self._row = 0
        self.add_buttons()
        self._label_frame.pack(pady=4)

    def add_checkbutton(self, title: str, tk_var: tk.BooleanVar, default_value: bool):
        tk_var.set(default_value)
        tk.Checkbutton(
            self._label_frame, text=title, variable=tk_var,
            command=self._guru_parent_redraw).grid(column=0, row=self._row, padx=5, pady=1)
        self._row += 1

    def add_radiobutton(self, title: str, tk_var: tk.IntVar, value: int):
        tk.Radiobutton(
            self._label_frame, text=title, variable=tk_var, value=value,
            command=self._guru_parent_redraw).grid(column=0, row=self._row, padx=5, pady=1)
        self._row += 1

    def add_dropdown(self, title: str, tk_var: tk.StringVar, default_value: str, values: list[str], callback: Callable):
        assert default_value in values

        tk_var.set(default_value)
        tk.Label(self._label_frame, text=title).grid(column=0, row=self._row, pady=0, padx=5, sticky=tk.W)

        tk.OptionMenu(self._label_frame, tk_var, values[0], values[1], values[2],
                      command=callback).grid(column=0, row=self._row + 1, pady=1, padx=5, sticky=tk.W)
        self._row += 2

    # Abstract method for each control to provide
    def add_buttons(self):
        abstract_method.enforce()
