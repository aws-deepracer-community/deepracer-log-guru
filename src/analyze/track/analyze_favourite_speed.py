import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics

from src.action_space.action_util import *

import src.analyze.util.visitor as v

HIGH_VISITOR_MAP = 0
MEDIUM_VISITOR_MAP = 1
LOW_VISITOR_MAP = 2

class AnalyzeFavouriteSpeed(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self.visitor_maps = None
        self.skip_starts = tk.BooleanVar()
        self.granularity = tk.IntVar()
        self.threshold = tk.IntVar()

    def build_control_frame(self, control_frame):

        tk.Checkbutton(
            control_frame, text="Skip Starts",
            variable=self.skip_starts,
            command=self.checkbutton_press_skip_starts).grid(column=0, row=0, pady=5, padx=5)

        tk.Radiobutton(control_frame, text="3 cm", variable=self.granularity, value=3,
                       command=self.chosen_new_granularity).grid(column=0, row=1, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="5 cm", variable=self.granularity, value=5,
                       command=self.chosen_new_granularity).grid(column=0, row=2, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="10 cm", variable=self.granularity, value=10,
                       command=self.chosen_new_granularity).grid(column=0, row=3, pady=5, padx=5)
        self.granularity.set(5)

        tk.Radiobutton(control_frame, text="5+ visits", variable=self.threshold, value=5,
                       command=self.chosen_new_threshold).grid(column=0, row=4, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="10+ visits", variable=self.threshold, value=10,
                       command=self.chosen_new_threshold).grid(column=0, row=5, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="20+ visits", variable=self.threshold, value=20,
                       command=self.chosen_new_threshold).grid(column=0, row=6, pady=5, padx=5)
        self.threshold.set(10)

    def redraw(self):
        if self.skip_starts.get():
            skip = 20
        else:
            skip = 0

        if self.filtered_episodes:
            if not self.visitor_maps:
                self.visitor_maps = []
                for i in range(0, 3):
                    self.visitor_maps.append(self.current_track.get_visitor_map(self.granularity.get() / 100))
                for e in self.filtered_episodes:
                    e.apply_speed_to_visitor_map(self.visitor_maps[HIGH_VISITOR_MAP], skip, self.action_space_filter, is_high_speed)
                    e.apply_speed_to_visitor_map(self.visitor_maps[MEDIUM_VISITOR_MAP], skip, self.action_space_filter, is_medium_speed)
                    e.apply_speed_to_visitor_map(self.visitor_maps[LOW_VISITOR_MAP], skip, self.action_space_filter, is_low_speed)

            colours = [ "", "", "" ]
            colours[HIGH_VISITOR_MAP] = "green"
            colours[MEDIUM_VISITOR_MAP] = "yellow"
            colours[LOW_VISITOR_MAP] = "red"

            v.multi_draw(self.track_graphics, self.visitor_maps, colours, self.threshold.get())

    def warning_filtered_episodes_changed(self):
        self.visitor_maps = None

    def warning_track_changed(self):
        self.visitor_maps = None

    def warning_action_space_filter_changed(self):
        self.visitor_maps = None

    def checkbutton_press_skip_starts(self):
        self.visitor_maps = None
        self.guru_parent_redraw()

    def chosen_new_granularity(self):
        self.visitor_maps = None
        self.guru_parent_redraw()

    def chosen_new_threshold(self):
        self.guru_parent_redraw()

