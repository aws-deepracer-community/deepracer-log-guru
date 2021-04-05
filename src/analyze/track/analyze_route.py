import tkinter as tk
import numpy as np


import src.secret_sauce.glue.glue as ss
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.event.event_meta import Event
from src.graphics.track_graphics import TrackGraphics
from src.ui.log_event_info_window import LogEventInfoWindow
from src.analyze.selector.episode_selector import EpisodeSelector

from src.analyze.core.controls import MeasurementControl, TrackAppearanceControl, MoreFiltersControl
from src.utils.colors import get_color_for_data, ColorPalette

_WORST_SLIDE = 20
_HIGHEST_STEERING = 30

class AnalyzeRoute(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._measurement_control = MeasurementControl(guru_parent_redraw, control_frame, True)
        self._appearance_control = TrackAppearanceControl(guru_parent_redraw, control_frame,
                                                          self.redraw_new_appearance, self.redraw_new_appearance,
                                                          None)
        self._more_filters_control = MoreFiltersControl(guru_parent_redraw, control_frame, True)

        self.episode_selector = episode_selector

        self.chosen_event = None

        self.floating_window = None

        self.show_heading = False
        self.show_true_bearing = False

        self.single_tone = ""   # Will be populated just in time
        self.dual_tone = ""
        self.color_palette = ColorPalette.MULTI_COLOR_A

        self.reward_percentiles = None
        self.new_reward_percentiles = None
        self.discounted_future_reward_percentiles = None

    def build_control_frame(self, control_frame):

        self._measurement_control.add_to_control_frame()
        self._appearance_control.add_to_control_frame()
        self._more_filters_control.add_to_control_frame()

        episode_selector_frame = self.episode_selector.get_label_frame(
            control_frame, self.callback_selected_episode_changed)
        episode_selector_frame.pack()

    def left_button_pressed(self, track_point):
        episode = self.episode_selector.get_selected_episode()

        if episode:
            (self.chosen_event, self.chosen_event_index) = episode.get_closest_event_to_point(track_point)
            self.draw_chosen_event_()
            self.display_info_about_chosen_event()

    def go_backwards(self, track_point):
        episode = self.episode_selector.get_selected_episode()

        if episode and self.chosen_event and self.chosen_event_index > 0:
                self.chosen_event_index -= 1
                self.chosen_event = episode.events[self.chosen_event_index]
                self.draw_chosen_event_()
                self.display_info_about_chosen_event()

    def go_forwards(self, track_point):
        episode = self.episode_selector.get_selected_episode()

        if episode and self.chosen_event and self.chosen_event_index < len(episode.events) - 1:
            self.chosen_event_index += 1
            self.chosen_event = episode.events[self.chosen_event_index]
            self.draw_chosen_event_()
            self.display_info_about_chosen_event()

    def redraw(self):

        if not self.filtered_episodes:
            return

        self.draw_episode(self.episode_selector.get_selected_episode())
        self.draw_chosen_event_()

    def get_increased_blob_size(self):
        if self._appearance_control.small_blob_size():
            return 0
        elif self._appearance_control.medium_blob_size():
            return 1
        elif self._appearance_control.large_blob_size():
            return 2

    def redraw_new_appearance(self, new_value):
        self.guru_parent_redraw()
        self.draw_chosen_event_()

    def draw_chosen_event_(self):
        self.track_graphics.remove_highlights()

        if self.chosen_event:
            if self.show_heading:
                self.track_graphics.plot_angle_line_highlight((self.chosen_event.x, self.chosen_event.y),
                                                    self.chosen_event.heading, 2, 2, "orange")
            if self.show_true_bearing:
                self.track_graphics.plot_angle_line_highlight((self.chosen_event.x, self.chosen_event.y),
                                                              self.chosen_event.true_bearing, 2, 2, "purple")
                self.track_graphics.plot_angle_line_highlight((self.chosen_event.x, self.chosen_event.y),
                                                              self.chosen_event.true_bearing + 180, 2, 2, "purple")
            if self.show_heading:
                self.track_graphics.plot_angle_line_highlight((self.chosen_event.x, self.chosen_event.y),
                                                    self.chosen_event.heading, 2, 2, "orange")

            self.track_graphics.plot_ring_highlight((self.chosen_event.x, self.chosen_event.y),
                                                    6 + self.get_increased_blob_size(), "orange", 2)

    def display_info_about_chosen_event(self):

        if not self.floating_window or self.floating_window.winfo_exists() == 0:
            self.floating_window = LogEventInfoWindow(self.track_graphics.canvas)

        self.floating_window.show_event(self.chosen_event, self.current_track)

        if ss.SHOW_SS:
            print("Secret Sauce:")
            print(ss.get_info_about_event(self.current_track, self.chosen_event))

    def warning_track_changed(self):
        self.chosen_event = None

    def warning_filtered_episodes_changed(self):
        self.chosen_event = None

    def warning_all_episodes_changed(self):
        if self.all_episodes and len(self.all_episodes) >= 1:
            all_rewards = self.all_episodes[0].rewards
            for e in self.all_episodes[1:]:
                all_rewards = np.append(all_rewards, e.rewards)
            self.reward_percentiles = np.percentile(all_rewards, np.arange(100))

            all_discounted_future_rewards = self.all_episodes[0].discounted_future_rewards
            for e in self.all_episodes[1:]:
                all_discounted_future_rewards = np.append(all_discounted_future_rewards, e.discounted_future_rewards)
            self.discounted_future_reward_percentiles = np.percentile(all_discounted_future_rewards, np.arange(100))

            all_new_rewards = self.all_episodes[0].new_rewards
            for e in self.all_episodes[1:]:
                all_new_rewards = np.append(all_new_rewards, e.new_rewards)
            self.new_reward_percentiles = np.percentile(all_new_rewards, np.arange(100))
        else:
            self.reward_percentiles = None

    def callback_selected_episode_changed(self):
        self.chosen_event = None
        if self.floating_window is not None:
            self.floating_window.destroy()
            self.floating_window = None
        self.guru_parent_redraw()

    def draw_episode(self, episode):

        for obj in episode.object_locations:
            (x, y) = obj
            size = 0.4
            self.track_graphics.plot_box(x - size/2, y - size/2, x + size/2, y + size/2, "red")

        if self._measurement_control.measure_event_reward():
            plot_event_method = self.colour_scheme_reward
        elif self._measurement_control.measure_new_event_reward():
            plot_event_method = self.colour_scheme_new_reward
        elif self._measurement_control.measure_discounted_future_reward():
            plot_event_method = self.colour_scheme_discounted_future_reward
        elif self._measurement_control.measure_action_speed():
            plot_event_method = self.colour_scheme_action_speed
        elif self._measurement_control.measure_track_speed():
            plot_event_method = self.colour_scheme_track_speed
        elif self._measurement_control.measure_progress_speed():
            plot_event_method = self.colour_scheme_progress_speed
        elif self._measurement_control.measure_smoothness():
            plot_event_method = self.colour_scheme_smoothness
        elif self._measurement_control.measure_steering_straight():
            plot_event_method = self.colour_scheme_steering
        elif self._measurement_control.measure_slide():
            plot_event_method = self.colour_scheme_slide
        elif self._measurement_control.measure_seconds():
            plot_event_method = self.colour_scheme_per_second
        elif self._measurement_control.measure_visits():
            plot_event_method = self.colour_scheme_none
        else:
            print("OOOPS - unknown colour scheme!")
            return

        max_speed = self.action_space.get_max_speed()
        speed_range = self.action_space.get_speed_range()

        self.color_palette = self._appearance_control.get_chosen_color_palette()
        self.single_tone = get_color_for_data(0.6, self.color_palette)
        self.dual_tone = get_color_for_data(1, self.color_palette)

        show_all_actions = not self._more_filters_control.filter_actions()
        for e in episode.events[1:]:
            if show_all_actions or self.action_space_filter.should_show_action(e.action_taken):
                plot_event_method(e, max_speed, speed_range)

    def colour_scheme_reward(self, event, max_speed, speed_range):
        percentile = np.searchsorted(self.reward_percentiles, event.reward)
        brightness = min(1, percentile / 100 * 0.9 + 0.1)
        self._plot_dot(event, brightness)

    def colour_scheme_new_reward(self, event, max_speed, speed_range):
        percentile = np.searchsorted(self.new_reward_percentiles, event.new_reward)
        brightness = min(1, percentile / 100 * 0.9 + 0.1)
        self._plot_dot(event, brightness)

    def colour_scheme_discounted_future_reward(self, event, max_speed, speed_range):
        percentile = np.searchsorted(self.discounted_future_reward_percentiles, event.discounted_future_rewards[0])
        brightness = min(1, percentile / 100 * 0.9 + 0.1)
        self._plot_dot(event, brightness)

    def _plot_speed_dot(self, event, speed, max_speed, speed_range):
        speed_range = max(0.5, speed_range)   # Single speed training not only divide 0 but no variation for track or progress
        gap_from_best = max_speed - speed
        brightness = max(0.1, min(1, 1 - 0.9 * gap_from_best / speed_range))
        self._plot_dot(event, brightness)

    def _plot_dot(self, event, brightness):
        colour = get_color_for_data(brightness, self.color_palette)
        self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), colour)

    def colour_scheme_track_speed(self, event, max_speed, speed_range):
        self._plot_speed_dot(event, event.track_speed, max_speed, speed_range)

    def colour_scheme_action_speed(self, event, max_speed, speed_range):
        self._plot_speed_dot(event, event.speed, max_speed, speed_range)

    def colour_scheme_progress_speed(self, event, max_speed, speed_range):
        self._plot_speed_dot(event, event.progress_speed, max_speed, speed_range)

    def colour_scheme_smoothness(self, event, max_speed, speed_range):
        if event.sequence_count == 1:
            brightness = 0.05
        elif event.sequence_count == 2:
            brightness = 0.15
        else:
            brightness = min(1.0, 0.3 + event.sequence_count / 15)
        self._plot_dot(event, brightness)

    def colour_scheme_steering(self, event, max_speed, speed_range):
        brightness = max(0.1, min(1, 1 - 0.9 * abs(event.steering_angle) / _HIGHEST_STEERING))
        self._plot_dot(event, brightness)

    def colour_scheme_slide(self, event: Event, max_speed, speed_range):
        brightness = max(0.1, min(1, 0.1 + 0.9 * abs(event.slide) / _WORST_SLIDE))
        self._plot_dot(event, brightness)

    def colour_scheme_none(self, event, max_speed, speed_range):
        self._plot_dot(event, 0.7)

    def colour_scheme_per_second(self, event, max_speed, speed_range):
        if int(event.time_elapsed) % 2 == 0:
            self._plot_dot(event, 0.7)
        else:
            self._plot_dot(event, 1.0)

    def set_show_heading(self, setting :bool):
        self.show_heading = setting
        self.draw_chosen_event_()

    def set_show_true_bearing(self, setting :bool):
        self.show_true_bearing = setting
        self.draw_chosen_event_()
