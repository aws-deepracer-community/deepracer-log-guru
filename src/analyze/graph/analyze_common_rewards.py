import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer


class AnalyzeCommonRewards(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)



    def build_control_frame(self, control_frame):
        pass

    def add_plots(self):
        if not self.all_episodes:
            return

        gs = GridSpec(1, 2)
        axes_left :Axes = self.graph_figure.add_subplot(gs[0, 0])
        axes_right :Axes = self.graph_figure.add_subplot(gs[0, 1])

        self.plot_common_rewards(axes_left, self.all_episodes, "All", "C1")
        self.plot_common_rewards(axes_right, self.filtered_episodes, "Filtered", "C2")


    def plot_common_rewards(self, axes :Axes, episodes, label, colour):
        # Plot data

        if episodes:
            add_plot_for_common_rewards(axes, episodes, colour)

        # Format the plot
        axes.set_title("Most Frequent Reward Per Step\n(" + label + " Episodes)")
        axes.set_xlabel("Count")


# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list


def get_plot_data_for_common_rewards(episodes):

    all_step_rewards = []

    for e in episodes:
        for v in e.events:
            all_step_rewards.append(v.reward)

    unique_rewards, unique_counts = np.unique(np.array(all_step_rewards), return_counts=True)

    plot_rewards = []
    plot_counts = []

    for i in range(0, 10):
        index = np.argmax(unique_counts)

        plot_rewards.append(unique_rewards[index])
        plot_counts.append(unique_counts[index])

        unique_counts[index] = 0

    return plot_rewards, plot_counts

def add_plot_for_common_rewards(axes :Axes, episodes, colour):
    (plot_rewards, plot_counts) = get_plot_data_for_common_rewards(episodes)

    y_pos = np.arange(len(plot_counts))

    axes.barh(y_pos, plot_counts, color=colour)
    axes.set_yticks(y_pos)
    axes.set_yticklabels(plot_rewards)
