import math
import numpy as np

from src.action_space.action import MAX_POSSIBLE_ACTIONS
from src.action_space.action_space_filter import ActionSpaceFilter
from src.analyze.util.visitor import VisitorMap




class Episode:

    def __init__(self, id, iteration, events):

        self.events = events
        self.id = id
        self.iteration = iteration

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
        self.lap_time = 100 / last_event.progress * self.time_taken  # predicted

        self.rewards = self.get_list_of_rewards()
        self.total_reward = self.rewards.sum()
        self.average_reward = self.rewards.mean()
        self.lap_reward = 100 / last_event.progress * self.total_reward  # predicted

        self.action_frequency = self.get_action_frequency()
        self.repeated_action_percent = self.get_repeated_action_percent()

        self.peak_track_speed = 0
        self.set_track_speed_on_events()
        self.set_reward_total_on_events()
        self.set_time_elapsed_on_events()
        self.set_total_distance_travelled_on_events()

        # THESE MUST BE AT THE END SINCE THEY ARE CALCULATED FROM DATA SET FURTHER UP/ABOVE
        self.distance_travelled = self.get_distance_travelled()
        self.flying_start_speed = self.get_track_speed_after_seconds(1)



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

    def set_track_speed_on_events(self):
        previous = [self.events[0]] * 7
        for e in self.events:
            x_diff = e.x - previous[0].x
            y_diff = e.y - previous[0].y
            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
            time_taken = e.time - previous[0].time

            if time_taken > 0:
                e.track_speed = distance / time_taken

                if e.track_speed > self.peak_track_speed:
                    self.peak_track_speed = e.track_speed

            previous = previous[1:] + [e]

    def set_reward_total_on_events(self):
        reward_total = 0.0
        for e in self.events:
            reward_total += e.reward
            e.reward_total = reward_total

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


    def get_total_reward(self):
        total_reward = 0
        for e in self.events:
            total_reward += e.reward
        return total_reward

    def get_list_of_rewards(self):
        list_of_rewards = []
        for e in self.events:
            list_of_rewards.append(e.reward)
        return np.array(list_of_rewards)

    def get_action_frequency(self):
        action_frequency = [0] * MAX_POSSIBLE_ACTIONS
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

    def apply_to_visitor_map(self, visitor_map :VisitorMap, skip_count, action_space_filter :ActionSpaceFilter):
        self.apply_speed_to_visitor_map(visitor_map, skip_count, action_space_filter, is_any_speed)

    def apply_speed_to_visitor_map(self, visitor_map :VisitorMap, skip_count, action_space_filter :ActionSpaceFilter, is_correct_speed):
        previous = self.events[0]
        for e in self.events:

            if e.step >= skip_count and action_space_filter.should_show_action(e.action_taken) and is_correct_speed(e.speed):

                visitor_map.visit(e.x, e.y, self)

                x_diff = e.x - previous.x
                y_diff = e.y - previous.y

                visitor_map.visit(e.x - 0.25 * x_diff, e.y - 0.25 * y_diff, self)
                visitor_map.visit(e.x - 0.50 * x_diff, e.y - 0.50 * y_diff, self)
                visitor_map.visit(e.x - 0.75 * x_diff, e.y - 0.75 * y_diff, self)

            previous = e

def is_any_speed(speed):
    return True


