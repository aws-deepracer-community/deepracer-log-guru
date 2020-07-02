import tkinter as tk

from src.graphics.track_graphics import TrackGraphics

class TrackAnalyzer:

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):
        self.guru_parent_redraw = guru_parent_redraw
        self.track_graphics = track_graphics
        self.control_frame = control_frame

        self.current_track = None
        self.filtered_episodes = None
        self.action_space = None
        self.action_space_filter = None

    def take_control(self):

        for widget in self.control_frame.winfo_children():
            widget.destroy()

        self.build_control_frame(self.control_frame)

        self.control_frame.pack(side=tk.RIGHT)

    def set_track(self, current_track):
        self.current_track = current_track
        self.warning_track_changed()

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
        # You *MUST* override this
        pass

    def build_control_frame(self, control_frame):
        # You *MUST* override this
        pass

    def left_button_pressed(self, track_point):
        # You MIGHT override this
        pass

    def go_backwards(self, track_point):
        # You MIGHT override this
        pass

    def go_forwards(self, track_point):
        # You MIGHT override this
        pass

    def warning_track_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
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

