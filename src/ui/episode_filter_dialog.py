
from tkinter import Label, LabelFrame, Entry, Button, StringVar, BooleanVar, Checkbutton, W, E, ACTIVE
from src.ui.dialog import Dialog
from src.episode.episode_filter import EpisodeFilter

class EpisodeFilterDialog(Dialog):
    def __init__(self, parent):

        self.episode_filter :EpisodeFilter = parent.episode_filter

        self.filter_from_start_line = BooleanVar(value=self.episode_filter.filter_from_start_line)
        self.filter_max_steps = make_nullable_var(self.episode_filter.filter_max_steps)
        self.filter_min_percent = make_nullable_var(self.episode_filter.filter_min_percent)
        self.filter_min_average_reward = make_nullable_var(self.episode_filter.filter_min_average_reward)
        self.filter_peak_track_speed = make_nullable_var(self.episode_filter.filter_peak_track_speed)

        self.filter_specific_waypoint_id = make_nullable_var(self.episode_filter.filter_specific_waypoint_id)
        self.filter_specific_waypoint_min_reward = make_nullable_var(self.episode_filter.filter_specific_waypoint_min_reward)

        if self.episode_filter.filter_complete_section:
            (start, finish) = self.episode_filter.filter_complete_section
        else:
            (start, finish) = (None, None)
        self.filter_complete_section_start = make_nullable_var(start)
        self.filter_complete_section_finish = make_nullable_var(finish)
        self.filter_complete_section_time = make_nullable_var(self.episode_filter.filter_complete_section_time)
        self.filter_complete_section_steps = make_nullable_var(self.episode_filter.filter_complete_section_steps)

        self.filter_q1 = BooleanVar(value=self.episode_filter.filter_quarters[0])
        self.filter_q2 = BooleanVar(value=self.episode_filter.filter_quarters[1])
        self.filter_q3 = BooleanVar(value=self.episode_filter.filter_quarters[2])
        self.filter_q4 = BooleanVar(value=self.episode_filter.filter_quarters[3])

        super().__init__(parent, "Episode Filter")

    def body(self, master):

        reset_button = Button(master, text="Reset to All", width=15, command=self.reset_to_all, default=ACTIVE)
        reset_button.grid(column=0, row=0, pady=5, padx=5, sticky=W)


        #

        start_group = LabelFrame(master, text="Start", padx=5, pady=5)
        start_group.grid(column=0, row=1, pady=5, padx=5, sticky=W)

        Checkbutton(
            start_group, text="From Start Line Only",
            variable=self.filter_from_start_line).grid(column=0, row=0, pady=5, padx=5, columnspan=2)

        #

        iteration_group = LabelFrame(master, text="Iteration", padx=5, pady=5)
        iteration_group.grid(column=0, row=2, pady=5, padx=5, sticky=W, columnspan=4)

        Checkbutton(
            iteration_group, text="Q1",
            variable=self.filter_q1).grid(column=0, row=0, pady=5, padx=5)
        Checkbutton(
            iteration_group, text="Q2",
            variable=self.filter_q2).grid(column=1, row=0, pady=5, padx=5)
        Checkbutton(
            iteration_group, text="Q3",
            variable=self.filter_q3).grid(column=2, row=0, pady=5, padx=5)
        Checkbutton(
            iteration_group, text="Q4",
            variable=self.filter_q4).grid(column=3, row=0, pady=5, padx=5)

        #

        episode_stat_group = LabelFrame(master, text="Episode Stat", padx=5, pady=5)
        episode_stat_group.grid(column=0, row=3, pady=5, padx=5, sticky=W)

        Label(episode_stat_group, text="Steps <=").grid(column=0, row=2, pady=5, padx=5, sticky=E)
        default = Entry(
            episode_stat_group, textvariable=self.filter_max_steps,
            validate="key", validatecommand=self.validate_positive_integer).grid(column=1, row=2, pady=5, padx=5)

        Label(episode_stat_group, text="Percent Complete >=").grid(column=0, row=3, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_min_percent,
            validate="key", validatecommand=self.validate_whole_percent).grid(column=1, row=3, pady=5, padx=5)

        Label(episode_stat_group, text="Avg Reward >=").grid(column=0, row=4, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_min_average_reward,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=4, pady=5, padx=5)

        Label(episode_stat_group, text="Peak Track Speed >=").grid(column=0, row=5, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_peak_track_speed,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=5, pady=5, padx=5)

        #

        waypoint_group = LabelFrame(master, text="Waypoint", padx=5, pady=5)
        waypoint_group.grid(column=1, row=1, pady=5, padx=5, sticky=W, rowspan=2)

        Label(waypoint_group, text="Waypoint Id").grid(column=0, row=0, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_id,
            validate="key", validatecommand=self.validate_waypoint_id).grid(column=1, row=0, pady=5, padx=5)

        Label(waypoint_group, text="Reward >=").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_min_reward,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=1, pady=5, padx=5)

        #

        completed_section_group = LabelFrame(master, text="Completed Section", padx=5, pady=5)
        completed_section_group.grid(column=1, row=3, pady=5, padx=5, sticky=W)

        Label(completed_section_group, text="Start Waypoint Id").grid(column=0, row=0, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_start,
            validate="key", validatecommand=self.validate_waypoint_id).grid(column=1, row=0, pady=5, padx=5)

        Label(completed_section_group, text="Finish Waypoint Id").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_finish,
            validate="key", validatecommand=self.validate_waypoint_id).grid(column=1, row=1, pady=5, padx=5)

        Label(completed_section_group, text="Time (secs) <=").grid(column=0, row=2, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_time,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=2, pady=5, padx=5)

        Label(completed_section_group, text="Steps <=").grid(column=0, row=3, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_steps,
            validate="key", validatecommand=self.validate_positive_integer).grid(column=1, row=3, pady=5, padx=5)


        return default    # Returns widget to have initial focus


    def apply(self):
        self.episode_filter.filter_from_start_line = self.filter_from_start_line.get()

        self.episode_filter.filter_max_steps = get_nullable_int_entry(self.filter_max_steps)
        self.episode_filter.filter_min_percent = get_nullable_int_entry(self.filter_min_percent)
        self.episode_filter.filter_min_average_reward = get_nullable_float_entry(self.filter_min_average_reward)
        self.episode_filter.filter_peak_track_speed = get_nullable_float_entry(self.filter_peak_track_speed)

        self.episode_filter.set_filter_specific_waypoint_reward(
            get_nullable_int_entry(self.filter_specific_waypoint_id),
            get_nullable_float_entry(self.filter_specific_waypoint_min_reward))

        self.episode_filter.set_filter_complete_section_and_time(
            get_nullable_int_entry(self.filter_complete_section_start),
            get_nullable_int_entry(self.filter_complete_section_finish),
            get_nullable_float_entry(self.filter_complete_section_time),
            get_nullable_int_entry(self.filter_complete_section_steps))

        self.episode_filter.set_filter_quarters(self.filter_q1.get(), self.filter_q2.get(), self.filter_q3.get(), self.filter_q4.get())

        self.parent.reapply_episode_filter()

    def validate(self):
        return True

    def reset_to_all(self):
        self.episode_filter.reset()

        self.filter_from_start_line.set(False)
        self.filter_max_steps.set("")
        self.filter_min_percent.set("")
        self.filter_min_average_reward.set("")
        self.filter_peak_track_speed.set("")

        self.filter_specific_waypoint_id.set("")
        self.filter_specific_waypoint_min_reward.set("")

        self.filter_complete_section_start.set("")
        self.filter_complete_section_finish.set("")
        self.filter_complete_section_time.set("")
        self.filter_complete_section_steps.set("")


def make_nullable_var(initial_value):
    if initial_value is not None:
        return StringVar(value=str(initial_value))
    else:
        return StringVar(value=None)

def get_nullable_int_entry(tk_var):
    value = tk_var.get()
    if value == "":
        return None
    else:
        return int(value)

def get_nullable_float_entry(tk_var):
    value = tk_var.get()
    if value == "":
        return None
    else:
        return float(value)
