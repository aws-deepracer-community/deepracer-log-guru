import tkinter as tk
import numpy as np

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


class AnalyzeEpisodeSpeed(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self.episode_selector = episode_selector
        self.axis_tk_var = tk.IntVar(value=AXIS_TIME)

    def build_control_frame(self, control_frame):

        axis_group = tk.LabelFrame(control_frame, text="Axis", padx=5, pady=5)
        axis_group.grid(column=0, row=0, pady=5, padx=5, sticky=tk.W + tk.E)

        tk.Radiobutton(axis_group, text="Time", variable=self.axis_tk_var, value=AXIS_TIME,
                       command=self.guru_parent_redraw).grid(column=0, row=0, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Step", variable=self.axis_tk_var, value=AXIS_STEP,
                       command=self.guru_parent_redraw).grid(column=0, row=1, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Progress", variable=self.axis_tk_var, value=AXIS_PROGRESS,
                       command=self.guru_parent_redraw).grid(column=0, row=2, pady=2, padx=5)

        tk.Radiobutton(axis_group, text="Distance", variable=self.axis_tk_var, value=AXIS_DISTANCE,
                       command=self.guru_parent_redraw).grid(column=0, row=3, pady=2, padx=5)

        ####

        episode_selector_frame = self.episode_selector.get_label_frame(control_frame, self.guru_parent_redraw)
        episode_selector_frame.grid(column=0, row=1, pady=5, padx=5, sticky=tk.W + tk.E)

    def add_plots(self):
        axes :Axes = self.graph_figure.add_subplot()

        # Plot the data

        episode = self.episode_selector.get_selected_episode()
        if not episode:
            return

        plot_x = []
        general_title = "???"
        axis_label = "???"

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

        plot_y_action_speeds = get_plot_data_action_speeds(episode)
        plot_y_track_speeds = get_plot_data_track_speeds(episode)

        axes.fill_between(plot_x, plot_y_action_speeds, step="post", color="C1", label="Action Speed",)
        axes.plot(plot_x, plot_y_action_speeds, "o", color="black", markersize=3, label="Step")
        axes.plot(plot_x, plot_y_track_speeds, color="C2", label="Track Speed", linewidth=3)

        # Setup formatting
        axes.set_title("Speed " + general_title + " for Episode #" + str(episode.id))
        axes.set_xlabel(axis_label)
        axes.set_ylabel("Speed")

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

def get_plot_data_action_speeds(episode :Episode):

    speeds = []

    for v in episode.events:
        speeds.append(v.speed)

    return np.array(speeds)

def get_plot_data_track_speeds(episode :Episode):

    speeds = []

    for v in episode.events:
        speeds.append(v.track_speed)

    return np.array(speeds)