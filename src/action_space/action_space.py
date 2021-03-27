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

    def get_all_actions(self):
        return self._actions

    def get_all_action_names_for_x_axis(self):
        names = []
        for action in self._actions:
            names.append(action.get_readable_for_x_axis())
        return names

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


