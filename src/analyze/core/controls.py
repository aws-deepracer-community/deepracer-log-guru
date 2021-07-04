#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import math
import tkinter as tk
from enum import IntEnum

from src.analyze.core.control import Control
from src.configuration.config_manager import ConfigManager
from src.utils.colors import ColorPalette
from src.utils.discount_factors import discount_factors


class EpisodeCheckButtonControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Episodes")

        self._show_all = tk.BooleanVar(value=True)
        self._show_filtered = tk.BooleanVar(value=False)

        if include_evaluations:
            self._show_evaluations = tk.BooleanVar(value=False)
        else:
            self._show_evaluations = None

    def _add_widgets(self):
        self.add_checkbutton("All", self._show_all)
        self.add_checkbutton_right("Filtered", self._show_filtered)

        if self._show_evaluations:
            self.add_checkbutton_wide("Evaluations", self._show_evaluations)

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
        self.add_radiobutton_right("Filtered", self._show_what, EpisodeRadioButtonControl._Values.SHOW_FILTERED.value)

        if self.include_evaluations:
            self.add_radiobutton_wide("Evaluations", self._show_what, EpisodeRadioButtonControl._Values.SHOW_EVALUATIONS.value)

    def show_all(self):
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

        self._show_predictions = tk.BooleanVar(value=False)

    def _add_widgets(self):

        self.add_checkbutton("Show Predictions", self._show_predictions)

    def show_predictions(self):
        return self._show_predictions.get()


class GraphFormatControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Format")

        self._swap_axes = tk.BooleanVar(value=False)

    def _add_widgets(self):

        self.add_checkbutton("Swap Axes", self._swap_axes)

    def swap_axes(self):
        return self._swap_axes.get()


class MeasurementControl(Control):
    _VISITS = "Visits"
    _EVENT_REWARD = "Event Reward"
    _FUTURE_REWARD = "Future Reward"
    _NEW_EVENT_REWARD = "New Event Reward"
    _NEW_FUTURE_REWARD = "New Future Reward"
    _ACTION_SPEED = "Action Speed"
    _TRACK_SPEED = "Track Speed"
    _PROGRESS_SPEED = "Progress Speed"
    _ACCELERATION = "Acceleration"
    _BRAKING = "Braking"
    _SMOOTHNESS = "Smoothness"
    _STEERING_STRAIGHT = "Steering Straight"
    _STEERING_LEFT = "Steering Left"
    _STEERING_RIGHT = "Steering Right"
    _SKEW = "Skew"
    _SLIDE = "Slide"
    _PROJECTED_TRAVEL_DISTANCE = "Projected Travel"
    _SECONDS = "Seconds"
    _OTHER = "Other:"
    _ALTERNATE_DISCOUNT_FACTOR = "Future DF = "

    _ALL_MEASUREMENTS_EXCEPT_SECONDS = [
        _VISITS, _EVENT_REWARD, _FUTURE_REWARD, _NEW_EVENT_REWARD, _NEW_FUTURE_REWARD, _ACTION_SPEED, _TRACK_SPEED,
        _PROGRESS_SPEED, _ACCELERATION, _BRAKING, _SMOOTHNESS, _STEERING_STRAIGHT, _STEERING_LEFT,
        _STEERING_RIGHT, _SKEW, _SLIDE, _PROJECTED_TRAVEL_DISTANCE
                                        ]

    def __init__(self, redraw_callback: callable, control_frame: tk.Frame, measure_seconds: bool,
                 config_manager: ConfigManager):
        super().__init__(redraw_callback, control_frame, "Measure")
        self._current_measurement_button = tk.StringVar(value=MeasurementControl._VISITS)
        self._current_measurement_dropdown = tk.StringVar()
        self._show_measure_seconds = measure_seconds
        self._redraw_callback = redraw_callback
        self._alternate_discount_factor_dict = dict()
        self._config_manager = config_manager

    def _add_widgets(self):
        self.add_radiobutton_improved(MeasurementControl._VISITS, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._EVENT_REWARD, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._FUTURE_REWARD, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._ACTION_SPEED, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._TRACK_SPEED, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._SMOOTHNESS, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._SLIDE, self._current_measurement_button)
        self.add_radiobutton_improved(MeasurementControl._OTHER, self._current_measurement_button)

        all_measurements = MeasurementControl._ALL_MEASUREMENTS_EXCEPT_SECONDS.copy()
        if self._show_measure_seconds:
            all_measurements.append(MeasurementControl._SECONDS)
        if not self._config_manager.get_calculate_new_reward():
            all_measurements.remove(MeasurementControl._NEW_EVENT_REWARD)
            all_measurements.remove(MeasurementControl._NEW_FUTURE_REWARD)

        if self._config_manager.get_calculate_alternate_discount_factors():
            self._alternate_discount_factor_dict = dict()
            for i in range(0, discount_factors.get_number_of_discount_factors()):
                name = MeasurementControl._ALTERNATE_DISCOUNT_FACTOR + str(discount_factors.get_discount_factor(i))
                self._alternate_discount_factor_dict[name] = i
                if i > 0:
                    all_measurements.append(name)

        if self._current_measurement_dropdown.get() not in all_measurements:
            self._current_measurement_dropdown.set("")

        self.add_dropdown(
            "", self._current_measurement_dropdown,
            all_measurements, self._dropdown_callback)

    def _dropdown_callback(self, value):
        if self._current_measurement_button.get() == MeasurementControl._OTHER:
            self._redraw_callback(value)

    def _check_if_measurement(self, required_value):
        return self._current_measurement_button.get() == required_value or (
                self._current_measurement_button.get() == MeasurementControl._OTHER and
                self._current_measurement_dropdown.get() == required_value
        )

    def measure_event_reward(self):
        return self._check_if_measurement(MeasurementControl._EVENT_REWARD)

    def measure_new_event_reward(self):
        return self._check_if_measurement(MeasurementControl._NEW_EVENT_REWARD)

    def measure_discounted_future_reward(self):
        return self._check_if_measurement(MeasurementControl._FUTURE_REWARD)

    def measure_new_discounted_future_reward(self):
        return self._check_if_measurement(MeasurementControl._NEW_FUTURE_REWARD)

    def measure_action_speed(self):
        return self._check_if_measurement(MeasurementControl._ACTION_SPEED)

    def measure_track_speed(self):
        return self._check_if_measurement(MeasurementControl._TRACK_SPEED)

    def measure_progress_speed(self):
        return self._check_if_measurement(MeasurementControl._PROGRESS_SPEED)

    def measure_smoothness(self):
        return self._check_if_measurement(MeasurementControl._SMOOTHNESS)

    def measure_steering_straight(self):
        return self._check_if_measurement(MeasurementControl._STEERING_STRAIGHT)

    def measure_steering_left(self):
        return self._check_if_measurement(MeasurementControl._STEERING_LEFT)

    def measure_steering_right(self):
        return self._check_if_measurement(MeasurementControl._STEERING_RIGHT)

    def measure_slide(self):
        return self._check_if_measurement(MeasurementControl._SLIDE)

    def measure_skew(self):
        return self._check_if_measurement(MeasurementControl._SKEW)

    def measure_seconds(self):
        return self._check_if_measurement(MeasurementControl._SECONDS)

    def measure_visits(self):
        return self._check_if_measurement(MeasurementControl._VISITS)

    def measure_acceleration(self):
        return self._check_if_measurement(MeasurementControl._ACCELERATION)

    def measure_braking(self):
        return self._check_if_measurement(MeasurementControl._BRAKING)

    def measure_projected_travel_distance(self):
        return self._check_if_measurement(MeasurementControl._PROJECTED_TRAVEL_DISTANCE)

    def get_alternate_discount_factor_index(self):
        if self._current_measurement_button.get() == MeasurementControl._OTHER:
            choice = self._current_measurement_dropdown.get()
        else:
            choice = self._current_measurement_button.get()
        if choice.startswith(MeasurementControl._ALTERNATE_DISCOUNT_FACTOR):
            return self._alternate_discount_factor_dict[choice]
        else:
            return None


class ConvergenceGranularityControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Granularity")
        self._granularity = tk.IntVar(value=5)

    def _add_widgets(self):
        self.add_radiobutton("3 cm", self._granularity, 3)
        self.add_radiobutton("5 cm", self._granularity, 5)
        self.add_radiobutton_right("10 cm", self._granularity, 10)
        self.add_radiobutton_right("20 cm", self._granularity, 20)

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
    _BLOB_SIZE_SMALL = "Small            "
    _BLOB_SIZE_SMALL_PLUS_SIDES = "Small + Sides"
    _BLOB_SIZE_MEDIUM = "Medium       "
    _BLOB_SIZE_LARGE = "Large            "
    _BLOB_SIZES = [_BLOB_SIZE_SMALL, _BLOB_SIZE_SMALL_PLUS_SIDES, _BLOB_SIZE_MEDIUM, _BLOB_SIZE_LARGE]

    _PALETTE_GREYS = "Greys        "
    _PALETTE_3_COLOURS = "3 Colours "
    _PALETTE_5_COLOURS = "5 Colours "
    _PALETTE_MULTI_A = "Multi-A    "
    _PALETTE_MULTI_B = "Multi-B    "
    _PALETTES = [_PALETTE_GREYS, _PALETTE_3_COLOURS, _PALETTE_5_COLOURS, _PALETTE_MULTI_A, _PALETTE_MULTI_B]

    _BRIGHTNESS_FAINT = "Faint      "
    _BRIGHTNESS_NORMAL = "Normal    "
    _BRIGHTNESS_BRIGHT = "Bright    "
    _BRIGHTNESS_VERY_BRIGHT = "Very Bright"
    _BRIGHTNESSES = [_BRIGHTNESS_FAINT, _BRIGHTNESS_NORMAL, _BRIGHTNESS_BRIGHT, _BRIGHTNESS_VERY_BRIGHT]

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame,
                 blob_size_callback, palette_callback, brightness_callback):
        super().__init__(guru_parent_redraw, control_frame, "Appearance")

        self._blob_size = tk.StringVar(value=TrackAppearanceControl._BLOB_SIZE_MEDIUM)
        self._blob_size_callback = blob_size_callback

        self._palette = tk.StringVar(value=TrackAppearanceControl._PALETTE_MULTI_A)
        self._palette_callback = palette_callback

        self._brightness = tk.StringVar(value=TrackAppearanceControl._BRIGHTNESS_NORMAL)
        self._brightness_callback = brightness_callback

    def _add_widgets(self):
        if self._blob_size_callback:
            self.add_dropdown(
                "Blob Size", self._blob_size,
                TrackAppearanceControl._BLOB_SIZES, self._blob_size_callback)
        if self._palette_callback:
            self.add_dropdown(
                "Palette", self._palette,
                TrackAppearanceControl._PALETTES, self._palette_callback)
        if self._brightness_callback:
            self.add_dropdown(
                "Brightness", self._brightness,
                TrackAppearanceControl._BRIGHTNESSES, self._brightness_callback)

    def small_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_SMALL

    def small_blob_plus_sides(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_SMALL_PLUS_SIDES

    def medium_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_MEDIUM

    def large_blob_size(self):
        return self._blob_size.get() == TrackAppearanceControl._BLOB_SIZE_LARGE

    def get_chosen_color_palette(self) -> ColorPalette:
        choice = self._palette.get()
        if choice == TrackAppearanceControl._PALETTE_GREYS:
            return ColorPalette.GREYS
        if choice == TrackAppearanceControl._PALETTE_3_COLOURS:
            return ColorPalette.DISCRETE_THREE
        if choice == TrackAppearanceControl._PALETTE_5_COLOURS:
            return ColorPalette.DISCRETE_FIVE
        if choice == TrackAppearanceControl._PALETTE_MULTI_A:
            return ColorPalette.MULTI_COLOR_A
        if choice == TrackAppearanceControl._PALETTE_MULTI_B:
            return ColorPalette.MULTI_COLOR_B

    def faint_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_FAINT

    def normal_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_NORMAL

    def bright_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_BRIGHT

    def very_bright_brightness(self):
        return self._brightness.get() == TrackAppearanceControl._BRIGHTNESS_VERY_BRIGHT

class SkipControl(Control):
    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Skip")

        self._skip_starts = tk.BooleanVar(value=True)
        self._skip_bad_ends = tk.BooleanVar(value=True)

    def _add_widgets(self):
        self.add_checkbutton("Starts", self._skip_starts)
        self.add_checkbutton_right("Ends", self._skip_bad_ends)

    def skip_starts(self):
        return self._skip_starts.get()

    def skip_ends(self):
        return self._skip_bad_ends.get()


class MoreFiltersControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, actions_only: bool):
        super().__init__(guru_parent_redraw, control_frame, "More Filters")

        self._actions_only = actions_only
        self._filter_actions = tk.BooleanVar(value=False)
        self._filter_sector = tk.BooleanVar(value=False)
        self._filter_section = tk.BooleanVar(value=False)

    def _add_widgets(self):
        self.add_checkbutton("Actions", self._filter_actions)
        if not self._actions_only:
            self.add_checkbutton("Sector", self._filter_sector)

    def filter_actions(self):
        return self._filter_actions.get()

    def filter_sector(self):
        return self._filter_sector.get()

class StatsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Stats")

        self._show_mean = tk.BooleanVar(value=True)
        self._show_median = tk.BooleanVar(value=False)
        self._show_best = tk.BooleanVar(value=False)
        self._show_worst = tk.BooleanVar(value=False)

    def _add_widgets(self):
        self.add_checkbutton("Mean", self._show_mean)
        self.add_checkbutton_right("Best", self._show_best)
        self.add_checkbutton("Median", self._show_median)
        self.add_checkbutton_right("Worst", self._show_worst)

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
    _COMPLETE_LAP_TIME = 12

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, is_for_whole_laps: bool):
        super().__init__(guru_parent_redraw, control_frame, "Correlate With")
        self._correlation = tk.IntVar(value=CorrelationControl._TOTAL_DISTANCE)
        self._is_for_whole_laps = is_for_whole_laps

    def _add_widgets(self):
        self.add_radiobutton("Total Distance", self._correlation, CorrelationControl._TOTAL_DISTANCE)
        self.add_radiobutton("Peak Track Speed", self._correlation, CorrelationControl._PEAK_TRACK_SPEED)
        self.add_radiobutton("Peak Progress Speed", self._correlation, CorrelationControl._PEAK_PROGRESS_SPEED)
        self.add_radiobutton("Average Reward", self._correlation, CorrelationControl._AVERAGE_REWARD)
        self.add_radiobutton("Total Reward", self._correlation, CorrelationControl._TOTAL_REWARD)
        if self._is_for_whole_laps:
            self.add_radiobutton("Final Reward", self._correlation, CorrelationControl._FINAL_REWARD)
        self.add_radiobutton("Smoothness", self._correlation, CorrelationControl._SMOOTHNESS)
        self.add_radiobutton("Training Iteration", self._correlation, CorrelationControl._TRAINING_ITERATION)
        self.add_radiobutton("Max Slide", self._correlation, CorrelationControl._MAX_SLIDE)
        if self._is_for_whole_laps:
            self.add_radiobutton("Flying Start", self._correlation, CorrelationControl._FLYING_START)
            self.add_radiobutton("Starting Point", self._correlation, CorrelationControl._STARTING_POINT)
        else:
            self.add_radiobutton("Complete Lap Time", self._correlation, CorrelationControl._COMPLETE_LAP_TIME)

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

    def correlate_complete_lap_time(self):
        return self._correlation.get() == CorrelationControl._COMPLETE_LAP_TIME


