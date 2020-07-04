import math

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

        self.lap_complete = last_event.status == "lap_complete"
        self.step_count = len(events)
        self.percent_complete = last_event.progress
        self.is_real_start = first_event.closest_waypoint_index <= 1

        self.distance_travelled = self.get_distance_travelled()
        self.time_taken = last_event.time - first_event.time
        self.lap_time = 100 / last_event.progress * self.time_taken
        self.total_reward = self.get_total_reward()
        self.average_reward = self.total_reward / self.step_count

        self.action_frequency = self.get_action_frequency()

        self.peak_track_speed = 0
        self.set_track_speed_on_events()

    def get_distance_travelled(self):

        distance = 0.0
        previous = self.events[0]
        for e in self.events:
            x_diff = e.x - previous.x
            y_diff = e.y - previous.y
            distance += math.sqrt(x_diff * x_diff + y_diff * y_diff)
            previous = e

        return distance

    def set_track_speed_on_events(self):
        previous = self.events[0]
        for e in self.events:
            x_diff = e.x - previous.x
            y_diff = e.y - previous.y
            distance = math.sqrt(x_diff * x_diff + y_diff * y_diff)
            time_taken = e.time - previous.time

            if (time_taken) > 0:
                e.track_speed = distance / time_taken

                if e.track_speed > self.peak_track_speed:
                    self.peak_track_speed = e.track_speed

            previous = e

    def get_total_reward(self):
        total_reward = 0
        for e in self.events:
            total_reward += e.reward
        return total_reward

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
        previous = self.events[0]
        for e in self.events:

            if e.step >= skip_count and action_space_filter.should_show_action(e.action_taken):

                visitor_map.visit(e.x, e.y, self)

                x_diff = e.x - previous.x
                y_diff = e.y - previous.y

                visitor_map.visit(e.x - 0.25 * x_diff, e.y - 0.25 * y_diff, self)
                visitor_map.visit(e.x - 0.50 * x_diff, e.y - 0.50 * y_diff, self)
                visitor_map.visit(e.x - 0.75 * x_diff, e.y - 0.75 * y_diff, self)

            previous = e