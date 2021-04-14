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
from src.utils.colors import ColorPalette


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
    _PREDICTED_LAP = "Predicted Lap"
    _SMOOTHNESS = "Smoothness"
    _STEERING_STRAIGHT = "Steering Straight"
    _STEERING_LEFT = "Steering Left"
    _STEERING_RIGHT = "Steering Right"
    _SKEW = "Skew"
    _SLIDE = "Slide"
    _PROJECTED_TRAVEL_DISTANCE = "Projected Travel"
    _SECONDS = "Seconds"
    _OTHER = "Other:"

    _ALL_MEASUREMENTS_EXCEPT_SECONDS = [
        _VISITS, _EVENT_REWARD, _FUTURE_REWARD, _NEW_EVENT_REWARD, _NEW_FUTURE_REWARD, _ACTION_SPEED, _TRACK_SPEED,
        _PROGRESS_SPEED, _ACCELERATION, _BRAKING, _PREDICTED_LAP, _SMOOTHNESS, _STEERING_STRAIGHT, _STEERING_LEFT,
        _STEERING_RIGHT, _SKEW, _SLIDE, _PROJECTED_TRAVEL_DISTANCE
                                        ]

    def __init__(self, redraw_callback: callable, control_frame: tk.Frame, measure_seconds: bool):
        super().__init__(redraw_callback, control_frame, "Measure")
        self._current_measurement_button = tk.StringVar(value=MeasurementControl._VISITS)
        self._current_measurement_dropdown = tk.StringVar()
        self._show_measure_seconds = measure_seconds
        self._redraw_callback = redraw_callback

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
    _BLOB_SIZE_SMALL = "Small       "
    _BLOB_SIZE_MEDIUM = "Medium   "
    _BLOB_SIZE_LARGE = "Large       "
    _BLOB_SIZES = [_BLOB_SIZE_SMALL, _BLOB_SIZE_MEDIUM, _BLOB_SIZE_LARGE]

    _PALETTE_GREYS = "Greys       "
    _PALETTE_3_COLOURS = "3 Colours "
    _PALETTE_5_COLOURS = "5 Colours "
    _PALETTE_MULTI_A = "Multi-A"
    _PALETTE_MULTI_B = "Multi-B"
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
        self.add_checkbutton("Median", self._show_median)
        self.add_checkbutton("Best", self._show_best)
        self.add_checkbutton("Worst", self._show_worst)

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

    def __init__(self, guru_parent_redraw, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, control_frame, "Reward Types")

        self._reward_type = tk.StringVar(value=EpisodeRewardTypeControl._REWARD_PLUS_TOTAL)

    def _add_widgets(self):
        self.add_radiobutton_improved(EpisodeRewardTypeControl._REWARD_PLUS_TOTAL, self._reward_type)
        self.add_radiobutton_improved(EpisodeRewardTypeControl._REWARD_PLUS_FUTURE, self._reward_type)
        self.add_radiobutton_improved(EpisodeRewardTypeControl._NEW_REWARD_PLUS_TOTAL, self._reward_type)
        self.add_radiobutton_improved(EpisodeRewardTypeControl._NEW_REWARD_PLUS_FUTURE, self._reward_type)

    def show_reward_plus_total(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._REWARD_PLUS_TOTAL

    def show_reward_plus_future(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._REWARD_PLUS_FUTURE

    def show_new_reward_plus_total(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._NEW_REWARD_PLUS_TOTAL

    def show_new_reward_plus_future(self):
        return self._reward_type.get() == EpisodeRewardTypeControl._NEW_REWARD_PLUS_FUTURE


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
