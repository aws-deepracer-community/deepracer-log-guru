#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from re import fullmatch


class EpisodeSelector:

    def __init__(self):

        # All private

        self.tk_episode_info_var_ = tk.StringVar()
        self._episode_number_entry = tk.StringVar()
        self._chosen_episode_filter_index = 0
        self._chosen_episode_specific_id = None
        self._filtered_episodes = None
        self._all_episodes = None
        self.callback_method_ = None
        self.episode_info = None

        self._validate_episode_id = None

    #
    # Public Methods
    #

    def set_filtered_episodes(self, filtered_episodes):
        self._filtered_episodes = filtered_episodes
        self._chosen_episode_filter_index = 0

        self.update_episode_info_in_ui_()

    def set_all_episodes(self, all_episodes):
        self._all_episodes = all_episodes
        self._chosen_episode_specific_id = None

        self.update_episode_info_in_ui_()

    def get_selected_episode(self):
        if self._chosen_episode_specific_id is None:
            if self._filtered_episodes:
                return self._filtered_episodes[self._chosen_episode_filter_index]
            else:
                return None
        else:
            if 0 <= self._chosen_episode_specific_id < len(self._all_episodes):
                episode = self._all_episodes[self._chosen_episode_specific_id]
                assert episode.id == self._chosen_episode_specific_id
                return episode
            else:
                return None

    def select_specific_episode(self, episode_id: int):
        assert 0 <= episode_id <= len(self._all_episodes)
        self._episode_number_entry.set(str(episode_id))
        self._chosen_episode_specific_id = episode_id
        self.update_episode_info_in_ui_()
        self.callback_method_()

    def add_to_control_frame(self, parent_frame, callback_method):
        self._validate_episode_id = (parent_frame.register(on_validate_episode_id), '%P')

        self.callback_method_ = callback_method

        label_frame = tk.LabelFrame(parent_frame, text="Episode", padx=5, pady=5)

        previous_button = tk.Button(label_frame, height=2, text="<<")
        previous_button["command"] = self.button_press_previous
        previous_button.grid(column=0, row=0, pady=5, padx=3)

        next_button = tk.Button(label_frame, height=2, text=">>")
        next_button["command"] = self.button_press_next
        next_button.grid(column=1, row=0, pady=5, padx=3)

        first_button = tk.Button(label_frame, height=2, text="First")
        first_button["command"] = self.button_press_first
        first_button.grid(column=2, row=0, pady=5, padx=3)

        tk.Label(label_frame, text="Or go to #").grid(column=0, row=1, columnspan=2, pady=5, padx=3)
        tk.Entry(
            label_frame, textvariable=self._episode_number_entry, width=5,
            validate="key", validatecommand=self._validate_episode_id).grid(column=2, row=1, pady=5, padx=5)

        self.episode_info = tk.Label(label_frame, text="", textvariable=self.tk_episode_info_var_, justify=tk.LEFT)
        self.episode_info.grid(column=0, row=2, columnspan=3, pady=3, sticky=tk.W)

        self.update_episode_info_in_ui_()

        label_frame.pack(pady=4, fill=tk.X, padx=10)

    #
    # Private methods
    #

    def button_press_next(self):
        if not self._filtered_episodes:
            return

        self._remove_any_specific_episode_choice()

        self._chosen_episode_filter_index += 1

        if self._chosen_episode_filter_index >= len(self._filtered_episodes):
            self._chosen_episode_filter_index = 0

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def button_press_previous(self):
        if not self._filtered_episodes:
            return

        self._remove_any_specific_episode_choice()

        self._chosen_episode_filter_index -= 1

        if self._chosen_episode_filter_index < 0:
            self._chosen_episode_filter_index = len(self._filtered_episodes) - 1

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def button_press_first(self):
        if not self._filtered_episodes:
            return

        self._remove_any_specific_episode_choice()

        self._chosen_episode_filter_index = 0

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def update_episode_info_in_ui_(self):
        episode = self.get_selected_episode()

        if not episode:
            self.tk_episode_info_var_.set("No Episode")
        else:
            if episode.time_taken > 0:
                average_speed = round(episode.distance_travelled / episode.time_taken, 1)
            else:
                average_speed = 0

            self.tk_episode_info_var_.set(
                "# " + str(episode.id) + "\n" +
                str(round(episode.predicted_lap_time, 1)) + " secs\n" +
                str(average_speed) + " m/s")

    def _remove_any_specific_episode_choice(self):
        self._chosen_episode_specific_id = None
        self._episode_number_entry.set("")


def on_validate_episode_id(new_value):
    return len(new_value) <= 5 and fullmatch('\\d*', new_value) is not None
