from src.graphics.track_graphics import TrackGraphics

class Annotation:
    def __init__(self, waypoint_id: int, side, distance_from_centre, colour):
        assert side == "L" or side == "R"
        assert waypoint_id >= 0
        assert distance_from_centre >= 0

        self.waypoint_id = waypoint_id
        self.side = side
        self.distance_from_centre = distance_from_centre
        self.colour = colour

    def draw_from_point(self, point, track_graphics: TrackGraphics):
        pass

class Dot(Annotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour):
        Annotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

    def draw_from_point(self, point, track_graphics: TrackGraphics):
        track_graphics.plot_dot(point, 4, self.colour)



class Line(Annotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour, bearing, length ):
        Annotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

        assert -180 <= bearing <= 180
        assert length > 0

        self.bearing = bearing
        self.length = length

    def draw_from_point(self, point, track_graphics: TrackGraphics):
        track_graphics.plot_dot(point, 3, self.colour)
        track_graphics.plot_angle_line(point, self.bearing, self.length, 2, self.colour)

class Cone(Annotation):
    def __init__(self, waypoint_id :int, side, distance_from_centre, colour, bearing, length, angular_width ):
        Annotation.__init__(self, waypoint_id, side, distance_from_centre, colour)

        assert -180 <= bearing <= 180
        assert length > 0
        assert angular_width > 0

        self.bearing = bearing
        self.length = length
        self.angular_width = angular_width

    def draw_from_point(self, point, track_graphics: TrackGraphics):
        track_graphics.plot_dot(point, 3, self.colour)
        track_graphics.plot_angle_line(point, self.bearing, self.length, 2, self.colour)
        track_graphics.plot_angle_line(point, self.bearing + self.angular_width / 2, self.length, 1, self.colour)
        track_graphics.plot_angle_line(point, self.bearing - self.angular_width / 2, self.length, 1, self.colour)

