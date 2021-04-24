#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.utils.lists import get_list_of_empty_lists

from src.analyze.core.controls import EpisodeCheckButtonControl, StatsControl


class AnalyzeRewardsPerWaypoint(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self._stats_control = StatsControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._stats_control.add_to_control_frame()

    def add_plots(self):
        if self.all_episodes:
            axes: Axes = self.graph_figure.add_subplot()
            self.plot_rewards_per_waypoint(axes)

    def plot_rewards_per_waypoint(self, axes: Axes):
        # Plot data

        num_waypoints = self.current_track.get_number_of_waypoints()

        if self.all_episodes and self._episodes_control.show_all():
            if self._stats_control.show_median():
                add_plot_for_rewards_per_waypoint(axes, "All - Median", self.all_episodes, np.median, "C5", num_waypoints)
            if self._stats_control.show_mean():
                add_plot_for_rewards_per_waypoint(axes, "All - Mean", self.all_episodes, np.mean, "C6", num_waypoints)
            if self._stats_control.show_best():
                add_plot_for_rewards_per_waypoint(axes, "All - Best", self.all_episodes, np.max, "C7", num_waypoints)
            if self._stats_control.show_worst():
                add_plot_for_rewards_per_waypoint(axes, "All - Worst", self.all_episodes, np.min, "C8", num_waypoints)
        if self.filtered_episodes and self._episodes_control.show_filtered():
            if self._stats_control.show_median():
                add_plot_for_rewards_per_waypoint(axes, "Filtered - Median", self.filtered_episodes, np.median, "C1", num_waypoints)
            if self._stats_control.show_mean():
                add_plot_for_rewards_per_waypoint(axes, "Filtered - Mean", self.filtered_episodes, np.mean, "C2", num_waypoints)
            if self._stats_control.show_best():
                add_plot_for_rewards_per_waypoint(axes, "Filtered - Best", self.filtered_episodes, np.max, "C3", num_waypoints)
            if self._stats_control.show_worst():
                add_plot_for_rewards_per_waypoint(axes, "Filtered - Worst", self.filtered_episodes, np.min, "C4", num_waypoints)

        # Format the plot
        axes.set_title("Rewards per Waypoint")
        axes.set_xlabel("Waypoint")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


def get_plot_data_for_rewards_per_waypoint(episodes, stat_method, num_waypoints):

    rewards = get_list_of_empty_lists(num_waypoints)

    for e in episodes:
        for v in e.events:
            rewards[v.closest_waypoint_index].append(v.reward)

    plot_waypoints = np.arange(0, num_waypoints)
    plot_rewards = np.zeros(num_waypoints)

    for i, r in enumerate(rewards):
        if r:
            plot_rewards[i] = stat_method(r)
        else:
            plot_rewards[i] = None

    return plot_waypoints, plot_rewards


def add_plot_for_rewards_per_waypoint(axes: Axes, label, episodes, stat_method, colour, num_waypoints):
    (plot_x, plot_y) = get_plot_data_for_rewards_per_waypoint(episodes, stat_method, num_waypoints)
    axes.plot(plot_x, plot_y, color=colour, label=label)
