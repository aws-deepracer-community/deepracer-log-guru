import tkinter as tk

class EpisodeSelector:

    def __init__(self):

        # All private

        self.tk_episode_info_var_ = tk.StringVar()
        self.chosen_episode_index_ = 0
        self.filtered_episodes_ = None
        self.callback_method_ = None
        self.filtered_episodes_ = None

    #
    # Public Methods
    #

    def set_filtered_episodes(self, filtered_episodes):
        self.filtered_episodes_ = filtered_episodes
        self.chosen_episode_index_ = 0

        self.update_episode_info_in_ui_()

    def get_selected_episode(self):
        if self.filtered_episodes_:
            return self.filtered_episodes_[self.chosen_episode_index_]
        else:
            return None

    def get_label_frame(self, parent_frame, callback_method):
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

        self.episode_info = tk.Label(label_frame, text="", textvariable=self.tk_episode_info_var_)
        self.episode_info.grid(column=0, row=1, columnspan=3, pady=3)

        self.update_episode_info_in_ui_()

        return label_frame


    #
    # Private methods
    #

    def button_press_next(self):
        if not self.filtered_episodes_:
            return

        self.chosen_episode_index_ += 1

        if self.chosen_episode_index_ >= len(self.filtered_episodes_):
            self.chosen_episode_index_ = 0

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def button_press_previous(self):
        if not self.filtered_episodes_:
            return

        self.chosen_episode_index_ -= 1

        if self.chosen_episode_index_ < 0:
            self.chosen_episode_index_ = len(self.filtered_episodes_) - 1

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def button_press_first(self):
        if not self.filtered_episodes_:
            return

        self.chosen_episode_index_ = 0

        self.update_episode_info_in_ui_()
        self.callback_method_()

    def update_episode_info_in_ui_(self):
        episode = self.get_selected_episode()

        if not episode:
            self.tk_episode_info_var_.set("No Episode")
        else:
            average_speed = round(episode.distance_travelled / episode.time_taken, 1)

            self.tk_episode_info_var_.set(
                "# " + str(episode.id) + "\n" +
                str(round(episode.predicted_lap_time, 1)) + " secs\n" +
                str(average_speed) + " m/s")







