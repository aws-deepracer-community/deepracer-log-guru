#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
import math

from matplotlib.artist import Artist
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style as mpl_style
from src.analyze.core.analyzer import Analyzer


class GraphAnalyzer(Analyzer):
    last_drawn_analyzer = None

    def __init__(self, guru_parent_redraw, matplotlib_canvas: FigureCanvasTkAgg,
                 control_frame: tk.Frame, guru_parent_callback_for_episode_choice=None):
        super().__init__(guru_parent_redraw, control_frame)
        self.matplotlib_canvas = matplotlib_canvas
        self.graph_figure: Figure = matplotlib_canvas.figure
        mpl_style.use("seaborn")
        self.graph_figure.patch.set_facecolor('lightgrey')
        self.graph_figure.canvas.mpl_connect('pick_event', self.handle_mouse_picker)
        self._guru_parent_callback_for_episode_choice = guru_parent_callback_for_episode_choice

    def uses_graph_canvas(self):
        return True

    def uses_track_graphics(self):
        return False

    def redraw(self):
        GraphAnalyzer.last_drawn_analyzer = self
        old_axes = self.graph_figure.get_axes()
        for ax in old_axes:
            self.graph_figure.delaxes(ax)

        self.add_plots()

        self.matplotlib_canvas.draw()

    def handle_mouse_picker(self, event):
        mouse_event = event.mouseevent
        if (mouse_event.button == 3) or (mouse_event.button == 1 and mouse_event.dblclick):
            if self == GraphAnalyzer.last_drawn_analyzer:
                if len(event.ind == 1) and event.artist.axes in self.graph_figure.get_axes():
                    self.handle_chosen_item(event.ind[0], event.artist)

    ########################
    #  ABSTRACT INTERFACE  #
    ########################

    # These are ADDITIONAL to the interface in Analyzer

    def add_plots(self):
        # You *MUST* override this
        pass

    def handle_chosen_item(self, item_index: int, artist: Artist):
        # You *MAY* override this
        pass

    @staticmethod
    def _plot_solo_items(axes, x_values, y_values, colour):
        x_solo = []
        y_solo = []

        previous_y = math.nan
        for i, y in enumerate(y_values):
            if math.isnan(previous_y) and not math.isnan(y):
                if i == len(y_values) - 1 or math.isnan(y_values[i + 1]):
                    x_solo.append(x_values[i])
                    y_solo.append(y)
            previous_y = y

        axes.plot(x_solo, y_solo, ".", color=colour)
