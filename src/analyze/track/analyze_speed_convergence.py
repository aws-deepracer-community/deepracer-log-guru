import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.ui.please_wait import PleaseWait
from src.analyze.core.controls import ConvergenceGranularityControl, SpeedControl,\
    TrackAppearanceControl, EpisodeRadioButtonControl, AdvancedFiltersControl


import src.analyze.util.visitor as v

HIGH_VISITOR_MAP = 0
MEDIUM_VISITOR_MAP = 1
LOW_VISITOR_MAP = 2


class AnalyzeSpeedConvergence(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame, please_wait :PleaseWait):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(self.chosen_new_episodes, control_frame, False)
        self._granularity_control = ConvergenceGranularityControl(self.chosen_new_granularity, control_frame)
        self._speed_control = SpeedControl(self.chosen_new_speed, control_frame)
        self._appearance_control = TrackAppearanceControl(guru_parent_redraw, control_frame,
                                                          None, self.chosen_new_appearance, self.chosen_new_appearance)
        self._skip_starts_control = AdvancedFiltersControl(self.chosen_new_episodes, control_frame)

        self.visitor_maps = None
        self.please_wait = please_wait

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._granularity_control.add_to_control_frame()
        self._appearance_control.add_to_control_frame()
        self._speed_control.add_to_control_frame()
        self._skip_starts_control.add_to_control_frame()

    def redraw(self):
        if self.visitor_maps:
            colours = [ "", "", "" ]
            colours[HIGH_VISITOR_MAP] = "green"
            colours[MEDIUM_VISITOR_MAP] = "yellow"
            colours[LOW_VISITOR_MAP] = "red"

            if self._appearance_control.very_bright_brightness():
                threshold = 5
            elif self._appearance_control.bright_brightness():
                threshold = 10
            elif self._appearance_control.normal_brightness():
                threshold = 20
            else:
                threshold = 30

            v.multi_draw(self.track_graphics, self.visitor_maps, colours, threshold)

    def warning_filtered_episodes_changed(self):
        if self._episodes_control.show_filtered():
            self.visitor_maps = None

    def warning_all_episodes_changed(self):
        self.visitor_maps = None

    def warning_track_changed(self):
        self.visitor_maps = None

    def warning_action_space_filter_changed(self):
        self.visitor_maps = None

    def chosen_skip_starts(self):
        self.visitor_maps = None
        self.guru_parent_redraw()

    def chosen_new_granularity(self):
        self.visitor_maps = None
        self.guru_parent_redraw()

    def chosen_new_speed(self):
        self.visitor_maps = None
        self.guru_parent_redraw()

    def chosen_new_episodes(self):
        self.visitor_maps = None
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
            if not self.visitor_maps:
                self.please_wait.start("Calculating")

                self.visitor_maps = []
                for i in range(0, 3):
                    self.visitor_maps.append(self.current_track.get_new_visitor_map(self._granularity_control.granularity() / 100))
                for i, e in enumerate(episodes):
                    if self._speed_control.action_speed():
                        apply_to_visitor_map = e.apply_action_speed_to_visitor_map
                    elif self._speed_control.track_speed():
                        apply_to_visitor_map = e.apply_track_speed_to_visitor_map
                    elif self._speed_control.progress_speed():
                        apply_to_visitor_map = e.apply_progress_speed_to_visitor_map
                    else:
                        print("OOOPS - unknown type of speed!")
                        return

                    apply_to_visitor_map(self.visitor_maps[HIGH_VISITOR_MAP], skip, self.action_space_filter, self.action_space.is_high_speed)
                    apply_to_visitor_map(self.visitor_maps[MEDIUM_VISITOR_MAP], skip, self.action_space_filter, self.action_space.is_medium_speed)
                    apply_to_visitor_map(self.visitor_maps[LOW_VISITOR_MAP], skip, self.action_space_filter, self.action_space.is_low_speed)

                    self.please_wait.set_progress((i+1) / len(episodes) * 100)


