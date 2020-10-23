import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.selector.episode_selector import EpisodeSelector
from src.episode.episode import Episode
from src.analyze.core.controls import EpisodeAxisControl


AXIS_TIME = 1
AXIS_STEP = 2
AXIS_PROGRESS = 3
AXIS_DISTANCE = 4
AXIS_LAP_POSITION = 5

class AnalyzeEpisodeReward(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_selector = episode_selector

        self.axis_control = EpisodeAxisControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):

        self.axis_control.add_to_control_frame()

        ####

        episode_selector_frame = self.episode_selector.get_label_frame(control_frame, self.guru_parent_redraw)
        episode_selector_frame.pack()

    def add_plots(self):
        axes :Axes = self.graph_figure.add_subplot()
        axes2 :Axes = axes.twinx()

        # Plot the data

        episode = self.episode_selector.get_selected_episode()
        if not episode:
            return

        plot_x = []
        general_title = "???"
        axis_label = "???"
        wrap_point = None

        if self.axis_control.show_time():
            plot_x = get_plot_data_times(episode)
            general_title = "by Time"
            axis_label = "Time / seconds"
        if self.axis_control.show_step():
            plot_x = get_plot_data_steps(episode)
            general_title = "per Step"
            axis_label = "Step"
        if self.axis_control.show_progress():
            plot_x = get_plot_data_progresses(episode)
            general_title = "by Progress"
            axis_label = "Progress %"
        if self.axis_control.show_distance():
            plot_x = get_plot_data_distances(episode)
            general_title = "by Distance"
            axis_label = "Distance Travelled / metres"
        if self.axis_control.show_lap_position():
            plot_x, wrap_point = get_plot_data_lap_positions(episode, self.current_track)
            general_title = "by Lap Position"
            axis_label = "Lap Position / %"
            axes.set_xbound(0, 100)

        plot_y_reward_per_step = get_plot_data_reward_per_step(episode, wrap_point)
        plot_y_total_reward = get_plot_data_track_total_reward(episode, wrap_point)

        axes.fill_between(plot_x, plot_y_reward_per_step, step="post", color="C1", label="Step Reward")
        axes2.plot(plot_x, plot_y_total_reward, color="C2", label="Total Reward", linewidth=3)

        # Setup formatting
        axes.set_title("Reward " + general_title + " for Episode #" + str(episode.id))
        axes.set_xlabel(axis_label)
        axes.set_ylabel("Reward Per Step")
        axes2.set_ylabel("Total Reward")
        axes2.grid(False)

        if self.axis_control.show_lap_position():
            axes.set_xbound(0, 100)

        if axes.has_data():
            axes2.legend(frameon=True, framealpha=0.8, shadow=True)


def get_plot_data_steps(episode :Episode):

    steps = []

    for v in episode.events:
        steps.append(v.step)

    return np.array(steps)

def get_plot_data_progresses(episode :Episode):

    progresses = []

    for v in episode.events:
        progresses.append(v.progress)

    return np.array(progresses)

# time_elapsed

def get_plot_data_times(episode :Episode):

    times = []

    for v in episode.events:
        times.append(v.time_elapsed)

    return np.array(times)

def get_plot_data_distances(episode :Episode):

    distances = []

    for v in episode.events:
        distances.append(v.total_distance_travelled)

    return np.array(distances)

def get_plot_data_lap_positions(episode :Episode, track):
    episode_start_position = episode.get_starting_position_as_percent_from_race_start(track)

    positions = []
    wrap_point = None

    for i, v in enumerate(episode.events):
        position = v.progress + episode_start_position
        if position > 100:
            position -= 100
            if not wrap_point:
                wrap_point = i
        positions.append(position)

    if wrap_point:
        positions = positions[wrap_point:] + [math.nan] + positions[:wrap_point]

    return np.array(positions), wrap_point

def get_plot_data_reward_per_step(episode :Episode, wrap_point):

    rewards = []

    for v in episode.events:
        rewards.append(v.reward)

    if wrap_point:
        rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

    return np.array(rewards)

def get_plot_data_track_total_reward(episode :Episode, wrap_point):

    rewards = []

    for v in episode.events:
        rewards.append(v.reward_total)

    if wrap_point:
        rewards = rewards[wrap_point:] + [math.nan] + rewards[:wrap_point]

    return np.array(rewards)
