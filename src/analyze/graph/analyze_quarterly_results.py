import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer

SHOW_ALL = 1
SHOW_FILTERED = 2

class AnalyzeQuarterlyResults(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_what = tk.IntVar(value=SHOW_ALL)

    def build_control_frame(self, control_frame):

        episodes_group = tk.LabelFrame(control_frame, text="Episodes", padx=5, pady=5)
        episodes_group.grid(column=0, row=0, pady=5, padx=5)

        tk.Radiobutton(
            episodes_group, text="All",
            variable=self.show_what, value=SHOW_ALL,
            command=self.guru_parent_redraw).grid(column=0, row=0, pady=5, padx=5)

        tk.Radiobutton(
            episodes_group, text="Filtered",
            variable=self.show_what, value=SHOW_FILTERED,
            command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)


    def add_plots(self):
        if self.show_what.get() == SHOW_ALL:
            episodes = self.all_episodes
        else:
            episodes = self.filtered_episodes

        if not episodes:
            return

        gs = GridSpec(2, 4)

        self.plot_percents(episodes, gs, 10, 0, 0)
        self.plot_percents(episodes, gs, 25, 0, 1)
        self.plot_percents(episodes, gs, 33, 0, 2)
        self.plot_percents(episodes, gs, 50, 0, 3)
        self.plot_percents(episodes, gs, 100, 1, 0)




    def plot_percents(self, episodes, gs, minimum_percent, graph_x, graph_y):
        axes :Axes = self.graph_figure.add_subplot(gs[graph_x, graph_y])

        plot_x = np.array([1, 2, 3, 4])
        plot_y = get_data_percent_progress(episodes, minimum_percent)
        # replace_zero_with_none(plot_y)

        bars = axes.bar(plot_x, plot_y, color="C1")

        for bar in bars:
            height = bar.get_height()
            if height > 0:
                axes.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 2),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        if minimum_percent < 100:
            axes.set_title("Progress >= " + str(minimum_percent) + "%")
        else:
            axes.set_title("Full Laps")

        axes.get_xaxis().set_ticklabels([])
        axes.get_yaxis().set_ticklabels([])

        max_value = np.max(plot_y)
        min_value = np.min(plot_y)
        if max_value != min_value:
            border = 0.15 * (max_value - min_value)
            axes.set_ybound(max(0.0, min_value - border), max_value + border)


def get_data_percent_progress(episodes, minimum_percent):
    result = np.zeros((4,), dtype=int)
    for e in episodes:
        if e.percent_complete >= minimum_percent:
            result[e.quarter-1] += 1

    return result


def replace_zero_with_none(plot_data):
    for i, d in enumerate(plot_data):
        if d == 0:
            plot_data[i] = None
