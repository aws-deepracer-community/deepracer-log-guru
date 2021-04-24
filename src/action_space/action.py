#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import src.utils.formatting as formatting
import src.utils.geometry as geometry


class Action:
    #
    # PUBLIC interface
    #

    def __init__(self, index, speed, steering_angle):
        self._index = index
        self._speed = speed
        self._steering_angle = steering_angle

        self._is_left = geometry.is_left_bearing(steering_angle)
        self._is_right = geometry.is_right_bearing(steering_angle)
        self._is_straight = not (self._is_left or self._is_right)

        if self._is_left:
            self._print_steering = "L +" + formatting.get_pretty_small_float(steering_angle, 30, 0)
        elif self._is_right:
            self._print_steering = "R -" + formatting.get_pretty_small_float(-steering_angle, 30, 0)
        else:
            self._print_steering = "AHEAD"

        self._print_speed = formatting.get_pretty_small_float(speed, 4, 1) + " m/s"
        self._print_str = self._print_steering + " @ " + self._print_speed

    def get_index(self) -> int:
        return self._index

    def get_speed(self) -> float:
        return self._speed

    def get_steering_angle(self) -> float:
        return self._steering_angle

    def is_steering_left(self) -> bool:
        return self._is_left

    def is_steering_right(self) -> bool:
        return self._is_right

    def is_steering_straight(self) -> bool:
        return self._is_straight

    def get_steering_group_name(self) -> str:
        if self._is_straight:
            return "Ahead"
        elif abs(self._steering_angle) <= 15:
            severity = "Gentle"
        else:
            severity = "Hard"
        if self._is_left:
            return severity + " Left"
        else:
            return severity + " Right"

    def get_speed_group_name(self) -> str:
        return self._print_speed

    def get_readable_without_index(self) -> str:
        return self._print_str

    def get_readable_with_index(self) -> str:
        if self._index < 10:
            prepend = " "
        else:
            prepend = ""
        return prepend + str(self._index) + ": " + self._print_str

    def get_readable_for_x_axis(self) -> str:
        return str(self._index) + ": \n" + self._print_steering + "\n" + self._print_speed

    def is_same_as(self, another_action: 'Action') -> bool:
        return self._speed == another_action.get_speed() and \
               self._steering_angle == another_action.get_steering_angle() and \
               self._index == another_action.get_index()

