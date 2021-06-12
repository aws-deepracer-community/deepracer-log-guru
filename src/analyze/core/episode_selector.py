#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from re import fullmatch
from tkinter import messagebox


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
        old_episode = self.get_selected_episode()
        if old_episode is not None:
            old_episode_id = old_episode.id
        else:
            old_episode_id = None

        self._filtered_episodes = filtered_episodes
        self._chosen_episode_filter_index = 0

        keep_specific_choice = False
        if old_episode_id is not None and filtered_episodes is not None:
            for i, e in enumerate(filtered_episodes):
                if e.id == old_episode_id:
                    self._chosen_episode_filter_index = i
                    if old_episode_id == self._chosen_episode_specific_id:
                        keep_specific_choice = True

        if not keep_specific_choice:
            self._remove_any_specific_episode_choice()

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
        assert 0 <= episode_id < len(self._all_episodes)
        self._episode_number_entry.set(str(episode_id))
        self._chosen_episode_specific_id = episode_id
        self.update_episode_info_in_ui_()
        self.callback_method_()

    def add_to_control_frame(self, parent_frame, callback_method):
        self._validate_episode_id = (parent_frame.register(on_validate_episode_id), '%P')

        self.callback_method_ = callback_method

        label_frame = tk.LabelFrame(parent_frame, text="Episode", padx=5, pady=5)

        previous_button = tk.Button(label_frame, width=4, text="<<")
        previous_button["command"] = self.button_press_previous
        previous_button.grid(column=0, row=0, pady=5, padx=3)

        next_button = tk.Button(label_frame, width=4, text=">>")
        next_button["command"] = self.button_press_next
        next_button.grid(column=1, row=0, pady=5, padx=3)

        first_button = tk.Button(label_frame, width=4, text="First")
        first_button["command"] = self.button_press_first
        first_button.grid(column=2, row=0, pady=5, padx=3)

        goto_button = tk.Button(label_frame, width=4, text="Go to")
        goto_button["command"] = self.button_press_goto
        goto_button.grid(column=0, row=1, pady=5, padx=3)

        tk.Entry(
            label_frame, textvariable=self._episode_number_entry, width=5,
            validate="key", validatecommand=self._validate_episode_id).grid(column=1, row=1, sticky=tk.E, pady=5, padx=5)

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

        if self._chosen_episode_specific_id is not None:
            current_index = self._get_nearest_filter_index(self._chosen_episode_specific_id)
            if self._filtered_episodes[current_index].id == self._chosen_episode_specific_id:
                self._chosen_episode_filter_index = current_index + 1
            else:
                self._chosen_episode_filter_index = current_index
            self._remove_any_specific_episode_choice()
        else:
            self._chosen_episode_filter_index += 1

        if self._chosen_episode_filter_index >= len(self._filtered_episodes):
            self._chosen_episode_filter_index = 0

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def button_press_previous(self):
        if not self._filtered_episodes:
            return

        if self._chosen_episode_specific_id is not None:
            current_index = self._get_nearest_filter_index(self._chosen_episode_specific_id)
            self._chosen_episode_filter_index = current_index - 1
            self._remove_any_specific_episode_choice()
        else:
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

    def button_press_goto(self):
        if self._episode_number_entry.get() != "" and self._all_episodes is not None:
            episode_id = int(self._episode_number_entry.get())
            max_episode_id = len(self._all_episodes) - 1
            if episode_id > max_episode_id:
                messagebox.showerror("Invalid Episode Id",
                                     "No such episode #" + str(episode_id) +
                                     "\nEnter a number in the range 0 to " + str(max_episode_id))
            else:
                self.select_specific_episode(episode_id)

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

    def _get_nearest_filter_index(self, actual_episode_id):
        if self._filtered_episodes is not None:
            for i, e in enumerate(self._filtered_episodes):
                if e.id >= actual_episode_id:
                    return i
            return 0
        else:
            return None


def on_validate_episode_id(new_value):
    return len(new_value) <= 5 and fullmatch('\\d*', new_value) is not None
