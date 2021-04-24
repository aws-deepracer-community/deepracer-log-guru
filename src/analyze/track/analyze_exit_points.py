#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics

from src.analyze.core.controls import EpisodeRadioButtonControl


class AnalyzeExitPoints(TrackAnalyzer):


    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()

    def redraw(self):
        if self._episodes_control.show_filtered():
            episodes = self.filtered_episodes
        elif self._episodes_control.show_all():
            episodes = self.all_episodes
        else:
            episodes = None

        if episodes:
            for e in episodes:
                if not e.lap_complete:
                    exit_point = (e.events[-1].x, e.events[-1].y)
                    self.track_graphics.plot_dot(exit_point, 2, "orange")

        elif self._episodes_control.show_evaluations():
            for v in self.evaluation_phases:
                pass
                # TODO
