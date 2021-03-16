#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from enum import IntEnum, auto

from src.analyze.core.control import Control


class EpisodeCheckButtonControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_all = tk.BooleanVar()
        self._show_filtered = tk.BooleanVar()

        if include_evaluations:
            self._show_evaluations = tk.BooleanVar()
        else:
            self._show_evaluations = None

    def _add_widgets(self):
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
    class _Values(IntEnum):
        SHOW_ALL = 1
        SHOW_FILTERED = 2
        SHOW_EVALUATIONS = 3

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_what = tk.IntVar(value=EpisodeRadioButtonControl._Values.SHOW_ALL.value)
        self.include_evaluations = include_evaluations

    def _add_widgets(self):
        self.add_radiobutton("All", self._show_what, EpisodeRadioButtonControl._Values.SHOW_ALL.value)
        self.add_radiobutton("Filtered", self._show_what, EpisodeRadioButtonControl._Values.SHOW_FILTERED.value)

        if self.include_evaluations:
            self.add_radiobutton("Evaluations", self._show_what, EpisodeRadioButtonControl._Values.SHOW_EVALUATIONS.value)

    def show_all(self):
        x = self._show_what.get()
        y = EpisodeRadioButtonControl._Values.SHOW_ALL
        return self._show_what.get() == EpisodeRadioButtonControl._Values.SHOW_ALL.value

    def show_filtered(self):
        return self._show_what.get() == EpisodeRadioButtonControl._Values.SHOW_FILTERED.value

    def show_evaluations(self):
        return self._show_what.get() == EpisodeRadioButtonControl._Values.SHOW_EVALUATIONS.value


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

    def _add_widgets(self):
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

    def _add_widgets(self):

        self.add_checkbutton("Show Predictions", self._show_predictions, False)

    def show_predictions(self):
        return self._show_predictions.get()


class GraphFormatControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Format")

        self._swap_axes = tk.BooleanVar()

    def _add_widgets(self):

        self.add_checkbutton("Swap Axes", self._swap_axes, False)

    def swap_axes(self):
        return self._swap_axes.get()


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

    def _add_widgets(self):
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

    def _add_widgets(self):
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

    def _add_widgets(self):
        self.add_radiobutton("Action", self._speed, SpeedControl._ACTION_SPEED)
        self.add_radiobutton("Track", self._speed, SpeedControl._TRACK_SPEED)
        self.add_radiobutton("Progress", self._speed, SpeedControl._PROGRESS_SPEED)

    def action_speed(self):
        return self._speed.get() == SpeedControl._ACTION_SPEED

    def track_speed(self):
        return self._speed.get() == SpeedControl._TRACK_SPEED

    def progress_speed(self):
        return self._speed.get() == SpeedControl._PROGRESS_SPEED


class TrackAppearanceControl(Control):
    _BLOB_SIZE_SMALL = "Small       "
    _BLOB_SIZE_MEDIUM = "Medium   "
    _BLOB_SIZE_LARGE = "Large       "
    _BLOB_SIZES = [_BLOB_SIZE_SMALL, _BLOB_SIZE_MEDIUM, _BLOB_SIZE_LARGE]

    _PALETTE_MONO = "Mono       "
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

    def _add_widgets(self):
        if self._blob_size_callback:
            self.add_dropdown(
                "Blob Size", self._blob_size, TrackAppearanceControl._BLOB_SIZE_MEDIUM,
                TrackAppearanceControl._BLOB_SIZES, self._blob_size_callback)
        if self._palette_callback:
            self.add_dropdown(
                "Palette", self._palette, TrackAppearanceControl._PALETTE_3_COLOURS,
                TrackAppearanceControl._PALETTES, self._palette_callback)
        if self._brightness_callback:
            self.add_dropdown(
                "Brightness", self._brightness, TrackAppearanceControl._BRIGHTNESS_NORMAL,
                TrackAppearanceControl._BRIGHTNESSES, self._brightness_callback)

    def small_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_SMALL

    def medium_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_MEDIUM

    def large_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_LARGE

    def mono_palette(self):
        return self._palette.get() == TrackAppearanceControl._PALETTE_MONO

    def three_colour_palette(self):
        return self._palette.get() == TrackAppearanceControl._PALETTE_3_COLOURS

    def five_colour_palette(self):
        return self._palette.get() == TrackAppearanceControl._PALETTE_5_COLOURS

    def normal_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_NORMAL

    def bright_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_BRIGHT

    def very_bright_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_VERY_BRIGHT


class AdvancedFiltersControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Advanced Filters")

        self._skip_starts = tk.BooleanVar()
        self._filter_actions = tk.BooleanVar()
        self._filter_sector = tk.BooleanVar()
        self._filter_section = tk.BooleanVar()

    def _add_widgets(self):
        self.add_checkbutton("Skip starts", self._skip_starts, True)
        self.add_checkbutton("Actions", self._filter_actions, False)
        self.add_checkbutton("Sector", self._filter_sector, False)
        self.add_checkbutton("Section", self._filter_section, False)

    def skip_starts(self):
        return self._skip_starts.get()

    def filter_actions(self):
        return self._filter_actions.get()

    def filter_sector(self):
        return self._filter_actions.get()

    def filter_section(self):
        return self._filter_actions.get()


class StatsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Stats")

        self._show_mean = tk.BooleanVar()
        self._show_median = tk.BooleanVar()
        self._show_best = tk.BooleanVar()
        self._show_worst = tk.BooleanVar()

    def _add_widgets(self):
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

    def _add_widgets(self):
        self.add_radiobutton("Exact", self._rounding, RoundingControl._ROUNDING_EXACT)
        self.add_radiobutton("Integer", self._rounding, RoundingControl._ROUNDING_INTEGER)

    def rounding_exact(self):
        return self._rounding.get() == RoundingControl._ROUNDING_EXACT

    def rounding_integer(self):
        return self._rounding.get() == RoundingControl._ROUNDING_INTEGER


class CorrelationControl(Control):
    _TOTAL_DISTANCE = 1
    _PEAK_TRACK_SPEED = 2
    _PEAK_PROGRESS_SPEED = 3
    _STARTING_POINT = 4
    _AVERAGE_REWARD = 5
    _TOTAL_REWARD = 6
    _FINAL_REWARD = 7
    _SMOOTHNESS = 8
    _TRAINING_ITERATION = 9
    _FLYING_START = 10
    _MAX_SLIDE = 11

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Correlate With")
        self._correlation = tk.IntVar(value=CorrelationControl._TOTAL_DISTANCE)

    def _add_widgets(self):
        self.add_radiobutton("Total Distance", self._correlation, CorrelationControl._TOTAL_DISTANCE)
        self.add_radiobutton("Peak Track Speed", self._correlation, CorrelationControl._PEAK_TRACK_SPEED)
        self.add_radiobutton("Peak Progress Speed", self._correlation, CorrelationControl._PEAK_PROGRESS_SPEED)
        self.add_radiobutton("Starting Point", self._correlation, CorrelationControl._STARTING_POINT)
        self.add_radiobutton("Average Reward", self._correlation, CorrelationControl._AVERAGE_REWARD)
        self.add_radiobutton("Total Reward", self._correlation, CorrelationControl._TOTAL_REWARD)
        self.add_radiobutton("Final Reward", self._correlation, CorrelationControl._FINAL_REWARD)
        self.add_radiobutton("Smoothness", self._correlation, CorrelationControl._SMOOTHNESS)
        self.add_radiobutton("Training Iteration", self._correlation, CorrelationControl._TRAINING_ITERATION)
        self.add_radiobutton("Flying Start", self._correlation, CorrelationControl._FLYING_START)
        self.add_radiobutton("Max Slide", self._correlation, CorrelationControl._MAX_SLIDE)

    def correlate_total_distance(self):
        return self._correlation.get() == CorrelationControl._TOTAL_DISTANCE

    def correlate_peak_track_speed(self):
        return self._correlation.get() == CorrelationControl._PEAK_TRACK_SPEED

    def correlate_peak_progress_speed(self):
        return self._correlation.get() == CorrelationControl._PEAK_PROGRESS_SPEED

    def correlate_starting_point(self):
        return self._correlation.get() == CorrelationControl._STARTING_POINT

    def correlate_average_reward(self):
        return self._correlation.get() == CorrelationControl._AVERAGE_REWARD

    def correlate_total_reward(self):
        return self._correlation.get() == CorrelationControl._TOTAL_REWARD

    def correlate_final_reward(self):
        return self._correlation.get() == CorrelationControl._FINAL_REWARD

    def correlate_smoothness(self):
        return self._correlation.get() == CorrelationControl._SMOOTHNESS

    def correlate_training_iteration(self):
        return self._correlation.get() == CorrelationControl._TRAINING_ITERATION

    def correlate_flying_start(self):
        return self._correlation.get() == CorrelationControl._FLYING_START

    def correlate_max_slide(self):
        return self._correlation.get() == CorrelationControl._MAX_SLIDE


class GraphScaleControl(Control):
    _FIXED_SCALE = 1
    _DYNAMIC_SCALE = 2

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Scale")

        self._scale = tk.IntVar(value=GraphScaleControl._FIXED_SCALE)

    def _add_widgets(self):

        self.add_radiobutton("Fixed", self._scale, GraphScaleControl._FIXED_SCALE)
        self.add_radiobutton("Dynamic", self._scale, GraphScaleControl._DYNAMIC_SCALE)

    def fixed_scale(self):
        return self._scale.get() == GraphScaleControl._FIXED_SCALE

    def dynamic_scale(self):
        return self._scale.get() == GraphScaleControl._DYNAMIC_SCALE


class GraphLineFittingControl(Control):
    _NONE = 1
    _LINEAR = 2
    _QUADRATIC = 3

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Line Fitting")

        self._smoothing = tk.IntVar(value=GraphLineFittingControl._NONE)

    def _add_widgets(self):
        self.add_radiobutton("None", self._smoothing, GraphLineFittingControl._NONE)
        self.add_radiobutton("Linear", self._smoothing, GraphLineFittingControl._LINEAR)
        self.add_radiobutton("Quadratic", self._smoothing, GraphLineFittingControl._QUADRATIC)

    def no_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._NONE

    def linear_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._LINEAR

    def quadratic_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._QUADRATIC
