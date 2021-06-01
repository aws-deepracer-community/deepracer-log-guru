#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes
from matplotlib.figure import SubplotParams

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.episode_selector import EpisodeSelector
from src.analyze.core.controls import EpisodeAxisControl


class AnalyzeEpisodeStat(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector,
                 title_word: str, bar_label :str, line_label :str,
                 show_step_dots :bool=False, use_second_axis_scale :bool=False,
                 second_axis_label: str=""):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_selector = episode_selector
        self.episode = None
        self.show_step_dots = show_step_dots
        self.use_second_axis_scale = use_second_axis_scale
        self.title_word = title_word
        self.bar_label= bar_label
        self.line_label = line_label
        self.second_axis_label = second_axis_label

        self.axis_control = EpisodeAxisControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self.axis_control.add_to_control_frame()

        self.episode_selector.add_to_control_frame(control_frame, self.guru_parent_redraw)

    def reset_labels(self, title_word: str, bar_label :str, line_label :str, second_axis_label: str=""):
        self.title_word = title_word
        self.bar_label = bar_label
        self.line_label = line_label
        if second_axis_label:
            self.second_axis_label = second_axis_label

    def add_plots(self):
        self.additional_preparation_for_plots()

        if self.use_second_axis_scale:
            grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.92, bottom=0.08, top=0.92)
        else:
            grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])
        if self.use_second_axis_scale:
            axes2 :Axes = axes.twinx()
        else:
            axes2 = None

        # Plot the data

        self.episode = self.episode_selector.get_selected_episode()
        if not self.episode:
            return

        plot_x = []
        general_title = "???"
        axis_label = "???"
        wrap_point = None
        max_xscale_override = None

        if self.axis_control.show_time():
            plot_x = self.get_plot_data_times()
            general_title = "by Time"
            axis_label = "Time / seconds"
        if self.axis_control.show_step():
            plot_x = self.get_plot_data_steps()
            general_title = "per Step"
            axis_label = "Step"
        if self.axis_control.show_progress():
            plot_x = self.get_plot_data_progresses()
            general_title = "by Progress"
            axis_label = "Progress %"
            axes.set_xbound(0, round(max(plot_x)))
        if self.axis_control.show_distance():
            plot_x = self.get_plot_data_distances()
            general_title = "by Distance"
            axis_label = "Distance Travelled / metres"
        if self.axis_control.show_lap_position():
            plot_x, wrap_point = self.get_plot_data_lap_positions()
            general_title = "by Lap Position"
            axis_label = "Lap Position / %"
            max_xscale_override = 100
        if self.axis_control.show_waypoint_id():
            plot_x, wrap_point = self.get_plot_data_waypoints()
            general_title = "by Waypoint Id"
            axis_label = "Waypoint Id"
            max_xscale_override = self.current_track.get_number_of_waypoints()

        plot_y_bar_values_per_step = self.get_plot_bar_values_per_step(wrap_point)
        plot_y_line_values_per_step = self.get_plot_line_values_per_step(wrap_point)

        axes.fill_between(plot_x, plot_y_bar_values_per_step, step="mid", color="C1", label=self.bar_label)
        if self.show_step_dots:
            axes.plot(plot_x, plot_y_bar_values_per_step, "o", color="black", markersize=3, label="Step")
        if self.use_second_axis_scale:
            axes2.plot(plot_x, plot_y_line_values_per_step, color="C2", label=self.line_label, linewidth=3)
            self._plot_any_additional_lines(axes2, plot_x, wrap_point)
        else:
            axes.plot(plot_x, plot_y_line_values_per_step, color="C2", label=self.line_label, linewidth=3)
            self._plot_any_additional_lines(axes, plot_x, wrap_point)

        # Setup formatting
        axes.set_title(self.title_word + " " + general_title + " for Episode #" + str(self.episode.id))
        axes.set_xlabel(axis_label)
        axes.set_ylabel(self.bar_label + " per Step")
        if self.use_second_axis_scale and self.second_axis_label:
            axes2.set_ylabel(self.second_axis_label)
            axes2.grid(False)
            axes2.set_ybound(lower=0)

        if max_xscale_override:
            axes.set_xbound(0, max_xscale_override)
        else:
            axes.set_xbound(0, max(plot_x))

        if axes.has_data():
            if self.use_second_axis_scale:
                axes2.legend(frameon=True, framealpha=0.8, shadow=True)
            else:
                axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def _plot_any_additional_lines(self, axes, plot_x, wrap_point):
        all_extra_lines = self.get_any_additional_plot_lines(wrap_point)
        if all_extra_lines is not None:
            for extra_line in all_extra_lines:
                (colour, label, plot_y) = extra_line
                axes.plot(plot_x, plot_y, label=label, color=colour, linewidth=3)

    def get_plot_data_steps(self):

        steps = []

        for v in self.episode.events:
            steps.append(v.step)

        return np.array(steps)

    def get_plot_data_progresses(self):

        progresses = []

        for v in self.episode.events:
            progresses.append(v.progress)

        return np.array(progresses)

    # time_elapsed

    def get_plot_data_times(self):

        times = []

        for v in self.episode.events:
            times.append(v.time_elapsed)

        return np.array(times)

    def get_plot_data_distances(self):

        distances = []

        for v in self.episode.events:
            distances.append(v.total_distance_travelled)

        return np.array(distances)

    def get_plot_data_lap_positions(self):
        episode_start_position = self.episode.get_starting_position_as_percent_from_race_start(self.current_track)

        positions = []
        wrap_point = None

        for i, v in enumerate(self.episode.events):
            position = v.progress + episode_start_position
            if position > 100:
                position -= 100
                if not wrap_point:
                    wrap_point = i
            positions.append(position)

        if wrap_point:
            positions = positions[wrap_point:] + [math.nan] + positions[:wrap_point]

        return np.array(positions), wrap_point

    def get_plot_data_waypoints(self):
        waypoints = []
        wrap_point = None
        was_near_end = False

        for i, v in enumerate(self.episode.events):
            waypoint_id = v.closest_waypoint_index
            waypoints.append(waypoint_id)

            if not wrap_point and was_near_end and waypoint_id < self.current_track.get_number_of_waypoints() * 0.2:
                wrap_point = i

            was_near_end = waypoint_id > self.current_track.get_number_of_waypoints() * 0.8

        if wrap_point:
            waypoints = waypoints[wrap_point:] + [math.nan] + waypoints[:wrap_point]

        return np.array(waypoints), wrap_point

    def get_plot_bar_values_per_step(self, wrap_point):
        pass

    def get_plot_line_values_per_step(self, wrap_point):
        pass

    def get_any_additional_plot_lines(self, wrap_point):
        pass

    def additional_preparation_for_plots(self):
        pass
