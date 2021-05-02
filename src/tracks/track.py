#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import src.utils.geometry as geometry
from src.analyze.util.heatmap import HeatMap
from src.analyze.util.visitor import VisitorMap
from src.configuration.real_world import VEHICLE_LENGTH, VEHICLE_WIDTH
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

    def get_world_name(self):
        return self._world_name

    def get_number_of_waypoints(self):
        return len(self._track_waypoints)

    def get_waypoint(self, waypoint_id: int):
        return self._track_waypoints[waypoint_id]

    def get_width(self):
        return self._track_width

    def get_all_waypoints(self):
        return self._track_waypoints

    def get_track_bearing_at_point(self, point):
        closest_waypoint = self._get_closest_waypoint_id(point)
        (before_waypoint, after_waypoint) = self.get_waypoint_ids_before_and_after(point, closest_waypoint)
        return geometry.get_bearing_between_points(self._track_waypoints[before_waypoint],
                                                   self._track_waypoints[after_waypoint])

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

            track_graphics.plot_text(point, name, 18, colour)

    def get_bearing_and_distance_to_next_waypoint(self, waypoint_id: int):
        this_point = self._drawing_points[waypoint_id].middle
        next_point = self._drawing_points[self._get_next_waypoint_id(waypoint_id)].middle

        distance = geometry.get_distance_between_points(this_point, next_point)
        bearing = geometry.get_bearing_between_points(this_point, next_point)

        return bearing, distance

    def get_bearing_and_distance_from_previous_waypoint(self, waypoint_id: int):
        return self.get_bearing_and_distance_to_next_waypoint(self._get_previous_waypoint_id(waypoint_id))

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

    def get_position_of_point_relative_to_waypoint(self, point: Point, waypoint_id: int):
        dp = self._drawing_points[waypoint_id]

        left_distance = geometry.get_distance_between_points(point, dp.left)
        right_distance = geometry.get_distance_between_points(point, dp.right)

        if abs(left_distance - right_distance) < 0.001:
            return "C"
        elif left_distance < right_distance:
            return "L"
        else:
            return "R"

    def get_waypoint_ids_before_and_after(self, point: Point, closest_waypoint_id: int):
        assert 0 <= closest_waypoint_id < len(self._track_waypoints)

        previous_id = self._get_previous_waypoint_id(closest_waypoint_id)
        next_id = self._get_next_waypoint_id(closest_waypoint_id)

        previous_waypoint = self._drawing_points[previous_id].middle
        next_waypoint = self._drawing_points[next_id].middle
        closest_waypoint = self._drawing_points[closest_waypoint_id].middle

        target_dist = geometry.get_distance_between_points(closest_waypoint, previous_waypoint)
        if target_dist == 0.0:
            previous_ratio = 99999.0
        else:
            previous_ratio = geometry.get_distance_between_points(point, previous_waypoint) / target_dist

        target_dist = geometry.get_distance_between_points(closest_waypoint, next_waypoint)
        if target_dist == 0.0:
            next_ratio = 99999.0
        else:
            next_ratio = geometry.get_distance_between_points(point, next_waypoint) / target_dist

        if previous_ratio > next_ratio:
            return closest_waypoint_id, next_id
        else:
            return previous_id, closest_waypoint_id

    def get_projected_distance_on_track(self, point: Point, heading: float, closest_waypoint_id: int):

        travel_distance = 0

        for w in self._drawing_points[closest_waypoint_id:] + self._drawing_points[:closest_waypoint_id]:
            direction_to_left_target = geometry.get_bearing_between_points(point, w.left_safe)
            direction_to_right_target = geometry.get_bearing_between_points(point, w.right_safe)

            relative_direction_to_left_target = geometry.get_turn_between_directions(heading, direction_to_left_target)
            relative_direction_to_right_target = geometry.get_turn_between_directions(heading, direction_to_right_target)

            if relative_direction_to_left_target >= 0 and relative_direction_to_right_target <= 0:
                if abs(relative_direction_to_left_target) < abs(relative_direction_to_right_target):
                    travel_distance = geometry.get_distance_between_points(point, w.left_safe)
                else:
                    travel_distance = geometry.get_distance_between_points(point, w.right_safe)
            else:
                return travel_distance

    def get_sector_coordinates(self, sector: str):
        start, finish = self.get_sector_start_and_finish(sector)
        (x1, y1) = self._drawing_points[start].middle
        (x2, y2) = self._drawing_points[start].middle
        p: Track.DrawingPoint
        for p in self._drawing_points[start:finish+1]:
            (x, y) = p.left_outer
            x1 = min(x1, x)
            x2 = max(x2, x)
            y1 = min(y1, y)
            y2 = max(y2, y)
            (x, y) = p.right_outer
            x1 = min(x1, x)
            x2 = max(x2, x)
            y1 = min(y1, y)
            y2 = max(y2, y)
        return x1, y1, x2, y2

    def get_closest_waypoint_id(self, point: Point):
        best_distance = geometry.get_distance_between_points(point, self._drawing_points[0].middle)
        best_waypoint = 0

        for i, p in enumerate(self._drawing_points):
            distance = min(
                geometry.get_distance_between_points(point, p.left),
                geometry.get_distance_between_points(point, p.right),
                geometry.get_distance_between_points(point, p.middle))
            if distance < best_distance:
                best_distance = distance
                best_waypoint = i

        return best_waypoint

    def get_bearing_at_waypoint(self, waypoint_id):
        previous_point = self._track_waypoints[self._get_previous_waypoint_id(waypoint_id)]
        next_point = self._track_waypoints[self._get_next_waypoint_id(waypoint_id)]
        mid_point = self._track_waypoints[waypoint_id]

        before_bearing = geometry.get_bearing_between_points(previous_point, mid_point)
        after_bearing = geometry.get_bearing_between_points(mid_point, next_point)
        change_in_bearing = after_bearing - before_bearing

        return geometry.get_angle_in_proper_range(before_bearing + change_in_bearing / 2)



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
        assert 10 < self._ui_length_in_m < 100
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
        previous = self._track_waypoints[-2]  # Must be penultimate since last one is same as first one

        (self._min_x, self._min_y) = previous
        (self._max_x, self._max_y) = previous

        left = previous
        right = previous
        left_outer = previous
        right_outer = previous
        left_safe = previous
        right_safe = previous

        edge_error_tolerance = 0.01
        safe_car_overhang = min(VEHICLE_LENGTH, VEHICLE_WIDTH) / 2
        outer_distance = 0.08

        for i, w in enumerate(self._track_waypoints + [self._track_waypoints[0]]):
            # Tracks often contain a repeated waypoint, suspect this is deliberate to mess up waypoint algorithms!
            if previous != w:
                if i < len(self._track_waypoints) - 1:
                    future = self._track_waypoints[i + 1]
                else:
                    future = self._track_waypoints[0]

                previous_left = left
                previous_right = right
                left = geometry.get_edge_point(previous, w, future, 90, self._track_width / 2)
                if geometry.get_distance_between_points(previous_left, left) < edge_error_tolerance:
                    left = previous_left
                else:
                    left_outer = geometry.get_edge_point(previous, w, future, 90, self._track_width / 2 + outer_distance)
                    left_safe = geometry.get_edge_point(previous, w, future, 90, self._track_width / 2 + safe_car_overhang)
                right = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2)
                if geometry.get_distance_between_points(previous_right, right) < edge_error_tolerance:
                    right = previous_right
                else:
                    right_outer = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2 + outer_distance)
                    right_safe = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2 + safe_car_overhang)
                self._consider_new_point_in_area(left_outer)
                self._consider_new_point_in_area(w)
                self._consider_new_point_in_area(right_outer)
                previous = w

            is_divider = (i in self._track_sector_dividers)
            self._drawing_points.append(Track.DrawingPoint(left, w, right, left_outer, right_outer,
                                                           left_safe, right_safe, is_divider))

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

    def _get_next_waypoint_id(self, waypoint_id):
        if waypoint_id >= len(self._track_waypoints) - 1:
            return 0
        else:
            return waypoint_id + 1

    def _get_previous_waypoint_id(self, waypoint_id):
        if waypoint_id < 1:
            return len(self._track_waypoints) - 1
        else:
            return waypoint_id - 1

    def _get_closest_waypoint_id(self, point):
        distance = geometry.get_distance_between_points(self._track_waypoints[0], point)
        closest_id = 0
        for i, w in enumerate(self._track_waypoints[1:]):
            new_distance = geometry.get_distance_between_points(w, point)
            if new_distance < distance:
                distance = new_distance
                closest_id = i + 1
        return closest_id

    @staticmethod
    def _get_sector_name(sector_id: int):
        return chr(ord("A") + sector_id)

    class DrawingPoint:
        def __init__(self, left: Point, middle: Point, right: Point,
                     left_outer: Point, right_outer: Point,
                     left_safe: Point, right_safe: Point,
                     is_divider: bool):
            self.left = left
            self.middle = middle
            self.right = right
            self.left_outer = left_outer
            self.right_outer = right_outer
            self.left_safe = left_safe
            self.right_safe = right_safe
            self.is_divider = is_divider
