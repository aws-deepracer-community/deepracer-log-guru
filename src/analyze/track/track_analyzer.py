#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.graphics.track_graphics import TrackGraphics
from src.analyze.core.analyzer import Analyzer


class TrackAnalyzer(Analyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):
        super().__init__(guru_parent_redraw, control_frame)
        self.track_graphics = track_graphics

    def uses_graph_canvas(self):
        return False

    def uses_track_graphics(self):
        return True

    ##########################
    ### ABSTRACT INTERFACE ###
    ##########################

    # These are ADDITIONAL to the interface in Analyzer

    def right_button_pressed(self, track_point):
        # You MIGHT override this
        pass

    def go_backwards(self, track_point):
        # You MIGHT override this
        pass

    def go_forwards(self, track_point):
        # You MIGHT override this
        pass

