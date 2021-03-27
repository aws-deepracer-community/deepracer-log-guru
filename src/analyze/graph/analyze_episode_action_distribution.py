import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeCheckButtonControl, MoreFiltersControl
from src.analyze.selector.episode_selector import EpisodeSelector
from src.episode.episode import Episode


class AnalyzeEpisodeActionDistribution(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, episode_selector: EpisodeSelector):
        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._episodes_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self._more_filters_control = MoreFiltersControl(guru_parent_redraw, control_frame, True)
        self._episode_selector = episode_selector

    def build_control_frame(self, control_frame: tk.Frame):
        self._episodes_control.add_to_control_frame()
        self._more_filters_control.add_to_control_frame()

        episode_selector_frame = self._episode_selector.get_label_frame(control_frame, self.guru_parent_redraw)
        episode_selector_frame.pack()

    def add_plots(self):
        if not self.all_episodes:
            return

        episode = self._episode_selector.get_selected_episode()
        if not episode:
            return

        action_names = self._get_filtered_list(self.action_space.get_all_action_names_for_x_axis())
        this_episode_counts = get_counts_as_percentage(self._get_filtered_list(np.array(episode.action_frequency)))

        show_filtered = self._episodes_control.show_filtered()
        show_all = self._episodes_control.show_all()

        x_ticks = np.arange(len(action_names))

        axes: Axes = self.graph_figure.add_subplot()
        axes.bar(x_ticks, this_episode_counts, 0.9, label='This Episode')

        if show_filtered and show_all:
            filtered_episodes_counts = self._get_data_for_episodes(self.filtered_episodes)
            all_episodes_counts = self._get_data_for_episodes(self.all_episodes)
            axes.bar(x_ticks - 0.1, filtered_episodes_counts, 0.2, label='Filtered')
            axes.bar(x_ticks + 0.1, all_episodes_counts, 0.2, label='All')
        elif show_filtered:
            filtered_episodes_counts = self._get_data_for_episodes(self.filtered_episodes)
            axes.bar(x_ticks - 0, filtered_episodes_counts, 0.3, label='Filtered')
        elif show_all:
            all_episodes_counts = self._get_data_for_episodes(self.all_episodes)
            axes.bar(x_ticks - 0, all_episodes_counts, 0.3, label='All')

        axes.set_xticks(x_ticks)
        axes.set_xticklabels(action_names)

        if len(action_names) >= 5:
            axes.set_ybound(0, 50)
        else:
            axes.set_ybound(0, 100)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def _get_data_for_episodes(self, episodes):
        data = np.array(episodes[0].action_frequency)
        episode: Episode
        for episode in episodes[1:]:
            data = np.add(data, episode.action_frequency)
        return get_counts_as_percentage(self._get_filtered_list(data))

    def _get_filtered_list(self, full_list: np.ndarray):
        assert len(full_list) == self.action_space.get_number_of_actions()

        if self._more_filters_control.filter_actions():
            filtered_list = []
            for i in range(len(full_list)):
                if self.action_space_filter.should_show_action(i):
                    filtered_list.append(full_list[i])
            return np.array(filtered_list)
        else:
            return full_list


def get_counts_as_percentage(counts: np.ndarray):
    total_count = sum(counts)
    return counts * 100 / total_count
