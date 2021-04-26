#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import src.utils.geometry as geometry

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.configuration.real_world import VEHICLE_WIDTH
from src.graphics.track_graphics import TrackGraphics
from src.sequences.sequence import Sequence


class AnalyzeCurveFitting(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics: TrackGraphics, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)
        self._all_sequences = []

    def build_control_frame(self, control_frame):
        pass

    def redraw(self):
        pass

    def right_button_pressed(self, chosen_point):
        waypoint_id = self.current_track.get_closest_waypoint_id(chosen_point)
        waypoint = self.current_track.get_waypoint(waypoint_id)

        distance_from_waypoint = geometry.get_distance_between_points(waypoint, chosen_point)
        max_distance_from_centre = (self.current_track.get_width() + VEHICLE_WIDTH) / 2

        if distance_from_waypoint > max_distance_from_centre:
            bearing_of_point = geometry.get_bearing_between_points(waypoint, chosen_point)
            chosen_point = geometry.get_point_at_bearing(waypoint, bearing_of_point, max_distance_from_centre)

        self.track_graphics.plot_dot(waypoint, 3, "blue")
        self.track_graphics.plot_dot(chosen_point, 3, "red")

        default_bearing = self.current_track.get_bearing_at_waypoint(waypoint_id)

        self.track_graphics.plot_angle_line(chosen_point, default_bearing, 1, 3, "red")

        print(len(self._all_sequences))

    def set_all_sequences(self, sequences: list[Sequence]):
        self._all_sequences = sequences