class GraphScaleControl(Control):
    _FIXED_SCALE = 1
    _DYNAMIC_SCALE = 2

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Scale")

        self._scale = tk.IntVar(value=GraphScaleControl._FIXED_SCALE)

    def _add_widgets(self):

        self.add_radiobutton("Fixed", self._scale, GraphScaleControl._FIXED_SCALE)
        self.add_radiobutton_right("Dynamic", self._scale, GraphScaleControl._DYNAMIC_SCALE)

    def fixed_scale(self):
        return self._scale.get() == GraphScaleControl._FIXED_SCALE

    def dynamic_scale(self):
        return self._scale.get() == GraphScaleControl._DYNAMIC_SCALE


class GraphLineFittingControl(Control):
    _NONE = 1
    _JOINED = 2
    _LINEAR = 3
    _QUADRATIC = 4
    _CUBIC = 5

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, is_correlation: bool = True):
        super().__init__(guru_parent_redraw, control_frame, "Line Fitting")

        self._is_correlation = is_correlation
        self._smoothing = tk.IntVar(value=GraphLineFittingControl._NONE)
        self._show_scatter = tk.BooleanVar(value=True)
        if not is_correlation:
            self._smoothing.set(value=GraphLineFittingControl._JOINED)
            self._show_scatter.set(False)

    def _add_widgets(self):
        self.add_radiobutton("None", self._smoothing, GraphLineFittingControl._NONE)
        if not self._is_correlation:
            self.add_radiobutton("Joined", self._smoothing, GraphLineFittingControl._JOINED)
        self.add_radiobutton("Linear", self._smoothing, GraphLineFittingControl._LINEAR)
        self.add_radiobutton("Quadratic", self._smoothing, GraphLineFittingControl._QUADRATIC)
        self.add_radiobutton("Cubic", self._smoothing, GraphLineFittingControl._CUBIC)
        self.add_checkbutton("+ Scatter", self._show_scatter)

    def no_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._NONE

    def joined_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._JOINED

    def linear_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._LINEAR

    def quadratic_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._QUADRATIC

    def cubic_fitting(self):
        return self._smoothing.get() == GraphLineFittingControl._CUBIC

    def show_scatter(self):
        return self._show_scatter.get()


class ActionGroupControl(Control):
    _NONE = 1
    _SPEED = 2
    _STEERING = 3

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Group By")

        self._group = tk.IntVar(value=ActionGroupControl._NONE)

    def _add_widgets(self):
        self.add_radiobutton("None", self._group, ActionGroupControl._NONE)
        self.add_radiobutton("Speed", self._group, ActionGroupControl._SPEED)
        self.add_radiobutton("Steering", self._group, ActionGroupControl._STEERING)

    def no_grouping(self):
        return self._group.get() == ActionGroupControl._NONE

    def group_by_speed(self):
        return self._group.get() == ActionGroupControl._SPEED

    def group_by_steering(self):
        return self._group.get() == ActionGroupControl._STEERING


