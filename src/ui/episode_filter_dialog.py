
from tkinter import Label, LabelFrame, Entry, StringVar, BooleanVar, IntVar, Radiobutton, Checkbutton, W, E, LEFT
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

        #

        start_group = LabelFrame(master, text="Start", padx=5, pady=5)
        start_group.grid(column=0, row=0, pady=5, padx=5, sticky=W)

        Checkbutton(
            start_group, text="From Start Line Only",
            variable=self.filter_from_start_line).grid(column=0, row=0, pady=5, padx=5, columnspan=2)

        #

        episode_stat_group = LabelFrame(master, text="Episode Stat", padx=5, pady=5)
        episode_stat_group.grid(column=0, row=1, pady=5, padx=5, sticky=W)

        Checkbutton(
            episode_stat_group, text="Complete Laps",
            variable=self.filter_complete_laps).grid(column=0, row=1, pady=5, padx=5, columnspan=2)

        Label(episode_stat_group, text="Steps <=").grid(column=0, row=2, pady=5, padx=5, sticky=E)
        default = Entry(
            episode_stat_group, textvariable=self.filter_max_steps).grid(column=1, row=2, pady=5, padx=5)

        Label(episode_stat_group, text="Percent Complete >=").grid(column=0, row=3, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_min_percent).grid(column=1, row=3, pady=5, padx=5)

        Label(episode_stat_group, text="Avg Reward >=").grid(column=0, row=4, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_min_average_reward).grid(column=1, row=4, pady=5, padx=5)

        Label(episode_stat_group, text="Peak Track Speed >=").grid(column=0, row=5, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_peak_track_speed).grid(column=1, row=5, pady=5, padx=5)

        #

        waypoint_group = LabelFrame(master, text="Waypoint", padx=5, pady=5)
        waypoint_group.grid(column=0, row=2, pady=5, padx=5, sticky=W)

        Label(waypoint_group, text="Waypoint Id").grid(column=0, row=0, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_id).grid(column=1, row=0, pady=5, padx=5)

        Label(waypoint_group, text="Reward >=").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_min_reward).grid(column=1, row=1, pady=5, padx=5)

        #

        completed_section_group = LabelFrame(master, text="Completed Section", padx=5, pady=5)
        completed_section_group.grid(column=0, row=3, pady=5, padx=5, sticky=W)

        Label(completed_section_group, text="Start Waypoint Id").grid(column=0, row=0, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_start).grid(column=1, row=0, pady=5, padx=5)

        Label(completed_section_group, text="Finish Waypoint Id").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_finish).grid(column=1, row=1, pady=5, padx=5)

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
