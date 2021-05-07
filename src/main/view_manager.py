#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.track import Track
from src.episode.episode_filter import EpisodeFilter

COLOUR_GREY = "Grey30"
COLOUR_BLUE = "Blue"
SECTOR_BORDER = 0.2


class ViewManager:

    def __init__(self):
        self.track_colour = ""

        self.waypoint_major_size = 0
        self.waypoint_minor_size = 0

        self.waypoints_on = True
        self.waypoint_labels_on = False
        self.grid_on = False
        self.annotations_on = False
        self.sectors_on = False

        self.drawing_order = [ "G", "A", "T", "N" ]

        self.set_track_colour_grey()
        self.set_waypoint_sizes_micro()

        self.zoom_x = None
        self.zoom_y = None
        self.zoom_x2 = None
        self.zoom_y2 = None

        self.zoom_in = False

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

    def set_waypoint_labels_on(self):
        self.waypoint_labels_on = True

    def set_waypoint_labels_off(self):
        self.waypoint_labels_on = False

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

    def set_sectors_on(self):
        self.sectors_on = True

    def set_sectors_off(self):
        self.sectors_on = False

    def redraw(self, current_track :Track, track_graphics, analyzer, background_analyser, episode_filter: EpisodeFilter):
        analyzer.recalculate()
        if background_analyser:
            background_analyser.recalculate()

        track_graphics.reset_to_blank()

        if self.zoom_in and self.zoom_x:
            track_graphics.set_track_area(self.zoom_x, self.zoom_y, self.zoom_x2, self.zoom_y2)
        else:
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
                if self.sectors_on:
                    current_track.draw_sector_dividers(track_graphics, self.track_colour)
                    current_track.draw_sector_labels(track_graphics, self.track_colour)
                if self.waypoints_on:
                    current_track.draw_waypoints(track_graphics, self.track_colour, self.waypoint_minor_size, self.waypoint_major_size)
                    if self.waypoint_labels_on:
                        current_track.draw_waypoint_labels(track_graphics, self.track_colour, 10)

            if do == "A":
                if background_analyser:
                    background_analyser.redraw()
                analyzer.redraw()

            if do == "N" and self.annotations_on:
                current_track.draw_annotations(track_graphics)

    def zoom_set(self, track_graphics, x, y, x2, y2):
        real_x, real_y = track_graphics.get_real_point_for_widget_location(x, y)
        real_x2, real_y2 = track_graphics.get_real_point_for_widget_location(x2, y2)

        self.zoom_x = min(real_x, real_x2)
        self.zoom_x2 = max(real_x, real_x2)
        self.zoom_y = min(real_y, real_y2)
        self.zoom_y2 = max(real_y, real_y2)

        self.zoom_in = True

    def zoom_sector(self, track: Track, sector: str):
        (self.zoom_x, self.zoom_y, self.zoom_x2, self.zoom_y2) = track.get_sector_coordinates(sector)
        self.zoom_x -= SECTOR_BORDER
        self.zoom_y -= SECTOR_BORDER
        self.zoom_x2 += SECTOR_BORDER
        self.zoom_y2 += SECTOR_BORDER
        self.zoom_in = True

    def zoom_toggle(self):
        self.zoom_in = not self.zoom_in

    def zoom_clear(self):
        self.zoom_x = None
        self.zoom_y = None
        self.zoom_x2 = None
        self.zoom_y2 = None

        self.zoom_in = False


