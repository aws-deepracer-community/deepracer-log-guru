#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.analyze.core.controls import InformationTextControl, NumericButtonsControl
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.utils import geometry

BEARING_STEP = 2


class AnalyzeStraightFitting(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics: TrackGraphics, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._path_width_control = NumericButtonsControl(guru_parent_redraw, control_frame,
                                                         "Path Width", "cm", [0, 2, 5, 10, 20], 0)
        self._information_control = InformationTextControl(guru_parent_redraw, control_frame)

        self._chosen_point = None
        self._chosen_bearing = 0.0
        self._distance = 0.0
        self._waypoint_id = 0
        self._path_width = self._path_width_control.get_value()

    def build_control_frame(self, control_frame):
        self._path_width_control.add_to_control_frame()
        self._information_control.add_to_control_frame()

    def redraw(self):
        if self._chosen_point:
            new_path_width = self._path_width_control.get_value()
            if new_path_width != self._path_width:
                self._path_width = new_path_width
                self._calculate_new_path()

            self._information_control.display_text(
                "Length = " + str(round(self._distance, 2)) + " m\n" +
                "Bearing = " + str(round(self._chosen_bearing, 1)) + " degrees")

            self.track_graphics.plot_dot(self._chosen_point, 3, "red")
            if self._path_width > 0.0:
                side_point_1 = geometry.get_point_at_bearing(self._chosen_point, self._chosen_bearing + 90,
                                                             self._path_width / 2)
                side_point_2 = geometry.get_point_at_bearing(self._chosen_point, self._chosen_bearing - 90,
                                                             self._path_width / 2)

                self.track_graphics.plot_angle_line(side_point_1, self._chosen_bearing, self._distance, 2, "red")
                self.track_graphics.plot_angle_line(side_point_2, self._chosen_bearing, self._distance, 2, "red")
            else:
                self.track_graphics.plot_angle_line(self._chosen_point, self._chosen_bearing, self._distance, 2, "red")

    def warning_track_changed(self):
        self._chosen_point = None

    def right_button_pressed(self, chosen_point):
        self._chosen_point, self._waypoint_id = self.current_track.get_adjusted_point_on_track(chosen_point,
                                                                                               self._path_width / 2)
        self._path_width = self._path_width_control.get_value()
        self._calculate_new_path()
        self.guru_parent_redraw()

    def _calculate_new_path(self):
        self._distance = 0.0
        self._chosen_bearing = 0.0
        self._try_bearings(-180, 180, BEARING_STEP, self._waypoint_id)
        self._try_bearings(self._chosen_bearing - BEARING_STEP, self._chosen_bearing + BEARING_STEP, BEARING_STEP / 10,
                           self._waypoint_id)

    def _try_bearings(self, start, finish, step, waypoint_id):
        path_width = self._path_width_control.get_value()
        bearing = start
        while bearing <= finish:
            distance = self.current_track.get_projected_distance_on_track(self._chosen_point, bearing, waypoint_id,
                                                                          path_width)
            if distance > self._distance:
                self._distance = distance
                self._chosen_bearing = bearing
            bearing += step
