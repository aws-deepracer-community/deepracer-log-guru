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


class AnalyzeStraightFitting(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics: TrackGraphics, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

    def build_control_frame(self, control_frame):
        pass

    def redraw(self):
        pass

    def right_button_pressed(self, chosen_point):
        waypoint_id = self.current_track.get_closest_waypoint_id(chosen_point)
        waypoint = self.current_track.get_waypoint(waypoint_id)
