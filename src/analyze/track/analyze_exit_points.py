#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.episode.episode import LAP_COMPLETE, OFF_TRACK, CRASHED, REVERSED, LOST_CONTROL
from src.graphics.track_graphics import TrackGraphics

from src.analyze.core.controls import EpisodeRadioButtonControl, OutcomesCheckButtonControl


class AnalyzeExitPoints(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics: TrackGraphics, control_frame: tk.Frame):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame, True)
        self._outcome_control = OutcomesCheckButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._outcome_control.add_to_control_frame()

    def redraw(self):
        if self._episodes_control.show_filtered():
            episodes = self.filtered_episodes
        elif self._episodes_control.show_all():
            episodes = self.all_episodes
        else:
            episodes = None

        if episodes:
            for e in episodes:
                colour = None
                if e.outcome == LAP_COMPLETE and self._outcome_control.show_lap_complete():
                    colour = "green"
                if e.outcome == OFF_TRACK and self._outcome_control.show_off_track():
                    colour = "orange"
                if e.outcome == CRASHED and self._outcome_control.show_crashed():
                    colour = "red"
                if e.outcome == REVERSED and self._outcome_control.show_reversed():
                    colour = "cyan"
                if e.outcome == LOST_CONTROL and self._outcome_control.show_lost_control():
                    colour = "yellow"

                if colour:
                    exit_point = (e.events[-1].x, e.events[-1].y)
                    self.track_graphics.plot_dot(exit_point, 3, colour)

        elif self._episodes_control.show_evaluations():
            start_wp = self.all_episodes[0].events[0].closest_waypoint_index
            start_percent = self.current_track.get_waypoint_percent_from_race_start(start_wp)

            whole_lap = False
            for v in self.evaluation_phases:
                for p in v.progresses:
                    if p == 100:
                        whole_lap = True
                    else:
                        p += start_percent
                        if p > 100:
                            p -= 100
                        exit_point = self.current_track.get_percent_progress_point_on_centre_line(p)
                        self.track_graphics.plot_dot(exit_point, 3, "orange")
            if whole_lap:
                exit_point = self.current_track.get_percent_progress_point_on_centre_line(start_percent)
                self.track_graphics.plot_dot(exit_point, 5, "green")

