#
# DeepRacer Guru
#
# Version 3.0 onwards
#
# Copyright (c) 2021 dmh23
#

import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import src.secret_sauce.glue.glue as ss

from src.analyze.track.analyze_heatmap import AnalyzeHeatmap
from src.analyze.track.analyze_exit_points import AnalyzeExitPoints
from src.analyze.track.analyze_route import AnalyzeRoute
from src.analyze.track.analyze_race import AnalyzeRace
from src.analyze.track.analyze_curve_fitting import AnalyzeCurveFitting
from src.analyze.track.analyze_straight_fitting import AnalyzeStraightFitting

from src.analyze.graph.analyze_training_progress import AnalyzeTrainingProgress
from src.analyze.graph.analyze_quarterly_results import AnalyzeQuarterlyResults
from src.analyze.graph.analyze_reward_distribution import AnalyzeRewardDistribution
from src.analyze.graph.analyze_common_rewards import AnalyzeCommonRewards
from src.analyze.graph.analyze_rewards_per_waypoint import AnalyzeRewardsPerWaypoint
from src.analyze.graph.analyze_episode_speed import AnalyzeEpisodeSpeed
from src.analyze.graph.analyze_episode_reward import AnalyzeEpisodeReward
from src.analyze.graph.analyze_episode_slide import AnalyzeEpisodeSlide
from src.analyze.graph.analyze_episode_action_distribution import AnalyzeEpisodeActionDistribution
from src.analyze.graph.analyze_lap_time_correlations import AnalyzeLapTimeCorrelations
from src.analyze.graph.analyze_sector_time_correlations import AnalyzeSectorTimeCorrelations
from src.analyze.graph.analyze_lap_time_distribution import AnalyzeLapTimeDistribution
from src.analyze.graph.analyze_complete_lap_percentage import AnalyzeCompleteLapPercentage
from src.analyze.graph.analyze_discount_factors import AnalyzeDiscountFactors

from src.action_space.action_space_filter import ActionSpaceFilter
from src.configuration.config_manager import ConfigManager
from src.episode.episode_filter import EpisodeFilter
from src.graphics.track_graphics import TrackGraphics
from src.log.log import Log
from src.main.version import VERSION
from src.main.view_manager import ViewManager
from src.tracks.tracks import get_all_tracks
from src.ui.menu_bar import MenuBar
from src.ui.please_wait import PleaseWait
from src.ui.status_frame import StatusFrame
from src.analyze.core.episode_selector import EpisodeSelector
from src.ui.view_log_file_info import ViewLogFileInfo
from src.utils.reward_percentiles import RewardPercentiles

DEFAULT_CANVAS_WIDTH = 900
DEFAULT_CANVAS_HEIGHT = 650


