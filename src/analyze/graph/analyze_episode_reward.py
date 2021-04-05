import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from src.analyze.core.controls import EpisodeRewardTypeControl
from src.analyze.graph.analyze_episode_graph_base import AnalyzeEpisodeStat
from src.analyze.selector.episode_selector import EpisodeSelector

class AnalyzeEpisodeReward(AnalyzeEpisodeStat):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame, episode_selector,
                         "Reward", "Step Reward", "Total Reward", False, True)

        self._rewardTypeControl = EpisodeRewardTypeControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._rewardTypeControl.add_to_control_frame()
        super().build_control_frame(control_frame)

    def get_plot_bar_values_per_step(self, wrap_point):

        rewards = []

        if self._rewardTypeControl.show_reward_plus_total() or self._rewardTypeControl.show_reward_plus_future():
            for v in self.episode.events:
                rewards.append(v.reward)
        elif self._rewardTypeControl.show_new_reward_plus_total() or self._rewardTypeControl.show_new_reward_plus_future():
            for v in self.episode.events:
                rewards.append(v.new_reward)
        if wrap_point:
            rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

        return np.array(rewards)

    def get_plot_line_values_per_step(self, wrap_point):

        rewards = []

        if self._rewardTypeControl.show_reward_plus_total():
            for v in self.episode.events:
                rewards.append(v.reward_total)
        elif self._rewardTypeControl.show_new_reward_plus_total():
            for v in self.episode.events:
                rewards.append(v.new_reward_total)
        elif self._rewardTypeControl.show_reward_plus_future():
            for v in self.episode.events:
                rewards.append(v.discounted_future_rewards[0])
        elif self._rewardTypeControl.show_new_reward_plus_future():
            for v in self.episode.events:
                rewards.append(v.new_discounted_future_reward)

        if wrap_point:
            rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

        return np.array(rewards)

    def additional_preparation_for_plots(self):
        if self._rewardTypeControl.show_reward_plus_total():
            self.reset_labels("Reward and Total Reward", "Reward", "Total Reward", "Total Reward")
        elif self._rewardTypeControl.show_reward_plus_future():
            self.reset_labels("Reward and Future Discounted Reward", "Reward", "Future Reward", "Future Reward")
        elif self._rewardTypeControl.show_new_reward_plus_total():
            self.reset_labels("New Reward and Total New Reward", "New Reward", "Total New Reward", "Total New Reward")
        elif self._rewardTypeControl.show_new_reward_plus_future():
            self.reset_labels("New Reward and Future Discounted New Reward", "New Reward", "Future New Reward", "Future New Reward")
