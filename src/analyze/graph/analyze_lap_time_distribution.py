#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np
from matplotlib import ticker

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeRadioButtonControl, QuarterlyDistributionControl, \
    ShowMeanOrMedianStatControl, QuartersCheckButtonControl
from src.episode.episodes_plot_data import get_lap_times, get_lap_times_per_quarter


class AnalyzeLapTimeDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame)
        self._distribution_control = QuarterlyDistributionControl(guru_parent_redraw, control_frame)
        self._mean_or_median_control = ShowMeanOrMedianStatControl(guru_parent_redraw, control_frame)
        self._quarters = QuartersCheckButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()
        self._distribution_control.add_to_control_frame()
        self._mean_or_median_control.add_to_control_frame()
        self._quarters.add_to_control_frame()

    def add_plots(self):
        if not self.all_episodes:
            return

        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

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

        plot_data = get_lap_times(episodes)

        all_quarterly_plot_data = get_lap_times_per_quarter(episodes)
        all_q_labels = ["Q1", "Q2", "Q3", "Q4"]
        all_q_colours = ["C3", "C6", "C4", "C5"]   # Better order so early quarters are dimmer than later ones

        quarterly_plot_data = []
        q_labels = []
        q_colours = []

        if self._quarters.show_q1():
            quarterly_plot_data.append(all_quarterly_plot_data[0])
            q_labels.append(all_q_labels[0])
            q_colours.append(all_q_colours[0])
        if self._quarters.show_q2():
            quarterly_plot_data.append(all_quarterly_plot_data[1])
            q_labels.append(all_q_labels[1])
            q_colours.append(all_q_colours[1])
        if self._quarters.show_q3():
            quarterly_plot_data.append(all_quarterly_plot_data[2])
            q_labels.append(all_q_labels[2])
            q_colours.append(all_q_colours[2])
        if self._quarters.show_q4():
            quarterly_plot_data.append(all_quarterly_plot_data[3])
            q_labels.append(all_q_labels[3])
            q_colours.append(all_q_colours[3])

        min_bins = 15

        if self._distribution_control.show_none():
            axes.hist(plot_data, label=label, color=colour, bins=min_bins * 2)
        elif self._distribution_control.show_bars() and q_labels:
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins)
        elif self._distribution_control.show_stacked() and q_labels:
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins * 2, histtype="barstacked")
        elif self._distribution_control.show_lines() and q_labels:
            axes.hist(quarterly_plot_data, label=q_labels, color=q_colours, bins=min_bins, histtype="step", linewidth=3)

        if not self._mean_or_median_control.show_none() and len(plot_data) > 0:
            if self._mean_or_median_control.show_median():
                stat_method = np.median
            else:
                stat_method = np.mean
            _, top_y = axes.get_ybound()

            if self._distribution_control.show_none():
                stat_y = top_y * 0.95
                stat_x = stat_method(plot_data)
                axes.plot(stat_x, stat_y, marker="o", markersize=12, color="Black")
                axes.plot(stat_x, stat_y, marker="o", markersize=10, color=colour)
            else:
                for i, plot_data in enumerate(quarterly_plot_data):
                    if len(plot_data) > 0:
                        stat_y = top_y * (0.75 + (4 - i) * 0.05)
                        stat_x = stat_method(plot_data)
                        axes.plot(stat_x, stat_y, marker="o", markersize=10, color="Black")
                        axes.plot(stat_x, stat_y, marker="o", markersize=8, color=q_colours[i])

        # Format the plot
        axes.set_title("Lap Time Distribution")
        axes.set_xlabel("Lap Time / Seconds")
        axes.set_ylabel("Occurrences")
        axes.get_yaxis().set_major_locator(ticker.MaxNLocator(integer=True))

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


