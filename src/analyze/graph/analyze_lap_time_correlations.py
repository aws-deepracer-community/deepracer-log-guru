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
from src.analyze.core.controls import EpisodeCheckButtonControl, PredictionsControl, \
    GraphFormatControl, CorrelationControl, GraphLineFittingControl
from src.analyze.core.line_fitting import get_linear_regression, get_quadratic_regression, get_cubic_regression
from src.episode.episode import Episode


class AnalyzeLapTimeCorrelations(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, guru_parent_callback_for_episode_choice: callable):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame, guru_parent_callback_for_episode_choice)

        self.episode_control = EpisodeCheckButtonControl(guru_parent_redraw, control_frame)
        self.predictions_control = PredictionsControl(guru_parent_redraw, control_frame)
        self.correlation_control = CorrelationControl(guru_parent_redraw, control_frame, True)
        self.format_control = GraphFormatControl(guru_parent_redraw, control_frame)
        self._line_fitting_control = GraphLineFittingControl(guru_parent_redraw, control_frame)

        self._plotted_episode_ids = dict()

    def build_control_frame(self, control_frame):
        self.episode_control.add_to_control_frame()
        self.predictions_control.add_to_control_frame()
        self.correlation_control.add_to_control_frame()
        self.format_control.add_to_control_frame()
        self._line_fitting_control.add_to_control_frame()

    def add_plots(self):
        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

        self._plotted_episode_ids = dict()

        if self.episode_control.show_all():
            self.plot_episodes(axes, self.all_episodes, False, "C1", "All", "o")
            if self.predictions_control.show_predictions():
                self.plot_episodes(axes, self.all_episodes, True, "C3", "All - Predicted", ".")

        if self.episode_control.show_filtered():
            self.plot_episodes(axes, self.filtered_episodes, False, "C2", "Filtered", "o")
            if self.predictions_control.show_predictions():
                self.plot_episodes(axes, self.filtered_episodes, True, "C4", "Filtered - Predicted", ".")

        self.format_axes(axes)

    def plot_episodes(self, axes: Axes, episodes: list, make_predictions: bool, colour, label, shape):

        if not episodes:
            return

        if make_predictions:
            if self.correlation_control.correlate_total_reward():
                plot_y = get_plot_data_total_rewards_predicted(episodes)
            elif self.correlation_control.correlate_starting_point():
                plot_y = get_plot_data_starting_points_predicted(episodes)
            elif self.correlation_control.correlate_average_reward():
                plot_y = get_plot_data_average_rewards_predicted(episodes)
            elif self.correlation_control.correlate_training_iteration():
                plot_y = get_plot_data_iterations_predicted(episodes)
            else:
                return
        else:
            if self.correlation_control.correlate_total_distance():
                plot_y = get_plot_data_distances(episodes)
            elif self.correlation_control.correlate_peak_track_speed():
                plot_y = get_plot_data_peak_track_speeds(episodes)
            elif self.correlation_control.correlate_peak_progress_speed():
                plot_y = get_plot_data_peak_progress_speeds(episodes)
            elif self.correlation_control.correlate_starting_point():
                plot_y = get_plot_data_starting_points(episodes)
            elif self.correlation_control.correlate_average_reward():
                plot_y = get_plot_data_average_rewards(episodes)
            elif self.correlation_control.correlate_total_reward():
                plot_y = get_plot_data_total_rewards(episodes)
            elif self.correlation_control.correlate_final_reward():
                plot_y = get_plot_data_final_rewards(episodes)
            elif self.correlation_control.correlate_smoothness():
                plot_y = get_plot_data_repeats(episodes)
            elif self.correlation_control.correlate_training_iteration():
                plot_y = get_plot_data_iterations(episodes)
            elif self.correlation_control.correlate_flying_start():
                plot_y = get_plot_data_flying_starts(episodes)
            elif self.correlation_control.correlate_max_slide():
                plot_y = get_plot_data_max_slide(episodes)
            else:
                return

        if make_predictions:
            plot_x, episode_ids = get_plot_data_lap_times_predicted(episodes)
        else:
            plot_x, episode_ids = get_plot_data_lap_times(episodes)

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
                self._plotted_episode_ids[artist] = episode_ids
            if smoothed_y is not None:
                axes.plot(smoothed_y, smoothed_x, color=colour, label=r_label)
        else:
            if self._line_fitting_control.show_scatter():
                artist, = axes.plot(plot_x, plot_y, shape, color=colour, label=label, picker=True)
                self._plotted_episode_ids[artist] = episode_ids
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
        if self.correlation_control.correlate_starting_point():
            general_title = "Starting Point"
            axis_label = "Start Waypoint Id"
        if self.correlation_control.correlate_average_reward():
            general_title = "Average Reward Per Step"
            axis_label = general_title
        if self.correlation_control.correlate_total_reward():
            general_title = "Total Reward"
            axis_label = general_title
        if self.correlation_control.correlate_final_reward():
            general_title = "Final Reward"
            axis_label = general_title
        if self.correlation_control.correlate_smoothness():
            general_title = "Smoothness"
            axis_label = "Repeat Action Percent"
        if self.correlation_control.correlate_training_iteration():
            general_title = "Training Iteration"
            axis_label = general_title
        if self.correlation_control.correlate_flying_start():
            general_title = "Flying Start"
            axis_label = "Track Speed At One Second / metres per second"
        if self.correlation_control.correlate_max_slide():
            general_title = "Maximum Slide"
            axis_label = general_title

        axes.set_title("Lap Time Correlated With " + general_title)

        if self.format_control.swap_axes():
            axes.set_ylabel("Lap Time / Seconds")
            axes.set_xlabel(axis_label)
        else:
            axes.set_xlabel("Lap Time / Seconds")
            axes.set_ylabel(axis_label)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    def handle_chosen_item(self, item_index: int, artist: Artist):
        if artist in self._plotted_episode_ids:
            self._guru_parent_callback_for_episode_choice(self._plotted_episode_ids[artist][item_index])


