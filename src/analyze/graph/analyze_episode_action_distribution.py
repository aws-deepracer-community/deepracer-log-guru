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
from matplotlib.ticker import PercentFormatter

from src.action_space.action import Action
from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeCheckButtonControl, MoreFiltersControl, ActionGroupControl
from src.analyze.core.episode_selector import EpisodeSelector
from src.episode.episode import Episode


class AnalyzeEpisodeActionDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, episode_selector: EpisodeSelector):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self._more_filters_control = MoreFiltersControl(guru_parent_redraw, control_frame, True)
        self._group_control = ActionGroupControl(guru_parent_redraw, control_frame)
        self._episode_selector = episode_selector

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()
        self._more_filters_control.add_to_control_frame()
        self._group_control.add_to_control_frame()

        self._episode_selector.add_to_control_frame(control_frame, self.guru_parent_redraw)

    def add_plots(self):
        if not self.all_episodes:
            return

        episode = self._episode_selector.get_selected_episode()
        if not episode:
            return

        action_mapping = self._get_action_mapping()
        action_names = [name for name in action_mapping.keys()]

        this_episode_data = self._map_frequencies(np.array(episode.action_frequency), action_mapping)

        show_filtered = self._episodes_control.show_filtered()
        show_all = self._episodes_control.show_all()

        x_ticks = np.arange(len(action_names))

        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.11, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

        axes.bar(x_ticks, this_episode_data, 0.9, label='This Episode')

        if show_filtered and show_all:
            filtered_episodes_data = self._get_mapped_data_for_episodes(self.filtered_episodes, action_mapping)
            all_episodes_data = self._get_mapped_data_for_episodes(self.all_episodes, action_mapping)
            axes.bar(x_ticks - 0.1, filtered_episodes_data, 0.2, label='Filtered')
            axes.bar(x_ticks + 0.1, all_episodes_data, 0.2, label='All')
        elif show_filtered:
            filtered_episodes_data = self._get_mapped_data_for_episodes(self.filtered_episodes, action_mapping)
            axes.bar(x_ticks - 0, filtered_episodes_data, 0.3, label='Filtered')
        elif show_all:
            all_episodes_data = self._get_mapped_data_for_episodes(self.all_episodes, action_mapping)
            axes.bar(x_ticks - 0, all_episodes_data, 0.3, label='All')

        axes.set_xticks(x_ticks)
        axes.set_xticklabels(action_names)
        axes.yaxis.set_major_formatter(PercentFormatter())
        axes.set_title("Action Distribution for Episode #" + str(episode.id))

        if len(action_names) >= 5:
            axes.set_ybound(0, 50)
        else:
            axes.set_ybound(0, 100)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def _get_mapped_data_for_episodes(self, episodes, action_mapping: dict):
        data = np.array(episodes[0].action_frequency)
        episode: Episode
        for episode in episodes[1:]:
            data = np.add(data, episode.action_frequency)

        return self._map_frequencies(data, action_mapping)

    def _map_frequencies(self, frequencies: np.ndarray, action_mapping: dict):
        mapped_frequencies = []
        for mapping in action_mapping.values():
            freq = 0
            for i in mapping:
                freq += frequencies[i]
            mapped_frequencies.append(freq)
        return self._get_counts_as_percentage(np.array(mapped_frequencies))

    @staticmethod
    def _get_counts_as_percentage(counts: np.ndarray):
        total_count = sum(counts)
        return counts * 100 / total_count

    def _get_action_mapping(self):
        show_all_actions = not self._more_filters_control.filter_actions()
        group_by_steering = self._group_control.group_by_steering()
        group_by_speed = self._group_control.group_by_speed()
        assert not (group_by_steering and group_by_speed)

        mapping = {}
        action: Action
        for action in self.action_space.get_all_actions():
            if show_all_actions or self.action_space_filter.should_show_action(action.get_index()):
                if group_by_speed:
                    action_name = action.get_speed_group_name()
                elif group_by_steering:
                    action_name = action.get_steering_group_name()
                else:
                    action_name = action.get_readable_for_x_axis()
                if action_name in mapping:
                    mapping[action_name].append(action.get_index())
                else:
                    mapping[action_name] = [action.get_index()]

        return mapping

