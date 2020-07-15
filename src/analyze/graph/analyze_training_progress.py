import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MultipleLocator

from src.analyze.graph.graph_analyzer import GraphAnalyzer


class AnalyzeTrainingProgress(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_all = tk.BooleanVar()
        self.show_filtered = tk.BooleanVar()

        self.show_mean = tk.BooleanVar()
        self.show_median = tk.BooleanVar()
        self.show_best = tk.BooleanVar()
        self.show_worst = tk.BooleanVar()

        self.show_filtered.set(True)
        self.show_mean.set(True)
        self.show_best.set(True)



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

        stats_group = tk.LabelFrame(control_frame, text="Stats", padx=5, pady=5)
        stats_group.grid(column=0, row=1, pady=5, padx=5)

        tk.Checkbutton(
            stats_group, text="Mean",
            variable=self.show_mean,
            command=self.guru_parent_redraw).grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            stats_group, text="Median",
            variable=self.show_median,
            command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)

        tk.Checkbutton(
            stats_group, text="Best",
            variable=self.show_best,
            command=self.guru_parent_redraw).grid(column=0, row=2, pady=5, padx=5)

        tk.Checkbutton(
            stats_group, text="Worst",
            variable=self.show_worst,
            command=self.guru_parent_redraw).grid(column=0, row=3, pady=5, padx=5)


    def add_plots(self):
        if not self.all_episodes:
            return

        gs = GridSpec(1, 2)
        axes_left :Axes = self.graph_figure.add_subplot(gs[0, 0])
        axes_right :Axes = self.graph_figure.add_subplot(gs[0, 1])

        self.create_plot_iteration_vs_total_reward(axes_left)
        self.create_plot_iteration_vs_percent_complete(axes_right)

    def create_plot_iteration_vs_total_reward(self, axes):
        # Plot data

        if self.show_all.get():
            if self.show_median.get():
                add_plot_iteration_vs_total_reward(axes, "All - Median", self.all_episodes, np.median, "C5")
            if self.show_mean.get():
                add_plot_iteration_vs_total_reward(axes, "All - Mean", self.all_episodes, np.mean, "C6")
            if self.show_best.get():
                add_plot_iteration_vs_total_reward(axes, "All - Best", self.all_episodes, np.max, "C7")
            if self.show_worst.get():
                add_plot_iteration_vs_total_reward(axes, "All - Worst", self.all_episodes, np.min, "C8")

        if self.filtered_episodes and self.show_filtered.get():
            if self.show_median.get():
                add_plot_iteration_vs_total_reward(axes, "Filtered - Median", self.filtered_episodes, np.median, "C1")
            if self.show_mean.get():
                add_plot_iteration_vs_total_reward(axes, "Filtered - Mean", self.filtered_episodes, np.mean, "C2")
            if self.show_best.get():
                add_plot_iteration_vs_total_reward(axes, "Filtered - Best", self.filtered_episodes, np.max, "C3")
            if self.show_worst.get():
                add_plot_iteration_vs_total_reward(axes, "Filtered - Worst", self.filtered_episodes, np.min, "C4")

        # Format the plot
        axes.set_title("Total Reward")
        axes.set_xlabel("Training Iteration")

        if self.log_meta:
            best = self.log_meta.episode_stats.best_reward
            worst = self.log_meta.episode_stats.worst_reward
            if best != worst:
                border = 0.02 * (best - worst)
                axes.set_ybound(worst - border, best + border)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def create_plot_iteration_vs_percent_complete(self, axes):

        # Plot data
        if self.show_all.get():
            if self.show_median.get():
                add_plot_iteration_vs_percent_complete(axes, "All - Median", self.all_episodes, np.median, "C5")
            if self.show_mean.get():
                add_plot_iteration_vs_percent_complete(axes, "All - Mean", self.all_episodes, np.mean, "C6")
            if self.show_best.get():
                add_plot_iteration_vs_percent_complete(axes, "All - Best", self.all_episodes, np.max, "C7")
            if self.show_worst.get():
                add_plot_iteration_vs_percent_complete(axes, "All - Worst", self.all_episodes, np.min, "C8")

        if self.filtered_episodes and self.show_filtered.get():
            if self.show_median.get():
                add_plot_iteration_vs_percent_complete(axes, "Filtered - Median", self.filtered_episodes, np.median, "C1")
            if self.show_mean.get():
                add_plot_iteration_vs_percent_complete(axes, "Filtered - Mean", self.filtered_episodes, np.mean, "C2")
            if self.show_best.get():
                add_plot_iteration_vs_percent_complete(axes, "Filtered - Best", self.filtered_episodes, np.max, "C3")
            if self.show_worst.get():
                add_plot_iteration_vs_percent_complete(axes, "Filtered - Worst", self.filtered_episodes, np.min, "C4")

        # Format the plot
        axes.set_title("Track Completion")
        axes.set_xlabel("Training Iteration")
        axes.set_ybound(0, 105)
        axes.yaxis.set_major_formatter(PercentFormatter())

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)



# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list


def get_plot_data_iteration_vs_total_reward(episodes, stat_method):
    iteration_count = episodes[-1].iteration + 1

    # Gather all the percentage completions into a list per iteration
    iteration_reward = get_list_of_empty_lists(iteration_count)
    for e in episodes:
        iteration_reward[e.iteration].append(e.total_reward)

    # Build the plot data using numpy to get the average percent for each iteration
    plot_iteration = np.arange(0, iteration_count)
    plot_total_reward = np.zeros(iteration_count)
    for i, ir in enumerate(iteration_reward):
        if ir:
            plot_total_reward[i] = stat_method(np.array(ir))
        else:
            plot_total_reward[i] = np.nan

    return plot_iteration, plot_total_reward

def add_plot_iteration_vs_total_reward(axes :Axes, label, episodes, stat_method, colour):
    (plot_x, plot_y) = get_plot_data_iteration_vs_total_reward(episodes, stat_method)
    axes.plot(plot_x, plot_y, colour, label=label)


def get_plot_data_iteration_vs_percent_complete(episodes, stat_method):
    iteration_count = episodes[-1].iteration + 1

    # Gather all the percentage completions into a list per iteration
    iteration_percent_complete = get_list_of_empty_lists(iteration_count)
    for e in episodes:
        iteration_percent_complete[e.iteration].append(e.percent_complete)

    # Build the plot data using numpy to get the average percent for each iteration
    plot_iteration = np.arange(0, iteration_count)
    plot_percent_complete = np.zeros(iteration_count)
    for i, ipc in enumerate(iteration_percent_complete):
        if ipc:
            plot_percent_complete[i] = stat_method(np.array(ipc))
        else:
            plot_percent_complete[i] = np.nan

    return plot_iteration, plot_percent_complete

def add_plot_iteration_vs_percent_complete(axes :Axes, label, episodes, stat_method, colour):
    (plot_x, plot_y) = get_plot_data_iteration_vs_percent_complete(episodes, stat_method)
    axes.plot(plot_x, plot_y, colour, label=label)