def get_plot_data_distances(episodes: list):
    distances = []

    for e in episodes:
        if e.lap_complete:
            distances.append(e.distance_travelled)

    return np.array(distances)


def get_plot_data_peak_track_speeds(episodes: list):
    speeds = []

    for e in episodes:
        if e.lap_complete:
            speeds.append(e.peak_track_speed)

    return np.array(speeds)


def get_plot_data_peak_progress_speeds(episodes: list):
    speeds = []

    for e in episodes:
        if e.lap_complete:
            speeds.append(e.peak_progress_speed)

    return np.array(speeds)


def get_plot_data_lap_times(episodes: list):
    lap_times = []
    episode_ids = []

    for e in episodes:
        if e.lap_complete:
            lap_times.append(e.time_taken)
            episode_ids.append(e.id)

    return np.array(lap_times), episode_ids


def get_plot_data_lap_times_predicted(episodes: list):
    lap_times = []
    episode_ids = []

    for e in episodes:
        if is_predicted_episode(e):
            lap_times.append(e.predicted_lap_time)
            episode_ids.append(e.id)

    return np.array(lap_times), episode_ids


def get_plot_data_starting_points(episodes: list):
    starts = []

    for e in episodes:
        if e.lap_complete:
            starts.append(e.events[0].closest_waypoint_index)

    return np.array(starts)


def get_plot_data_starting_points_predicted(episodes: list):
    starts = []

    for e in episodes:
        if is_predicted_episode(e):
            starts.append(e.events[0].closest_waypoint_index)

    return np.array(starts)


def get_plot_data_average_rewards(episodes: list):
    rewards = []

    for e in episodes:
        if e.lap_complete:
            rewards.append(e.average_reward)

    return np.array(rewards)


def get_plot_data_average_rewards_predicted(episodes: list):
    rewards = []

    for e in episodes:
        if is_predicted_episode(e):
            rewards.append(e.average_reward)

    return np.array(rewards)


def get_plot_data_total_rewards(episodes: list):
    rewards = []

    for e in episodes:
        if e.lap_complete:
            rewards.append(e.total_reward)

    return np.array(rewards)


def get_plot_data_final_rewards(episodes: list):
    rewards = []

    e: Episode
    for e in episodes:
        if e.lap_complete:
            rewards.append(e.events[-1].reward)

    return np.array(rewards)


def get_plot_data_total_rewards_predicted(episodes: list):
    rewards = []

    for e in episodes:
        if is_predicted_episode(e):
            rewards.append(e.predicted_lap_reward)

    return np.array(rewards)


def get_plot_data_repeats(episodes: list):
    repeats = []

    for e in episodes:
        if e.lap_complete:
            repeats.append(e.repeated_action_percent)

    return np.array(repeats)


def get_plot_data_iterations(episodes: list):
    iterations = []

    for e in episodes:
        if e.lap_complete:
            iterations.append(e.iteration)

    return np.array(iterations)


def get_plot_data_iterations_predicted(episodes: list):
    iterations = []

    for e in episodes:
        if is_predicted_episode(e):
            iterations.append(e.iteration)

    return np.array(iterations)


def get_plot_data_flying_starts(episodes: list):
    starts = []

    for e in episodes:
        if e.lap_complete:
            starts.append(e.flying_start_speed)

    return np.array(starts)


def get_plot_data_max_slide(episodes: list):
    slides = []

    for e in episodes:
        if e.lap_complete:
            slides.append(e.max_slide)

    return np.array(slides)


def is_predicted_episode(e):
    return not e.lap_complete and e.percent_complete >= 5
