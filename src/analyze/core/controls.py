import tkinter as tk

class Control:

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, title :str):
        self.guru_parent_redraw = guru_parent_redraw
        self.control_frame = control_frame
        self.title = title
        self.row = None
        self.label_frame = None

    def add_to_control_frame(self):
        self.label_frame = tk.LabelFrame(self.control_frame, text=self.title, padx=5, pady=3)
        self.row = 0
        self.add_buttons()
        self.label_frame.pack()

    def add_checkbutton(self, title, tk_var :tk.BooleanVar):
        tk.Checkbutton(
            self.label_frame, text=title, variable=tk_var,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, padx=5, pady=3)
        self.row += 1

    def add_radiobutton(self, title, tk_var :tk.IntVar, value :int):
        tk.Radiobutton(
            self.label_frame, text=title, variable=tk_var, value=value,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, padx=5, pady=3)
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


class EpisodeAxisControl(Control):
    AXIS_TIME = 1
    AXIS_STEP = 2
    AXIS_PROGRESS = 3
    AXIS_DISTANCE = 4
    AXIS_LAP_POSITION = 5
    AXIS_WAYPOINT_ID = 6

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Axis")

        self._show_what = tk.IntVar(value=EpisodeAxisControl.AXIS_TIME)

    def add_buttons(self):
        self.add_radiobutton("Time", self._show_what, EpisodeAxisControl.AXIS_TIME)
        self.add_radiobutton("Step", self._show_what, EpisodeAxisControl.AXIS_STEP)
        self.add_radiobutton("Progress", self._show_what, EpisodeAxisControl.AXIS_PROGRESS)
        self.add_radiobutton("Distance", self._show_what, EpisodeAxisControl.AXIS_DISTANCE)
        self.add_radiobutton("Lap Position", self._show_what, EpisodeAxisControl.AXIS_LAP_POSITION)
        self.add_radiobutton("Waypoint Id", self._show_what, EpisodeAxisControl.AXIS_WAYPOINT_ID)

    def show_time(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_TIME

    def show_step(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_STEP

    def show_progress(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_PROGRESS

    def show_distance(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_DISTANCE

    def show_lap_position(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_LAP_POSITION

    def show_waypoint_id(self):
        return self._show_what.get() == EpisodeAxisControl.AXIS_WAYPOINT_ID



class PredictionsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Predictions")

        self._show_predictions = tk.BooleanVar(value="False")


    def add_buttons(self):

        self.add_checkbutton("Show Predictions", self._show_predictions)

    def show_predictions(self):
        return self._show_predictions.get()


class GraphFormatControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Format")

        self._swap_axes = tk.BooleanVar(value="False")
        self._show_trends = tk.BooleanVar(value="False")

    def add_buttons(self):

        self.add_checkbutton("Swap Axes", self._swap_axes)
        self.add_checkbutton("Show Trends", self._show_trends)

    def swap_axes(self):
        return self._swap_axes.get()

    def show_trends(self):
        return self._show_trends.get()


class EpisodeRouteColourSchemeControl(Control):

    SCHEME_REWARD = 1
    SCHEME_ACTION_SPEED = 2
    SCHEME_TRACK_SPEED = 3
    SCHEME_PROGRESS_SPEED = 4
    SCHEME_SMOOTHNESS = 5
    SCHEME_STEERING = 6
    SCHEME_SLIDE = 7
    SCHEME_PER_SECOND = 8
    SCHEME_NONE = 9

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Colour Scheme")
        self._colour_scheme = tk.IntVar(value=EpisodeRouteColourSchemeControl.SCHEME_NONE)

    def add_buttons(self):
        self.add_radiobutton("Reward", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_REWARD)
        self.add_radiobutton("Action Speed", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_ACTION_SPEED)
        self.add_radiobutton("Track Speed", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_TRACK_SPEED)
        self.add_radiobutton("Progress Speed", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_PROGRESS_SPEED)
        self.add_radiobutton("Smoothness", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_SMOOTHNESS)
        self.add_radiobutton("Steering", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_STEERING)
        self.add_radiobutton("Slide", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_SLIDE)
        self.add_radiobutton("Per Second", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_PER_SECOND)
        self.add_radiobutton("None", self._colour_scheme, EpisodeRouteColourSchemeControl.SCHEME_NONE)

    def scheme_reward(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_REWARD

    def scheme_action_speed(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_ACTION_SPEED

    def scheme_track_speed(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_TRACK_SPEED

    def scheme_progress_speed(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_PROGRESS_SPEED

    def scheme_smoothness(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_SMOOTHNESS

    def scheme_steering(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_STEERING

    def scheme_slide(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_SLIDE

    def scheme_per_second(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_PER_SECOND

    def scheme_none(self):
        return self._colour_scheme.get() == EpisodeRouteColourSchemeControl.SCHEME_NONE
