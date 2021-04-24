#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.analyze.graph.analyze_episode_graph_base import AnalyzeEpisodeStat
from src.analyze.core.episode_selector import EpisodeSelector


class AnalyzeEpisodeSpeed(AnalyzeEpisodeStat):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, episode_selector: EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame, episode_selector,
                         "Speed", "Action Speed", "Track Speed", True, False)


    def get_plot_bar_values_per_step(self, wrap_point):

        speeds = []

        for v in self.episode.events:
            speeds.append(v.speed)

        if wrap_point:
            speeds = speeds[wrap_point:] + [math.nan] + speeds[:wrap_point]

        return np.array(speeds)

    def get_plot_line_values_per_step(self, wrap_point):

        speeds = []

        for v in self.episode.events:
            speeds.append(v.track_speed)

        if wrap_point:
            speeds = speeds[wrap_point:] + [math.nan] + speeds[:wrap_point]

        return np.array(speeds)
