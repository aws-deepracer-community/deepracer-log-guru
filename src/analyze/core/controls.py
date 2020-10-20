import tkinter as tk

class Control:

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, title :str):
        self.guru_parent_redraw = guru_parent_redraw
        self.control_frame = control_frame
        self.title = title
        self.row = None
        self.label_frame = None

    def add_to_control_frame(self):
        self.label_frame = tk.LabelFrame(self.control_frame, text=self.title, padx=5, pady=5)
        self.row = 0
        self.add_buttons()
        self.label_frame.pack()

    def add_checkbutton(self, title, tk_var :tk.BooleanVar):
        tk.Checkbutton(
            self.label_frame, text=title, variable=tk_var,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, pady=5, padx=5)
        self.row += 1

    def add_radiobutton(self, title, tk_var :tk.IntVar, value :int):
        tk.Radiobutton(
            self.label_frame, text=title, variable=tk_var, value=value,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, pady=5, padx=5)
        self.row += 1

    ## Abstract method for each control to provide
    def add_buttons(self):
        pass


class EpisodeCheckButtonControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_all = tk.BooleanVar(value="True")
        self._show_filtered = tk.BooleanVar(value="False")

        if include_evaluations:
            self._show_evaluations = tk.BooleanVar(value="False")
        else:
            self._show_evaluations = None

    def add_buttons(self):

        self.add_checkbutton("All", self._show_all)
        self.add_checkbutton("Filtered", self._show_filtered)

        if self._show_evaluations:
            self.add_checkbutton("Evaluations", self._show_evaluations)

    def show_all(self):
        return self._show_all.get()

    def show_filtered(self):
        return self._show_filtered.get()

    def show_evaluations(self):
        return self._show_evaluations and self._show_evaluations.get()

class EpisodeRadioButtonControl(Control):

    SHOW_ALL = 1
    SHOW_FILTERED = 2
    SHOW_EVALUATIONS = 3


    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_what = tk.IntVar(value=EpisodeRadioButtonControl.SHOW_ALL)
        self.include_evaluations = include_evaluations


    def add_buttons(self):

        self.add_radiobutton("All", self._show_what, EpisodeRadioButtonControl.SHOW_ALL)
        self.add_radiobutton("Filtered", self._show_what, EpisodeRadioButtonControl.SHOW_FILTERED)

        if self.include_evaluations:
            self.add_radiobutton("Evaluations", self._show_what, EpisodeRadioButtonControl.SHOW_EVALUATIONS)

    def show_all(self):
        return self._show_what.get() == EpisodeRadioButtonControl.SHOW_ALL

    def show_filtered(self):
        return self._show_what.get() == EpisodeRadioButtonControl.SHOW_FILTERED

    def show_evaluations(self):
        return self._show_what.get() == EpisodeRadioButtonControl.SHOW_EVALUATIONS