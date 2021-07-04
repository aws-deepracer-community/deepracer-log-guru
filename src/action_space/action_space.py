#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.action_space.action import Action


class ActionSpace:
    #
    # PUBLIC interface
    #

    def __init__(self):
        self._actions = []
        self._min_speed = 0.0
        self._max_speed = 0.0
        self._speed_range = 0.0
        self._is_continuous = False
        self._continuous_speed = None
        self._continuous_steering = None

    def add_action(self, action: Action) -> None:
        assert action.get_index() == len(self._actions)
        self._actions.append(action)
        if action.get_index() == 0:
            self._min_speed = action.get_speed()
            self._max_speed = action.get_speed()
        else:
            self._min_speed = min(self._min_speed, action.get_speed())
            self._max_speed = max(self._max_speed, action.get_speed())
        self._speed_range = self._max_speed - self._min_speed

    def get_action(self, index: int) -> Action:
        return self._actions[index]

    def mark_as_continuous(self):
        self._is_continuous = True

    def is_continuous(self):
        return self._is_continuous

    def define_continuous_action_limits(self, low_speed: float, high_speed: float, low_steering: float, high_steering: float):
        assert 0 <= low_speed <= high_speed <= 4
        assert -30 <= low_steering <= high_steering <= 30
        self._continuous_speed = (low_speed, high_speed)
        self._continuous_steering = (low_steering, high_steering)

        self._min_speed = low_speed
        self._max_speed = high_speed
        self._speed_range = self._max_speed - self._min_speed

    def get_continuous_action_limits(self):
        assert self._is_continuous
        (low_speed, high_speed) = self._continuous_speed
        (low_steering, high_steering) = self._continuous_steering
        return low_speed, high_speed, low_steering, high_steering

    def get_all_actions(self):
        return self._actions

    def get_number_of_actions(self):
        return len(self._actions)

    def get_new_frequency_counter(self):
        return [0] * len(self._actions)

    def get_new_boolean_marker(self, default_value: bool):
        return [default_value] * len(self._actions)

    def get_new_boolean_marker_that_matches(self, matching_function: callable):
        new_marker = []
        action: Action
        for action in self._actions:
            new_marker.append(matching_function(action))
        return new_marker

    def get_min_speed(self):
        return self._min_speed

    def get_max_speed(self):
        return self._max_speed

    def get_speed_range(self):
        return self._speed_range

    def is_high_speed(self, speed: float):
        return speed >= self._max_speed - 0.33 * self._speed_range

    def is_medium_speed(self, speed: float):
        return self._max_speed - 0.66 * self._speed_range <= speed < self._max_speed - 0.33 * self._speed_range

    def is_low_speed(self, speed: float):
        return speed < self._max_speed - 0.66 * self._speed_range

    def is_high_speed_action(self, action: Action):
        return self.is_high_speed(action.get_speed())

    def is_medium_speed_action(self, action: Action):
        return self.is_medium_speed(action.get_speed())

    def is_low_speed_action(self, action: Action):
        return self.is_low_speed(action.get_speed())
