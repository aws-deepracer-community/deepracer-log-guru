#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

import src.analyze.core.measurement_brightness as measurement_brightness

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.configuration.config_manager import ConfigManager
from src.episode.episode import Episode
from src.graphics.track_graphics import TrackGraphics
from src.ui.please_wait import PleaseWait
from src.analyze.core.controls import ConvergenceGranularityControl, TrackAppearanceControl,\
    EpisodeRadioButtonControl, MoreFiltersControl, MeasurementControl, SkipControl


class AnalyzeHeatmap(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame,
                 please_wait :PleaseWait, config_manager: ConfigManager):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._measurement_control = MeasurementControl(self._callback_different_measurement, control_frame, False, config_manager)
        self._episodes_control = EpisodeRadioButtonControl(self._callback_full_recalculate, control_frame, False)
        self._granularity_control = ConvergenceGranularityControl(self._callback_full_recalculate, control_frame)
        self._appearance_control = TrackAppearanceControl(guru_parent_redraw, control_frame,
                                                          None, self._callback_quick_change_appearance, self._callback_quick_change_appearance)
        self._skip_control = SkipControl(self._callback_full_recalculate, control_frame)
        self._more_filters_control = MoreFiltersControl(self._callback_full_recalculate, control_frame, False)

        self._visits_heat_map = None
        self._statistics_heat_map = None
        self.please_wait = please_wait

        self._alternate_discount_factor_index = None

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._measurement_control.add_to_control_frame()
        self._granularity_control.add_to_control_frame()
        self._appearance_control.add_to_control_frame()
        self._skip_control.add_to_control_frame()
        self._more_filters_control.add_to_control_frame()

    def redraw(self):
        if self._visits_heat_map:
            brightness = 0
            if self._appearance_control.bright_brightness():
                brightness = 1
            elif self._appearance_control.very_bright_brightness():
                brightness = 2
            elif self._appearance_control.faint_brightness():
                brightness = -1

            color_palette = self._appearance_control.get_chosen_color_palette()

            if self._measurement_control.measure_progress_speed() or self._measurement_control.measure_action_speed() or self._measurement_control.measure_track_speed():
                max_speed = self.action_space.get_max_speed()
                min_speed = self.action_space.get_min_speed()
                if self._measurement_control.measure_progress_speed():
                    max_speed *= 1.2
                    min_speed *= 0.8
                self._statistics_heat_map.draw_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map, max_speed, min_speed)
            elif self._measurement_control.measure_visits():
                self._visits_heat_map.draw_visits(self.track_graphics, brightness, color_palette)
            elif self._measurement_control.measure_steering_straight() or \
                    self._measurement_control.measure_steering_left() or \
                    self._measurement_control.measure_steering_right() or \
                    self._measurement_control.measure_projected_travel_distance():
                self._statistics_heat_map.draw_brightness_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map)
            ### Otherwise the OLD kludgy way...
            elif self._measurement_control.measure_slide():
                self._statistics_heat_map.draw_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map, 14, 0)
            elif self._measurement_control.measure_skew():
                self._statistics_heat_map.draw_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map, 60, 0)
            elif self._measurement_control.measure_steering_left() or self._measurement_control.measure_steering_right():
                self._statistics_heat_map.draw_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map, 30, 0)
            else:
                self._statistics_heat_map.draw_statistic(self.track_graphics, brightness, color_palette, self._visits_heat_map)

    def warning_filtered_episodes_changed(self):
        if self._episodes_control.show_filtered():
            self._visits_heat_map = None
            self._statistics_heat_map = None

    def warning_track_changed(self):
        self._visits_heat_map = None
        self._statistics_heat_map = None

    def warning_all_episodes_changed(self):
        self._visits_heat_map = None
        self._statistics_heat_map = None

    def warning_action_space_filter_changed(self):
        if self._more_filters_control.filter_actions():
            self._visits_heat_map = None
            self._statistics_heat_map = None

    def warning_sector_filter_changed(self):
        if self._more_filters_control.filter_sector():
            self._visits_heat_map = None
            self._statistics_heat_map = None

    def _callback_full_recalculate(self, optional_value=None):
        self._visits_heat_map = None
        self._statistics_heat_map = None
        self.guru_parent_redraw()

    def _callback_different_measurement(self, optional_value=None):
        self._statistics_heat_map = None
        self.guru_parent_redraw()

    def _callback_quick_change_appearance(self, optional_value=None):
        self.guru_parent_redraw()

    def recalculate(self):
        if self._skip_control.skip_starts():
            skip_start = 20
        else:
            skip_start = 0

        if self._skip_control.skip_ends():
            skip_end = 10
        else:
            skip_end = 0

        if self._episodes_control.show_all():
            episodes = self.all_episodes
        elif self._episodes_control.show_filtered():
            episodes = self.filtered_episodes
        else:
            episodes = None

        if episodes:
            if not self._visits_heat_map or (
                    not self._measurement_control.measure_visits() and not self._statistics_heat_map):

                self.please_wait.start("Calculating")

                self._statistics_heat_map = self.current_track.get_new_heat_map(
                    self._granularity_control.granularity() / 100, True)
                if self._visits_heat_map:
                    recalculate_visits = False
                else:
                    recalculate_visits = True
                    self._visits_heat_map = self.current_track.get_new_heat_map(
                        self._granularity_control.granularity() / 100, False)

                if self._more_filters_control.filter_actions():
                    action_space_filter = self.action_space_filter
                else:
                    action_space_filter = None

                if self._more_filters_control.filter_sector() and self.sector_filter and len(self.sector_filter) == 1:
                    waypoint_range = self.current_track.get_sector_start_and_finish(self.sector_filter)
                else:
                    waypoint_range = None

                # Plug in brightness method - the new way
                if self._measurement_control.measure_steering_straight():
                    brightness_method = measurement_brightness.get_brightness_for_steering_straight
                elif self._measurement_control.measure_steering_left():
                    brightness_method = measurement_brightness.get_brightness_for_steering_left
                elif self._measurement_control.measure_steering_right():
                    brightness_method = measurement_brightness.get_brightness_for_steering_right
                elif self._measurement_control.measure_projected_travel_distance():
                    brightness_method = measurement_brightness.get_brightness_for_projected_travel_distance
                else:
                    brightness_method = None

                if brightness_method:
                    e: Episode
                    for i, e in enumerate(episodes):
                        e.apply_event_stat_to_heat_map(brightness_method, self._statistics_heat_map, skip_start, skip_end,
                                                       action_space_filter, waypoint_range)
                        if recalculate_visits:
                            e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter,
                                                       waypoint_range)
                        self.please_wait.set_progress((i + 1) / len(episodes) * 100)

                # Else still doing it the OLD kludgy way ...
                elif self._measurement_control.measure_visits():
                    self._recalculate_measure_visits(episodes, skip_start, skip_end, action_space_filter, waypoint_range)
                elif self._measurement_control.measure_action_speed():
                    self._recalculate_measure_action_speed(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_progress_speed():
                    self._recalculate_measure_progress_speed(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_track_speed():
                    self._recalculate_measure_track_speed(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_event_reward():
                    self._recalculate_measure_reward(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_new_event_reward():
                    self._recalculate_measure_new_reward(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_discounted_future_reward():
                    self._recalculate_measure_discounted_future_reward(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_new_discounted_future_reward():
                    self._recalculate_measure_new_discounted_future_reward(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_slide():
                    self._recalculate_measure_slide(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_skew():
                    self._recalculate_measure_skew(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_smoothness():
                    self._recalculate_measure_smoothness(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_acceleration():
                    self._recalculate_measure_acceleration(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                elif self._measurement_control.measure_braking():
                    self._recalculate_measure_braking(episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits)
                else:
                    self._alternate_discount_factor_index = self._measurement_control.get_alternate_discount_factor_index()
                    if self._alternate_discount_factor_index is not None:
                        self._recalculate_measure_alternate_discounted_future_reward(episodes, skip_start, skip_end,
                                                                                     action_space_filter, waypoint_range, recalculate_visits)

    def _recalculate_measure_visits(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_action_speed(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_action_speed_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_track_speed(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_track_speed_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_progress_speed(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_progress_speed_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_reward(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_reward_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_new_reward(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_new_reward_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_discounted_future_reward(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_discounted_future_reward_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_alternate_discounted_future_reward(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_alternate_discounted_future_reward_to_heat_map(self._statistics_heat_map, skip_start, skip_end,
                                                                   action_space_filter, waypoint_range,
                                                                   self._alternate_discount_factor_index)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_new_discounted_future_reward(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_new_discounted_future_reward_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_slide(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_slide_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_skew(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_skew_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_smoothness(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_smoothness_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_acceleration(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_acceleration_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_braking(self, episodes, skip_start, skip_end, action_space_filter, waypoint_range, recalculate_visits: bool):
        e: Episode
        for i, e in enumerate(episodes):
            e.apply_braking_to_heat_map(self._statistics_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            if recalculate_visits:
                e.apply_visits_to_heat_map(self._visits_heat_map, skip_start, skip_end, action_space_filter, waypoint_range)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)
