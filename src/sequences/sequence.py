#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#


from src.event.event_meta import Event
from src.utils.geometry import get_bearing_between_points, get_distance_between_points, get_angle_in_proper_range, get_point_at_bearing

MINIMUM_USEFUL_SEQUENCE_LENGTH = 5


class Sequence:
    def __init__(self, events: list[Event]):
        assert len(events) >= MINIMUM_USEFUL_SEQUENCE_LENGTH >= 2
        first_event = events[0]
        last_event = events[-1]

        self.initial_track_speed = round(first_event.track_speed, 1)
        self.initial_slide = round(first_event.slide)
        self.action_speed = round(first_event.speed, 1)
        self.action_steering_angle = round(first_event.steering_angle)

        self.final_track_speed = round(last_event.track_speed, 1)
        self.final_slide = round(last_event.slide)

        self.steps = []
        self.dodgy_data = first_event.dodgy_data

        previous_location = (first_event.x, first_event.y)
        for e in events[1:]:
            self.dodgy_data = self.dodgy_data or e.dodgy_data
            current_location = (e.x, e.y)
            distance = get_distance_between_points(previous_location, current_location)
            original_bearing = e.true_bearing
            relative_bearing = get_angle_in_proper_range(original_bearing - first_event.true_bearing)
            self.steps.append(Sequence.Step(distance, relative_bearing))
            previous_location = current_location

    def get_plot_points(self, point, initial_heading):
        points = [point]
        for s in self.steps:
            point = get_point_at_bearing(point, s.bearing + initial_heading, s.distance)
            points.append(point)
        return points

    class Step:
        def __init__(self, distance, bearing):
            self.distance = distance
            self.bearing = bearing
