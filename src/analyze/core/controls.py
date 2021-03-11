import tkinter as tk


class Control:

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, title: str):
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

    def add_checkbutton(self, title, tk_var: tk.BooleanVar, default_value: bool):
        tk_var.set(default_value)
        tk.Checkbutton(
            self.label_frame, text=title, variable=tk_var,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, padx=5, pady=3)
        self.row += 1

    def add_radiobutton(self, title, tk_var: tk.IntVar, value: int):
        tk.Radiobutton(
            self.label_frame, text=title, variable=tk_var, value=value,
            command=self.guru_parent_redraw).grid(column=0, row=self.row, padx=5, pady=3)
        self.row += 1

    def add_dropdown(self, title, tk_var: tk.StringVar, default_value: str, values: list[str], callback):
        assert default_value in values

        tk_var.set(default_value)
        tk.Label(self.label_frame, text=title).grid(column=0, row=self.row, pady=0, padx=5, sticky=tk.W)

        tk.OptionMenu(self.label_frame, tk_var, values[0], values[1], values[2],
                      command=callback).grid(column=0, row=self.row + 1, pady=1, padx=5, sticky=tk.W)
        self.row += 2

    # Abstract method for each control to provide
    def add_buttons(self):
        pass


class EpisodeCheckButtonControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_all = tk.BooleanVar()
        self._show_filtered = tk.BooleanVar()

        if include_evaluations:
            self._show_evaluations = tk.BooleanVar()
        else:
            self._show_evaluations = None

    def add_buttons(self):

        self.add_checkbutton("All", self._show_all, True)
        self.add_checkbutton("Filtered", self._show_filtered, False)

        if self._show_evaluations:
            self.add_checkbutton("Evaluations", self._show_evaluations, False)

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

        self._show_predictions = tk.BooleanVar()

    def add_buttons(self):

        self.add_checkbutton("Show Predictions", self._show_predictions, False)

    def show_predictions(self):
        return self._show_predictions.get()


class GraphFormatControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Format")

        self._swap_axes = tk.BooleanVar()
        self._show_trends = tk.BooleanVar()

    def add_buttons(self):

        self.add_checkbutton("Swap Axes", self._swap_axes, False)
        self.add_checkbutton("Show Trends", self._show_trends, False)

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


class ConvergenceGranularityControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Granularity")
        self._granularity = tk.IntVar(value=5)

    def add_buttons(self):
        self.add_radiobutton("3 cm", self._granularity, 3)
        self.add_radiobutton("5 cm", self._granularity, 5)
        self.add_radiobutton("10 cm", self._granularity, 10)
        self.add_radiobutton("20 cm", self._granularity, 20)

    def granularity(self):
        return self._granularity.get()


class SpeedControl(Control):

    _ACTION_SPEED = 1
    _TRACK_SPEED = 2
    _PROGRESS_SPEED = 3

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Speed")
        self._speed = tk.IntVar(value=SpeedControl._ACTION_SPEED)

    def add_buttons(self):
        self.add_radiobutton("Action", self._speed, SpeedControl._ACTION_SPEED)
        self.add_radiobutton("Track", self._speed, SpeedControl._TRACK_SPEED)
        self.add_radiobutton("Progress", self._speed, SpeedControl._PROGRESS_SPEED)

    def action_speed(self):
        return self._speed.get() == SpeedControl._ACTION_SPEED

    def track_speed(self):
        return self._speed.get() == SpeedControl._TRACK_SPEED

    def progress_speed(self):
        return self._speed.get() == SpeedControl._PROGRESS_SPEED


