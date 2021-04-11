import tkinter as tk
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.utils.discount_factors import discount_factors


class AnalyzeDiscountFactors(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

    def build_control_frame(self, control_frame):
        pass   # No controls yet

    def add_plots(self):
        axes: Axes = self.graph_figure.add_subplot()
        
        colours = ["blue", "C1", "C2", "C3", "C4", "C5"]

        for i in range(discount_factors.get_number_of_discount_factors()):
            (plot_x, plot_y) = discount_factors.get_weights_plot_data(i)
            axes.plot(plot_x, plot_y, colours[i], label=str(discount_factors.get_discount_factor(i)))

        # Format the plot
        axes.set_title("Discount Factors - Future Reward Weights")
        axes.set_xlabel("Steps in Future")

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

