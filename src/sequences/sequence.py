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
    def __init__(self):
        self.initial_track_speed = 0
        self.initial_slide = 0
        self.action_speed = 0
        self.action_steering_angle = 0
        self.final_track_speed = 0
        self.final_slide = 0
        self.max_slide = 0
        self.steps = []
        self._is_invalid = True
        self._add_on = None

    def set_from_events(self, events: list[Event]):
        assert len(events) >= MINIMUM_USEFUL_SEQUENCE_LENGTH >= 2
        first_event = events[0]
        last_event = events[-1]

        self.initial_track_speed = round(first_event.track_speed / 2, SPEED_ROUNDING) * 2
        self.initial_slide = round(first_event.slide / 2, SLIDE_ROUNDING) * 2
        self.action_speed = round(first_event.speed, SPEED_ROUNDING)
        self.action_steering_angle = round(first_event.steering_angle, ANGLE_ROUNDING)

        self.final_track_speed = round(last_event.track_speed / 2, SPEED_ROUNDING) * 2
        self.final_slide = round(last_event.slide / 2, SLIDE_ROUNDING) * 2

        self.max_slide = abs(round(first_event.slide, SLIDE_ROUNDING))

        self.steps = []
        self._is_invalid = first_event.dodgy_data
        self._add_on = None

        previous_location = (first_event.x, first_event.y)
        for e in events[1:]:
            self._is_invalid = self._is_invalid or e.dodgy_data
            if self._is_invalid:
                return
            current_location = (e.x, e.y)
            distance = get_distance_between_points(previous_location, current_location)
            original_bearing = e.true_bearing
            relative_bearing = get_angle_in_proper_range(original_bearing - first_event.true_bearing)
            elapsed_time = e.time - first_event.time
            self.steps.append(Sequence.Step(distance, relative_bearing, elapsed_time))
            self.max_slide = max(self.max_slide, abs(round(e.slide, SLIDE_ROUNDING)))
            previous_location = current_location

    def get_plot_points(self, point, initial_heading, with_add_on=True):
        points = [point]
        for s in self.steps:
            point = get_point_at_bearing(point, s.bearing + initial_heading, s.distance)
            points.append(point)
        if with_add_on and self._add_on is not None:
            points += self._add_on.get_plot_points(point, self.steps[-1].bearing + initial_heading, False)
        return points

    def is_valid(self):
        return not self._is_invalid

    def get_simple_key(self):
        return str(self.initial_track_speed) + "#" + str(self.initial_slide) + "#" + str(
            self.action_speed) + "#" + str(self.action_steering_angle)

    def get_simple_inverted_key(self):
        return str(self.initial_track_speed) + "#" + str(-self.initial_slide) + "#" + str(
            self.action_speed) + "#" + str(-self.action_steering_angle)

    def get_simple_key_for_add_on(self):
        return str(self.final_track_speed) + "#" + str(self.final_slide) + "#" + str(
            self.action_speed) + "#" + str(self.action_steering_angle)

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

    def set_add_on(self, add_on):
        self._add_on = add_on

    def print_debug(self):
        print(
            "Action: ", self.action_speed, self.action_steering_angle,
            "Entry speed/slide:", self.initial_track_speed, self.initial_slide,
            "Final speed/slide:", self.final_track_speed, self.final_slide,
            "Max slide:", self.max_slide,
            "Length:", self.get_length(),
            "Has Add-on", self._add_on is not None
        )

    def get_as_json(self):
        new_json = dict()
        new_json["initial_track_speed"] = self.initial_track_speed
        new_json["initial_slide"] = self.initial_slide
        new_json["action_speed"] = self.action_speed
        new_json["action_steering_angle"] = self.action_steering_angle
        new_json["final_track_speed"] = self.final_track_speed
        new_json["final_slide"] = self.final_slide
        new_json["max_slide"] = self.max_slide

        steps_json = []
        for s in self.steps:
            steps_json.append(s.get_as_json())

        new_json["steps"] = steps_json
        return new_json

    def set_from_json(self, received_json):
        self.initial_track_speed = received_json["initial_track_speed"]
        self.initial_slide = received_json["initial_slide"]
        self.action_speed = received_json["action_speed"]
        self.action_steering_angle = received_json["action_steering_angle"]
        self.final_track_speed = received_json["final_track_speed"]
        self.final_slide = received_json["final_slide"]
        self.max_slide = received_json["max_slide"]

        self.steps = []
        for s in received_json["steps"]:
            new_step = Sequence.Step(0, 0, 0)
            new_step.set_from_json(s)
            self.steps.append(new_step)

        self._is_invalid = False
        self._add_on = None

    def matches(self, initial_track_speed, initial_slide, action_speed, action_steering_angle):
        return self._matches_value(initial_track_speed, self.initial_track_speed) and \
               self._matches_value(initial_slide, self.initial_slide) and \
               self._matches_value(action_speed, self.action_speed) and \
               self._matches_value(action_steering_angle, self.action_steering_angle)

    @staticmethod
    def _matches_value(filter_value, real_value):
        if filter_value is None:
            return True
        else:
            (value1, value2) = filter_value
            min_value = min(value1, value2)
            max_value = max(value1, value2)
            return min_value <= real_value <= max_value

    class Step:
        def __init__(self, distance, bearing, elapsed_time):
            self.distance = round(distance, 3)
            self.bearing = round(bearing, 3)
            self.elapsed_time = round(elapsed_time, 2)

        def invert(self):
            self.bearing = -self.bearing

        def get_as_json(self):
            new_json = dict()
            new_json["distance"] = self.distance
            new_json["bearing"] = self.bearing
            new_json["elapsed_time"] = self.elapsed_time
            return new_json

        def set_from_json(self, received_json):
            self.distance = received_json["distance"]
            self.bearing = received_json["bearing"]
            self.elapsed_time = received_json["elapsed_time"]

