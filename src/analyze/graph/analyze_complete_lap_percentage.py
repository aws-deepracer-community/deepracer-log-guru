import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes
from matplotlib.ticker import PercentFormatter
from matplotlib.ticker import MultipleLocator

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.utils.lists import get_list_of_empty_lists


class AnalyzeCompleteLapPercentage(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_all = tk.BooleanVar()
        self.show_filtered = tk.BooleanVar()
        self.show_evaluations = tk.BooleanVar()

        self.show_filtered.set(True)
        self.show_evaluations.set(True)


    def build_control_frame(self, control_frame):

        episodes_group = tk.LabelFrame(control_frame, text="Episodes", padx=5, pady=5)
        episodes_group.pack()

        tk.Checkbutton(
            episodes_group, text="All Episodes",
            variable=self.show_all,
            command=self.guru_parent_redraw).grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="Filtered Episodes",
            variable=self.show_filtered,
            command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)

        tk.Checkbutton(
            episodes_group, text="Evaluations",
            variable=self.show_evaluations,
            command=self.guru_parent_redraw).grid(column=0, row=2, pady=5, padx=5)

    def add_plots(self):
        if not self.all_episodes:
            return

        axes :Axes = self.graph_figure.add_subplot()


        # Plot data

        if self.show_all.get():
            add_plot_for_episodes(axes, "All Episodes", self.all_episodes, "C1")

        if self.filtered_episodes and self.show_filtered.get():
            add_plot_for_episodes(axes, "Filtered Episodes", self.filtered_episodes, "C2")

        if self.show_evaluations.get():
            add_plot_for_evaluations(axes, "Evaluations", self.evaluation_phases, "C3")

        # Format the plot
        axes.set_title("Complete Lap Percentage")
        axes.set_xlabel("Training Iteration")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)



def get_plot_data_for_episodes(episodes):
    iteration_count = episodes[-1].iteration + 1

    # Gather all the percentage completions into a list per iteration
    iteration_percent_complete = get_list_of_empty_lists(iteration_count)
    for e in episodes:
        iteration_percent_complete[e.iteration].append(e.percent_complete)

    # Build the plot data using numpy to get the average percent for each iteration
    plot_iteration = np.arange(0, iteration_count)
    plot_data = np.zeros(iteration_count)
    for i, ir in enumerate(iteration_percent_complete):
        if ir:
            plot_data[i] = ir.count(100) / len(ir) * 100
        else:
            plot_data[i] = np.nan

    return plot_iteration, plot_data

def add_plot_for_episodes(axes :Axes, label, episodes, colour):
    (plot_x, plot_y) = get_plot_data_for_episodes(episodes)
    axes.plot(plot_x, plot_y, colour, label=label)



def get_plot_data_for_evaluations(evaluation_phases):
    iteration_count = len(evaluation_phases)
    plot_iteration = np.arange(0, iteration_count)
    plot_data = np.zeros(iteration_count)

    for i, eval in enumerate(evaluation_phases):
        eval_list = list(eval.progresses)
        plot_data[i] = eval_list.count(100) / len(eval_list) * 100

    return plot_iteration, plot_data

def add_plot_for_evaluations(axes :Axes, label, evaluation_phases, colour):
    (plot_x, plot_y) = get_plot_data_for_evaluations(evaluation_phases)
    axes.plot(plot_x, plot_y, colour, label=label)
