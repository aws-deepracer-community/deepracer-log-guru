from episode.episode_filter import EpisodeFilter
from graphics.track_analysis_canvas import TrackAnalysisCanvas
from tracks.track import Track
from ui.colours import Colours

SECTOR_BORDER = 0.2

class TrackPainter:
    def __init__(self):
        self._track_colour = Colours.TRACK_GREY

        self._waypoint_major_size = 0
        self._waypoint_minor_size = 0

        self._waypoints_on = True
        self._waypoint_labels_on = False
        self._grid_on = False
        self._annotations_on = False
        self._sectors_on = False

        self._drawing_order = ["G", "A", "T", "N"]

        self.set_track_colour_grey()
        self.set_waypoint_sizes_micro()

        # Moves elsewhere
        # self.zoom_x = None
        # self.zoom_y = None
        # self.zoom_x2 = None
        # self.zoom_y2 = None
        #
        # self.zoom_in = False

    def set_track_colour_grey(self):
        self._track_colour = Colours.TRACK_GREY

    def set_track_colour_blue(self):
        self._track_colour = Colours.TRACK_BLUE

    def set_waypoint_sizes_large(self):
        self._waypoint_minor_size = 5
        self._waypoint_major_size = 9
        self._waypoints_on = True

    def set_waypoint_sizes_small(self):
        self._waypoint_minor_size = 3
        self._waypoint_major_size = 5
        self._waypoints_on = True

    def set_waypoint_sizes_micro(self):
        self._waypoint_minor_size = 2
        self._waypoint_major_size = 3
        self._waypoints_on = True

    def set_waypoints_off(self):
        self._waypoints_on = False

    def set_waypoint_labels_on(self):
        self._waypoint_labels_on = True

    def set_waypoint_labels_off(self):
        self._waypoint_labels_on = False

    def set_grid_front(self):
        self._grid_on = True
        self._drawing_order.remove("G")
        self._drawing_order.append("G")

    def set_grid_back(self):
        self._grid_on = True
        self._drawing_order.remove("G")
        self._drawing_order.insert(0, "G")

    def set_grid_off(self):
        self._grid_on = False

    def set_track_front(self):
        self._drawing_order.remove("T")
        self._drawing_order.append("T")

    def set_track_back(self):
        self._drawing_order.remove("T")
        self._drawing_order.insert(0, "T")

    def set_analyze_front(self):
        self._drawing_order.remove("A")
        self._drawing_order.append("A")

    def set_analyze_back(self):
        self._drawing_order.remove("A")
        self._drawing_order.insert(0, "A")

    def set_annotations_front(self):
        self._annotations_on = True
        self._drawing_order.remove("N")
        self._drawing_order.append("N")

    def set_annotations_back(self):
        self._annotations_on = True
        self._drawing_order.remove("N")
        self._drawing_order.insert(0, "N")

    def set_annotations_off(self):
        self._annotations_on = False

    def set_sectors_on(self):
        self._sectors_on = True

    def set_sectors_off(self):
        self._sectors_on = False

    def draw(self, track_canvas: TrackAnalysisCanvas, current_track: Track, episode_filter: EpisodeFilter):
        # analyzer.recalculate()
        # if background_analyser:
        #     background_analyser.recalculate()
        #
        # track_graphics.reset_to_blank()
        #
        # if self.zoom_in and self.zoom_x:
        #     track_graphics.set_track_area(self.zoom_x, self.zoom_y, self.zoom_x2, self.zoom_y2)
        # else:
        #     current_track.configure_track_graphics(track_graphics)

        for do in self._drawing_order:
            if do == "G" and self._grid_on:
                current_track.draw_grid(track_canvas, Colours.GRID_GREY)

            if do == "T":
                current_track.draw_track_edges(track_canvas, self._track_colour)
                if episode_filter.filter_complete_section:
                    (start, finish) = episode_filter.filter_complete_section
                    current_track.draw_section_highlight(track_canvas, self._track_colour, start, finish)

                current_track.draw_starting_line(track_canvas, self._track_colour)
                if self._sectors_on:
                    current_track.draw_sector_dividers(track_canvas, self._track_colour)
                    current_track.draw_sector_labels(track_canvas, self._track_colour)
                if self._waypoints_on:
                    current_track.draw_waypoints(track_canvas, self._track_colour, self._waypoint_minor_size,
                                                 self._waypoint_major_size)
                    if self._waypoint_labels_on:
                        current_track.draw_waypoint_labels(track_canvas, self._track_colour, 9)

            # if do == "A":
            #     if background_analyser:
            #         background_analyser.redraw()
            #     analyzer.redraw()

            if do == "N" and self._annotations_on:
                current_track.draw_annotations(track_canvas)

    # def zoom_set(self, track_graphics, x, y, x2, y2):
    #     real_x, real_y = track_graphics.get_real_point_for_widget_location(x, y)
    #     real_x2, real_y2 = track_graphics.get_real_point_for_widget_location(x2, y2)
    #
    #     self.zoom_x = min(real_x, real_x2)
    #     self.zoom_x2 = max(real_x, real_x2)
    #     self.zoom_y = min(real_y, real_y2)
    #     self.zoom_y2 = max(real_y, real_y2)
    #
    #     self.zoom_in = True
    #
    # def zoom_sector(self, track: Track, sector: str):
    #     (self.zoom_x, self.zoom_y, self.zoom_x2, self.zoom_y2) = track.get_sector_coordinates(sector)
    #     self.zoom_x -= SECTOR_BORDER
    #     self.zoom_y -= SECTOR_BORDER
    #     self.zoom_x2 += SECTOR_BORDER
    #     self.zoom_y2 += SECTOR_BORDER
    #     self.zoom_in = True
    #
    # def zoom_toggle(self):
    #     self.zoom_in = not self.zoom_in
    #
    # def zoom_clear(self):
    #     self.zoom_x = None
    #     self.zoom_y = None
    #     self.zoom_x2 = None
    #     self.zoom_y2 = None
    #
    #     self.zoom_in = False
