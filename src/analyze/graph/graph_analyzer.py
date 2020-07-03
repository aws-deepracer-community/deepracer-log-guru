import tkinter as tk
from matplotlib.figure import Figure

class GraphAnalyzer:

    def __init__(self, guru_parent_redraw, graph_figure :Figure, control_frame :tk.Frame):
        self.guru_parent_redraw = guru_parent_redraw
        self.graph_figure = graph_figure
        self.control_frame = control_frame

        self.filtered_episodes = None
        self.action_space = None
        self.action_space_filter = None

    def uses_graph_canvas(self):
        return True

    def uses_track_graphics(self):
        return False

    def take_control(self):

        for widget in self.control_frame.winfo_children():
            widget.destroy()

        self.build_control_frame(self.control_frame)

        self.control_frame.pack(side=tk.RIGHT)

    def set_track(self, current_track):
        # Change of track is not relevant to graphs, so simply ignore it
        pass

    def set_filtered_episodes(self, filtered_episodes):
        self.filtered_episodes = filtered_episodes
        self.warning_filtered_episodes_changed()

    def set_action_space(self, action_space):
        self.action_space = action_space
        self.warning_action_space_changed()

    def set_action_space_filter(self, action_space_filter):
        self.action_space_filter = action_space_filter
        self.warning_action_space_filter_changed()

    def redraw(self):
        old_axes = self.graph_figure.get_axes()
        for ax in old_axes:
            self.graph_figure.delaxes(ax)

        self.add_plots()

    def add_plots(self):
        # You *MUST* override this
        pass

    def build_control_frame(self, control_frame):
        # You *MUST* override this
        pass

    def warning_filtered_episodes_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_action_space_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_action_space_filter_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass