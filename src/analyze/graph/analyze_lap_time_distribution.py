import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeRadioButtonControl


class AnalyzeLapTimeDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg, control_frame: tk.Frame):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeRadioButtonControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()

    def add_plots(self):
        if not self.all_episodes:
            return

        axes: Axes = self.graph_figure.add_subplot()

        show_filtered = self.filtered_episodes and self._episodes_control.show_filtered()
        show_all = self.all_episodes and self._episodes_control.show_all()

        if show_filtered:
            (plot_data) = get_plot_data_lap_times(self.filtered_episodes)
            label = "Filtered"
            colour = "C2"
        elif show_all:
            (plot_data) = get_plot_data_lap_times(self.all_episodes)
            label = "All"
            colour = "C1"
        else:
            return

        axes.hist(plot_data, label=label, color=colour, bins=30)

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