class EpisodeRewardTypeControl(Control):
    _REWARD_PLUS_TOTAL = "Reward + Total"
    _REWARD_PLUS_FUTURE = "Reward + Future"
    _NEW_REWARD_PLUS_TOTAL = "New Reward + Total"
    _NEW_REWARD_PLUS_FUTURE = "New Reward + Future"
    _ALL_DISCOUNT_FACTORS = "All Discount Factors"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, config_manager: ConfigManager):
        super().__init__(guru_parent_redraw, control_frame, "Reward Types")

        self._reward_type = tk.StringVar(value=EpisodeRewardTypeControl._REWARD_PLUS_TOTAL)
        self._config_manager = config_manager

    def _add_widgets(self):
        self.add_radiobutton_improved(EpisodeRewardTypeControl._REWARD_PLUS_TOTAL, self._reward_type)
        self.add_radiobutton_improved(EpisodeRewardTypeControl._REWARD_PLUS_FUTURE, self._reward_type)

        if self._config_manager.get_calculate_new_reward():
            self.add_radiobutton_improved(EpisodeRewardTypeControl._NEW_REWARD_PLUS_TOTAL, self._reward_type)
            self.add_radiobutton_improved(EpisodeRewardTypeControl._NEW_REWARD_PLUS_FUTURE, self._reward_type)
        elif self._reward_type.get() in [EpisodeRewardTypeControl._NEW_REWARD_PLUS_TOTAL, EpisodeRewardTypeControl._NEW_REWARD_PLUS_FUTURE]:
            self._reward_type.set(EpisodeRewardTypeControl._REWARD_PLUS_TOTAL)

        if self._config_manager.get_calculate_alternate_discount_factors():
            self.add_radiobutton_improved(EpisodeRewardTypeControl._ALL_DISCOUNT_FACTORS, self._reward_type)
        elif self._reward_type.get() == EpisodeRewardTypeControl._ALL_DISCOUNT_FACTORS:
            self._reward_type.set(EpisodeRewardTypeControl._REWARD_PLUS_TOTAL)

    def show_reward_plus_total(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._REWARD_PLUS_TOTAL

    def show_reward_plus_future(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._REWARD_PLUS_FUTURE

    def show_new_reward_plus_total(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._NEW_REWARD_PLUS_TOTAL

    def show_new_reward_plus_future(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._NEW_REWARD_PLUS_FUTURE

    def show_all_discount_factors(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._ALL_DISCOUNT_FACTORS


class VideoControls(Control):
    RESET = "Reset"
    PLAY = "Play"
    STOP = "Stop"

    def __init__(self, parent_callback: callable, control_frame: tk.Frame):
        super().__init__(parent_callback, control_frame, "Play")

    def _add_widgets(self):
        self.add_horizontal_push_button(VideoControls.RESET, self.callback_reset)
        self.add_horizontal_push_button(VideoControls.PLAY, self.callback_play)
        self.add_horizontal_push_button(VideoControls.STOP, self.callback_stop)

    def callback_reset(self):
        self._guru_parent_redraw(VideoControls.RESET)

    def callback_play(self):
        self._guru_parent_redraw(VideoControls.PLAY)

    def callback_stop(self):
        self._guru_parent_redraw(VideoControls.STOP)


class LapTimeControl(Control):

    def __init__(self, control_frame: tk.Frame):
        super().__init__(self.no_callback, control_frame, "Time")

        self._minutes = tk.IntVar(value=0)
        self._seconds = tk.IntVar(value=0)
        self._milliseconds = tk.IntVar(value=0)

    def _add_widgets(self):
        tk.Label(self._label_frame, textvariable=self._minutes).grid(column=0, row=0, pady=0, padx=5, sticky=tk.W)
        tk.Label(self._label_frame, text=":").grid(column=1, row=0, pady=0, padx=5, sticky=tk.W)
        tk.Label(self._label_frame, textvariable=self._seconds).grid(column=2, row=0, pady=0, padx=5, sticky=tk.W)
        tk.Label(self._label_frame, text=":").grid(column=3, row=0, pady=0, padx=5, sticky=tk.W)
        tk.Label(self._label_frame, textvariable=self._milliseconds).grid(column=4, row=0, pady=0, padx=5, sticky=tk.W)

    def no_callback(self):
        pass

    def show_time(self, seconds: float):
        whole_seconds = math.floor(seconds)
        whole_minutes = math.floor(seconds / 60)
        milliseconds = int(1000 * (seconds - whole_seconds))

        self._minutes.set(whole_minutes)
        self._seconds.set(("0" + str(whole_seconds))[-2:])
        self._milliseconds.set((str(milliseconds) + "000")[:3])


class DiscountFactorAnalysisControl(Control):
    _FUTURE_WEIGHTS = "Future Weights"
    _REMAINING_STEPS = "Remaining Steps"
    _BONUS_10 = "Final Bonus 10"
    _BONUS_100 = "Final Bonus 100"
    _BONUS_1000 = "Final Bonus 1,000"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Comparison")

        self._analysis_choice = tk.StringVar(value=DiscountFactorAnalysisControl._FUTURE_WEIGHTS)

    def _add_widgets(self):
        self.add_radiobutton_improved(DiscountFactorAnalysisControl._FUTURE_WEIGHTS, self._analysis_choice)
        self.add_radiobutton_improved(DiscountFactorAnalysisControl._REMAINING_STEPS, self._analysis_choice)
        self.add_radiobutton_improved(DiscountFactorAnalysisControl._BONUS_10, self._analysis_choice)
        self.add_radiobutton_improved(DiscountFactorAnalysisControl._BONUS_100, self._analysis_choice)
        self.add_radiobutton_improved(DiscountFactorAnalysisControl._BONUS_1000, self._analysis_choice)

    def show_future_weights(self):
        return self._analysis_choice.get() == DiscountFactorAnalysisControl._FUTURE_WEIGHTS

    def show_remaining_steps(self):
        return self._analysis_choice.get() == DiscountFactorAnalysisControl._REMAINING_STEPS

    def show_bonus_10(self):
        return self._analysis_choice.get() == DiscountFactorAnalysisControl._BONUS_10

    def show_bonus_100(self):
        return self._analysis_choice.get() == DiscountFactorAnalysisControl._BONUS_100

    def show_bonus_1000(self):
        return self._analysis_choice.get() == DiscountFactorAnalysisControl._BONUS_1000


class ZoomInAndOutControl(Control):
    _IN = "In <<"
    _OUT = "Out >>"
    _RESET = "Reset"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Zoom")

        self._zoom_level = 0

    def _add_widgets(self):
        self.add_horizontal_push_button(ZoomInAndOutControl._IN, self.callback_zoom_in)
        self.add_horizontal_push_button(ZoomInAndOutControl._OUT, self.callback_zoom_out)
        self.add_horizontal_push_button(ZoomInAndOutControl._RESET, self.callback_zoom_reset)

    def callback_zoom_in(self):
        self._zoom_level += 1
        self._guru_parent_redraw()

    def callback_zoom_out(self):
        if self._zoom_level > 0:
            self._zoom_level -= 1
            self._guru_parent_redraw()

    def callback_zoom_reset(self):
        if self._zoom_level > 0:
            self._zoom_level = 0
            self._guru_parent_redraw()

    def get_zoom_level(self):
        return self._zoom_level


class QuarterlyDistributionControl(Control):
    _NONE = "None"
    _BARS = "Bars"
    _STACKED = "Stacked"
    _LINES = "Lines"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Show Quarters As")

        self._distribution_choice = tk.StringVar(value=QuarterlyDistributionControl._BARS)

    def _add_widgets(self):
        self.add_radiobutton_improved(QuarterlyDistributionControl._NONE, self._distribution_choice)
        self.add_radiobutton_improved(QuarterlyDistributionControl._BARS, self._distribution_choice)
        self.add_radiobutton_improved(QuarterlyDistributionControl._STACKED, self._distribution_choice)
        self.add_radiobutton_improved(QuarterlyDistributionControl._LINES, self._distribution_choice)

    def show_none(self):
        return self._distribution_choice.get() == QuarterlyDistributionControl._NONE

    def show_bars(self):
        return self._distribution_choice.get() == QuarterlyDistributionControl._BARS

    def show_stacked(self):
        return self._distribution_choice.get() == QuarterlyDistributionControl._STACKED

    def show_lines(self):
        return self._distribution_choice.get() == QuarterlyDistributionControl._LINES


class ShowMeanOrMedianStatControl(Control):
    _NONE = "None"
    _MEAN = "Mean"
    _MEDIAN = "Median"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Show Statistic")

        self._distribution_choice = tk.StringVar(value=ShowMeanOrMedianStatControl._NONE)

    def _add_widgets(self):
        self.add_radiobutton_improved(ShowMeanOrMedianStatControl._NONE, self._distribution_choice)
        self.add_radiobutton_improved(ShowMeanOrMedianStatControl._MEAN, self._distribution_choice)
        self.add_radiobutton_improved(ShowMeanOrMedianStatControl._MEDIAN, self._distribution_choice)

    def show_none(self):
        return self._distribution_choice.get() == ShowMeanOrMedianStatControl._NONE

    def show_mean(self):
        return self._distribution_choice.get() == ShowMeanOrMedianStatControl._MEAN

    def show_median(self):
        return self._distribution_choice.get() == ShowMeanOrMedianStatControl._MEDIAN


class CurveDirectionControl(Control):
    _LEFT = "Left"
    _RIGHT = "Right"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Steering Direction")

        self._direction = tk.StringVar(value=CurveDirectionControl._LEFT)

    def _add_widgets(self):
        self.add_radiobutton_improved(CurveDirectionControl._LEFT, self._direction)
        self.add_radiobutton_right_improved(CurveDirectionControl._RIGHT, self._direction)

    def direction_left(self):
        return self._direction.get() == CurveDirectionControl._LEFT

    def direction_right(self):
        return self._direction.get() == CurveDirectionControl._RIGHT


class CurveSteeringDegreesControl(Control):
    _LOW = "0 - 10"
    _MEDIUM = "11 - 20"
    _HIGH = "21 - 30"
    _ALL = "All"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Steering Degrees")

        self._degrees = tk.StringVar(value=CurveSteeringDegreesControl._ALL)

    def _add_widgets(self):
        self.add_radiobutton_improved(CurveSteeringDegreesControl._LOW, self._degrees)
        self.add_radiobutton_right_improved(CurveSteeringDegreesControl._MEDIUM, self._degrees)
        self.add_radiobutton_improved(CurveSteeringDegreesControl._HIGH, self._degrees)
        self.add_radiobutton_right_improved(CurveSteeringDegreesControl._ALL, self._degrees)

    def get_steering_range(self):
        if self._degrees.get() == CurveSteeringDegreesControl._LOW:
            return 0, 10.5
        elif self._degrees.get() == CurveSteeringDegreesControl._MEDIUM:
            return 10.5, 20.5
        elif self._degrees.get() == CurveSteeringDegreesControl._HIGH:
            return 20.5, 30
        else:
            return 0, 30


class CurveSpeedControl(Control):
    _L1 = "< 1.0"
    _L2 = "1.0 - 1.9"
    _L3 = "2.0 - 2.9"
    _L4 = ">= 3.0"
    _ALL = "All"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, speed_type: str):
        super().__init__(guru_parent_redraw, control_frame, speed_type + " Speed")

        self._speed = tk.StringVar(value=CurveSpeedControl._ALL)

    def _add_widgets(self):
        self.add_radiobutton_improved(CurveSpeedControl._L1, self._speed)
        self.add_radiobutton_improved(CurveSpeedControl._L2, self._speed)
        self.add_radiobutton_improved(CurveSpeedControl._L3, self._speed)
        self.add_radiobutton_improved(CurveSpeedControl._L4, self._speed)
        self.add_radiobutton_improved(CurveSpeedControl._ALL, self._speed)

    def get_speed_range(self):
        if self._speed.get() == CurveSpeedControl._L1:
            return 0, 0.9
        elif self._speed.get() == CurveSpeedControl._L2:
            return 1.0, 1.9
        elif self._speed.get() == CurveSpeedControl._L3:
            return 2.0, 2.9
        elif self._speed.get() == CurveSpeedControl._L4:
            return 3.0, 99
        else:
            return None


class CurveInitialSlideControl(Control):
    _LOW = "Low"
    _ALL = "All"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Initial Slide")

        self._slide = tk.StringVar(value=CurveInitialSlideControl._LOW)

    def _add_widgets(self):
        self.add_radiobutton_improved(CurveInitialSlideControl._LOW, self._slide)
        self.add_radiobutton_right_improved(CurveInitialSlideControl._ALL, self._slide)

    def get_initial_slide_range(self):
        if self._slide.get() == CurveInitialSlideControl._LOW:
            return -2, 2
        else:
            return None


class CurveHighlightControl(Control):
    def __init__(self, guru_parent_redraw, control_frame: tk.Frame,
                 callback_before: callable, callback_after: callable):
        super().__init__(guru_parent_redraw, control_frame, "Highlighted Curve")

        self._text = tk.StringVar()
        self._callback_before = callback_before
        self._callback_after = callback_after

    def _add_widgets(self):
        self.add_horizontal_push_button("<<", self._callback_before)
        self.add_horizontal_push_button(">>", self._callback_after, True)
        self.add_information_text(self._text)

    def display_text(self, new_text):
        self._text.set(new_text)


class NumericButtonsControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame,
                 title: str, unit: str, values: list[int], default: int):
        super().__init__(guru_parent_redraw, control_frame, title)

        assert default in values

        self._all_values = values
        self._unit = unit
        self._value = tk.StringVar(value=self._make_value_string(default))

    def _add_widgets(self):
        for v in self._all_values:
            self.add_radiobutton_improved(self._make_value_string(v), self._value)

    def _make_value_string(self, value):
        return str(value) + " " + self._unit

    def get_value(self):
        return float(self._value.get()[:-len(self._unit)-1]) / 100


class InformationTextControl(Control):
    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Longest Path")

        self._text = tk.StringVar()

    def _add_widgets(self):
        self.add_information_text(self._text)

    def display_text(self, new_text):
        self._text.set(new_text)


class EvaluationPairsControl(Control):
    _SEPARATE = "Separate"
    _COMBINED = "Combined"
    _ODD = "Odd"
    _EVEN = "Even"

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Evaluation Pairs")

        self._pairing = tk.StringVar(value=EvaluationPairsControl._SEPARATE)

    def _add_widgets(self):
        self.add_radiobutton_improved(EvaluationPairsControl._SEPARATE, self._pairing)
        self.add_radiobutton_improved(EvaluationPairsControl._COMBINED, self._pairing)
        self.add_radiobutton_improved(EvaluationPairsControl._ODD, self._pairing)
        self.add_radiobutton_improved(EvaluationPairsControl._EVEN, self._pairing)

    def show_separate(self):
        return self._pairing.get() == EvaluationPairsControl._SEPARATE

    def show_combined(self):
        return self._pairing.get() == EvaluationPairsControl._COMBINED

    def show_odd(self):
        return self._pairing.get() == EvaluationPairsControl._ODD

    def show_even(self):
        return self._pairing.get() == EvaluationPairsControl._EVEN


class QuartersCheckButtonControl(Control):
    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Quarters")

        self._q1 = tk.BooleanVar(value=True)
        self._q2 = tk.BooleanVar(value=False)
        self._q3 = tk.BooleanVar(value=False)
        self._q4 = tk.BooleanVar(value=True)

    def _add_widgets(self):
        self.add_checkbutton("Q1", self._q1)
        self.add_checkbutton("Q2", self._q2)
        self.add_checkbutton("Q3", self._q3)
        self.add_checkbutton("Q4", self._q4)

    def show_q1(self):
        return self._q1.get()

    def show_q2(self):
        return self._q2.get()

    def show_q3(self):
        return self._q3.get()

    def show_q4(self):
        return self._q4.get()


class ShowLastStepControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Last Step")

        self._show_last_step = tk.BooleanVar(value=True)

    def _add_widgets(self):
        self.add_checkbutton("Show", self._show_last_step)

    def show_last_step(self):
        return self._show_last_step.get()


class ShowFinalIterationControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Final Iteration")

        self._show_final_iteration = tk.BooleanVar(value=False)

    def _add_widgets(self):
        self.add_checkbutton("Show", self._show_final_iteration)

    def show_final_iteration(self):
        return self._show_final_iteration.get()


class OutcomesCheckButtonControl(Control):

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame, include_evaluations=False):
        super().__init__(guru_parent_redraw, control_frame, "Outcome")

        self._lap_complete = tk.BooleanVar(value=False)
        self._off_track = tk.BooleanVar(value=True)
        self._crashed = tk.BooleanVar(value=False)
        self._reversed = tk.BooleanVar(value=False)
        self._lost_control = tk.BooleanVar(value=False)

    def _add_widgets(self):
        self.add_checkbutton("Lap Complete", self._lap_complete)
        self.add_checkbutton("Off Track", self._off_track)
        self.add_checkbutton("Crashed", self._crashed)
        self.add_checkbutton("Reversed", self._reversed)
        self.add_checkbutton("Lost Control", self._lost_control)

    def show_lap_complete(self):
        return self._lap_complete.get()

    def show_off_track(self):
        return self._off_track.get()

    def show_crashed(self):
        return self._crashed.get()

    def show_reversed(self):
        return self._reversed.get()

    def show_lost_control(self):
        return self._lost_control.get()


class RewardTypeControl(Control):
    _EVENT_REWARD = "Event Reward"
    _FUTURE_REWARD = "Future Reward"
    _NEW_EVENT_REWARD = "New Event Reward"
    _NEW_FUTURE_REWARD = "New Future Reward"
    _ALTERNATE_DISCOUNT_FACTOR = "Future DF = "

    def __init__(self, redraw_callback: callable, control_frame: tk.Frame, config_manager: ConfigManager):
        super().__init__(redraw_callback, control_frame, "Reward Type")
        self._chosen_reward_type = tk.StringVar(value=RewardTypeControl._EVENT_REWARD)
        self._redraw_callback = redraw_callback
        self._alternate_discount_factor_dict = dict()
        self._config_manager = config_manager

    def _add_widgets(self):
        self.add_radiobutton_improved(RewardTypeControl._EVENT_REWARD, self._chosen_reward_type)
        self.add_radiobutton_improved(RewardTypeControl._FUTURE_REWARD, self._chosen_reward_type)
        if self._config_manager.get_calculate_new_reward():
            self.add_radiobutton_improved(RewardTypeControl._NEW_EVENT_REWARD, self._chosen_reward_type)
            self.add_radiobutton_improved(RewardTypeControl._NEW_FUTURE_REWARD, self._chosen_reward_type)
        if self._config_manager.get_calculate_alternate_discount_factors():
            self._alternate_discount_factor_dict = dict()
            for i in range(0, discount_factors.get_number_of_discount_factors()):
                name = RewardTypeControl._ALTERNATE_DISCOUNT_FACTOR + str(discount_factors.get_discount_factor(i))
                self._alternate_discount_factor_dict[name] = i
                if i > 0:
                    self.add_radiobutton_improved(name, self._chosen_reward_type)

    def measure_event_reward(self):
        return self._chosen_reward_type.get() == RewardTypeControl._EVENT_REWARD

    def measure_new_event_reward(self):
        return self._chosen_reward_type.get() == RewardTypeControl._NEW_EVENT_REWARD

    def measure_discounted_future_reward(self):
        return self._chosen_reward_type.get() == RewardTypeControl._FUTURE_REWARD

    def measure_new_discounted_future_reward(self):
        return self._chosen_reward_type.get() == RewardTypeControl._NEW_FUTURE_REWARD

    def measure_alternate_discounted_future_reward(self):
        return self._chosen_reward_type.get() in self._alternate_discount_factor_dict.keys()

    def get_alternate_discount_factor_index(self):
        if self.measure_alternate_discounted_future_reward():
            return self._alternate_discount_factor_dict[self._chosen_reward_type.get()]
        else:
            return None

    def get_alternate_discount_factor(self):
        index = self.get_alternate_discount_factor_index()
        if index is not None:
            return discount_factors.get_discount_factor(index)
        else:
            return None


class EpisodeTrainingRewardTypeControl(Control):
    _TOTAL_EVENT_REWARD = "Total Event Reward"
    _MAX_FUTURE_REWARD = "Max Future Reward"
    _MEAN_FUTURE_REWARD = "Mean Future Reward"

    def __init__(self, redraw_callback: callable, control_frame: tk.Frame):
        super().__init__(redraw_callback, control_frame, "Episode Reward")
        self._chosen_reward_type = tk.StringVar(value=EpisodeTrainingRewardTypeControl._TOTAL_EVENT_REWARD)
        self._redraw_callback = redraw_callback

    def _add_widgets(self):
        self.add_radiobutton_improved(EpisodeTrainingRewardTypeControl._TOTAL_EVENT_REWARD, self._chosen_reward_type)
        self.add_radiobutton_improved(EpisodeTrainingRewardTypeControl._MAX_FUTURE_REWARD, self._chosen_reward_type)
        self.add_radiobutton_improved(EpisodeTrainingRewardTypeControl._MEAN_FUTURE_REWARD, self._chosen_reward_type)

    def measure_total_event_rewards(self):
        return self._chosen_reward_type.get() == EpisodeTrainingRewardTypeControl._TOTAL_EVENT_REWARD

    def measure_max_future_reward(self):
        return self._chosen_reward_type.get() == EpisodeTrainingRewardTypeControl._MAX_FUTURE_REWARD

    def measure_mean_future_reward(self):
        return self._chosen_reward_type.get() == EpisodeTrainingRewardTypeControl._MEAN_FUTURE_REWARD


