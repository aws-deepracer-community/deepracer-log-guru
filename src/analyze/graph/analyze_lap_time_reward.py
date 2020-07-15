import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer

MIN_PERCENT_FOR_GOOD_PREDICTION = 3

class AnalyzeLapTimeReward(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_all = tk.BooleanVar()
        self.show_filtered = tk.BooleanVar()
        self.show_filtered_predictions = tk.BooleanVar()

        self.show_filtered.set(True)

        self.min_time = None
        self.max_time = None

        self.min_total_reward = None
        self.max_total_reward = None

        self.min_average_reward = None
        self.max_average_reward = None

    def build_control_frame(self, control_frame):

        episodes_group = tk.LabelFrame(control_frame, text="Episodes", padx=5, pady=5)
        episodes_group.grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="All",
            variable=self.show_all,
            command=self.guru_parent_redraw).grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="Filtered",
            variable=self.show_filtered,
            command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="Filtered\nPredictions",
            variable=self.show_filtered_predictions,
            command=self.guru_parent_redraw).grid(column=0, row=2, pady=5, padx=5)


    def add_plots(self):
        if not self.all_episodes:
            return

        gs = GridSpec(1, 2)
        axes_left :Axes = self.graph_figure.add_subplot(gs[0, 0])
        axes_right :Axes = self.graph_figure.add_subplot(gs[0, 1])

        self.plot_for_total_reward(axes_left)
        self.plot_for_average_reward(axes_right)

    def plot_for_total_reward(self, axes :Axes):
        # Plot data

        if self.filtered_episodes and self.show_filtered_predictions.get():
            add_plot_for_total_reward_predictions(axes, "Filtered\nPredictions", self.filtered_episodes, "C3")

        if self.show_all.get():
            add_plot_for_total_reward(axes, "All", self.all_episodes, "C1")

        if self.filtered_episodes and self.show_filtered.get():
            add_plot_for_total_reward(axes, "Filtered", self.filtered_episodes, "C2")

        # Format the plot
        axes.set_title("Lap Time Versus Total Reward")
        axes.set_xlabel("Lap Time")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

        xborder = get_axis_border(self.min_time, self.max_time)
        axes.set_xbound(self.min_time - xborder, self.max_time + xborder)

        yborder = get_axis_border(self.min_total_reward, self.max_total_reward)
        axes.set_ybound(self.min_total_reward - yborder, self.max_total_reward + yborder)

    def plot_for_average_reward(self, axes: Axes):
        # Plot data

        if self.filtered_episodes and self.show_filtered_predictions.get():
            add_plot_for_average_reward_predictions(axes, "Filtered\nPredictions", self.filtered_episodes, "C3")

        if self.show_all.get():
            add_plot_for_average_reward(axes, "All", self.all_episodes, "C1")

        if self.filtered_episodes and self.show_filtered.get():
            add_plot_for_average_reward(axes, "Filtered", self.filtered_episodes, "C2")

        # Format the plot
        axes.set_title("Lap Time Versus Average Reward")
        axes.set_xlabel("Lap Time")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


        xborder = get_axis_border(self.min_time, self.max_time)
        axes.set_xbound(self.min_time - xborder, self.max_time + xborder)

        yborder = get_axis_border(self.min_average_reward, self.max_average_reward)
        axes.set_ybound(self.min_average_reward - yborder, self.max_average_reward + yborder)

    def warning_all_episodes_changed(self):
        if not self.all_episodes:
            return

        (plot_time, plot_total_reward) = get_plot_data_for_total_reward(self.all_episodes)
        (_, plot_average_reward) = get_plot_data_for_average_reward(self.all_episodes)

        if not plot_time.any():
            (plot_time, plot_total_reward) = get_plot_data_for_total_reward_predictions(self.all_episodes)
            (_, plot_average_reward) = get_plot_data_for_average_reward_predictions(self.all_episodes)

        self.min_time = np.min(plot_time)
        self.max_time = np.max(plot_time)

        self.min_average_reward = np.min(plot_average_reward)
        self.max_average_reward = np.max(plot_average_reward)

        self.min_total_reward = np.min(plot_total_reward)
        self.max_total_reward = np.max(plot_total_reward)




# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list


def get_plot_data_for_total_reward(episodes):

    plot_time = []
    plot_reward = []

    for e in episodes:
        if e.lap_complete:
            plot_time.append(e.time_taken)
            plot_reward.append(e.total_reward)

    return np.array(plot_time), np.array(plot_reward)

def add_plot_for_total_reward(axes :Axes, label, episodes, colour):
    (plot_x, plot_y) = get_plot_data_for_total_reward(episodes)
    axes.plot(plot_x, plot_y, "o", color=colour, label=label)


def get_plot_data_for_average_reward(episodes):

    plot_time = []
    plot_reward = []

    for e in episodes:
        if e.lap_complete:
            plot_time.append(e.time_taken)
            plot_reward.append(e.average_reward)

    return np.array(plot_time), np.array(plot_reward)

def add_plot_for_average_reward(axes :Axes, label, episodes, colour):
    (plot_x, plot_y) = get_plot_data_for_average_reward(episodes)
    axes.plot(plot_x, plot_y, "o", color=colour, label=label)

def get_plot_data_for_total_reward_predictions(episodes):
    plot_time = []
    plot_reward = []

    for e in episodes:
        if not e.lap_complete and e.percent_complete >= MIN_PERCENT_FOR_GOOD_PREDICTION:
            plot_time.append(e.lap_time)
            plot_reward.append(e.lap_reward)

    return np.array(plot_time), np.array(plot_reward)

def add_plot_for_total_reward_predictions(axes: Axes, label, episodes, colour):
    (plot_x, plot_y) = get_plot_data_for_total_reward_predictions(episodes)
    axes.plot(plot_x, plot_y, ".", color=colour, label=label)

def get_plot_data_for_average_reward_predictions(episodes):
    plot_time = []
    plot_reward = []

    for e in episodes:
        if not e.lap_complete and e.percent_complete >= MIN_PERCENT_FOR_GOOD_PREDICTION:
            plot_time.append(e.lap_time)
            plot_reward.append(e.average_reward)

    return np.array(plot_time), np.array(plot_reward)

def add_plot_for_average_reward_predictions(axes: Axes, label, episodes, colour):
    (plot_x, plot_y) = get_plot_data_for_average_reward_predictions(episodes)
    axes.plot(plot_x, plot_y, ".", color=colour, label=label)

def get_axis_border(min_value, max_value):
    if max_value > min_value:
        return (max_value - min_value) * 0.02
    else:
        return 0.1 * max_value


