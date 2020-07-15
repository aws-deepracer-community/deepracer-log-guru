import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer


class AnalyzeRewardDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_filtered = tk.BooleanVar()

        self.show_filtered.set(True)


    def build_control_frame(self, control_frame):

        episodes_group = tk.LabelFrame(control_frame, text="Episodes", padx=5, pady=5)
        episodes_group.grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="Filtered",
            variable=self.show_filtered,
            command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)

    def add_plots(self):
        if not self.all_episodes:
            return

        gs = GridSpec(1, 3)
        axes_left :Axes = self.graph_figure.add_subplot(gs[0, 0])
        axes_middle :Axes = self.graph_figure.add_subplot(gs[0, 1])
        axes_right :Axes = self.graph_figure.add_subplot(gs[0, 2])

        self.plot_for_total_reward(axes_left)
        self.plot_for_average_reward(axes_middle)
        self.plot_for_reward_per_step(axes_right)

    def plot_for_total_reward(self, axes :Axes):
        # Plot data

        (plot_data_all) = get_plot_data_for_total_reward(self.all_episodes)

        if self.filtered_episodes and self.show_filtered.get():
            (plot_data_filtered) = get_plot_data_for_total_reward(self.filtered_episodes)
            axes.hist([plot_data_all, plot_data_filtered], density=True, label=["All", "Filtered"], color=["C1", "C2"])
        else:
            axes.hist(plot_data_all, label="All", color="C1")

        # Format the plot
        axes.set_title("Total Reward per Episode")
        axes.set_xlabel("Reward")
        axes.get_yaxis().set_ticklabels([])

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def plot_for_average_reward(self, axes: Axes):
        # Plot data

        (plot_data_all) = get_plot_data_for_average_reward(self.all_episodes)

        if self.filtered_episodes and self.show_filtered.get():
            (plot_data_filtered) = get_plot_data_for_average_reward(self.filtered_episodes)
            axes.hist([plot_data_all, plot_data_filtered], density=True, label=["All", "Filtered"], color=["C1", "C2"])
        else:
            axes.hist(plot_data_all, label="All", color="C1")

        # Format the plot
        axes.set_title("Average Reward per Episode")
        axes.set_xlabel("Reward")
        axes.get_yaxis().set_ticklabels([])

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def plot_for_reward_per_step(self, axes: Axes):
        # Plot data

        (plot_data_all) = get_plot_data_for_reward_per_step(self.all_episodes)

        if self.filtered_episodes and self.show_filtered.get():
            (plot_data_filtered) = get_plot_data_for_reward_per_step(self.filtered_episodes)
            axes.hist([plot_data_all, plot_data_filtered], density=True,  label=["All","Filtered"], color=["C1","C2"])
        else:
            axes.hist(plot_data_all, label="All", color="C1")

        # Format the plot
        axes.set_title("Reward per Step")
        axes.set_xlabel("Reward")
        axes.get_yaxis().set_ticklabels([])

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list


def get_plot_data_for_total_reward(episodes):

    plot_reward = []

    for e in episodes:
        plot_reward.append(e.total_reward)

    return np.array(plot_reward)

def add_plot_for_total_reward(axes :Axes, label, episodes, colour):
    (plot_data) = get_plot_data_for_total_reward(episodes)
    axes.hist(plot_data, label=label, color=colour)


def get_plot_data_for_average_reward(episodes):

    plot_reward = []

    for e in episodes:
        plot_reward.append(e.average_reward)

    return np.array(plot_reward)

def add_plot_for_average_reward(axes :Axes, label, episodes, colour):
    (plot_data) = get_plot_data_for_average_reward(episodes)
    axes.hist(plot_data, label=label, color=colour)


def get_plot_data_for_reward_per_step(episodes):

    plot_reward = []

    for e in episodes:
        for v in e.events:
            plot_reward.append(v.reward)

    return np.array(plot_reward)





