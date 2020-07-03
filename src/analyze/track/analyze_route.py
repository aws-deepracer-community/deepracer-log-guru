import tkinter as tk

import src.secret_sauce.glue.glue as ss
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics

COLOUR_SCHEME_REWARD_20 = 0
COLOUR_SCHEME_REWARD_100 = 1
COLOUR_SCHEME_TRACK_SPEED = 2
COLOUR_SCHEME_ACTION_SPEED = 3
COLOUR_SCHEME_SMOOTHNESS = 4
COLOUR_SCHEME_STRAIGHTNESS = 5
COLOUR_SCHEME_NONE = 6


class AnalyzeRoute(TrackAnalyzer):


    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self.chosen_route_index = 0

        self.chosen_event = None
        chosen_event_index = -1

        self.colour_scheme = tk.IntVar()

        self.smoothness_alternate = False
        self.smoothness_current = False

    def build_control_frame(self, control_frame):

        tk.Radiobutton(control_frame, text="Reward 20", variable=self.colour_scheme, value=COLOUR_SCHEME_REWARD_20,
                       command=self.guru_parent_redraw).grid(column=0, row=0, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="Reward 100", variable=self.colour_scheme, value=COLOUR_SCHEME_REWARD_100,
                       command=self.guru_parent_redraw).grid(column=0, row=1, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="Track Speed", variable=self.colour_scheme, value=COLOUR_SCHEME_TRACK_SPEED,
                       command=self.guru_parent_redraw).grid(column=0, row=2, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="Action Speed", variable=self.colour_scheme, value=COLOUR_SCHEME_ACTION_SPEED,
                       command=self.guru_parent_redraw).grid(column=0, row=3, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="Smoothness", variable=self.colour_scheme, value=COLOUR_SCHEME_SMOOTHNESS,
                       command=self.guru_parent_redraw).grid(column=0, row=4, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="Straightness", variable=self.colour_scheme, value=COLOUR_SCHEME_STRAIGHTNESS,
                       command=self.guru_parent_redraw).grid(column=0, row=5, pady=5, padx=5)
        tk.Radiobutton(control_frame, text="None", variable=self.colour_scheme, value=COLOUR_SCHEME_NONE,
                       command=self.guru_parent_redraw).grid(column=0, row=6, pady=5, padx=5)

        self.colour_scheme.set(COLOUR_SCHEME_NONE)

        next_button = tk.Button(control_frame, height=2, text="Next")
        next_button["command"] = self.button_press_next
        next_button.grid(column=0, row=7, pady=5, padx=5)

        previous_button = tk.Button(control_frame, height=2, text="Previous")
        previous_button["command"] = self.button_press_previous
        previous_button.grid(column=0, row=8, pady=5, padx=5)

        first_button = tk.Button(control_frame, height=2, text="First")
        first_button["command"] = self.button_press_first
        first_button.grid(column=0, row=9, pady=5, padx=5)

        self.episode_info = tk.Label(control_frame, text="#None")
        self.episode_info.grid(column=0, row=10, pady=20)

    def left_button_pressed(self, track_point):
        if self.filtered_episodes:
            (self.chosen_event, self.chosen_event_index) = self.filtered_episodes[self.chosen_route_index].get_closest_event_to_point(track_point)
            self.draw_chosen_event_()
            self.display_info_about_chosen_event()

    def go_backwards(self, track_point):
        episode_events = self.filtered_episodes[self.chosen_route_index].events

        if self.filtered_episodes and self.chosen_event and self.chosen_event_index > 0:
            self.chosen_event_index -= 1
            self.chosen_event = episode_events[self.chosen_event_index]
            self.draw_chosen_event_()
            self.display_info_about_chosen_event()

    def go_forwards(self, track_point):
        episode_events = self.filtered_episodes[self.chosen_route_index].events

        if self.filtered_episodes and self.chosen_event and self.chosen_event_index < len(episode_events) - 1:
            self.chosen_event_index += 1
            self.chosen_event = episode_events[self.chosen_event_index]
            self.draw_chosen_event_()
            self.display_info_about_chosen_event()

    def redraw(self):

        if not self.filtered_episodes:
            return

        if self.chosen_route_index >= len(self.filtered_episodes):
            self.chosen_route_index = 0
        elif self.chosen_route_index < 0:
            self.chosen_route_index = len(self.filtered_episodes) - 1

        self.draw_episode(self.filtered_episodes[self.chosen_route_index])
        self.draw_chosen_event_()

    def draw_chosen_event_(self):
        if self.chosen_event:
            self.track_graphics.plot_ring_highlight((self.chosen_event.x, self.chosen_event.y), 6, "orange", 2)

    def display_info_about_chosen_event(self):
        print("-------------")
        print("Waypoint = #", self.chosen_event.closest_waypoint_index)
        print("Reward = ", self.chosen_event.reward)
        print("Action = ", self.chosen_event.speed, "m/s   turning", self.chosen_event.steering_angle, "degrees")

        if self.chosen_event.debug_log:
            print("Debug Output:")
            print(self.chosen_event.debug_log)

        if ss.SHOW_SS:
            print("Secret Sauce:")
            print(ss.get_info_about_event(self.current_track, self.chosen_event))

    def warning_track_changed(self):
        self.chosen_route_index = 0
        self.chosen_event = None

    def warning_filtered_episodes_changed(self):
        self.chosen_route_index = 0
        self.chosen_event = None

    def button_press_next(self):
        self.chosen_route_index += 1
        self.chosen_event = None
        self.guru_parent_redraw()

    def button_press_previous(self):
        self.chosen_route_index -= 1
        self.chosen_event = None
        self.guru_parent_redraw()

    def button_press_first(self):
        self.chosen_route_index = 0
        self.chosen_event = None
        self.guru_parent_redraw()


    def draw_episode(self, episode):
        freq_str = ""

        # Want to display this better in its own window etc.
        #for i, f in enumerate(episode.action_frequency):
        #    action = self.action_space[i]
        #    if action is not None:
        #        freq_str += self.action_space[i].get_readable_with_index() + " x " + str(f) + "\n"


        average_speed = round(episode.distance_travelled / episode.time_taken, 1)
        self.episode_info.configure(text="# " + str(episode.id) + "\n" +
                                         str(round(episode.lap_time, 1)) + " secs\n" +
                                         str(average_speed) + " m/s\n" +
                                         str(round(episode.peak_track_speed, 1)) + " m/s\n" +
                                         str(round(episode.average_reward)) + " avg\n" + freq_str)

        if self.colour_scheme.get() == COLOUR_SCHEME_TRACK_SPEED:
            plot_event_method = self.colour_scheme_track_speed
        elif self.colour_scheme.get() == COLOUR_SCHEME_REWARD_100:
            plot_event_method = self.colour_scheme_reward_100
        elif self.colour_scheme.get() == COLOUR_SCHEME_REWARD_20:
            plot_event_method = self.colour_scheme_reward_20
        elif self.colour_scheme.get() == COLOUR_SCHEME_ACTION_SPEED:
            plot_event_method = self.colour_scheme_action_speed
        elif self.colour_scheme.get() == COLOUR_SCHEME_SMOOTHNESS:
            plot_event_method = self.colour_scheme_smoothness
        elif self.colour_scheme.get() == COLOUR_SCHEME_STRAIGHTNESS:
            plot_event_method = self.colour_scheme_straightness
        elif self.colour_scheme.get() == COLOUR_SCHEME_NONE:
            plot_event_method = self.colour_scheme_none
        else:
            print("OOOPS - unknown colour scheme!")
            return

        previous_event = episode.events[0]
        for e in episode.events[1:]:
            if self.action_space_filter.should_show_action(e.action_taken):
                plot_event_method(e, previous_event)
                previous_event = e

    def colour_scheme_reward_100(self, event, previous_event):
        if event.reward >= 1000:
            self.track_graphics.plot_dot((event.x, event.y), 4, "white")
        elif event.reward >= 100:
            self.track_graphics.plot_dot((event.x, event.y), 3, "blue")
        elif event.reward >= 50:
            self.track_graphics.plot_dot((event.x, event.y), 3, "green")
        elif event.reward >= 10:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_reward_20(self, event, previous_event):
        if event.reward >= 100:
            self.track_graphics.plot_dot((event.x, event.y), 4, "white")
        elif event.reward >= 20:
            self.track_graphics.plot_dot((event.x, event.y), 3, "blue")
        elif event.reward >= 10:
            self.track_graphics.plot_dot((event.x, event.y), 3, "green")
        elif event.reward >= 1:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_track_speed(self, event, previous_event):
        if event.track_speed >= 3.5:
            self.track_graphics.plot_dot((event.x, event.y), 4, "white")
        elif event.track_speed >= 3:
            self.track_graphics.plot_dot((event.x, event.y), 3, "blue")
        elif event.track_speed >= 2.5:
            self.track_graphics.plot_dot((event.x, event.y), 3, "green")
        elif event.track_speed >= 1.8:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_action_speed(self, event, previous_event):
        if event.speed >= 3:
            self.track_graphics.plot_dot((event.x, event.y), 4, "green")
        elif event.speed >= 2:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_smoothness(self, event, previous_event):
        if event.action_taken == previous_event.action_taken:
            if self.smoothness_alternate:
                colour = "green"
            else:
                colour = "blue"

            self.track_graphics.plot_dot((event.x, event.y), 3, colour)
            self.track_graphics.plot_dot((previous_event.x, previous_event.y), 3, colour)
            self.smoothness_current = True
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")
            if self.smoothness_current:
                self.smoothness_current = False
                self.smoothness_alternate = not self.smoothness_alternate

    def colour_scheme_straightness(self, event, previous_event):
        if abs(event.steering_angle) < 0.1:
            self.track_graphics.plot_dot((event.x, event.y), 4, "green")
        elif abs(event.steering_angle) < 10.1:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_none(self, event, previous_event):
        self.track_graphics.plot_dot((event.x, event.y), 2, "green")

