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
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeCheckButtonControl


class AnalyzeRewardDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()

    def add_plots(self):
        if not self.all_episodes:
            return

        gs = GridSpec(1, 3, left=0.02, right=0.98, bottom=0.08, top=0.92)
        axes_left: Axes = self.graph_figure.add_subplot(gs[0, 0])
        axes_middle: Axes = self.graph_figure.add_subplot(gs[0, 1])
        axes_right: Axes = self.graph_figure.add_subplot(gs[0, 2])

        self.plot_data(axes_left, get_plot_data_for_total_reward, "Total Reward per Episode")
        self.plot_data(axes_middle, get_plot_data_for_average_reward, "Average Reward per Episode")
        self.plot_data(axes_right, get_plot_data_for_reward_per_step, "Reward per Step")

    def plot_data(self, axes: Axes, get_data_method, title):
        show_filtered = self.filtered_episodes and self._episodes_control.show_filtered()
        show_all = self.all_episodes and self._episodes_control.show_all()

        if show_all and show_filtered:
            (plot_data_all) = get_data_method(self.all_episodes)
            (plot_data_filtered) = get_data_method(self.filtered_episodes)
            axes.hist([plot_data_all, plot_data_filtered], density=True, label=["All", "Filtered"], color=["C1", "C2"])
        elif show_all:
            (plot_data_all) = get_data_method(self.all_episodes)
            axes.hist(plot_data_all, label="All", color="C1")
        elif show_filtered:
            (plot_data_filtered) = get_data_method(self.filtered_episodes)
            axes.hist(plot_data_filtered, label="Filtered", color="C2")

        # Format the plot
        axes.set_title(title)
        axes.set_xlabel("Reward")
        axes.get_yaxis().set_ticklabels([])

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


def get_plot_data_for_total_reward(episodes):

    plot_reward = []

    for e in episodes:
        plot_reward.append(e.total_reward)

    return np.array(plot_reward)


def add_plot_for_total_reward(axes: Axes, label, episodes, colour):
    (plot_data) = get_plot_data_for_total_reward(episodes)
    axes.hist(plot_data, label=label, color=colour)


def get_plot_data_for_average_reward(episodes):

    plot_reward = []

    for e in episodes:
        plot_reward.append(e.average_reward)

    return np.array(plot_reward)


def add_plot_for_average_reward(axes: Axes, label, episodes, colour):
    (plot_data) = get_plot_data_for_average_reward(episodes)
    axes.hist(plot_data, label=label, color=colour)


def get_plot_data_for_reward_per_step(episodes):

    plot_reward = []

    for e in episodes:
        for v in e.events:
            plot_reward.append(v.reward)

    return np.array(plot_reward)