class MainApp(tk.Frame):
    def __init__(self, root):
        #
        # Basic frame initialization
        #

        super().__init__(root)

        #
        # First of all, get config manager up and running so we have access to any settings that it manages for us
        #

        self._config_manager = ConfigManager()

        #
        # Initialise all internal settings not related to UI components
        #

        self.tracks = get_all_tracks()
        self.current_track = self.tracks[self._config_manager.get_last_open_track()]

        self.log = None
        self.filtered_episodes = None

        self.episode_filter = EpisodeFilter()
        self.view_manager = ViewManager()
        self.action_space_filter = ActionSpaceFilter()
        self.episode_selector = EpisodeSelector()
        self.sector_filter = ""

        #
        # Create the simple high level UI components (the canvas, control frame and status frame)
        #

        self.status_frame = StatusFrame(self)

        self.track_canvas = tk.Canvas(self, bg="black", width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT)
        self.track_canvas.bind("<Configure>", self.redraw)
        self.track_canvas.bind("<Button-3>", self.right_button_pressed_on_track_canvas)
        self.track_canvas.bind("<Left>", self.left_or_down_key_pressed_on_track_canvas)
        self.track_canvas.bind("<Up>", self.right_or_up_key_pressed_on_track_canvas)
        self.track_canvas.bind("<Right>", self.right_or_up_key_pressed_on_track_canvas)
        self.track_canvas.bind("<Down>", self.left_or_down_key_pressed_on_track_canvas)

        self.track_canvas.bind("<Button-1>", self.left_button_pressed_on_track_canvas)
        self.track_canvas.bind("<B1-Motion>", self.left_button_moved_on_track_canvas)
        self.track_canvas.bind("<ButtonRelease-1>", self.left_button_released_on_track_canvas)
        self.track_canvas.bind("<Double-1>", self.left_button_double_clicked_on_track_canvas)


        self.control_frame = tk.Frame(root)
        self.inner_control_frame = tk.Frame(self.control_frame)

        #
        # Initialise variables to control the right mouse zoom-in feature over a canvas
        #

        self.zoom_start_x = None
        self.zoom_start_y = None
        self.zoom_widget = None

        #
        # Create the graph plotting UI components using the magic of matplotlib
        #

        graph_figure = Figure(figsize=(5, 4), dpi=100)
        matplotlib_canvas = FigureCanvasTkAgg(graph_figure, master=self)
        self.graph_canvas = matplotlib_canvas.get_tk_widget()
        self.graph_canvas.config(width=DEFAULT_CANVAS_WIDTH, height=DEFAULT_CANVAS_HEIGHT)


        #
        # Initialize the "please wait" widget in the middle of each canvas
        #

        self.please_wait_track = PleaseWait(root, self.track_canvas)
        self.please_wait_graph = PleaseWait(root, self.graph_canvas)
        self.please_wait = self.please_wait_track


        #
        # Create the various "analyzers" and let them take control of the contents of the high level UI components
        #

        self.track_graphics = TrackGraphics(self.track_canvas)
        self.current_track.configure_track_graphics(self.track_graphics)

        self.analyze_route = AnalyzeRoute(self.redraw, self.track_graphics, self.inner_control_frame, self.episode_selector, self._config_manager)
        self.analyze_track_heatmap = AnalyzeHeatmap(self.redraw, self.track_graphics, self.inner_control_frame, self.please_wait_track, self._config_manager)
        self.analyze_exit_points = AnalyzeExitPoints(self.redraw, self.track_graphics, self.inner_control_frame)
        self.analyze_race = AnalyzeRace(self.redraw, self.track_graphics, self.inner_control_frame)
        self.analyze_curve_fitting = AnalyzeCurveFitting(self.redraw, self.track_graphics, self.inner_control_frame)
        self.analyze_straight_fitting = AnalyzeStraightFitting(self.redraw, self.track_graphics, self.inner_control_frame)
        self.analyze_training_progress = AnalyzeTrainingProgress(self.redraw, matplotlib_canvas, self.inner_control_frame, self.switch_to_specific_episode_default_analysis)
        self.analyze_quarterly_results = AnalyzeQuarterlyResults(self.redraw, matplotlib_canvas, self.inner_control_frame)
        self.analyze_reward_distribution = AnalyzeRewardDistribution(self.redraw, matplotlib_canvas, self.inner_control_frame)
        self.analyze_common_rewards = AnalyzeCommonRewards(self.redraw, matplotlib_canvas, self.inner_control_frame)
        self.analyze_rewards_per_waypoint = AnalyzeRewardsPerWaypoint(self.redraw, matplotlib_canvas, self.inner_control_frame, self._config_manager)
        self.analyze_episode_speed = AnalyzeEpisodeSpeed(self.redraw, matplotlib_canvas, self.inner_control_frame, self.episode_selector)
        self.analyze_episode_reward = AnalyzeEpisodeReward(self.redraw, matplotlib_canvas, self.inner_control_frame, self.episode_selector, self._config_manager)
        self.analyze_episode_slide = AnalyzeEpisodeSlide(self.redraw, matplotlib_canvas, self.inner_control_frame, self.episode_selector)
        self.analyze_episode_action_distribution = AnalyzeEpisodeActionDistribution(self.redraw, matplotlib_canvas, self.inner_control_frame, self.episode_selector)
        self.analyze_lap_time_correlations = AnalyzeLapTimeCorrelations(self.redraw, matplotlib_canvas, self.inner_control_frame, self.switch_to_specific_episode_default_analysis)
        self.analyze_sector_time_correlations = AnalyzeSectorTimeCorrelations(self.redraw, matplotlib_canvas, self.inner_control_frame, self.switch_to_specific_episode_default_analysis)
        self.analyze_lap_time_distribution = AnalyzeLapTimeDistribution(self.redraw, matplotlib_canvas, self.inner_control_frame)
        self.analyze_complete_lap_percentage = AnalyzeCompleteLapPercentage(self.redraw, matplotlib_canvas, self.inner_control_frame)
        self.analyze_discount_factors = AnalyzeDiscountFactors(self.redraw, matplotlib_canvas, self.inner_control_frame)

        self.all_analyzers = [
            self.analyze_route,
            self.analyze_track_heatmap,
            self.analyze_exit_points,
            self.analyze_race,
            self.analyze_curve_fitting,
            self.analyze_straight_fitting,
            self.analyze_training_progress,
            self.analyze_quarterly_results,
            self.analyze_reward_distribution,
            self.analyze_common_rewards,
            self.analyze_rewards_per_waypoint,
            self.analyze_episode_speed,
            self.analyze_episode_reward,
            self.analyze_episode_slide,
            self.analyze_episode_action_distribution,
            self.analyze_lap_time_correlations,
            self.analyze_sector_time_correlations,
            self.analyze_lap_time_distribution,
            self.analyze_complete_lap_percentage,
            self.analyze_discount_factors
        ]

        for v in self.all_analyzers:
            v.set_track(self.current_track)

        self.analyzer = self.analyze_route
        self.background_analyzer = None
        self.analyzer.take_control()

        if ss.SHOW_SS:
            self.secret_analyzers = ss.get_secret_analyzers(self.redraw, self.track_graphics, self.inner_control_frame)
        else:
            self.secret_analyzers = None


        #
        # Define the layout of the high level UI components
        #

        self.layout_ui_for_track_analyzer()


        #
        # Configure the rest of the application window and then make it appear
        #

        self.master.title("Deep Racer Guru v" + VERSION)
        self.menu_bar = MenuBar(root, self, False, False)


        #
        # All done, so display main window now
        #

        self.already_drawing = False
        self.update()


        #
        # And now lock-in the sizes of the control and status frames so switches between views will be smooth
        #

        self.control_frame.pack_propagate(0)
        self.control_frame.grid_propagate(0)

        self.status_frame.pack_propagate(0)
        self.status_frame.grid_propagate(0)

    def layout_ui_for_track_analyzer(self):
        self.status_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.track_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.control_frame.pack(fill=tk.BOTH, side=tk.RIGHT)
        self.inner_control_frame.pack()
        self.pack(fill=tk.BOTH, expand=True)
        self.please_wait = self.please_wait_track

    def layout_ui_for_graph_analyzer(self):
        self.status_frame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        self.graph_canvas.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.control_frame.pack(fill=tk.BOTH, side=tk.RIGHT)
        self.inner_control_frame.pack()
        self.pack(fill=tk.BOTH, expand=True)
        self.please_wait = self.please_wait_graph

    def menu_callback_switch_track(self, new_track):
        self.log = None
        self.filtered_episodes = None

        self.status_frame.reset()

        self.current_track = new_track
        self._config_manager.set_last_open_track(new_track.get_world_name())

        for v in self.all_analyzers:
            v.set_track(new_track)

        self.episode_selector.set_filtered_episodes(None)
        self.episode_selector.set_all_episodes(None)

        self._reset_analyzer(self.analyzer)
        if self.background_analyzer:
            self._reset_analyzer(self.background_analyzer)

        self.view_manager.zoom_clear()

        self.menu_bar = MenuBar(root, self, False, False)

        self.redraw()

    def _reset_analyzer(self, analyzer):
        analyzer.set_track(self.current_track)
        analyzer.set_filtered_episodes(None)
        analyzer.set_all_episodes(None, None)
        analyzer.set_log_meta(None)
        analyzer.set_evaluation_phases(None)

    def switch_analyzer(self, new_analyzer, new_background_analyzer=None):
        self.analyzer.lost_control()

        if new_background_analyzer:
            assert new_background_analyzer.uses_track_graphics() and new_analyzer.uses_track_graphics()

        if new_analyzer.uses_graph_canvas() and not self.analyzer.uses_graph_canvas():
            self.track_canvas.pack_forget()
            self.layout_ui_for_graph_analyzer()
        elif new_analyzer.uses_track_graphics() and not self.analyzer.uses_track_graphics():
            self.graph_canvas.pack_forget()
            self.layout_ui_for_track_analyzer()

        self.analyzer = new_analyzer
        self.background_analyzer = new_background_analyzer
        self.analyzer.take_control()

        self.redraw()

    def menu_callback_analyze_track_heatmap(self):
        self.switch_analyzer(self.analyze_track_heatmap)

    def menu_callback_analyze_exit_points(self):
        self.switch_analyzer(self.analyze_exit_points)

    def menu_callback_analyze_race(self):
        self.switch_analyzer(self.analyze_race)

    def menu_callback_analyze_curve_fitting(self):
        self.switch_analyzer(self.analyze_curve_fitting)

    def menu_callback_analyze_straight_fitting(self):
        self.switch_analyzer(self.analyze_straight_fitting)

    def menu_callback_analyze_route(self):
        self.switch_analyzer(self.analyze_route)

    def menu_callback_analyze_route_over_heatmap(self):
        self.switch_analyzer(self.analyze_route, self.analyze_track_heatmap)

    def menu_callback_analyze_exit_points_over_heatmap(self):
        self.switch_analyzer(self.analyze_exit_points, self.analyze_track_heatmap)

    def menu_callback_analyze_training_progress(self):
        self.switch_analyzer(self.analyze_training_progress)

    def menu_callback_analyze_quarterly_results(self):
        self.switch_analyzer(self.analyze_quarterly_results)

    def menu_callback_analyze_reward_distribution(self):
        self.switch_analyzer(self.analyze_reward_distribution)

    def menu_callback_analyze_common_rewards(self):
        self.switch_analyzer(self.analyze_common_rewards)

    def menu_callback_analyze_rewards_per_waypoint(self):
        self.switch_analyzer(self.analyze_rewards_per_waypoint)

    def menu_callback_analyze_episode_speed(self):
        self.switch_analyzer(self.analyze_episode_speed)

    def menu_callback_analyze_episode_reward(self):
        self.switch_analyzer(self.analyze_episode_reward)

    def menu_callback_analyze_episode_slide(self):
        self.switch_analyzer(self.analyze_episode_slide)

    def menu_callback_analyze_episode_action_distribution(self):
        self.switch_analyzer(self.analyze_episode_action_distribution)

    def menu_callback_analyze_lap_time_correlations(self):
        self.switch_analyzer(self.analyze_lap_time_correlations)

    def menu_callback_analyze_sector_time_correlations(self):
        self.switch_analyzer(self.analyze_sector_time_correlations)

    def menu_callback_analyze_lap_time_distribution(self):
        self.switch_analyzer(self.analyze_lap_time_distribution)

    def menu_callback_analyze_complete_lap_percentage(self):
        self.switch_analyzer(self.analyze_complete_lap_percentage)

    def menu_callback_analyze_discount_factors(self):
        self.switch_analyzer(self.analyze_discount_factors)

    def menu_callback_switch_directory(self):
        result = tk.filedialog.askdirectory(title="Choose the directory where log files are stored",
                                            mustexist=True,
                                            initialdir=self._config_manager.get_log_directory())
        if result:
            self._config_manager.set_log_directory(result)
            self.menu_bar.refresh()

    def callback_open_this_file(self, file_name):

        redraw_menu_afterwards = not self.log

        self.log = Log(self._config_manager.get_log_directory())
        self.log.load_all(file_name, self.please_wait, self.current_track,
                          self._config_manager.get_calculate_new_reward(),
                          self._config_manager.get_calculate_alternate_discount_factors())

        self.status_frame.change_model_name(self.log.get_log_meta().model_name)
        self.apply_new_action_space()

        reward_percentiles = RewardPercentiles(self.log.get_episodes(), self._config_manager.get_calculate_new_reward())
        for v in self.all_analyzers:
            v.set_all_episodes(self.log.get_episodes(), reward_percentiles)
            v.set_log_meta(self.log.get_log_meta())
            v.set_evaluation_phases(self.log.get_evaluation_phases())

        self.episode_selector.set_all_episodes(self.log.get_episodes())
        self.episode_filter.set_all_episodes(self.log.get_episodes())
        self.reapply_episode_filter()

        # Re-issue control to current analyzer so it has the chance to redraw its controls for the new log
        self.analyzer.take_control()

        if redraw_menu_afterwards:
            self.menu_bar = MenuBar(root, self, True, self.log.get_log_meta().action_space.is_continuous())
            self.update()

    def apply_new_action_space(self):
        self.action_space_filter.set_new_action_space(self.log.get_log_meta().action_space)
        for v in self.all_analyzers:
            v.set_action_space(self.log.get_log_meta().action_space)
            v.set_action_space_filter(self.action_space_filter)

    def reapply_action_space_filter(self):
        for v in self.all_analyzers:
            v.set_action_space_filter(self.action_space_filter)
        self.redraw()

    def reapply_sector_filter(self):
        for v in self.all_analyzers:
            v.set_sector_filter(self.sector_filter)
        self.redraw()

    def reapply_episode_filter(self):
        self.filtered_episodes = self.episode_filter.get_filtered_episodes(self.current_track)

        self.episode_selector.set_filtered_episodes(self.filtered_episodes)

        for v in self.all_analyzers:
            v.set_filtered_episodes(self.filtered_episodes)

        self.status_frame.change_episodes(len(self.log.get_episodes()), len(self.filtered_episodes))

        self.redraw()

    def redraw(self, event=None):
        if not self.already_drawing:   # Nasty workaround to avoid multiple calls due to "please wait"
            self.already_drawing = True
            self.view_manager.redraw(self.current_track, self.track_graphics, self.analyzer, self.background_analyzer, self.episode_filter)
            self.please_wait.stop()
            self.already_drawing = False

    def refresh_analysis_controls(self):
        self.analyzer.take_control()

    def close_file(self):
        self.log = None
        self.filtered_episodes = None
        self.status_frame.reset()
        self.episode_selector.set_filtered_episodes(None)
        self.episode_selector.set_all_episodes(None)
        self._reset_analyzer(self.analyzer)
        if self.background_analyzer:
            self._reset_analyzer(self.background_analyzer)
        self.menu_bar = MenuBar(root, self, False, False)
        self.redraw()

    def right_button_pressed_on_track_canvas(self, event):
        track_point = self.track_graphics.get_real_point_for_widget_location(event.x, event.y)
        self.analyzer.right_button_pressed(track_point)
        self.track_canvas.focus_set() # Set focus so we will now receive keyboard events too

    def left_button_pressed_on_track_canvas(self, event):
        self.zoom_start_x = event.x
        self.zoom_start_y = event.y

    def left_button_moved_on_track_canvas(self, event):
        if self.zoom_widget:
            self.track_canvas.delete(self.zoom_widget)
        self.zoom_widget = self.track_canvas.create_rectangle(
            self.zoom_start_x, self.zoom_start_y, event.x, event.y, outline="blue", width=2, dash=(4, 4))

    def left_button_released_on_track_canvas(self, event):
        if self.zoom_widget:
            self.track_canvas.delete(self.zoom_widget)
            x_diff = abs(self.zoom_start_x - event.x)
            y_diff = abs(self.zoom_start_y - event.y)
            if x_diff > 10 and y_diff > 10:
                self.view_manager.zoom_set(self.track_graphics, self.zoom_start_x, self.zoom_start_y, event.x, event.y)
                self.redraw()

    def left_button_double_clicked_on_track_canvas(self, event):
        self.right_button_pressed_on_track_canvas(event)

    def right_or_up_key_pressed_on_track_canvas(self, event):
        track_point = self.track_graphics.get_real_point_for_widget_location(event.x, event.y)
        self.analyzer.go_forwards(track_point)

    def left_or_down_key_pressed_on_track_canvas(self, event):
        track_point = self.track_graphics.get_real_point_for_widget_location(event.x, event.y)
        self.analyzer.go_backwards(track_point)

    def menu_callback_episodes_all(self):
        self.episode_filter.reset()
        self.reapply_episode_filter()

    def menu_callback_episodes_all_from_start(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_from_start_line(True)
        self.reapply_episode_filter()

    def menu_callback_episodes_complete_laps(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(100)
        self.reapply_episode_filter()

    def menu_callback_episodes_fast_laps(self):
        es = self.log.get_log_meta().episode_stats
        target_steps = round((es.average_steps + es.best_steps) / 2)

        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(100)
        self.episode_filter.set_filter_max_steps(target_steps)
        self.reapply_episode_filter()

    def menu_callback_episodes_complete_laps_from_start(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(100)
        self.episode_filter.set_filter_from_start_line(True)
        self.reapply_episode_filter()

    def menu_callback_episodes_min_percent_10(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(10)
        self.reapply_episode_filter()

    def menu_callback_episodes_min_percent_25(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(25)
        self.reapply_episode_filter()

    def menu_callback_episodes_min_percent_33(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(33)
        self.reapply_episode_filter()

    def menu_callback_episodes_min_percent_50(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_min_percent(50)
        self.reapply_episode_filter()

    def menu_callback_episodes_q1(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_quarters(True, False, False, False)
        self.reapply_episode_filter()

    def menu_callback_episodes_q2(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_quarters(False, True, False, False)
        self.reapply_episode_filter()

    def menu_callback_episodes_q3(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_quarters(False, False, True, False)
        self.reapply_episode_filter()

    def menu_callback_episodes_q4(self):
        self.episode_filter.reset()
        self.episode_filter.set_filter_quarters(False, False, False, True)
        self.reapply_episode_filter()

    def menu_callback_episodes_sector(self, sector):
        self.episode_filter.reset()
        (start, finish) = self.current_track.get_sector_start_and_finish(sector)
        self.episode_filter.set_filter_complete_section_and_time(start, finish, None, None)
        self.reapply_episode_filter()

    def menu_callback_actions_all(self):
        self.action_space_filter.set_filter_all()
        self.reapply_action_space_filter()

    def menu_callback_actions_high_speed(self):
        self.action_space_filter.set_filter_high_speed()
        self.reapply_action_space_filter()

    def menu_callback_actions_medium_speed(self):
        self.action_space_filter.set_filter_medium_speed()
        self.reapply_action_space_filter()

    def menu_callback_actions_low_speed(self):
        self.action_space_filter.set_filter_low_speed()
        self.reapply_action_space_filter()

    def menu_callback_actions_straight(self):
        self.action_space_filter.set_filter_straight()
        self.reapply_action_space_filter()

    def menu_callback_sector_filter(self, sector: str):
        assert len(sector) == 1
        self.sector_filter = sector
        self.reapply_sector_filter()

    def menu_callback_sector_zoom(self, sector: str):
        assert len(sector) == 1
        self.view_manager.zoom_sector(self.current_track, sector)
        self.redraw()

    def menu_callback_zoom_in_out(self):
        self.view_manager.zoom_toggle()
        self.redraw()

    def menu_callback_grid_front(self):
        self.view_manager.set_grid_front()
        self.redraw()

    def menu_callback_grid_back(self):
        self.view_manager.set_grid_back()
        self.redraw()

    def menu_callback_grid_off(self):
        self.view_manager.set_grid_off()
        self.redraw()

    def menu_callback_track_front(self):
        self.view_manager.set_track_front()
        self.redraw()

    def menu_callback_track_back(self):
        self.view_manager.set_track_back()
        self.redraw()

    def menu_callback_track_grey(self):
        self.view_manager.set_track_colour_grey()
        self.redraw()

    def menu_callback_track_blue(self):
        self.view_manager.set_track_colour_blue()
        self.redraw()

    def menu_callback_sectors_on(self):
        self.view_manager.set_sectors_on()
        self.redraw()

    def menu_callback_sectors_off(self):
        self.view_manager.set_sectors_off()
        self.redraw()

    def menu_callback_waypoints_large(self):
        self.view_manager.set_waypoint_sizes_large()
        self.redraw()

    def menu_callback_waypoints_small(self):
        self.view_manager.set_waypoint_sizes_small()
        self.redraw()

    def menu_callback_waypoints_micro(self):
        self.view_manager.set_waypoint_sizes_micro()
        self.redraw()

    def menu_callback_waypoints_off(self):
        self.view_manager.set_waypoints_off()
        self.redraw()

    def menu_callback_waypoint_labels_on(self):
        self.view_manager.set_waypoint_labels_on()
        self.redraw()

    def menu_callback_waypoint_labels_off(self):
        self.view_manager.set_waypoint_labels_off()
        self.redraw()

    def menu_callback_analyze_front(self):
        self.view_manager.set_analyze_front()
        self.redraw()

    def menu_callback_analyze_back(self):
        self.view_manager.set_analyze_back()
        self.redraw()

    def menu_callback_annotations_front(self):
        self.view_manager.set_annotations_front()
        self.redraw()

    def menu_callback_annotations_back(self):
        self.view_manager.set_annotations_back()
        self.redraw()

    def menu_callback_annotations_off(self):
        self.view_manager.set_annotations_off()
        self.redraw()

    def menu_callback_heading_on(self):
        self.analyze_route.set_show_heading(True)

    def menu_callback_heading_off(self):
        self.analyze_route.set_show_heading(False)

    def menu_callback_true_bearing_on(self):
        self.analyze_route.set_show_true_bearing(True)

    def menu_callback_true_bearing_off(self):
        self.analyze_route.set_show_true_bearing(False)

    def menu_callback_camera_vision_on(self):
        self.analyze_route.set_show_camera_vision(True)

    def menu_callback_camera_vision_off(self):
        self.analyze_route.set_show_camera_vision(False)

    def menu_callback_view_log_file_info(self):
        if self.log:
            ViewLogFileInfo(self, self.log)

    def get_log_directory(self):
        return self._config_manager.get_log_directory()

    def get_config_manager(self):
        return self._config_manager

    def switch_to_specific_episode_default_analysis(self, episode_id):
        self.episode_selector.select_specific_episode(episode_id)
        self.switch_analyzer(self.analyze_route)

    def expect_objects(self):
        return self.log is not None and self.log.get_log_meta().race_type == "OBJECT_AVOIDANCE"



root = tk.Tk()
app = MainApp(root)
app.mainloop()