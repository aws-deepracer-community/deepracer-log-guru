class EpisodeFilter:

    def __init__(self):
        self.filter_complete_laps = False
        self.filter_from_start_line = False
        self.filter_max_steps = 0
        self.filter_min_percent = 0
        self.filter_complete_section = None
        self.filter_min_average_reward = 0
        self.filter_peak_track_speed = 0
        self.filter_specific_waypoint_id = -1
        self.filter_specific_waypoint_min_reward = 0

        self.all_episodes = None

    def reset(self):
        self.filter_complete_laps = False
        self.filter_from_start_line = False
        self.filter_max_steps = 0
        self.filter_min_percent = 0
        self.filter_complete_section = None
        self.filter_min_average_reward = 0
        self.filter_peak_track_speed = 0
        self.filter_specific_waypoint_id = -1
        self.filter_specific_waypoint_min_reward = 0

    def set_filter_complete_laps(self, setting :bool):
        self.filter_complete_laps = setting

    def set_filter_from_start_line(self, setting :bool):
        self.filter_from_start_line = setting

    def set_filter_max_steps(self, setting: int):
        self.filter_max_steps = setting

    def set_filter_min_percent(self, percent: int):
        self.filter_min_percent = percent

    def set_filter_min_average_reward(self, min_reward: int):
        self.filter_min_average_reward = min_reward

    def set_filter_complete_section(self, waypoint_id_1, waypoint_id_2):
        self.filter_complete_section = (waypoint_id_1, waypoint_id_2)

    def set_filter_peak_track_speed(self, peak_track_speed):
        self.filter_peak_track_speed = peak_track_speed

    def set_filter_specific_waypoint_reward(self, waypoint_id :int, min_reward :float):
        self.filter_specific_waypoint_id = waypoint_id
        self.filter_specific_waypoint_min_reward = min_reward

    def set_all_episodes(self, all_episodes):
        self.all_episodes = all_episodes

    def get_filtered_episodes(self):
        if not self.all_episodes:
            return None

        result = []
        for e in self.all_episodes:
            if e.lap_complete or not self.filter_complete_laps:
                if e.is_real_start or not self.filter_from_start_line:
                    if e.step_count <= self.filter_max_steps or self.filter_max_steps == 0:
                        if e.percent_complete >= self.filter_min_percent:
                            if e.average_reward >= self.filter_min_average_reward:
                                if e.peak_track_speed >= self.filter_peak_track_speed:
                                    if self.matches_complete_section_filter(e):
                                        if self.matches_specific_waypoint_reward_filter(e):
                                            result.append(e)

        return result

    def matches_specific_waypoint_reward_filter(self, episode):
        if self.filter_specific_waypoint_id < 0 or self.filter_specific_waypoint_min_reward == 0:
            return True
        else:
            for e in episode.events:
                if e.closest_waypoint_index == self.filter_specific_waypoint_id and e.reward >= self.filter_specific_waypoint_min_reward:
                    return True

        return False

    def matches_complete_section_filter(self, episode):
        if self.filter_complete_section == None:
            return True

        (start, finish) = self.filter_complete_section

        actual_start = episode.events[0].closest_waypoint_index
        actual_finish = episode.events[-1].closest_waypoint_index

        # This logic is only for finish >= start    # the opposite is TODO (i.e. crosing start line)
        assert(finish >= start)

        if actual_start <= start and actual_finish >= finish:
            return True

        if actual_finish >= finish and actual_start > actual_finish:
            return True

        if actual_start > actual_finish and actual_start <= start:
            return True

        return False