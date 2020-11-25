class EpisodeFilter:

    def __init__(self):
        self.filter_from_start_line = False
        self.filter_max_steps = None
        self.filter_min_percent = None
        self.filter_complete_section = None
        self.filter_complete_section_time = None
        self.filter_complete_section_steps = None
        self.filter_min_average_reward = None
        self.filter_peak_track_speed = None
        self.filter_specific_waypoint_id = None
        self.filter_specific_waypoint_min_reward = None
        self.filter_quarters = [ True, True, True, True ]
        self.filter_debug_contains = None
        self.filter_max_skew = None

        self.all_episodes = None

    def reset(self):
        self.filter_from_start_line = False
        self.filter_max_steps = None
        self.filter_min_percent = None
        self.filter_complete_section = None
        self.filter_complete_section_time = None
        self.filter_complete_section_steps = None
        self.filter_min_average_reward = None
        self.filter_peak_track_speed = None
        self.filter_specific_waypoint_id = None
        self.filter_specific_waypoint_min_reward = None
        self.filter_quarters = [ True, True, True, True ]
        self.filter_debug_contains = None
        self.filter_max_skew = None


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

    def set_filter_peak_track_speed(self, peak_track_speed):
        self.filter_peak_track_speed = peak_track_speed

    def set_filter_specific_waypoint_reward(self, waypoint_id :int, min_reward :float):
        self.filter_specific_waypoint_id = waypoint_id

        if waypoint_id is not None:
            self.filter_specific_waypoint_min_reward = min_reward
        else:
            self.filter_specific_waypoint_min_reward = None

    def set_filter_debug_contains(self, debug_contains):
        self.filter_debug_contains = debug_contains

    def set_filter_max_skew(self, max_skew):
        self.filter_max_skew = max_skew

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
                                    if self.filter_max_skew is None or e.max_skew <= self.filter_max_skew:
                                        if self.matches_complete_section_filter(e, track):
                                            if self.matches_specific_waypoint_reward_filter(e):
                                                if self.filter_debug_contains is None or e.does_debug_contain(self.filter_debug_contains):
                                                    result.append(e)

        return result

    def matches_specific_waypoint_reward_filter(self, episode):
        if self.filter_specific_waypoint_id is None:
            return True
        else:
            for e in episode.events:
                if e.closest_waypoint_index == self.filter_specific_waypoint_id and (
                            self.filter_specific_waypoint_min_reward is None or e.reward >= self.filter_specific_waypoint_min_reward):
                    return True

        return False

    def matches_complete_section_filter(self, episode, track):
        if not self.filter_complete_section:
            return True

        if not self.filter_complete_section_time and not self.filter_complete_section_steps:
            return True

        (start, finish) = self.filter_complete_section

        events = episode.get_section_start_and_finish_events(start, finish, track)
        if not events:
            return False

        (start_event, finish_event) = events

        time_ok = not self.filter_complete_section_time or finish_event.time - start_event.time <= self.filter_complete_section_time
        steps_ok = not self.filter_complete_section_steps or finish_event.step - start_event.step <= self.filter_complete_section_steps

        return time_ok and steps_ok