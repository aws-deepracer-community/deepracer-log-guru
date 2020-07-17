
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
