import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics


class AnalyzeConvergence(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):
        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self.visitor_map = None
        self.skip_starts = tk.BooleanVar()
        self.granularity = tk.IntVar()
        self.extra_bright = tk.BooleanVar()

    def build_control_frame(self, control_frame):

        tk.Checkbutton(
            control_frame, text="Skip Starts",
            variable=self.skip_starts,
            command=self.checkbutton_press_skip_starts).grid(column=0, row=0, pady=5, padx=5)

        tk.Checkbutton(
            control_frame, text="Extra Bright",
            variable=self.extra_bright,
            command=self.checkbutton_press_extra_bright).grid(column=0, row=1, pady=5, padx=5)

        granularity_group = tk.LabelFrame(control_frame, text="Granularity", padx=5, pady=5)
        granularity_group.grid(column=0, row=2, pady=5, padx=5)

        tk.Radiobutton(granularity_group, text="3 cm", variable=self.granularity, value=3,
                       command=self.chosen_new_granularity).grid(column=0, row=0, pady=5, padx=5)
        tk.Radiobutton(granularity_group, text="5 cm", variable=self.granularity, value=5,
                       command=self.chosen_new_granularity).grid(column=0, row=1, pady=5, padx=5)
        tk.Radiobutton(granularity_group, text="10 cm", variable=self.granularity, value=10,
                       command=self.chosen_new_granularity).grid(column=0, row=2, pady=5, padx=5)
        self.granularity.set(3)


    def redraw(self):
        if self.skip_starts.get():
            skip = 20
        else:
            skip = 0

        if self.filtered_episodes:
            if not self.visitor_map:
                self.visitor_map = self.current_track.get_visitor_map(self.granularity.get()/100)
                for e in self.filtered_episodes:
                    e.apply_to_visitor_map(self.visitor_map, skip, self.action_space_filter)
            self.visitor_map.draw(self.track_graphics, self.extra_bright.get())

    def warning_filtered_episodes_changed(self):
        self.visitor_map = None

    def warning_track_changed(self):
        self.visitor_map = None

    def warning_action_space_filter_changed(self):
        self.visitor_map = None

    def checkbutton_press_skip_starts(self):
        self.visitor_map = None
        self.guru_parent_redraw()

    def checkbutton_press_extra_bright(self):
        self.guru_parent_redraw()

    def chosen_new_granularity(self):
        self.visitor_map = None
        self.guru_parent_redraw()

