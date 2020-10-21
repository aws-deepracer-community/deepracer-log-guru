import tkinter as tk
import numpy as np
import math

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.gridspec import GridSpec
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.analyze.selector.episode_selector import EpisodeSelector
from src.episode.episode import Episode


AXIS_TIME = 1
AXIS_STEP = 2
AXIS_PROGRESS = 3
AXIS_DISTANCE = 4
AXIS_LAP_POSITION = 5

class AnalyzeEpisodeSpeed(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_selector = episode_selector
        self.axis_tk_var = tk.IntVar(value=AXIS_TIME)

    def build_control_frame(self, control_frame):

        axis_group = tk.LabelFrame(control_frame, text="Axis", padx=5, pady=5)
        axis_group.pack()

        tk.Radiobutton(axis_group, text="Time", variable=self.axis_tk_var, value=AXIS_TIME,
                       command=self.guru_parent_redraw).grid(column=0, row=0, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Step", variable=self.axis_tk_var, value=AXIS_STEP,
                       command=self.guru_parent_redraw).grid(column=0, row=1, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Progress", variable=self.axis_tk_var, value=AXIS_PROGRESS,
                       command=self.guru_parent_redraw).grid(column=0, row=2, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Distance", variable=self.axis_tk_var, value=AXIS_DISTANCE,
                       command=self.guru_parent_redraw).grid(column=0, row=3, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Lap Position", variable=self.axis_tk_var, value=AXIS_LAP_POSITION,
                       command=self.guru_parent_redraw).grid(column=0, row=4, pady=2, padx=5)

        ####

        episode_selector_frame = self.episode_selector.get_label_frame(control_frame, self.guru_parent_redraw)
        episode_selector_frame.pack()

    def add_plots(self):
        axes :Axes = self.graph_figure.add_subplot()

        # Plot the data

        episode = self.episode_selector.get_selected_episode()
        if not episode:
            return

        plot_x = []
        general_title = "???"
        axis_label = "???"
        wrap_point = None

        if self.axis_tk_var.get() == AXIS_TIME:
            plot_x = get_plot_data_times(episode)
            general_title = "by Time"
            axis_label = "Time / seconds"
        if self.axis_tk_var.get() == AXIS_STEP:
            plot_x = get_plot_data_steps(episode)
            general_title = "per Step"
            axis_label = "Step"
        if self.axis_tk_var.get() == AXIS_PROGRESS:
            plot_x = get_plot_data_progresses(episode)
            general_title = "by Progress"
            axis_label = "Progress %"
        if self.axis_tk_var.get() == AXIS_DISTANCE:
            plot_x = get_plot_data_distances(episode)
            general_title = "by Distance"
            axis_label = "Distance Travelled / metres"
        if self.axis_tk_var.get() == AXIS_LAP_POSITION:
            plot_x, wrap_point = get_plot_data_lap_positions(episode, self.current_track)
            general_title = "by Lap Position"
            axis_label = "Lap Position / %"
            axes.set_xbound(0, 100)

        plot_y_action_speeds = get_plot_data_action_speeds(episode, wrap_point)
        plot_y_track_speeds = get_plot_data_track_speeds(episode, wrap_point)

        axes.fill_between(plot_x, plot_y_action_speeds, step="post", color="C1", label="Action Speed",)
        axes.plot(plot_x, plot_y_action_speeds, "o", color="black", markersize=3, label="Step")
        axes.plot(plot_x, plot_y_track_speeds, color="C2", label="Track Speed", linewidth=3)

        # Setup formatting
        axes.set_title("Speed " + general_title + " for Episode #" + str(episode.id))
        axes.set_xlabel(axis_label)
        axes.set_ylabel("Speed")

        if self.axis_tk_var.get() == AXIS_LAP_POSITION:
            axes.set_xbound(0, 100)

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)


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

def get_plot_data_action_speeds(episode :Episode, wrap_point):

    speeds = []

    for v in episode.events:
        speeds.append(v.speed)

    if wrap_point:
        speeds = speeds[wrap_point:] + [math.nan] + speeds[:wrap_point]

    return np.array(speeds)

def get_plot_data_track_speeds(episode :Episode, wrap_point):

    speeds = []

    for v in episode.events:
        speeds.append(v.track_speed)

    if wrap_point:
        speeds = speeds[wrap_point:] + [math.nan] + speeds[:wrap_point]

    return np.array(speeds)
