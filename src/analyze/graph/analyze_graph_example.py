import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MultipleLocator

from src.analyze.graph.graph_analyzer import GraphAnalyzer


class AnalyzeGraphExample(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)


    def build_control_frame(self, control_frame):

        self.hello_info = tk.Label(control_frame, text="Hello")
        self.hello_info.grid(column=0, row=10, pady=20)


    def add_plots(self):
        if not self.filtered_episodes or not self.all_episodes:
            return

        # gs = GridSpec(1, 2)
        # axes_left :Axes = self.graph_figure.add_subplot(gs[0, 0])
        # axes_right :Axes = self.graph_figure.add_subplot(gs[0, 1])
        # t = np.arange(0, 10, .01)
        # axes_left.plot(t, 2 * np.sin(2 * np.pi * t))

        axes_right = self.graph_figure.add_subplot()

        # Plot data
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.filtered_episodes, np.median)
        axes_right.plot(plot_x, plot_y, label="Filtered - Median")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.filtered_episodes, np.mean)
        axes_right.plot(plot_x, plot_y, label="Filtered - Mean")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.filtered_episodes, np.max)
        axes_right.plot(plot_x, plot_y, label="Filtered - Best")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.filtered_episodes, np.min)
        axes_right.plot(plot_x, plot_y, label="Filtered - Worst")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.all_episodes, np.median)
        axes_right.plot(plot_x, plot_y, label="All - Median")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.all_episodes, np.mean)
        axes_right.plot(plot_x, plot_y, label="All - Mean")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.all_episodes, np.max)
        axes_right.plot(plot_x, plot_y, label="All - Best")
        (plot_x, plot_y) = get_plot_data_for_iteration_versus_percent_complete(self.all_episodes, np.min)
        axes_right.plot(plot_x, plot_y, label="All - Worst")

        # Format the plot
        axes_right.legend()
        axes_right.set_title("Track Completion")
        axes_right.set_xlabel("Training Iteration")
        axes_right.set_ybound(0, 105)
        axes_right.yaxis.set_major_formatter(PercentFormatter())
        axes_right.xaxis.set_major_locator(MultipleLocator(5))
        axes_right.xaxis.set_minor_locator(MultipleLocator(1))


# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list

def get_plot_data_for_iteration_versus_percent_complete(episodes, stat_method):
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

