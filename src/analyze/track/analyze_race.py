import threading
import time

import tkinter as tk

from src.analyze.track.track_analyzer import TrackAnalyzer
from src.graphics.track_graphics import TrackGraphics

from src.analyze.core.controls import VideoControls


class AnalyzeRace(TrackAnalyzer):

    def __init__(self, guru_parent_redraw, track_graphics :TrackGraphics, control_frame :tk.Frame):

        super().__init__(guru_parent_redraw, track_graphics, control_frame)

        self._video_controls = VideoControls(self._button_pressed, control_frame)
        self._timer = AnalyzeRace.Timer(self._draw)

        # self._race_episode = self.all_episodes[0]

    def build_control_frame(self, control_frame):
        self._video_controls.add_to_control_frame()

    def _button_pressed(self, button_type):
        if button_type == VideoControls.STOP:
            self._timer.stop()
        elif button_type == VideoControls.RESET:
            self._timer.reset()
        elif button_type == VideoControls.PLAY:
            self._timer.play()

    def redraw(self):
        self._timer.redraw()

    def _draw(self, simulation_time):
        # print("Time = ", round(simulation_time, 1))
        self.track_graphics.remove_cars()

        if self.filtered_episodes:
            episode = self.filtered_episodes[0]
            event_index = min(int(simulation_time * 15), len(episode.events) - 1)
            event = episode.events[event_index]
            self.track_graphics.draw_car(event.x, event.y)
        # print("Draw is done")

    class Timer:
        def __init__(self, redraw_callback: callable):
            self._machine_start_time = 0.0
            self._simulation_start_time = 0.0
            self._simulation_stop_time = 0.0
            self._keep_running = False
            self._thread = None
            self._redraw_callback = redraw_callback

        def stop(self):
            if self._keep_running:
                self._keep_running = False
                # self._thread.join()

        def play(self):
            if not self._keep_running:
                self._keep_running = True
                self._thread = threading.Thread(target=self._run_until_stopped)
                self._thread.start()

        def reset(self):
            if self._simulation_start_time > 0 or self._simulation_stop_time > 0 or self._keep_running:
                self.stop()
                self._simulation_stop_time = 0.0
                self._simulation_start_time = 0.0
                self._redraw_callback(0.0)

        def redraw(self):
            if self._keep_running:
                self._redraw_callback(self.get_current_simulation_time())
            else:
                self._redraw_callback(self._simulation_stop_time)

        def _run_until_stopped(self):
            self._simulation_start_time = self._simulation_stop_time
            self._machine_start_time = time.time()
            while self._keep_running:
                time.sleep(0.05)
                simulation_time = self.get_current_simulation_time()
                self._redraw_callback(simulation_time)
                # print("Looping", round(simulation_time, 2))
            self._simulation_stop_time = self.get_current_simulation_time()
            # print("Thread Ending.....")

        def get_current_simulation_time(self):
            return time.time() - self._machine_start_time + self._simulation_start_time









