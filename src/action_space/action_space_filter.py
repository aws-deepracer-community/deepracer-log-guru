#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.action_space.action_space import ActionSpace
from src.action_space.action import Action


class ActionSpaceFilter:
    def __init__(self):
        self._action_space = ActionSpace()
        self._action_on = self._action_space.get_new_boolean_marker(True)

    def set_new_action_space(self, new_action_space: ActionSpace):
        self._action_space = new_action_space
        self._action_on = new_action_space.get_new_boolean_marker(True)

    def should_show_action(self, index):
        return self._action_on[index]

    def set_filter_all(self):
        self._action_on = self._action_space.get_new_boolean_marker(True)

    def set_filter_high_speed(self):
        self._action_on = self._action_space.get_new_boolean_marker_that_matches(self._action_space.is_high_speed_action)

    def set_filter_medium_speed(self):
        self._action_on = self._action_space.get_new_boolean_marker_that_matches(self._action_space.is_medium_speed_action)

    def set_filter_low_speed(self):
        self._action_on = self._action_space.get_new_boolean_marker_that_matches(self._action_space.is_low_speed_action)

    def set_filter_straight(self):
        self._action_on = self._action_space.get_new_boolean_marker_that_matches(is_straight_action)


def is_straight_action(action: Action):
    return action.is_steering_straight()








