#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.episode_selector import EpisodeSelector
from src.episode.episode import Episode


class AnalyzeEpisodeSlide(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_selector = episode_selector

    def build_control_frame(self, control_frame):
        self.episode_selector.add_to_control_frame(control_frame, self.guru_parent_redraw)

    def add_plots(self):
        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

        # Plot the data

        episode = self.episode_selector.get_selected_episode()
        if not episode:
            return

        plot_x = get_plot_data_steps(episode)

        plot_y_slide = get_plot_data_slide(episode)

        plot_y_track_speeds = get_plot_data_track_speeds(episode)

        axes.plot(plot_x, plot_y_slide, color="C2", label="Slide", linewidth=3)

        # Setup formatting
        axes.set_title("Slide for Episode #" + str(episode.id))
        axes.set_xlabel("Step")
        axes.set_ylabel("Slide (degrees)")
        axes.set_ybound(-20, 20)


def get_plot_data_steps(episode :Episode):

    steps = []

    for v in episode.events:
        steps.append(v.step)

    return np.array(steps)

def get_plot_data_track_speeds(episode :Episode):

    speeds = []

    for v in episode.events:
        speeds.append(v.track_speed)

    return np.array(speeds)

def get_plot_data_slide(episode :Episode):

    slide = []

    for v in episode.events:
        slide.append(v.slide)

    return np.array(slide)