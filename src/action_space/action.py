from src.action_space.action_util import is_left_turn, is_right_turn
from src.utils.formatting import get_pretty_small_float

MAX_POSSIBLE_ACTIONS = 30

class Action:

    def __init__(self, index, speed, steering_angle):
        assert index < MAX_POSSIBLE_ACTIONS

        self.index = index
        self.speed = speed
        self.steering_angle = steering_angle

        self.is_left = is_left_turn(steering_angle)
        self.is_right = is_right_turn(steering_angle)

        if self.is_left:
            self.print_str_ = "L +" + get_pretty_small_float(steering_angle, 30, 0)
        elif self.is_right:
            self.print_str_ = "R -" + get_pretty_small_float(-steering_angle, 30, 0)
        else:
            self.print_str_ = "AHEAD"

        self.print_str_ += " @ " + get_pretty_small_float(speed, 4, 1) + " m/s"

    def get_readable_without_index(self):
        return self.print_str_

    def get_readable_with_index(self):
        if self.index < 10:
            prepend = " "
        else:
            prepend = ""
        return prepend + str(self.index) + ": " + self.print_str_

    def is_same_as(self, another_action):
        return self.speed == another_action.speed and\
               self.steering_angle == another_action.steering_angle and\
               self.index == another_action.index
