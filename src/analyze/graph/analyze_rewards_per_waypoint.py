import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer



class AnalyzeRewardsPerWaypoint(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.show_filtered = tk.BooleanVar(value=True)


    def build_control_frame(self, control_frame):
        pass


    def add_plots(self):
        if not self.all_episodes:
            return


        axes :Axes = self.graph_figure.add_subplot()

        self.plot_rewards_per_waypoint(axes)


    def plot_rewards_per_waypoint(self, axes :Axes):
        # Plot data

        num_waypoints = len(self.current_track.track_waypoints)

        add_plot_for_rewards_per_waypoint(axes, "All", self.all_episodes, "C1", num_waypoints)

        if self.filtered_episodes and self.show_filtered.get():
            add_plot_for_rewards_per_waypoint(axes, "Filtered", self.filtered_episodes, "C2", num_waypoints)

        # Format the plot
        axes.set_title("Rewards per Waypoint")
        axes.set_xlabel("Waypoint")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


# Ugly but using * operator gives a list of the same list (by reference) instead of unique lists
def get_list_of_empty_lists(size):
    new_list = []
    for i in range(0, size):
        new_list.append([])
    return new_list


def get_plot_data_for_rewards_per_waypoint(episodes, num_waypoints):

    rewards = get_list_of_empty_lists(num_waypoints)

    for e in episodes:
        for v in e.events:
            rewards[v.closest_waypoint_index].append(v.reward)

    plot_waypoints = np.arange(0, num_waypoints)
    plot_rewards = np.zeros(num_waypoints)

    for i, r in enumerate(rewards):
        if r:
            plot_rewards[i] = np.average(r)
        else:
            plot_rewards[i] = None

    return plot_waypoints, plot_rewards



def add_plot_for_rewards_per_waypoint(axes: Axes, label, episodes, colour, num_waypoints):
    (plot_x, plot_y) = get_plot_data_for_rewards_per_waypoint(episodes, num_waypoints)
    axes.plot(plot_x, plot_y, color=colour, label=label)