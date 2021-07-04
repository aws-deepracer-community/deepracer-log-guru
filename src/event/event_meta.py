#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from src.tracks.track import Track

_STATUS_OFF_TRACK = "off_track"

_STATUS_CRASHED = "crashed"    # TODO - get correct value, this is just a guess
_STATUS_REVERSED = "reversed"    # TODO - get correct value, this is just a guess


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

        self.debug_log = ""

        # Data added separately (everything above comes direct from the log, whereas this is calculated by us ...
        self.before_waypoint_index = 0
        self.after_waypoint_index = 0
        self.track_speed = 0.0
        self.progress_speed = 0.0
        self.reward_total = 0.0
        self.average_reward_so_far = 0.0
        self.time_elapsed = 0.0
        self.total_distance_travelled = 0.0
        self.slide = 0.0
        self.skew = 0.0
        self.true_bearing = 0.0
        self.distance_from_center = 0.0
        self.sequence_count = 0
        self.discounted_future_rewards = []
        self.new_reward = 0.0
        self.new_reward_total = 0.0
        self.new_discounted_future_reward = 0.0
        self.acceleration = 0.0
        self.braking = 0.0
        self.projected_travel_distance = 0.0
        self.track_side = "L"

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

    def get_reward_input_params(self, current_track: Track):
        point = (self.x, self.y)
        side = current_track.get_position_of_point_relative_to_waypoint(point, self.closest_waypoint_index)
        params = {
            'all_wheels_on_track': self.all_wheels_on_track,
            'x': self.x,
            'y': self.y,
            'heading': self.heading,
            'distance_from_center': self.distance_from_center,
            'projection_distance': 0.0,             # TODO
            'progress': self.progress,
            'steps': float(self.step),
            'speed': float(self.speed),
            'steering_angle': float(self.steering_angle),
            'track_width': current_track.get_width(),
            'track_length': float(self.track_length),
            'waypoints': current_track.get_all_waypoints(),
            'closest_waypoints': [int(self.before_waypoint_index), int(self.after_waypoint_index)],
            'is_left_of_center': side == "L",
            'is_reversed': self.status == _STATUS_REVERSED,
            'is_crashed': self.status == _STATUS_CRASHED,
            'is_offtrack': self.status == _STATUS_OFF_TRACK,
            'closest_objects': [0, 0],              # TODO
            'objects_location': [],                 # TODO
            'objects_left_of_center': [],           # TODO
            'object_in_camera': [],                 # TODO
            'objects_speed': [],                    # TODO
            'objects_heading': [],                  # TODO
            'objects_distance_from_center': [],     # TODO
            'objects_distance': []                  # TODO
        }
        return params

        # SAMPLE AS AT 31st MARCH 2021:
        #
        # 'all_wheels_on_track': True
        # 'x': 4.085043155152535
        # 'y': 0.6837354098890907
        # 'heading': 0.034683898621264996
        # 'distance_from_center': 0.00012227425889283888
        # 'projection_distance': 1.025310673102175
        # 'progress': 0.7897196081016897
        # 'steps': 2.0
        # 'speed': 1.3333333333333333
        # 'steering_angle': 15.0
        # 'track_width': 0.7619997315412399
        # 'track_length': 17.709159380834848
        # 'waypoints': [(3.059733510017395, 0.6826554089784622), (3.2095088958740234, 0.6831344813108444), ... ... ...
        # 'closest_waypoints': [6, 7]
        # 'is_left_of_center': True
        # 'is_reversed': False
        # 'closest_objects': [0, 0]
        # 'objects_location': []
        # 'objects_left_of_center': []
        # 'object_in_camera': False
        # 'objects_speed': []
        # 'objects_heading': []
        # 'objects_distance_from_center': []
        # 'objects_distance': []
        # 'is_crashed': False
        # 'is_offtrack': False
