#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
import copy

from src.event.event_meta import Event
from src.utils.geometry import get_bearing_between_points, get_distance_between_points, get_angle_in_proper_range, get_point_at_bearing

MINIMUM_USEFUL_SEQUENCE_LENGTH = 5

SPEED_ROUNDING = 1
ANGLE_ROUNDING = 0
SLIDE_ROUNDING = 0

class Sequence:
    def __init__(self, events: list[Event]):
        assert len(events) >= MINIMUM_USEFUL_SEQUENCE_LENGTH >= 2
        first_event = events[0]
        last_event = events[-1]

        self.initial_track_speed = round(first_event.track_speed, SPEED_ROUNDING)
        self.initial_slide = round(first_event.slide, SLIDE_ROUNDING)
        self.action_speed = round(first_event.speed, SPEED_ROUNDING)
        self.action_steering_angle = round(first_event.steering_angle, ANGLE_ROUNDING)

        self.final_track_speed = round(last_event.track_speed, SPEED_ROUNDING)
        self.final_slide = round(last_event.slide, SLIDE_ROUNDING)

        self.steps = []
        self._is_invalid = first_event.dodgy_data

        previous_location = (first_event.x, first_event.y)
        for e in events[1:]:
            self._is_invalid = self._is_invalid or e.dodgy_data
            if self._is_invalid:
                return
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

    def is_valid(self):
        return not self._is_invalid

    def get_simple_key(self):
        return str(self.initial_track_speed) + "#" + str(self.initial_slide) + "#" + str(
            self.action_speed) + "#" + str(self.action_steering_angle)

    def get_simple_inverted_key(self):
        return str(self.initial_track_speed) + "#" + str(-self.initial_slide) + "#" + str(
            self.action_speed) + "#" + str(-self.action_steering_angle)

    def get_length(self):
        return len(self.steps)

    def invert(self):
        self.action_steering_angle = -self.action_steering_angle
        self.initial_slide = -self.initial_slide
        self.final_slide = -self.final_slide
        for s in self.steps:
            s.invert()

    def build_inverted_copy(self):
        inversion = copy.deepcopy(self)
        inversion.invert()
        return inversion

    def print_debug(self):
        print("Length = ", self.get_length())
        print("Key = ", self.get_simple_key())

    def matches(self, initial_track_speed, initial_slide, action_speed, action_steering_angle):
        return self._matches_value(initial_track_speed, self.initial_track_speed, SPEED_ROUNDING) and \
               self._matches_value(initial_slide, self.initial_slide, SLIDE_ROUNDING) and \
               self._matches_value(action_speed, self.action_speed, SPEED_ROUNDING) and \
               self._matches_value(action_steering_angle, self.action_steering_angle, ANGLE_ROUNDING)

    @staticmethod
    def _matches_value(filter_value, real_value, rounding: int):
        if filter_value is None:
            return True
        else:
            (value1, value2) = filter_value
            min_value = round(min(value1, value2), rounding)
            max_value = round(max(value1, value2), rounding)
            return min_value <= real_value <= max_value

    class Step:
        def __init__(self, distance, bearing):
            self.distance = round(distance, 3)
            self.bearing = round(bearing, 3)

        def invert(self):
            self.bearing = -self.bearing
