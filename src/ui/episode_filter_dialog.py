#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from tkinter import *

from src.episode.episode import REVERSED, OFF_TRACK, CRASHED, LAP_COMPLETE, LOST_CONTROL
from src.episode.episode import POS_XLEFT, POS_LEFT, POS_CENTRAL, POS_RIGHT, POS_XRIGHT
from src.tracks.track import Track
from src.ui.dialog import Dialog, on_validate_waypoint_id
from src.episode.episode_filter import EpisodeFilter, OBJECT_POSITIONS

OPTION_NO_SECTOR = "n/a"

OUTCOME_MAPPING = {"": None, "Reversed": REVERSED, "Off Track": OFF_TRACK, "Crashed": CRASHED,
                   "Lap Complete": LAP_COMPLETE, "Lost Control": LOST_CONTROL}

TRACK_POSITION_MAPPING = {"": None, "Extreme Left": POS_XLEFT, "Left": POS_LEFT, "Central": POS_CENTRAL,
                          "Right": POS_RIGHT, "Extreme Right": POS_XRIGHT}


class EpisodeFilterDialog(Dialog):
    def __init__(self, parent):

        self.episode_filter :EpisodeFilter = parent.episode_filter
        self._current_track: Track = parent.current_track
        self._expect_objects = parent.expect_objects()

        # Instead of the usual "validate_waypoint_id" frm our parent, this one can do the clever stuff
        # to keep the sector name updated with any edits to the waypoint ids
        self.validate_section_start_waypoint_id = (parent.register(self._validate_modified_section_start), '%P')
        self.validate_section_finish_waypoint_id = (parent.register(self._validate_modified_section_finish), '%P')

        self.filter_from_start_line = BooleanVar(value=self.episode_filter.filter_from_start_line)
        self.filter_max_steps = make_nullable_var(self.episode_filter.filter_max_steps)
        self.filter_min_percent = make_nullable_var(self.episode_filter.filter_min_percent)
        self.filter_min_average_reward = make_nullable_var(self.episode_filter.filter_min_average_reward)
        self.filter_peak_track_speed = make_nullable_var(self.episode_filter.filter_peak_track_speed)
        self.filter_max_slide = make_nullable_var(self.episode_filter.filter_max_slide)

        self.filter_outcome = StringVar(value=None)
        for (ui_text, episode_key) in OUTCOME_MAPPING.items():
            if episode_key == self.episode_filter.filter_outcome:
                self.filter_outcome.set(ui_text)

        self.filter_specific_waypoint_id = make_nullable_var(self.episode_filter.filter_specific_waypoint_id)
        self.filter_specific_waypoint_min_reward = make_nullable_var(self.episode_filter.filter_specific_waypoint_min_reward)
        self.filter_specific_waypoint_min_future_reward = make_nullable_var(self.episode_filter.filter_specific_waypoint_min_future_reward)
        self.filter_specific_waypoint_min_track_speed = make_nullable_var(self.episode_filter.filter_specific_waypoint_min_track_speed)
        self.filter_specific_waypoint_max_track_speed = make_nullable_var(self.episode_filter.filter_specific_waypoint_max_track_speed)

        self.filter_specific_waypoint_track_position = StringVar(value=None)
        for (ui_text, episode_key) in TRACK_POSITION_MAPPING.items():
            if episode_key == self.episode_filter.filter_specific_waypoint_track_position:
                self.filter_specific_waypoint_track_position.set(ui_text)

        if self.episode_filter.filter_complete_section:
            (start, finish) = self.episode_filter.filter_complete_section
        else:
            (start, finish) = (None, None)
        self.filter_complete_section_start = make_nullable_var(start)
        self.filter_complete_section_finish = make_nullable_var(finish)
        self.filter_complete_section_time = make_nullable_var(self.episode_filter.filter_complete_section_time)
        self.filter_complete_section_steps = make_nullable_var(self.episode_filter.filter_complete_section_steps)

        if self.episode_filter.filter_object_section:
            (start, finish) = self.episode_filter.filter_object_section
        else:
            (start, finish) = (None, None)
        self.filter_object_section_start = make_nullable_var(start)
        self.filter_object_section_finish = make_nullable_var(finish)
        self.filter_object_section_positions = make_nullable_var(self.episode_filter.filter_object_section_positions)

        self.filter_q1 = BooleanVar(value=self.episode_filter.filter_quarters[0])
        self.filter_q2 = BooleanVar(value=self.episode_filter.filter_quarters[1])
        self.filter_q3 = BooleanVar(value=self.episode_filter.filter_quarters[2])
        self.filter_q4 = BooleanVar(value=self.episode_filter.filter_quarters[3])

        self.filter_debug_contains = make_nullable_var(self.episode_filter.filter_debug_contains)

        self._filter_sector = StringVar(value=self._deduce_name_of_filter_sector(
            self.filter_complete_section_start.get(), self.filter_complete_section_finish.get()))

        super().__init__(parent, "Episode Filter")

    def body(self, master):

        reset_button = Button(master, text="Reset to All", width=15, command=self.reset_to_all, default=ACTIVE)
        reset_button.grid(column=0, row=0, pady=5, padx=5, sticky=W)

        #

        misc_group = LabelFrame(master, text="Miscellaneous", padx=5, pady=5)
        misc_group.grid(column=0, row=1, pady=5, padx=5, sticky=W)

        Checkbutton(
            misc_group, text="From Start Line Only",
            variable=self.filter_from_start_line).grid(column=0, row=0, pady=5, padx=5, columnspan=2, sticky=E)

        Label(misc_group, text="Debug contains").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            misc_group, textvariable=self.filter_debug_contains).grid(column=1, row=1, pady=5, padx=5)

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

        episode_stat_group = LabelFrame(master, text="Whole Episode", padx=5, pady=5)
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

        Label(episode_stat_group, text="Max Slide <=").grid(column=0, row=6, pady=5, padx=5, sticky=E)
        Entry(
            episode_stat_group, textvariable=self.filter_max_slide,
            validate="key", validatecommand=self.validate_positive_integer).grid(column=1, row=6, pady=5, padx=5)

        Label(episode_stat_group, text="Outcome =").grid(column=0, row=7, pady=5, padx=5, sticky=E)
        OptionMenu(episode_stat_group, self.filter_outcome,
                   *OUTCOME_MAPPING.keys()).grid(column=1, row=7, pady=5, padx=5, sticky=W)

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

        Label(waypoint_group, text="Future Reward >=").grid(column=0, row=2, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_min_future_reward,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=2, pady=5, padx=5)

        Label(waypoint_group, text="Track Speed >=").grid(column=0, row=3, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_min_track_speed,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=3, pady=5, padx=5)

        Label(waypoint_group, text="Track Speed <=").grid(column=0, row=4, pady=5, padx=5, sticky=E)
        Entry(
            waypoint_group, textvariable=self.filter_specific_waypoint_max_track_speed,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=4, pady=5, padx=5)

        Label(waypoint_group, text="Position =").grid(column=0, row=5, pady=5, padx=5, sticky=E)
        OptionMenu(waypoint_group, self.filter_specific_waypoint_track_position,
                   *TRACK_POSITION_MAPPING.keys()).grid(column=1, row=5, pady=5, padx=5, sticky=W)

        #

        completed_section_group = LabelFrame(master, text="Completed Section/Sector", padx=5, pady=5)
        completed_section_group.grid(column=1, row=3, pady=5, padx=5, sticky=W)

        menu_values = [OPTION_NO_SECTOR] + self._current_track.get_all_sector_names()
        Label(completed_section_group, text="Sector").grid(column=0, row=0, pady=5, padx=5, sticky=E)
        OptionMenu(completed_section_group, self._filter_sector, *menu_values,
                   command=self._chose_sector).grid(column=1, row=0, pady=5, padx=5, sticky=W)

        Label(completed_section_group, text="Start Waypoint Id").grid(column=0, row=1, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_start,
            validate="key", validatecommand=self.validate_section_start_waypoint_id).grid(column=1, row=1, pady=5, padx=5)

        Label(completed_section_group, text="Finish Waypoint Id").grid(column=0, row=2, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_finish,
            validate="key", validatecommand=self.validate_section_finish_waypoint_id).grid(column=1, row=2, pady=5, padx=5)

        Label(completed_section_group, text="Time (secs) <=").grid(column=0, row=3, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_time,
            validate="key", validatecommand=self.validate_simple_float).grid(column=1, row=3, pady=5, padx=5)

        Label(completed_section_group, text="Steps <=").grid(column=0, row=4, pady=5, padx=5, sticky=E)
        Entry(
            completed_section_group, textvariable=self.filter_complete_section_steps,
            validate="key", validatecommand=self.validate_positive_integer).grid(column=1, row=4, pady=5, padx=5)

        #

        if self._expect_objects:
            obstacle_group = LabelFrame(master, text="Obstacles", padx=5, pady=5)
            obstacle_group.grid(column=2, row=1, pady=5, padx=5, sticky=W, rowspan=2)

            Label(obstacle_group, text="Start Waypoint Id").grid(column=0, row=1, pady=5, padx=5, sticky=E)
            Entry(
                obstacle_group, textvariable=self.filter_object_section_start,
                validate="key", validatecommand=self.validate_waypoint_id).grid(column=1, row=1, pady=5, padx=5)

            Label(obstacle_group, text="Finish Waypoint Id").grid(column=0, row=2, pady=5, padx=5, sticky=E)
            Entry(
                obstacle_group, textvariable=self.filter_object_section_finish,
                validate="key", validatecommand=self.validate_waypoint_id).grid(column=1, row=2, pady=5, padx=5)

            Label(obstacle_group, text="Object Position(s)").grid(column=0, row=3, pady=5, padx=5, sticky=E)
            OptionMenu(obstacle_group, self.filter_object_section_positions,
                       *OBJECT_POSITIONS).grid(column=1, row=3, pady=5, padx=5, sticky=W)

        #

        return default    # Returns widget to have initial focus

    def apply(self):
        if not self._expect_objects:
            self.filter_object_section_start.set("")
            self.filter_object_section_finish.set("")
            self.filter_object_section_positions.set("")

        self.episode_filter.filter_from_start_line = self.filter_from_start_line.get()

        self.episode_filter.filter_max_steps = get_nullable_int_entry(self.filter_max_steps)
        self.episode_filter.filter_min_percent = get_nullable_int_entry(self.filter_min_percent)
        self.episode_filter.filter_min_average_reward = get_nullable_float_entry(self.filter_min_average_reward)
        self.episode_filter.filter_peak_track_speed = get_nullable_float_entry(self.filter_peak_track_speed)
        self.episode_filter.filter_max_slide = get_nullable_int_entry(self.filter_max_slide)
        self.episode_filter.filter_outcome = OUTCOME_MAPPING[self.filter_outcome.get()]

        specific_waypoint_id = get_nullable_int_entry(self.filter_specific_waypoint_id)
        self.episode_filter.set_filter_specific_waypoint_reward(
            specific_waypoint_id, get_nullable_float_entry(self.filter_specific_waypoint_min_reward))
        self.episode_filter.set_filter_specific_waypoint_future_reward(
            specific_waypoint_id, get_nullable_float_entry(self.filter_specific_waypoint_min_future_reward))
        self.episode_filter.set_filter_specific_waypoint_min_track_speed(
            specific_waypoint_id, get_nullable_float_entry(self.filter_specific_waypoint_min_track_speed))
        self.episode_filter.set_filter_specific_waypoint_max_track_speed(
            specific_waypoint_id, get_nullable_float_entry(self.filter_specific_waypoint_max_track_speed))
        self.episode_filter.set_filter_specific_waypoint_track_position(
            specific_waypoint_id, TRACK_POSITION_MAPPING[self.filter_specific_waypoint_track_position.get()])

        self.episode_filter.set_filter_complete_section_and_time(
            get_nullable_int_entry(self.filter_complete_section_start),
            get_nullable_int_entry(self.filter_complete_section_finish),
            get_nullable_float_entry(self.filter_complete_section_time),
            get_nullable_int_entry(self.filter_complete_section_steps))

        self.episode_filter.set_filter_object_section_and_positions(
            get_nullable_int_entry(self.filter_object_section_start),
            get_nullable_int_entry(self.filter_object_section_finish),
            self.filter_object_section_positions.get())

        self.episode_filter.set_filter_quarters(self.filter_q1.get(), self.filter_q2.get(), self.filter_q3.get(), self.filter_q4.get())
        self.episode_filter.set_filter_debug_contains(self.filter_debug_contains.get())

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
        self.filter_max_slide.set("")
        self.filter_outcome.set("")

        self.filter_specific_waypoint_id.set("")
        self.filter_specific_waypoint_min_reward.set("")
        self.filter_specific_waypoint_min_future_reward.set("")
        self.filter_specific_waypoint_min_track_speed.set("")
        self.filter_specific_waypoint_max_track_speed.set("")
        self.filter_specific_waypoint_track_position.set("")

        self.filter_complete_section_start.set("")
        self.filter_complete_section_finish.set("")
        self.filter_complete_section_time.set("")
        self.filter_complete_section_steps.set("")

        self.filter_object_section_start.set("")
        self.filter_object_section_finish.set("")
        self.filter_object_section_positions.set("")

        self.filter_q1.set(True)
        self.filter_q2.set(True)
        self.filter_q3.set(True)
        self.filter_q4.set(True)

        self.filter_debug_contains.set("")

    def _deduce_name_of_filter_sector(self, filter_start: str, filter_finish: str):
        if filter_start and filter_finish:
            filter_start = int(filter_start)
            filter_finish = int(filter_finish)
            sector_names = self._current_track.get_all_sector_names()
            for s in sector_names:
                (start, finish) = self._current_track.get_sector_start_and_finish(s)
                if start == filter_start and finish == filter_finish:
                    return s

        return OPTION_NO_SECTOR

    def _chose_sector(self, value):
        if value != OPTION_NO_SECTOR:
            (start, finish) = self._current_track.get_sector_start_and_finish(value)
            self.filter_complete_section_start.set(start)
            self.filter_complete_section_finish.set(finish)

    def _validate_modified_section_start(self, value):
        is_good = on_validate_waypoint_id(value)
        if is_good:
            self._filter_sector.set(self._deduce_name_of_filter_sector(value, self.filter_complete_section_finish.get()))
        return is_good

    def _validate_modified_section_finish(self, value):
        is_good = on_validate_waypoint_id(value)
        if is_good:
            self._filter_sector.set(self._deduce_name_of_filter_sector(self.filter_complete_section_start.get(), value))
        return is_good


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
