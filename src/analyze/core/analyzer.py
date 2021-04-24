#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.log.log_meta import LogMeta


class Analyzer:

    def __init__(self, guru_parent_redraw, control_frame :tk.Frame):
        self.guru_parent_redraw = guru_parent_redraw
        self.control_frame = control_frame

        self.current_track = None
        self.filtered_episodes = None
        self.all_episodes = None
        self.all_episodes_reward_percentiles = None
        self.action_space = None
        self.action_space_filter = None
        self.sector_filter = None
        self.log_meta = None
        self.evaluation_phases = None

    def take_control(self):
        for widget in self.control_frame.winfo_children():
            widget.destroy()

        self.build_control_frame(self.control_frame)

        # Dodgy but sets correct total width for the control section
        tk.Label(self.control_frame, text="                                                          ").pack()

        self.control_frame.pack(side=tk.RIGHT)

    def lost_control(self):
        self.warning_lost_control()

    def set_track(self, current_track):
        self.current_track = current_track
        self.warning_track_changed()

    def set_all_episodes(self, all_episodes, all_episodes_reward_percentiles):
        self.all_episodes = all_episodes
        self.all_episodes_reward_percentiles = all_episodes_reward_percentiles
        self.warning_all_episodes_changed()

    def set_log_meta(self, log_meta :LogMeta):
        self.log_meta = log_meta

    def set_evaluation_phases(self, evaluation_phases):
        self.evaluation_phases = evaluation_phases

    def set_filtered_episodes(self, filtered_episodes):
        self.filtered_episodes = filtered_episodes
        self.warning_filtered_episodes_changed()

    def set_action_space(self, action_space):
        self.action_space = action_space
        self.warning_action_space_changed()

    def set_action_space_filter(self, action_space_filter):
        self.action_space_filter = action_space_filter
        self.warning_action_space_filter_changed()

    def set_sector_filter(self, sector):
        self.sector_filter = sector
        self.warning_sector_filter_changed()

    ##########################
    ### ABSTRACT INTERFACE ###
    ##########################

    def uses_graph_canvas(self):
        # You *MUST* override this
        pass

    def uses_track_graphics(self):
        # You *MUST* override this
        pass

    def redraw(self):
        # You *MUST* override this
        pass

    def build_control_frame(self, control_frame):
        # You *MUST* override this
        pass

    def recalculate(self):
        # You MIGHT override this to perform time-consuming analysis before redrawing
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

    def warning_lost_control(self):
        # You MIGHT override this to stop activities such an animation if another analyser has just been chosen
        pass

    def warning_action_space_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_action_space_filter_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

    def warning_sector_filter_changed(self):
        # You MIGHT override this to manage cached or pre-calculated data structures
        # Do not override to redraw() since Guru already calls redraw() at the right times!
        pass

