import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeRadioButtonControl, QuarterlyDistributionControl


class AnalyzeLapTimeDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame)
        self._distribution_control = QuarterlyDistributionControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()
        self._distribution_control.add_to_control_frame()

    def add_plots(self):
        if not self.all_episodes:
            return

        axes: Axes = self.graph_figure.add_subplot()

        show_filtered = self.filtered_episodes and self._episodes_control.show_filtered()
        show_all = self.all_episodes and self._episodes_control.show_all()

        if show_filtered:
            episodes = self.filtered_episodes
            label = "Filtered"
            colour = "C2"
        elif show_all:
            episodes = self.all_episodes
            label = "All"
            colour = "C1"
        else:
            return

        plot_data = get_plot_data_lap_times(episodes)
        quarterly_plot_data = get_plot_data_lap_times_per_quarter(episodes)

        q_labels = ("Q1", "Q2", "Q3", "Q4")
        q_colours = ["C3", "C4", "C5", "C6"]

        min_bins = 15

        if self._distribution_control.show_none():
            axes.hist(plot_data, label=label, color=colour, bins=min_bins * 2)
        elif self._distribution_control.show_bars():
            axes.hist(plot_data, label=label, color=colour, bins=min_bins * 2)
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins)
        elif self._distribution_control.show_stacked():
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins * 2, histtype="barstacked")
        elif self._distribution_control.show_lines():
            axes.hist(plot_data, label=label, color=colour, bins=min_bins * 2, histtype="step", linewidth=3)
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins, histtype="step", linewidth=3)

        # Format the plot
        axes.set_title("Lap Time Distribution")
        axes.set_xlabel("Lap Time / Seconds")
        axes.get_yaxis().set_ticklabels([])

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


def get_plot_data_lap_times(episodes: list):
    lap_times = []

    for e in episodes:
        if e.lap_complete:
            lap_times.append(e.time_taken)

    return np.array(lap_times)


def get_plot_data_lap_times_per_quarter(episodes: list):
    lap_times = [[], [], [], []]

    for e in episodes:
        if e.lap_complete:
            lap_times[e.quarter - 1].append(e.time_taken)

    return [np.array(lap_times[0]), np.array(lap_times[1]), np.array(lap_times[2]), np.array(lap_times[3])]

