#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

from tkinter import Menu, messagebox

import src.log.log_utils
from src.ui.file_options_dialog import FileOptionsDialog
from src.ui.open_file_dialog import OpenFileDialog
from src.ui.new_files_dialog import NewFilesDialog
from src.ui.episode_filter_dialog import EpisodeFilterDialog
from src.ui.action_filter_dialog import ActionSpaceFilterDialog

import src.secret_sauce.glue.glue as ss


class MenuBar():
    def __init__(self, root, main_app, file_is_open:bool, is_continuous_action_space:bool):
        self.main_app = main_app
        self.root = root
        self.menubar = Menu(root)
        self._file_is_open = file_is_open
        self._is_continuous_action_space = is_continuous_action_space
        self._create_menus()

    def _create_menus(self):
        self.add_file_menu()
        self.add_track_menu()

        if self._file_is_open:
            self.add_episode_menu()
            if not self._is_continuous_action_space:
                self.add_action_menu()
            self.add_sector_menu()
            self.add_analyze_menu()

        self.add_fitting_menu()
        self.add_zoom_menu()
        self.add_view_menu()
        self.add_secret_sauce_menu()
        self.add_admin_menu()

        self.root.config(menu=self.menubar)

    def refresh(self):
        self.menubar = Menu(self.root)
        self._create_menus()

    def add_track_menu(self):
        existing_log_world_names = src.log.log_utils.get_world_names_of_existing_logs(self.main_app.get_log_directory())

        menu = Menu(self.menubar, tearoff=0)

        if existing_log_world_names:
            for i, t in enumerate(self.main_app.tracks.values()):
                if t.get_world_name() in existing_log_world_names:
                    menu.add_command(label=t.get_name_on_menu(), command=lambda track=t: self.choose_track(track))
            menu.add_separator()

        for i, t in enumerate(self.main_app.tracks.values()):
            if t.get_world_name() not in existing_log_world_names:
                menu.add_command(label=t.get_name_on_menu(), command=lambda track=t: self.choose_track(track))

        self.menubar.add_cascade(label="Track", menu=menu)

    def add_sector_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        for s in self.main_app.current_track.get_all_sector_names():
            menu.add_command(label="Sector " + s,
                             command=lambda sector=s: self.choose_sector(sector))

        self.menubar.add_cascade(label="Sector", menu=menu)

    def add_file_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="New File(s)", command=self.new_files)
        menu.add_command(label="Open File", command=self.open_file)
        menu.add_command(label="Switch Directory", command=self.main_app.menu_callback_switch_directory)
        menu.add_separator()
        menu.add_command(label="Options", command=self.file_options)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.root.quit)

        self.menubar.add_cascade(label="File", menu=menu)

    def add_zoom_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="Zoom - In/Out", command=self.main_app.menu_callback_zoom_in_out)
        menu.add_separator()

        for s in self.main_app.current_track.get_all_sector_names():
            menu.add_command(label="Sector " + s,
                             command=lambda sector=s: self.zoom_sector(sector))

        self.menubar.add_cascade(label="Zoom", menu=menu)

    def add_view_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="Grid - Front", command=self.main_app.menu_callback_grid_front)
        menu.add_command(label="Grid - Back", command=self.main_app.menu_callback_grid_back)
        menu.add_command(label="Grid - Off", command=self.main_app.menu_callback_grid_off)
        menu.add_separator()
        menu.add_command(label="Analysis - Front", command=self.main_app.menu_callback_analyze_front)
        menu.add_command(label="Analysis - Back", command=self.main_app.menu_callback_analyze_back)
        menu.add_separator()
        menu.add_command(label="Track - Front", command=self.main_app.menu_callback_track_front)
        menu.add_command(label="Track - Back", command=self.main_app.menu_callback_track_back)
        menu.add_separator()
        menu.add_command(label="Track - Grey", command=self.main_app.menu_callback_track_grey)
        menu.add_command(label="Track - Blue", command=self.main_app.menu_callback_track_blue)
        menu.add_separator()
        menu.add_command(label="Sectors - On", command=self.main_app.menu_callback_sectors_on)
        menu.add_command(label="Sectors - Off", command=self.main_app.menu_callback_sectors_off)
        menu.add_separator()
        menu.add_command(label="Waypoints - Large", command=self.main_app.menu_callback_waypoints_large)
        menu.add_command(label="Waypoints - Small", command=self.main_app.menu_callback_waypoints_small)
        menu.add_command(label="Waypoints - Micro", command=self.main_app.menu_callback_waypoints_micro)
        menu.add_command(label="Waypoints - Off", command=self.main_app.menu_callback_waypoints_off)
        menu.add_separator()
        menu.add_command(label="Waypoint Labels - On", command=self.main_app.menu_callback_waypoint_labels_on)
        menu.add_command(label="Waypoint Labels - Off", command=self.main_app.menu_callback_waypoint_labels_off)
        menu.add_separator()
        menu.add_command(label="Annotations - Front", command=self.main_app.menu_callback_annotations_front)
        menu.add_command(label="Annotations - Back", command=self.main_app.menu_callback_annotations_back)
        menu.add_command(label="Annotations - Off", command=self.main_app.menu_callback_annotations_off)
        menu.add_separator()
        menu.add_command(label="Heading - On", command=self.main_app.menu_callback_heading_on)
        menu.add_command(label="Heading - Off", command=self.main_app.menu_callback_heading_off)
        menu.add_separator()
        menu.add_command(label="True Bearing - On", command=self.main_app.menu_callback_true_bearing_on)
        menu.add_command(label="True Bearing - Off", command=self.main_app.menu_callback_true_bearing_off)
        menu.add_separator()
        menu.add_command(label="Camera Vision - On", command=self.main_app.menu_callback_camera_vision_on)
        menu.add_command(label="Camera Vision - Off", command=self.main_app.menu_callback_camera_vision_off)

        self.menubar.add_cascade(label="View", menu=menu)

    def add_analyze_menu(self):
        menu = Menu(self.menubar, tearoff=0)

        menu.add_command(label="Episode Route", command=self.main_app.menu_callback_analyze_route)
        menu.add_command(label="Episode Speed", command=self.main_app.menu_callback_analyze_episode_speed)
        menu.add_command(label="Episode Reward", command=self.main_app.menu_callback_analyze_episode_reward)
        menu.add_command(label="Episode Slide", command=self.main_app.menu_callback_analyze_episode_slide)
        if not self._is_continuous_action_space:
            menu.add_command(label="Episode Action Distribution", command=self.main_app.menu_callback_analyze_episode_action_distribution)

        menu.add_separator()
        menu.add_command(label="Heatmap", command=self.main_app.menu_callback_analyze_track_heatmap)
        menu.add_command(label="Heatmap + Episode Route", command=self.main_app.menu_callback_analyze_route_over_heatmap)
        menu.add_command(label="Heatmap + Exit Points", command=self.main_app.menu_callback_analyze_exit_points_over_heatmap)

        menu.add_separator()
        menu.add_command(label="Exit Points", command=self.main_app.menu_callback_analyze_exit_points)
        menu.add_command(label="Simulate Race", command=self.main_app.menu_callback_analyze_race)

        menu.add_separator()    # TODO - hyperparams ...
        # menu.add_command(label="View Hyperparameters", command=self.main_app.menu_callback_analyze_hyperparameters)
        menu.add_command(label="Compare Discount Factors", command=self.main_app.menu_callback_analyze_discount_factors)

        menu.add_separator()
        menu.add_command(label="Training Progress", command=self.main_app.menu_callback_analyze_training_progress)
        menu.add_command(label="Quarterly Results", command=self.main_app.menu_callback_analyze_quarterly_results)
        menu.add_command(label="Complete Lap Percentage", command=self.main_app.menu_callback_analyze_complete_lap_percentage)

        menu.add_separator()
        menu.add_command(label="Lap Time Correlations", command=self.main_app.menu_callback_analyze_lap_time_correlations)
        menu.add_command(label="Lap Time Distribution", command=self.main_app.menu_callback_analyze_lap_time_distribution)

        menu.add_separator()
        menu.add_command(label="Sector Time Correlations", command=self.main_app.menu_callback_analyze_sector_time_correlations)

        menu.add_separator()
        menu.add_command(label="Reward Distribution", command=self.main_app.menu_callback_analyze_reward_distribution)
        menu.add_command(label="Common Rewards", command=self.main_app.menu_callback_analyze_common_rewards)
        menu.add_command(label="Rewards per Waypoint", command=self.main_app.menu_callback_analyze_rewards_per_waypoint)

        self.menubar.add_cascade(label="Analyze", menu=menu)

    def add_fitting_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="Track Curve Fitting", command=self.main_app.menu_callback_analyze_curve_fitting)
        menu.add_command(label="Track Straight Fitting", command=self.main_app.menu_callback_analyze_straight_fitting)

        self.menubar.add_cascade(label="Fitting", menu=menu)

    def add_episode_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="All", command=self.main_app.menu_callback_episodes_all)
        menu.add_command(label="All From Start", command=self.main_app.menu_callback_episodes_all_from_start)
        menu.add_separator()

        menu.add_command(label="Complete Laps", command=self.main_app.menu_callback_episodes_complete_laps)
        menu.add_command(label="Complete Laps from Start", command=self.main_app.menu_callback_episodes_complete_laps_from_start)
        menu.add_command(label="Fast Laps", command=self.main_app.menu_callback_episodes_fast_laps)
        menu.add_separator()

        menu.add_command(label="10% complete", command=self.main_app.menu_callback_episodes_min_percent_10)
        menu.add_command(label="25% complete", command=self.main_app.menu_callback_episodes_min_percent_25)
        menu.add_command(label="33% complete", command=self.main_app.menu_callback_episodes_min_percent_33)
        menu.add_command(label="50% complete", command=self.main_app.menu_callback_episodes_min_percent_50)
        menu.add_separator()

        menu.add_command(label="Q1", command=self.main_app.menu_callback_episodes_q1)
        menu.add_command(label="Q2", command=self.main_app.menu_callback_episodes_q2)
        menu.add_command(label="Q3", command=self.main_app.menu_callback_episodes_q3)
        menu.add_command(label="Q4", command=self.main_app.menu_callback_episodes_q4)
        menu.add_separator()

        for s in self.main_app.current_track.get_all_sector_names():
            menu.add_command(label="Sector " + s,
                             command=lambda sector=s: self._choose_episode_filter_sector(sector))
        menu.add_separator()

        menu.add_command(label="More ...", command=self.open_episode_filter_dialog)

        self.menubar.add_cascade(label="Episodes", menu=menu)

    def add_action_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="All", command=self.main_app.menu_callback_actions_all)
        menu.add_command(label="High Speed", command=self.main_app.menu_callback_actions_high_speed)
        menu.add_command(label="Medium Speed", command=self.main_app.menu_callback_actions_medium_speed)
        menu.add_command(label="Low Speed", command=self.main_app.menu_callback_actions_low_speed)
        menu.add_command(label="Straight", command=self.main_app.menu_callback_actions_straight)
        menu.add_separator()
        menu.add_command(label="More ...", command=self.open_action_space_filter_dialog)

        self.menubar.add_cascade(label="Actions", menu=menu)

    def add_secret_sauce_menu(self):
        if ss.SHOW_SS:
            ss.make_menu(self.menubar, self.main_app)

    def add_admin_menu(self):
        menu = Menu(self.menubar, tearoff=0)
        menu.add_command(label="Re-calculate Log Meta", command=self.refresh_all_log_meta)
        menu.add_command(label="View Log File Info", command=self.main_app.menu_callback_view_log_file_info)

        self.menubar.add_cascade(label="Admin", menu=menu)

    def new_files(self):
        NewFilesDialog(self.main_app, self.main_app.please_wait)
        self.refresh()

    def open_file(self):
        OpenFileDialog(self.main_app, "Open File")

    def file_options(self):
        FileOptionsDialog(self.main_app)

    def choose_track(self, track):
        self.main_app.menu_callback_switch_track(track)

    def choose_sector(self, sector: str):
        self.main_app.menu_callback_sector_filter(sector)

    def zoom_sector(self, sector: str):
        self.main_app.menu_callback_sector_zoom(sector)

    def _choose_episode_filter_sector(self, sector: str):
        self.main_app.menu_callback_episodes_sector(sector)

    def open_episode_filter_dialog(self):
        EpisodeFilterDialog(self.main_app)

    def open_action_space_filter_dialog(self):
        ActionSpaceFilterDialog(self.main_app)

    def refresh_all_log_meta(self):
        src.log.log_utils.refresh_all_log_meta(self.main_app.please_wait, self.main_app.get_log_directory())
        self.main_app.please_wait.stop()
        messagebox.showinfo("Refresh All Log Meta", "Refresh succeeded!")
        self.refresh()
