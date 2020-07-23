from src.tracks.track import Track
from src.graphics.track_graphics import TrackGraphics
from src.episode.episode_filter import EpisodeFilter

COLOUR_GREY = "Grey30"
COLOUR_BLUE = "Blue"

class ViewManager:

    def __init__(self):
        self.track_colour = ""

        self.waypoint_major_size = 0
        self.waypoint_minor_size = 0

        self.waypoints_on = True
        self.grid_on = True
        self.annotations_on = False

        self.drawing_order = [ "G", "A", "T", "N" ]

        self.set_track_colour_blue()
        self.set_waypoint_sizes_micro()

    def set_track_colour_grey(self):
        self.track_colour = COLOUR_GREY

    def set_track_colour_blue(self):
        self.track_colour = COLOUR_BLUE

    def set_waypoint_sizes_large(self):
        self.waypoint_minor_size = 2
        self.waypoint_major_size = 4
        self.waypoints_on = True

    def set_waypoint_sizes_small(self):
        self.waypoint_minor_size = 1
        self.waypoint_major_size = 3
        self.waypoints_on = True

    def set_waypoint_sizes_micro(self):
        self.waypoint_minor_size = 0
        self.waypoint_major_size = 0
        self.waypoints_on = True

    def set_waypoints_off(self):
        self.waypoints_on = False

    def set_grid_front(self):
        self.grid_on = True
        self.drawing_order.remove("G")
        self.drawing_order.append("G")

    def set_grid_back(self):
        self.grid_on = True
        self.drawing_order.remove("G")
        self.drawing_order.insert(0, "G")

    def set_grid_off(self):
        self.grid_on = False

    def set_track_front(self):
        self.drawing_order.remove("T")
        self.drawing_order.append("T")

    def set_track_back(self):
        self.drawing_order.remove("T")
        self.drawing_order.insert(0, "T")

    def set_analyze_front(self):
        self.drawing_order.remove("A")
        self.drawing_order.append("A")

    def set_analyze_back(self):
        self.drawing_order.remove("A")
        self.drawing_order.insert(0, "A")

    def set_annotations_front(self):
        self.annotations_on = True
        self.drawing_order.remove("N")
        self.drawing_order.append("N")

    def set_annotations_back(self):
        self.annotations_on = True
        self.drawing_order.remove("N")
        self.drawing_order.insert(0, "N")

    def set_annotations_off(self):
        self.annotations_on = False

    def redraw(self, current_track :Track, track_graphics, analyzer, episode_filter: EpisodeFilter):
        track_graphics.reset_to_blank()

        current_track.configure_track_graphics(track_graphics)

        for do in self.drawing_order:
            if do == "G" and self.grid_on:
                current_track.draw_grid(track_graphics, COLOUR_GREY)

            if do == "T":
                current_track.draw_track_edges(track_graphics, self.track_colour)
                if episode_filter.filter_complete_section:
                    (start, finish) = episode_filter.filter_complete_section
                    current_track.draw_section_highlight(track_graphics, self.track_colour, start, finish)

                current_track.draw_starting_line(track_graphics, self.track_colour)
                if self.waypoints_on:
                    current_track.draw_waypoints(track_graphics, self.track_colour, self.waypoint_minor_size, self.waypoint_major_size)

            if do == "A":
                analyzer.redraw()

            if do == "N" and self.annotations_on:
                current_track.draw_annotations(track_graphics)

