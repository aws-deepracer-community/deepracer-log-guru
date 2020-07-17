import math

import src.utils.geometry as geometry

from src.analyze.util.visitor import VisitorMap
from src.graphics.track_graphics import TrackGraphics
from src.graphics.track_annotations import Annotation

DISPLAY_BORDER = 0.3

class Track:
    def __init__(self):

        # Fields that the subclass needs to provide to define the track
        self.ui_name = ""
        self.ui_description = ""
        self.ui_length_in_m = 0
        self.ui_width_in_cm = 0
        self.ui_difficulty = ""
        self.private_description = ""
        self.world_name = ""
        self.track_section_dividers = []
        self.track_width = 0
        self.track_waypoints = []
        self.annotations = []

        # Fields that we will populate automatically
        self.drawing_points = []
        self.measured_left_distance = 0.0
        self.measured_middle_distance = 0.0
        self.measured_right_distance = 0.0
        self.min_x = 0.0
        self.max_x = 0.0
        self.min_y = 0.0
        self.max_y = 0.0
        self.mid_x = 0.0
        self.mid_y = 0.0

        self.is_ready = False

    def prepare(self):
        self.assert_sensible_info()
        self.make_last_waypoint_complete_loop()
        self.process_raw_waypoints()
        self.calculate_distances()
        self.calculate_range_of_coordinates()

        self.is_ready = True

    def assert_sensible_info(self):
        track_width_error_in_cm = abs(self.ui_width_in_cm - 100 * self.track_width)

        assert len(self.ui_name) > 5
        assert len(self.ui_description) > 10
        assert 10 < self.ui_length_in_m < 70
        assert 70 < self.ui_width_in_cm < 110
        assert self.ui_difficulty in ["Easy", "Medium", "Hard", "*NONE*"]
        assert len(self.private_description) > 10
        assert len(self.world_name) > 5
        # assert track_width_error_in_cm < 2
        assert len(self.track_waypoints) > 20

        # Comment this out to avoid chatter in public version
        if track_width_error_in_cm > 0.1:
            #print("WARNING - UI width is wrong by " + str(round(track_width_error_in_cm)) + " cm for track: " + self.ui_name)
            #print(self.ui_width_in_cm, self.track_width)
            pass

    def process_raw_waypoints(self):
        section_centers = self.get_section_centers()

        section = "A"
        previous = self.track_waypoints[-2]   # Must be penultimate since last one is same as first one

        (self.min_x, self.min_y) = previous
        (self.max_x, self.max_y) = previous

        for i, w in enumerate(self.track_waypoints):
            # Tracks often contain a repeated waypoint, suspect this is deliberate to mess up waypoint algorithms!
            if previous != w:

                left = self.get_target_point(previous, w, 90, self.track_width / 2)
                right = self.get_target_point(previous, w, -90, self.track_width / 2)

                is_divider = ( i in self.track_section_dividers)
                is_center = ( i in section_centers )

                if is_divider:
                    section = chr(ord(section) + 1)

                self.drawing_points.append(Track.DrawingPoint(left, w, right, is_divider, is_center, section))
                previous = w

                self.consider_new_point_in_area(left)
                self.consider_new_point_in_area(w)
                self.consider_new_point_in_area(right)

        self.mid_x = (self.min_x + self.max_x) / 2
        self.mid_y = (self.min_y + self.max_y) / 2



    def get_section_centers(self):
        centers = []
        previous = 0
        for d in self.track_section_dividers:
            centers.append(round((d + previous)/2))
            previous = d

        centers.append(round((len(self.track_waypoints) + previous) / 2))

        return centers

    def consider_new_point_in_area(self, point):
        (x, y) = point
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)

        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

    def calculate_distances(self):
        previous = self.drawing_points[-1]
        for p in self.drawing_points:
            self.measured_left_distance += geometry.get_distance_between_points(previous.left, p.left)
            self.measured_middle_distance += geometry.get_distance_between_points(previous.middle, p.middle)
            self.measured_right_distance += geometry.get_distance_between_points(previous.right, p.right)
            previous = p

    def calculate_range_of_coordinates(self):
        (self.min_x, self.min_y) = self.drawing_points[0].middle
        self.max_x = self.min_x
        self.max_y = self.min_y

        for p in self.drawing_points:
            (x1, y1) = p.left
            (x2, y2) = p.middle
            (x3, y3) = p.right

            self.min_x = min(self.min_x, x1, x2, x3)
            self.max_x = max(self.max_x, x1, x2, x3)

            self.min_y = min(self.min_y, y1, y2, y3)
            self.max_y = max(self.max_y, y1, y2, y3)

    def make_last_waypoint_complete_loop(self):
        last_point = self.track_waypoints[-1]
        first_point = self.track_waypoints[0]

        (last_x, last_y) = last_point
        (first_x, first_y) = first_point

        if abs(last_x - first_x) > 0.0001 or abs(last_y - first_y) > 0.0001:
            self.track_waypoints.append(first_point)

    def get_target_point(self, start, finish, direction_offset, distance):

        (start_x, start_y) = start
        (finish_x, finish_y) = finish

        direction_in_radians = math.atan2(finish_y - start_y, finish_x - start_x)

        direction_to_target = math.degrees(direction_in_radians) + direction_offset
        radians_to_target = math.radians(direction_to_target)

        x = finish_x + math.cos(radians_to_target) * distance
        y = finish_y + math.sin(radians_to_target) * distance

        return x, y

    def configure_track_graphics(self, track_graphics :TrackGraphics):
        track_graphics.set_track_area(self.min_x - DISPLAY_BORDER, self.min_y - DISPLAY_BORDER, self.max_x + DISPLAY_BORDER, self.max_y + DISPLAY_BORDER)


    def draw_track_edges(self, track_graphics, colour):

        previous_left = self.drawing_points[-1].left
        previous_right = self.drawing_points[-1].right

        for p in self.drawing_points:
            if geometry.get_distance_between_points(previous_left, p.left) > 0.08:
                track_graphics.plot_line(previous_left, p.left, 3, colour)
                previous_left = p.left
            if geometry.get_distance_between_points(previous_right, p.right) > 0.08:
                track_graphics.plot_line(previous_right, p.right, 3, colour)
                previous_right = p.right

    def draw_starting_line(self, track_graphics, colour):
        track_graphics.plot_line(self.drawing_points[0].left, self.drawing_points[0].right, 3, colour)

    def draw_section_dividers(self, track_graphics, colour):
        for p in self.drawing_points:
            if p.is_divider:
                track_graphics.plot_line(p.left, p.right, 3, colour)

    def draw_waypoints(self, track_graphics, colour, minor_size, major_size):
        for (i, p) in enumerate(self.drawing_points):
            if i % 10 == 0:
                track_graphics.plot_dot(p.middle, major_size, colour)
            else:
                track_graphics.plot_dot(p.middle, minor_size, colour)

    def draw_annotations(self, track_graphics):
        for a in self.annotations:
            p = self.get_annotation_start_point(a)
            a.draw_from_point(p, track_graphics)

    def get_annotation_start_point(self, annotation: Annotation):
        points = self.drawing_points[annotation.waypoint_id]

        if annotation.distance_from_centre == 0:
            return points.middle

        if annotation.side == "L":
            (side_x, side_y) = points.left
        else:
            (side_x, side_y) = points.right

        side_fraction = annotation.distance_from_centre / self.track_width * 2
        ( start_x, start_y ) = points.middle

        x = start_x + (side_x - start_x) * side_fraction
        y = start_y + (side_y - start_y) * side_fraction

        return x, y


    def draw_grid(self, track_graphics, colour):
        x = self.min_x

        while x < self.max_x:
            track_graphics.plot_line(
                (x, self.min_y),
                (x, self.max_y),
                1,
                colour)
            x += 1

        y = self.min_y

        while y < self.max_y:
            track_graphics.plot_line(
                (self.min_x, y),
                (self.max_x, y),
                1,
                colour)
            y += 1



    def get_position_of_point_relative_to_waypoint(self, point, waypoint_id):
        dp = self.drawing_points[waypoint_id]

        left_distance = geometry.get_distance_between_points(point, dp.left)
        right_distance = geometry.get_distance_between_points(point, dp.right)

        if abs(left_distance - right_distance) < 0.001:
            return "C"
        elif left_distance < right_distance:
            return "L"
        else:
            return "R"

    def get_bearing_and_distance_to_next_waypoint(self, waypoint_id):
        this_point = self.drawing_points[waypoint_id].middle

        if waypoint_id >= len(self.drawing_points) - 1:
            next_point = self.drawing_points[0].middle
        else:
            next_point = self.drawing_points[waypoint_id + 1].middle

        distance = geometry.get_distance_between_points(this_point, next_point)
        bearing = geometry.get_bearing_between_points(this_point, next_point)

        return bearing, distance

    def get_bearing_and_distance_from_previous_waypoint(self, waypoint_id):
        previous_id = waypoint_id - 1
        if previous_id < 0:
            previous_id = len(self.drawing_points) - 1

        return self.get_bearing_and_distance_to_next_waypoint(previous_id)


    class DrawingPoint:
        def __init__(self, left, middle, right, is_divider, is_center, section):
            self.left = left
            self.middle = middle
            self.right = right
            self.is_divider = is_divider
            self.is_center = is_center
            self.section = section

    def get_visitor_map(self, granularity):
        return VisitorMap(self.min_x - DISPLAY_BORDER, self.min_y - DISPLAY_BORDER, self.max_x + DISPLAY_BORDER, self.max_y + DISPLAY_BORDER, granularity)


