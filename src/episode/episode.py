#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import math
import typing

import numpy as np

from src.action_space.action_space_filter import ActionSpaceFilter
from src.action_space.action_space import ActionSpace
from src.analyze.util.heatmap import HeatMap
from src.event.event_meta import Event
from src.sequences.sequences import Sequences
from src.utils.geometry import get_bearing_between_points, get_turn_between_directions,\
    get_distance_between_points, get_distance_of_point_from_line

from src.tracks.track import Track
from src.sequences.sequence import Sequence
from src.utils.discount_factors import discount_factors

from src.personalize.configuration.analysis import NEW_REWARD_FUNCTION, TIME_BEFORE_FIRST_STEP

SLIDE_SETTLING_PERIOD = 6

REVERSED = "R"
OFF_TRACK = "OT"
CRASHED = "C"
LAP_COMPLETE = "LP"
LOST_CONTROL = "LC"

ALL_OUTCOMES = [REVERSED, OFF_TRACK, CRASHED, LAP_COMPLETE, LOST_CONTROL]

POS_XLEFT = "XL"
POS_LEFT = "L"
POS_CENTRAL = "C"
POS_RIGHT = "R"
POS_XRIGHT = "XR"

ALL_POSITIONS = [POS_XLEFT, POS_LEFT, POS_CENTRAL, POS_RIGHT, POS_XRIGHT]


