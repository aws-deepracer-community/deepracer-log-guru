
from tkinter import Label, Entry, StringVar, BooleanVar, IntVar, Radiobutton, Checkbutton, W, LEFT
from src.ui.dialog import Dialog
from src.episode.episode_filter import EpisodeFilter

class EpisodeFilterDialog(Dialog):
    def __init__(self, parent):
        self.episode_filter:EpisodeFilter = parent.episode_filter

        self.filter_from_start_line = BooleanVar(value=self.episode_filter.filter_from_start_line)
        self.filter_complete_laps = BooleanVar(value=self.episode_filter.filter_complete_laps)
        self.filter_max_steps = IntVar(value=self.episode_filter.filter_max_steps)
        self.filter_min_percent = IntVar(value=self.episode_filter.filter_min_percent)
        self.filter_min_average_reward = IntVar(value=self.episode_filter.filter_min_average_reward)
        self.filter_peak_track_speed = StringVar(value=str(self.episode_filter.filter_peak_track_speed))

        if self.episode_filter.filter_specific_waypoint_id >= 0:
            self.filter_specific_waypoint_id = IntVar(value=self.episode_filter.filter_specific_waypoint_id)
            self.filter_specific_waypoint_min_reward = StringVar(value=str(self.episode_filter.filter_specific_waypoint_min_reward))
        else:
            self.filter_specific_waypoint_id = IntVar()
            self.filter_specific_waypoint_min_reward = StringVar()

        if self.episode_filter.filter_complete_section is None:
            self.filter_complete_section_start = IntVar()
            self.filter_complete_section_finish = IntVar()
        else:
            (start, finish) = self.episode_filter.filter_complete_section
            self.filter_complete_section_start = IntVar(value=start)
            self.filter_complete_section_finish = IntVar(value=finish)

        super().__init__(parent, "Episode Filter")


    def body(self, master):

        Checkbutton(
            master, text="From Start Line Only",
            variable=self.filter_from_start_line).grid(column=0, row=0, pady=5, padx=5, columnspan=2)

        Checkbutton(
            master, text="Complete Laps",
            variable=self.filter_complete_laps).grid(column=0, row=1, pady=5, padx=5, columnspan=2)

        Label(master, text="Steps <=").grid(column=0, row=2, pady=5, padx=5)
        default = Entry(
            master, textvariable=self.filter_max_steps).grid(column=1, row=2, pady=5, padx=5)

        Label(master, text="Percent Complete >=").grid(column=0, row=3, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_min_percent).grid(column=1, row=3, pady=5, padx=5)

        Label(master, text="Avg Reward >=").grid(column=0, row=4, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_min_average_reward).grid(column=1, row=4, pady=5, padx=5)

        Label(master, text="Peak Track Speed >=").grid(column=0, row=5, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_peak_track_speed).grid(column=1, row=5, pady=5, padx=5)

        Label(master, text="Waypoint Reward ...").grid(column=0, row=6, pady=5, padx=5)
        Label(master, text="Waypoint=").grid(column=0, row=7, pady=5, padx=5)
        Label(master, text="Reward>=").grid(column=1, row=7, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_specific_waypoint_id).grid(column=0, row=8, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_specific_waypoint_min_reward).grid(column=1, row=8, pady=5, padx=5)


        Label(master, text="Completed Section ...").grid(column=0, row=9, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_complete_section_start).grid(column=0, row=10, pady=5, padx=5)
        Entry(
            master, textvariable=self.filter_complete_section_finish).grid(column=1, row=10, pady=5, padx=5)

        return default    # Returns widget to have initial focus

    def apply(self):
        self.episode_filter.filter_from_start_line = self.filter_from_start_line.get()
        self.episode_filter.filter_complete_laps = self.filter_complete_laps.get()
        self.episode_filter.filter_max_steps = self.filter_max_steps.get()
        self.episode_filter.filter_min_percent = self.filter_min_percent.get()
        self.episode_filter.filter_min_average_reward = self.filter_min_average_reward.get()
        self.episode_filter.filter_peak_track_speed = float(self.filter_peak_track_speed.get())

        if self.filter_specific_waypoint_id.get() >= 0 and self.filter_specific_waypoint_min_reward.get():
            self.episode_filter.set_filter_specific_waypoint_reward(self.filter_specific_waypoint_id.get(),
                                                                    float(self.filter_specific_waypoint_min_reward.get()))

        if self.filter_complete_section_start.get() > 0 and self.filter_complete_section_finish.get() > 0:
            self.episode_filter.filter_complete_section = (self.filter_complete_section_start.get(),
                                                           self.filter_complete_section_finish.get())
        elif self.filter_complete_section_start.get() > 0:
            self.episode_filter.filter_complete_section = (self.filter_complete_section_start.get(),
                                                           self.filter_complete_section_start.get())
        else:
            self.episode_filter.filter_complete_section = None

        self.parent.reapply_episode_filter()

    def validate(self):
        return True
