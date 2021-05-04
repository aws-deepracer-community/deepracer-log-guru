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

BEARING_RANGE = 60
BEARING_STEP = 10


class AnalyzeStraightFitting(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics: TrackGraphics, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._chosen_point = None
        self._chosen_bearing = 0.0
        self._distance = 0.0

    def build_control_frame(self, control_frame):
        pass

    def redraw(self):
        if self._chosen_point:
            self.track_graphics.plot_dot(self._chosen_point, 5, "red")
            self.track_graphics.plot_angle_line(self._chosen_point, self._chosen_bearing, self._distance, 2, "red")

    def right_button_pressed(self, chosen_point):
        self._chosen_point, waypoint_id = self.current_track.get_adjusted_point_on_track(chosen_point)
        mid_bearing = int(round(self.current_track.get_bearing_at_waypoint(waypoint_id)))
        self._distance = 0.0
        self._chosen_bearing = mid_bearing

        self._try_bearings(mid_bearing - BEARING_RANGE, mid_bearing + BEARING_RANGE, BEARING_STEP, waypoint_id)
        self._try_bearings(self._chosen_bearing - BEARING_STEP, self._chosen_bearing + BEARING_STEP, 1, waypoint_id)

        self.guru_parent_redraw()

    def _try_bearings(self, start, finish, step, waypoint_id):
        bearing = start
        while bearing <= finish:
            distance = self.current_track.get_projected_distance_on_track(self._chosen_point, bearing, waypoint_id)
            if distance > self._distance:
                self._distance = distance
                self._chosen_bearing = bearing
            bearing += step