class Episode:

    def __init__(self, episode_id, iteration, events, object_locations, action_space: ActionSpace,
                 do_full_analysis: bool, track: Track = None,
                 calculate_new_reward=False, calculate_alternate_discount_factors=False):

        assert track is not None or not do_full_analysis

        self.events = events
        self.id = episode_id
        self.iteration = iteration
        self.object_locations = object_locations

        first_event = events[0]
        last_event = events[-1]

        if last_event.status == "lap_complete":
            self.outcome = LAP_COMPLETE
        elif last_event.status == "reversed":
            self.outcome = REVERSED
        elif last_event.status == "off_track":
            self.outcome = OFF_TRACK
        elif last_event.status == "crashed":
            self.outcome = CRASHED
        else:
            assert last_event.status == "immobilized"
            self.outcome = LOST_CONTROL

        if self.outcome == LAP_COMPLETE:
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

        self.time_taken = last_event.time - first_event.time + TIME_BEFORE_FIRST_STEP
        self.predicted_lap_time = 100 / last_event.progress * self.time_taken

        self.rewards = self.get_list_of_rewards()
        np_rewards = np.array(self.rewards)
        self.total_reward = np_rewards.sum()
        self.average_reward = np_rewards.mean()
        self.predicted_lap_reward = 100 / last_event.progress * self.total_reward  # predicted

        if action_space.is_continuous():
            self.action_frequency = None
            self.repeated_action_percent = None
        else:
            self.action_frequency = self._get_action_frequency(action_space)
            self.repeated_action_percent = self.get_repeated_action_percent(self.events)

        self._mark_dodgy_data()   # Must be first, before all the analysis below, especially for speeds

        self.peak_track_speed = 0
        self.peak_progress_speed = 0
        self.set_track_speed_on_events()
        self.set_progress_speed_on_events()
        self.set_reward_total_on_events()
        self.set_time_elapsed_on_events()
        self.set_total_distance_travelled_on_events()
        self.max_slide = 0.0
        self.set_true_bearing_and_slide_on_events()
        self.set_sequence_length_on_events()
        self.set_acceleration_and_braking_on_events()

        if do_full_analysis:
            (self._blocked_left_waypoints, self._blocked_right_waypoints,
             self._blocked_left_object_locations, self._blocked_right_object_locations) = self.get_blocked_waypoints(track)
            self.set_projected_distances_on_events(track)   # Relies on blocked waypoints
            self._set_side_and_distance_from_center_on_events(track)
            self._set_before_and_after_waypoints_on_events(track)
            self._set_skew_on_events(track)   # Relies on before and after

            if calculate_new_reward:
                self._set_new_rewards(track)
                self.new_rewards = self._get_list_of_new_rewards()
                self._set_new_discounted_future_reward()
                self.new_discounted_future_rewards = self._get_list_of_new_discounted_future_rewards()
            else:
                self.new_rewards = None
                self.new_discounted_future_rewards = None

            self._set_discounted_future_rewards(calculate_alternate_discount_factors)
            self.discounted_future_rewards = self._get_lists_of_discounted_future_rewards()
        else:
            self.new_rewards = []
            self.new_discounted_future_rewards = []
            self._blocked_left_waypoints = []
            self._blocked_right_waypoints = []
            self._blocked_left_object_locations = []
            self._blocked_right_object_locations = []

        # THESE MUST BE AT THE END SINCE THEY ARE CALCULATED FROM DATA SET FURTHER UP/ABOVE
        self.distance_travelled = self.get_distance_travelled()
        self.flying_start_speed = self.get_track_speed_after_seconds(1)

        # THIS VARIABLE IS ASSIGNED RETROSPECTIVELY AFTER THE Log CLASS HAS LOADED ALL EPISODES
        self.quarter = None

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

    # Otherwise known as "smoothness"
    @staticmethod
    def get_repeated_action_percent(events):
        if not events or len(events) < 2:
            return 0

        previous_action_taken = events[0].action_taken
        count = 0

        for e in events[1:]:
            if e.action_taken == previous_action_taken:
                count += 1
            previous_action_taken = e.action_taken

        return 100 * count / len(events)

    def set_quarter(self, quarter: int):
        assert 1 <= quarter <= 4
        self.quarter = quarter

    def _mark_dodgy_data(self):
        e: Event
        for i, e in enumerate(self.events[1:-1]):
            previous_event = self.events[i]
            previous_point = (previous_event.x, previous_event.y)
            next_event = self.events[i + 2]
            next_point = (next_event.x, next_event.y)
            current_point = (e.x, e.y)

            distance_to_previous = get_distance_between_points(current_point, previous_point)
            distance_to_next = get_distance_between_points(current_point, next_point)

            time_gap_to_previous = e.time - previous_event.time
            time_gap_to_next = next_event.time - e.time

            if time_gap_to_previous > 3 * time_gap_to_next:
                e.dodgy_data = True
            elif max(distance_to_next, distance_to_previous) > 0.1:
                if distance_to_next > 2 * distance_to_previous or distance_to_previous > 2 * distance_to_next:
                    e.dodgy_data = True

    def set_track_speed_on_events(self):
        previous = [self.events[0]] * 6   # 6 here matches DRF, but (TODO) DRF is marginally more accurate algorithm
        improve_previous = False
        for e in self.events:
            if e.dodgy_data or previous[0].dodgy_data:
                e.track_speed = previous[-1].track_speed
                improve_previous = True
            else:
                distance = get_distance_between_points((e.x, e.y), (previous[0].x, previous[0].y))
                time_taken = e.time - previous[0].time
                if time_taken > 0:
                    e.track_speed = distance / time_taken
                    if e.track_speed > self.peak_track_speed:
                        self.peak_track_speed = e.track_speed
                    if improve_previous:
                        previous[-1].track_speed = (e.track_speed + previous[-1].track_speed) / 2
                improve_previous = False

            previous = previous[1:] + [e]

    def set_progress_speed_on_events(self):
        previous = [self.events[0]] * 5   # 5 here excludes current step so matches DRF of 6 including current step
        improve_previous = False
        for e in self.events:
            if e.dodgy_data or previous[0].dodgy_data:
                e.progress_speed = previous[-1].progress_speed
                improve_previous = True
            else:
                progress_gain = e.progress - previous[0].progress
                time_taken = e.time - previous[0].time

                if time_taken > 0:
                    e.progress_speed = progress_gain / 100 * e.track_length / time_taken
                    if e.progress_speed > self.peak_progress_speed:
                        self.peak_progress_speed = e.progress_speed
                    if improve_previous:
                        previous[-1].progress_speed = (e.progress_speed + previous[-1].progress_speed) / 2
                improve_previous = False

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

    def _set_side_and_distance_from_center_on_events(self, track: Track):
        for e in self.events:
            current_location = (e.x, e.y)
            e.track_side = track.get_position_of_point_relative_to_waypoint(current_location, e.closest_waypoint_index)
            closest_waypoint = track.get_waypoint(e.closest_waypoint_index)
            next_waypoint = track.get_next_different_waypoint(e.closest_waypoint_index)
            previous_waypoint = track.get_previous_different_waypoint(e.closest_waypoint_index)
            distance_of_next_waypoint = get_distance_between_points(current_location, next_waypoint)
            distance_of_previous_waypoint = get_distance_between_points(current_location, previous_waypoint)
            if distance_of_next_waypoint < distance_of_previous_waypoint:
                e.distance_from_center = get_distance_of_point_from_line(current_location, closest_waypoint, next_waypoint)
            else:
                e.distance_from_center = get_distance_of_point_from_line(current_location, closest_waypoint, previous_waypoint)

    def _set_before_and_after_waypoints_on_events(self, track: Track):
        e: Event
        for e in self.events:
            (e.before_waypoint_index, e.after_waypoint_index) = track.get_waypoint_ids_before_and_after((e.x, e.y),
                                                                                                        e.closest_waypoint_index)

    def _set_skew_on_events(self, track: Track):
        e: Event
        for e in self.events:
            (track_bearing, _) = track.get_bearing_and_distance_to_next_waypoint(e.before_waypoint_index)
            e.skew = get_turn_between_directions(track_bearing, e.true_bearing)

    def set_acceleration_and_braking_on_events(self):
        previous_time = -1
        max_event_id = len(self.events) - 1
        for i, e in enumerate(self.events):
            if e.time_elapsed != previous_time:
                earlier_event = self.events[max(0, i - 2)]
                later_event = self.events[min(max_event_id, i + 2)]
                time_difference = later_event.time_elapsed - earlier_event.time_elapsed
                if e.speed < 1.05 * e.track_speed and earlier_event.track_speed > later_event.track_speed:
                    e.braking = (earlier_event.track_speed - later_event.track_speed) / time_difference
                elif e.speed > 0.95 * e.track_speed and earlier_event.track_speed < later_event.track_speed:
                    e.acceleration = (later_event.track_speed - earlier_event.track_speed) / time_difference
            previous_time = e.time_elapsed

    def get_blocked_waypoints(self, track: Track):
        left_wps = []
        right_wps = []
        left_locations = []
        right_locations = []

        for obj in self.object_locations:
            wp = track.get_closest_waypoint_id(obj)
            pos = track.get_position_of_point_relative_to_waypoint(obj, wp)
            if pos == "L":
                left_wps.append(wp)
                left_locations.append(obj)
            else:
                right_wps.append(wp)
                right_locations.append(obj)
        return left_wps, right_wps, left_locations, right_locations

    def set_projected_distances_on_events(self, track: Track):
        e: Event
        for e in self.events:
            e.projected_travel_distance = track.get_projected_distance_on_track((e.x, e.y), e.true_bearing,
                                                                                e.closest_waypoint_index, 0.0,
                                                                                self._blocked_left_waypoints,
                                                                                self._blocked_right_waypoints,
                                                                                self._blocked_left_object_locations,
                                                                                self._blocked_right_object_locations)
        if self.outcome in [OFF_TRACK, CRASHED]:
            self.events[-1].projected_travel_distance = 0.0

    def set_reward_total_on_events(self):
        reward_total = 0.0
        for e in self.events:
            reward_total += e.reward
            e.reward_total = reward_total
            e.average_reward_so_far = reward_total / e.step

    def set_time_elapsed_on_events(self):
        start_time = self.events[0].time
        for e in self.events:
            e.time_elapsed = e.time - start_time + TIME_BEFORE_FIRST_STEP

    def set_total_distance_travelled_on_events(self):
        distance = 0.0
        previous = self.events[0]

        for e in self.events:
            x_diff = e.x - previous.x
            y_diff = e.y - previous.y
            distance += math.sqrt(x_diff * x_diff + y_diff * y_diff)
            e.total_distance_travelled = distance
            previous = e

    def set_sequence_length_on_events(self):
        sequence = 0
        previous_action_id = -1

        for e in self.events:
            if e.action_taken is None:
                sequence = 1
            elif e.action_taken == previous_action_id:
                sequence += 1
            else:
                sequence = 1
                previous_action_id = e.action_taken
            e.sequence_count = sequence

    def _set_discounted_future_rewards(self, calculate_alternate_discount_factors: bool):
        for i in range(len(self.events)):
            self.events[i].discounted_future_rewards = discount_factors.get_discounted_future_rewards(
                self.rewards[i:], calculate_alternate_discount_factors, True)

    def _set_new_discounted_future_reward(self):
        for i in range(len(self.events)):
            self.events[i].new_discounted_future_reward = discount_factors.get_discounted_future_rewards(
                self.new_rewards[i:], False, False)

    def get_list_of_rewards(self):
        list_of_rewards = []
        for e in self.events:
            list_of_rewards.append(e.reward)
        return list_of_rewards

    def _get_list_of_new_rewards(self):
        list_of_new_rewards = []
        for e in self.events:
            list_of_new_rewards.append(e.new_reward)
        return list_of_new_rewards

    # List of lists since there is a list of rewards per discount factor (0 = the current DF)
    def _get_lists_of_discounted_future_rewards(self):
        all_lists = []
        for i in range(len(self.events[0].discounted_future_rewards)):
            list_of_rewards = []
            for e in self.events:
                list_of_rewards.append(e.discounted_future_rewards[i])
            all_lists.append(list_of_rewards)
        return all_lists

    # Single list since for NEW future rewards we only do the current DF for efficiency
    def _get_list_of_new_discounted_future_rewards(self):
        list_of_rewards = []
        for e in self.events:
            list_of_rewards.append(e.new_discounted_future_reward)
        return list_of_rewards

    def _get_action_frequency(self, action_space: ActionSpace):
        action_frequency = action_space.get_new_frequency_counter()
        for e in self.events:
            action_frequency[e.action_taken] += 1
        return action_frequency

    def _set_new_rewards(self, track: Track):
        if NEW_REWARD_FUNCTION:
            total = 0.0
            for e in self.events:
                e.new_reward = NEW_REWARD_FUNCTION(e.get_reward_input_params(track))
                total += e.new_reward
                e.new_reward_total = total

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

    def apply_visits_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                      action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range, self._get_event_visitor_dummy)

    def apply_track_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                      action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range, self._get_event_track_speed)

    def apply_action_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                       action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_action_speed)

    def apply_progress_speed_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                         action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_progress_speed)

    def apply_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                 action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_reward)

    def apply_new_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                 action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_new_event_reward)

    def apply_discounted_future_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                 action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_future_discounted_reward)

    def apply_alternate_discounted_future_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                 action_space_filter: ActionSpaceFilter, waypoint_range, discount_factor_index):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_alternate_future_discounted_reward, discount_factor_index)

    def apply_new_discounted_future_reward_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                 action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_new_future_discounted_reward)

    def apply_slide_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_slide)

    def apply_skew_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                               action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_skew)

    def apply_smoothness_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                   action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_smoothness)

    def apply_acceleration_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                   action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_acceleration)

    def apply_braking_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end,
                                   action_space_filter: ActionSpaceFilter, waypoint_range):
        self._apply_episode_to_heat_map(heat_map, skip_start, skip_end, action_space_filter, waypoint_range,
                                        self._get_event_braking)

    @staticmethod
    def _get_event_track_speed(event: Event):
        return event.track_speed

    @staticmethod
    def _get_event_action_speed(event: Event):
        return event.speed

    @staticmethod
    def _get_event_progress_speed(event: Event):
        return max(0, event.progress_speed)

    @staticmethod
    def _get_event_reward(event: Event):
        return max(0, event.reward)

    @staticmethod
    def _get_new_event_reward(event: Event):
        return max(0, event.new_reward)

    @staticmethod
    def _get_event_future_discounted_reward(event: Event):
        return max(0, event.discounted_future_rewards[0])

    @staticmethod
    def _get_event_alternate_future_discounted_reward(event: Event, discount_factor_index: int):
        return max(0, event.discounted_future_rewards[discount_factor_index])

    @staticmethod
    def _get_event_new_future_discounted_reward(event: Event):
        return max(0, event.new_discounted_future_reward)

    @staticmethod
    def _get_event_slide(event: Event):
        return abs(event.slide)

    @staticmethod
    def _get_event_skew(event: Event):
        return abs(event.skew)

    @staticmethod
    def _get_event_steering(event: Event):
        return max(0, 30 - abs(event.steering_angle))

    @staticmethod
    def _get_event_smoothness(event: Event):
        return event.sequence_count - 1

    @staticmethod
    def _get_event_acceleration(event: Event):
        return event.acceleration

    @staticmethod
    def _get_event_braking(event: Event):
        return event.braking

    @staticmethod
    def _get_event_visitor_dummy(event: Event):
        return 1

    def apply_event_stat_to_heat_map(self, stat_extractor: callable, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter, waypoint_range):
        assert min(skip_start, skip_end) >= 0
        previous = self.events[0]
        if self.lap_complete:
            skip_end = self.events[-1].step
        else:
            skip_end = self.events[-1].step - skip_end
        for e in self.events:
            e: Event
            stat = stat_extractor(e)
            if skip_start <= e.step <= skip_end and e.is_within_waypoint_range(waypoint_range) and (
                    not action_space_filter or action_space_filter.should_show_action(e.action_taken)):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, stat)
            previous = e

    # This is now the OLD way to do this
    def _apply_episode_to_heat_map(self, heat_map: HeatMap, skip_start, skip_end, action_space_filter: ActionSpaceFilter, waypoint_range, stat_extractor: callable, optional_parameter=None):
        assert min(skip_start, skip_end) >= 0
        previous = self.events[0]
        if self.lap_complete:
            skip_end = self.events[-1].step
        else:
            skip_end = self.events[-1].step - skip_end
        for e in self.events:
            e: Event
            if optional_parameter is None:
                stat = stat_extractor(e)
            else:
                stat = stat_extractor(e, optional_parameter)
            if skip_start <= e.step <= skip_end and e.is_within_waypoint_range(waypoint_range) and (
                    not action_space_filter or action_space_filter.should_show_action(e.action_taken)):
                self._apply_event_stat_to_heat_map(e, previous, heat_map, stat)
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

    def get_events_in_range(self, start_event: Event, finish_event: Event):
        assert start_event.step <= finish_event.step
        return self.events[start_event.step - 1:finish_event.step]

    def does_debug_contain(self, search_string):
        for e in self.events:
            if search_string in e.debug_log:
                return True

        return False

    def get_latest_event_index_on_or_before(self, required_time):
        if required_time <= 0.0:
            return 0
        elif required_time >= self.events[-1].time_elapsed:
            return len(self.events) - 1
        else:
            events_per_second = len(self.events) / self.events[-1].time_elapsed
            index = int(events_per_second * required_time)

            while self.events[index].time_elapsed < required_time:
                index += 1

            while index > 0 and self.events[index].time_elapsed > required_time:
                index -= 1

            return index

    def count_objects_in_section(self, start_wp: int, end_wp: int):
        left = 0
        for w in self._blocked_left_waypoints:
            if start_wp <= end_wp and start_wp <= w <= end_wp:
                left += 1
            elif start_wp > end_wp and (w >= start_wp or w <= end_wp):
                left += 1
        right = 0
        for w in self._blocked_right_waypoints:
            if start_wp <= end_wp and start_wp <= w <= end_wp:
                right += 1
            elif start_wp > end_wp and (w >= start_wp or w <= end_wp):
                right += 1

        return left, right

    def extract_all_sequences(self, min_sequence_length: int):
        sequences = Sequences()
        for i, e in enumerate(self.events):
            if e.sequence_count == 1 and i >= min_sequence_length:
                previous_event: Event = self.events[i-1]
                if previous_event.steering_angle != 0 and previous_event.sequence_count >= min_sequence_length:
                    new_sequence = Sequence()
                    new_sequence.set_from_events(self.events[i - previous_event.sequence_count:i])
                    sequences.add(new_sequence)
        return sequences


def are_close_waypoint_ids(id1, id2, track :Track):
    if abs(id1 - id2) <= 2:
        return True

    if max(id1, id2) >= track.get_number_of_waypoints() - 1 and min(id1, id2) <= 2:
        return True
    else:
        return False


def extract_all_sequences(episodes: list[Episode], min_sequence_length: int):
    result = Sequences()
    if episodes is not None:
        for e in episodes:
            result.add_sequences(e.extract_all_sequences(min_sequence_length))
    return result


