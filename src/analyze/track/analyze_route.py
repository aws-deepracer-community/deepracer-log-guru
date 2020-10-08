import tkinter as tk

import src.secret_sauce.glue.glue as ss
from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics
from src.ui.log_event_info_window import LogEventInfoWindow
from src.analyze.selector.episode_selector import EpisodeSelector


COLOUR_SCHEME_REWARD_20 = 0
COLOUR_SCHEME_REWARD_100 = 1
COLOUR_SCHEME_TRACK_SPEED = 2
COLOUR_SCHEME_ACTION_SPEED = 3
COLOUR_SCHEME_SMOOTHNESS = 4
COLOUR_SCHEME_STRAIGHTNESS = 5
COLOUR_SCHEME_PER_SECOND = 6
COLOUR_SCHEME_NONE = 7

BLOB_SIZE_SMALL = "Small"
BLOB_SIZE_MEDIUM = "Medium"
BLOB_SIZE_LARGE = "Large"


class AnalyzeRoute(TrackAnalyzer):


    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics,
                 control_frame :tk.Frame, episode_selector :EpisodeSelector):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self.episode_selector = episode_selector

        self.chosen_event = None

        self.colour_scheme = tk.IntVar()
        self.colour_scheme.set(COLOUR_SCHEME_NONE)

        self.smoothness_alternate = False
        self.smoothness_current = False

        self.floating_window = None

        self.blob_size = tk.StringVar()
        self.blob_size.set(BLOB_SIZE_MEDIUM)


    def build_control_frame(self, control_frame):

        colour_schema_group = tk.LabelFrame(control_frame, text="Colour Scheme", padx=5, pady=5)
        colour_schema_group.pack()

        tk.Radiobutton(colour_schema_group, text="Reward 20", variable=self.colour_scheme, value=COLOUR_SCHEME_REWARD_20,
                       command=self.guru_parent_redraw).grid(column=0, row=0, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Reward 100", variable=self.colour_scheme, value=COLOUR_SCHEME_REWARD_100,
                       command=self.guru_parent_redraw).grid(column=0, row=1, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Track Speed", variable=self.colour_scheme, value=COLOUR_SCHEME_TRACK_SPEED,
                       command=self.guru_parent_redraw).grid(column=0, row=2, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Action Speed", variable=self.colour_scheme, value=COLOUR_SCHEME_ACTION_SPEED,
                       command=self.guru_parent_redraw).grid(column=0, row=3, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Smoothness", variable=self.colour_scheme, value=COLOUR_SCHEME_SMOOTHNESS,
                       command=self.guru_parent_redraw).grid(column=0, row=4, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Straightness", variable=self.colour_scheme, value=COLOUR_SCHEME_STRAIGHTNESS,
                       command=self.guru_parent_redraw).grid(column=0, row=5, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="Per Second", variable=self.colour_scheme, value=COLOUR_SCHEME_PER_SECOND,
                       command=self.guru_parent_redraw).grid(column=0, row=6, pady=2, padx=5)
        tk.Radiobutton(colour_schema_group, text="None", variable=self.colour_scheme, value=COLOUR_SCHEME_NONE,
                       command=self.guru_parent_redraw).grid(column=0, row=7, pady=2, padx=5)

        #######

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
        if self.chosen_event:
            self.track_graphics.plot_ring_highlight((self.chosen_event.x, self.chosen_event.y),
                                                    6 + self.get_increased_blob_size(), "orange", 2)

            self.track_graphics.plot_angle_line_highlight((self.chosen_event.x, self.chosen_event.y),
                                                self.chosen_event.heading, 2, 1, "orange")

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

    def callback_selected_episode_changed(self):
        self.chosen_event = None
        self.guru_parent_redraw()

    def draw_episode(self, episode):

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
        elif self.colour_scheme.get() == COLOUR_SCHEME_PER_SECOND:
            plot_event_method = self.colour_scheme_per_second
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
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.reward >= 100:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "blue")
        elif event.reward >= 50:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.reward >= 10:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_reward_20(self, event, previous_event):
        if event.reward >= 100:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.reward >= 20:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "blue")
        elif event.reward >= 10:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.reward >= 1:
            self.track_graphics.plot_dot((event.x, event.y), 2, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_track_speed(self, event, previous_event):
        if event.track_speed >= 3.5:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "white")
        elif event.track_speed >= 3:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "blue")
        elif event.track_speed >= 2.5:
            self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")
        elif event.track_speed >= 1.8:
            self.track_graphics.plot_dot((event.x, event.y), 2, "yellow")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_action_speed(self, event, previous_event):
        if event.speed >= 3:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "green")
        elif event.speed >= 2:
            self.track_graphics.plot_dot((event.x, event.y), 2, "yellow")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_smoothness(self, event, previous_event):
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

    def colour_scheme_straightness(self, event, previous_event):
        if abs(event.steering_angle) < 0.1:
            self.track_graphics.plot_dot((event.x, event.y), 4 + self.get_increased_blob_size(), "green")
        elif abs(event.steering_angle) < 10.1:
            self.track_graphics.plot_dot((event.x, event.y), 1, "orange")
        else:
            self.track_graphics.plot_dot((event.x, event.y), 1, "grey")

    def colour_scheme_none(self, event, previous_event):
        self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), "green")

    def colour_scheme_per_second(self, event, previous_event):
        if int(event.time_elapsed) % 2 == 0:
            colour = "green"
        else:
            colour = "purple"

        self.track_graphics.plot_dot((event.x, event.y), 3 + self.get_increased_blob_size(), colour)

