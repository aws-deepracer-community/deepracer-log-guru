import math

class Event:
    def __init__(self):
        self.episode = 0
        self.step = 0
        self.x = 0.0
        self.y = 0.0
        self.heading = 0.0
        self.steering_angle = 0.0
        self.speed = 0.0
        self.action_taken = 0
        self.reward = 0.0
        self.job_completed = False
        self.all_wheels_on_track = True
        self.progress = 0.0
        self.closest_waypoint_index = 0
        self.time = 0.0
        self.status = ""

        self.debug_log = ""

        # Data added separately (everything above comes direct from the log, whereas this is calculated by us ...
        self.track_speed = 0

