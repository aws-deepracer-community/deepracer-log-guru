#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#
from src.episode.episode import ALL_OUTCOMES, POS_XLEFT, POS_LEFT, POS_CENTRAL, POS_RIGHT, POS_XRIGHT

OBJ_NONE = "None"
OBJ_LEFT = "Single Left"
OBJ_MULTIPLE_LEFT = "Multiple Left"
OBJ_RIGHT = "Single Right"
OBJ_MULTIPLE_RIGHT = "Multiple Right"
OBJ_BOTH = "Left and Right"

OBJECT_POSITIONS = ["", OBJ_NONE, OBJ_LEFT, OBJ_MULTIPLE_LEFT, OBJ_RIGHT, OBJ_MULTIPLE_RIGHT, OBJ_BOTH]


class EpisodeFilter:

    def __init__(self):
        self.filter_from_start_line = False
        self.filter_max_steps = None
        self.filter_min_percent = None
        self.filter_min_average_reward = None
        self.filter_peak_track_speed = None

        self.filter_complete_section = None
        self.filter_complete_section_time = None
        self.filter_complete_section_steps = None

        self.filter_object_section = None
        self.filter_object_section_positions = None

        self.filter_specific_waypoint_id = None
        self.filter_specific_waypoint_min_reward = None
        self.filter_specific_waypoint_min_future_reward = None
        self.filter_specific_waypoint_min_track_speed = None
        self.filter_specific_waypoint_max_track_speed = None
        self.filter_specific_waypoint_track_position = None

        self.filter_quarters = [ True, True, True, True ]
        self.filter_debug_contains = None
        self.filter_max_slide = None
        self.filter_outcome = None

        self.all_episodes = None

    def reset(self):
        self.filter_from_start_line = False
        self.filter_max_steps = None
        self.filter_min_percent = None
        self.filter_min_average_reward = None
        self.filter_peak_track_speed = None

        self.filter_complete_section = None
        self.filter_complete_section_time = None
        self.filter_complete_section_steps = None

        self.filter_object_section = None
        self.filter_object_section_positions = None

        self.filter_specific_waypoint_id = None
        self.filter_specific_waypoint_min_reward = None
        self.filter_specific_waypoint_min_future_reward = None
        self.filter_specific_waypoint_min_track_speed = None
        self.filter_specific_waypoint_max_track_speed = None
        self.filter_specific_waypoint_track_position = None

        self.filter_quarters = [ True, True, True, True ]
        self.filter_debug_contains = None
        self.filter_max_slide = None
        self.filter_outcome = None

    def set_filter_from_start_line(self, setting :bool):
        self.filter_from_start_line = setting

    def set_filter_max_steps(self, setting: int):
        self.filter_max_steps = setting

    def set_filter_min_percent(self, percent: int):
        self.filter_min_percent = percent

    def set_filter_min_average_reward(self, min_reward: int):
        self.filter_min_average_reward = min_reward

    def set_filter_quarters(self, q1: bool, q2: bool, q3: bool, q4: bool):
        self.filter_quarters = [ q1, q2, q3, q4 ]

    def set_filter_complete_section_and_time(self, start_waypoint_id, finish_waypoint_id, optional_time, optional_steps):
        self.filter_complete_section_time = optional_time
        self.filter_complete_section_steps = optional_steps

        if start_waypoint_id is not None and finish_waypoint_id is not None:
            self.filter_complete_section = (start_waypoint_id, finish_waypoint_id)
        elif start_waypoint_id is not None:
            self.filter_complete_section = (start_waypoint_id, start_waypoint_id)
        elif finish_waypoint_id is not None:
            self.filter_complete_section = (finish_waypoint_id, finish_waypoint_id)
        else:
            self.filter_complete_section = None

    def set_filter_object_section_and_positions(self, start_waypoint_id, finish_waypoint_id, positions):
        self.filter_object_section_positions = positions

        if start_waypoint_id is not None and finish_waypoint_id is not None:
            self.filter_object_section = (start_waypoint_id, finish_waypoint_id)
        elif start_waypoint_id is not None:
            self.filter_object_section = (start_waypoint_id, start_waypoint_id)
        elif finish_waypoint_id is not None:
            self.filter_object_section = (finish_waypoint_id, finish_waypoint_id)
        else:
            self.filter_object_section = None

    def set_filter_peak_track_speed(self, peak_track_speed):
        self.filter_peak_track_speed = peak_track_speed

    def set_filter_specific_waypoint_reward(self, waypoint_id: int, min_reward: float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_min_reward = min_reward
        else:
            self.filter_specific_waypoint_min_reward = None

    def set_filter_specific_waypoint_future_reward(self, waypoint_id: int, min_future_reward: float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_min_future_reward = min_future_reward
        else:
            self.filter_specific_waypoint_min_future_reward = None

    def set_filter_specific_waypoint_min_track_speed(self, waypoint_id: int, min_track_speed: float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_min_track_speed = min_track_speed
        else:
            self.filter_specific_waypoint_min_track_speed = None

    def set_filter_specific_waypoint_max_track_speed(self, waypoint_id: int, max_track_speed: float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_max_track_speed = max_track_speed
        else:
            self.filter_specific_waypoint_max_track_speed = None

    def set_filter_specific_waypoint_track_position(self, waypoint_id: int, track_position: float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_track_position = track_position
        else:
            self.filter_specific_waypoint_track_position = None

    def set_filter_debug_contains(self, debug_contains):
        self.filter_debug_contains = debug_contains

    def set_filter_max_slide(self, max_slide):
        self.filter_max_slide = max_slide

    def set_filter_outcome(self, outcome):
        assert outcome in ALL_OUTCOMES
        self.filter_outcome = outcome

    def set_all_episodes(self, all_episodes):
        self.all_episodes = all_episodes

    def get_filtered_episodes(self, track):
        if not self.all_episodes:
            return None

        result = []
        for e in self.all_episodes:
            if self.filter_quarters[e.quarter - 1]:
                if e.is_real_start or not self.filter_from_start_line:
                    if self.filter_max_steps is None or e.step_count <= self.filter_max_steps:
                        if self.filter_min_percent is None or e.percent_complete >= self.filter_min_percent:
                            if self.filter_min_average_reward is None or e.average_reward >= self.filter_min_average_reward:
                                if self.filter_peak_track_speed is None or e.peak_track_speed >= self.filter_peak_track_speed:
                                    if self.filter_max_slide is None or e.max_slide <= self.filter_max_slide:
                                        if self.filter_outcome is None or e.outcome == self.filter_outcome:
                                            if self.matches_complete_section_filter(e, track):
                                                if self.matches_object_section_filter(e):
                                                    if self.matches_specific_waypoint_reward_filter(e):
                                                        if self.filter_debug_contains is None or e.does_debug_contain(self.filter_debug_contains):
                                                            result.append(e)
        return result

    def matches_specific_waypoint_reward_filter(self, episode):
        if self.filter_specific_waypoint_id is None:
            return True
        else:
            for e in episode.events:
                if e.closest_waypoint_index == self.filter_specific_waypoint_id:
                    matches = True
                    if self.filter_specific_waypoint_min_reward is not None and e.reward < self.filter_specific_waypoint_min_reward:
                        matches = False
                    if self.filter_specific_waypoint_min_future_reward is not None and e.discounted_future_rewards[0] < self.filter_specific_waypoint_min_future_reward:
                        matches = False
                    if self.filter_specific_waypoint_min_track_speed is not None and e.track_speed < self.filter_specific_waypoint_min_track_speed:
                        matches = False
                    if self.filter_specific_waypoint_max_track_speed is not None and e.track_speed > self.filter_specific_waypoint_max_track_speed:
                        matches = False
                    if self.filter_specific_waypoint_track_position is not None and not self._matches_track_position(e):
                        matches = False
                    if matches:
                        return True
        return False

    def _matches_track_position(self, event):
        if self.filter_specific_waypoint_track_position == POS_XLEFT:
            return event.track_side == "L" and not event.all_wheels_on_track
        if self.filter_specific_waypoint_track_position == POS_LEFT:
            return event.track_side == "L"
        if self.filter_specific_waypoint_track_position == POS_CENTRAL:
            return event.distance_from_center <= 0.1
        if self.filter_specific_waypoint_track_position == POS_RIGHT:
            return event.track_side == "R"
        if self.filter_specific_waypoint_track_position == POS_XRIGHT:
            return event.track_side == "R" and not event.all_wheels_on_track

        return False

    def matches_complete_section_filter(self, episode, track):
        if not self.filter_complete_section:
            return True

        (start, finish) = self.filter_complete_section

        events = episode.get_section_start_and_finish_events(start, finish, track)
        if not events:
            return False

        (start_event, finish_event) = events

        time_ok = not self.filter_complete_section_time or finish_event.time - start_event.time <= self.filter_complete_section_time
        steps_ok = not self.filter_complete_section_steps or finish_event.step - start_event.step <= self.filter_complete_section_steps

        return time_ok and steps_ok

    def matches_object_section_filter(self, episode):
        if not self.filter_object_section:
            return True

        (start, finish) = self.filter_object_section

        left, right = episode.count_objects_in_section(start, finish)

        if self.filter_object_section_positions == OBJ_RIGHT:
            return left == 0 and right == 1
        if self.filter_object_section_positions == OBJ_LEFT:
            return left == 1 and right == 0
        if self.filter_object_section_positions == OBJ_MULTIPLE_RIGHT:
            return left == 0 and right >= 2
        if self.filter_object_section_positions == OBJ_MULTIPLE_LEFT:
            return left >= 2 and right == 0
        if self.filter_object_section_positions == OBJ_BOTH:
            return left >= 1 and right >= 1
        if self.filter_object_section_positions == OBJ_NONE:
            return left == 0 and right == 0
        else:
            assert self.filter_object_section_positions is None or self.filter_object_section_positions == ""
            return True