class TrackAppearanceOptions(Control):
    _BLOB_SIZE_SMALL = "Small     "
    _BLOB_SIZE_MEDIUM = "Medium    "
    _BLOB_SIZE_LARGE = "Large     "
    _BLOB_SIZES = [_BLOB_SIZE_SMALL, _BLOB_SIZE_MEDIUM, _BLOB_SIZE_LARGE]

    _PALETTE_MONO = "Mono      "
    _PALETTE_3_COLOURS = "3 Colours "
    _PALETTE_5_COLOURS = "5 Colours "
    _PALETTES = [_PALETTE_MONO, _PALETTE_3_COLOURS, _PALETTE_5_COLOURS]

    _BRIGHTNESS_NORMAL = "Normal    "
    _BRIGHTNESS_BRIGHT = "Bright    "
    _BRIGHTNESS_VERY_BRIGHT = "Very Bright"
    _BRIGHTNESSES = [_BRIGHTNESS_NORMAL, _BRIGHTNESS_BRIGHT, _BRIGHTNESS_VERY_BRIGHT]

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame,
                 blob_size_callback, palette_callback, brightness_callback):
        super().__init__(guru_parent_redraw, control_frame, "Appearance")

        self._blob_size = tk.StringVar()
        self._blob_size_callback = blob_size_callback

        self._palette = tk.StringVar()
        self._palette_callback = palette_callback

        self._brightness = tk.StringVar()
        self._brightness_callback = brightness_callback

    def add_buttons(self):
        if self._blob_size_callback:
            self.add_dropdown(
                "Blob Size", self._blob_size, TrackAppearanceOptions._BLOB_SIZE_MEDIUM,
                TrackAppearanceOptions._BLOB_SIZES, self._blob_size_callback)
        if self._palette_callback:
            self.add_dropdown(
                "Palette", self._palette, TrackAppearanceOptions._PALETTE_3_COLOURS,
                TrackAppearanceOptions._PALETTES, self._palette_callback)
        if self._brightness_callback:
            self.add_dropdown(
                "Brightness", self._brightness, TrackAppearanceOptions._BRIGHTNESS_NORMAL,
                TrackAppearanceOptions._BRIGHTNESSES, self._brightness_callback)

    def small_blob_size(self):
        return self._blob_size.get() == TrackAppearanceOptions._BLOB_SIZE_SMALL

    def medium_blob_size(self):
        return self._blob_size.get() == TrackAppearanceOptions._BLOB_SIZE_MEDIUM

    def large_blob_size(self):
        return self._blob_size.get() == TrackAppearanceOptions._BLOB_SIZE_LARGE

    def mono_palette(self):
        return self._palette.get() == TrackAppearanceOptions._PALETTE_MONO

    def three_colour_palette(self):
        return self._palette.get() == TrackAppearanceOptions._PALETTE_3_COLOURS

    def five_colour_palette(self):
        return self._palette.get() == TrackAppearanceOptions._PALETTE_5_COLOURS

    def normal_brightness(self):
        return self._brightness.get() == TrackAppearanceOptions._BRIGHTNESS_NORMAL

    def bright_brightness(self):
        return self._brightness.get() == TrackAppearanceOptions._BRIGHTNESS_BRIGHT

    def very_bright_brightness(self):
        return self._brightness.get() == TrackAppearanceOptions._BRIGHTNESS_VERY_BRIGHT


class SkipStartsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Skip")

        self._skip_starts = tk.BooleanVar()

    def add_buttons(self):
        self.add_checkbutton("Skip starts", self._skip_starts, True)

    def skip_starts(self):
        return self._skip_starts.get()


class StatsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Stats")

        self._show_mean = tk.BooleanVar()
        self._show_median = tk.BooleanVar()
        self._show_best = tk.BooleanVar()
        self._show_worst = tk.BooleanVar()

    def add_buttons(self):
        self.add_checkbutton("Mean", self._show_mean, True)
        self.add_checkbutton("Median", self._show_median, False)
        self.add_checkbutton("Best", self._show_best, False)
        self.add_checkbutton("Worst", self._show_worst, False)

    def show_mean(self):
        return self._show_mean.get()

    def show_median(self):
        return self._show_median.get()

    def show_best(self):
        return self._show_best.get()

    def show_worst(self):
        return self._show_worst.get()


class RoundingControl(Control):

    _ROUNDING_EXACT = 1
    _ROUNDING_INTEGER = 2

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Rounding")
        self._rounding = tk.IntVar(value=RoundingControl._ROUNDING_EXACT)

    def add_buttons(self):
        self.add_radiobutton("Exact", self._rounding, RoundingControl._ROUNDING_EXACT)
        self.add_radiobutton("Integer", self._rounding, RoundingControl._ROUNDING_INTEGER)

    def rounding_exact(self):
        return self._rounding.get() == RoundingControl._ROUNDING_EXACT

    def rounding_integer(self):
        return self._rounding.get() == RoundingControl._ROUNDING_INTEGER
