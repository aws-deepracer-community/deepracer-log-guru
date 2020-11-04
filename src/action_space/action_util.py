
def get_min_and_max_action_speeds(action_space):
    min_speed = 999
    max_speed = 0
    for action in action_space:
        if action:
            min_speed = min(action.speed, min_speed)
            max_speed = max(action.speed, max_speed)

    return min_speed, max_speed


def is_high_speed(speed):
    return speed > 3

def is_medium_speed(speed):
    return 2 <= speed <= 3

def is_low_speed(speed):
    return speed < 2

def is_left_turn(steering_angle):
    return steering_angle > 0.0001

def is_right_turn(steering_angle):
    return steering_angle < -0.0001
