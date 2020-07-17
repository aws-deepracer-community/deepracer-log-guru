import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from src.log.log_meta import LogMeta
from matplotlib import style as mpl_style



class GraphAnalyzer:

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):
        self.guru_parent_redraw = guru_parent_redraw
        self.matplotlib_canvas = matplotlib_canvas
        self.graph_figure :Figure = matplotlib_canvas.figure
        self.control_frame = control_frame

        self.current_track = None
        self.filtered_episodes = None
        self.all_episodes = None
        self.action_space = None
        self.action_space_filter = None

        mpl_style.use("seaborn")
        self.graph_figure.patch.set_facecolor('lightgrey')

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
        self.current_track = current_track
        self.warning_track_changed()

    def set_all_episodes(self, all_episodes):
        self.all_episodes = all_episodes
        self.warning_all_episodes_changed()

    def set_log_meta(self, log_meta :LogMeta):
        self.log_meta = log_meta

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

        self.matplotlib_canvas.draw()


    def add_plots(self):
        # You *MUST* override this
        pass

    def build_control_frame(self, control_frame):
        # You *MUST* override this
        pass

    def warning_track_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_filtered_episodes_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_all_episodes_changed(self):
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