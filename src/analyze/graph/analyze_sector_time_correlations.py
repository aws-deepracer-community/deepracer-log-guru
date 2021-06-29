#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import numpy as np
from matplotlib.artist import Artist

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.core.controls import EpisodeCheckButtonControl, GraphFormatControl, CorrelationControl, \
    GraphLineFittingControl
from src.analyze.core.line_fitting import get_linear_regression, get_quadratic_regression, get_cubic_regression
from src.episode.episode import Episode
from src.event.event_meta import Event


class AnalyzeSectorTimeCorrelations(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, guru_parent_callback_for_episode_choice: callable):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame, guru_parent_callback_for_episode_choice)

        self.episode_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self.correlation_control = CorrelationControl(guru_parent_redraw, control_frame, False)
        self.format_control = GraphFormatControl(guru_parent_redraw, control_frame)
        self._line_fitting_control = GraphLineFittingControl(guru_parent_redraw, control_frame)

        self._plotted_episode_info = dict()

    def build_control_frame(self, control_frame):
        self.episode_control.add_to_control_frame()
        self.correlation_control.add_to_control_frame()
        self.format_control.add_to_control_frame()
        self._line_fitting_control.add_to_control_frame()

    def add_plots(self):
        if not self.sector_filter:
            return

        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

        self._plotted_episode_info = dict()

        if self.episode_control.show_all():
            self.plot_episodes(axes, self.all_episodes, "C1", "All", "o")

        if self.episode_control.show_filtered():
            self.plot_episodes(axes, self.filtered_episodes, "C2", "Filtered", "o")

        self.format_axes(axes)

    def plot_episodes(self, axes: Axes, episodes: list, colour, label, shape):

        if not episodes:
            return

        episode_info = self._get_episode_info(episodes)

        plot_x = self._get_plot_data_sector_times(episode_info)

        if self.correlation_control.correlate_complete_lap_time():
            plot_y = self._get_plot_data_lap_times(episode_info)
        elif self.correlation_control.correlate_total_distance():
            plot_y = self._get_plot_data_total_distance(episode_info)
        elif self.correlation_control.correlate_training_iteration():
            plot_y = self._get_plot_data_training_iteration(episode_info)
        elif self.correlation_control.correlate_total_reward():
            plot_y = self._get_plot_data_total_reward(episode_info)
        elif self.correlation_control.correlate_average_reward():
            plot_y = self._get_plot_data_average_reward(episode_info)
        elif self.correlation_control.correlate_peak_track_speed():
            plot_y = self._get_plot_data_peak_track_speed(episode_info)
        elif self.correlation_control.correlate_peak_progress_speed():
            plot_y = self._get_plot_data_peak_progress_speed(episode_info)
        elif self.correlation_control.correlate_max_slide():
            plot_y = self._get_plot_data_max_slide(episode_info)
        elif self.correlation_control.correlate_smoothness():
            plot_y = self._get_plot_data_smoothness(episode_info)
        else:
            return

        # Calculate linear regression line through the points, if requested
        (smoothed_x, smoothed_y, r_label) = (None, None, None)
        if self._line_fitting_control.linear_fitting():
            (smoothed_x, smoothed_y, r) = get_linear_regression(plot_x, plot_y)
            r_label = "R = " + str(round(r, 2))
        elif self._line_fitting_control.quadratic_fitting():
            (smoothed_x, smoothed_y) = get_quadratic_regression(plot_x, plot_y)
            r_label = "Quadratic"
        elif self._line_fitting_control.cubic_fitting():
            (smoothed_x, smoothed_y) = get_cubic_regression(plot_x, plot_y)
            r_label = "Cubic"

        # Finally plot the data we have gathered
        if self.format_control.swap_axes():
            if self._line_fitting_control.show_scatter():
                artist, = axes.plot(plot_y, plot_x, shape, color=colour, label=label, picker=True)
                self._plotted_episode_info[artist] = episode_info
            if smoothed_y is not None:
                axes.plot(smoothed_y, smoothed_x, color=colour, label=r_label)
        else:
            if self._line_fitting_control.show_scatter():
                artist, = axes.plot(plot_x, plot_y, shape, color=colour, label=label, picker=True)
                self._plotted_episode_info[artist] = episode_info
            if smoothed_y is not None:
                axes.plot(smoothed_x, smoothed_y, color=colour, label=r_label)

    def format_axes(self, axes: Axes):

        general_title = "???"
        axis_label = "???"

        if self.correlation_control.correlate_total_distance():
            general_title = "Total Distance"
            axis_label = "Distance / metres"
        if self.correlation_control.correlate_peak_track_speed():
            general_title = "Peak Track Speed"
            axis_label = "Peak Speed / metres per second"
        if self.correlation_control.correlate_peak_progress_speed():
            general_title = "Peak Progress Speed"
            axis_label = "Peak Speed / metres per second"
        if self.correlation_control.correlate_average_reward():
            general_title = "Average Reward Per Step"
            axis_label = general_title
        if self.correlation_control.correlate_total_reward():
            general_title = "Total Reward"
            axis_label = general_title
        if self.correlation_control.correlate_smoothness():
            general_title = "Smoothness"
            axis_label = "Repeat Action Percent"
        if self.correlation_control.correlate_training_iteration():
            general_title = "Training Iteration"
            axis_label = general_title
        if self.correlation_control.correlate_max_slide():
            general_title = "Maximum Slide"
            axis_label = general_title
        if self.correlation_control.correlate_complete_lap_time():
            general_title = "Complete Lap Time"
            axis_label = general_title

        axes.set_title("Sector " + self.sector_filter + " Time Correlated With " + general_title)

        if self.format_control.swap_axes():
            axes.set_ylabel("Sector Time / Seconds")
            axes.set_xlabel(axis_label)
        else:
            axes.set_xlabel("Sector Time / Seconds")
            axes.set_ylabel(axis_label)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def _get_episode_info(self, episodes: list):
        info = []

        complete_laps_only = self.correlation_control.correlate_complete_lap_time()
        (start, finish) = self.current_track.get_sector_start_and_finish(self.sector_filter)

        e: Episode
        for e in episodes:
            if e.lap_complete or not complete_laps_only:
                events = e.get_section_start_and_finish_events(start, finish, self.current_track)
                if events:
                    (start_event, finish_event) = events
                    info.append((e, start_event, finish_event))

        return info

    def handle_chosen_item(self, item_index: int, artist: Artist):
        if artist in self._plotted_episode_info:
            episode, _, _ = self._plotted_episode_info[artist][item_index]
            self._guru_parent_callback_for_episode_choice(episode.id)

    @staticmethod
    def _get_plot_data_sector_times(episode_info: list):
        times = []
        for info in episode_info:
            episode: Episode
            (episode, start_event, finish_event) = info
            times.append(finish_event.time - start_event.time)
        return np.array(times)

    @staticmethod
    def _get_plot_data_lap_times(episode_info: list):
        times = []
        for info in episode_info:
            episode: Episode
            (episode, start_event, finish_event) = info
            times.append(episode.time_taken)
        return np.array(times)

    @staticmethod
    def _get_plot_data_training_iteration(episode_info: list):
        iterations = []
        for info in episode_info:
            episode: Episode
            (episode, start_event, finish_event) = info
            iterations.append(episode.iteration)
        return np.array(iterations)

    @staticmethod
    def _get_plot_data_total_distance(episode_info: list):
        distances = []
        for info in episode_info:
            start_event: Event
            finish_event: Event
            (_, start_event, finish_event) = info
            distances.append(finish_event.total_distance_travelled - start_event.total_distance_travelled)
        return np.array(distances)

    @staticmethod
    def _get_plot_data_total_reward(episode_info: list):
        rewards = []
        for info in episode_info:
            start_event: Event
            finish_event: Event
            (_, start_event, finish_event) = info
            rewards.append(finish_event.reward_total - start_event.reward_total)
        return np.array(rewards)

    @staticmethod
    def _get_plot_data_average_reward(episode_info: list):
        distances = []
        for info in episode_info:
            start_event: Event
            finish_event: Event
            (_, start_event, finish_event) = info
            reward_gain = finish_event.reward_total - start_event.reward_total
            steps = finish_event.step - start_event.step
            distances.append(reward_gain / steps)
        return np.array(distances)

    @staticmethod
    def _get_plot_data_peak_track_speed(episode_info: list):
        peak_speeds = []
        for info in episode_info:
            episode: Episode
            start_event: Event
            finish_event: Event
            (episode, start_event, finish_event) = info
            peak = start_event.track_speed
            event: Event
            for event in episode.get_events_in_range(start_event, finish_event):
                peak = max(peak, event.track_speed)
            peak_speeds.append(peak)
        return np.array(peak_speeds)

    @staticmethod
    def _get_plot_data_peak_progress_speed(episode_info: list):
        peak_speeds = []
        for info in episode_info:
            episode: Episode
            start_event: Event
            finish_event: Event
            (episode, start_event, finish_event) = info
            peak = start_event.progress_speed
            event: Event
            for event in episode.get_events_in_range(start_event, finish_event):
                peak = max(peak, event.progress_speed)
            peak_speeds.append(peak)
        return np.array(peak_speeds)

    @staticmethod
    def _get_plot_data_max_slide(episode_info: list):
        max_slides = []
        for info in episode_info:
            episode: Episode
            start_event: Event
            finish_event: Event
            (episode, start_event, finish_event) = info
            peak = abs(start_event.slide)
            event: Event
            for event in episode.get_events_in_range(start_event, finish_event):
                peak = max(peak, abs(event.slide))
            max_slides.append(peak)
        return np.array(max_slides)

    @staticmethod
    def _get_plot_data_smoothness(episode_info: list):
        repeated_percents = []
        for info in episode_info:
            episode: Episode
            start_event: Event
            finish_event: Event
            (episode, start_event, finish_event) = info
            events = episode.get_events_in_range(start_event, finish_event)
            repeated_percents.append(episode.get_repeated_action_percent(events))
        return np.array(repeated_percents)
