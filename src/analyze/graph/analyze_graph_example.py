import tkinter as tk

from src.analyze.graph.graph_analyzer import GraphAnalyzer

from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

import numpy as np


class AnalyzeGraphExample(GraphAnalyzer):


    def __init__(self, guru_parent_redraw, graph_figure :Figure, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, graph_figure, control_frame)



    def build_control_frame(self, control_frame):

        self.hello_info = tk.Label(control_frame, text="Hello")
        self.hello_info.grid(column=0, row=10, pady=20)


    def add_plots(self):
        gs = GridSpec(1, 2)

        axes_left = self.graph_figure.add_subplot(gs[0, 0])
        axes_right = self.graph_figure.add_subplot(gs[0, 1])

        t = np.arange(0, 10, .01)

        axes_left.plot(t, 2 * np.sin(2 * np.pi * t))
        axes_right.plot(t, 5 * np.sin(5 * np.pi * t))





