import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.ui.please_wait import PleaseWait
from src.analyze.core.controls import ConvergenceGranularityControl, TrackAppearanceControl,\
    EpisodeRadioButtonControl, AdvancedFiltersControl


class AnalyzeConvergence(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame, please_wait :PleaseWait):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(self.chosen_new_episodes, control_frame, False)
        self._granularity_control = ConvergenceGranularityControl(self.chosen_new_granularity, control_frame)
        self._appearance_control = TrackAppearanceControl(guru_parent_redraw, control_frame,
                                                          None, self.chosen_new_appearance, self.chosen_new_appearance)
        self._skip_starts_control = AdvancedFiltersControl(self.chosen_skip_starts, control_frame)

        self.visitor_map = None
        self.please_wait = please_wait

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._granularity_control.add_to_control_frame()
        self._appearance_control.add_to_control_frame()
        self._skip_starts_control.add_to_control_frame()

    def redraw(self):
        if self.visitor_map:
            brightness = 0
            if self._appearance_control.bright_brightness():
                brightness = 1
            elif self._appearance_control.very_bright_brightness():
                brightness = 2
            elif self._appearance_control.faint_brightness():
                brightness = -1
            self.visitor_map.draw(self.track_graphics, brightness, self._appearance_control.get_chosen_color_palette())

    def warning_filtered_episodes_changed(self):
        if self._episodes_control.show_filtered():
            self.visitor_map = None

    def warning_track_changed(self):
        self.visitor_map = None

    def warning_action_space_filter_changed(self):
        self.visitor_map = None

    def chosen_skip_starts(self):
        self.visitor_map = None
        self.guru_parent_redraw()

    def chosen_new_granularity(self):
        self.visitor_map = None
        self.guru_parent_redraw()

    def chosen_new_episodes(self):
        self.visitor_map = None
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
            if not self.visitor_map:
                self.please_wait.start("Calculating")
                self.visitor_map = self.current_track.get_new_visitor_map(self._granularity_control.granularity() / 100)
                for i, e in enumerate(episodes):
                    e.apply_to_visitor_map(self.visitor_map, skip, self.action_space_filter)
                    self.please_wait.set_progress((i+1) / len(episodes) * 100)
