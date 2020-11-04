import tkinter as tk

import src.secret_sauce.glue.glue as ss
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.ui.log_event_info_window import LogEventInfoWindow
from src.analyze.selector.episode_selector import EpisodeSelector




class AnalyzeExitPoints(TrackAnalyzer):


    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self.show_episodes = tk.BooleanVar(value=True)
        self.show_evaluations = tk.BooleanVar(value=False)

    def build_control_frame(self, control_frame):

        show_group = tk.LabelFrame(control_frame, text="Show", padx=5, pady=5)
        show_group.pack()

        tk.Checkbutton(
            show_group, text="Episodes",
            variable=self.show_episodes,
            command=self.guru_parent_redraw).pack()

        tk.Checkbutton(
            show_group, text="Evaluations(TBD)",
            variable=self.show_evaluations,
            command=self.guru_parent_redraw).pack()


    def redraw(self):

        if self.show_episodes.get() and self.filtered_episodes:
            for e in self.filtered_episodes:
                if not e.lap_complete:
                    exit_point = (e.events[-1].x, e.events[-1].y)
                    self.track_graphics.plot_dot(exit_point, 2, "orange")

        if self.show_evaluations.get():
            for v in self.evaluation_phases:
                pass # do something




