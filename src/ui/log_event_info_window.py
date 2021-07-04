#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk

from src.configuration.config_manager import ConfigManager
from src.event.event_meta import Event
from src.tracks.track import Track
from src.ui.debug_text_formatter import get_formatted_debug

from src.utils.formatting import get_pretty_small_float, get_pretty_large_float, get_pretty_large_integer
import src.utils.geometry as geometry
from src.utils.discount_factors import discount_factors


class LogEventInfoWindow(tk.Toplevel):

    def __init__(self, parent, config_manager: ConfigManager):

        tk.Toplevel.__init__(self)

        self.title("Detailed Event Info")

        self._config_manager = config_manager

        event_reward_frame = tk.LabelFrame(self, text="Event Reward")
        new_event_reward_frame = tk.LabelFrame(self, text="Alternate Reward")
        discount_factors_frame = tk.LabelFrame(self, text="Other Discount Factors")
        waypoint_frame = tk.LabelFrame(self, text="Closest Waypoint")
        state_frame = tk.LabelFrame(self, text="State")
        action_frame = tk.LabelFrame(self, text="Chosen Action")
        debug_frame = tk.LabelFrame(self, text="Log File Debug")

        stickiness = tk.NW+tk.E
        event_reward_frame.grid(row=0, column=0, pady=5, padx=5, sticky=stickiness)
        if self._config_manager.get_calculate_new_reward():
            new_event_reward_frame.grid(row=1, column=0, pady=5, padx=5, sticky=stickiness)
        if self._config_manager.get_calculate_alternate_discount_factors():
            discount_factors_frame.grid(row=2, column=0, pady=5, padx=5, sticky=stickiness)
        state_frame.grid(row=0, column=1, rowspan=3, pady=5, padx=5, sticky=stickiness)
        waypoint_frame.grid(row=0, column=2, rowspan=2, pady=5, padx=5, sticky=stickiness)
        action_frame.grid(row=2, column=2, pady=5, padx=5, sticky=stickiness)
        debug_frame.grid(row=3, column=0, columnspan=4, pady=5, padx=5, sticky=stickiness)

        # The debug frame stretches into column 3 so we tell it to absorb stretch instead of messing up data cols 0-2
        self.columnconfigure(3, weight=1)

        self.waypoint_lap_position = tk.StringVar()
        self.waypoint_previous_id = tk.StringVar()
        self.waypoint_closest_id = tk.StringVar()
        self.waypoint_next_id = tk.StringVar()
        self.waypoint_previous_bearing = tk.StringVar()
        self.waypoint_current_bearing = tk.StringVar()
        self.waypoint_next_bearing = tk.StringVar()

        self.make_label_and_value(waypoint_frame, 0, "Lap Position", self.waypoint_lap_position)
        self.make_label_and_value(waypoint_frame, 1, "Previous Waypoint Id", self.waypoint_previous_id)
        self.make_label_and_value(waypoint_frame, 2, "Closest Waypoint Id", self.waypoint_closest_id)
        self.make_label_and_value(waypoint_frame, 3, "Next Waypoint Id", self.waypoint_next_id)
        self.make_label_and_value(waypoint_frame, 4, "Previous Track Bearing", self.waypoint_previous_bearing)
        self.make_label_and_value(waypoint_frame, 5, "Closest Track Bearing", self.waypoint_current_bearing)
        self.make_label_and_value(waypoint_frame, 6, "Next Track Bearing", self.waypoint_next_bearing)

        self.state_progress = tk.StringVar()
        self.state_time = tk.StringVar()
        self.state_step = tk.StringVar()
        self.state_track_speed = tk.StringVar()
        self.state_progress_speed = tk.StringVar()
        self.state_heading = tk.StringVar()
        self.state_true_bearing = tk.StringVar()
        self.state_slide = tk.StringVar()
        self.state_skew = tk.StringVar()
        self.state_side = tk.StringVar()
        self.state_distance_from_centre = tk.StringVar()
        self.state_all_wheels_on_track = tk.StringVar()
        self.state_acceleration = tk.StringVar()
        self.state_braking = tk.StringVar()
        self.state_projected_travel_distance = tk.StringVar()

        self.make_label_and_value(state_frame, 0, "Progress", self.state_progress)
        self.make_label_and_value(state_frame, 1, "Time", self.state_time)
        self.make_label_and_value(state_frame, 2, "Step", self.state_step)
        self.make_label_and_value(state_frame, 3, "Track Speed", self.state_track_speed)
        self.make_label_and_value(state_frame, 4, "Progress Speed", self.state_progress_speed)
        self.make_label_and_value(state_frame, 5, "Heading", self.state_heading)
        self.make_label_and_value(state_frame, 6, "True Bearing", self.state_true_bearing)
        self.make_label_and_value(state_frame, 7, "Slide", self.state_slide)
        self.make_label_and_value(state_frame, 8, "Skew", self.state_skew)
        self.make_label_and_value(state_frame, 9, "Side", self.state_side)
        self.make_label_and_value(state_frame, 10, "Distance from Centre", self.state_distance_from_centre)
        self.make_label_and_value(state_frame, 11, "All Wheels on Track", self.state_all_wheels_on_track)
        self.make_label_and_value(state_frame, 12, "Acceleration", self.state_acceleration)
        self.make_label_and_value(state_frame, 13, "Braking", self.state_braking)
        self.make_label_and_value(state_frame, 14, "Projected Travel", self.state_projected_travel_distance)

        self.action_id = tk.StringVar()
        self.action_steering = tk.StringVar()
        self.action_speed = tk.StringVar()
        self.action_sequence = tk.StringVar()

        self.make_label_and_value(action_frame, 0, "Action", self.action_id)
        self.make_label_and_value(action_frame, 1, "Steering", self.action_steering)
        self.make_label_and_value(action_frame, 2, "Speed", self.action_speed)
        self.make_label_and_value(action_frame, 3, "Sequence", self.action_sequence)

        self.reward_value = tk.StringVar()
        self.reward_average = tk.StringVar()
        self.reward_total = tk.StringVar()
        self.discounted_future_reward = tk.StringVar()

        df_title = self._make_long_discount_factor_title(0)

        self.make_label_and_value(event_reward_frame, 0, "Reward", self.reward_value)
        self.make_label_and_value(event_reward_frame, 1, "Average so far", self.reward_average)
        self.make_label_and_value(event_reward_frame, 2, "Total so far", self.reward_total)
        self.make_label_and_value(event_reward_frame, 3, df_title, self.discounted_future_reward)

        self.new_reward = tk.StringVar()
        self.new_discounted_future_reward = tk.StringVar()
        if self._config_manager.get_calculate_new_reward():
            self.make_label_and_value(new_event_reward_frame, 0, "Reward", self.new_reward)
            self.make_label_and_value(new_event_reward_frame, 1, df_title, self.new_discounted_future_reward)

        self.other_discounted_future_rewards = []
        if self._config_manager.get_calculate_alternate_discount_factors():
            for i in range(discount_factors.get_number_of_discount_factors() - 1):
                new_tk_var = tk.StringVar()
                self.other_discounted_future_rewards.append(new_tk_var)
                df_title = self._make_short_discount_factor_title(i + 1)
                self.make_label_and_value(discount_factors_frame, i, df_title, new_tk_var)

        self.debug_output = tk.StringVar()

        tk.Label(debug_frame, textvariable=self.debug_output, justify=tk.LEFT, font='TkFixedFont').grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        self.geometry("+%d+%d" % (parent.winfo_rootx(), parent.winfo_rooty()))

    @staticmethod
    def make_label_and_value(parent_frame, row, label, tk_variable):
        if ":" not in label:
            label += ":"
        tk.Label(parent_frame, text=label, anchor=tk.E, justify=tk.RIGHT).grid(row=row, column=0, pady=5, padx=5, sticky=tk.E)
        tk.Label(parent_frame, textvariable=tk_variable).grid(row=row, column=1, pady=5, padx=5, sticky=tk.W)

    def show_event(self, event: Event, track: Track):
        (previous_bearing, _) = track.get_bearing_and_distance_from_previous_waypoint(event.before_waypoint_index)
        (current_bearing, _) = track.get_bearing_and_distance_to_next_waypoint(event.before_waypoint_index)
        (next_bearing, _) = track.get_bearing_and_distance_to_next_waypoint(event.after_waypoint_index)

        self.waypoint_lap_position.set(str(round(track.get_waypoint_percent_from_race_start(event.closest_waypoint_index), 1)) + "  %")
        self.waypoint_previous_id.set(str(event.before_waypoint_index))
        self.waypoint_closest_id.set(str(event.closest_waypoint_index))
        self.waypoint_next_id.set(str(event.after_waypoint_index))

        self.waypoint_previous_bearing.set(str(round(previous_bearing)))
        self.waypoint_current_bearing.set(str(round(current_bearing)))
        self.waypoint_next_bearing.set(str(round(next_bearing)))

        self.state_progress.set(str(round(event.progress, 1)) + "  %")
        self.state_time.set(str(round(event.time_elapsed, 1)) + "  secs")
        self.state_step.set(str(event.step))
        self.state_track_speed.set(str(round(event.track_speed, 1)) + "  m/s")
        self.state_progress_speed.set(str(round(event.progress_speed, 1)) + "  m/s")
        self.state_heading.set(str(round(event.heading)))
        self.state_true_bearing.set(str(round(event.true_bearing)))
        self.state_slide.set(str(round(event.slide)))
        self.state_skew.set(str(round(event.skew)))
        self.state_side.set(event.track_side)
        self.state_distance_from_centre.set(str(round(event.distance_from_center, 2)))
        self.state_all_wheels_on_track.set(str(event.all_wheels_on_track))
        if event.acceleration > 0.0:
            self.state_acceleration.set(str(round(event.acceleration, 1)) + "  m/s/s")
        else:
            self.state_acceleration.set("---")
        if event.braking > 0.0:
            self.state_braking.set(str(round(event.braking, 1)) + "  m/s/s")
        else:
            self.state_braking.set("---")
        self.state_projected_travel_distance.set(str(round(event.projected_travel_distance, 1)) + " m")

        if event.action_taken is None:
            self.action_id.set("n/a")
        else:
            self.action_id.set(str(event.action_taken))
        self.action_steering.set(get_formatted_steering(event.steering_angle))
        self.action_speed.set(str(event.speed) + "  m/s")
        self.action_sequence.set(str(event.sequence_count))

        self.reward_value.set(get_pretty_large_float(round(event.reward, 5)))
        self.reward_average.set(get_pretty_large_integer(event.average_reward_so_far))
        self.reward_total.set(get_pretty_large_integer(event.reward_total))
        self.discounted_future_reward.set(get_pretty_large_integer(event.discounted_future_rewards[0]))
        if self._config_manager.get_calculate_new_reward():
            self.new_reward.set(get_pretty_large_float(round(event.new_reward, 5)))
            self.new_discounted_future_reward.set(get_pretty_large_integer(event.new_discounted_future_reward))

        if self._config_manager.get_calculate_alternate_discount_factors():
            for i, r in enumerate(self.other_discounted_future_rewards):
                r.set(get_pretty_large_integer(event.discounted_future_rewards[i + 1]))

        self.debug_output.set(get_formatted_debug(event.debug_log, 10, 80, []))  # TODO - expose configuration
        self.lift()

    def _make_long_discount_factor_title(self, factor_id):
        return "Future:\n" + self._make_short_discount_factor_title(factor_id)

    @staticmethod
    def _make_short_discount_factor_title(factor_id):
        factor = discount_factors.get_discount_factor(factor_id)
        return "( DF = " + str(factor) + " )"


def get_formatted_steering(steering_angle):
    if geometry.is_right_bearing(steering_angle):
        return "RIGHT " + get_pretty_small_float(abs(steering_angle), 30, 1)
    elif geometry.is_left_bearing(steering_angle):
        return "LEFT " + get_pretty_small_float(abs(steering_angle), 30, 1)
    else:
        return "AHEAD"
