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
from src.configuration.real_world import VEHICLE_LENGTH, VEHICLE_WIDTH, BOX_OBSTACLE_WIDTH, BOX_OBSTACLE_LENGTH
from src.graphics.track_graphics import TrackGraphics
from src.utils.types import Point

DISPLAY_BORDER = 0.3

LEFT = "L"
RIGHT = "R"


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

    def get_percent_progress_point_on_centre_line(self, percent: float):
        assert 0 <= percent <= 100

        i = 0
        while self._percent_from_race_start[i] < percent:
            i += 1

        distance_gap = geometry.get_distance_between_points(self._drawing_points[i].middle,
                                                            self._drawing_points[i - 1].middle)
        percent_gap = self._percent_from_race_start[i] - self._percent_from_race_start[i-1]
        bearing = geometry.get_bearing_between_points(self._drawing_points[i].middle,
                                                      self._drawing_points[i - 1].middle)

        ratio = (self._percent_from_race_start[i] - percent) / percent_gap

        return geometry.get_point_at_bearing(self._drawing_points[i].middle, bearing, ratio * distance_gap)

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

    def draw_waypoint_labels(self, track_graphics: TrackGraphics, colour: str, font_size: int):
        last_label_position = None
        for (i, p) in enumerate(self._drawing_points[:-2]):
            if self._is_vertical_at_waypoint(i):
                label = track_graphics.plot_text(p.middle, str(i), font_size, colour, -1.5 * font_size, 0.0)
            else:
                label = track_graphics.plot_text(p.middle, str(i), font_size, colour, 0.0, 1.5 * font_size)

            label_position = track_graphics.get_widget_position(label)
            if last_label_position is None:
                last_label_position = label_position
            elif geometry.get_distance_between_points(last_label_position, label_position) < 2.5 * font_size:
                track_graphics.delete_widget(label)
            else:
                last_label_position = label_position

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

            if self._is_vertical_at_waypoint(label_waypoint):
                track_graphics.plot_text(point, name, 20, colour, 14, 0)
            else:
                track_graphics.plot_text(point, name, 20, colour, 0, -14)

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

    def get_waypoint_ids_before_and_after(self, point: Point, closest_waypoint_id: int, prefer_forwards=False):
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

        if prefer_forwards:   # Make the behind waypoint appear 5% further away
            previous_ratio *= 1.05

        if previous_ratio > next_ratio:
            return closest_waypoint_id, next_id
        else:
            return previous_id, closest_waypoint_id

    def get_projected_distance_on_track(self, point: Point, heading: float, closest_waypoint_id: int,
                                        path_width: float = 0.0,
                                        blocked_left_waypoints=None, blocked_right_waypoints=None,
                                        blocked_left_object_locations=None, blocked_right_object_locations=None):
        if blocked_left_waypoints is None:
            blocked_left_waypoints = []
            blocked_left_object_locations = []
        if blocked_right_waypoints is None:
            blocked_right_waypoints = []
            blocked_right_object_locations = []

        heading = geometry.get_angle_in_proper_range(heading)

        if path_width > 0.0:
            side_point_1 = geometry.get_point_at_bearing(point, heading + 90, path_width / 2)
            side_point_2 = geometry.get_point_at_bearing(point, heading - 90, path_width / 2)

            d1 = self.get_projected_distance_on_track(point, heading, closest_waypoint_id, 0.0,
                                                      blocked_left_waypoints, blocked_right_waypoints,
                                                      blocked_left_object_locations, blocked_right_object_locations)
            d2 = self.get_projected_distance_on_track(side_point_1, heading, closest_waypoint_id, 0.0,
                                                      blocked_left_waypoints, blocked_right_waypoints,
                                                      blocked_left_object_locations, blocked_right_object_locations)
            d3 = self.get_projected_distance_on_track(side_point_2, heading, closest_waypoint_id, 0.0,
                                                      blocked_left_waypoints, blocked_right_waypoints,
                                                      blocked_left_object_locations, blocked_right_object_locations)
            return min(d1, d2, d3)

        before_waypoint_id, after_waypoint_id = self.get_waypoint_ids_before_and_after(point, closest_waypoint_id, True)

        previous_left = self._drawing_points[before_waypoint_id].left_safe
        previous_right = self._drawing_points[before_waypoint_id].right_safe

        for w in self._drawing_points[after_waypoint_id:] + self._drawing_points[:after_waypoint_id]:
            off_track_distance = self._get_off_track_distance(point, heading, previous_left, previous_right, w)
            hit_object_distance = self._get_hit_object_distance(point, heading,
                                                                blocked_left_waypoints, blocked_right_waypoints,
                                                                blocked_left_object_locations,
                                                                blocked_right_object_locations, w)

            if off_track_distance is None and hit_object_distance is None:
                previous_left = w.left_safe
                previous_right = w.right_safe
            elif off_track_distance is None:
                return hit_object_distance
            elif hit_object_distance is None:
                return off_track_distance
            else:
                return min(hit_object_distance, off_track_distance)

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
        previous_point = self._track_waypoints[self._get_previous_different_waypoint_id(waypoint_id)]
        next_point = self._track_waypoints[self._get_next_different_waypoint_id(waypoint_id)]
        mid_point = self._track_waypoints[waypoint_id]

        before_bearing = geometry.get_bearing_between_points(previous_point, mid_point)
        after_bearing = geometry.get_bearing_between_points(mid_point, next_point)
        change_in_bearing = geometry.get_angle_in_proper_range(after_bearing - before_bearing)

        return geometry.get_angle_in_proper_range(before_bearing + change_in_bearing / 2)

    def get_adjusted_point_on_track(self, chosen_point: Point, margin: float = 0.0):
        waypoint_id = self.get_closest_waypoint_id(chosen_point)
        waypoint = self.get_waypoint(waypoint_id)

        distance_from_waypoint = geometry.get_distance_between_points(waypoint, chosen_point)
        max_distance_from_centre = (self.get_width() + VEHICLE_WIDTH) / 2 - margin

        if distance_from_waypoint > max_distance_from_centre:
            bearing_of_point = geometry.get_bearing_between_points(waypoint, chosen_point)
            adjusted_point = geometry.get_point_at_bearing(waypoint, bearing_of_point, max_distance_from_centre)
        else:
            adjusted_point = chosen_point

        return adjusted_point, waypoint_id

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
                    left_outer = geometry.get_edge_point(previous, w, future, 90,
                                                         self._track_width / 2 + outer_distance)
                    left_safe = geometry.get_edge_point(previous, w, future, 90,
                                                        self._track_width / 2 + safe_car_overhang)
                right = geometry.get_edge_point(previous, w, future, -90, self._track_width / 2)
                if geometry.get_distance_between_points(previous_right, right) < edge_error_tolerance:
                    right = previous_right
                else:
                    right_outer = geometry.get_edge_point(previous, w, future, -90,
                                                          self._track_width / 2 + outer_distance)
                    right_safe = geometry.get_edge_point(previous, w, future, -90,
                                                         self._track_width / 2 + safe_car_overhang)
                self._consider_new_point_in_area(left_outer)
                self._consider_new_point_in_area(w)
                self._consider_new_point_in_area(right_outer)
                previous = w

            is_divider = (i in self._track_sector_dividers)
            self._drawing_points.append(Track.DrawingPoint(i, left, w, right, left_outer, right_outer,
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

    def _get_next_different_waypoint_id(self, waypoint_id):
        current_point = self._track_waypoints[waypoint_id]
        next_waypoint_id = self._get_next_waypoint_id(waypoint_id)
        while current_point == self._track_waypoints[next_waypoint_id]:
            next_waypoint_id = self._get_next_waypoint_id(next_waypoint_id)
        return next_waypoint_id

    def _get_previous_different_waypoint_id(self, waypoint_id):
        current_point = self._track_waypoints[waypoint_id]
        previous_waypoint_id = self._get_previous_waypoint_id(waypoint_id)
        while current_point == self._track_waypoints[previous_waypoint_id]:
            previous_waypoint_id = self._get_previous_waypoint_id(previous_waypoint_id)
        return previous_waypoint_id

    def _get_closest_waypoint_id(self, point):
        distance = geometry.get_distance_between_points(self._track_waypoints[0], point)
        closest_id = 0
        for i, w in enumerate(self._track_waypoints[1:]):
            new_distance = geometry.get_distance_between_points(w, point)
            if new_distance < distance:
                distance = new_distance
                closest_id = i + 1
        return closest_id

    def _is_vertical_at_waypoint(self, waypoint_id: int):
        bearing = self.get_bearing_at_waypoint(waypoint_id)
        return -135 < bearing < -45 or 45 < bearing < 135

    @staticmethod
    def _get_sector_name(sector_id: int):
        return chr(ord("A") + sector_id)

    @staticmethod
    def _get_off_track_distance(point: Point, heading: float, previous_left, previous_right, drawing_point):
        left_safe = drawing_point.left_safe
        right_safe = drawing_point.right_safe

        direction_to_left_target = geometry.get_bearing_between_points(point, left_safe)
        direction_to_right_target = geometry.get_bearing_between_points(point, right_safe)

        relative_direction_to_left_target = geometry.get_turn_between_directions(heading, direction_to_left_target)
        relative_direction_to_right_target = geometry.get_turn_between_directions(heading, direction_to_right_target)

        if relative_direction_to_left_target >= 0 and relative_direction_to_right_target <= 0:
            return None
        else:
            point2 = geometry.get_point_at_bearing(point, heading, 1)  # Just some random distance (1m)
            if left_safe == previous_left:
                off_track_left = previous_left
            else:
                off_track_left = geometry.get_intersection_of_two_lines(point, point2, left_safe, previous_left)
            if right_safe == previous_right:
                off_track_right = previous_right
            else:
                off_track_right = geometry.get_intersection_of_two_lines(point, point2, right_safe, previous_right)

            left_bearing = geometry.get_bearing_between_points(point, off_track_left)
            right_bearing = geometry.get_bearing_between_points(point, off_track_right)

            distances = []
            if abs(geometry.get_turn_between_directions(left_bearing, heading)) < 1:
                if geometry.is_point_between(off_track_left, left_safe, previous_left):
                    distances += [geometry.get_distance_between_points(point, off_track_left)]
            if abs(geometry.get_turn_between_directions(right_bearing, heading)) < 1:
                if geometry.is_point_between(off_track_right, right_safe, previous_right):
                    distances += [geometry.get_distance_between_points(point, off_track_right)]

            if len(distances) > 0:
                return max(distances)
            else:
                return 0.0

    @staticmethod
    def _get_object_location_at_waypoint(waypoint_id: int, blocked_left, blocked_right,
                                         blocked_left_object_locations, blocked_right_object_locations):
        if waypoint_id in blocked_left:
            return blocked_left_object_locations[blocked_left.index(waypoint_id)]
        if waypoint_id in blocked_right:
            return blocked_right_object_locations[blocked_right.index(waypoint_id)]
        return None

    def _get_hit_object_distance(self, point: Point, heading: float, blocked_left, blocked_right,
                                 blocked_left_object_locations, blocked_right_object_locations, drawing_point):

        obj_middle = self._get_object_location_at_waypoint(drawing_point.id, blocked_left, blocked_right,
                                                           blocked_left_object_locations,
                                                           blocked_right_object_locations)
        if obj_middle is None:
            wp = self._get_previous_waypoint_id(drawing_point.id)
            obj_middle = self._get_object_location_at_waypoint(wp, blocked_left, blocked_right,
                                                               blocked_left_object_locations,
                                                               blocked_right_object_locations)
        if obj_middle is None:
            wp = self._get_next_waypoint_id(drawing_point.id)
            obj_middle = self._get_object_location_at_waypoint(wp, blocked_left, blocked_right,
                                                               blocked_left_object_locations,
                                                               blocked_right_object_locations)
        if obj_middle is None:
            return None

        point2 = geometry.get_point_at_bearing(point, heading, 1)  # Just some random distance (1m) to define line
        track_bearing = self.get_track_bearing_at_point(obj_middle)
        safe_border = min(VEHICLE_WIDTH, VEHICLE_LENGTH) / 3  # Effectively enlarge the box

        front_middle = geometry.get_point_at_bearing(obj_middle, track_bearing, BOX_OBSTACLE_LENGTH / 2 + safe_border)
        front_left = geometry.get_point_at_bearing(front_middle, track_bearing + 90,
                                                   BOX_OBSTACLE_WIDTH / 2 + safe_border)
        front_right = geometry.get_point_at_bearing(front_middle, track_bearing - 90,
                                                    BOX_OBSTACLE_WIDTH / 2 + safe_border)

        rear_middle = geometry.get_point_at_bearing(obj_middle, track_bearing, -BOX_OBSTACLE_LENGTH / 2 - safe_border)
        rear_left = geometry.get_point_at_bearing(rear_middle, track_bearing + 90, BOX_OBSTACLE_WIDTH / 2 + safe_border)
        rear_right = geometry.get_point_at_bearing(rear_middle, track_bearing - 90,
                                                   BOX_OBSTACLE_WIDTH / 2 + safe_border)

        distances = []
        for box_side in [(front_left, front_right), (rear_left, rear_right),
                         (front_left, rear_left), (front_right, rear_right)]:
            (box_point1, box_point2) = box_side
            hit_point = geometry.get_intersection_of_two_lines(point, point2, box_point1, box_point2)
            if hit_point is not None and geometry.is_point_between(hit_point, box_point1, box_point2):
                # Make sure it's in front of us!
                bearing_to_hit_point = geometry.get_bearing_between_points(point, hit_point)
                if abs(geometry.get_turn_between_directions(bearing_to_hit_point, heading)) < 1:
                    distances.append(geometry.get_distance_between_points(point, hit_point))

        if not distances:
            return None
        else:
            return min(distances)

    class DrawingPoint:
        def __init__(self, waypoint_id: int, left: Point, middle: Point, right: Point,
                     left_outer: Point, right_outer: Point,
                     left_safe: Point, right_safe: Point,
                     is_divider: bool):
            self.id = waypoint_id
            self.left = left
            self.middle = middle
            self.right = right
            self.left_outer = left_outer
            self.right_outer = right_outer
            self.left_safe = left_safe
            self.right_safe = right_safe
            self.is_divider = is_divider
