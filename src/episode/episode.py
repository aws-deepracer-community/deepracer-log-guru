import math
import typing

import numpy as np

from src.action_space.action_space_filter import ActionSpaceFilter
from src.action_space.action_space import ActionSpace
from src.analyze.util.heatmap import HeatMap
from src.analyze.util.visitor import VisitorMap
from src.utils.geometry import get_bearing_between_points, get_turn_between_directions,\
    get_distance_between_points, get_distance_of_point_from_line

from src.tracks.track import Track

SLIDE_SETTLING_PERIOD = 6


class Episode:

    def __init__(self, id, iteration, events, object_locations, action_space: ActionSpace):

        self.events = events
        self.id = id
        self.iteration = iteration
        self.object_locations = object_locations

        first_event = events[0]
        last_event = events[-1]

        if last_event.status == "lap_complete":
            self.lap_complete = True
            self.percent_complete = 100
        elif len(events) == 1:
            self.lap_complete = False
            self.percent_complete = last_event.progress
        else:
            second_to_last_event = events[-2]
            self.lap_complete = False
            self.percent_complete = second_to_last_event.progress

        self.step_count = len(events)
        self.is_real_start = first_event.closest_waypoint_index <= 1

        self.time_taken = last_event.time - first_event.time
        self.predicted_lap_time = 100 / last_event.progress * self.time_taken  # predicted

        self.rewards = self.get_list_of_rewards()
        self.total_reward = self.rewards.sum()
        self.average_reward = self.rewards.mean()
        self.predicted_lap_reward = 100 / last_event.progress * self.total_reward  # predicted

        self.action_frequency = self._get_action_frequency(action_space)
        self.repeated_action_percent = self.get_repeated_action_percent()

        self.peak_track_speed = 0
        self.peak_progress_speed = 0
        self.set_track_speed_on_events()
        self.set_progress_speed_on_events()
        self.set_reward_total_on_events()
        self.set_time_elapsed_on_events()
        self.set_total_distance_travelled_on_events()
        self.max_slide = 0.0
        self.set_true_bearing_and_slide_on_events()

        # THESE MUST BE AT THE END SINCE THEY ARE CALCULATED FROM DATA SET FURTHER UP/ABOVE
        self.distance_travelled = self.get_distance_travelled()
        self.flying_start_speed = self.get_track_speed_after_seconds(1)

        # THIS VARIABLE IS ASSIGNED RETROSPECTIVELY AFTER THE Log CLASS HAS LOADED ALL EPISODES
        self.quarter = None

    def set_track(self, track: Track):
        self.set_distance_from_center_on_events(track)

    def get_starting_position_as_percent_from_race_start(self, track :Track):
        first_event_percent = track.get_waypoint_percent_from_race_start(self.events[0].closest_waypoint_index)

        #  5 is magic number because there are 20 evenly spaced start points, i.e. every 5% round the track
        return round(first_event_percent / 5) * 5

    def get_distance_travelled(self):

        if self.events:
            return self.events[-1].total_distance_travelled
        else:
            return 0

    def get_track_speed_after_seconds(self, seconds):
        for e in self.events:
            if e.time_elapsed >= seconds:
                return e.track_speed

    def get_repeated_action_percent(self):
        if not self.events or len(self.events) < 2 or self.percent_complete < 100:
            return 0

        previous_action_taken = self.events[0].action_taken
        count = 0

        for e in self.events[1:]:
            if e.action_taken == previous_action_taken:
                count += 1
            previous_action_taken = e.action_taken

        return 100 * count / len(self.events)

    def set_quarter(self, quarter: int):
        assert 1 <= quarter <= 4
        self.quarter = quarter

    def set_track_speed_on_events(self):
        previous = [self.events[0]] * 6   # 6 here matches DRF, but (TODO) DRF is marginally more accurate algorithm
        for e in self.events:
            distance = get_distance_between_points((e.x, e.y), (previous[0].x, previous[0].y))
            time_taken = e.time - previous[0].time

            if time_taken > 0:
                e.track_speed = distance / time_taken

                if e.track_speed > self.peak_track_speed:
                    self.peak_track_speed = e.track_speed

            previous = previous[1:] + [e]

    def set_progress_speed_on_events(self):
        previous = [self.events[0]] * 5   # 5 here excludes current step so matches DRF of 6 including current step
        for e in self.events:
            progress_gain = e.progress - previous[0].progress
            time_taken = e.time - previous[0].time

            if time_taken > 0:
                e.progress_speed = progress_gain / 100 * e.track_length / time_taken

                if e.progress_speed > self.peak_progress_speed:
                    self.peak_progress_speed = e.progress_speed

            previous = previous[1:] + [e]

    def set_true_bearing_and_slide_on_events(self):

        previous_event = self.events[0]
        self.events[0].slide = 0.0
        self.events[0].true_bearing = self.events[0].heading
        self.max_slide = 0.0

        for e in self.events[1:]:
            previous_location = (previous_event.x, previous_event.y)
            current_location = (e.x, e.y)
            if e.progress == previous_event.progress:   # Handle new AWS bug duplicating log entry position
                e.true_bearing = previous_event.true_bearing
            elif e.progress - previous_event.progress < 0.05:   # x and y rounding means slow progress is inaccurate
                e.true_bearing = previous_event.true_bearing
            else:
                e.true_bearing = get_bearing_between_points(previous_location, current_location)
            e.slide = get_turn_between_directions(e.heading, e.true_bearing)
            if e.step > SLIDE_SETTLING_PERIOD:
                self.max_slide = max(self.max_slide, abs(e.slide))
            previous_event = e

    def set_distance_from_center_on_events(self, track :Track):
        for e in self.events:
            current_location = (e.x, e.y)
            closest_waypoint = track.get_waypoint(e.closest_waypoint_index)
            next_waypoint = track.get_next_different_waypoint(e.closest_waypoint_index)
            previous_waypoint = track.get_previous_different_waypoint(e.closest_waypoint_index)
            distance_of_next_waypoint = get_distance_between_points(current_location, next_waypoint)
            distance_of_previous_waypoint = get_distance_between_points(current_location, previous_waypoint)
            if distance_of_next_waypoint < distance_of_previous_waypoint:
                e.distance_from_center = get_distance_of_point_from_line(current_location, closest_waypoint, next_waypoint)
            else:
                e.distance_from_center = get_distance_of_point_from_line(current_location, closest_waypoint, previous_waypoint)



    def set_reward_total_on_events(self):
        reward_total = 0.0
        for e in self.events:
            reward_total += e.reward
            e.reward_total = reward_total
            e.average_reward_so_far = reward_total / e.step

    def set_time_elapsed_on_events(self):
        start_time = self.events[0].time
        for e in self.events:
            e.time_elapsed = e.time - start_time

    def set_total_distance_travelled_on_events(self):
        distance = 0.0
        previous = self.events[0]

        for e in self.events:
            x_diff = e.x - previous.x
            y_diff = e.y - previous.y
            distance += math.sqrt(x_diff * x_diff + y_diff * y_diff)
            e.total_distance_travelled = distance
            previous = e

    def get_list_of_rewards(self):
        list_of_rewards = []
        for e in self.events:
            list_of_rewards.append(e.reward)
        return np.array(list_of_rewards)

    def _get_action_frequency(self, action_space: ActionSpace):
        action_frequency = action_space.get_new_frequency_counter()
        for e in self.events:
            action_frequency[e.action_taken] += 1
        return action_frequency

    def get_closest_event_to_point(self, point):
        (x, y) = point
        event = None
        index = -1
        distance = 0

        for i, e in enumerate(self.events):
            d = (e.x - x) * (e.x - x) + (e.y - y) * (e.y - y)
            if d < distance or not event:
                event = e
                distance = d
                index = i

        return event, index

    def apply_visits_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, 1)
            previous = e

    def apply_action_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, e.speed)
            previous = e

    def apply_progress_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, e.progress_speed)
            previous = e

    def apply_track_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, e.track_speed)
            previous = e

    def apply_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, e.reward)
            previous = e

    def apply_slide_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, abs(e.slide))
            previous = e

    def apply_steering_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter):
        previous = self.events[0]
        for e in self.events:
            if e.step >= skip_start and action_space_filter.should_show_action(e.action_taken):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, 30 - abs(e.steering_angle))
            previous = e

    def _apply_event_stat_to_heat_map(self, e, previous, heat_map: HeatMap, stat: typing.Union[float, int]):
        stat = max(0, stat)
        heat_map.visit(e.x, e.y, self, stat)
        x_diff = e.x - previous.x
        y_diff = e.y - previous.y
        heat_map.visit(e.x - 0.25 * x_diff, e.y - 0.25 * y_diff, self, stat)
        heat_map.visit(e.x - 0.50 * x_diff, e.y - 0.50 * y_diff, self, stat)
        heat_map.visit(e.x - 0.75 * x_diff, e.y - 0.75 * y_diff, self, stat)

    # Only "probably" because spinning can fool this simple logic
    def probably_finishes_section_(self, start, finish):
        actual_start = self.events[0].closest_waypoint_index
        actual_finish = self.events[-1].closest_waypoint_index

        if finish >= start:
            if self.lap_complete:
                if actual_start < start or actual_start > finish:
                    return True

            if actual_start < start and actual_finish > finish:
                return True

            if actual_start > actual_finish and actual_finish > finish:
                return True

            if actual_start > actual_finish and actual_start < start:
                return True
            else:
                return False
        else:
            # Finish is before start, so basically it means the section crosses the start line
            if self.lap_complete:
                if finish < actual_start < start:
                    return True

            if actual_start > actual_finish and finish < actual_start < start and actual_finish > finish:
                return True
            else:
                # I believe no more logic needed here ?!?!?!?!
                return False


    def get_section_start_and_finish_events(self, start, finish, track :Track):
        if not self.probably_finishes_section_(start, finish):
            return None

        start_event = None
        finish_event = None

        start_dist = 9999
        finish_dist = 9999

        for e in self.events:
            if not finish_event and are_close_waypoint_ids(e.closest_waypoint_index, start, track):
                (x2, y2) = track.get_waypoint(start)
                dist = (x2 - e.x) * (x2 - e.x) + (y2 - e.y) * (y2 - e.y)
                if dist < start_dist:
                    start_dist = dist
                    start_event = e
            if start_event and are_close_waypoint_ids(e.closest_waypoint_index, finish, track):
                (x2, y2) = track.get_waypoint(finish)
                dist = (x2 - e.x) * (x2 - e.x) + (y2 - e.y) * (y2 - e.y)
                if dist < finish_dist:
                    finish_dist = dist
                    finish_event = e

        if finish_event:
            return start_event, finish_event
        else:
            return None

    def does_debug_contain(self, search_string):
        for e in self.events:
            if search_string in e.debug_log:
                return True

        return False


def are_close_waypoint_ids(id1, id2, track :Track):
    if abs(id1 - id2) <= 2:
        return True

    if max(id1, id2) >= track.get_number_of_waypoints() - 1 and min(id1, id2) <= 2:
        return True
    else:
        return False



