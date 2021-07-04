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
from src.configuration.config_manager import ConfigManager
from src.event.event_meta import Event
from src.utils.lists import get_list_of_empty_lists

from src.analyze.core.controls import EpisodeCheckButtonControl, StatsControl, ShowLastStepControl, RewardTypeControl


class AnalyzeRewardsPerWaypoint(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame,
                 config_manager: ConfigManager):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self._reward_type_control = RewardTypeControl(guru_parent_redraw, control_frame, config_manager)
        self._stats_control = StatsControl(guru_parent_redraw, control_frame)
        self._showLastStepControl = ShowLastStepControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._episodes_control.add_to_control_frame()
        self._reward_type_control.add_to_control_frame()
        self._stats_control.add_to_control_frame()
        self._showLastStepControl.add_to_control_frame()

    def add_plots(self):
        if self.all_episodes:
            grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
            axes: Axes = self.graph_figure.add_subplot(grid_spec[0])
            self.plot_rewards_per_waypoint(axes)

    def plot_rewards_per_waypoint(self, axes: Axes):
        # Plot data

        num_waypoints = self.current_track.get_number_of_waypoints()

        if self.all_episodes and self._episodes_control.show_all():
            if self._stats_control.show_median():
                self.add_plot_for_rewards_per_waypoint(axes, "All - Median", self.all_episodes, np.median, "C5", num_waypoints)
            if self._stats_control.show_mean():
                self.add_plot_for_rewards_per_waypoint(axes, "All - Mean", self.all_episodes, np.mean, "C6", num_waypoints)
            if self._stats_control.show_best():
                self.add_plot_for_rewards_per_waypoint(axes, "All - Best", self.all_episodes, np.max, "C7", num_waypoints)
            if self._stats_control.show_worst():
                self.add_plot_for_rewards_per_waypoint(axes, "All - Worst", self.all_episodes, np.min, "C8", num_waypoints)
        if self.filtered_episodes and self._episodes_control.show_filtered():
            if self._stats_control.show_median():
                self.add_plot_for_rewards_per_waypoint(axes, "Filtered - Median", self.filtered_episodes, np.median, "C1", num_waypoints)
            if self._stats_control.show_mean():
                self.add_plot_for_rewards_per_waypoint(axes, "Filtered - Mean", self.filtered_episodes, np.mean, "C2", num_waypoints)
            if self._stats_control.show_best():
                self.add_plot_for_rewards_per_waypoint(axes, "Filtered - Best", self.filtered_episodes, np.max, "C3", num_waypoints)
            if self._stats_control.show_worst():
                self.add_plot_for_rewards_per_waypoint(axes, "Filtered - Worst", self.filtered_episodes, np.min, "C4", num_waypoints)

        # Format the plot
        if self._reward_type_control.measure_event_reward():
            axes.set_title("Event Reward per Waypoint")
        elif self._reward_type_control.measure_discounted_future_reward():
            axes.set_title("Future Reward per Waypoint")
        elif self._reward_type_control.measure_new_event_reward():
            axes.set_title("New Event Reward per Waypoint")
        elif self._reward_type_control.measure_new_discounted_future_reward():
            axes.set_title("New Future Reward per Waypoint")
        else:
            assert self._reward_type_control.measure_alternate_discounted_future_reward()
            index = self._reward_type_control.get_alternate_discount_factor()
            axes.set_title("Future Reward per Waypoint Using Alternate DF = " + str(index))

        axes.set_xlabel("Waypoint")
        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def get_plot_data_for_rewards_per_waypoint(self, episodes, stat_method, num_waypoints):

        rewards = get_list_of_empty_lists(num_waypoints)

        for e in episodes:
            if self._showLastStepControl.show_last_step():
                events = e.events
            else:
                events = e.events[:-1]

            v: Event
            for v in events:
                if self._reward_type_control.measure_event_reward():
                    rewards[v.closest_waypoint_index].append(v.reward)
                elif self._reward_type_control.measure_discounted_future_reward():
                    rewards[v.closest_waypoint_index].append(v.discounted_future_rewards[0])
                elif self._reward_type_control.measure_new_event_reward():
                    rewards[v.closest_waypoint_index].append(v.new_reward)
                elif self._reward_type_control.measure_new_discounted_future_reward():
                    rewards[v.closest_waypoint_index].append(v.new_discounted_future_reward)
                else:
                    assert self._reward_type_control.measure_alternate_discounted_future_reward()
                    index = self._reward_type_control.get_alternate_discount_factor_index()
                    rewards[v.closest_waypoint_index].append(v.discounted_future_rewards[index])

        plot_waypoints = np.arange(0, num_waypoints)
        plot_rewards = np.zeros(num_waypoints)

        for i, r in enumerate(rewards):
            if r:
                plot_rewards[i] = stat_method(r)
            else:
                plot_rewards[i] = None

        return plot_waypoints, plot_rewards

    def add_plot_for_rewards_per_waypoint(self, axes: Axes, label, episodes, stat_method, colour, num_waypoints):
        (plot_x, plot_y) = self.get_plot_data_for_rewards_per_waypoint(episodes, stat_method, num_waypoints)
        axes.plot(plot_x, plot_y, color=colour, label=label)
