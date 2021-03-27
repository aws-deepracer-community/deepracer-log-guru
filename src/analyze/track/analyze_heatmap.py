import tkinter as tk
import numpy as np

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.ui.please_wait import PleaseWait
from src.analyze.core.controls import ConvergenceGranularityControl, TrackAppearanceControl,\
    EpisodeRadioButtonControl, AdvancedFiltersControl, MeasurementControl


class AnalyzeHeatmap(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame, please_wait :PleaseWait):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._measurement_control = MeasurementControl(self.chosen_new_measurement, control_frame, False)
        self._episodes_control = EpisodeRadioButtonControl(self.chosen_new_episodes, control_frame, False)
        self._granularity_control = ConvergenceGranularityControl(self.chosen_new_granularity, control_frame)
        self._appearance_control = TrackAppearanceControl(guru_parent_redraw, control_frame,
                                                          None, self.chosen_new_appearance, self.chosen_new_appearance)
        self._skip_starts_control = AdvancedFiltersControl(self.chosen_skip_starts, control_frame)

        self._heat_map = None
        self.please_wait = please_wait

    def build_control_frame(self, control_frame):
        self._measurement_control.add_to_control_frame()
        self._episodes_control.add_to_control_frame()
        self._granularity_control.add_to_control_frame()
        self._appearance_control.add_to_control_frame()
        self._skip_starts_control.add_to_control_frame()

    def redraw(self):
        if self._heat_map:
            brightness = 0
            if self._appearance_control.bright_brightness():
                brightness = 1
            elif self._appearance_control.very_bright_brightness():
                brightness = 2
            elif self._appearance_control.faint_brightness():
                brightness = -1

            color_palette = self._appearance_control.get_chosen_color_palette()

            if self._measurement_control.measure_visits():
                self._heat_map.draw_visits(self.track_graphics, brightness, color_palette)
            elif self._measurement_control.measure_slide():
                self._heat_map.draw_statistic(self.track_graphics, brightness, color_palette, 12, 0)
            elif self._measurement_control.measure_steering():
                self._heat_map.draw_statistic(self.track_graphics, brightness, color_palette, 30, 0)
            else:
                max_speed = self.action_space.get_max_speed()
                min_speed = self.action_space.get_min_speed()
                if self._measurement_control.measure_progress_speed():
                    max_speed *= 1.2
                    min_speed *= 0.8
                self._heat_map.draw_statistic(self.track_graphics, brightness, color_palette, max_speed, min_speed)

    def warning_filtered_episodes_changed(self):
        if self._episodes_control.show_filtered():
            self._heat_map = None

    def warning_track_changed(self):
        self._heat_map = None

    def warning_action_space_filter_changed(self):
        self._heat_map = None

    def chosen_skip_starts(self):
        self._heat_map = None
        self.guru_parent_redraw()

    def chosen_new_granularity(self):
        self._heat_map = None
        self.guru_parent_redraw()

    def chosen_new_episodes(self):
        self._heat_map = None
        self.guru_parent_redraw()

    def chosen_new_measurement(self):
        self._heat_map = None
        self.guru_parent_redraw()

    def chosen_new_appearance(self, new_value):
        self.guru_parent_redraw()

    def recalculate(self):
        if self._skip_starts_control.skip_starts():
            skip = 20
        else:
            skip = 0

        if self._episodes_control.show_all():
            episodes = self.all_episodes
        elif self._episodes_control.show_filtered():
            episodes = self.filtered_episodes
        else:
            episodes = None

        if episodes:
            if not self._heat_map:
                self.please_wait.start("Calculating")
                if self._measurement_control.measure_visits():
                    self._recalculate_measure_visits(episodes, skip)
                elif self._measurement_control.measure_action_speed():
                    self._recalculate_measure_action_speed(episodes, skip)
                elif self._measurement_control.measure_progress_speed():
                    self._recalculate_measure_progress_speed(episodes, skip)
                elif self._measurement_control.measure_track_speed():
                    self._recalculate_measure_track_speed(episodes, skip)
                elif self._measurement_control.measure_reward():
                    self._recalculate_measure_reward(episodes, skip)
                elif self._measurement_control.measure_slide():
                    self._recalculate_measure_slide(episodes, skip)
                elif self._measurement_control.measure_steering():
                    self._recalculate_measure_steering(episodes, skip)

    def _recalculate_measure_visits(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, False)
        for i, e in enumerate(episodes):
            e.apply_visits_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_action_speed(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_action_speed_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_track_speed(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_track_speed_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_progress_speed(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_progress_speed_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_reward(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_reward_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_slide(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_slide_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)

    def _recalculate_measure_steering(self, episodes, skip):
        self._heat_map = self.current_track.get_new_heat_map(self._granularity_control.granularity() / 100, True)
        for i, e in enumerate(episodes):
            e.apply_steering_to_heat_map(self._heat_map, skip, self.action_space_filter)
            self.please_wait.set_progress((i + 1) / len(episodes) * 100)