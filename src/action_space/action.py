
MAX_POSSIBLE_ACTIONS = 30

class Action:

    def __init__(self, index, speed, steering_angle):
        assert index < MAX_POSSIBLE_ACTIONS

        self.index = index
        self.speed = speed
        self.steering_angle = steering_angle

        self.is_left = steering_angle > 0.0001
        self.is_right = steering_angle < -0.0001

        if self.is_left:
            self.print_str_ = "L +" + get_pretty_number_(steering_angle, 30, 0)
        elif self.is_right:
            self.print_str_ = "R -" + get_pretty_number_(-steering_angle, 30, 0)
        else:
            self.print_str_ = "AHEAD"

        self.print_str_ += " @ " + get_pretty_number_(speed, 4, 1) + " m/s"

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

def get_pretty_number_(number, max, decimal_places):
    assert 0 <= decimal_places <= 1

    if max >= 10 and abs(round(number, decimal_places)) < 10:
        prepend = " "
    else:
        prepend = ""

    full_str = prepend + str(round(number, decimal_places))

    if full_str.count(".") == 1 and decimal_places == 0:
        return full_str[0:-2]
    elif full_str.endswith(".0") and decimal_places == 1:
        return full_str[0:-2] + "  "
    elif full_str.count(".") == 0 and decimal_places == 1:
        return full_str + "  "
    else:
        return full_str

#print("<<" + get_pretty_number_(9.9999, 30, 0) + ">>")
#print("<<" + get_pretty_number_(10, 30, 0) + ">>")
#print("<<" + get_pretty_number_(10.001, 30, 0) + ">>")

#print("<<" + get_pretty_number_(9.9999, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10.001, 30, 1) + ">>")
#print("<<" + get_pretty_number_(10.101, 30, 1) + ">>")


#print(round(20, 3))