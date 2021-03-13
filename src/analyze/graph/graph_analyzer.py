import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style as mpl_style
from src.analyze.core.analyzer import Analyzer


class GraphAnalyzer(Analyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):
        super().__init__(guru_parent_redraw, control_frame)
        self.matplotlib_canvas = matplotlib_canvas
        self.graph_figure :Figure = matplotlib_canvas.figure
        mpl_style.use("seaborn")
        self.graph_figure.patch.set_facecolor('lightgrey')

    def uses_graph_canvas(self):
        return True

    def uses_track_graphics(self):
        return False

    def redraw(self):
        old_axes = self.graph_figure.get_axes()
        for ax in old_axes:
            self.graph_figure.delaxes(ax)

        self.add_plots()

        self.matplotlib_canvas.draw()


    ##########################
    ### ABSTRACT INTERFACE ###
    ##########################

    # These are ADDITIONAL to the interface in Analyzer

    def add_plots(self):
        # You *MUST* override this
        pass
