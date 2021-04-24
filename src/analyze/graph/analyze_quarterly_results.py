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
from src.episode.episodes_plot_data import get_lap_times_per_quarter
from src.utils.lists import get_list_of_empty_lists

from src.analyze.core.controls import EpisodeRadioButtonControl


class AnalyzeQuarterlyResults(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self.episode_control.add_to_control_frame()

    def add_plots(self):
        if self.episode_control.show_all():
            episodes = self.all_episodes
        elif self.episode_control.show_filtered():
            episodes = self.filtered_episodes
        else:
            episodes = None

        gs = GridSpec(3, 4, left=0.03, right=0.97, bottom=0.03, top=0.92, hspace=0.35)

        self.plot_minimum_percents(episodes, gs, 10, 0, 0)
        self.plot_minimum_percents(episodes, gs, 25, 0, 1)
        self.plot_minimum_percents(episodes, gs, 33, 0, 2)
        self.plot_minimum_percents(episodes, gs, 50, 0, 3)

        self.plot_percent_stat(episodes, gs, np.mean, 1, 0)
        self.plot_percent_stat(episodes, gs, np.median, 1, 1)

        self.plot_episode_reward_stat(episodes, gs, np.mean, 1, 2)
        self.plot_episode_reward_stat(episodes, gs, np.median, 1, 3)

        self.plot_minimum_percents(episodes, gs, 100, 2, 0)

        self.plot_lap_times_stat(episodes, gs, np.median, 2, 1)

    def plot_minimum_percents(self, episodes, gs, minimum_percent, graph_x, graph_y):
        axes :Axes = self.graph_figure.add_subplot(gs[graph_x, graph_y])

        if minimum_percent < 100:
            axes.set_title("Progress >= " + str(minimum_percent) + "%")
        else:
            axes.set_title("Full Laps")

        axes.get_xaxis().set_ticklabels([])
        axes.get_yaxis().set_ticklabels([])

        if not episodes:
            return

        plot_x = np.array([1, 2, 3, 4])
        plot_y = get_data_minimum_percents(episodes, minimum_percent)

        bars = axes.bar(plot_x, plot_y, color="C1")

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        max_value = np.max(plot_y)
        min_value = np.min(plot_y)
        if max_value != min_value:
            border = 0.15 * (max_value - min_value)
            axes.set_ybound(max(0.0, min_value - border), max_value + border)

    def plot_percent_stat(self, episodes, gs, stat_method, graph_x, graph_y):
        axes :Axes = self.graph_figure.add_subplot(gs[graph_x, graph_y])

        axes.set_title("Progress % " + stat_method.__name__)

        axes.get_xaxis().set_ticklabels([])
        axes.get_yaxis().set_ticklabels([])

        if not episodes:
            return

        plot_x = np.array([1, 2, 3, 4])
        plot_y = get_data_percent_stat(episodes, stat_method)

        bars = axes.bar(plot_x, plot_y, color="C1")

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes.annotate(str(round(height, 1)),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        max_value = np.max(plot_y)
        min_value = np.min(plot_y)
        if max_value != min_value:
            border = 0.15 * (max_value - min_value)
            axes.set_ybound(max(0.0, min_value - border), max_value + border)

    def plot_episode_reward_stat(self, episodes, gs, stat_method, graph_x, graph_y):
        axes :Axes = self.graph_figure.add_subplot(gs[graph_x, graph_y])

        axes.set_title("Reward " + stat_method.__name__)

        axes.get_xaxis().set_ticklabels([])
        axes.get_yaxis().set_ticklabels([])

        if not episodes:
            return

        plot_x = np.array([1, 2, 3, 4])
        plot_y = get_data_episode_reward_stat(episodes, stat_method)

        bars = axes.bar(plot_x, plot_y, color="C1")

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                if np.max(plot_y) > 5000:
                    pretty_value = str(round(height/1000)) + "k"
                else:
                    pretty_value = str(round(height))

                axes.annotate(pretty_value,
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        max_value = np.max(plot_y)
        min_value = np.min(plot_y)
        if max_value != min_value:
            border = 0.15 * (max_value - min_value)
            axes.set_ybound(max(0.0, min_value - border), max_value + border)

    def plot_lap_times_stat(self, episodes, gs, stat_method, graph_x, graph_y):
        axes :Axes = self.graph_figure.add_subplot(gs[graph_x, graph_y])

        axes.set_title("Lap Time " + stat_method.__name__)

        axes.get_xaxis().set_ticklabels([])
        axes.get_yaxis().set_ticklabels([])

        if not episodes:
            return

        plot_x = np.array([1, 2, 3, 4])
        plot_y = get_data_lap_times_stat(episodes, stat_method)

        bars = axes.bar(plot_x, plot_y, color="C1")

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes.annotate(round(height, 1),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        max_value = np.max(plot_y)
        min_value = np.min(plot_y)
        if max_value != min_value:
            border = 0.15 * (max_value - min_value)
            axes.set_ybound(max(0.0, min_value - border), max_value + border)


def get_data_minimum_percents(episodes, minimum_percent):
    result = np.zeros((4,), dtype=int)
    for e in episodes:
        if e.percent_complete >= minimum_percent:
            result[e.quarter-1] += 1

    return result


def get_data_percent_stat(episodes, stat_method):
    # Gather all the percentage completions into a list per iteration
    quarterly_percent_complete = get_list_of_empty_lists(4)
    for e in episodes:
        quarterly_percent_complete[e.quarter - 1].append(e.percent_complete)

    plot_data = np.zeros(4)
    for i, ipc in enumerate(quarterly_percent_complete):
        if ipc:
            plot_data[i] = stat_method(np.array(ipc))

    return plot_data


def get_data_episode_reward_stat(episodes, stat_method):
    # Gather all the percentage completions into a list per iteration
    quarterly_total_rewards = get_list_of_empty_lists(4)
    for e in episodes:
        quarterly_total_rewards[e.quarter - 1].append(e.total_reward)

    plot_data = np.zeros(4)
    for i, ipc in enumerate(quarterly_total_rewards):
        if ipc:
            plot_data[i] = stat_method(np.array(ipc))

    return plot_data


def get_data_lap_times_stat(episodes, stat_method):
    plot_data = np.zeros(4)
    for i, times in enumerate(get_lap_times_per_quarter(episodes)):
        if times.any():
            plot_data[i] = stat_method(np.array(times))

    return plot_data
