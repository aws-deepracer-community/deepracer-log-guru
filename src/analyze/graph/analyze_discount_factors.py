#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.axes import Axes

from src.analyze.core.controls import DiscountFactorAnalysisControl, ZoomInAndOutControl
from src.analyze.graph.graph_analyzer import GraphAnalyzer
from src.utils.discount_factors import discount_factors


class AnalyzeDiscountFactors(GraphAnalyzer):

    def __init__(self, guru_parent_redraw, matplotlib_canvas :FigureCanvasTkAgg, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, matplotlib_canvas, control_frame)

        self._analysis_choice_control = DiscountFactorAnalysisControl(guru_parent_redraw, control_frame)
        self._zoom_control = ZoomInAndOutControl(guru_parent_redraw, control_frame)

    def build_control_frame(self, control_frame):
        self._analysis_choice_control.add_to_control_frame()
        self._zoom_control.add_to_control_frame()

    def add_plots(self):
        grid_spec = self.graph_figure.add_gridspec(1, 1, left=0.08, right=0.98, bottom=0.08, top=0.92)
        axes: Axes = self.graph_figure.add_subplot(grid_spec[0])

        for i in range(discount_factors.get_number_of_discount_factors()):
            zoom_level = self._zoom_control.get_zoom_level()
            if self._analysis_choice_control.show_future_weights():
                (plot_x, plot_y) = discount_factors.get_weights_plot_data(i, zoom_level)
                axes.set_title("Discount Factors - Future Reward Weights")
                axes.set_xlabel("Steps in Future")
                axes.set_ylabel("Relative Weight")
            elif self._analysis_choice_control.show_remaining_steps():
                (plot_x, plot_y) = discount_factors.get_time_until_death_plot_data(i, zoom_level, 1)
                self.set_axes_titles_remaining_steps(axes, 1)
            elif self._analysis_choice_control.show_bonus_10():
                (plot_x, plot_y) = discount_factors.get_time_until_death_plot_data(i, zoom_level, 10)
                self.set_axes_titles_remaining_steps(axes, 10)
            elif self._analysis_choice_control.show_bonus_100():
                (plot_x, plot_y) = discount_factors.get_time_until_death_plot_data(i, zoom_level, 100)
                self.set_axes_titles_remaining_steps(axes, 100)
            elif self._analysis_choice_control.show_bonus_1000():
                (plot_x, plot_y) = discount_factors.get_time_until_death_plot_data(i, zoom_level, 1000)
                self.set_axes_titles_remaining_steps(axes, 1000)
            else:
                return

            label = str(discount_factors.get_discount_factor(i))
            if i == 0:
                label += " (current)"
            axes.plot(plot_x, plot_y, label=label)

        # Format the plot

        if axes.has_data():
            axes.legend(frameon=True, framealpha=0.8, shadow=True)

    @staticmethod
    def set_axes_titles_remaining_steps(axes: Axes, bonus: int):
        if bonus > 1:
            bonus_str = " + Bonus of x" + str(bonus)
        else:
            bonus_str = ""

        axes.set_title("Discount Factors - Steps Until End of Episode" + bonus_str)
        axes.set_xlabel("Remaining Steps")
        axes.set_ylabel("Future Reward")
