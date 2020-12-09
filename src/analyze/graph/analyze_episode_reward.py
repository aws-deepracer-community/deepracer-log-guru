import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.analyze.graph.analyze_episode_graph_base import AnalyzeEpisodeStat
from src.analyze.selector.episode_selector import EpisodeSelector

class AnalyzeEpisodeReward(AnalyzeEpisodeStat):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame, episode_selector,
                         "Reward", "Step Reward", "Total Reward", False, True)


    def get_plot_bar_values_per_step(self, wrap_point):

        rewards = []

        for v in self.episode.events:
            rewards.append(v.reward)

        if wrap_point:
            rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

        return np.array(rewards)

    def get_plot_line_values_per_step(self, wrap_point):

        rewards = []

        for v in self.episode.events:
            rewards.append(v.reward_total)

        if wrap_point:
            rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

        return np.array(rewards)
