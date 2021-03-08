import tkinter as tk
import numpy as np


import src.secret_sauce.glue.glue as ss
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.event.event_meta import Event
from src.graphics.track_graphics import TrackGraphics
from src.ui.log_event_info_window import LogEventInfoWindow
from src.analyze.selector.episode_selector import EpisodeSelector
from src.action_space.action_util import get_min_and_max_action_speeds

from src.analyze.core.controls import EpisodeRouteColourSchemeControl



BLOB_SIZE_SMALL = "Small"
BLOB_SIZE_MEDIUM = "Medium"
BLOB_SIZE_LARGE = "Large"


class AnalyzeRoute(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._colour_scheme_control = EpisodeRouteColourSchemeControl(guru_parent_redraw, control_frame)

        self.episode_selector = episode_selector

        self.chosen_event = None

        self.smoothness_alternate = False
        self.smoothness_current = False

        self.floating_window = None

        self.blob_size = tk.StringVar()
        self.blob_size.set(BLOB_SIZE_MEDIUM)

        self.show_heading = False
        self.show_true_bearing = False


    def build_control_frame(self, control_frame):

        self._colour_scheme_control.add_to_control_frame()

        ####

        format_group = tk.LabelFrame(control_frame, text="Format", padx=5, pady=5)
        format_group.pack()

        tk.Label(format_group, text="Blob size").grid(column=0, row=0, pady=2, padx=5, sticky=tk.W)
        tk.OptionMenu(format_group, self.blob_size, BLOB_SIZE_SMALL, BLOB_SIZE_MEDIUM, BLOB_SIZE_LARGE,
                      command=self.redraw_new_blob_size).grid(column=0, row=1, pady=2, padx=5, sticky=tk.W)

        #######

        episode_selector_frame = self.episode_selector.get_label_frame(control_frame, self.callback_selected_episode_changed)
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
        if self.blob_size.get() == BLOB_SIZE_SMALL:
            return 0
        elif self.blob_size.get() == BLOB_SIZE_MEDIUM:
            return 1
        elif self.blob_size.get() == BLOB_SIZE_LARGE:
            return 2

    def redraw_new_blob_size(self, new_value):
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

            # TODO - need to do a lot more work here to make better auto choices
            self.reward_percentiles = np.percentile(all_rewards, [10, 37, 64, 90])

            if (self.reward_percentiles[0] == self.reward_percentiles[2]):
                self.reward_percentiles = np.percentile(all_rewards, [64, 73, 82, 91])
            elif (self.reward_percentiles[0] == self.reward_percentiles[1]):
                self.reward_percentiles = np.percentile(all_rewards, [37, 55, 73, 90])
        else:
            self.reward_percentiles = None

    def callback_selected_episode_changed(self):
        self.chosen_event = None
        self.guru_parent_redraw()

    def draw_episode(self, episode):

        for obj in episode.object_locations:
            (x, y) = obj
            size = 0.4
            self.track_graphics.plot_box(x - size/2, y - size/2, x + size/2, y + size/2, "red")

        if self._colour_scheme_control.scheme_reward():
            plot_event_method = self.colour_scheme_reward
        elif self._colour_scheme_control.scheme_action_speed():
            plot_event_method = self.colour_scheme_action_speed
        elif self._colour_scheme_control.scheme_track_speed():
            plot_event_method = self.colour_scheme_track_speed
        elif self._colour_scheme_control.scheme_progress_speed():
            plot_event_method = self.colour_scheme_progress_speed
        elif self._colour_scheme_control.scheme_smoothness():
            plot_event_method = self.colour_scheme_smoothness
        elif self._colour_scheme_control.scheme_steering():
            plot_event_method = self.colour_scheme_steering
        elif self._colour_scheme_control.scheme_slide():
            plot_event_method = self.colour_scheme_slide
        elif self._colour_scheme_control.scheme_per_second():
            plot_event_method = self.colour_scheme_per_second
        elif self._colour_scheme_control.scheme_none():
            plot_event_method = self.colour_scheme_none
        else:
            print("OOOPS - unknown colour scheme!")
            return

        (min_speed, max_speed) = get_min_and_max_action_speeds(self.action_space)
        speed_range = max_speed - min_speed

        previous_event = episode.events[0]
        for e in episode.events[1:]:
            if self.action_space_filter.should_show_action(e.action_taken):
                plot_event_method(e, previous_event, max_speed, speed_range)
                previous_event = e

    def colour_scheme_reward(self, event, previous_event, max_speed, speed_range):
        if event.reward >= self.reward_percentiles[3]:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.reward >= self.reward_percentiles[2]:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "blue")
        elif event.reward >= self.reward_percentiles[1]:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.reward >= self.reward_percentiles[0]:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_track_speed(self, event, previous_event, max_speed, speed_range):
        if event.track_speed >= max_speed - 0.2 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.track_speed >= max_speed - 0.4 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "blue")
        elif event.track_speed >= max_speed - 0.6 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.track_speed >= max_speed - 0.8 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 2, "yellow")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_action_speed(self, event, previous_event, max_speed, speed_range):
        if event.speed >= max_speed - 0.33 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "green")
        elif event.speed >= max_speed - 0.66 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 2, "yellow")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_progress_speed(self, event, previous_event, max_speed, speed_range):
        if event.progress_speed >= max_speed - 0.2 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.progress_speed >= max_speed - 0.4 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "blue")
        elif event.progress_speed >= max_speed - 0.6 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.progress_speed >= max_speed - 0.8 * speed_range:
            self.track_graphics.plot_dot((event.x, event.y), 2, "yellow")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_smoothness(self, event, previous_event, max_speed, speed_range):
        if event.action_taken == previous_event.action_taken:
            if self.smoothness_alternate:
                colour = "green"
            else:
                colour = "purple"

            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), colour)
            self.track_graphics.plot_dot((previous_event.x, previous_event.y), 3 + self.get_increased_blob_size(), colour)
            self.smoothness_current = True
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")
            if self.smoothness_current:
                self.smoothness_current = False
                self.smoothness_alternate = not self.smoothness_alternate

    def colour_scheme_steering(self, event, previous_event, max_speed, speed_range):
        if abs(event.steering_angle) < 0.1:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "green")
        elif abs(event.steering_angle) < 10.1:
            self.track_graphics.plot_dot((event.x, event.y), 1, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_slide(self, event: Event, previous_event, max_speed, speed_range):
        if abs(event.slide) > 20:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "red")
        elif abs(event.slide) > 10:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 2, "green")

    def colour_scheme_none(self, event, previous_event, max_speed, speed_range):
        self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")

    def colour_scheme_per_second(self, event, previous_event, max_speed, speed_range):
        if int(event.time_elapsed) % 2 == 0:
            colour = "green"
        else:
            colour = "purple"

        self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), colour)

    def set_show_heading(self, setting :bool):
        self.show_heading = setting
        self.draw_chosen_event_()

    def set_show_true_bearing(self, setting :bool):
        self.show_true_bearing = setting
        self.draw_chosen_event_()

