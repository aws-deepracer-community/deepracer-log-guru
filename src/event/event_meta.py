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
        self.track_length = 0.0
        self.sequence_count = 0

        self.debug_log = ""

        # Data added separately (everything above comes direct from the log, whereas this is calculated by us ...
        self.track_speed = 0.0
        self.progress_speed = 0.0
        self.reward_total = 0.0
        self.average_reward_so_far = 0.0
        self.time_elapsed = 0.0
        self.total_distance_travelled = 0.0
        self.slide = 0.0
        self.true_bearing = 0.0
        self.distance_from_center = 0.0
        self.discounted_future_rewards = []

        self.dodgy_data = False

    def is_within_waypoint_range(self, waypoint_range):
        if waypoint_range:
            (start, finish) = waypoint_range
            if start <= finish:
                return start <= self.closest_waypoint_index <= finish
            else:
                return self.closest_waypoint_index >= start or self.closest_waypoint_index <= finish
        else:
            return True
