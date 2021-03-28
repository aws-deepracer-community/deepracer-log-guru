import src.utils.geometry as geometry
from src.analyze.util.heatmap import HeatMap
from src.analyze.util.visitor import VisitorMap
from src.graphics.track_graphics import TrackGraphics
from src.utils.types import Point

DISPLAY_BORDER = 0.3


class Track:
    #
    # PUBLIC interface
    #

    def get_name_on_menu(self):
        return self._ui_name

    def has_world_name(self, world_name: str):
        return world_name == self._world_name

    def get_number_of_waypoints(self):
        return len(self._track_waypoints)

    def get_waypoint(self, waypoint_id: int):
        return self._track_waypoints[waypoint_id]

    def get_previous_different_waypoint(self, waypoint_id: int):
        (avoid_x, avoid_y) = self.get_waypoint(waypoint_id)
        (result_x, result_y) = (avoid_x, avoid_y)
        result_id = waypoint_id

        while avoid_x == result_x and avoid_y == result_y:
            result_id -= 1
            (result_x, result_y) = self.get_waypoint(result_id)

        return result_x, result_y

    def get_next_different_waypoint(self, waypoint_id: int):
        (avoid_x, avoid_y) = self.get_waypoint(waypoint_id)
        (result_x, result_y) = (avoid_x, avoid_y)
        result_id = waypoint_id

        while avoid_x == result_x and avoid_y == result_y:
            if result_id >= len(self._track_waypoints) - 1:
                result_id = 0
            else:
                result_id += 1
            (result_x, result_y) = self.get_waypoint(result_id)

        return result_x, result_y

    def get_waypoint_percent_from_race_start(self, waypoint_id: int):
        return self._percent_from_race_start[waypoint_id]

    def prepare(self, all_tracks: dict):
        self._assert_sensible_info()
        self._make_last_waypoint_complete_loop()
        self._process_raw_waypoints()
        self._calculate_distances()
        self._calculate_range_of_coordinates()

        self._is_ready = True

        all_tracks[self._world_name] = self

    def configure_track_graphics(self, track_graphics: TrackGraphics):
        track_graphics.set_track_area(
            self._min_x - DISPLAY_BORDER, self._min_y - DISPLAY_BORDER,
            self._max_x + DISPLAY_BORDER, self._max_y + DISPLAY_BORDER)

    def draw_track_edges(self, track_graphics: TrackGraphics, colour: str):
        previous_left = self._drawing_points[-1].left
        previous_right = self._drawing_points[-1].right

        for p in self._drawing_points:
            track_graphics.plot_line(previous_left, p.left, 3, colour)
            previous_left = p.left
            track_graphics.plot_line(previous_right, p.right, 3, colour)
            previous_right = p.right

    def draw_section_highlight(self, track_graphics: TrackGraphics, colour: str, start: int, finish: int):
        previous_left = self._drawing_points[start].left_outer
        previous_right = self._drawing_points[start].right_outer

        if finish >= start:
            highlight_points = self._drawing_points[start + 1:finish + 1]
        else:
            highlight_points = self._drawing_points[start:] + self._drawing_points[:finish + 1]

        for p in highlight_points:
            track_graphics.plot_line(previous_left, p.left_outer, 5, colour)
            previous_left = p.left_outer
            track_graphics.plot_line(previous_right, p.right_outer, 5, colour)
            previous_right = p.right_outer

    def draw_starting_line(self, track_graphics: TrackGraphics, colour: str):
        track_graphics.plot_line(self._drawing_points[0].left, self._drawing_points[0].right, 3, colour)

    def draw_sector_dividers(self, track_graphics: TrackGraphics, colour: str):
        for p in self._drawing_points:
            if p.is_divider:
                track_graphics.plot_line(p.left, p.right, 3, colour, (4, 2))

    def draw_waypoints(self, track_graphics: TrackGraphics, colour: str, minor_size: int, major_size: int):
        assert major_size >= minor_size
        for (i, p) in enumerate(self._drawing_points):
            if i % 10 == 0:
                track_graphics.plot_dot(p.middle, major_size, colour)
            else:
                track_graphics.plot_dot(p.middle, minor_size, colour)

    def draw_annotations(self, track_graphics: TrackGraphics):
        for a in self._annotations:
            a.draw(track_graphics, self._drawing_points, self._track_width)

    def draw_grid(self, track_graphics: TrackGraphics, colour: str):
        x = self._min_x
        while x < self._max_x:
            track_graphics.plot_line(
                (x, self._min_y),
                (x, self._max_y),
                1,
                colour)
            x += 1

        y = self._min_y
        while y < self._max_y:
            track_graphics.plot_line(
                (self._min_x, y),
                (self._max_x, y),
                1,
                colour)
            y += 1

    def draw_sector_labels(self, track_graphics: TrackGraphics, colour: str):
        for name in self.get_all_sector_names():
            (start, finish) = self.get_sector_start_and_finish(name)
            label_waypoint = int((start + finish) / 2)
            point = self._drawing_points[label_waypoint].middle

            track_graphics.plot_text(point, name, 14, colour)

    def get_bearing_and_distance_to_next_waypoint(self, waypoint_id: int):
        this_point = self._drawing_points[waypoint_id].middle

        if waypoint_id >= len(self._drawing_points) - 1:
            next_point = self._drawing_points[0].middle
        else:
            next_point = self._drawing_points[waypoint_id + 1].middle

        distance = geometry.get_distance_between_points(this_point, next_point)
        bearing = geometry.get_bearing_between_points(this_point, next_point)

        return bearing, distance

    def get_bearing_and_distance_from_previous_waypoint(self, waypoint_id: int):
        previous_id = waypoint_id - 1
        if previous_id < 0:
            previous_id = len(self._drawing_points) - 1

        return self.get_bearing_and_distance_to_next_waypoint(previous_id)

    def get_new_visitor_map(self, granularity: float):
        return VisitorMap(
            self._min_x - DISPLAY_BORDER, self._min_y - DISPLAY_BORDER,
            self._max_x + DISPLAY_BORDER, self._max_y + DISPLAY_BORDER,
            granularity)

    def get_new_heat_map(self, granularity: float, allow_repeats: bool):
        return HeatMap(
            self._min_x - DISPLAY_BORDER, self._min_y - DISPLAY_BORDER,
            self._max_x + DISPLAY_BORDER, self._max_y + DISPLAY_BORDER,
            granularity, allow_repeats)

    def get_all_sector_names(self):
        return [self._get_sector_name(x) for x in range(len(self._track_sector_dividers) + 1)]

    def get_sector_start_and_finish(self, sector_name: str):
        assert len(sector_name) == 1
        sector_id = ord(sector_name) - ord("A")
        assert 0 <= sector_id <= len(self._track_sector_dividers)

        if sector_id == 0:
            start = 0
        else:
            start = self._track_sector_dividers[sector_id - 1]

        if sector_id == len(self._track_sector_dividers):
            finish = len(self._track_waypoints) - 1
        else:
            finish = self._track_sector_dividers[sector_id]

        return start, finish




    #
    # PRIVATE implementation
    #

    def __init__(self):
        # Fields that the subclass needs to provide to define the track
        self._ui_name = ""
        self._ui_description = ""
        self._ui_length_in_m = 0
        self._ui_width_in_cm = 0
        self._world_name = ""
        self._track_sector_dividers = []
        self._track_width = 0
        self._track_waypoints = []
        self._annotations = []

        # Fields that we will populate automatically
        self._drawing_points = []
        self._percent_from_race_start = []
        self._measured_left_distance = 0.0
        self._measured_middle_distance = 0.0
        self._measured_right_distance = 0.0
        self._min_x = 0.0
        self._max_x = 0.0
        self._min_y = 0.0
        self._max_y = 0.0
        self._mid_x = 0.0
        self._mid_y = 0.0

        self._is_ready = False

    def _assert_sensible_info(self):
        assert len(self._ui_name) > 5
        assert len(self._ui_description) > 10
        assert 10 < self._ui_length_in_m < 70
        assert 70 < self._ui_width_in_cm < 140
        assert len(self._world_name) > 5
        assert len(self._track_waypoints) > 20
        assert len(self._track_sector_dividers) > 0

        prev = self._track_sector_dividers[0] - 1
        for d in self._track_sector_dividers:
            assert 0 < d < len(self._track_waypoints) - 1
            assert d > prev
            assert d == round(d)
            prev = d

    def _process_raw_waypoints(self):
        previous = self._track_waypoints[-2]   # Must be penultimate since last one is same as first one

        (self._min_x, self._min_y) = previous
        (self._max_x, self._max_y) = previous

        left = previous
        right = previous
        left_outer = previous
        right_outer = previous

        edge_error_tolerance = 0.01
        for i, w in enumerate(self._track_waypoints):
            # Tracks often contain a repeated waypoint, suspect this is deliberate to mess up waypoint algorithms!
            if previous != w:
                if i < len(self._track_waypoints)-1:
                    future = self._track_waypoints[i + 1]
                else:
                    future = self._track_waypoints[0]

                previous_left = left
                previous_right = right
                left = geometry.get_edge_point(previous, w, future, 90, self._track_width / 2)
                if geometry.get_distance_between_points(previous_left, left) < edge_error_tolerance:
                    left = previous_left
                else:
                    left_outer = geometry.get_edge_point(previous, w, future, 90, self._track_width / 2 + 0.08)
                right = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2)
                if geometry.get_distance_between_points(previous_right, right) < edge_error_tolerance:
                    right = previous_right
                else:
                    right_outer = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2 + 0.08)
                self._consider_new_point_in_area(left_outer)
                self._consider_new_point_in_area(w)
                self._consider_new_point_in_area(right_outer)
                previous = w

            is_divider = (i in self._track_sector_dividers)
            self._drawing_points.append(Track.DrawingPoint(left, w, right, left_outer, right_outer, is_divider))

        self._mid_x = (self._min_x + self._max_x) / 2
        self._mid_y = (self._min_y + self._max_y) / 2

    def _consider_new_point_in_area(self, point: Point):
        (x, y) = point
        self._min_x = min(self._min_x, x)
        self._min_y = min(self._min_y, y)

        self._max_x = max(self._max_x, x)
        self._max_y = max(self._max_y, y)

    def _calculate_distances(self):
        previous = self._drawing_points[-1]
        for p in self._drawing_points:
            self._measured_left_distance += geometry.get_distance_between_points(previous.left, p.left)
            self._measured_middle_distance += geometry.get_distance_between_points(previous.middle, p.middle)
            self._measured_right_distance += geometry.get_distance_between_points(previous.right, p.right)
            previous = p

        previous = self._drawing_points[0]
        progress_distance = 0.0
        for p in self._drawing_points:
            progress_distance += geometry.get_distance_between_points(previous.middle, p.middle)
            self._percent_from_race_start.append(round(progress_distance / self._measured_middle_distance * 100, 2))
            previous = p

    def _calculate_range_of_coordinates(self):
        (self._min_x, self._min_y) = self._drawing_points[0].middle
        self._max_x = self._min_x
        self._max_y = self._min_y

        for p in self._drawing_points:
            (x1, y1) = p.left
            (x2, y2) = p.middle
            (x3, y3) = p.right

            self._min_x = min(self._min_x, x1, x2, x3)
            self._max_x = max(self._max_x, x1, x2, x3)

            self._min_y = min(self._min_y, y1, y2, y3)
            self._max_y = max(self._max_y, y1, y2, y3)

    def _make_last_waypoint_complete_loop(self):
        last_point = self._track_waypoints[-1]
        first_point = self._track_waypoints[0]

        (last_x, last_y) = last_point
        (first_x, first_y) = first_point

        if abs(last_x - first_x) > 0.0001 or abs(last_y - first_y) > 0.0001:
            self._track_waypoints.append(first_point)

    def _get_position_of_point_relative_to_waypoint(self, point: Point, waypoint_id: int):
        dp = self._drawing_points[waypoint_id]

        left_distance = geometry.get_distance_between_points(point, dp.left)
        right_distance = geometry.get_distance_between_points(point, dp.right)

        if abs(left_distance - right_distance) < 0.001:
            return "C"
        elif left_distance < right_distance:
            return "L"
        else:
            return "R"

    @staticmethod
    def _get_sector_name(sector_id: int):
        return chr(ord("A") + sector_id)

    class DrawingPoint:
        def __init__(self, left: Point, middle: Point, right: Point,
                     left_outer: Point, right_outer: Point,
                     is_divider: bool):
            self.left = left
            self.middle = middle
            self.right = right
            self.left_outer = left_outer
            self.right_outer = right_outer
            self.is_divider = is_divider
