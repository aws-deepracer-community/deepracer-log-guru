#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.graphics.track_graphics import TrackGraphics

class Annotation:
    def draw(self, track_graphics: TrackGraphics, track_drawing_points, track_width):
        pass # Override in child classes

def get_exact_point_(drawing_points, track_width, waypoint_id: int, side, distance_from_centre):
    points = drawing_points[waypoint_id]

    if distance_from_centre == 0:
        return points.middle

    if side == "L":
        (side_x, side_y) = points.left
    else:
        (side_x, side_y) = points.right

    side_fraction = distance_from_centre / track_width * 2
    (start_x, start_y) = points.middle

    x = start_x + (side_x - start_x) * side_fraction
    y = start_y + (side_y - start_y) * side_fraction

    return x, y

class PointAnnotation(Annotation):
    def __init__(self, waypoint_id: int, side, distance_from_centre, colour):
        assert side == "L" or side == "R"
        assert waypoint_id >= 0
        assert distance_from_centre >= 0

        self.waypoint_id = waypoint_id
        self.side = side
        self.distance_from_centre = distance_from_centre
        self.colour = colour

    def draw(self, track_graphics: TrackGraphics, track_drawing_points, track_width):
        exact_point = get_exact_point_(track_drawing_points, track_width, self.waypoint_id, self.side, self.distance_from_centre)
        self.draw_at_point_(track_graphics, exact_point)

    def draw_at_point_(self, track_graphics: TrackGraphics, point):
        pass  # Must override in child classes


class Dot(PointAnnotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour):
        PointAnnotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

    def draw_at_point_(self, track_graphics: TrackGraphics, point):
        track_graphics.plot_dot(point, 4, self.colour)

class Line(PointAnnotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour, bearing, length ):
        PointAnnotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

        assert -180 <= bearing <= 180
        assert length > 0

        self.bearing = bearing
        self.length = length

    def draw_at_point_(self, track_graphics: TrackGraphics, point):
        track_graphics.plot_dot(point, 3, self.colour)
        track_graphics.plot_angle_line(point, self.bearing, self.length, 2, self.colour)

class Cone(PointAnnotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour, bearing, length, angular_width ):
        PointAnnotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

        assert -180 <= bearing <= 180
        assert length > 0
        assert angular_width > 0

        self.bearing = bearing
        self.length = length
        self.angular_width = angular_width

    def draw_at_point_(self, track_graphics: TrackGraphics, point):
        track_graphics.plot_dot(point, 3, self.colour)
        track_graphics.plot_angle_line(point, self.bearing, self.length, 2, self.colour)
        track_graphics.plot_angle_line(point, self.bearing + self.angular_width / 2, self.length, 1, self.colour)
        track_graphics.plot_angle_line(point, self.bearing - self.angular_width / 2, self.length, 1, self.colour)


class Route(Annotation):
    def __init__(self, default_colour, route_points):
        self.route_points = route_points
        self.default_colour = default_colour

        previous = -1
        for p in route_points:
            assert p.waypoint_id > previous
            previous = p.waypoint_id

    def draw(self, track_graphics: TrackGraphics, track_drawing_points, track_width):
        previous_point1 = None
        previous_point2 = None

        for p in self.route_points:
            route_point1 = get_exact_point_(track_drawing_points, track_width, p.waypoint_id, p.side1, p.distance1)
            route_point2 = get_exact_point_(track_drawing_points, track_width, p.waypoint_id, p.side2, p.distance2)

            if previous_point1:
                colour = p.colour
                if not colour:
                    colour = self.default_colour
                track_graphics.plot_polygon([previous_point1, previous_point2, route_point2, route_point1], colour)

            previous_point1 = route_point1
            previous_point2 = route_point2


class RoutePoint:
    def __init__(self, waypoint_id, side1, distance1, side2, distance2, colour=None):
        assert waypoint_id >= 0
        assert side1 == "L" or side1 == "R"
        assert side2 == "L" or side2 == "R"
        assert distance1 >= 0
        assert distance2 >= 0
        assert (side1 != side2) or (distance1 != distance2)

        self.waypoint_id = waypoint_id
        self.side1 = side1
        self.side2 = side2
        self.distance1 = distance1
        self.distance2 = distance2
        self.colour = colour

class WorldDot(Annotation):
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def draw(self, track_graphics: TrackGraphics, track_drawing_points, track_width):
        track_graphics.plot_dot((self.x, self.y), 4, self.colour)




